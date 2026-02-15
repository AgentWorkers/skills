---
name: toggl-track
description: |
  Toggl Track API integration with managed OAuth. Track time, manage projects, clients, and tags.
  Use this skill when users want to create, read, update, or delete time entries, projects, clients, or tags in Toggl Track.
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

# Toggl Track

通过管理的OAuth认证来访问Toggl Track API。您可以跟踪时间、管理项目、客户、标签和工作空间。

## 快速入门

```bash
# Get current user info
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/toggl-track/api/v9/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/toggl-track/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的Toggl Track API端点路径。该网关会将请求代理到 `api.track.toggl.com` 并自动插入您的凭据。

## 认证

所有请求都需要在 `Authorization` 头部包含Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的Toggl Track OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=toggl-track&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'toggl-track'}).encode()
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
    "connection_id": "0acc2145-4d3e-4eaf-bdfd-7b04e0e0d649",
    "status": "ACTIVE",
    "creation_time": "2026-02-13T19:31:31.452264Z",
    "last_updated_time": "2026-02-13T19:36:10.489069Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "toggl-track",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成OAuth认证。

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

如果您有多个Toggl Track连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/toggl-track/api/v9/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '0acc2145-4d3e-4eaf-bdfd-7b04e0e0d649')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略，则网关将使用默认的（最旧的）活动连接。

## API参考

### 用户与工作空间

#### 获取当前用户

```bash
GET /toggl-track/api/v9/me
```

**响应：**
```json
{
  "id": 12932942,
  "email": "user@example.com",
  "fullname": "John Doe",
  "timezone": "America/Los_Angeles",
  "default_workspace_id": 21180405,
  "beginning_of_week": 1,
  "image_url": "https://assets.track.toggl.com/images/profile.png"
}
```

#### 列出工作空间

```bash
GET /toggl-track/api/v9/me/workspaces
```

#### 获取工作空间信息

```bash
GET /toggl-track/api/v9/workspaces/{workspace_id}
```

#### 列出工作空间用户

```bash
GET /toggl-track/api/v9/workspaces/{workspace_id}/users
```

### 时间记录

#### 列出时间记录

```bash
GET /toggl-track/api/v9/me/time_entries
```

**查询参数：**
- `since` (整数) - 从此时间之后修改的时间记录的UNIX时间戳
- `before` (字符串) - 在此日期之前的时间记录（RFC3339或YYYY-MM-DD格式）
- `start_date` (字符串) - 过滤开始日期（YYYY-MM-DD格式）
- `end_date` (字符串) - 过滤结束日期（YYYY-MM-DD格式）

#### 获取当前正在进行的时间记录

```bash
GET /toggl-track/api/v9/me/time_entries/current
```

如果没有正在进行的时间记录，则返回 `null`。

#### 通过ID获取时间记录

```bash
GET /toggl-track/api/v9/me/time_entries/{time_entry_id}
```

#### 创建时间记录

```bash
POST /toggl-track/api/v9/workspaces/{workspace_id}/time_entries
Content-Type: application/json

{
  "description": "Working on project",
  "start": "2026-02-13T10:00:00Z",
  "duration": -1,
  "workspace_id": 21180405,
  "project_id": 216896134,
  "tag_ids": [20053808],
  "created_with": "maton-api"
}
```

**注意：** 将 `duration` 设置为 `-1` 以启动计时器。`created_with` 字段是必需的。

**响应：**
```json
{
  "id": 4290254971,
  "workspace_id": 21180405,
  "project_id": null,
  "task_id": null,
  "billable": false,
  "start": "2026-02-13T19:58:43Z",
  "stop": null,
  "duration": -1,
  "description": "Working on project",
  "tags": null,
  "tag_ids": null,
  "user_id": 12932942
}
```

#### 更新时间记录

```bash
PUT /toggl-track/api/v9/workspaces/{workspace_id}/time_entries/{time_entry_id}
Content-Type: application/json

{
  "description": "Updated description",
  "project_id": 216896134
}
```

#### 停止计时器

```bash
PATCH /toggl-track/api/v9/workspaces/{workspace_id}/time_entries/{time_entry_id}/stop
```

#### 删除时间记录

```bash
DELETE /toggl-track/api/v9/workspaces/{workspace_id}/time_entries/{time_entry_id}
```

### 项目

#### 列出项目

```bash
GET /toggl-track/api/v9/workspaces/{workspace_id}/projects
```

**查询参数：**
- `active` (布尔值) - 按活动状态过滤
- `since` (整数) - 修改时间的UNIX时间戳
- `name` (字符串) - 按项目名称过滤
- `page` (整数) - 页码
- `per_page` (整数) - 每页显示的项目数量（最多200个）

#### 获取项目信息

```bash
GET /toggl-track/api/v9/workspaces/{workspace_id}/projects/{project_id}
```

#### 创建项目

```bash
POST /toggl-track/api/v9/workspaces/{workspace_id}/projects
Content-Type: application/json

{
  "name": "New Project",
  "active": true,
  "is_private": true,
  "client_id": 68493239,
  "color": "#0b83d9",
  "billable": true
}
```

**响应：**
```json
{
  "id": 216896134,
  "workspace_id": 21180405,
  "client_id": null,
  "name": "New Project",
  "is_private": true,
  "active": true,
  "color": "#0b83d9",
  "billable": true,
  "created_at": "2026-02-13T19:58:36+00:00"
}
```

#### 更新项目信息

```bash
PUT /toggl-track/api/v9/workspaces/{workspace_id}/projects/{project_id}
Content-Type: application/json

{
  "name": "Updated Project Name",
  "color": "#ff0000"
}
```

#### 删除项目

```bash
DELETE /toggl-track/api/v9/workspaces/{workspace_id}/projects/{project_id}
```

### 客户

#### 列出客户

```bash
GET /toggl-track/api/v9/workspaces/{workspace_id}/clients
```

**查询参数：**
- `status` (字符串) - 过滤条件：`active`、`archived` 或 `both`
- `name` (字符串) - 不区分大小写的名称过滤

#### 获取客户信息

```bash
GET /toggl-track/api/v9/workspaces/{workspace_id}/clients/{client_id}
```

#### 创建客户

```bash
POST /toggl-track/api/v9/workspaces/{workspace_id}/clients
Content-Type: application/json

{
  "name": "New Client",
  "notes": "Client notes here"
}
```

**响应：**
```json
{
  "id": 68493239,
  "wid": 21180405,
  "archived": false,
  "name": "New Client",
  "at": "2026-02-13T19:58:36+00:00",
  "creator_id": 12932942
}
```

#### 更新客户信息

```bash
PUT /toggl-track/api/v9/workspaces/{workspace_id}/clients/{client_id}
Content-Type: application/json

{
  "name": "Updated Client Name"
}
```

#### 删除客户

```bash
DELETE /toggl-track/api/v9/workspaces/{workspace_id}/clients/{client_id}
```

#### 归档客户

```bash
POST /toggl-track/api/v9/workspaces/{workspace_id}/clients/{client_id}/archive
```

#### 恢复客户

```bash
POST /toggl-track/api/v9/workspaces/{workspace_id}/clients/{client_id}/restore
Content-Type: application/json

{
  "restore_all_projects": true
}
```

### 标签

#### 列出标签

```bash
GET /toggl-track/api/v9/workspaces/{workspace_id}/tags
```

**查询参数：**
- `page` (整数) - 页码
- `per_page` (整数) - 每页显示的标签数量

#### 创建标签

```bash
POST /toggl-track/api/v9/workspaces/{workspace_id}/tags
Content-Type: application/json

{
  "name": "New Tag"
}
```

**响应：**
```json
{
  "id": 20053808,
  "workspace_id": 21180405,
  "name": "New Tag",
  "at": "2026-02-13T19:58:37.115714Z",
  "creator_id": 12932942
}
```

#### 更新标签信息

```bash
PUT /toggl-track/api/v9/workspaces/{workspace_id}/tags/{tag_id}
Content-Type: application/json

{
  "name": "Updated Tag Name"
}
```

#### 删除标签

```bash
DELETE /toggl-track/api/v9/workspaces/{workspace_id}/tags/{tag_id}
```

## 分页

Toggl Track 对大多数列表端点使用基于页码的分页：

```bash
GET /toggl-track/api/v9/workspaces/{workspace_id}/projects?page=1&per_page=50
```

对于时间记录，可以使用基于时间戳的过滤：

```bash
GET /toggl-track/api/v9/me/time_entries?since=1707840000&start_date=2026-02-01&end_date=2026-02-28
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/toggl-track/api/v9/me/time_entries',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const timeEntries = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/toggl-track/api/v9/me/time_entries',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
time_entries = response.json()
```

### 启动计时器

```python
import os
import requests
from datetime import datetime, timezone

response = requests.post(
    'https://gateway.maton.ai/toggl-track/api/v9/workspaces/21180405/time_entries',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'description': 'Working on task',
        'start': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'duration': -1,
        'workspace_id': 21180405,
        'created_with': 'maton-api'
    }
)
```

## 注意事项

- 工作空间ID是整数（例如：`21180405`）
- 时间记录ID是大整数（例如：`4290254971`）
- 持续时间是秒；使用 `-1` 来启动计时器
- 时间戳使用ISO 8601格式（例如：`2026-02-13T19:58:43Z`）
- 创建时间记录时必须填写 `created_with` 字段
- 重要提示：当URL包含括号时，使用 `curl -g` 可以防止glob解析
- 重要提示：在将curl输出传递给 `jq` 或其他命令时，某些shell环境中环境变量（如 `$MATON_API_KEY`）可能无法正确展开

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 未找到Toggl Track连接或请求无效 |
| 401 | Maton API密钥无效或缺失 |
| 403 | 访问被拒绝 |
| 404 | 资源未找到 |
| 429 | 请求频率限制 |
| 4xx/5xx | 来自Toggl Track API的传递错误 |

### 故障排除：API密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

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

1. 确保您的URL路径以 `toggl-track` 开头。例如：
- 正确：`https://gateway.maton.ai/toggl-track/api/v9/me`
- 错误：`https://gateway.maton.ai/api/v9/me`

## 资源

- [Toggl Track API文档](https://engineering.toggl.com/docs/)
- [Toggl Track API参考](https://engineering.toggl.com/docs/api/)
- [时间记录API](https://engineering.toggl.com/docs/api/time_entries)
- [项目API](https://engineering.toggl.com/docs/api/projects)
- [客户API](https://engineering.toggl.com/docs/api/clients)
- [标签API](https://engineering.toggl.com/docs/api/tags)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)