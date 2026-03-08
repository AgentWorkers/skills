---
name: mindkeeper
description: >
  **AI大脑的“时间机器”——用于管理代理上下文文件的版本控制工具**  
  当用户询问 `SOUL.md`、`AGENTS.md`、`MEMORY.md` 或其他代理上下文文件的变化情况时；当他们需要撤销操作、回滚到之前的版本，或进行版本比较时；又或者在进行高风险编辑之前需要创建一个检查点时，都可以使用这个工具。
version: 1.2.1
homepage: https://github.com/seekcontext/mindkeeper
repository: https://github.com/seekcontext/mindkeeper
---
# Mindkeeper — 为您的人工智能“大脑”提供时间回溯功能

当用户询问其代理上下文文件（AGENTS.md、SOUL.md、USER.md、IDENTITY.md、TOOLS.md、MEMORY.md、memory/、skills/）的变更、历史记录或版本信息时，请使用 Mindkeeper 工具。

## 初始化（一次性设置）

**当用户启用 Mindkeeper 或请求使用 Mindkeeper 功能时**，首先尝试运行 `mind_status` 命令。如果该命令失败（例如工具未找到或出现类似错误），请按照以下步骤操作：

1. **获取用户确认**：告知用户：“Mindkeeper 需要 `mindkeeper-openclaw` 插件才能正常工作。我需要执行 `openclaw plugins install mindkeeper-openclaw` 并重启 Gateway。您确定要继续吗？”**请在用户明确同意之前，切勿进行任何安装或重启操作。**

2. **用户确认后**，执行以下步骤：
   - **安装插件**：通过 bash 命令执行 `openclaw plugins install mindkeeper-openclaw`。
   - **重启 Gateway**：使用 `gateway` 工具，设置 `action: "restart"` 并添加注释 `note: "重启以加载 Mindkeeper 插件"`。如果 Gateway 无法重启或重启失败，请告知用户：“插件已安装，请手动重启 Gateway 以应用更改。”
   - **确认安装结果**：告知用户：“Mindkeeper 已准备好。重启完成，现在您可以查询文件的历史记录、差异内容或执行回滚操作了。”

3. **如果用户希望手动安装插件**，请告知他们：“在终端中运行 `openclaw plugins install mindkeeper-openclaw`，然后重启 Gateway。之后 Mindkeeper 将可正常使用。”

如果 `mind_status` 命令成功执行，说明插件已经安装完成，可以直接根据用户的请求继续操作。

## 可用工具

| 工具 | 功能 |
|------|---------|
| `mind_status` | 显示被跟踪的文件以及是否存在未保存的变更 |
| `mind_history` | 查看单个文件或所有文件的变更记录 |
| `mind_diff` | 逐行比较两个文件版本之间的差异 |
| `mind_rollback` | 将文件恢复到之前的版本（务必先预览） |
| `mind_snapshot` | 在进行重要更改前创建带有名称的快照 |

## 使用场景

| 用户请求 | 操作建议 |
|-----------|--------|
| “SOUL.md 文件发生了哪些变更？” | 使用 `mind_history` 并指定文件路径 `file: "SOUL.md"` |
| “显示上周的变更记录” | 先使用 `mind_history` 查找相关提交记录，再使用 `mind_diff` 比较版本差异 |
| “撤销之前的更改” / “回滚 AGENTS.md 文件” | 执行完整的回滚操作（详见下文） |
| “在实验前创建快照” | 使用 `mind_snapshot` 并为快照指定描述性名称 |
| “Mindkeeper 是否正在跟踪我的文件？” | 使用 `mind_status` 查询文件跟踪情况 |
| “我的文件历史记录是什么样的？” | 不指定文件路径，直接使用 `mind_history` 查看历史记录 |

## 工具使用指南

### mind_status
如果您不确定 Mindkeeper 是否已初始化或哪些文件被跟踪，请先执行此命令。
```
mind_status → { initialized, workDir, pendingChanges, snapshots }
```

### mind_history
返回包含提交哈希、日期和提交信息的变更记录列表。
- `file`（可选）：指定要查询的文件路径，例如 `"SOUL.md"`。
- `limit`（可选）：返回的记录条数（默认为 10 条，可根据需要增加）。
```
mind_history({ file: "SOUL.md", limit: 20 })
→ { count, entries: [{ oid, date, message }] }
```

### mind_diff
比较两个文件版本之间的差异。`from` 和 `to` 参数可以接受简短的提交哈希或完整的提交哈希（来自 `mind_history`）。
- 如果省略 `to` 参数，系统会自动将 `from` 参数与当前版本（HEAD）进行比较。
```
mind_diff({ file: "SOUL.md", from: "a1b2c3d4" })
→ { file, from, to, additions, deletions, unified }
```

### mind_snapshot
为所有被跟踪的文件创建一个带有名称的快照。在进行高风险更改前建议使用此命令。
- `name`：快照的名称，例如 `"stable-v2"` 或 `"before-experiment"`。
- `message`（可选）：为快照添加描述性文字。
```
mind_snapshot({ name: "stable-v2", message: "Personality tuned, rules finalized" })
→ { success, snapshot, commit: { oid, message } }
```

### mind_rollback
**请务必按照两步流程操作**，切勿跳过预览步骤。

**步骤 1 — 预览：**
```
mind_rollback({ file: "SOUL.md", to: "a1b2c3d4", preview: true })
→ { preview: true, diff: { unified, additions, deletions }, instruction }
```
向用户展示文件差异内容，并请求用户确认是否继续执行回滚操作。

**步骤 2 — 执行回滚（仅在用户确认后执行）：**
```
mind_rollback({ file: "SOUL.md", to: "a1b2c3d4", preview: false })
→ { preview: false, success: true, commit: { oid, message } }
```
回滚操作成功后，告知用户：“请运行 `/new` 命令将更改应用到当前会话中。”

## 重要说明

- **回滚操作是针对单个文件的**，只会恢复指定的文件，不会同时恢复所有文件。
- **回滚操作是非破坏性的**：每次回滚都会创建一个新的提交记录，因此也可以随时撤销。
- **Mindkeeper 会自动在后台生成快照**：用户无需手动保存文件变更，系统会自动捕获所有变更。
- **建议在进行重大配置或规则更改前创建快照**：这有助于防止数据丢失。
- **如果历史记录为空**，可能表示 Mindkeeper 尚未初始化，或者自安装以来没有发生任何变更。请运行 `mind_status` 命令进行确认。
- **提交哈希**：请始终使用 `mind_history` 返回的 `oid` 字段作为哈希值。8 个字符的简短哈希即可。