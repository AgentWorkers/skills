---
name: clockify
description: |
  Clockify API integration with managed OAuth. Track time, manage projects, clients, tasks, and workspaces.
  Use this skill when users want to track time, create or manage projects, view time entries, or manage workspace members.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# Clockify

通过管理的 OAuth 认证访问 Clockify API。您可以跟踪工作时间、管理项目、客户、任务、标签和工作空间。

## 快速入门

```bash
# Get current user
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/clockify/api/v1/user')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/clockify/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Clockify API 端点路径。该网关会将请求代理到 `api.clockify.me` 并自动插入您的凭据。

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
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Clockify OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=clockify&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'clockify'}).encode()
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
    "connection_id": "13fe7b78-42ba-4b43-9631-69a4bf7091ec",
    "status": "ACTIVE",
    "creation_time": "2026-02-13T09:18:02.529448Z",
    "last_updated_time": "2026-02-13T09:18:09.334540Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "clockify",
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

如果您有多个 Clockify 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/clockify/api/v1/user')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '13fe7b78-42ba-4b43-9631-69a4bf7091ec')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### 用户操作

#### 获取当前用户

```bash
GET /clockify/api/v1/user
```

**响应：**
```json
{
  "id": "698eeb9f5cd3a921db12069f",
  "email": "user@example.com",
  "name": "John Doe",
  "activeWorkspace": "698eeb9e5cd3a921db120693",
  "defaultWorkspace": "698eeb9e5cd3a921db120693",
  "status": "ACTIVE"
}
```

### 工作空间操作

#### 列出工作空间

```bash
GET /clockify/api/v1/workspaces
```

#### 获取工作空间信息

```bash
GET /clockify/api/v1/workspaces/{workspaceId}
```

#### 创建工作空间

```bash
POST /clockify/api/v1/workspaces
Content-Type: application/json

{
  "name": "My Workspace"
}
```

#### 列出工作空间用户

```bash
GET /clockify/api/v1/workspaces/{workspaceId}/users
```

### 项目操作

#### 列出项目

```bash
GET /clockify/api/v1/workspaces/{workspaceId}/projects
```

#### 获取项目信息

```bash
GET /clockify/api/v1/workspaces/{workspaceId}/projects/{projectId}
```

#### 创建项目

```bash
POST /clockify/api/v1/workspaces/{workspaceId}/projects
Content-Type: application/json

{
  "name": "My Project",
  "isPublic": true,
  "clientId": "optional-client-id"
}
```

**响应：**
```json
{
  "id": "698f7cba4f748f6209ea8995",
  "name": "My Project",
  "clientId": "",
  "workspaceId": "698eeb9e5cd3a921db120693",
  "billable": true,
  "color": "#1976D2",
  "archived": false,
  "public": true
}
```

#### 更新项目

```bash
PUT /clockify/api/v1/workspaces/{workspaceId}/projects/{projectId}
Content-Type: application/json

{
  "name": "Updated Project Name",
  "archived": true
}
```

#### 删除项目

```bash
DELETE /clockify/api/v1/workspaces/{workspaceId}/projects/{projectId}
```

**注意：** 不能删除正在使用中的项目。请先将其设置为 `archived: true`。

### 客户操作

#### 列出客户

```bash
GET /clockify/api/v1/workspaces/{workspaceId}/clients
```

#### 获取客户信息

```bash
GET /clockify/api/v1/workspaces/{workspaceId}/clients/{clientId}
```

#### 创建客户

```bash
POST /clockify/api/v1/workspaces/{workspaceId}/clients
Content-Type: application/json

{
  "name": "Acme Corp",
  "address": "123 Main St",
  "note": "Important client"
}
```

**响应：**
```json
{
  "id": "698f7cba0705b7d880830262",
  "name": "Acme Corp",
  "workspaceId": "698eeb9e5cd3a921db120693",
  "archived": false,
  "address": "123 Main St",
  "note": "Important client"
}
```

#### 更新客户信息

```bash
PUT /clockify/api/v1/workspaces/{workspaceId}/clients/{clientId}
Content-Type: application/json

{
  "name": "Acme Corporation"
}
```

#### 删除客户

```bash
DELETE /clockify/api/v1/workspaces/{workspaceId}/clients/{clientId}
```

### 标签操作

#### 列出标签

```bash
GET /clockify/api/v1/workspaces/{workspaceId}/tags
```

#### 获取标签信息

```bash
GET /clockify/api/v1/workspaces/{workspaceId}/tags/{tagId}
```

#### 创建标签

```bash
POST /clockify/api/v1/workspaces/{workspaceId}/tags
Content-Type: application/json

{
  "name": "urgent"
}
```

**响应：**
```json
{
  "id": "698f7cbbaa9e9f33e5fc0126",
  "name": "urgent",
  "workspaceId": "698eeb9e5cd3a921db120693",
  "archived": false
}
```

#### 更新标签信息

```bash
PUT /clockify/api/v1/workspaces/{workspaceId}/tags/{tagId}
Content-Type: application/json

{
  "name": "high-priority"
}
```

#### 删除标签

```bash
DELETE /clockify/api/v1/workspaces/{workspaceId}/tags/{tagId}
```

### 任务操作

#### 列出项目中的任务

```bash
GET /clockify/api/v1/workspaces/{workspaceId}/projects/{projectId}/tasks
```

#### 获取任务信息

```bash
GET /clockify/api/v1/workspaces/{workspaceId}/projects/{projectId}/tasks/{taskId}
```

#### 创建任务

```bash
POST /clockify/api/v1/workspaces/{workspaceId}/projects/{projectId}/tasks
Content-Type: application/json

{
  "name": "Implement feature",
  "assigneeIds": ["user-id-1"],
  "estimate": "PT2H",
  "billable": true
}
```

**响应：**
```json
{
  "id": "698f7cc4aa9e9f33e5fc017b",
  "name": "Implement feature",
  "projectId": "698f7cba4f748f6209ea8995",
  "assigneeIds": [],
  "estimate": "PT0S",
  "status": "ACTIVE",
  "billable": true
}
```

#### 更新任务信息

```bash
PUT /clockify/api/v1/workspaces/{workspaceId}/projects/{projectId}/tasks/{taskId}
Content-Type: application/json

{
  "name": "Updated task name",
  "status": "DONE"
}
```

#### 删除任务

```bash
DELETE /clockify/api/v1/workspaces/{workspaceId}/projects/{projectId}/tasks/{taskId}
```

**注意：** 不能删除正在使用中的任务。请先将其状态设置为 `status: "DONE"`。

### 时间记录操作

#### 获取用户的时间记录

```bash
GET /clockify/api/v1/workspaces/{workspaceId}/user/{userId}/time-entries
```

**响应：**
```json
[
  {
    "id": "698f7cc4aa9e9f33e5fc0180",
    "description": "Working on project",
    "userId": "698eeb9f5cd3a921db12069f",
    "billable": true,
    "projectId": "698f7cba4f748f6209ea8995",
    "taskId": null,
    "workspaceId": "698eeb9e5cd3a921db120693",
    "timeInterval": {
      "start": "2026-02-13T18:34:28Z",
      "end": "2026-02-13T19:34:28Z",
      "duration": "PT1H"
    }
  }
]
```

#### 创建时间记录

```bash
POST /clockify/api/v1/workspaces/{workspaceId}/time-entries
Content-Type: application/json

{
  "start": "2026-02-13T09:00:00Z",
  "end": "2026-02-13T10:00:00Z",
  "description": "Team meeting",
  "projectId": "project-id",
  "taskId": "task-id",
  "tagIds": ["tag-id-1", "tag-id-2"],
  "billable": true
}
```

#### 为其他用户创建时间记录

```bash
POST /clockify/api/v1/workspaces/{workspaceId}/user/{userId}/time-entries
Content-Type: application/json

{
  "start": "2026-02-13T09:00:00Z",
  "end": "2026-02-13T10:00:00Z",
  "description": "Team meeting"
}
```

#### 获取时间记录信息

```bash
GET /clockify/api/v1/workspaces/{workspaceId}/time-entries/{timeEntryId}
```

#### 更新时间记录

```bash
PUT /clockify/api/v1/workspaces/{workspaceId}/time-entries/{timeEntryId}
Content-Type: application/json

{
  "start": "2026-02-13T09:00:00Z",
  "end": "2026-02-13T11:00:00Z",
  "description": "Extended meeting"
}
```

#### 删除时间记录

```bash
DELETE /clockify/api/v1/workspaces/{workspaceId}/time-entries/{timeEntryId}
```

#### 停止计时器

```bash
PATCH /clockify/api/v1/workspaces/{workspaceId}/user/{userId}/time-entries
Content-Type: application/json

{
  "end": "2026-02-13T17:00:00Z"
}
```

#### 获取进行中的时间记录

```bash
GET /clockify/api/v1/workspaces/{workspaceId}/time-entries
```

## 分页

Clockify 使用基于页面的分页机制：

```bash
GET /clockify/api/v1/workspaces/{workspaceId}/projects?page=1&page-size=50
```

**查询参数：**
- `page` - 页码（从 1 开始计数，默认值：1）
- `page-size` - 每页显示的项数（因端点而异）

响应中包含一个 `Last-Page` 头部，用于指示是否还有更多页面。

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/clockify/api/v1/workspaces',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const workspaces = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/clockify/api/v1/workspaces',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
workspaces = response.json()
```

### 使用 Python 创建时间记录

```python
import os
import requests
from datetime import datetime, timedelta, timezone

workspace_id = "your-workspace-id"
start_time = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat().replace('+00:00', 'Z')
end_time = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

response = requests.post(
    f'https://gateway.maton.ai/clockify/api/v1/workspaces/{workspace_id}/time-entries',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'start': start_time,
        'end': end_time,
        'description': 'Working on feature'
    }
)
```

## 注意事项

- 所有 ID 都是字符串标识符。
- 时间戳必须采用 ISO 8601 格式，并指定 UTC 时区（例如：`2026-02-13T09:00:00Z`）。
- 持续时间格式也采用 ISO 8601 格式（例如：`PT1H` 表示 1 小时，`PT30M` 表示 30 分钟）。
- 不能删除正在使用中的项目或任务——必须先将其归档。
- 每个工作空间的请求速率限制为每秒 50 次。
- **重要提示：** 当 URL 中包含括号时，使用 `curl -g` 选项来禁用全局解析。
- **重要提示：** 当将 curl 输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确解析。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 未找到 Clockify 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 403 | 权限不足 |
| 404 | 资源未找到 |
| 429 | 每个工作空间的请求速率限制达到（每秒 50 次） |
| 4xx/5xx | 来自 Clockify API 的传递错误 |

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

1. 确保您的 URL 路径以 `clockify` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/clockify/api/v1/user`
- 错误的路径：`https://gateway.maton.ai/api/v1/user`

## 资源

- [Clockify API 文档](https://docs.clockify.me/)
- [Clockify API 参考](https://docs.clockify.me/#tag/Time-entry)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)