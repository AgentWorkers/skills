---
name: clickup-pro
description: 基于人工智能的 ClickUp 项目管理工具：支持任务管理、文件夹组织、时间跟踪、评论功能以及自定义字段的设置。该工具能够根据任务的紧急性和重要性进行智能排序，并自动生成每日站会（daily standup）内容。适用于项目管理、冲刺计划制定以及团队协作。
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+, ClickUp API key
metadata: {"openclaw": {"emoji": "\u2705", "requires": {"env": ["CLICKUP_API_KEY"]}, "primaryEnv": "CLICKUP_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# ✅ ClickUp Pro

这是一个专为 OpenClaw 代理设计的、基于 AI 的任务管理工具。它基于 clickup-api v1.0.3 进行开发，并在任务优先级排序和每日站会生成功能方面进行了大幅改进。

## 与 clickup-api 的主要区别

- **AI 任务优先级排序**：利用大型语言模型（LLM）根据任务的紧急性和重要性为任务评分。
- **每日站会生成器**：自动总结已完成、进行中或被阻塞的任务。
- **时间跟踪**：支持开始/停止时间记录以及时间条目的添加。
- **自定义字段**：可以读取和写入自定义字段。
- **评论**：允许为任务添加评论。
- **完整的 CRUD 操作**：支持对任务、文件夹和列表进行创建、读取、更新和删除操作。

## 必需配置项

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `CLICKUP_API_KEY` | ✅ | ClickUp 个人 API 密钥 |
| `OPENROUTER_API_KEY` | 可选 | 用于 AI 任务优先级排序和生成每日站会 |

## 快速入门

```bash
# List workspaces (teams)
python3 {baseDir}/scripts/clickup_api.py workspaces

# List spaces
python3 {baseDir}/scripts/clickup_api.py spaces <team_id>

# List folders in a space
python3 {baseDir}/scripts/clickup_api.py folders <space_id>

# List lists in a folder
python3 {baseDir}/scripts/clickup_api.py lists <folder_id>

# List tasks in a list
python3 {baseDir}/scripts/clickup_api.py tasks <list_id>

# Create a task
python3 {baseDir}/scripts/clickup_api.py create-task <list_id> --name "Fix bug" --priority 2 --due "2026-02-20"

# Update a task
python3 {baseDir}/scripts/clickup_api.py update-task <task_id> --status "in progress" --assignee user123

# Add comment
python3 {baseDir}/scripts/clickup_api.py comment <task_id> --text "Working on this now"

# Time tracking
python3 {baseDir}/scripts/clickup_api.py start-timer <task_id>
python3 {baseDir}/scripts/clickup_api.py stop-timer <team_id>
python3 {baseDir}/scripts/clickup_api.py log-time <task_id> --duration 3600000 --description "Code review"

# AI prioritize tasks in a list
python3 {baseDir}/scripts/clickup_api.py prioritize <list_id>

# Daily standup summary
python3 {baseDir}/scripts/clickup_api.py standup <list_id>
```

## 命令

### 导航
- `workspaces`：列出所有工作空间/团队。
- `spaces <team_id>`：列出特定工作空间内的所有文件夹。
- `folders <space_id>`：列出特定工作空间内的所有文件夹。
- `lists <folder_id>`：列出特定文件夹内的所有任务列表（也可以使用 `folderless-lists <space_id>`）。

### 任务管理
- `tasks <list_id>`：列出任务列表（支持使用 `--status`、`--assignee`、`--subtasks` 等筛选条件）。
- `get-task <task_id>`：获取任务详情。
- `create-task <list_id>`：创建新任务（支持设置 `--name`、`--description`、`--priority`（1-4）、`--due DATE`、`--assignee` 等参数）。
- `update-task <task_id>`：更新任务信息（支持 `--name`、`--status`、`--priority`、`--due`、`--assignee` 等参数）。
- `delete-task <task_id>`：删除任务。

### 时间跟踪
- `start-timer <task_id>`：开始记录任务时间。
- `stop-timer <team_id>`：停止当前任务的时间记录。
- `log-time <task_id>`：记录时间条目（支持指定 `--duration MS` 和 `--description`）。

### 评论
- `comment <task_id>`：为任务添加评论。

### AI 功能（需要 `OPENROUTER_API_KEY`）
- `prioritize <list_id>`：利用 AI 根据任务的紧急性和重要性对任务进行排序，并生成排名列表。
- `standup <list_id>`：生成每日站会报告（显示已完成、进行中或被阻塞的任务）。

## 开发者信息

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)