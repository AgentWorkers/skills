---
name: todoist
description: >
  **通过自然语言与 Todoist 任务管理工具集成**  
  当用户希望通过对话式命令（如“显示我今天的任务”、“将‘看牙医’添加到我的待办事项列表中”、“完成关于会议的任务”）来管理 Todoist 任务或项目时，可以使用此功能。这些命令可以涉及 Todoist、任务、截止日期或项目管理等相关内容。
credentials:
  - name: TODOIST_API_KEY
    description: Todoist API token from https://todoist.com/app/settings/integrations/developer
    required: true
    sensitive: true
---
# Todoist 技能 — 自然语言任务管理

通过自然语言与 Todoist 任务进行交互。无需记住命令行（CLI）的语法，只需简单地描述您的任务即可。

## 自然语言示例

该技能能够理解以下自然语言指令：

**列出任务：**
- “我今天有哪些任务？”
- “显示我这周的 Todoist 任务列表”
- “哪些任务已经逾期了？”
- “显示优先级为 1 的任务”

**添加任务：**
- “在我的待办事项列表中添加‘买牛奶’”
- “创建一个明天去看牙医的任务”
- “我需要在周五之前审阅第四季度的报告”
- “添加一个每周例会的任务”

**完成任务：**
- “完成关于看牙医的任务”
- “将‘买牛奶’的任务标记为已完成”
- “我已经完成了报告”

**管理项目：**
- “我在 Todoist 中有哪些项目？”
- “显示‘工作’项目中的任务”

## 先决条件

- 必须将 `TODOIST_API_KEY` 环境变量设置为您的 Todoist API 令牌
- 请在以下链接获取您的令牌：https://todoist.com/app/settings/integrations/developer

## 技术使用方法

如果您更喜欢使用命令行命令或需要编写脚本，请直接使用 Python 脚本：

```bash
# List today's tasks
python3 todoist/scripts/todoist.py list --filter "today"

# Add a task
python3 todoist/scripts/todoist.py add "Buy milk" --due "tomorrow" --priority 2

# Complete a task by ID
python3 todoist/scripts/todoist.py complete "TASK_ID"

# List all projects
python3 todoist/scripts/todoist.py projects
```

## 过滤语法

通过自然语言或命令行过滤任务时，可以使用以下关键词：

- `today` — 今日到期的任务
- `overdue` — 过期的任务
- `tomorrow` — 明天到期的任务
- `p1`, `p2`, `p3`, `p4` — 优先级过滤器
- `7 days` — 下 7 天内到期的任务
- `@label` — 具有特定标签的任务
- `#project` — 属于某个项目的任务
- 可以使用 `&`（与）和 `|`（或）组合过滤条件：`today & p1`

## 优先级级别

- `1` — 紧急（红色）
- `2` — 高优先级（橙色）
- `3` — 中等优先级（蓝色）
- `4` — 低优先级（白色/灰色，默认值）

## 功能特点

- ✅ 支持自然语言任务管理
- ✅ 兼容时区设置，能够正确解析“今天”这样的时间表达
- ✅ 智能过滤功能（排除已完成的任务）
- ✅ 支持重复性任务
- ✅ 完全兼容 Todoist API v1 的所有功能

## 响应格式

该脚本会输出 JSON 格式的数据，便于程序化使用。有关完整的 API 文档，请参阅 `references/api.md`。

## 注意事项

- 该技能会自动过滤掉已完成的任务
- “今天”这个时间表达会使用您的本地时区设置（如需调整，请设置 `TZ` 环境变量）
- 自然语言中的日期（如“明天”、“下周五”）会使用 Todoist 的内置解析功能