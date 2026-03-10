---
name: mindkeeper
description: >
  **AI大脑的“时间机器”——用于管理代理上下文文件的版本控制系统**  
  当用户询问 `SOUL.md`、`AGENTS.md`、`MEMORY.md` 或其他代理上下文文件的变化情况时；当他们希望撤销操作、回滚到之前的版本，或进行版本比较时；又或者在进行高风险编辑之前需要创建一个检查点时，都可以使用这个工具。
version: 1.2.4
homepage: https://github.com/seekcontext/mindkeeper
repository: https://github.com/seekcontext/mindkeeper
---
# Mindkeeper — 为您的人工智能大脑提供“时间机器”功能

当用户询问其代理上下文文件（`AGENTS.md`、`SOUL.md`、`USER.md`、`IDENTITY.md`、`TOOLS.md`、`HEARTBEAT.md`、`MEMORY.md`、`memory/`、`skills/`）的变更、历史记录或版本信息时，请使用 Mindkeeper 工具。

## 启动流程（一次性设置）

**当用户启用 Mindkeeper 或请求 Mindkeeper 功能时**，首先尝试执行 `mind_status` 命令。如果该命令失败（例如工具未找到或出现类似错误），请按照以下步骤操作：

1. **获取用户确认**：告知用户：“Mindkeeper 需要 `mindkeeper-openclaw` 插件才能正常工作。我需要运行 `openclaw plugins install mindkeeper-openclaw` 并重启 Gateway。您确认继续吗？”**在用户明确同意之前，切勿进行安装或重启操作。**

2. **用户确认后**，执行以下步骤：
   - **安装插件**：通过 bash 命令安装插件：
     ```bash
     openclaw plugins install mindkeeper-openclaw
     ```
   - **如果运行时环境支持重启**：使用相应的机制重启 Gateway。如果无法重启或重启失败，告知用户：“插件已安装，但需要手动重启 Gateway 才能使用这些工具。”
   - **确认重启结果**：如果重启成功，告知用户：“Mindkeeper 已准备就绪。现在您可以查询历史记录、文件差异、回滚操作或创建快照了。”如果重启失败，请告知用户插件已安装，但需要重启 Gateway 才能使用这些工具。

3. **替代方案**：如果用户希望手动安装插件，可以告知他们：“在终端中运行 `openclaw plugins install mindkeeper-openclaw`，然后重启 Gateway。完成后 Mindkeeper 将可正常使用。”

如果 `mind_status` 命令成功执行，说明插件已安装，可直接进入用户的请求处理流程。

## 工具使用建议

在 OpenClaw 插件模式下，对于常规的 Mindkeeper 操作，建议优先使用 `mind_*` 系列工具而非 CLI 命令：
- 在 `mind_status`、`mind_history`、`mind_diff`、`mind_snapshot` 和 `mind_rollback` 可用时，优先使用这些工具。
- 如果插件工具可用，切勿使用 `openclaw mind ...` 或 `mindkeeper ...` 命令来执行常规的历史记录查询、文件差异比较、快照创建或回滚操作。
- CLI 命令仅用于一次性设置、故障排除、手动操作或用户特别要求使用终端命令的情况。

## 可用工具

| 工具 | 功能 |
|------|---------|
| `mind_status` | 显示被跟踪的文件列表以及是否存在未保存的变更 |
| `mind_history` | 查看单个文件或所有文件的变更记录 |
| `mind_diff` | 逐行比较两个文件版本 |
| `mindrollback` | 将文件恢复到之前的版本（务必先预览） |
| `mind_snapshot` | 在进行重大更改前创建带有名称的快照 |

## 跟踪文件范围

Mindkeeper 默认跟踪以下文件：
- `AGENTS.md`、`SOUL.md`、`USER.md`、`IDENTITY.md`
- `TOOLS.md`、`HEARTBEAT.md`、`MEMORY.md`
- `memory/**/*.md`
- `skills/**/*.md`

默认不跟踪的文件包括：`BOOTSTRAP.md`、`canvas/**`、`.git/`、`.mindkeeper/`。

## 使用场景

| 用户请求 | 操作建议 |
|-----------|--------|
| “`SOUL.md` 文件发生了哪些变化？” | 使用 `mind_history` 并指定文件路径 `file: "SOUL.md"` |
| “显示上周的变更记录” | 先使用 `mind_history` 查找对应的提交记录，再使用 `mind_diff` |
| “撤销该更改” / “回滚 `AGENTS.md` 的内容” | 执行完整的回滚操作（详见下文） |
| “在实验前创建快照” | 使用 `mind_snapshot` 并为快照指定描述性名称 |
| “Mindkeeper 是否正在跟踪我的文件？” | 使用 `mind_status` 查询 |
| “我的历史记录是什么样的？” | 不指定文件路径，直接使用 `mind_history` |

## 直接编辑文件

如果用户请求直接编辑被跟踪的文件（如 `SOUL.md`、`AGENTS.md` 或 `MEMORY.md`），请直接执行编辑操作：
- 不要因为 CLI 命令不可用而阻碍用户操作。
- 除非用户明确要求使用 CLI 命令，否则不要提及 CLI 命令的可用性。
- Mindkeeper 的后台监控机制会自动捕获编辑后的变更。
- 如有必要，可以提醒用户该变更现在已被 Mindkeeper 记录下来。

## 工具使用指南

### `mind_status`
当用户询问历史记录、跟踪状态、快照或回滚操作时，或您不确定 Mindkeeper 是否已初始化时，首先调用此命令。
```
mind_status → { initialized, workDir, pendingChanges, snapshots }
```

在用户仅进行简单编辑操作时，无需先调用 `mind_status`，除非用户特别询问有关跟踪或历史记录的信息。

### `mind_history`
返回包含提交哈希、日期和提交信息的变更记录列表：
- `file`（可选）：指定要查询的文件路径，例如 `"SOUL.md"`
- `limit`（可选）：返回的记录条目数量（默认为 10 条，可根据需要增加）

```
mind_history({ file: "SOUL.md", limit: 20 })
→ { count, entries: [{ oid, date, message }] }
```

### `mind_diff`
比较两个文件版本。`from` 和 `to` 参数可以指定来自 `mind_history` 的提交哈希值（简写或完整格式）。
- 如果省略 `to` 参数，系统会自动将 `from` 对象与当前版本（HEAD）进行比较。

```
mind_diff({ file: "SOUL.md", from: "a1b2c3d4" })
→ { file, from, to, additions, deletions, unified }
```

### `mind_snapshot`
创建所有被跟踪文件的当前状态快照。在进行可能带来风险的更改前使用此命令：
- `name`：为快照指定一个简短的标识符，例如 `"stable-v2"` 或 `"before-experiment"`
- `message`（可选）：为快照添加描述性文字

```
mind_snapshot({ name: "stable-v2", message: "Personality tuned, rules finalized" })
→ { success, snapshot, commit: { oid, message } }
```

### `mindrollback`
**请务必遵循两步流程**：务必先预览更改内容。
**第一步——预览：**
```
mind_rollback({ file: "SOUL.md", to: "a1b2c3d4", preview: true })
→ { preview: true, diff: { unified, additions, deletions }, instruction }
```
向用户展示文件差异，并请求用户确认是否继续执行回滚操作。

**第二步——执行回滚：**
```
mind_rollback({ file: "SOUL.md", to: "a1b2c3d4", preview: false })
→ { preview: false, success: true, commit: { oid, message } }
```
回滚操作成功后，告知用户：“请运行 `/new` 命令将更改应用到当前会话中。”

## 重要说明

- **本文档仅提供使用指南，实际功能由插件实现**：`mindkeeper-openclaw` 插件提供了 `mind_*` 系列工具和监控机制；本文档旨在指导 AI 如何正确配置和使用这些工具。
- **优先使用插件工具**：在 OpenClaw 插件模式下，常规操作应优先使用 `mind_*` 工具。
- **回滚操作是针对单个文件的**：仅恢复指定的文件，不会同时恢复所有文件。
- **回滚操作是可逆的**：每次回滚都会生成一个新的提交记录，因此可以随时撤销。
- **自动快照功能在后台运行**：用户无需手动操作，Mindkeeper 会自动捕获所有更改。
- **LLM 的提交信息目前仅通过插件提供**：独立运行的 CLI 模式会使用默认的提示信息。
- **建议创建命名快照**：在进行重要配置或规则更改前，请创建快照。
- **如果历史记录为空**：可能表示 Mindkeeper 尚未初始化，或者自安装以来没有发生任何更改。请使用 `mind_status` 进行检查。
- **提交哈希值**：请使用 `mind_history` 返回的 `oid` 字段生成哈希值（8 个字符即可）。
- **保持用户界面的简洁性**：如果任务可以通过文件编辑或 `mind_*` 工具完成，无需向用户展示不可用的 CLI 详细信息。