---
name: sunsama
description: >
  **Sunsama MCP与受管理认证的集成**  
  支持用户管理日常任务、日历事件、待办事项、目标以及时间跟踪功能。  
  当用户需要通过Sunsama进行任务管理和日常规划时，可使用此功能。  
  对于其他第三方应用程序，建议使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji:
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---
# Sunsama MCP

通过MCP（模型上下文协议，Model Context Protocol）访问Sunsama，并使用受管理的身份验证机制进行访问。

## 快速入门

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'searchTerm': 'meeting'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/sunsama/search_tasks', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/sunsama/{tool-name}
```

请将 `{tool-name}` 替换为实际的MCP工具名称（例如 `search_tasks`）。该网关会代理请求到Sunsama的MCP服务器，并自动注入您的凭据。

## 身份验证

所有请求都需要Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的Sunsama MCP连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=sunsama&method=MCP&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'sunsama', 'method': 'MCP'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接信息

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "connection": {
    "connection_id": "313c5234-8ddb-4be6-b0f2-836a864bed9f",
    "status": "PENDING",
    "creation_time": "2026-03-03T10:44:23.480898Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "sunsama",
    "method": "MCP",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成OAuth授权。

### 删除连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## MCP参考

所有MCP工具都使用 `POST` 方法：

### 任务管理

| 工具 | 描述 | 架构 |
|------|-------------|--------|
| `search_tasks` | 按关键词搜索任务 | [schema](schemas/search_tasks.json) |
| `create_task` | 创建新任务 | [schema](schemas/create_task.json) |
| `edit_task_title` | 更新任务标题 | [schema](schemas/edit_task_title.json) |
| `delete_task` | 删除任务 | [schema](schemas/delete_task.json) |
| `mark_task_as_completed` | 标记任务已完成 | [schema](schemas/mark_task_as_completed.json) |
| `mark_task_as_incomplete` | 标记任务未完成 | [schema](schemas/mark_task_as_incomplete.json) |
| `append_task_notes` | 为任务添加备注 | [schema](schemas/append_task_notes.json) |
| `edit_task_time_estimate` | 设置任务预计完成时间 | [schema](schemas/edit_task_time_estimate.json) |
| `edit_task_recurrence_rule` | 设置任务重复规则 | [schema](schemas/edit_task_recurrence_rule.json) |
| `get_task_time_estimate` | 获取任务的AI预估时间 | [schema](schemas/get_task_time_estimate.json) |
| `restore_task` | 恢复已删除的任务 | [schema](schemas/restore_task.json) |

### 子任务

| 工具 | 描述 | 架构 |
|------|-------------|--------|
| `add_subtasks_to_task` | 为任务添加子任务 | [schema](schemas/add_subtasks_to_task.json) |
| `edit_subtask_title` | 更新子任务标题 | [schema](schemas/edit_subtask_title.json) |
| `mark_subtask_as_completed` | 标记子任务已完成 | [schema](schemas/mark_subtask_as_completed.json) |
| `mark_subtask_as_incomplete` | 标记子任务未完成 | [schema](schemas/mark_subtask_as_incomplete.json) |

### 待办事项

| 工具 | 描述 | 架构 |
|------|-------------|--------|
| `get_backlog_tasks` | 列出待办事项中的任务 | [schema](schemas/get_backlog_tasks.json) |
| `move_task_to_backlog` | 将任务移至待办事项 | [schema](schemas/move_task_to_backlog.json) |
| `move_task_from_backlog` | 从待办事项移出任务 | [schema](schemas/move_task_from_backlog.json) |
| `reposition_task_in_backlog` | 重新排列待办事项中的任务 | [schema](schemas/reposition_task_in_backlog.json) |
| `change_backlog_folder` | 更改任务所属的文件夹 | [schema](schemas/change_backlog_folder.json) |
| `create_braindump_task` | 创建待办事项任务 | [schema](schemas/create_braindump_task.json) |

### 日程安排

| 工具 | 描述 | 架构 |
|------|-------------|--------|
| `move_task_to_day` | 重新安排任务的时间 | [schema](schemas/move_task_to_day.json) |
| `reorder_tasks` | 重新排列当天的任务 | [schema](schemas/reorder_tasks.json) |
| `timebox_a_task_to_calendar` | 为任务设置时间框 | [schema](schemas/timebox_a_task_to_calendar.json) |
| `set_shutdown_time` | 设置每日结束时间 | [schema](schemas/set_shutdown_time.json) |

### 日历事件

| 工具 | 描述 | 架构 |
|------|-------------|--------|
| `create_calendar_event` | 创建日历事件 | [schema](schemas/create_calendar_event.json) |
| `delete_calendar_event` | 删除日历事件 | [schema](schemas/delete_calendar_event.json) |
| `move_calendar_event` | 重新安排事件的时间 | [schema](schemas/move_calendar_event.json) |
| `import_task_from_calendar_event` | 将日历事件导入为任务 | [schema](schemas/import_task_from_calendar_event.json) |
| `set_calendar_event_allow_task_projections` | 切换任务是否可以与其他事件重叠 | [schema](schemas/set_calendar_event_allow_task_projections.json) |
| `accept_meeting_invite` | 接受会议邀请 | [schema](schemas/accept_meeting_invite.json) |
| `decline_meeting_invite` | 拒绝会议邀请 | [schema](schemas/decline_meeting_invite.json) |

### 时间跟踪

| 工具 | 描述 | 架构 |
|------|-------------|--------|
| `start_task_timer` | 启动计时器 | [schema](schemas/start_task_timer.json) |
| `stop_task_timer` | 停止计时器 | [schema](schemas/stop_task_timer.json) |

### 渠道与目标

| 工具 | 描述 | 架构 |
|------|-------------|--------|
| `create_channel` | 创建频道/上下文 | [schema](schemas/create_channel.json) |
| `add_task_to_channel` | 将任务分配到频道 | [schema](schemas/add_task_to_channel.json) |
| `create_weekly_objective` | 创建每周目标 | [schema](schemas/create_weekly_objective.json) |
| `align_task_with_objective` | 将任务与目标关联 | [schema](schemas/align_task_with_objective.json) |

### 归档

| 工具 | 描述 | 架构 |
|------|-------------|--------|
| `get_archived_tasks` | 列出已归档的任务 | [schema](schemas/get_archived_tasks.json) |
| `unarchive_task` | 恢复已归档的任务 | [schema](schemas/unarchive_task.json) |

### 邮件集成

| 工具 | 描述 | 架构 |
|------|-------------|--------|
| `list_email_threads` | 列出邮件线程 | [schema](schemas/list_email_threads.json) |
| `create_follow_up_task_from_email` | 从邮件中创建任务 | [schema](schemas/create_follow_up_task_from_email.json) |
| `delete_email_thread` | 删除邮件线程 | [schema](schemas/delete_email_thread.json) |
| `mark_email_thread_as_read` | 标记邮件为已读 | [schema](schemas/mark_email_thread_as_read.json) |

### 循环任务

| 工具 | 描述 | 架构 |
|------|-------------|--------|
| `delete_all_incomplete_recurring_task_instances` | 删除所有未完成的循环任务实例 | [schema](schemas/delete_all_incomplete_recurring_task_instances.json) |
| `update_all_incomplete_recurring_task_instances` | 更新所有未完成的循环任务实例 | [schema](schemas/update_all_incomplete_recurring_task_instances.json) |

### 设置与偏好

| 工具 | 描述 | 架构 |
|------|-------------|--------|
| `toggle_auto_import_events` | 切换事件自动导入功能 | [schema](schemas/toggle_auto_import_events.json) |
| `update_calendar_preferences` | 更新日历设置 | [schema](schemas/update_calendar_preferences.json) |
| `update_import_event_filters` | 设置事件导入过滤器 | [schema](schemas/update_import_event_filters.json) |
| `log_user_feedback` | 提交用户反馈 | [schema](schemas/log_user_feedback.json) |

---

## 常见端点

### 搜索任务

按关键词搜索任务：
```bash
POST /sunsama/search_tasks
Content-Type: application/json

{
  "searchTerm": "meeting"
}
```

**响应：**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"tasks\":[{\"_id\":\"69a6bf3a04d3cd0001595308\",\"title\":\"Team meeting prep\",\"scheduledDate\":\"2026-03-03\",\"completed\":false}]}"
    }
  ],
  "isError": false
}
```

### 创建任务

创建一个计划在未来特定日期执行的新任务：
```bash
POST /sunsama/create_task
Content-Type: application/json

{
  "title": "Review quarterly report",
  "day": "2026-03-03",
  "alreadyInTaskList": false
}
```

**响应：**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"success\":true,\"task\":{\"_id\":\"69a6bf3a04d3cd0001595308\",\"title\":\"Review quarterly report\",\"notes\":\"\",\"timeEstimate\":\"20 minutes\",\"sortOrder\":-1772535610535,\"isPersonal\":false,\"isWork\":true,\"isPrivate\":false,\"isArchived\":false,\"completed\":false,\"isBacklogged\":false,\"scheduledDate\":\"2026-03-03\",\"subtasks\":[],\"channel\":\"work\",\"folder\":null,\"timeboxEventIds\":[]}}"
    }
  ],
  "isError": false
}
```

### 获取待办事项中的任务

列出所有待办事项中的任务：
```bash
POST /sunsama/get_backlog_tasks
Content-Type: application/json

{}
```

**响应：**
```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"tasks\":[],\"queryId\":\"bb7d004a-0b29-49d9-8345-6d9037786fbb\",\"totalPages\":1}"
    }
  ],
  "isError": false
}
```

### 标记任务为已完成

```bash
POST /sunsama/mark_task_as_completed
Content-Type: application/json

{
  "taskId": "69a6bf3a04d3cd0001595308",
  "finishedDay": "2026-03-03"
}
```

### 为任务添加子任务

```bash
POST /sunsama/add_subtasks_to_task
Content-Type: application/json

{
  "taskId": "69a6bf3a04d3cd0001595308",
  "subtasks": [
    {"title": "Step 1: Research"},
    {"title": "Step 2: Draft outline"},
    {"title": "Step 3: Review"}
  ]
}
```

### 创建日历事件

```bash
POST /sunsama/create_calendar_event
Content-Type: application/json

{
  "title": "Team standup",
  "startDate": "2026-03-03T09:00:00"
}
```

### 将任务移至当天

将任务重新安排到不同的日期：
```bash
POST /sunsama/move_task_to_day
Content-Type: application/json

{
  "taskId": "69a6bf3a04d3cd0001595308",
  "calendarDay": "2026-03-04"
}
```

### 为任务设置时间框

在日历中为任务设置时间框：
```bash
POST /sunsama/timebox_a_task_to_calendar
Content-Type: application/json

{
  "taskId": "69a6bf3a04d3cd0001595308",
  "startDate": "2026-03-03",
  "startTime": "14:00"
}
```

### 创建每周目标

```bash
POST /sunsama/create_weekly_objective
Content-Type: application/json

{
  "title": "Complete Q1 planning",
  "weekStartDay": "2026-03-03"
}
```

### 创建待办事项任务（带有时间限制）

创建一个带有时间限制的待办事项任务：
```bash
POST /sunsama/create_braindump_task
Content-Type: application/json

{
  "title": "Research new tools",
  "timeBucket": "in the next month"
}
```

**时间限制选项：**
- `"在接下来的两周内"`
- `"在接下来的一个月内"`
- `"在接下来的一个季度内"`
- `"在接下来的一年内"`
- `"在某个日期"`
- `"从不"`

### 启动/停止任务计时器

```bash
POST /sunsama/start_task_timer
Content-Type: application/json

{
  "taskId": "69a6bf3a04d3cd0001595308"
}
```

```bash
POST /sunsama/stop_task_timer
Content-Type: application/json

{
  "taskId": "69a6bf3a04d3cd0001595308"
}
```

### 设置工作日结束时间

设置您的工作日结束时间：
```bash
POST /sunsama/set_shutdown_time
Content-Type: application/json

{
  "calendarDay": "2026-03-03",
  "hour": 18,
  "minute": 0
}
```

## 代码示例

### JavaScript

```javascript
const response = await fetch('https://gateway.maton.ai/sunsama/search_tasks', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`
  },
  body: JSON.stringify({
    searchTerm: 'meeting'
  })
});
const data = await response.json();
console.log(data);
```

### Python

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/sunsama/search_tasks',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'searchTerm': 'meeting'
    }
)
print(response.json())
```

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 无法建立MCP连接或工具名称无效 |
| 401 | Maton API密钥无效或缺失 |
| 429 | 请求次数达到限制 |

### 故障排除：API密钥问题

1. 确保 `MATON_API_KEY` 环境变量已设置：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证API密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 注意事项

- 所有任务ID都是MongoDB ObjectIds（24个字符的十六进制字符串）。
- 日期格式：日期使用 `YYYY-MM-DD`，时间使用ISO 8601格式。
- MCP工具的响应内容采用 `{"content": [{"type": "text", "text": "..."}, "isError": false}` 的格式。
- `text` 字段包含需要解析的JSON字符串数据。
- 时间估计以人类可读的字符串形式返回（例如：“20分钟”）。

## 资源

- [Sunsama](https://sunsama.com)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)