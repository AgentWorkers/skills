---
name: tasknotes
description: 通过 TaskNotes 插件 API 在 Obsidian 中管理任务。当用户需要创建任务、列出任务、按状态或项目查询任务、更新任务状态、删除任务或查看自己需要完成的任务时，可以使用该 API。
---

# TaskNotes 技能

通过 TaskNotes 插件的 HTTP API 管理 Obsidian 任务。

## 要求

1. Obsidian 中已安装 TaskNotes 插件。
2. 在 TaskNotes 设置中启用 HTTP API：
   - 打开 Obsidian 设置 → TaskNotes
   - 勾选“启用 HTTP API”选项
   - 设置 API 端口（默认：8080）
   - API 令牌：如不需要认证则留空；如需要认证，请设置一个令牌
3. 在 vault 根目录下的 `.env` 文件中设置环境变量（如果使用认证）：
   ```
   TASKNOTES_API_PORT=8080
   TASKNOTES_API_KEY=your_token_here
   ```
   如果 TaskNotes 未设置认证令牌，则不需要 `.env` 文件。

## 命令行接口（CLI）命令

```bash
# List all tasks
uv run scripts/tasks.py list

# List by status (use your configured status values)
uv run scripts/tasks.py list --status "in-progress"

# List by project
uv run scripts/tasks.py list --project "My Project"

# Create task
uv run scripts/tasks.py create "Task title" --project "My Project" --priority high

# Create task with scheduled time
uv run scripts/tasks.py create "Meeting prep" --scheduled "2025-01-15T14:00:00"

# Update task status
uv run scripts/tasks.py update "Tasks/task-file.md" --status done

# Add/update task description
uv run scripts/tasks.py update "Tasks/task-file.md" --details "Additional context here."

# Delete task
uv run scripts/tasks.py delete "Tasks/task-file.md"

# Get available options (statuses, priorities, projects)
uv run scripts/tasks.py options --table

# Human-readable output (add --table)
uv run scripts/tasks.py list --table
```

## 任务属性

**状态和优先级值：** 在 TaskNotes 插件设置中进行配置。运行 `options` 命令可查看可用值：
```bash
uv run scripts/tasks.py options --table
```

**其他字段：**
- `projects` - 项目链接数组，例如 `["[[项目名称]]"]`
- `contexts` - 类似 `["办公室", "高能耗"]` 的数组
- `due` - 截止日期（YYYY-MM-DD）
- `scheduled` - 计划日期/时间（YYYY-MM-DD 或 YYYY-MM-DDTHH:MM:SS）
- `timeEstimate` - 预计完成时间（分钟）
- `tags` - 标签数组
- `details` - 任务描述（写入 markdown 正文部分，而非前置内容）

## API 参考

基础 URL：`http://localhost:8080/api`

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| GET | /tasks | 列出任务（支持过滤） |
| POST | /tasks | 创建任务 |
| GET | /tasks/{id} | 获取单个任务 |
| PUT | /tasks/{id} | 更新任务 |
| DELETE | /tasks/{id} | 删除任务 |
| GET | /filter-options | 可用的状态、优先级、项目列表 |

### GET /tasks 的查询参数

- `status` - 按状态过滤
- `project` - 按项目名称过滤
- `priority` - 按优先级过滤
- `tag` - 按标签过滤
- `overdue` - 是否逾期（true/false）
- `sort` - 排序字段
- `limit` - 最大结果数量
- `offset` - 分页偏移量

## 使用场景

- “为 X 创建任务” → 创建任务
- “显示我的任务” → 列出所有任务
- “显示进行中的任务” → 列出状态为“进行中”的任务
- “将 X 标记为已完成” → 将任务状态更新为已完成
- “我应该做什么” → 按状态列出任务

## 示例工作流程

```bash
# Morning: Check what to work on
uv run scripts/tasks.py list --status in-progress --table
uv run scripts/tasks.py list --limit 5 --table

# Create task linked to project
uv run scripts/tasks.py create "Finish landing page" \
  --project "Website Redesign" \
  --priority high

# Complete a task
uv run scripts/tasks.py update "Tasks/finish-landing-page.md" --status done
```