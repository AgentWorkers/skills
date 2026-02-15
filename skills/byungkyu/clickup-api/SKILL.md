---
name: clickup
description: |
  ClickUp API integration with managed OAuth. Access tasks, lists, folders, spaces, workspaces, users, and manage webhooks. Use this skill when users want to manage work items, track projects, or integrate with ClickUp workflows. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# ClickUp

通过管理的OAuth认证来访问ClickUp API。您可以管理任务、列表、文件夹、工作空间、用户和Webhook，以实现工作管理。

## 快速入门

```bash
# List workspaces (teams)
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/clickup/api/v2/team')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/clickup/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的ClickUp API端点路径。该网关会将请求代理到 `api.clickup.com`，并自动插入您的OAuth令牌。

## 认证

所有请求都需要在 `Authorization` 头部包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 上管理您的ClickUp OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=clickup&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'clickup'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接

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
    "app": "clickup",
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

如果您有多个ClickUp连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/clickup/api/v2/team')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略，则网关将使用默认的（最旧的）活动连接。

## ClickUp 数据结构

ClickUp 以层次结构组织数据：
- **工作空间（团队）** → **空间** → **文件夹** → **列表** → **任务**

注意：在API中，工作空间被称为“团队”。

## API 参考

### 工作空间（团队）

#### 获取授权的工作空间

```bash
GET /clickup/api/v2/team
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/clickup/api/v2/team')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "teams": [
    {
      "id": "1234567",
      "name": "Acme Corp",
      "color": "#7B68EE",
      "avatar": null,
      "members": [
        {
          "user": {
            "id": 123,
            "username": "Alice Johnson",
            "email": "alice@acme.com"
          }
        }
      ]
    }
  ]
}
```

### 空间

#### 获取空间

```bash
GET /clickup/api/v2/team/{team_id}/space
```

查询参数：
- `archived` - 是否包含已归档的空间（true/false）

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/clickup/api/v2/team/1234567/space')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "spaces": [
    {
      "id": "90120001",
      "name": "Engineering",
      "private": false,
      "statuses": [
        {"status": "to do", "type": "open"},
        {"status": "in progress", "type": "custom"},
        {"status": "done", "type": "closed"}
      ]
    }
  ]
}
```

#### 获取一个空间

```bash
GET /clickup/api/v2/space/{space_id}
```

#### 创建一个空间

```bash
POST /clickup/api/v2/team/{team_id}/space
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'name': 'New Space', 'multiple_assignees': True, 'features': {'due_dates': {'enabled': True}, 'time_tracking': {'enabled': True}}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/clickup/api/v2/team/1234567/space', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 更新一个空间

```bash
PUT /clickup/api/v2/space/{space_id}
```

#### 删除一个空间

```bash
DELETE /clickup/api/v2/space/{space_id}
```

### 文件夹

#### 获取文件夹

```bash
GET /clickup/api/v2/space/{space_id}/folder
```

查询参数：
- `archived` - 是否包含已归档的文件夹（true/false）

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/clickup/api/v2/space/90120001/folder')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "folders": [
    {
      "id": "456789",
      "name": "Sprint 1",
      "orderindex": 0,
      "hidden": false,
      "space": {"id": "90120001", "name": "Engineering"},
      "task_count": "12",
      "lists": []
    }
  ]
}
```

#### 获取一个文件夹

```bash
GET /clickup/api/v2/folder/{folder_id}
```

#### 创建一个文件夹

```bash
POST /clickup/api/v2/space/{space_id}/folder
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'name': 'New Folder'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/clickup/api/v2/space/90120001/folder', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 更新一个文件夹

```bash
PUT /clickup/api/v2/folder/{folder_id}
```

#### 删除一个文件夹

```bash
DELETE /clickup/api/v2/folder/{folder_id}
```

### 列表

#### 获取列表

```bash
GET /clickup/api/v2/folder/{folder_id}/list
```

查询参数：
- `archived` - 是否包含已归档的列表（true/false）

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/clickup/api/v2/folder/456789/list')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "lists": [
    {
      "id": "901234",
      "name": "Backlog",
      "orderindex": 0,
      "status": {"status": "active", "color": "#87909e"},
      "task_count": 25,
      "folder": {"id": "456789", "name": "Sprint 1"}
    }
  ]
}
```

#### 获取无文件夹的列表

```bash
GET /clickup/api/v2/space/{space_id}/list
```

#### 获取一个列表

```bash
GET /clickup/api/v2/list/{list_id}
```

#### 创建一个列表

```bash
POST /clickup/api/v2/folder/{folder_id}/list
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'name': 'New List'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/clickup/api/v2/folder/456789/list', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建一个无文件夹的列表

```bash
POST /clickup/api/v2/space/{space_id}/list
```

#### 更新一个列表

```bash
PUT /clickup/api/v2/list/{list_id}
```

#### 删除一个列表

```bash
DELETE /clickup/api/v2/list/{list_id}
```

### 任务

#### 获取任务

```bash
GET /clickup/api/v2/list/{list_id}/task
```

查询参数：
- `archived` - 是否包含已归档的任务（true/false）
- `page` - 页码（从0开始计数）
- `order_by` - 按字段排序（创建时间、更新时间、截止日期）
- `reverse` - 是否反转排序顺序（true/false）
- `subtasks` - 是否包含子任务（true/false）
- `statuses[]` - 按状态过滤
- `include_closed` - 是否包含已关闭的任务（true/false）
- `assignees[]` - 按分配者ID过滤
- `due_date_gt` - 截止日期大于（Unix毫秒）
- `due_date_lt` - 截止日期小于（Unix毫秒）

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/clickup/api/v2/list/901234/task?include_closed=true')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "tasks": [
    {
      "id": "abc123",
      "name": "Implement login feature",
      "status": {"status": "in progress", "type": "custom", "color": "#4194f6"},
      "priority": {"id": "2", "priority": "high", "color": "#f9d900"},
      "due_date": "1709251200000",
      "assignees": [{"id": 123, "username": "Alice Johnson", "email": "alice@acme.com"}],
      "description": "Add OAuth login flow",
      "date_created": "1707436800000",
      "date_updated": "1708646400000"
    }
  ]
}
```

#### 获取一个任务

```bash
GET /clickup/api/v2/task/{task_id}
```

查询参数：
- `custom_task_ids` - 是否使用自定义任务ID（true/false）
- `team_id` - 使用 `custom_task_ids` 时必需
- `include_subtasks` - 是否包含子任务（true/false）

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/clickup/api/v2/task/abc123')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建一个任务

```bash
POST /clickup/api/v2/list/{list_id}/task
Content-Type: application/json

{
  "name": "Task name",
  "description": "Task description",
  "assignees": [123],
  "status": "to do",
  "priority": 2,
  "due_date": 1709251200000,
  "tags": ["api", "backend"],
  "parent": null
}
```

字段：
- `name`（必填）- 任务标题
- `description` - 任务描述（支持Markdown）
- `assignees` - 用户ID数组
- `status` - 状态名称（必须与列表中的状态名称匹配）
- `priority` - 优先级（1=紧急，2=高，3=普通，4=低，null=无）
- `due_date` - Unix时间戳（毫秒）
- `due_date_time` - 是否包含截止日期的时间（true/false）
- `start_date` - Unix时间戳（毫秒）
- `time_estimate` - 时间估算（毫秒）
- `tags` - 标签名称数组
- `parent` - 子任务的父任务ID
- `custom_fields` - 自定义字段对象数组

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'name': 'Complete API integration', 'description': 'Integrate with the new payment API', 'priority': 2, 'due_date': 1709251200000, 'assignees': [123]}).encode()
req = urllib.request.Request('https://gateway.maton.ai/clickup/api/v2/list/901234/task', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 更新一个任务

```bash
PUT /clickup/api/v2/task/{task_id}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'status': 'complete', 'priority': None}).encode()
req = urllib.request.Request('https://gateway.maton.ai/clickup/api/v2/task/abc123', data=data, method='PUT')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 删除一个任务

```bash
DELETE /clickup/api/v2/task/{task_id}
```

#### 获取筛选后的团队任务

```bash
GET /clickup/api/v2/team/{team_id}/task
```

查询参数：
- `page` - 页码（从0开始计数）
- `order_by` - 排序字段
- `statuses[]` - 按状态过滤
- `assignees[]` - 按分配者过滤
- `list_ids[]` - 按列表ID过滤
- `space_ids[]` - 按空间ID过滤
- `folder_ids[]` - 按文件夹ID过滤

### 用户

#### 获取当前用户

```bash
GET /clickup/api/v2/user
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/clickup/api/v2/user')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "user": {
    "id": 123,
    "username": "Alice Johnson",
    "email": "alice@acme.com",
    "color": "#7B68EE",
    "profilePicture": "https://...",
    "initials": "AJ",
    "week_start_day": 0,
    "timezone": "America/New_York"
  }
}
```

### Webhook

#### 获取Webhook

```bash
GET /clickup/api/v2/team/{team_id}/webhook
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/clickup/api/v2/team/1234567/webhook')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建Webhook

```bash
POST /clickup/api/v2/team/{team_id}/webhook
Content-Type: application/json

{
  "endpoint": "https://example.com/webhook",
  "events": ["taskCreated", "taskUpdated", "taskDeleted"],
  "space_id": "90120001",
  "folder_id": "456789",
  "list_id": "901234",
  "task_id": "abc123"
}
```

事件：
- `taskCreated`, `taskUpdated`, `taskDeleted`
- `taskPriorityUpdated`, `taskStatusUpdated`
- `taskAssigneeUpdated`, `taskDueDateUpdated`
- `taskTagUpdated`, `taskCommentPosted`, `taskCommentUpdated`
- `taskTimeEstimateUpdated`, `taskTimeTrackedUpdated`
- `listCreated`, `listUpdated`, `listDeleted`
- `folderCreated`, `folderUpdated`, `folderDeleted`
- `spaceCreated`, `spaceUpdated`, `spaceDeleted`
- `goalCreated`, `goalUpdated`, `goalDeleted`
- `keyResultCreated`, `keyResultUpdated`, `keyResultDeleted`

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'endpoint': 'https://example.com/webhook', 'events': ['taskCreated', 'taskUpdated']}).encode()
req = urllib.request.Request('https://gateway.maton.ai/clickup/api/v2/team/1234567/webhook', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "id": "webhook123",
  "webhook": {
    "id": "webhook123",
    "userid": 123,
    "team_id": "1234567",
    "endpoint": "https://example.com/webhook",
    "client_id": "...",
    "events": ["taskCreated", "taskUpdated"],
    "health": {"status": "active", "fail_count": 0},
    "secret": "..."
  }
}
```

#### 更新Webhook

```bash
PUT /clickup/api/v2/webhook/{webhook_id}
```

#### 删除Webhook

```bash
DELETE /clickup/api/v2/webhook/{webhook_id}
```

## 分页

ClickUp 使用基于页的分页机制。使用 `page` 参数（从0开始计数）：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/clickup/api/v2/list/901234/task?page=0')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

响应每页限制为100个任务。响应中包含一个 `last_page` 布尔字段。继续增加页码，直到 `last_page` 为 `true`。

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/clickup/api/v2/list/901234/task',
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
    'https://gateway.maton.ai/clickup/api/v2/list/901234/task',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
```

## 注意事项

- 任务ID是字符串。
- 时间戳是Unix毫秒。
- 优先级值：1=紧急，2=高，3=普通，4=低，null=无。
- 在API中，工作空间被称为“团队”。
- 状态值必须与列表中配置的状态名称完全匹配。
- 响应每页限制为100条记录。
- 重要提示：当URL包含括号（如 `statuses[]`, `assignees[]`, `list_ids[]`）时，使用 `curl -g` 可以防止全局解析。
- 重要提示：当将curl输出传递给 `jq` 或其他命令时，在某些shell环境中，环境变量 `$MATON_API_KEY` 可能无法正确展开，可能会导致“无效API密钥”错误。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 请求错误或缺少ClickUp连接 |
| 401 | 无效或缺少Maton API密钥 |
| 403 | 禁止访问 - 权限不足 |
| 404 | 资源未找到 |
| 429 | 请求速率限制 |
| 4xx/5xx | 来自ClickUp API的传递错误 |

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

1. 确保您的URL路径以 `clickup` 开头。例如：
- 正确：`https://gateway.maton.ai/clickup/api/v2/team`
- 错误：`https://gateway.maton.ai/api/v2/team`

## 资源

- [ClickUp API概述](https://developer.clickup.com/docs/Getting%20Started.md)
- [获取任务](https://developer.clickup.com/reference/gettasks.md)
- [创建任务](https://developer.clickup.com/reference/createtask.md)
- [更新任务](https://developer.clickup.com/reference/updatetask.md)
- [删除任务](https://developer.clickup.com/reference/deletetask.md)
- [获取空间](https://developer.clickup.com/reference/getspaces.md)
- [获取列表](https://developer.clickup.com/reference/getlists.md)
- [创建Webhook](https://developer.clickup.com/reference/createwebhook.md)
- [自定义字段](https://developer.clickup.com/docs/customfields.md)
- [速率限制](https://developer.clickup.com/docs/rate-limits.md)
- [LLM参考](https://developer.clickup.com/llms.txt)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)