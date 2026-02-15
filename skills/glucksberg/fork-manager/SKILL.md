---
name: fork-manager
description: **使用未合并的 PR（Open PRs）管理分支**  
- 同步上游代码；  
- 重新基线（rebase）分支；  
- 跟踪 PR 的状态；  
- 维护包含待合并贡献的生产分支。  

**适用场景**：  
- 在同步分支时；  
- 在重新基线 PR 分支时；  
- 在构建整合所有未合并 PR 的生产分支时；  
- 在审核已关闭/被拒绝的 PR 时；  
- 在管理未同步到上游的本地代码补丁时。  

**所需工具**：  
- Git；  
- GitHub CLI（gh）。
metadata: {"openclaw": {"requires": {"bins": ["git", "gh"]}}}
---

# 分支管理技能

该技能用于管理你在其中提交 Pull Request (PR) 的分支，并在上游合并之前使用这些改进。它支持本地补丁——即使上游的 PR 被关闭或拒绝，这些补丁也会保留在生产分支中。

## 使用场景

- 将分支与上游同步
- 检查未合并的 PR 状态
- 将 PR 分支重新基线到最新的上游版本
- 构建一个生产分支，合并所有未合并的 PR 和本地补丁
- 审查最近关闭/拒绝的 PR，并决定是保留它们还是不保留
- 管理本地补丁（未被提交或上游拒绝的修复）

## 不适用场景

- 一般的 GitHub 查询（问题、PR、任何仓库的 CI 状态）→ 使用 `github` 技能
- 问题分类/排序/优先级设定 → 使用 `issue-prioritizer` 技能
- 在提交 PR 之前审查代码更改 → 使用 `pr-review` 技能
- 从头开始创建新的 PR（而非同步分支）→ 直接使用 `gh pr create`

## Cron 模式

当通过 Cron 作业（自动重复同步）调用时，请遵循以下指南以确保高效执行：

1. **跳过交互式提示** — 自动处理不需要人工输入的决策：
   - 重新基线：尝试自动执行，报告失败情况
   - 已关闭的 PR：报告但推迟决策（不要在没有人工输入的情况下删除或保留）
   - 审计发现：报告但不采取行动
2. **压缩输出** — 使用摘要格式，而不是完整的详细报告：
   ```
   🍴 Fork Sync Complete — <repo>
   Main: synced N commits (old_sha → new_sha)
   PRs: X open, Y changed state
   - Rebased: A/B clean (C conflicts)
   Production: rebuilt clean | N conflicts
   Notable upstream: [1-3 bullet highlights]
   ```
3. **失败时创建检查点** — 如果重新基线失败或生产构建出现冲突，将状态写入 `repos/<name>/checkpoint.json`，以便下一次运行（或手动调用）可以继续
4. **时间预算** — 总时间控制在 <10 分钟内。如果需要重新基线 20 个以上的 PR，建议批量推送而不是逐个分支推送

## 配置

配置按仓库组织在 `repos/<repo-name>/config.json` 文件中：

```
fork-manager/
├── SKILL.md
└── repos/
    ├── project-a/
    │   └── config.json
    └── project-b/
        └── config.json
```

`config.json` 的格式：

```json
{
  "repo": "owner/repo",
  "fork": "your-user/repo",
  "localPath": "/path/to/local/clone",
  "mainBranch": "main",
  "productionBranch": "main-with-all-prs",
  "upstreamRemote": "upstream",
  "forkRemote": "origin",
  "openPRs": [123, 456],
  "prBranches": {
    "123": "fix/issue-123",
    "456": "feat/feature-456"
  },
  "localPatches": {
    "local/my-custom-fix": {
      "description": "Breve descrição do que o patch faz",
      "originalPR": 789,
      "closedReason": "rejected|superseded|duplicate|wontfix",
      "keepReason": "Motivo pelo qual mantemos localmente",
      "addedAt": "2026-02-07T00:00:00Z",
      "reviewDate": "2026-03-07T00:00:00Z"
    }
  },
  "lastSync": "2026-01-28T12:00:00Z",
  "notes": {
    "mergedUpstream": {},
    "closedWithoutMerge": {},
    "droppedPatches": {}
  }
}
```

### `localPatches` 字段

`localPatches` 中的每个条目都是一个本地分支，它被保留在生产分支中，但在上游没有对应的未合并 PR。

| 字段 | 描述 |
|-------|-----------|
| `description` | 补丁的功能 |
| `originalPR` | 原始 PR 的编号（如果直接作为补丁创建，则可选） |
| `closedReason` | PR 被关闭的原因：`rejected`（维护者拒绝）、`superseded`（另一个 PR 部分解决了问题但未完全解决）、`duplicate`（我们自己关闭了）、`wontfix`（上游不会解决） |
| `keepReason` | 我们需要保留它的原因 |
| `addedAt` | 被转换为本地补丁的日期 |
| `reviewDate` | 重新评估是否仍需保留的日期（上游可能已经解决了问题） |

## 执行历史

每个被管理的仓库都有一个 `history.md` 文件，它以只读追加的方式记录了该技能的所有执行记录：

```
fork-manager/
└── repos/
    ├── project-a/
    │   ├── config.json
    │   └── history.md
    └── project-b/
        ├── config.json
        └── history.md
```

### 规则：在开始前阅读最新输出

**在任何操作之前**，阅读目标仓库的 `history.md` 文件并提取**最后一条记录**（最后的 `---` 标签部分）。这可以提供以下信息：
- 上次执行了哪些操作
- 哪些 PR 出现了问题
- 采取了哪些决策
- 是否有未完成的操作

```bash
# Ler última entrada do history (tudo após o último "---")
tail -n +$(grep -n '^---$' "$SKILL_DIR/repos/<repo-name>/history.md" | tail -1 | cut -d: -f1) "$SKILL_DIR/repos/<repo-name>/history.md"
```

如果文件不存在，请创建它并继续正常操作。

### 规则：执行完成后记录输出

**每次执行完成后**，将完整结果追加到 `history.md` 文件中。格式如下：

```markdown
---
## YYYY-MM-DD HH:MM UTC | <comando>
**Operator:** <claude-code | openclaw-agent | manual>

### Summary
- Main: <status do sync>
- PRs: <X open, Y merged, Z closed, W reopened>
- Local Patches: <N total, M com review vencida>
- Production: <rebuilt OK | not rebuilt | build failed>

### Actions Taken
- <lista de ações executadas, ex: "Synced main (was 12 commits behind)">
- <"Rebased 21/21 branches clean">
- <"PR #999 closed → kept as local patch local/my-fix">
- <"PR #777 reopened → restored to openPRs (was in droppedPatches)">

### Pending
- <ações que ficaram pendentes, ex: "PR #456 has conflicts — needs manual resolution">
- <"3 local patches with expired reviewDate — run review-patches">

### Full Report
<o relatório completo que seria mostrado ao usuário, colado aqui na íntegra>
```

**重要提示：**`Full Report` 标签部分包含完整的报告，没有缩写。这确保下一个读取历史记录的代理能够获取所有信息，而不仅仅是摘要。

## 分析流程

### 1. 加载配置和历史记录

加载技能目录（`SKILL.md` 所在的位置）：

```bash
# SKILL_DIR is the directory containing this SKILL.md
# Resolve it relative to the agent's workspace or skill install path
SKILL_DIR="<path-to-fork-manager-skill>"

# Load config for the target repo
cat "$SKILL_DIR/repos/<repo-name>/config.json"

# Ler último output do history para contexto
HISTORY="$SKILL_DIR/repos/<repo-name>/history.md"
if [ -f "$HISTORY" ]; then
  # Extrair última entrada (após último ---)
  LAST_SEP=$(grep -n '^---$' "$HISTORY" | tail -1 | cut -d: -f1)
  if [ -n "$LAST_SEP" ]; then
    tail -n +"$LAST_SEP" "$HISTORY"
  fi
fi
```

### 2. 导航到仓库

```bash
cd <localPath>
```

### 3. 从两个远程仓库获取数据

```bash
git fetch <upstreamRemote>
git fetch <originRemote>
```

### 4. 分析主分支的状态

```bash
# Commits que upstream tem e origin/main não tem
git log --oneline <originRemote>/<mainBranch>..<upstreamRemote>/<mainBranch>

# Contar commits atrás
git rev-list --count <originRemote>/<mainBranch>..<upstreamRemote>/<mainBranch>
```

### 5. 通过 GitHub CLI 查看未合并的 PR

```bash
# Listar PRs abertos do usuário
gh pr list --state open --author @me --json number,title,headRefName,state

# Verificar status de um PR específico
gh pr view <number> --json state,mergedAt,closedAt,title
```

### 6. 对每个 PR 进行分类

对于配置文件中的每个 PR，检查以下状态：

| 状态       | 条件                          | 操作                                    |
| ------------ | --------------------------------- | --------------------------------------- |
| **open**     | 在 GitHub 上未合并的 PR               | 保留，并检查是否需要重新基线     |
| **merged**   | PR 已经合并                   | 从配置文件中删除，删除本地分支 |
| **closed**   | PR 被关闭但未合并              | **执行 `review-closed`**（见下文） |
| **conflict** | 分支与上游有冲突 | 需要手动重新基线                   |
| **outdated** | 分支落后于上游     | 需要重新基线                          |

检查分支是否需要重新基线的命令：

```bash
git log --oneline <upstreamRemote>/<mainBranch>..<originRemote>/<branch> | wc -l  # commits à frente
git log --oneline <originRemote>/<branch>..<upstreamRemote>/<mainBranch> | wc -l  # commits atrás
```

### 7. 审查最近关闭的 PR (`review-closed`)

当检测到 PR 被关闭但未合并时，**不要自动删除**。启动交互式审查流程：

#### 7.1. 收集关闭原因

```bash
# Buscar comentários e motivo do fechamento
gh pr view <number> --repo <repo> --json title,closedAt,state,comments,labels

# Verificar se upstream resolveu o problema de outra forma
# (procurar PRs mergeados recentes que toquem os mesmos arquivos)
gh pr list --state merged --repo <repo> --json number,title,mergedAt --limit 30
```

#### 7.2. 分类关闭原因

| 类别 | 描述 | 标准操作 |
|-----------|-----------|-------------|
| **resolved_upstream** | 上游通过其他方式解决了问题 | `drop` — 不再需要这个 PR |
| **superseded_by_ours** | 我们自己关闭了它，替换为另一个 PR | `drop` — 替代 PR 已经在 `openPRs` 中 |
| **rejected_approach** | 维护者不喜欢这种解决方案，但问题仍然存在 | `review` — 考虑以不同的方式重新提交 |
| **rejected_need** | 维护者认为这不是问题 | `review` — 评估是否需要在本地解决 |
| **wontfix** | 上游标记为不会解决 | `review` — 可能适合作为本地补丁 |

#### 7.3. 向用户展示以供决策

对于每个关闭的 PR，展示相关信息：

```markdown
### PR #<number> — <title>
- **Fechado em:** <data>
- **Motivo:** <categoria>
- **Comentários do mantenedor:** <resumo>
- **O fix ainda é relevante pra nós?** Análise: <o que o patch faz e se upstream resolve>

**Opções:**
1. 🗑️ **Drop** — remover completamente (branch local + remote)
2. 📌 **Keep as local patch** — mover para `localPatches`, manter na production branch
3. 🔄 **Resubmit** — retrabalhar e abrir novo PR com abordagem diferente
4. ⏸️ **Defer** — manter no limbo por agora, revisitar depois
```

#### 7.4. 执行决策

**删除：**
```bash
git branch -D <branch> 2>/dev/null
git push <originRemote> --delete <branch> 2>/dev/null
# Mover para notes.droppedPatches no config
```

**保留为本地补丁：**
```bash
# Branch continua existindo, mas sai de openPRs/prBranches
# Entra em localPatches com metadata completa
# Renomear branch de fix/xxx para local/xxx (opcional, para clareza)
```

**重新提交：**
```bash
# Manter branch, criar novo PR com descrição atualizada
gh pr create --title "<novo titulo>" --body "<nova descrição com contexto>"
# Atualizar config com novo número de PR
```

**推迟：**
```bash
# Mover para uma seção notes.deferred no config
# Será apresentado novamente no próximo full-sync
```

### 8. 审查未合并的 PR (`audit-open`)

主动审查**仍在打开的 PR**，以检测重复和过时的情况。该步骤应在 `update-config` 之后执行：

#### 8.1. 上游已解决

检查上游是否已经解决了我们的 PR 所解决的问题，但尚未合并：

```bash
# Para cada PR aberto, buscar os arquivos que ele toca
gh pr view <number> --repo <repo> --json files --jq '[.files[].path]'

# Verificar se upstream alterou esses mesmos arquivos recentemente
# (commits no upstream/main que não estão no nosso PR branch)
git log --oneline upstream/main --since="<lastSync>" -- <files>

# Se houve mudanças upstream nos mesmos arquivos, verificar se o diff
# do nosso PR ainda faz diferença (pode ter sido absorvido)
git diff upstream/main..origin/<branch> -- <files>
```

- 如果 PR 的差异为空（上游已经合并了更改）：标记为 `resolved_upstream`。
- 如果差异部分存在（上游只解决了一部分）：标记为 `partially_resolved`，以便进一步审查。

#### 8.2. 外部重复

检查是否有人打开了另一个解决相同问题的 PR：

```bash
# Buscar PRs abertos no upstream que tocam os mesmos arquivos
gh pr list --state open --repo <repo> --json number,title,headRefName,files --limit 50

# Buscar PRs mergeados recentes que tocam os mesmos arquivos
gh pr list --state merged --repo <repo> --json number,title,mergedAt,files --limit 30 \
  | jq '[.[] | select(.mergedAt >= "<lastSync>")]'
```

对于每个涉及相同文件的 PR，比较：
- 是否引用了同一个问题？
- 是否修改了相同的代码区域？
- 是否使用了相同的修复方法？

如果匹配度很高：标记为 `duplicate_external` 或 `superseded_external`。

#### 8.3. 自身重复

检测我们自己的未合并 PR 之间的重复情况：

```bash
# Coletar files de todos os nossos PRs abertos
for pr in <openPRs>; do
  gh pr view $pr --repo <repo> --json number,files --jq '{number, files: [.files[].path]}'
done

# Cruzar: se dois PRs tocam os mesmos arquivos, são candidatos a duplicata
```

对于每一对有文件重叠的 PR：
- 检查差异是相似的还是互补的
- 如果相似：建议关闭较旧或较不干净的 PR
- 如果互补：仅记录相关信息

#### 8.4. 显示结果

```markdown
### Audit de PRs Abertos

#### Possivelmente resolvidos upstream
| # | Titulo | Arquivos em comum | Status |
|---|--------|-------------------|--------|
| 123 | fix(foo): bar | foo.ts (changed upstream 3 days ago) | ⚠️ Verificar |

#### Possíveis duplicatas externas
| Nosso PR | PR externo | Overlap | Recomendação |
|----------|-----------|---------|--------------|
| #123 | #456 (@user) | foo.ts, bar.ts | ⚠️ Mesmo issue, verificar |

#### Self-duplicates (nossos PRs que se sobrepõem)
| PR A | PR B | Arquivos em comum | Recomendação |
|------|------|-------------------|--------------|
| #6471 | #8386 | skills/refresh.ts | 🗑️ Fechar #6471 (duplicata) |

**Opções por PR flagged:**
1. 🗑️ **Close** — fechar o PR no upstream e drop
2. ✅ **Keep** — falso positivo, manter aberto
3. 🔄 **Merge into** — combinar com outro PR
4. ⏸️ **Defer** — revisitar depois
```

## 代理命令

### `status` - 查看当前状态

1. 加载配置
2. 从远程仓库获取数据
3. 计算与上游相比的提交次数
4. 列出 PR 及其状态
5. 向用户报告结果

### `sync` - 将主分支与上游同步

```bash
cd <localPath>
git fetch <upstreamRemote>
git checkout <mainBranch>
git merge <upstreamRemote>/<mainBranch>
git push <originRemote> <mainBranch>
```

### `rebase <branch>` - 重新基线特定分支

```bash
git checkout <branch>
git fetch <upstreamRemote>
git rebase <upstreamRemote>/<mainBranch>
# Se conflito: resolver e git rebase --continue
git push <originRemote> <branch> --force-with-lease
```

### `rebase-all` - 重新基线所有 PR 分支

对于 `prBranches` 中的每个分支：
1. 检出该分支
2. 在上游/主分支上重新基线
3. 使用 `--force-with-lease` 推送
4. 报告成功/失败情况

### `update-config` - 使用当前的 PR 更新配置

```bash
# Buscar PRs abertos
gh pr list --state open --author @me --repo <repo> --json number,headRefName

# Atualizar o arquivo $SKILL_DIR/repos/<repo-name>/config.json com os PRs atuais
# Usar jq ou editar manualmente o JSON
```

#### 检测重新打开的 PR

将 GitHub 的 PR 列表（`gh pr list --state open`）与本地配置进行比较，以检测以下三种情况：

| 情况 | 条件 | 操作 |
|---------|----------|------|
| **新 PR** | 在 GitHub 上存在，但在 `openPRs`、`localPatches` 或 `notes` 中都不存在 | 将其添加到 `openPRs` 和 `prBranches` 中 |
| **重新打开的 PR (已删除)** | 在 GitHub 上显示为 open 状态，但在 `notes.closedWithoutMerge` 或 `notes.droppedPatches` 中存在 | **恢复**：将其移回 `openPRs` 和 `prBranches`，并从 `notes` 中删除。执行 `git fetch <originRemote> <branch>`。在报告中记录为 "🔄 Reopened" |
| **重新打开的 PR (本地补丁)** | 在 GitHub 上显示为 open 状态，但在 `localPatches` 中存在（通过 `originalPR` 字段识别） | **提升**：将其从 `localPatches` 移到 `openPRs` 和 `prBranches`。在报告中记录为 "🔄 Reopened (was local patch)" |

**实现细节：**

```bash
# Para cada PR open no GitHub que NÃO está em openPRs:
# 1. Checar se o número está em notes.closedWithoutMerge ou notes.droppedPatches
#    → Se sim: PR foi reaberto. Restaurar automaticamente.
# 2. Checar se algum entry em localPatches tem originalPR == número
#    → Se sim: PR foi reaberto. Promover de volta a openPRs.
# 3. Se não encontrado em lugar nenhum: PR genuinamente novo.

# Restaurar branch se foi deletada:
git fetch <originRemote> <branch> 2>/dev/null || git fetch <originRemote> pull/<number>/head:<branch>
```

**注意：**恢复操作是自动执行的（无需人工干预），因为维护者重新打开 PR 表明它应该重新被跟踪。报告总是会列出所有被恢复的 PR，以便用户查看。

### `build-production` - 创建包含所有 PR 和本地补丁的生产分支

```bash
cd <localPath>
git fetch <upstreamRemote>
git fetch <originRemote>

# ⚠️ SEMPRE preservar arquivos não-commitados antes de trocar de branch
if [ -n "$(git status --porcelain)" ]; then
  git stash push --include-untracked -m "fork-manager: pre-build-production $(date -u +%Y%m%dT%H%M%S)"
  STASHED=1
fi

# Deletar branch antiga se existir
git branch -D <productionBranch> 2>/dev/null || true

# Criar nova branch a partir do upstream
git checkout -b <productionBranch> <upstreamRemote>/<mainBranch>

# 1. Mergear cada PR branch (contribuições upstream pendentes)
for branch in <prBranches>; do
  git merge <originRemote>/$branch -m "Merge PR #<number>: <title>"
  # Se conflito, resolver
done

# 2. Mergear cada local patch (fixes mantidos localmente)
for branch in <localPatches>; do
  git merge <originRemote>/$branch -m "Merge local patch: <description>"
  # Se conflito, resolver
done

# Push
git push <originRemote> <productionBranch> --force

# Restaurar arquivos não-commitados
if [ "$STASHED" = "1" ]; then
  git stash pop
fi
```

**在重建生产分支后，如果需要，提醒用户运行他们的项目构建命令。**

**合并顺序：** 先合并未合并的 PR（按编号升序），然后再合并本地补丁。这样可以确保本地补丁应用于最完整的基础代码上。

### `audit-open` - 审查未合并的 PR 以检测重复和过时的情况

主动审查所有打开的 PR（如第 8 节所述）：

1. 对于每个打开的 PR，收集涉及的文件
2. **上游已解决**：检查上游是否自上次同步后修改了相同文件；如果 PR 的差异为空，标记为 `resolved_upstream`。
3. **外部重复**：查找上游的 PR（open 状态且最近已合并），这些 PR 修改了相同的文件。
4. **自身重复**：检查我们自己的未合并 PR 之间的文件重叠情况。
5. 向用户展示发现的结果，并提供关闭/保留/合并到现有 PR/推迟的选项。
6. 执行相应的操作。
7. 更新配置。

### `review-closed` - 审查最近关闭的 PR

检测自上次同步以来被关闭/合并的 PR，并指导用户做出决策：

1. 在 GitHub 中查找所有配置文件中的 PR
2. 识别状态发生变化的 PR（已合并或关闭的 PR）。
3. 对于已合并的 PR：将其移至 `notes.mergedUpstream`，并删除相关分支。
4. 对于未合并的 PR：启动交互式审查流程（见第 7 节）。
5. 对于每个关闭的 PR，向用户展示相关信息并提供选项。
6. 执行决策：删除/保留为本地补丁/重新提交/推迟。
7. 更新配置。

### `review-patches` - 重新评估现有的本地补丁

对于 `localPatches` 中每个 `reviewDate` 已过期的条目：
1. 检查上游是否在最后一次审查后解决了问题。
2. 检查补丁是否仍然适用（没有冲突）。
3. 向用户展示选项：保留/删除/重新提交/延长 reviewDate。
4. 更新配置。

### `full-sync` - 完整同步

1. **Stash** - 如果有未提交的文件，使用 `git stash --include-untracked` 进行存储。
2. **sync** - 更新主分支。
3. **update-config** - 更新 PR 列表。
4. **`review-closed` - 审查最近关闭/合并的 PR（交互式）。
5. **`audit-open` - 审查未合并的 PR 以检测重复和过时的情况（交互式）。
6. **`review-patches` - 重新评估过期的本地补丁（交互式）。
7. **rebase-all** - 重新基线所有分支（PR 和本地补丁）。
8. **build-production** - 重新创建生产分支（包含 PR 和本地补丁）。
9. **Pop stash** - 使用 `git stash pop` 恢复本地文件。
10. 如果需要，提醒用户运行他们的项目构建命令。

**关于顺序的说明：**`update-config` 在 `review-closed` 之前执行，因为这时会检测到并自动恢复重新打开的 PR。之后，`review-closed` 会处理真正关闭的 PR。最后，`audit-open` 会在配置列表更新后执行。

## 向用户报告

执行任何操作后，生成报告：

```markdown
## 🍴 Fork Status: <repo>

### Upstream Sync

- **Main branch:** X commits behind upstream
- **Last sync:** <date>

### Open PRs (Y total)

| #   | Branch        | Status           | Action Needed     |
| --- | ------------- | ---------------- | ----------------- |
| 123 | fix/issue-123 | ✅ Up to date    | None              |
| 456 | feat/feature  | ⚠️ Needs rebase  | Run rebase        |
| 789 | fix/bug       | ❌ Has conflicts | Manual resolution |

### Local Patches (Z total)

| Branch             | Original PR | Motivo          | Review em  |
| ------------------ | ----------- | --------------- | ---------- |
| local/my-fix       | #321        | rejected_need   | 2026-03-07 |
| local/custom-tweak | —           | wontfix         | 2026-04-01 |

### Audit de PRs Abertos

| #   | Título           | Flag                | Detalhe                          |
| --- | ---------------- | ------------------- | -------------------------------- |
| 123 | fix(foo): bar    | ⚠️ resolved_upstream | upstream changed foo.ts 3d ago   |
| 456 | fix(baz): qux    | ⚠️ duplicate_external | similar to #789 by @user         |
| 111 | fix(a): b        | ⚠️ self_duplicate    | overlaps with our #222           |

### PRs Reabertos (restaurados automaticamente)

| #   | Título           | Origem              | Ação                    |
| --- | ---------------- | ------------------- | ----------------------- |
| 777 | fix(foo): bar    | notes.droppedPatches | 🔄 Restored to openPRs |
| 888 | feat(baz): qux   | localPatches         | 🔄 Promoted to openPRs |

_Seção presente apenas quando há PRs reabertos no ciclo atual._

### PRs Recém-Fechados (aguardando decisão)

| #   | Título           | Fechado em | Motivo              | Recomendação     |
| --- | ---------------- | ---------- | ------------------- | ---------------- |
| 999 | fix(foo): bar    | 2026-02-05 | resolved_upstream   | 🗑️ Drop          |
| 888 | feat(baz): qux   | 2026-02-06 | rejected_need       | 📌 Local patch   |

### Production Branch

- **Branch:** main-with-all-prs
- **Contains:** PRs #123, #456 + Local patches: local/my-fix, local/custom-tweak
- **Status:** ✅ Up to date / ⚠️ Needs rebuild

### Recommended Actions

1. ...
2. ...
```

## 重要提示

- 在推送时始终使用 `--force-with-lease` 而不是 `--force`。
- 在执行破坏性操作之前始终进行备份。
- 使用项目的包管理器（如 bun/npm/yarn/pnpm）来运行构建命令。
- 每次操作后更新配置文件。
- **本地补丁非常重要**：重新基线、构建和报告应包括所有未合并的 PR 和本地补丁。
- **永远不要自动删除未合并的 PR**。始终通过 `review-closed` 流程让用户做出决策。
- **为本地补丁设置 review 日期**：创建本地补丁时，指定一个 review 日期（默认为 30 天）。在 `full-sync` 过程中，会向用户展示过期的补丁以供重新评估。
- **本地补丁的命名规则**：使用前缀 `local/` 以区分它们和 PR 分支（例如：`local/my-custom-fix`）。原始分支可以重命名或保留——关键是配置文件能够正确跟踪分支。

### ⚠️ 在执行破坏性操作前保护未提交的文件

在任何更改分支或删除/重新创建分支的操作之前（特别是 `build-production` 和 `full-sync`），**务必** 检查并保存未提交的文件、未跟踪的文件和已暂存的文件：

```bash
cd <localPath>

# 1. Checar se há arquivos em risco
git status --porcelain

# 2. Se houver arquivos modificados/untracked, fazer stash com untracked
git stash push --include-untracked -m "fork-manager: pre-sync stash $(date -u +%Y%m%dT%H%M%S)"

# 3. Executar a operação (rebase, checkout, merge, etc.)
# ...

# 4. Após concluir, restaurar o stash
git stash pop
```

**为什么？** 在删除和重新创建生产分支（`git branch -D <productionBranch>`）时，仅存在于工作目录中的未提交文件会永久丢失。这些文件包括：
- 生成的文件（仪表板、历史记录、状态文件）
- 本地配置文件（serve.ts、.env）
- 积累的数据（JSON、SQLite）

**规则：** 如果 `git status --porcelain` 显示任何错误信息，请在执行操作之前使用 `git stash --include-untracked`。操作完成后使用 `git stash pop` 恢复这些文件。

## 安全提示

此技能的设计需要广泛的文件系统和网络访问权限：

- **Git 操作**：从多个远程仓库和分支获取、检出、合并、重新基线和推送文件。
- **GitHub CLI**：读取 PR 状态、创建 PR、查询仓库元数据。

**在使用此技能之前：**
- 所有的 git 推送操作都使用 `--force-with-lease`（而不是 `--force`），以防止数据丢失。
- 该技能总是在执行破坏性分支操作之前将未提交的文件存储起来。

这些功能是分支管理的一部分，无法删除，否则会导致核心功能失效。

## 使用示例

用户：“同步我的 project-x 分支”

代理：
1. 从 `$SKILL_DIR/repos/project-x/config.json` 加载配置文件。
2. 运行 `status` 以评估当前状态。
3. 如果主分支落后于上游，运行 `sync`。
4. 如果需要重新基线 PR，运行 `rebase-all`。
5. 如有需要，更新 `productionBranch`。
6. 如果需要，提醒用户重新构建项目。
7. 向用户报告结果。