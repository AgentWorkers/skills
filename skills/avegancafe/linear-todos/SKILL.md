---
name: linear-todos
description: 这是一个命令行工具（CLI），它通过 Linear 的 API 执行 Python 源代码来管理待办事项。该工具允许用户使用自然语言输入日期、优先级和调度信息来创建任务。这属于“源代码执行”（source-execution）类型的技能：当用户调用相关命令时，位于 `src/linear_todos/` 目录下的 Python 代码会被自动执行。
author: K
tags: [todos, linear, tasks, reminders, productivity]
metadata:
  openclaw:
    primaryEnv: LINEAR_API_KEY
    requires:
      env: [LINEAR_API_KEY]
      config: [~/.config/linear-todos/config.json]
    install:
      - kind: uv
        id: linear-todos
        label: Linear Todos CLI
---
# 线性待办事项管理技能（Linear Todos Skill）

> **⚠️ 这是一个需要源代码执行的技能。** 当您通过命令行界面（CLI）调用相关命令时，该技能会从 `src/linear_todos/` 目录运行 Python 代码。请注意，这不仅仅是一个用于显示信息的技能，还需要您进行一些配置操作。在使用前，请务必阅读 `src/linear_todos/api.py` 文件。

> **🔐 安全提示：** 该技能会将您的 Linear API 密钥以明文形式存储在 `~/.config/linear-todos/config.json` 文件中，**仅当您执行 `setup` 命令时**才会进行存储。请使用具有最小权限范围的专用 API 密钥。该密钥仅用于调用 Linear API，且不会被传输到其他地方。建议使用环境变量（`LINEAR_API_KEY`）来避免数据持久化。

> **审计信息：** 该技能仅向 `api.linear.app`（Linear 的官方 GraphQL API）发送 HTTPS 请求，不会将任何数据发送到其他地方。具体实现细节请参见 `src/linear_todos/api.py` 文件。

## 所需凭证

| 变量        | 是否必需 | 说明                          |
|--------------|---------|--------------------------------------|
| `LINEAR_API_KEY`    | 是        | 来自 [linear.app/settings/api](https://linear.app/settings/api) 的 Linear API 密钥 |
| `LINEAR_team_ID`   | 否        | 默认的待办事项团队 ID                |
| `LINEAR_STATE_ID`   | 否        | 新待办事项的默认状态                |
| `LINEAR_DONE_STATE_ID` | 否        | 已完成的待办事项的状态                |

**配置文件路径：** `~/.config/linear-todos/config.json`（由 `setup` 命令创建，权限设置为 0o600）

## 安全性与审计

### 该技能的功能

- **HTTP 请求：** 仅向 `https://api.linear.appgraphql`（Linear 的官方 API）发送 HTTPS 请求，不涉及任何遥测数据或第三方服务。
- **数据存储：** 仅在您执行 `setup` 命令时，才会将 API 密钥和配置信息以明文形式存储在 `~/.config/linear-todos/config.json` 文件中（权限设置为 0o600）。团队/任务数据每次运行时都会重新获取，不会被缓存到本地。
- **运行时行为：** 该技能通过捆绑的 Python 源代码运行（而非预安装的系统工具）。当您通过 CLI 调用命令时，它会执行 `main.py` 以及 `src/linear_todos/` 目录中的代码。
- **设置流程：** 在交互式设置过程中，向导会临时将 `LINEAR_API_KEY` 设置在进程环境中以进行测试，但这种设置不会被持久化。
- **自动启用：** 该技能不会自动请求系统权限（默认设置为 `false`），也不会自动为所有代理启用。
- **代码位置：**
  - `src/linear_todos/api.py`：处理所有针对 Linear 的 HTTP 请求
  - `src/linear_todos/config.py`：处理配置文件
  - `src/linear_todos/setup_wizard.py`：实现交互式设置流程
  - `src/linear_todos/cli.py`：包含 CLI 命令

### 推荐的安全实践

1. **使用专用 API 密钥：** 为该技能创建一个具有最小权限范围的专用 Linear API 密钥。如果卸载或停止使用该技能，请及时撤销该密钥。
2. **优先使用环境变量：** 将 `LINEAR_API_KEY` 设置在 shell 环境变量中，避免生成明文配置文件。
3. **审核代码：** 在首次使用前，请仔细检查 `src/linear_todos/api.py` 文件，确保 HTTP 请求的目标地址是正确的。
4. **在隔离环境中进行初始设置：** 如果不确定该技能的行为，请在容器或虚拟机中运行设置流程以进行测试。

### Cron 作业（可选）

`cron-jobs.txt` 文件包含每日任务摘要的示例 cron 任务。**这些任务不会自动安装**，需要您手动添加。

**推荐替代方案：** 使用 OpenClaw 内置的 cron 功能，而不是系统自带的 crontab 功能：
```bash
openclaw cron add --name "morning-digest" --schedule "0 8 * * *" \
  --payload "linear-todos digest" --session-target isolated
```

OpenClaw 是一个基于 Linear 构建的强大待办事项管理系统，支持智能日期解析、优先级设置以及完整的 CLI 工作流程。

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

## 设置流程

### 1. 获取 API 密钥

从 [linear.app/settings/api](https://linear.app/settings/api) 获取您的 API 密钥。**建议：** 为该技能创建一个具有最小权限范围的专用 API 密钥。

### 2. 运行设置流程

```bash
uv run python main.py setup
```

这个交互式向导将：
- 验证您的 API 密钥
- 列出您的 Linear 团队
- 允许您选择待办事项所属的团队
- 配置待办事项的初始状态和完成状态
- 将设置保存到 `~/.config/linear-todos/config.json` 文件（格式为明文 JSON）

### 3. 手动配置（可选）

您也可以通过设置环境变量来配置该技能：
```bash
export LINEAR_API_KEY="lin_api_..."
export LINEAR_TEAM_ID="your-team-id"
export LINEAR_STATE_ID="your-todo-state-id"
export LINEAR_DONE_STATE_ID="your-done-state-id"
```

或者手动创建 `~/.config/linear-todos/config.json` 文件：
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

创建一个新的待办事项，可指定完成时间、优先级和描述。

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

**完成示例：**
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

列出所有的待办事项。

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

每日执行一次任务审核，按紧急程度对待办事项进行分类。

```bash
uv run python main.py review
```

输出结果包括：
- 🚨 **逾期** - 已过截止日期
- 📅 **今日到期** - 今天到期的任务
- ⚡ **高优先级** - 紧急/高优先级的任务
- 📊 **本周内完成** - 7 天内需要完成的任务
- 📅 **本月内完成** - 28 天内需要完成的任务
- 📝 **无截止日期** - 无具体完成日期的任务

### setup

交互式设置向导，用于配置与 Linear 的集成。

```bash
uv run python main.py setup
```

设置流程包括：
- 验证您的 API 密钥
- 选择所属的 Linear 团队
- 配置待办事项的初始状态和完成状态
- 将设置保存到 `~/.config/linear-todos/config.json`

## 代理端的处理逻辑

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

如果用户未指定优先级，系统会自动分配如下优先级：
- **紧急** (🔥) - 需立即处理的关键任务
- **高** (⚡) - 重要但可以稍后处理的任务
- **普通** (📌) - 标准优先级的任务（默认值）
- **低** (💤) - 可以延迟处理的任务

### 3. 每日任务汇总

当用户询问“今天有什么任务需要处理”时，系统会按照以下格式显示结果：
```bash
uv run python main.py review
```

请确保以原始格式显示结果，不要进行任何格式化或总结。

### 4. 标记任务为已完成

当用户表示某项任务已完成时，系统会将其标记为已完成。

```bash
uv run python main.py done ISSUE-123
```

## 日期解析参考

| 输入            | 解析结果                          |
|-----------------|--------------------------------------------|
| `today`         | 今天                          |
| `tomorrow`        | 明天                          |
| `next Monday`      | 下周的周一                        |
| `this Friday`     | 当前的周五                        |
| `in 3 days`       | 3 天后                          |
| `in 2 weeks`       | 14 天后                          |
| `2025-04-15`      | 具体的日期                        |

## 优先级等级

| 等级 | 数字 | 图标 | 适用场景                        |
|---------|------|---------------------------|
| 紧急     | 1    | 🔥 | 需立即处理的关键任务                |
| 高        | 2    | ⚡ | 重要且时间敏感的任务                |
| 普通       | 3    | 📌 | 标准优先级的任务                    |
| 低        | 4    | 💤 | 可以延迟处理的任务                  |
| 无        | 0    | 📋 | 未设置优先级的任务                  |

## 配置优先级顺序

配置项的加载顺序如下（后面的配置会覆盖之前的设置）：
1. 默认值
2. 配置文件：`~/.config/linear-todos/config.json`
3. 环境变量：`LINEAR_*
4. 命令行参数：`--team`, `--state`

## 相关文件

| 文件          | 用途                          |
|--------------|--------------------------------------------|
| `main.py`       | CLI 的主入口脚本                    |
| `src/linear_todos/cli.py` | 包含所有 CLI 命令的脚本                |
| `src/linear_todos/api.py` | 用于与 Linear API 交互的脚本                |
| `src/linear_todos/config.py` | 配置管理脚本                      |
| `src/linear_todos/dates.py` | 用于日期解析的辅助脚本                |
| `src/linear_todos/setup_wizard.py` | 交互式设置向导脚本                |