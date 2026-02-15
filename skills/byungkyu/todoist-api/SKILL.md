---
name: todoist
description: |
  Todoist API integration with managed OAuth. Manage tasks, projects, sections, labels, and comments. Use this skill when users want to create, update, complete, or organize tasks and projects in Todoist. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Todoist

您可以使用受管理的OAuth认证来访问Todoist REST API v2，从而管理任务、项目、章节、标签和评论。

## 快速入门

```bash
# List all tasks
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/todoist/rest/v2/tasks')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/todoist/rest/v2/{resource}
```

该网关会将请求代理到`api.todoist.com/rest/v2`，并自动插入您的OAuth令牌。

## 认证

所有请求都必须在`Authorization`头部包含Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为`MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取您的API密钥

1. 在[maton.ai](https://maton.ai)上登录或创建账户。
2. 转到[maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在`https://ctrl.maton.ai`上管理您的Todoist OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=todoist&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'todoist'}).encode()
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
    "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "todoist",
    "metadata": {}
  }
}
```

在浏览器中打开返回的`url`以完成OAuth认证。

### 删除连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 指定连接

如果您有多个Todoist连接，请使用`Maton-Connection`头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/todoist/rest/v2/tasks')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略，则网关将使用默认的（最旧的）活动连接。

## API参考

### 项目

#### 列出项目

```bash
GET /todoist/rest/v2/projects
```

**响应：**
```json
[
  {
    "id": "2366738772",
    "name": "Inbox",
    "color": "charcoal",
    "parent_id": null,
    "order": 0,
    "is_shared": false,
    "is_favorite": false,
    "is_inbox_project": true,
    "view_style": "list",
    "url": "https://app.todoist.com/app/project/..."
  }
]
```

#### 获取项目信息

```bash
GET /todoist/rest/v2/projects/{id}
```

#### 创建项目

```bash
POST /todoist/rest/v2/projects
Content-Type: application/json

{
  "name": "My Project",
  "color": "blue",
  "is_favorite": true,
  "view_style": "board"
}
```

**参数：**
- `name`（必填）- 项目名称
- `parent_id`- 父项目ID（用于嵌套）
- `color`- 项目颜色（例如：“red”、“blue”、“green”）
- `is_favorite`- 喜欢状态（布尔值）
- `view_style`- “list”或“board”（默认：list）

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'name': 'My New Project', 'color': 'blue'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/todoist/rest/v2/projects', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 更新项目

```bash
POST /todoist/rest/v2/projects/{id}
Content-Type: application/json

{
  "name": "Updated Project Name",
  "color": "red"
}
```

#### 删除项目

```bash
DELETE /todoist/rest/v2/projects/{id}
```

成功时返回204（No Content）。

#### 获取项目协作者

```bash
GET /todoist/rest/v2/projects/{id}/collaborators
```

### 任务

#### 列出任务

```bash
GET /todoist/rest/v2/tasks
```

**查询参数：**
| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `project_id` | string | 按项目过滤 |
| `section_id` | string | 按章节过滤 |
| `label` | string | 按标签名称过滤 |
| `filter` | string | Todoist过滤表达式 |
| `ids` | string | 用逗号分隔的任务ID |

**响应：**
```json
[
  {
    "id": "9993408170",
    "content": "Buy groceries",
    "description": "",
    "project_id": "2366834771",
    "section_id": null,
    "parent_id": null,
    "order": 1,
    "priority": 2,
    "is_completed": false,
    "labels": [],
    "due": {
      "date": "2026-02-07",
      "string": "tomorrow",
      "lang": "en",
      "is_recurring": false
    },
    "url": "https://app.todoist.com/app/task/9993408170",
    "comment_count": 0,
    "created_at": "2026-02-06T20:41:08.449320Z"
  }
]
```

#### 获取任务信息

```bash
GET /todoist/rest/v2/tasks/{id}
```

#### 创建任务

```bash
POST /todoist/rest/v2/tasks
Content-Type: application/json

{
  "content": "Buy groceries",
  "project_id": "2366834771",
  "priority": 2,
  "due_string": "tomorrow at 10am",
  "labels": ["shopping", "errands"]
}
```

**必填字段：**
- `content` - 任务内容/标题

**可选字段：**
- `description` - 任务描述
- `project_id` - 要添加任务的项目（默认为Inbox）
- `section_id` - 项目内的章节
- `parent_id` - 子任务的父任务ID
- `labels` - 标签名称数组
- `priority` - 1（普通）到4（紧急）
- `due_string` - 自然语言截止日期（例如：“tomorrow”、“next Monday 3pm”）
- `due_date` - ISO格式（YYYY-MM-DD）
- `due_datetime` - 带时区的RFC3339格式
- `assignee_id` - 分配任务的用户ID
- `duration` - 任务持续时间（整数）
- `duration_unit` - “minute”或“day”

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    'content': 'Complete project report',
    'priority': 4,
    'due_string': 'tomorrow at 5pm',
    'labels': ['work', 'urgent']
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/todoist/rest/v2/tasks', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 更新任务

```bash
POST /todoist/rest/v2/tasks/{id}
Content-Type: application/json

{
  "content": "Updated task content",
  "priority": 3
}
```

#### 完成任务（Close Task）

```bash
POST /todoist/rest/v2/tasks/{id}/close
```

返回204（No Content）。对于重复任务，这将安排下一次任务发生的时间。

#### 重新打开任务（Reopen Task）

```bash
POST /todoist/rest/v2/tasks/{id}/reopen
```

返回204（No Content）。

#### 删除任务

```bash
DELETE /todoist/rest/v2/tasks/{id}
```

返回204（No Content）。

### 章节

#### 列出章节

```bash
GET /todoist/rest/v2/sections
GET /todoist/rest/v2/sections?project_id={project_id}
```

**响应：**
```json
[
  {
    "id": "214670251",
    "project_id": "2366834771",
    "order": 1,
    "name": "To Do"
  }
]
```

#### 获取章节信息

```bash
GET /todoist/rest/v2/sections/{id}
```

#### 创建章节

```bash
POST /todoist/rest/v2/sections
Content-Type: application/json

{
  "name": "In Progress",
  "project_id": "2366834771",
  "order": 2
}
```

**必填字段：**
- `name` - 章节名称
- `project_id` - 父项目ID

#### 更新章节

```bash
POST /todoist/rest/v2/sections/{id}
Content-Type: application/json

{
  "name": "Updated Section Name"
}
```

#### 删除章节

```bash
DELETE /todoist/rest/v2/sections/{id}
```

返回204（No Content）。

### 标签

#### 列出标签

```bash
GET /todoist/rest/v2/labels
```

**响应：**
```json
[
  {
    "id": "2182980313",
    "name": "urgent",
    "color": "red",
    "order": 1,
    "is_favorite": false
  }
]
```

#### 获取标签信息

```bash
GET /todoist/rest/v2/labels/{id}
```

#### 创建标签

```bash
POST /todoist/rest/v2/labels
Content-Type: application/json

{
  "name": "work",
  "color": "blue",
  "is_favorite": true
}
```

**参数：**
- `name`（必填）- 标签名称
- `color` - 标签颜色
- `order` - 排序顺序
- `is_favorite` - 喜欢状态（布尔值）

#### 更新标签

```bash
POST /todoist/rest/v2/labels/{id}
Content-Type: application/json

{
  "name": "updated-label",
  "color": "green"
}
```

#### 删除标签

```bash
DELETE /todoist/rest/v2/labels/{id}
```

返回204（No Content）。

### 评论

#### 列出评论

```bash
GET /todoist/rest/v2/comments?task_id={task_id}
GET /todoist/rest/v2/comments?project_id={project_id}
```

**注意：** 必须提供`task_id`或`project_id`。

**响应：**
```json
[
  {
    "id": "3966541561",
    "task_id": "9993408170",
    "project_id": null,
    "content": "This is a comment",
    "posted_at": "2026-02-06T20:41:35.734376Z",
    "posted_by_id": "57402826"
  }
]
```

#### 获取评论信息

```bash
GET /todoist/rest/v2/comments/{id}
```

#### 创建评论

```bash
POST /todoist/rest/v2/comments
Content-Type: application/json

{
  "task_id": "9993408170",
  "content": "Don't forget to check the budget"
}
```

**必填字段：**
- `content` - 评论内容
- `task_id` 或 `project_id` - 评论要附加到的任务/项目

#### 更新评论

```bash
POST /todoist/rest/v2/comments/{id}
Content-Type: application/json

{
  "content": "Updated comment text"
}
```

#### 删除评论

```bash
DELETE /todoist/rest/v2/comments/{id}
```

返回204（No Content）。

## 优先级值

| 优先级 | 含义 |
|----------|---------|
| 1 | 普通（默认） |
| 2 | 中等 |
| 3 | 高 |
| 4 | 紧急 |

## 截止日期格式

每次请求请使用以下格式之一：

- `due_string` - 自然语言格式：例如：“tomorrow”、“next Monday at 3pm”、“every week”
- `due_date` - 仅日期格式：例如：“2026-02-15”
- `due_datetime` - 完整的日期时间格式：例如：“2026-02-15T14:00:00Z”

## 代码示例

### JavaScript

```javascript
// Create a task
const response = await fetch('https://gateway.maton.ai/todoist/rest/v2/tasks', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    content: 'Review pull request',
    priority: 3,
    due_string: 'today at 5pm'
  })
});
const task = await response.json();
```

### Python

```python
import os
import requests

# Create a task
response = requests.post(
    'https://gateway.maton.ai/todoist/rest/v2/tasks',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={
        'content': 'Review pull request',
        'priority': 3,
        'due_string': 'today at 5pm'
    }
)
task = response.json()
```

## 注意事项

- 任务ID和项目ID是字符串，而不是整数。
- 优先级4表示最高优先级（紧急），优先级1表示普通优先级。
- 每次请求只能使用一种截止日期格式（`due_string`、`due_date`或`due_datetime`）。
- 完成重复任务会安排下一次任务的发生时间。
- 无法删除Inbox项目。
- 重要提示：当将curl输出传递给`jq`或其他命令时，在某些shell环境中，环境变量（如`$MATON_API_KEY`）可能无法正确展开。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 204 | 成功（无内容） - 用于完成、重新打开或删除操作 |
| 400 | 无效请求或缺少Todoist连接 |
| 401 | 无效或缺少Maton API密钥 |
| 404 | 资源未找到 |
| 429 | 请求速率限制 |
| 4xx/5xx | 来自Todoist API的传递错误 |

### 故障排除：API密钥问题

1. 确保设置了`MATON_API_KEY`环境变量：

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

### 故障排除：应用程序名称无效

1. 确保您的URL路径以`todoist`开头。例如：
- 正确：`https://gateway.maton.ai/todoist/rest/v2/tasks`
- 错误：`https://gateway.maton.ai/rest/v2/tasks`

## 资源

- [Todoist REST API v2文档](https://developer.todoist.com/rest/v2)
- [Todoist API v1文档](https://developer.todoist.com/api/v1)
- [Todoist过滤语法](https://todoist.com/help/articles/introduction-to-filters)
- [Todoist OAuth文档](https://developer.todoist.com/guides/#oauth)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)