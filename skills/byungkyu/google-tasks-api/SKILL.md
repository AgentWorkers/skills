---
name: google-tasks
description: |
  Google Tasks API integration with managed OAuth. Manage task lists and tasks with full CRUD operations.
  Use this skill when users want to read, create, update, or delete tasks and task lists in Google Tasks.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Google Tasks

通过托管的 OAuth 认证来访问 Google Tasks API。您可以执行完整的 CRUD 操作（创建、读取、更新和删除）来管理任务列表和任务。

## 快速入门

```bash
# List all task lists
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-tasks/tasks/v1/users/@me/lists')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/google-tasks/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Google Tasks API 端点路径。该网关会将请求代理到 `tasks.googleapis.com` 并自动插入您的 OAuth 令牌。

## 认证

所有请求都需要在 `Authorization` 标头中包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取您的 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Google Tasks OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-tasks&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-tasks'}).encode()
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
    "connection_id": "0e13cacd-cec8-4b6b-9368-c62cc9b06dd9",
    "status": "ACTIVE",
    "creation_time": "2026-02-07T02:35:51.002199Z",
    "last_updated_time": "2026-02-07T05:32:30.369186Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "google-tasks",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成 OAuth 认证。

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

如果您有多个 Google Tasks 连接，请使用 `Maton-Connection` 标头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-tasks/tasks/v1/users/@me/lists')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '0e13cacd-cec8-4b6b-9368-c62cc9b06dd9')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此参数，网关将使用默认的（最旧的）活动连接。

## API 参考

### 任务列表

#### 列出所有任务列表

```bash
GET /google-tasks/tasks/v1/users/@me/lists
```

**查询参数：**
- `maxResults` - 返回的任务列表的最大数量（默认：20，最大值：100）
- `pageToken` - 分页令牌

**响应：**
```json
{
  "kind": "tasks#taskLists",
  "etag": "\"OW7pv01-vgQ\"",
  "items": [
    {
      "kind": "tasks#taskList",
      "id": "MDEzMTQ2ODk4NDc2ODkyOTIyMTE6MDow",
      "etag": "\"Yz7ljQZ5Xuw\"",
      "title": "My Tasks",
      "updated": "2023-09-18T06:12:59.468Z",
      "selfLink": "https://www.googleapis.com/tasks/v1/users/@me/lists/MDEzMTQ2ODk4NDc2ODkyOTIyMTE6MDow"
    }
  ]
}
```

#### 获取任务列表

```bash
GET /google-tasks/tasks/v1/users/@me/lists/{tasklistId}
```

#### 创建任务列表

```bash
POST /google-tasks/tasks/v1/users/@me/lists
Content-Type: application/json

{
  "title": "New Task List"
}
```

**响应：**
```json
{
  "kind": "tasks#taskList",
  "id": "OFYyU09veWMyWl84SjNQXw",
  "etag": "\"XTqLSxP4QZQ\"",
  "title": "New Task List",
  "updated": "2026-02-07T05:45:22.685Z",
  "selfLink": "https://www.googleapis.com/tasks/v1/users/@me/lists/OFYyU09veWMyWl84SjNQXw"
}
```

#### 更新任务列表（PATCH - 部分更新）

```bash
PATCH /google-tasks/tasks/v1/users/@me/lists/{tasklistId}
Content-Type: application/json

{
  "title": "Updated Title"
}
```

#### 更新任务列表（PUT - 完整替换）

```bash
PUT /google-tasks/tasks/v1/users/@me/lists/{tasklistId}
Content-Type: application/json

{
  "title": "Replaced Title"
}
```

#### 删除任务列表

```bash
DELETE /google-tasks/tasks/v1/users/@me/lists/{tasklistId}
```

### 任务

#### 列出任务

```bash
GET /google-tasks/tasks/v1/lists/{tasklistId}/tasks
```

**查询参数：**
- `maxResults` - 返回的任务的最大数量（默认：20，最大值：100）
- `pageToken` - 分页令牌
- `showCompleted` - 是否包含已完成的任务（默认：true）
- `showDeleted` - 是否包含已删除的任务（默认：false）
- `showHidden` - 是否包含隐藏的任务（默认：false）
- `dueMin` - 截止日期的下限（RFC 3339 时间戳）
- `dueMax` - 截止日期的上限（RFC 3339 时间戳）
- `completedMin` - 完成日期的下限（RFC 3339 时间戳）
- `completedMax` - 完成日期的上限（RFC 3339 时间戳）
- `updatedMin` - 最后更新时间的上限（RFC 3339 时间戳）

**响应：**
```json
{
  "kind": "tasks#tasks",
  "etag": "\"Jhh35adkRkU\"",
  "nextPageToken": "CgwI27nR6AUQsKHh7QIa...",
  "items": [
    {
      "kind": "tasks#task",
      "id": "blJQR1hfaXhSU0tMY3gwdg",
      "etag": "\"Uqc8Y3T9VOA\"",
      "title": "Example Task",
      "updated": "2020-11-09T21:17:08.911Z",
      "selfLink": "https://www.googleapis.com/tasks/v1/lists/.../tasks/blJQR1hfaXhSU0tMY3gwdg",
      "position": "00000000000000000000",
      "status": "needsAction",
      "due": "2020-12-08T00:00:00.000Z",
      "notes": "Task notes here",
      "links": [],
      "webViewLink": "https://tasks.google.com/task/nRPGX_ixRSKLcx0v?sa=6"
    }
  ]
}
```

#### 获取任务信息

```bash
GET /google-tasks/tasks/v1/lists/{tasklistId}/tasks/{taskId}
```

#### 创建任务

```bash
POST /google-tasks/tasks/v1/lists/{tasklistId}/tasks
Content-Type: application/json

{
  "title": "New Task",
  "notes": "Task description",
  "due": "2026-03-01T00:00:00.000Z"
}
```

**查询参数（可选）：**
- `parent` - 父任务 ID（用于子任务）
- `previous` - 前一个同级任务的 ID（用于定位）

**响应：**
```json
{
  "kind": "tasks#task",
  "id": "bkludnJmdjZIZWVFejBnYg",
  "etag": "\"EKX4SVb-Ljk\"",
  "title": "New Task",
  "updated": "2026-02-07T05:45:05.371Z",
  "selfLink": "https://www.googleapis.com/tasks/v1/lists/.../tasks/bkludnJmdjZIZWVFejBnYg",
  "position": "00000000000000000000",
  "notes": "Task description",
  "status": "needsAction",
  "due": "2026-03-01T00:00:00.000Z",
  "links": [],
  "webViewLink": "https://tasks.google.com/task/nInvrfv6HeeEz0gb?sa=6"
}
```

#### 更新任务（PATCH - 部分更新）

```bash
PATCH /google-tasks/tasks/v1/lists/{tasklistId}/tasks/{taskId}
Content-Type: application/json

{
  "title": "Updated Task Title",
  "status": "completed"
}
```

**响应：**
```json
{
  "kind": "tasks#task",
  "id": "bkludnJmdjZIZWVFejBnYg",
  "etag": "\"OeWHIDNj-os\"",
  "title": "Updated Task Title",
  "updated": "2026-02-07T05:45:15.334Z",
  "selfLink": "https://www.googleapis.com/tasks/v1/lists/.../tasks/bkludnJmdjZIZWVFejBnYg",
  "position": "00000000000000000000",
  "notes": "Task description",
  "status": "completed",
  "completed": "2026-02-07T05:45:15.307Z",
  "links": [],
  "webViewLink": "https://tasks.google.com/task/nInvrfv6HeeEz0gb?sa=6"
}
```

#### 更新任务（PUT - 完整替换）

```bash
PUT /google-tasks/tasks/v1/lists/{tasklistId}/tasks/{taskId}
Content-Type: application/json

{
  "title": "Replaced Task",
  "notes": "New notes",
  "status": "needsAction"
}
```

#### 删除任务

```bash
DELETE /google-tasks/tasks/v1/lists/{tasklistId}/tasks/{taskId}
```

#### 移动任务

在任务列表中重新定位任务或更改其父任务。

**查询参数（可选）：**
- `parent` - 新的父任务 ID（用于将其设置为子任务）
- `previous` - 前一个同级任务的 ID（用于确定任务在列表中的位置）

**响应：**
```json
{
  "kind": "tasks#task",
  "id": "VkI5bTEzazdvNzlYNWVycw",
  "etag": "\"Uplv6eL0sDo\"",
  "title": "Task B",
  "updated": "2026-02-07T05:45:36.801Z",
  "selfLink": "https://www.googleapis.com/tasks/v1/lists/.../tasks/VkI5bTEzazdvNzlYNWVycw",
  "position": "00000000000000000001",
  "status": "needsAction",
  "links": [],
  "webViewLink": "https://tasks.google.com/task/VB9m13k7o79X5ers?sa=6"
}
```

#### 清除已完成的任务

从任务列表中删除所有已完成的任务。

```bash
POST /google-tasks/tasks/v1/lists/{tasklistId}/clear
```

成功时返回 HTTP 204 “No Content” 状态码。

## 任务资源字段

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `kind` | string | 始终为 “tasks#task”（仅用于输出） |
| `id` | string | 任务标识符 |
| `etag` | string | 资源的 ETag |
| `title` | string | 任务标题（最多 1024 个字符） |
| `updated` | string | 最后修改时间（RFC 3339，仅用于输出） |
| `selfLink` | string | 该任务的 URL（仅用于输出） |
| `parent` | string | 父任务 ID（仅用于输出） |
| `position` | string | 任务在列表中的位置（仅用于输出） |
| `notes` | string | 任务备注（最多 8192 个字符） |
| `status` | string | 状态：“needsAction” 或 “completed” |
| `due` | string | 截止日期（RFC 3339 时间戳） |
| `completed` | string | 完成日期（RFC 3339，仅用于输出） |
| `deleted` | boolean | 任务是否已删除 |
| `hidden` | boolean | 任务是否被隐藏 |
| `links` | array | 链接集合（仅用于输出） |
| `webViewLink` | string | 任务在 Google Tasks UI 中的链接（仅用于输出） |

## 任务列表资源字段

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `kind` | string | 始终为 “tasks#taskList”（仅用于输出） |
| `id` | string | 任务列表标识符 |
| `etag` | string | 资源的 ETag |
| `title` | string | 任务列表标题（最多 1024 个字符） |
| `updated` | string | 最后修改时间（RFC 3339，仅用于输出） |
| `selfLink` | string | 该任务列表的 URL（仅用于输出） |

## 分页

使用 `maxResults` 和 `pageToken` 进行分页：

```bash
GET /google-tasks/tasks/v1/lists/{tasklistId}/tasks?maxResults=50
```

当存在更多结果时，响应中会包含 `nextPageToken`：

```json
{
  "kind": "tasks#tasks",
  "etag": "...",
  "nextPageToken": "CgwI27nR6AUQsKHh7QIa...",
  "items": [...]
}
```

在后续请求中使用 `nextPageToken` 值：

```bash
GET /google-tasks/tasks/v1/lists/{tasklistId}/tasks?maxResults=50&pageToken=CgwI27nR6AUQsKHh7QIa...
```

## 代码示例

### JavaScript

```javascript
// List all task lists
const response = await fetch(
  'https://gateway.maton.ai/google-tasks/tasks/v1/users/@me/lists',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);

// Create a new task
const createResponse = await fetch(
  `https://gateway.maton.ai/google-tasks/tasks/v1/lists/${tasklistId}/tasks`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      title: 'New Task',
      notes: 'Task description',
      due: '2026-03-01T00:00:00.000Z'
    })
  }
);
```

### Python

```python
import os
import requests

# List all task lists
response = requests.get(
    'https://gateway.maton.ai/google-tasks/tasks/v1/users/@me/lists',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)

# Create a new task
create_response = requests.post(
    f'https://gateway.maton.ai/google-tasks/tasks/v1/lists/{tasklist_id}/tasks',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={
        'title': 'New Task',
        'notes': 'Task description',
        'due': '2026-03-01T00:00:00.000Z'
    }
)
```

## 注意事项

- 任务列表 ID 和任务 ID 是经过 Base64 编码的不透明字符串。
- 状态值为 “needsAction” 或 “completed”。
- 截止日期为 RFC 3339 时间戳。
- 任务标题的最大长度为 1024 个字符。
- 任务备注的最大长度为 8192 个字符。
- 重要提示：当使用 `curl` 命令时，如果 URL 中包含括号，请使用 `curl -g` 以禁用全局解析。
- 重要提示：当将 `curl` 的输出传递给 `jq` 或其他命令时，在某些 shell 环境中环境变量（如 `$MATON_API_KEY`）可能无法正确展开。这可能会导致 “Invalid API key” 错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Google Tasks 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 任务或任务列表未找到 |
| 429 | 请求频率限制 |
| 4xx/5xx | 来自 Google Tasks API 的传递错误 |

### 故障排除：API 密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证 API 密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用名称无效

1. 确保您的 URL 路径以 `google-tasks` 开头。例如：
- 正确：`https://gateway.maton.ai/google-tasks/tasks/v1/users/@me/lists`
- 错误：`https://gateway.maton.ai/tasks/v1/users/@me/lists`

## 资源

- [Google Tasks API 概述](https://developers.google.com/workspace/tasks)
- [任务参考](https://developers.google.com/workspace/tasks/reference/rest/v1/tasks)
- [任务列表参考](https://developers.google.com/workspace/tasks/reference/rest/v1/tasklists)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)