---
name: find-code-tasks
description: 列出仓库中所有的代码任务，包括它们的状态、日期和元数据。这对于了解待办的工作或查找特定任务非常有用。
type: anthropic-skill
version: "1.0"
---

# 查找代码任务

## 概述

此技能用于查找并显示仓库中的所有代码任务（`.code-task.md` 文件），包括它们的前置内容（frontmatter）状态和元数据。您可以使用它来快速了解待处理的工作、按状态查找任务或检查任务积压情况。

## 使用场景

- 在开始工作会话时，查看可用的任务
- 在运行代码辅助工具（`code-assist`）之前/之后，检查任务状态
- 按状态（待处理、进行中、已完成）查找任务
- 获取任务积压的汇总信息
- 导出任务数据以用于报告

## 参数

- **filter**（可选）：按状态过滤任务
  - `pending` - 仅显示待处理的任务
  - `in_progress` - 仅显示进行中的任务
  - `completed` - 仅显示已完成的任务
  - （无） - 显示所有任务

- **format**（可选，默认值："table"）：输出格式
  - `table` - 带有状态符号的易读表格
  - `json` - 用于程序化处理的 JSON 数组
  - `summary` - 仅按状态统计

- **tasks_dir**（可选，默认值：".ralph/tasks/"）：搜索任务的目录

## 使用示例

```bash
# Show all tasks in table format
/find-code-tasks

# Show only pending tasks
/find-code-tasks filter:pending

# Get JSON output for tooling
/find-code-tasks format:json

# Quick summary of task counts
/find-code-tasks format:summary

# Search custom directory
/find-code-tasks tasks_dir:tools/
```

## 步骤

### 1. 运行任务状态脚本

该脚本与本技能一起存储在 `.claude/skills/find-code-tasks/task-status.sh` 文件中。

使用适当的参数执行脚本：

```bash
# Default: table format, all tasks
.claude/skills/find-code-tasks/task-status.sh

# With filter
.claude/skills/find-code-tasks/task-status.sh --pending
.claude/skills/find-code-tasks/task-status.sh --in_progress
.claude/skills/find-code-tasks/task-status.sh --completed

# With format
.claude/skills/find-code-tasks/task-status.sh --json
.claude/skills/find-code-tasks/task-status.sh --summary

# Custom tasks directory
TASKS_DIR=tools/ .claude/skills/find-code-tasks/task-status.sh
```

### 2. 显示结果

将结果展示给用户。对于表格格式，输出内容如下：

| 符号 | 状态 |
|--------|--------|
| ○ | 待处理 |
| ● | 进行中 |
| ✓ | 已完成 |
| ■ | 被阻止 |

### 3. 建议下一步操作

根据结果，给出相应的建议：
- 如果有待处理的任务：`运行 `/code-assist .ralph/tasks/<task-name>.code-task.md` 以启动任务`
- 如果有进行中的任务：`已有进行中的任务——建议先完成这些任务`
- 如果所有任务都已完成：`所有任务已完成！使用 `/code-task-generator` 创建新任务`

## 输出示例

### 表格格式（默认）

```
TASKS STATUS
════════════════════════════════════════════════════════════════
    TASK                                     STATUS       DATE
────────────────────────────────────────────────────────────────
○ add-task-frontmatter-tracking            pending      2025-01-15
○ enhance-headless-tool-output             pending      -
● fix-ctrl-c-freeze                        in_progress  2025-01-14
✓ replay-backend                           completed    2025-01-13
────────────────────────────────────────────────────────────────
Total: 4 tasks
```

### 摘要格式

```
Task Summary
────────────
○ Pending:     10
● In Progress: 2
✓ Completed:   5
────────────
  Total:       17
```

### JSON 格式

```json
[
  {"task": "add-task-frontmatter-tracking", "status": "pending", "created": "2025-01-15", "started": null, "completed": null},
  {"task": "fix-ctrl-c-freeze", "status": "in_progress", "created": "2025-01-14", "started": "2025-01-14", "completed": null}
]
```

## 前置内容（Frontmatter）结构

具有前置内容跟踪的任务具有以下结构：

```yaml
---
status: pending | in_progress | completed | blocked
created: YYYY-MM-DD    # Date task was created
started: YYYY-MM-DD    # Date work began (null if not started)
completed: YYYY-MM-DD  # Date work finished (null if not done)
---
```

没有前置内容的任务会显示为 `pending`，并且日期字段显示为 `null`。

## 与其他技能的集成

- **code-task-generator**：创建带有前置内容的新任务
- **code-assist**：在开始/完成任务时更新任务状态
- **ralph-code-assist**：通过 Ralph 调度器运行任务

## 故障排除

### 未找到任务

如果未显示任何任务：
- 确认任务目录存在：`ls .ralph/tasks/`
- 检查文件扩展名是否为 `.code-task.md`
- 尝试指定目录：`/find-code-tasks tasks_dir:./`

### 脚本未找到

如果找不到 `task-status.sh` 脚本：
- 确保您位于仓库根目录
- 检查脚本是否存在：`ls .claude/skills/find-code-tasks/task-status.sh`
- 使脚本可执行：`chmod +x .claude/skills/find-code-tasks/task-status.sh`

### 前置内容未被解析

如果具有前置内容的任务的日期字段显示为 `-`：
- 确保前置内容的第一行以 `---` 开头
- 检查 YAML 语法是否有效
- 确认字段名称匹配：`status`、`created`、`started`、`completed`