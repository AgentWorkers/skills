---
name: fork-manager
description: >
  **使用未合并的 PR（Open PRs）管理分支**  
  - 同步上游代码；  
  - 重新基定（rebase）分支；  
  - 跟踪 PR 的状态；  
  - 维护包含待合并贡献的生产分支。  
  - 支持通过 `--auto-resolve` 标志自动解决冲突（该标志会启动 AI 辅助工具来处理合并冲突）。  
  **适用场景**：  
  - 同步分支时；  
  - 重新基定包含未合并 PR 的分支时；  
  - 构建整合所有未合并 PR 的生产分支时；  
  - 审查已关闭或被拒绝的 PR 时；  
  - 管理未同步到上游的本地修改（本地补丁）。  
  **系统要求**：  
  - 需要 Git 和 GitHub 命令行工具（gh）。
metadata: {"openclaw": {"requires": {"bins": ["git", "gh"]}}}
---
# 分支管理技能

该技能用于管理你在其中提交 Pull Request (PR) 的分支，并在上游合并之前应用这些改进。它支持本地补丁——即使上游的 PR 被关闭或拒绝，这些补丁也会保留在生产分支中。

## 使用场景

- 将分支与上游同步
- 检查未解决的 PR 状态
- 将 PR 分支重新基线到最新的上游代码
- 构建一个生产分支，合并所有未解决的 PR 和本地补丁
- 审查最近关闭/拒绝的 PR，并决定是保留它们还是删除

## 不适用场景

- 一般的 GitHub 查询（问题、PR、任何仓库的 CI 状态）→ 使用 `github` 技能
- 问题分类/优先级排序 → 使用 `issue-prioritizer` 技能
- 在提交 PR 之前审查代码更改 → 使用 `pr-review` 技能
- 从头开始创建新的 PR → 直接使用 `gh pr create`

## 执行模型 — Orchestator + Worker

**此技能绝不能由主代理直接执行。** 必须使用 orchestrator/worker 模型：

### 流程

1. **Orchestrator（主代理）** — 准备环境并创建一个子代理：
   ```
   sessions_spawn(
     task: "<prompt completo com contexto do repo, config, último history>",
     model: "<model adequado>",
     mode: "run"
   )
   ```
2. **Worker（子代理）** — 执行全同步、状态检查、重新基线等操作。读取 SKILL.md 文件，按照流程执行，并记录操作历史。
3. **监控** — Orchestrator 每 4 分钟通过 `sessions_list` / `sessions_history` 检查进度：
   - 如果 Worker 正在运行且有所进展 → 等待
   - 如果 Worker 停止或卡住（连续两次检查都没有新输出） → 异步终止子代理并创建新的 Worker
   - 如果 Worker 完成 → 读取结果并报告给用户
4. **故障处理** — 如果 Worker 出现故障（崩溃、超时、错误）：
   - Orchestrator 检查仓库状态（`git status`、最后一个检查点）
   - 创建一个新的 Worker，包含当前的环境和未完成的部分
   - 最多尝试 2 次失败后，向用户报告故障

### Worker 的环境信息

Orchestrator 需要在 Worker 的提示中提供以下信息：

- SKILL.md 文件的路径（供 Worker 读取和执行）
- 仓库的配置信息（直接提供或通过路径传递）
- 历史记录的最后一个条目（摘要或路径）
- 执行模式（全同步、状态检查、全部重新基线等）
- 是处于定时任务模式还是手动模式
- 用户的任何特定指令

### 为什么使用子代理？

- **弹性**：如果 Worker 出故障，Orchestrator 可以恢复操作
- **减少负担**：此技能处理的数据量很大（145 个以上的 PR 会产生大量输出），子代理可以在不占用主代理资源的情况下处理这些数据
- **支持并行处理**：可以同时为不同的仓库创建多个 Worker

## 定时任务模式

当通过定时任务（自动重复同步）调用此技能时，请遵循以下指南：

1. **跳过交互式提示** — 自动处理不需要用户输入的决策：
   - 重新基线：尝试自动执行，遇到失败时报告
   - 已关闭的 PR：报告结果，但推迟决策（不自动删除或保留）
   - 审计发现：报告结果，但不采取行动
2. **压缩输出** — 使用摘要格式，而不是详细的报告：
   ```
   🍴 Fork Sync Complete — <repo>
   Main: synced N commits (old_sha → new_sha)
   PRs: X open, Y changed state
   - Rebased: A/B clean (C conflicts)
   Production: rebuilt clean | N conflicts
   Notable upstream: [1-3 bullet highlights]
   ```
3. **故障时保存检查点** — 如果重新基线失败或构建过程中出现冲突，将状态保存到 `repos/<name>/checkpoint.json`，以便下一次运行或手动调用时可以继续
4. **时间限制** — 总时间控制在 10 分钟以内。如果需要重新基线 20 个以上的 PR，建议批量推送而不是逐个分支推送

## 配置

配置信息按仓库存储在 `repos/<repo-name>/config.json` 文件中：

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
  "autoResolveConflicts": false,
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

### 自动解决冲突 (`autoResolveConflicts`)

可以通过以下两种方式启用自动冲突解决功能：

1. **调用时的标志**（临时设置）：
   ```
   /fork-manager --auto-resolve
   /fork-manager full-sync --auto-resolve
   ```
2. **持久化的配置**（对该仓库始终生效）：
   ```json
   { "autoResolveConflicts": true }
   ```

| 来源 | 行为 |
|-------|---------------|
| 无（默认） | 报告冲突，但不自动解决。报告中会显示 "⚠️ 冲突需要开发者评估。" |
| `--auto-resolve` 或 `config.autoResolveConflicts: true` | 创建子代理 Opus 来解决冲突。结果会标记为简单冲突/语义冲突/无法解决。 |

**优先级**：即使配置中设置了 `false`，在调用时 `--auto-resolve` 也会启用自动解决功能。如果配置中设置了 `true` 但用户不希望自动解决冲突，可以手动跳过这一步。

**对于 ClawHub 用户**：只需在命令中添加 `--auto-resolve` 即可。无需为每个仓库单独配置。

### `localPatches` 字段

`localPatches` 中的每个条目代表一个在生产分支中维护的本地分支，但该分支在上游没有对应的开放 PR。

| 字段 | 描述 |
|-------|-----------|
| `description` | 补丁的作用 |
| `originalPR` | 原始 PR 的编号（如果补丁是直接创建的，则可选） |
| `closedReason` | PR 被关闭的原因：`rejected`（维护者拒绝）、`superseded`（另一个 PR 部分解决了问题但未完全解决）、`duplicate`（我们自己关闭了 PR）、`wontfix`（上游不会解决） |
| `keepReason` | 为什么需要保留该本地分支 |
| `addedAt` | 该补丁被添加到本地分支的时间 |
| `reviewDate` | 重新评估是否仍需保留该补丁的日期（上游可能已经解决了问题） |

## 执行历史

每个管理的仓库都有一个 `history.md` 文件，用于记录该技能的所有执行记录：

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

### 规则：在执行前读取最新记录

**在任何操作之前**，请读取目标仓库的 `history.md` 文件，并提取 **最后一个条目**（最后的 `---` 标签部分）。这可以提供以下信息：
- 上次执行了哪些操作
- 哪些 PR 出现了问题
- 采取了哪些决策
- 是否有未完成的操作

```bash
# Ler última entrada do history (tudo após o último "---")
tail -n +$(grep -n '^---$' "$SKILL_DIR/repos/<repo-name>/history.md" | tail -1 | cut -d: -f1) "$SKILL_DIR/repos/<repo-name>/history.md"
```

如果文件不存在，请创建该文件并继续执行。

### 规则：执行完成后记录结果

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

**重要提示：** `Full Report` 标签下的内容包含完整的报告，不会被简化。这样确保下一个执行该技能的代理能够获取所有信息，而不仅仅是摘要。

## 分析流程

### 1. 加载配置和历史记录

加载技能目录（包含 SKILL.md 文件）：

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

### 2. 导航到目标仓库

```bash
cd <localPath>
```

### 3. 从远程仓库获取数据

```bash
git fetch <upstreamRemote>
git fetch <originRemote>
```

### 4. 检查主分支的状态

```bash
# Commits que upstream tem e origin/main não tem
git log --oneline <originRemote>/<mainBranch>..<upstreamRemote>/<mainBranch>

# Contar commits atrás
git rev-list --count <originRemote>/<mainBranch>..<upstreamRemote>/<mainBranch>
```

### 5. 通过 GitHub CLI 检查打开的 PR

```bash
# Listar PRs abertos do usuário
gh pr list --state open --author @me --json number,title,headRefName,state

# Verificar status de um PR específico
gh pr view <number> --json state,mergedAt,closedAt,title
```

### 6. 对每个 PR 进行分类

对于配置文件中的每个 PR，需要检查以下状态：

| 状态       | 条件                          | 应采取的行动                                    |
| ------------ | --------------------------------- | --------------------------------------- |
| **open**     | 在 GitHub 上打开的 PR               | 保留该 PR，并检查是否需要重新基线     |
| **merged**   | PR 已经合并                   | 从配置文件中删除该 PR，并删除本地分支 |
| **closed**   | PR 被关闭但未合并              | **执行 `review-closed` 操作**（见下文） |
| **conflict** | 分支与上游代码有冲突 | 需要手动重新基线                   |
| **outdated** | 分支代码落后于上游     | 需要重新基线                          |

### 检查是否需要重新基线的命令：

```bash
git log --oneline <upstreamRemote>/<mainBranch>..<originRemote>/<branch> | wc -l  # commits à frente
git log --oneline <originRemote>/<branch>..<upstreamRemote>/<mainBranch> | wc -l  # commits atrás
```

### 7. 审查最近关闭的 PR (`review-closed`)

当检测到 PR 被关闭但未合并时，**不要自动删除**。启动以下交互式审查流程：

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
| **resolved_upstream** | 上游通过其他方式解决了问题 | 删除该 PR | |
| **superseded_by_ours** | 我们自己关闭了 PR，替换为另一个 PR | 删除该 PR | |
| **rejected_approach** | 维护者不认可该解决方案，但问题仍然存在 | 重新提交 PR，尝试不同的解决方案 | |
| **rejected_need** | 维护者认为问题不存在 | 重新提交 PR，重新评估是否需要解决 | |
| **wontfix** | 上游标记为无法解决 | 重新提交 PR，尝试手动解决 | |

#### 7.3. 向用户展示决策选项

对于每个关闭的 PR，向用户展示以下选项：

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

- **删除**：
```bash
git branch -D <branch> 2>/dev/null
git push <originRemote> --delete <branch> 2>/dev/null
# Mover para notes.droppedPatches no config
```

- **保留本地补丁**：
```bash
# Branch continua existindo, mas sai de openPRs/prBranches
# Entra em localPatches com metadata completa
# Renomear branch de fix/xxx para local/xxx (opcional, para clareza)
```

- **重新提交**：
```bash
# Manter branch, criar novo PR com descrição atualizada
gh pr create --title "<novo titulo>" --body "<nova descrição com contexto>"
# Atualizar config com novo número de PR
```

- **推迟**：
```bash
# Mover para uma seção notes.deferred no config
# Será apresentado novamente no próximo full-sync
```

### 8. 审查打开的 PR (`audit-open`)

主动审查仍然打开的 PR，以检测重复或过时的内容。应在 `full-sync` 操作之后执行此步骤：

#### 8.1. 上游已解决问题

检查上游是否已经解决了我们的 PR 所解决的问题，但未将其合并：

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

- 如果 PR 的差异为空（上游已经合并了所有更改），标记为 `resolved_upstream`。
- 如果差异部分存在（上游只合并了部分更改），标记为 `partially_resolved`，以便进一步审查。

#### 8.2. 外部重复 PR

检查是否有人提交了解决相同问题的新 PR：

```bash
# Buscar PRs abertos no upstream que tocam os mesmos arquivos
gh pr list --state open --repo <repo> --json number,title,headRefName,files --limit 50

# Buscar PRs mergeados recentes que tocam os mesmos arquivos
gh pr list --state merged --repo <repo> --json number,title,mergedAt,files --limit 30 \
  | jq '[.[] | select(.mergedAt >= "<lastSync>")]'
```

对于每个发现的重复 PR，比较以下内容：
- 是否引用相同的问题？
- 是否涉及相同的代码区域？
- 是否采用相同的修复方式？

如果匹配，标记为 `duplicate_external` 或 `superseded_external`。

#### 8.3. 内部重复 PR

检查我们自己的 PR 之间是否存在重复的修复：

```bash
# Coletar files de todos os nossos PRs abertos
for pr in <openPRs>; do
  gh pr view $pr --repo <repo> --json number,files --jq '{number, files: [.files[].path]}'
done

# Cruzar: se dois PRs tocam os mesmos arquivos, são candidatos a duplicata
```

对于每一对重复的 PR，比较以下内容：
- 差异是否相似或互补
- 如果相似：建议关闭较旧的或较不完整的 PR
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

### `status` - 检查当前状态

1. 加载配置文件
2. 从远程仓库获取数据
3. 计算上游的提交次数
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

### `rebase <branch>` - 重新基线指定的分支

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
2. 在上游代码基础上重新基线
3. 使用 `--force-with-lease` 推送更改
4. 报告操作结果

### `resolve-conflicts` - 通过子代理自动解决冲突

> **调用时需要设置 `--auto-resolve` 标志**，或在仓库配置中设置 `autoResolveConflicts: true`。如果没有设置这两个选项，此命令将不会执行，冲突只会被标记为 "⚠️ 冲突需要开发者评估。"`

在 `rebase-all` 执行完成后，**Orchestrator**（主代理）会创建子代理来尝试自动解决每个冲突。

#### 流程

1. `rebase-all` 的 Worker 会返回有冲突的分支列表
2. Orchestrator 会汇总这些冲突，并同时创建最多 5 个子代理来尝试解决它们
3. 随着子代理的完成，会不断创建新的子代理，直到所有冲突都被解决
4. 每个子代理的运行时间为 10 分钟
5. 解决结果会被收集并整合到最终报告中

#### 子代理的提示信息

每个子代理会收到以下提示：

```
Resolve o conflito de rebase da branch <branch> (PR #<number>) no repo <localPath>.

## Contexto
- Upstream: <upstreamRemote>/<mainBranch>
- Branch do PR: <originRemote>/<branch>
- Arquivos em conflito: <lista de arquivos do erro de rebase>

## Passos
1. cd <localPath>
2. git checkout -B <branch> <originRemote>/<branch> --no-track
3. git rebase <upstreamRemote>/<mainBranch>
   → O rebase vai parar com conflito
4. Para cada arquivo em conflito:
   a. Ler o arquivo com os marcadores de conflito (<<<<<<<, =======, >>>>>>>)
   b. Entender o que o upstream mudou (OURS) vs o que o PR mudou (THEIRS)
   c. Resolver preservando a intenção de ambos
   d. git add <arquivo>
5. git rebase --continue
6. Se houver mais conflitos em commits subsequentes, repetir 4-5
7. git push <originRemote> <branch> --force-with-lease

## Regras de resolução
- **Arquivo deletado no upstream + modificado pelo PR:** aceitar a deleção do upstream (nosso PR targeted código que não existe mais). git rm <arquivo> && git rebase --continue
- **Import/formatting conflicts:** mesclar ambos, preservar imports de ambos os lados
- **Lógica alterada em ambos os lados:** preservar a mudança do upstream E encaixar o fix do PR. Se o fix do PR não faz mais sentido com o novo código upstream, reportar como UNRESOLVABLE.
- **NUNCA alterar a lógica do PR** — apenas adaptar ao novo contexto do upstream

## Output
Responda com EXATAMENTE um destes formatos:

RESOLVED|<branch>|trivial|<resumo de 1 linha>
RESOLVED|<branch>|semantic|<resumo de 1 linha>
UNRESOLVABLE|<branch>|<motivo de 1 linha>
```

#### 结果分类

| 结果 | 含义 | 操作 |
|-----------|-------------|------|
| `RESOLVED\|trivial` | 机械性冲突（如导入、格式问题、文件删除）已解决 | ✅ 已成功推送，无需进一步审查 |
| `RESOLVED\|semantic` | 逻辑冲突已解决 | ⚠️ 已成功推送，但需要在报告中标记以便人工审查 |
| `UNRESOLVABLE` | 子代理无法解决冲突 | ❌ 不进行推送，会在报告中标记 |

#### 解决冲突后的处理

对于成功解决的分支：
1. 确认是否已成功推送（`git log --oneline <originRemote>/<branch> -1`）
2. 再次尝试重新基线，确保没有问题
3. 更新配置文件 `notes.conflictBranches`，删除已解决的冲突记录

对于未解决的分支：
1. 在 `notes.conflictBranches` 中记录冲突信息
2. 在报告中包含详细信息

### 与构建流程的集成

执行 `resolve-conflicts` 后，`build-production` 会正常运行。已成功解决冲突的分支现在可以合并到生产分支。如果仍有未解决的冲突（与重新基线的冲突不同），`build-production` 会按常规处理。

### `update-config` - 使用最新的 PR 更新配置

```bash
# Buscar PRs abertos
gh pr list --state open --author @me --repo <repo> --json number,headRefName

# Atualizar o arquivo $SKILL_DIR/repos/<repo-name>/config.json com os PRs atuais
# Usar jq ou editar manualmente o JSON
```

#### 检测重新打开的 PR

比较 GitHub 上的 PR 列表（`gh pr list --state open`）和本地配置文件，检测以下三种情况：

| 情况 | 处理方式 |
|---------|----------|------|
| **新 PR** | 在 GitHub 上存在，但在 `openPRs`、`localPatches` 或 `notes` 中不存在 | 添加到 `openPRs` 和 `prBranches` 中 |
| **重新打开的 PR（已删除）** | 在 GitHub 上显示为打开状态，但在 `notes.closedWithoutMerge` 或 `notes.droppedPatches` 中存在 | **恢复**：将其移回 `openPRs` 和 `prBranches`，并从 `notes` 中删除。执行 `git fetch <originRemote> <branch>`。在报告中标记为 "🔄 Reopened" |
| **本地补丁重新打开的 PR** | 在 GitHub 上显示为打开状态，但在 `localPatches` 中存在（通过 `originalPR` 字段识别） | **提升**：将其从 `localPatches` 移到 `openPRs` 和 `prBranches` 中。在报告中标记为 "🔄 Reopened (was local patch)" |

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

**注意：** 恢复操作是自动进行的（无需用户交互），因为维护者重新打开 PR 表明他们希望继续跟踪该 PR。报告中会列出所有被恢复的 PR。

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
git push <originRemote> <productionBranch> --force-with-lease

# Restaurar arquivos não-commitados
if [ "$STASHED" = "1" ]; then
  git stash pop
fi
```

**在重建生产分支后，如果需要，提醒用户运行他们的构建命令。**

**合并顺序**：先合并打开的 PR（按编号顺序），然后再合并本地补丁。这样可以确保本地补丁应用在最新的代码基础上。

### `audit-open` - 审查重复或过时的 PR

主动审查所有打开的 PR，以检测重复或过时的内容：

1. 对每个打开的 PR，收集涉及的文件
2. **上游已解决问题**：检查上游是否在最后一次同步后修改了相关文件；如果差异为空，标记为已解决
3. **外部重复 PR**：查找上游是否提交了解决相同问题的新 PR
4. **内部重复 PR**：检查我们自己的 PR 之间是否存在重复的修复
5. 向用户展示处理选项：关闭 / 保留 / 合并到现有 PR / 推迟处理
6. 根据用户的选择执行相应的操作
7. 更新配置文件

### `review-closed` - 审查最近关闭的 PR

检查自上次同步以来关闭/合并的 PR，并指导用户做出决策：

1. 在 GitHub 上查找所有相关的 PR
2. 确定哪些 PR 的状态发生了变化（合并或关闭）
3. 对于已合并的 PR，将其移至 `notes.mergedUpstream` 并删除相关分支
4. 对于未合并的 PR，启动交互式审查流程（见步骤 7）
5. 对于每个关闭的 PR，向用户展示处理选项
6. 根据用户的选择执行相应的操作：关闭 / 保留本地补丁 / 重新提交 / 推迟处理
7. 更新配置文件

### `review-patches` - 重新评估现有的本地补丁

对于 `localPatches` 中每个已过期的补丁，检查以下内容：

1. 查看上游是否在最后一次同步后解决了问题
2. 确认补丁是否仍然适用（没有新的冲突）
3. 向用户展示处理选项：保留 / 删除 / 重新提交 / 延长审查期限
4. 更新配置文件

### `full-sync` - 完整同步

1. **Stash** - 如果有未提交的文件，使用 `git stash --include-untracked` 进行暂存
2. **sync** - 更新主分支
   - **同步前**：记录 `OLD_SHA=$(git rev-parse upstream/main)`
   - **同步后**：记录 `NEW_SHA=$(git rev-parse upstream/main)`
3. **`post-sync hooks`** （可选，特定于仓库）- 运行自定义的同步后操作
   - 如果 `OLD_SHA == NEW_SHA`，则跳过此步骤（表示上游没有变化）
   - 配置文件 `config.json` 中的 `postSyncHooks` 部分定义了这些钩子（shell 命令或描述）
   - 例如：检测 CHANGELOG 更新，触发 CI 流程
   - 如果没有配置钩子，则跳过此步骤
4. **update-config` - 更新 PR 列表
5. **`review-closed` - 重新审查最近关闭/合并的 PR（交互式）
6. **audit-open** - 审查重复或过时的 PR（交互式）
7. **`review-patches` - 重新评估过期的本地补丁（交互式）
8. **rebase-all` - 重新基线所有分支（包括 PR 和本地补丁）
9. **resolve-conflicts** （仅当配置中设置了 `--auto-resolve` 或 `autoResolveConflicts: true` 时执行）- 通过子代理自动解决冲突（最多使用 5 个并行子代理，每个子代理的运行时间为 10 分钟）。如果这两个选项都没有设置，则跳过此步骤
10. **build-production** - 重新创建生产分支（包含所有 PR 和本地补丁）
11. **Pop stash** - 使用 `git stash pop` 恢复本地文件
12. 如果需要，提醒用户运行他们的构建命令

**关于执行顺序的说明：** `update-config` 会在 `review-closed` 之前执行，因为这样可以在检测到重新打开的 PR 时自动处理它们。之后，`review-closed` 会处理真正关闭的 PR。最后，`audit-open` 会处理所有打开的 PR。

## 向用户报告结果

执行任何操作后，都会生成报告：

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

#### 🔧 Resolução Automática de Conflitos

_Seção presente apenas quando resolução automática está ativa (`--auto-resolve` ou `autoResolveConflicts: true`). Caso contrário, substituir por:_
> ⚠️ **Conflitos requerem aval do desenvolvedor.** Resolução automática não ativada. Use `--auto-resolve` para tentar resolver automaticamente.

_Quando ativa: Conflitos semânticos (⚠️) foram resolvidos automaticamente mas **requerem revisão humana** — o subagente pode ter interpretado mal a intenção do código._

| #   | Branch        | Tipo      | Resultado          | Detalhe                          |
| --- | ------------- | --------- | ------------------ | -------------------------------- |
| 123 | fix/issue-123 | trivial   | ✅ Resolvido        | Removed deleted test file        |
| 456 | fix/issue-456 | semântico | ⚠️ Resolvido (revisar) | Adapted runner call to new API   |
| 789 | fix/issue-789 | —         | ❌ Não resolvido    | Lógica incompatível com upstream |

#### 🔴 Conflitos persistentes (3+ ciclos)

_Seção presente apenas quando há conflitos que persistem por 3 ou mais execuções consecutivas da skill, mesmo após tentativa de resolução automática. Esses PRs merecem atenção prioritária: considerar dropar, recriar sobre o main atual, ou resolver manualmente._

| #   | Branch        | Ciclos | Arquivo(s)        | Recomendação        |
| --- | ------------- | ------ | ----------------- | ------------------- |
| 789 | fix/bug       | 5      | agent-runner.ts   | 🗑️ Dropar ou recriar |

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

- 推送时始终使用 `--force-with-lease` 而不是 `--force`
- 在执行破坏性操作之前，务必备份数据
- 使用项目的包管理器（如 bun/npm/yarn/pnpm）来执行构建命令
- 每次操作后更新配置文件
- **自动解决冲突（需要 `--auto-resolve` 或 `autoResolveConflicts: true`）**：启用此功能后，`rebase-all` 会创建子代理（Opus，最多同时运行 5 个代理，每个代理运行 10 分钟）来尝试解决冲突。简单的冲突（如导入、格式问题、文件删除）会自动解决并推送。逻辑冲突会解决并标记为 ⚠️，需要人工审查。如果子代理无法解决冲突，会标记为 ❌ 并不推送。**
- **持续存在的冲突（连续 3 次未解决）**：如果冲突在连续 3 次执行后仍然存在（`notes.conflictBranches` 中会有相应的标记），会在报告中专门标记为 "🔴 持续存在的冲突"，并建议用户删除 PR 或重新创建分支。
- **本地补丁始终受到优先处理**：重新基线、构建和报告都会包含打开的 PR 和本地补丁
- **切勿自动删除未合并的 PR**：务必通过 `review-closed` 流程让用户做出决策
- **为本地补丁设置审查期限**：创建本地补丁时，需要设置一个审查期限（默认为 30 天）。在 `full-sync` 过程中，过期的补丁会显示给用户以便重新评估
- **本地补丁的命名规则**：使用 `local/` 前缀来区分本地补丁和 PR 分支（例如：`local/my-custom-fix`）。原始分支可以重命名或保留，但配置文件必须正确记录分支的名称

### ⚠️ 在执行破坏性操作前保护未提交的文件

在任何切换分支或删除/重新创建分支的操作之前（特别是 `build-production` 和 `full-sync`），**务必** 检查并保存未提交的文件：

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

**原因：** 在删除或重新创建生产分支时（`git branch -D <productionBranch>`），工作目录中未提交的文件会永久丢失。这些文件包括：
- 生成的文件（如仪表板、历史记录、配置文件）
- 本地配置文件（如 `serve.ts`、`.env`）
- 积累的数据（如 JSON、SQLite 文件）

**规则：** 如果 `git status --porcelain` 显示有未提交的文件，执行 `git stash --include-untracked` 后再继续操作。操作完成后，使用 `git stash pop` 恢复这些文件。

## 安全提示

该技能执行的操作需要广泛的文件系统和网络访问权限：

- **Git 操作**：从多个远程仓库获取数据、检出代码、合并文件、重新基线和推送文件
- **GitHub CLI**：读取 PR 状态、创建 PR、查询仓库元数据

**在使用该技能之前，请注意：**
- 所有的 Git 推送操作都必须使用 `--force-with-lease`（而不是 `--force`），以防止数据丢失
- 该技能在执行破坏性操作之前会自动暂存未提交的文件

这些功能是分支管理不可或缺的一部分，删除这些功能会导致核心功能失效。

## 使用示例

### 基本同步
用户：`sync my fork of project-x`

代理：
1. 从 `$SKILL_DIR/repos/project-x/config.json` 加载配置文件
2. 运行 `status` 命令检查当前状态
3. 如果主分支落后，运行 `sync` 命令
4. 如果需要重新基线，运行 `rebase-all` 命令
5. 如有必要，更新 `productionBranch`
6. 如果需要，提醒用户重新构建项目
7. 向用户报告操作结果

### 带有自动冲突解决的同步
用户：`/fork-manager --auto-resolve` 或 `/fork-manager full-sync --auto-resolve`

代理：
1. 执行与基本同步相同的操作，但在 `rebase-all` 之后：
2. 对于每个冲突，创建一个解决冲突的子代理（Opus）
3. 收集解决结果（简单冲突 ✅ / 逻辑冲突 ⚠️ / 无法解决 ❌）
4. 使用 `build-production` 命令重新构建分支
5. 报告结果时包含解决冲突的详细信息