---
name: todoist
description: 通过 Todoist CLI 扩展程序来管理 Todoist 任务、项目、标签和评论。当用户需要添加任务、查看待办事项列表、完成任务、管理项目或与他们的 Todoist 账户进行交互时，可以使用该工具。
---

# Todoist CLI

通过 REST API v2 管理 Todoist。

## 设置

1. 获取 API 令牌：进入 Todoist → 设置 → 集成 → 开发者 → API 令牌
2. 设置环境变量：
   ```bash
   export TODOIST_API_TOKEN="your_token_here"
   ```
3. 使 CLI 可执行：
   ```bash
   chmod +x ~/clawd/skills/todoist/scripts/todoist
   ```

## CLI 所在位置

```bash
~/clawd/skills/todoist/scripts/todoist
```

## 快速参考

### 任务
```bash
# List all tasks
todoist tasks

# List with filter
todoist tasks --filter "today"
todoist tasks --filter "overdue"
todoist tasks --filter "#Work"
todoist tasks --project PROJECT_ID

# Quick views
todoist today
todoist overdue
todoist upcoming

# Get single task
todoist task TASK_ID

# Add task
todoist add "Buy groceries"
todoist add "Call mom" --due tomorrow
todoist add "Meeting prep" --due "today 3pm" --priority 4
todoist add "Review PR" --project PROJECT_ID --labels "work,urgent"
todoist add "Write docs" --description "Include examples"

# Update task
todoist update TASK_ID --content "New title"
todoist update TASK_ID --due "next monday"
todoist update TASK_ID --priority 3

# Complete / reopen / delete
todoist complete TASK_ID
todoist reopen TASK_ID
todoist delete-task TASK_ID
```

### 项目
```bash
# List projects
todoist projects

# Get project
todoist project PROJECT_ID

# Create project
todoist add-project "Work"
todoist add-project "Personal" --color blue --favorite

# Update project
todoist update-project PROJECT_ID --name "New Name"
todoist update-project PROJECT_ID --color red

# Delete project
todoist delete-project PROJECT_ID
```

### 分类
```bash
# List sections
todoist sections
todoist sections PROJECT_ID

# Create section
todoist add-section --name "In Progress" --project PROJECT_ID

# Delete section
todoist delete-section SECTION_ID
```

### 标签
```bash
# List labels
todoist labels

# Create label
todoist add-label "urgent"
todoist add-label "blocked" --color red

# Delete label
todoist delete-label LABEL_ID
```

### 评论
```bash
# List comments
todoist comments --task TASK_ID
todoist comments --project PROJECT_ID

# Add comment
todoist add-comment "Need more info" --task TASK_ID

# Delete comment
todoist delete-comment COMMENT_ID
```

## 过滤语法

Todoist 支持强大的过滤查询：

| 过滤条件 | 描述 |
|---------|---------|
| `today`   | 今天到期的任务 |
| `tomorrow` | 明天到期的任务 |
| `overdue` | 已逾期的任务 |
| `7 days` | 7 天内到期的任务 |
| `no date` | 无到期日期的任务 |
| `#ProjectName` | 属于特定项目的任务 |
| `@label` | 带有指定标签的任务 |
| `p1`, `p2`, `p3`, `p4` | 优先级级别 |
| `assigned to: me` | 分配给你的任务 |
| `created: today` | 今天创建的任务 |

可以使用 `&`（与）或 `|`（或）组合多个过滤条件：
```bash
todoist tasks --filter "today & #Work"
todoist tasks --filter "overdue | p1"
```

## 到期日期格式

支持的到期日期格式：
- `today`, `tomorrow`, `yesterday`
- `next monday`, `next week`
- `in 3 days` | 3 天后
- `every day`, `every weekday` | 每天
- `every monday at 9am` | 每周一上午 9 点
- `Jan 15`, `2026-01-20` | 2026 年 1 月 15 日
- `today at 3pm` | 今天下午 3 点

## 优先级级别

| 优先级 | 含义 |
|--------|---------|
| 1       | 普通（默认） |
| 2       | 中等 |
| 3       | 高     |
| 4       | 紧急     |

## 输出结果

所有命令的输出均为 JSON 格式。可以使用 `jq` 工具进行格式化：
```bash
todoist tasks | jq '.[] | {id, content, due: .due.string}'
todoist today | jq -r '.[].content'
```

## 注意事项

- 需要安装 `curl` 和 `jq` 工具
- 所有输出均为 JSON 格式，便于脚本编写
- 任务 ID 为数字字符串（例如 "8765432109")
- 项目 ID 也为数字字符串