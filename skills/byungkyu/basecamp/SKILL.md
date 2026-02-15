---
name: basecamp
description: |
  Basecamp API integration with managed OAuth. Manage projects, to-dos, messages, schedules, documents, and team collaboration.
  Use this skill when users want to create and manage projects, to-do lists, schedule events, or collaborate with teams in Basecamp.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Basecamp

您可以使用托管的 OAuth 认证来访问 Basecamp 4 API，从而管理项目、待办事项、消息、日程安排、文档以及团队协作。

## 快速入门

```bash
# List all projects
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/basecamp/projects.json')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/basecamp/{resource}.json
```

该网关会将请求代理到 `3.basecampapi.com/{account_id}/`，并自动插入您的 OAuth 令牌和账户 ID。

**重要提示：** 所有 Basecamp API 的 URL 必须以 `.json` 结尾。

## 认证

所有请求都需要在 `Authorization` 头部包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Basecamp OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=basecamp&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'basecamp'}).encode()
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
    "connection_id": "71e313c8-9100-48c6-8ea1-6323f6fafd04",
    "status": "ACTIVE",
    "creation_time": "2026-02-08T03:12:39.815086Z",
    "last_updated_time": "2026-02-08T03:12:59.259878Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "basecamp",
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

如果您有多个 Basecamp 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/basecamp/projects.json')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '71e313c8-9100-48c6-8ea1-6323f6fafd04')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### 用户信息

#### 获取当前用户

```bash
GET /basecamp/my/profile.json
```

**响应：**
```json
{
  "id": 51197030,
  "name": "Chris Kim",
  "email_address": "chris@example.com",
  "admin": true,
  "owner": true,
  "time_zone": "America/Los_Angeles",
  "avatar_url": "https://..."
}
```

### 人员管理

#### 列出人员

```bash
GET /basecamp/people.json
```

**响应：**
```json
[
  {
    "id": 51197030,
    "name": "Chris Kim",
    "email_address": "chris@example.com",
    "admin": true,
    "owner": true,
    "employee": true,
    "time_zone": "America/Los_Angeles"
  }
]
```

#### 获取人员信息

```bash
GET /basecamp/people/{person_id}.json
```

#### 列出项目成员

```bash
GET /basecamp/projects/{project_id}/people.json
```

### 项目管理

#### 列出项目

```bash
GET /basecamp/projects.json
```

**响应：**
```json
[
  {
    "id": 46005636,
    "status": "active",
    "name": "Getting Started",
    "description": "Quickly get up to speed with everything Basecamp",
    "created_at": "2026-02-05T22:59:26.087Z",
    "url": "https://3.basecampapi.com/6153810/projects/46005636.json",
    "dock": [...]
  }
]
```

#### 获取项目信息

```bash
GET /basecamp/projects/{project_id}.json
```

项目响应中包含一个 `dock` 数组，其中列出了可用的工具（如消息板、待办事项管理器、文档库、聊天功能、日程安排等）。每个工具的详细信息包括：
- `id`：工具的 ID
- `name`：工具类型（例如 "todoset"、"message_board"）
- `enabled`：工具是否处于活动状态
- `url`：访问该工具的直接 URL

#### 创建项目

```bash
POST /basecamp/projects.json
Content-Type: application/json

{
  "name": "New Project",
  "description": "Project description"
}
```

#### 更新项目

```bash
PUT /basecamp/projects/{project_id}.json
Content-Type: application/json

{
  "name": "Updated Project Name",
  "description": "Updated description"
}
```

#### 删除项目

```bash
DELETE /basecamp/projects/{project_id}.json
```

### 待办事项管理

#### 获取待办事项管理器

首先，从项目的 `dock` 中获取待办事项管理器的 ID：

```bash
GET /basecamp/buckets/{project_id}/todosets/{todoset_id}.json
```

#### 列出待办事项列表

```bash
GET /basecamp/buckets/{project_id}/todosets/{todoset_id}/todolists.json
```

**响应：**
```json
[
  {
    "id": 9550474442,
    "title": "Basecamp essentials",
    "description": "",
    "completed": false,
    "completed_ratio": "0/5",
    "url": "https://..."
  }
]
```

#### 创建待办事项列表

```bash
POST /basecamp/buckets/{project_id}/todosets/{todoset_id}/todolists.json
Content-Type: application/json

{
  "name": "New Todo List",
  "description": "List description"
}
```

#### 获取待办事项列表

```bash
GET /basecamp/buckets/{project_id}/todolists/{todolist_id}.json
```

#### 列出待办事项

```bash
GET /basecamp/buckets/{project_id}/todolists/{todolist_id}/todos.json
```

**响应：**
```json
[
  {
    "id": 9550474446,
    "content": "Start here",
    "description": "",
    "completed": false,
    "due_on": null,
    "assignees": []
  }
]
```

#### 创建待办事项

```bash
POST /basecamp/buckets/{project_id}/todolists/{todolist_id}/todos.json
Content-Type: application/json

{
  "content": "New todo item",
  "description": "Todo description",
  "due_on": "2026-02-15",
  "assignee_ids": [51197030]
}
```

**响应：**
```json
{
  "id": 9555973289,
  "content": "New todo item",
  "completed": false
}
```

#### 更新待办事项

```bash
PUT /basecamp/buckets/{project_id}/todos/{todo_id}.json
Content-Type: application/json

{
  "content": "Updated todo",
  "description": "Updated description"
}
```

#### 完成待办事项

```bash
POST /basecamp/buckets/{project_id}/todos/{todo_id}/completion.json
```

成功时返回 204 状态码。

#### 取消待办事项

```bash
DELETE /basecamp/buckets/{project_id}/todos/{todo_id}/completion.json
```

### 消息板管理

#### 获取消息板

```bash
GET /basecamp/buckets/{project_id}/message_boards/{message_board_id}.json
```

#### 列出消息

```bash
GET /basecamp/buckets/{project_id}/message_boards/{message_board_id}/messages.json
```

#### 创建消息

```bash
POST /basecamp/buckets/{project_id}/message_boards/{message_board_id}/messages.json
Content-Type: application/json

{
  "subject": "Message Subject",
  "content": "<p>Message body with HTML</p>",
  "category_id": 123
}
```

#### 获取消息

```bash
GET /basecamp/buckets/{project_id}/messages/{message_id}.json
```

#### 更新消息

```bash
PUT /basecamp/buckets/{project_id}/messages/{message_id}.json
Content-Type: application/json

{
  "subject": "Updated Subject",
  "content": "<p>Updated content</p>"
}
```

### 日程安排管理

#### 获取日程安排

```bash
GET /basecamp/buckets/{project_id}/schedules/{schedule_id}.json
```

#### 列出日程安排条目

```bash
GET /basecamp/buckets/{project_id}/schedules/{schedule_id}/entries.json
```

#### 创建日程安排条目

```bash
POST /basecamp/buckets/{project_id}/schedules/{schedule_id}/entries.json
Content-Type: application/json

{
  "summary": "Team Meeting",
  "description": "Weekly sync",
  "starts_at": "2026-02-15T14:00:00Z",
  "ends_at": "2026-02-15T15:00:00Z",
  "all_day": false,
  "participant_ids": [51197030]
}
```

#### 更新日程安排条目

```bash
PUT /basecamp/buckets/{project_id}/schedule_entries/{entry_id}.json
Content-Type: application/json

{
  "summary": "Updated Meeting",
  "starts_at": "2026-02-15T15:00:00Z",
  "ends_at": "2026-02-15T16:00:00Z"
}
```

### 文档库（文档和文件）管理

#### 获取文档库

```bash
GET /basecamp/buckets/{project_id}/vaults/{vault_id}.json
```

#### 列出文档库中的文档

```bash
GET /basecamp/buckets/{project_id}/vaults/{vault_id}/documents.json
```

#### 创建文档

```bash
POST /basecamp/buckets/{project_id}/vaults/{vault_id}/documents.json
Content-Type: application/json

{
  "title": "Document Title",
  "content": "<p>Document content with HTML</p>"
}
```

#### 列出文档库中的上传文件

```bash
GET /basecamp/buckets/{project_id}/vaults/{vault_id}/uploads.json
```

### Campfire（聊天）管理

#### 列出所有聊天记录

```bash
GET /basecamp/chats.json
```

#### 获取聊天记录

```bash
GET /basecamp/buckets/{project_id}/chats/{chat_id}.json
```

#### 列出聊天记录中的消息

```bash
GET /basecamp/buckets/{project_id}/chats/{chat_id}/lines.json
```

#### 创建聊天记录

```bash
POST /basecamp/buckets/{project_id}/chats/{chat_id}/lines.json
Content-Type: application/json

{
  "content": "Hello from the API!"
}
```

### 评论管理

#### 列出记录的评论

```bash
GET /basecamp/buckets/{project_id}/recordings/{recording_id}/comments.json
```

#### 创建评论

```bash
POST /basecamp/buckets/{project_id}/recordings/{recording_id}/comments.json
Content-Type: application/json

{
  "content": "<p>Comment text</p>"
}
```

### 记录状态管理

所有内容项（待办事项、消息、文档等）都被视为“记录”，可以归档或删除。

#### 删除记录

```bash
PUT /basecamp/buckets/{project_id}/recordings/{recording_id}/status/trashed.json
```

#### 归档记录

```bash
PUT /basecamp/buckets/{project_id}/recordings/{recording_id}/status/archived.json
```

#### 解压记录

```bash
PUT /basecamp/buckets/{project_id}/recordings/{recording_id}/status/active.json
```

### 模板管理

#### 列出模板

```bash
GET /basecamp/templates.json
```

#### 根据模板创建项目

```bash
POST /basecamp/templates/{template_id}/project_constructions.json
Content-Type: application/json

{
  "name": "New Project from Template",
  "description": "Description"
}
```

## 分页

Basecamp 使用 `Link` 头部进行分页，其中 `rel="next"` 表示下一页：

**响应头：**
```
Link: <https://3.basecampapi.com/.../page=2>; rel="next"
X-Total-Count: 150
```

请跟随 `Link` 头部提供的 URL 进入下一页。当 `next` 不存在时，表示已到达最后一页。

**重要提示：** 不要手动构建分页 URL。始终使用 `Link` 头部提供的 URL。

## 关键概念

### “Bucket”和“项目”

“Bucket”是项目的内容容器。Bucket 的 ID 与 URL 中的项目 ID 相同：

```
/buckets/{project_id}/todosets/{todoset_id}.json
```

### “Dock”

每个项目都有一个包含可用工具的 “Dock”。在使用工具之前，请确保其状态为 `enabled: true`：

```json
{
  "dock": [
    {"name": "todoset", "id": 123, "enabled": true},
    {"name": "message_board", "id": 456, "enabled": false}
  ]
}
```

### 记录

所有内容项（待办事项、消息、文档、评论等）都被视为“记录”，具有以下属性：
- `status`：活动状态（active、archived 或 trashed）
- `parent`：指向其所属容器的链接
- 唯一 ID，可在多个 API 端点之间使用

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/basecamp/projects.json',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const projects = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/basecamp/projects.json',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
projects = response.json()
```

## 注意事项

- 所有 API 路径必须以 `.json` 结尾。
- 网关会自动插入账户 ID。
- 使用 Basecamp 4 API（bc3-api）。
- 时间戳采用 ISO 8601 格式。
- HTML 内容使用 `<div>`, `<p>`, `<strong>`, `<em>`, `<a>`, `<ul>`, `<ol>`, `<li>` 标签。
- 每个 IP 每 10 秒的请求限制约为 50 次。
- **重要提示：** 当将 curl 输出传递给 `jq` 或其他命令时，环境变量（如 `$MATON_API_KEY`）在某些 shell 环境中可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立 Basecamp 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 资源未找到、已被删除或无法访问 |
| 429 | 请求次数达到限制（请查看 `Retry-After` 头部信息） |
| 507 | 账户使用限制（例如项目数量限制） |
| 5xx | 服务器错误（请尝试重试）

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

### 故障排除：应用程序名称无效

1. 确保您的 URL 路径以 `basecamp` 开头。例如：
- 正确的格式：`https://gateway.maton.ai/basecamp/projects.json`
- 错误的格式：`https://gateway.maton.ai/projects.json`

## 资源

- [Basecamp 4 API 文档](https://github.com/basecamp/bc3-api)
- [认证指南](https://github.com/basecamp/bc3-api/blob/master/sections/authentication.md)
- [API 参考](https://github.com/basecamp/bc3-api#endpoints)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)