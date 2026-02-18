---
name: verk
description: "在 Verk 中管理任务、项目和工作流程——这是一款基于人工智能的任务管理工具。您可以创建、更新、分配和跟踪任务；添加注释、更改任务状态，并查看自动化流程的详细信息。"
metadata:
  openclaw:
    emoji: "⚡"
    requires:
      env:
        - VERK_API_KEY
        - VERK_ORG_ID
      bins:
        - node
    primaryEnv: VERK_API_KEY
---
# Verk 任务管理

您可以使用 `verk-cli.mjs` 命令行工具在 Verk 中管理任务、项目和自动化流程。

## 可用命令

### 任务

- **列出任务**：`node scripts/verk-cli.mjs tasks list [--status STATUS] [--priority PRIORITY] [--search QUERY]`
- **获取任务信息**：`node scripts/verk-cli.mjs tasks get <taskId>`
- **创建任务**：`node scripts/verk-cli.mjs tasks create --title "标题" [--description "描述"] [--status STATUS] [--priority PRIORITY] [--assigned userId1,userId2]`
- **更新任务**：`node scripts/verk-cli.mjs tasks update <taskId> [--title "新标题"] [--status STATUS] [--priority PRIORITY] [--assigned userId1,userId2]`
- **删除任务**：`node scripts/verk-cli.mjs tasks delete <taskId>`
- **在任务上添加评论**：`node scripts/verk-cli.mjs tasks comment <taskId> --text "评论内容"`

### 项目

- **列出项目**：`node scripts/verk-cli.mjs projects list`

### 自动化流程（工作流）

- **列出流程**：`node scripts/verk-cli.mjs flows list`

## 可用的值

- **状态**：`待办（Backlog）`, `进行中（In-Progress）`, `审核中（Review）`, `已完成（Done）`
- **优先级**：`紧急（Urgent）`, `高（High）`, `中等（Medium）`, `低（Low）`, `无（None）`

## 各命令的使用场景

- 要查看现有任务，请使用 `tasks list`。可以通过添加 `--status` 或 `--priority` 来过滤任务，或使用 `--search` 来查找特定任务。
- 要获取特定任务的信息，请使用 `tasks get <taskId>`。
- 要创建任务，请使用 `tasks create` 并指定至少 `--title` 参数。
- 要更新、修改任务，请使用 `tasks update <taskId>` 并提供需要修改的字段。
- 要将任务标记为已完成，请使用 `tasks update <taskId> --status Done`。
- 要分配任务，请使用 `tasks update <taskId> --assigned userId`。
- 要删除任务，请使用 `tasks delete <taskId>`。
- 要在任务上添加评论或备注，请使用 `tasks comment <taskId> --text "..."`。
- 要查看项目信息，请使用 `projects list`。
- 要查看自动化流程，请使用 `flows list`。
- 要查看任务的评论，请使用 `tasks get <taskId>`（评论会包含在任务响应中）。

## 输出格式

所有命令都会返回 JSON 格式的结果。请解析输出内容以提取对用户有用的信息。在列出任务时，只需显示关键字段（标题、状态、优先级、负责人），而无需显示完整的 JSON 数据。

## 示例

```bash
# List all high-priority tasks
node scripts/verk-cli.mjs tasks list --priority High

# Create a task and assign it
node scripts/verk-cli.mjs tasks create --title "Review Q2 roadmap" --priority High --status Todo

# Mark a task as done
node scripts/verk-cli.mjs tasks update task-abc123 --status Done

# Add a comment
node scripts/verk-cli.mjs tasks comment task-abc123 --text "Completed the review, looks good"
```