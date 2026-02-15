---
name: asana
description: |
  Asana API integration with managed OAuth. Access tasks, projects, workspaces, users, and manage webhooks. Use this skill when users want to manage work items, track projects, or integrate with Asana workflows. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Asana

您可以使用受管理的OAuth认证来访问Asana API，从而管理任务、项目、工作空间、用户以及用于工作管理的Webhook。

## 快速入门

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/asana/api/1.0/tasks?project=PROJECT_GID')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/asana/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的Asana API端点路径。该网关会将请求代理到 `app.asana.com` 并自动插入您的OAuth令牌。

## 认证

所有请求都需要在 `Authorization` 头部包含Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取您的API密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的Asana OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=asana&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'asana'}).encode()
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
    "app": "asana",
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

如果您有多个Asana连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/asana/api/1.0/tasks?project=PROJECT_GID')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API参考

### 任务

#### 获取多个任务

```bash
GET /asana/api/1.0/tasks
```

查询参数：
- `project` - 项目GID（用于过滤任务）
- `assignee` - 用户GID或“me”（用于获取已分配的任务）
- `workspace` - 工作空间GID（如果未指定项目，则必需）
- `completed_since` - ISO 8601格式的日期（用于过滤在此日期之后完成的任务）
- `opt_fields` - 以逗号分隔的字段列表（需要返回的字段）

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/asana/api/1.0/tasks?project=1234567890&opt_fields=name,completed,due_on')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": [
    {
      "gid": "1234567890",
      "name": "Review quarterly report",
      "completed": false,
      "due_on": "2025-03-15"
    }
  ]
}
```

#### 获取单个任务

```bash
GET /asana/api/1.0/tasks/{task_gid}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/asana/api/1.0/tasks/1234567890')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建任务

```bash
POST /asana/api/1.0/tasks
Content-Type: application/json

{
  "data": {
    "name": "New task",
    "projects": ["PROJECT_GID"],
    "assignee": "USER_GID",
    "due_on": "2025-03-20",
    "notes": "Task description here"
  }
}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'data': {'name': 'Complete API integration', 'projects': ['1234567890'], 'due_on': '2025-03-20'}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/asana/api/1.0/tasks', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 更新任务

```bash
PUT /asana/api/1.0/tasks/{task_gid}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'data': {'completed': True}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/asana/api/1.0/tasks/1234567890', data=data, method='PUT')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 删除任务

```bash
DELETE /asana/api/1.0/tasks/{task_gid}
```

#### 从项目中获取任务

```bash
GET /asana/api/1.0/projects/{project_gid}/tasks
```

#### 获取子任务

```bash
GET /asana/api/1.0/tasks/{task_gid}/subtasks
```

#### 创建子任务

```bash
POST /asana/api/1.0/tasks/{task_gid}/subtasks
Content-Type: application/json

{
  "data": {
    "name": "Subtask name",
    "assignee": "USER_GID",
    "due_on": "2025-03-20"
  }
}
```

#### 搜索任务（需Asana Premium订阅）

**注意：** 此端点需要Asana Premium订阅。

```bash
GET /asana/api/1.0/workspaces/{workspace_gid}/tasks/search
```

查询参数：
- `text` - 要搜索的文本
- `assignee.any` - 按分配者过滤
- `projects.any` - 按项目过滤
- `completed` - 按完成状态过滤

### 项目

#### 获取多个项目

```bash
GET /asana/api/1.0/projects
```

查询参数：
- `workspace` - 工作空间GID
- `team` - 团队GID
- `opt_fields` - 以逗号分隔的字段列表

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/asana/api/1.0/projects?workspace=1234567890&opt_fields=name,owner,due_date')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": [
    {
      "gid": "1234567890",
      "name": "Q1 Marketing Campaign",
      "owner": {
        "gid": "0987654321",
        "name": "Alice Johnson"
      },
      "due_date": "2025-03-31"
    }
  ]
}
```

#### 获取单个项目

```bash
GET /asana/api/1.0/projects/{project_gid}
```

#### 创建项目

```bash
POST /asana/api/1.0/projects
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'data': {'name': 'New Project', 'workspace': '1234567890', 'notes': 'Project description'}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/asana/api/1.0/projects', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 更新项目

```bash
PUT /asana/api/1.0/projects/{project_gid}
```

#### 删除项目

```bash
DELETE /asana/api/1.0/projects/{project_gid}
```

### 工作空间

#### 获取多个工作空间

```bash
GET /asana/api/1.0/workspaces
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/asana/api/1.0/workspaces')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": [
    {
      "gid": "1234567890",
      "name": "Acme Corp",
      "is_organization": true
    }
  ]
}
```

#### 获取单个工作空间

```bash
GET /asana/api/1.0/workspaces/{workspace_gid}
```

#### 更新工作空间

```bash
PUT /asana/api/1.0/workspaces/{workspace_gid}
```

#### 将用户添加到工作空间

```bash
POST /asana/api/1.0/workspaces/{workspace_gid}/addUser
```

#### 从工作空间中移除用户

```bash
POST /asana/api/1.0/workspaces/{workspace_gid}/removeUser
```

### 用户

#### 获取多个用户

```bash
GET /asana/api/1.0/users
```

查询参数：
- `workspace` - 工作空间GID（用于过滤用户）

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/asana/api/1.0/users?workspace=1234567890&opt_fields=name,email')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": [
    {
      "gid": "1234567890",
      "name": "Alice Johnson",
      "email": "alice.johnson@acme.com"
    }
  ]
}
```

#### 获取当前用户

```bash
GET /asana/api/1.0/users/me
```

#### 获取单个用户

```bash
GET /asana/api/1.0/users/{user_gid}
```

#### 获取团队中的用户

```bash
GET /asana/api/1.0/teams/{team_gid}/users
```

#### 获取工作空间中的用户

```bash
GET /asana/api/1.0/workspaces/{workspace_gid}/users
```

### Webhook

#### 获取多个Webhook

```bash
GET /asana/api/1.0/webhooks
```

查询参数：
- `workspace` - 工作空间GID（必需）
- `resource` - 资源GID（用于过滤）

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/asana/api/1.0/webhooks?workspace=1234567890')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建Webhook

**注意：** Asana会验证目标URL是否可访问，并在创建Webhook时返回200状态码。

```bash
POST /asana/api/1.0/webhooks
Content-Type: application/json

{
  "data": {
    "resource": "PROJECT_OR_TASK_GID",
    "target": "https://example.com/webhook",
    "filters": [
      {
        "resource_type": "task",
        "action": "changed",
        "fields": ["completed", "due_on"]
      }
    ]
  }
}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'data': {'resource': '1234567890', 'target': 'https://example.com/webhook'}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/asana/api/1.0/webhooks', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": {
    "gid": "1234567890",
    "resource": {
      "gid": "1234567890",
      "name": "Q1 Project"
    },
    "target": "https://example.com/webhook",
    "active": true
  }
}
```

#### 获取Webhook信息

```bash
GET /asana/api/1.0/webhooks/{webhook_gid}
```

#### 更新Webhook

```bash
PUT /asana/api/1.0/webhooks/{webhook_gid}
```

#### 删除Webhook

```bash
DELETE /asana/api/1.0/webhooks/{webhook_gid}
```

成功时返回 `200 OK` 且数据为空。

## 分页

Asana使用基于游标的分页机制。使用 `offset` 参数进行分页：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/asana/api/1.0/tasks?project=1234567890&limit=50&offset=OFFSET_TOKEN')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

当存在更多结果时，响应中会包含 `next_page`：

```json
{
  "data": [...],
  "next_page": {
    "offset": "eyJ0eXBlIjoib2Zmc2V0IiwidmFsdWUiOjUwfQ",
    "path": "/tasks?project=1234567890&limit=50&offset=eyJ0eXBlIjoib2Zmc2V0IiwidmFsdWUiOjUwfQ",
    "uri": "https://app.asana.com/api/1.0/tasks?project=1234567890&limit=50&offset=eyJ0eXBlIjoib2Zmc2V0IiwidmFsdWUiOjUwfQ"
  }
}
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/asana/api/1.0/tasks?project=1234567890',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/asana/api/1.0/tasks',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'project': '1234567890'}
)
data = response.json()
```

## 注意事项

- 资源ID（GID）为字符串形式。
- 时间戳采用ISO 8601格式。
- 使用 `opt_fields` 参数指定需要返回的字段。
- 工作空间是最高级别的组织单位。
- 组织是代表公司的专用工作空间。
- **重要提示：** 当使用curl命令时，如果URL包含方括号（如 `fields[]`、`sort[]`、`records[]`），请使用 `curl -g` 以禁用全局解析。
- **重要提示：** 当将curl输出传递给 `jq` 或其他命令时，在某些Shell环境中环境变量（如 `$MATON_API_KEY`）可能无法正确解析，可能会导致“无效API密钥”的错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 请求错误或未建立Asana连接 |
| 401 | API密钥无效或缺失 |
| 403 | 禁止访问 - 权限不足 |
| 404 | 资源未找到 |
| 429 | 请求频率限制 |
| 4xx/5xx | 来自Asana API的传递错误 |

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

1. 确保您的URL路径以 `asana` 开头。例如：
- 正确格式：`https://gateway.maton.ai/asana/api/1.0/tasks`
- 错误格式：`https://gateway.maton.ai/api/1.0/tasks`

## 资源

- [Asana API文档](https://developers.asana.com)
- [API参考](https://developers.asana.com/reference)
- [LLM参考](https://developers.asana.com/llms.txt)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)