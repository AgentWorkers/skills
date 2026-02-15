---
name: progress-sync
description: **多系统同步的全面进度同步工具（task.md → living docs → GitHub/JIRA/ADO）**  
适用于在多个系统之间同步进度、创建缺失的外部问题，或理解 `/sw:sync-progress` 命令的用法。当缺少外部链接时，该工具会自动创建相应的缺失问题。
---

# 进度同步专家

我是SpecWeave中负责全面进度同步的专家。我可以帮助您理解并使用`/sw:sync-progress`命令来实现端到端的进度同步。

---

## ⚠️ 重要提示：自动创建问题是必须的

**当执行`/sw:sync-progress`命令且没有外部问题时，必须使用Skill工具自动创建问题。**

该命令必须调用以下操作：
- 对于GitHub：`Skill({ skill: "sw-github:create", args: "<increment-id>" })`
- 对于JIRA：`Skill({ skill: "sw-jira:create", args: "<increment-id>" })`
- 对于Azure DevOps：`Skill({ skill: "sw-ado:create", args: "<increment-id>" })`

**不要仅仅报告“没有关联的问题”——实际上需要创建这些问题。**

---

## 什么是 `/sw:sync-progress`？

**这是一个真正的“一键式”工具，可以跨所有系统同步进度：**

```
tasks.md → spec.md ACs → living docs → AUTO-CREATE external issues → sync external tools (GitHub/JIRA/ADO)
```

**一个命令就能完成所有操作——包括创建缺失的外部问题！**
```bash
/sw:sync-progress
```

**再也不会出现“没有关联的GitHub问题”的错误了！** 这个命令会自动创建缺失的问题。

### ✅ 已归档的增量处理方式

**对于已归档/完成的增量，此命令会始终创建问题以进行历史记录：**

| 情况 | 操作 |
|-----------|--------|
| 问题已存在 | ✅ 同步最终状态并关闭/转换 |
| 无关联问题 | ✅ 自动创建问题并立即关闭（进行历史记录） |

**为什么？** 历史记录非常重要！已完成的工作应该有外部问题，以便：
- 团队成员能够查看
- 进行Sprint回顾
- 生成发布说明
- 保留审计追踪记录

**对于所有增量（无论是活跃的还是已完成的）**：如果缺少问题，都会自动创建问题（遵循“一键式”原则）。

---

## 何时使用此命令

### ✅ 在以下情况下使用 `/sw:sync-progress`：

1. **首次同步（尚未创建外部问题）**：刚刚创建了增量，想要同步 → 会自动创建GitHub/JIRA/ADO问题！
2. **完成任务后**：您已在`tasks.md`中标记任务为已完成，并希望同步到所有系统
3. **在关闭增量之前**：在执行`/sw:done`之前进行最终同步，以确保所有系统数据一致
4. **检查进度**：希望用最新进度更新状态行和外部工具
5. **批量完成任务后**：一次性同步多个任务
6. **手动触发同步**：如果钩子未触发或您希望强制同步
7. **出现“没有关联的GitHub问题”的错误**：此命令会通过自动创建问题来解决这个问题！

### ❌ 何时不要使用：

1. **仅想同步ACs**：请使用`/sw:sync-acs`（更快，更精准）
2. **仅想同步文档**：请使用`/sw:sync-specs`
3. **仅想同步GitHub（问题已经存在）**：请使用`/sw-github:sync`
4. **增量尚未开始**：还没有任务需要同步
5. **不想自动创建问题**：请使用`--no-create`标志或手动命令

---

## 工作原理

**多阶段协调**：

```
Phase 1: Tasks → ACs (spec.md)
  └─ Reads completed tasks from tasks.md
  └─ Finds linked ACs (via "Satisfies ACs" field)
  └─ Marks ACs as complete in spec.md: [ ] → [x]
  └─ Updates metadata.json with AC count

Phase 2: Spec → Living Docs (User Stories)
  └─ Syncs spec.md to living docs structure
  └─ Updates user story completion status
  └─ Generates/updates feature ID if needed

Phase 3: AUTO-CREATE External Issues (NEW!)
  ├─ Checks each configured external tool for linked issues
  ├─ If no issue exists → AUTO-CREATE via /sw-github:create, /sw-jira:create, /sw-ado:create
  ├─ Respects permissions (canUpsertInternalItems, canUpdateExternalItems)
  └─ Skip with --no-create flag if needed

Phase 4: Sync to External Tools (Two-Way)
  ├─ GitHub: Two-way sync (push progress, pull team changes)
  ├─ JIRA: Two-way sync (push tasks, pull status)
  └─ Azure DevOps: Two-way sync (push comments, pull updates)

Phase 5: Status Line Cache
  └─ Updates status line with latest completion %
```

---

## 使用示例

### 示例1：首次同步（尚未创建GitHub问题） ⭐

**场景**：刚刚创建了增量，完成了任务，但尚未创建GitHub问题。现在想要同步。

```bash
# Single command does EVERYTHING
/sw:sync-progress
```

**操作过程**：
1. ✅ 在`spec.md`中标记任务为已完成
2. ✅ 用户故事同步到实时文档
3. ✅ 自动创建GitHub问题（#123）
4. ✅ GitHub问题与任务进度同步
5. ✅ 状态行显示完成百分比%

**再也不会出现“没有关联的GitHub问题”的错误了！**

### 示例2：完成任务后（问题已存在）

**场景**：您完成了5个任务，并在`tasks.md`中进行了标记。GitHub问题已经存在。

```bash
# Single command syncs everything
/sw:sync-progress
```

**操作过程**：
1. ✅ 5个任务 → 在`spec.md`中标记为已完成
2. ✅ 2个用户故事在实时文档中标记为已完成
3. ✅ 检测到GitHub问题#123，并将其与进度同步
4. ✅ Epic问题清单更新（5/37个任务已完成）
5. ✅ 状态行显示完成百分比从68%更新为85%

### 示例3：在关闭增量之前

**场景**：所有37个任务都已完成，准备关闭增量。确保进行最终同步。

```bash
# Final sync before closure
/sw:sync-progress 0053

# Then close increment
/sw:done 0053
```

**为什么重要**：`/sw:done`用于验证完成情况。最终同步可以确保：
- 所有ACs都被标记为已完成
- 所有用户故事都已同步
- 所有GitHub问题都已关闭
- 状态行显示100%完成

### 示例4：干运行（预览模式）

**场景**：在执行之前想查看同步结果。

```bash
# Preview mode
/sw:sync-progress 0053 --dry-run
```

**输出结果**：
```
🔍 DRY-RUN MODE (No changes made)

Would sync:
   • 37 completed tasks → 70 ACs in spec.md
   • spec.md → 6 user stories in living docs
   • Living docs → 6 GitHub issues (would close completed)
   • Status line cache (would update completion %)

Run without --dry-run to execute sync.
```

### 示例5：仅本地同步（不涉及外部工具）

**场景**：正在离线工作，暂时不想同步到GitHub/JIRA。

```bash
# Skip external tools
/sw:sync-progress 0053 --no-github --no-jira --no-ado
```

**同步内容**：
- ✅ 任务 → ACs（在`spec.md`中）
- ✅ 规格文档 → 实时文档
- ❌ 不同步外部工具
- ✅ 状态行缓存

---

## 标志参数

| 标志 | 用途 | 示例 |
|------|---------|---------|
| `--dry-run` | 不执行同步，仅预览 | `--dry-run` |
| `--no-create` | 跳过缺失问题的自动创建 | `--no-create` |
| `--no-github` | 跳过GitHub同步 | `--no-github` |
| `--no-jira` | 跳过JIRA同步 | `--no-jira` |
| `--no-ado` | 跳过Azure DevOps同步 | `--no-ado` |
| `--force` | 即使验证失败也强制同步 | `--force` |

**标志组合**：
```bash
# Full sync with auto-create (DEFAULT - just works!)
/sw:sync-progress

# Sync only, don't create missing issues
/sw:sync-progress 0053 --no-create

# Dry-run with no external tools
/sw:sync-progress --dry-run --no-github

# Force sync, skip GitHub
/sw:sync-progress --force --no-github
```

---

## 与其他同步命令的比较

| 命令 | 同步范围 | 是否自动创建问题？ | 适用场景 |
|---------|-------|--------------|-------------|
| `/sw:sync-acs` | 仅同步任务到ACs | ❌ | 快速更新AC状态 |
| `/sw:sync-specs` | 仅同步规格文档 | ❌ | 规格文档更改后使用 |
| `/sw-github:create` | 创建GitHub问题 | ✅ | 手动创建问题 |
| `/sw-github:sync` | 仅同步文档到GitHub | ❌ | 仅针对GitHub的同步（问题必须存在） |
| `/sw:sync-progress` | **任务 → 文档 → 创建 → 同步** | ✅ | **全面同步** ✅（推荐使用！） |

**使用建议**：
- 如果需要**全面同步**：使用`/sw:sync-progress` ✅
- 如果需要**针对性同步**：使用特定命令（如`sync-acs`、`sync-specs`）
- 如果只需要**同步**（不希望自动创建问题）：使用`/sw:sync-progress --no-create` |

---

## 自动检测机制

**智能增量检测**：

```bash
# Explicit increment ID
/sw:sync-progress 0053

# Auto-detect from active increment
/sw:sync-progress
```

**自动检测的工作原理**：
1. 读取`.specweave/state/active-increment.json`文件
2. 找到第一个活跃的增量ID
3. 使用该增量进行同步

---

## 外部工具配置

**自动检测已配置的工具**：

该命令会检查`.specweave/config.json`文件中的配置：
- GitHub：`"provider": "github"`
- JIRA：`"provider": "jira"`
- Azure DevOps：`"provider": "azure-devops"`

**仅同步已配置的工具**：

```
✅ GitHub integration detected → Will sync
ℹ️  No JIRA integration → Skip
ℹ️  No ADO integration → Skip
```

---

## 错误处理

**优雅的错误处理机制**：

| 错误类型 | 处理方式 | 影响 |
|------------|----------|--------|
| AC同步失败 | ❌ 中止同步 | 严重问题——会阻止所有同步 |
| 文档同步失败 | ❌ 中止同步 | 严重问题——但文档仍会同步 |
| GitHub同步失败 | ⚠️ 记录警告，继续执行 | 非严重问题——文档仍会同步 |
| JIRA同步失败 | ⚠️ 记录警告，继续执行 | 非严重问题——文档仍会同步 |
| ADO同步失败 | ⚠️ 记录警告，继续执行 | 非严重问题——文档仍会同步 |

**原则**：核心同步（任务到文档）必须成功。外部工具同步则是尽力而为。

---

## 故障排除

### 错误1：“未找到活跃的增量”

**错误原因**：
```
❌ No active increment found
```

**解决方法**：
```bash
# Provide increment ID explicitly
/sw:sync-progress 0053
```

### 错误2：“AC同步出现警告”

**错误原因**：
```
⚠️  AC sync had warnings: 5 ACs not found in spec.md
```

**解决方法**：
```bash
# Embed ACs from living docs into spec.md
/sw:embed-acs 0053

# Then retry sync
/sw:sync-progress 0053
```

**原因说明**：`spec.md`中缺少内联的ACs（符合ADR-0064要求）。

---

### 错误3：“超过GitHub的速率限制”

**错误原因**：
```
⚠️  GitHub sync had warnings: Rate limit exceeded
```

**解决方法**：非严重问题。文档仍会同步。等待速率限制解除后再重试：

```bash
# Retry GitHub sync only (when rate limit resets)
/sw-github:sync 0053
```

## 与工作流的集成

**典型的增量工作流与进度同步**：

```bash
# 1. Plan increment
/sw:increment "Safe feature deletion"

# 2. Execute tasks
/sw:do

# [Complete tasks manually or via sub-agents...]

# 3. Sync progress after each batch of tasks
/sw:sync-progress

# 4. Final sync before closure
/sw:sync-progress 0053

# 5. Validate quality
/sw:validate 0053 --quality

# 6. Close increment
/sw:done 0053
```

## 最佳实践

### ✅ 应该这样做：

1. **批量完成任务后同步**：完成3-5个任务后进行同步 → 继续下一步
2. **关闭增量前进行最终同步**：确保在执行`/sw:done`之前所有数据都同步
3. **先进行干运行**：使用`--dry-run`预览更改
4. **检查外部工具**：同步后验证GitHub/JIRA的状态
5. **检查状态行**：确保完成百分比显示正确

### 不应该这样做：

1. **不要对每个任务都进行同步**：批量处理更高效
2. **不要跳过最终同步**：在执行`/sw:done`之前一定要同步
3. **不要忽略警告**：AC同步警告表示有遗漏的ACs
4. **不要强行同步**：使用`--force`标志会绕过验证步骤
5. **在任务未完成时不要同步**：只有当进度实际发生变化时才进行同步

---

## 架构原理

**为什么需要全面同步**：

```
Problem: Manual multi-step sync is error-prone
  1. Update spec.md ACs manually
  2. Run /sw:sync-specs
  3. Run /sw-github:sync
  4. Run /sw:update-status
  5. Check each system for correctness

Solution: Single command orchestrates all steps
  /sw:sync-progress → Does all 4 steps automatically
```

**好处**：
- ✅ **一键式操作**：通过一个命令完成所有同步
- ✅ **保证数据一致性**：所有系统的数据保持一致
- ✅ **容错能力强**：非关键性的错误不会影响核心同步
- ✅ **提供审计追踪**：详细的报告显示了同步的内容
- ✅ **支持预览**：执行前可以预览同步结果

---

## 背景信息

在此命令出现之前，用户需要手动执行以下操作：
1. 运行`/sw:sync-acs`
2. 运行`/sw:sync-specs`
3. 运行`/sw-github:sync`
4. 运行`/sw:update-status`

现在：**一个命令即可完成所有这些步骤** ✅

---

## 相关命令

- `/sw:sync-acs` - 仅同步任务到ACs
- `/sw:sync-specs` - 仅同步规格文档到实时文档
- `/sw:sync-tasks` - 双向同步外部工具和任务
- `/sw-github:sync` - 仅同步文档到GitHub
- `/sw-jira:sync` - 仅同步文档到JIRA
- `/sw-ado:sync` - 仅同步文档到Azure DevOps
- `/sw:update-status` - 更新状态行缓存

---

**我可以帮助您高效地在所有系统之间同步进度！**

如果您有任何疑问，请随时问我：
- “如何将进度同步到GitHub？”
- “`sync-progress`和`sync-acs`有什么区别？”
- “如何在不执行的情况下预览同步结果？”
- “为什么我的GitHub同步失败了？”
- “什么时候应该使用`--dry-run`？”