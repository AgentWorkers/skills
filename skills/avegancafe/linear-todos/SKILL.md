---
name: linear-todos
description: 使用 Linear 作为后端来管理待办事项和提醒。可以创建带有自然语言日期（如“明天”、“下周一”）、优先级以及智能调度功能的任务。系统支持每日任务回顾，并提供命令行界面（CLI）工具，以实现完整的待办事项工作流程。
author: K
tags: [todos, linear, tasks, reminders, productivity]
---
# Linear Todos

这是一个基于Linear框架构建的强大待办事项管理系统，具备智能日期解析功能、优先级设置以及完善的命令行（CLI）工作流程。

## 快速入门

```bash
# Setup (run once)
uv run python main.py setup

# Create todos
uv run python main.py create "Call mom" --when day
uv run python main.py create "Pay taxes" --date 2025-04-15
uv run python main.py create "Review PR" --priority high --when week

# Natural language dates
uv run python main.py create "Meeting prep" --date "tomorrow"
uv run python main.py create "Weekly report" --date "next Monday"
uv run python main.py create "Dentist" --date "in 3 days"

# Manage todos
uv run python main.py list
uv run python main.py done ABC-123
uv run python main.py snooze ABC-123 "next week"

# Daily review
uv run python main.py review
```

## 设置

### 1. 获取API密钥

请从 [linear.app/settings/api](https://linear.app/settings/api) 获取您的API密钥。

### 2. 运行设置向导

```bash
uv run python main.py setup
```

这个交互式向导将：
- 验证您的API密钥
- 列出您所属的Linear团队
- 允许您选择待办事项团队
- 配置待办事项的初始状态（未完成/已完成）
- 将设置保存到 `~/.config/linear-todos/config.json` 文件中。

### 3. 手动配置（可选）

您也可以通过设置环境变量来替代运行设置向导：

```bash
export LINEAR_API_KEY="lin_api_..."
export LINEAR_TEAM_ID="your-team-id"
export LINEAR_STATE_ID="your-todo-state-id"
export LINEAR_DONE_STATE_ID="your-done-state-id"
```

或者直接创建 `~/.config/linear-todos/config.json` 文件：

```json
{
  "apiKey": "lin_api_...",
  "teamId": "team-uuid",
  "stateId": "todo-state-uuid",
  "doneStateId": "done-state-uuid"
}
```

## 命令

### create

创建一个新的待办事项，可以指定完成时间、优先级和描述。

```bash
uv run python main.py create "Title" [options]

Options:
  --when day|week|month     Relative due date
  --date DATE               Specific due date (supports natural language)
  --priority LEVEL          urgent, high, normal, low, none
  --desc "Description"      Add description
```

**日期示例：**

```bash
uv run python main.py create "Task" --date "tomorrow"
uv run python main.py create "Task" --date "Friday"
uv run python main.py create "Task" --date "next Monday"
uv run python main.py create "Task" --date "in 3 days"
uv run python main.py create "Task" --date "in 2 weeks"
uv run python main.py create "Task" --date "2025-04-15"
```

**完整示例：**

```bash
# Due by end of today
uv run python main.py create "Call mom" --when day

# Due in 7 days
uv run python main.py create "Submit report" --when week

# Specific date with high priority
uv run python main.py create "Launch feature" --date 2025-03-15 --priority high

# Natural language date with description
uv run python main.py create "Team meeting prep" --date "next Monday" --desc "Prepare slides"

# Urgent priority, due tomorrow
uv run python main.py create "Fix production bug" --priority urgent --date tomorrow
```

### list

列出所有待办事项。

```bash
uv run python main.py list [options]

Options:
  --all       Include completed todos
  --json      Output as JSON
```

### done

将待办事项标记为已完成。

```bash
uv run python main.py done ISSUE_ID

# Examples
uv run python main.py done TODO-123
uv run python main.py done ABC-456
```

### snooze

将待办事项重新安排到未来的日期。

```bash
uv run python main.py snooze ISSUE_ID [when]

# Examples
uv run python main.py snooze TODO-123 "tomorrow"
uv run python main.py snooze TODO-123 "next Friday"
uv run python main.py snooze TODO-123 "in 1 week"
```

### review

每日执行此命令，按紧急程度对待办事项进行排序。

```bash
uv run python main.py review
```

输出结果包括：
- 🚨 **过期** - 已过截止日期
- 📅 **今日到期** - 今天到期
- ⚡ **高优先级** - 紧急/高优先级的任务
- 📊 **本周内完成** - 7天内需要完成
- 📅 **本月内完成** - 28天内需要完成
- 📝 **无截止日期** - 无具体完成时间的任务

### setup

交互式设置向导，用于配置您的Linear集成。

```bash
uv run python main.py setup
```

该向导将引导您完成以下步骤：
- 验证API密钥
- 选择所属的Linear团队
- 配置待办事项的初始状态（未完成/已完成）
- 将设置保存到 `~/.config/linear-todos/config.json` 文件中。

## 为代理（Agents）提供的功能

当用户请求提醒或查看待办事项时：

### 1. 解析自然语言日期

将用户输入的日期转换为具体的日期格式。

```bash
# "remind me Friday to call mom"
uv run python main.py create "Call mom" --date "2025-02-21"

# "remind me to pay taxes by April 15"
uv run python main.py create "Pay taxes" --date "2025-04-15"

# "remind me next week about the meeting"
uv run python main.py create "Meeting" --date "next Monday"
```

### 2. 确定优先级

如果用户未指定优先级，系统会自动分配如下等级：
- **紧急** (🔥) - 非常紧急，需要立即处理
- **高** (⚡) - 重要，需尽快处理
- **普通** (📌) - 标准优先级（默认）
- **低** (💤) - 可以稍后处理

### 3. 每日简报

当用户询问“今天有什么任务需要完成”时，执行以下操作：

```bash
uv run python main.py review
```

请**严格按照原始格式** 显示输出结果，不要重新格式化或总结内容。

### 4. 标记待办事项为已完成

当用户表示某项任务已完成时，执行以下操作：

```bash
uv run python main.py done ISSUE-123
```

## 日期解析参考

| 输入 | 解析结果 |
|-------|--------|
| `today` | 今天 |
| `tomorrow` | 明天 |
| `Friday` | 下一个周五 |
| `next Monday` | 下周的周一 |
| `this Friday` | 当前的周五（或如果今天是周末，则为下一个周五） |
| `in 3 days` | 3天后 |
| `in 2 weeks` | 14天后 |
| `2025-04-15` | 具体的日期 |

## 优先级等级

| 等级 | 数值 | 图标 | 适用场景 |
|-------|--------|------|---------|
| 紧急 | 1 | 🔥 | 非常紧急，可能会影响项目进度 |
| 高 | 2 | ⚡ | 重要，需尽快处理 |
| 普通 | 3 | 📌 | 标准优先级的任务（默认） |
| 低 | 4 | 💤 | 可以延后处理的任务 |
| 无 | 0 | 📋 | 未设置优先级 |

## 设置优先级的顺序

设置项的加载顺序如下（后面的设置会覆盖前面的设置）：
1. 默认值（未设置优先级）
2. 配置文件：`~/.config/linear-todos/config.json`
3. 环境变量：`LINEAR_*`
4. 命令行参数：`--team`, `--state`

## 相关文件

| 文件 | 用途 |
|------|---------|
| `main.py` | CLI程序的主入口文件 |
| `src/linear_todos/cli.py` | 包含所有命令的CLI实现 |
| `src/linear_todos/api.py` | Linear API客户端 |
| `src/linear_todos/config.py` | 负责配置管理 |
| `src/linear_todos/dates.py` | 日期解析工具类 |
| `src/linear_todos/setup_wizard.py` | 交互式设置向导程序 |