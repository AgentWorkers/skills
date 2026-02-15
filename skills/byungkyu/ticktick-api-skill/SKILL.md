---
name: ticktick
description: |
  TickTick API integration with managed OAuth. Manage tasks, projects, and task lists.
  Use this skill when users want to create, update, complete, or organize tasks and projects in TickTick.
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

# TickTick

使用托管的 OAuth 认证访问 TickTick API，支持对任务和项目进行完整的 CRUD 操作（创建、读取、更新、删除）。

## 快速入门

```bash
# List all projects
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/ticktick/open/v1/project')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/ticktick/{native-api-path}
```

该网关会将请求代理到 `api.ticktick.com`，并自动插入您的 OAuth 令牌。

## 认证

所有请求都必须在 `Authorization` 头部包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 上管理您的 TickTick OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=ticktick&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'ticktick'}).encode()
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
    "connection_id": "1fd9c3aa-6b46-456f-aa21-ed154de23ab7",
    "status": "ACTIVE",
    "creation_time": "2026-02-07T09:55:40.786711Z",
    "last_updated_time": "2026-02-07T09:56:30.403237Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "ticktick",
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

如果您有多个 TickTick 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/ticktick/open/v1/project')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '1fd9c3aa-6b46-456f-aa21-ed154de23ab7')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果未指定，网关将使用默认的（最旧的）活动连接。

## API 参考

### 项目操作

#### 列出项目

```bash
GET /ticktick/open/v1/project
```

**响应：**
```json
[
  {
    "id": "6984773291819e6d58b746a8",
    "name": "🏡Memo",
    "sortOrder": 0,
    "viewMode": "list",
    "kind": "TASK"
  },
  {
    "id": "6984773291819e6d58b746a9",
    "name": "🦄Wishlist",
    "sortOrder": -1099511627776,
    "viewMode": "list",
    "kind": "TASK"
  }
]
```

#### 获取包含任务的项目

```bash
GET /ticktick/open/v1/project/{projectId}/data
```

**响应：**
```json
{
  "project": {
    "id": "69847732b8e5e969f70e7460",
    "name": "👋Welcome",
    "sortOrder": -3298534883328,
    "viewMode": "list",
    "kind": "TASK"
  },
  "tasks": [
    {
      "id": "69847732b8e5e969f70e7464",
      "projectId": "69847732b8e5e969f70e7460",
      "title": "Sample task",
      "content": "Task description",
      "priority": 0,
      "status": 0,
      "tags": [],
      "isAllDay": false
    }
  ],
  "columns": [
    {
      "id": "69847732b8e5e969f70e7463",
      "projectId": "69847732b8e5e969f70e7460",
      "name": "Getting Start",
      "sortOrder": -2199023255552
    }
  ]
}
```

#### 创建项目

```bash
POST /ticktick/open/v1/project
Content-Type: application/json

{
  "name": "My New Project",
  "viewMode": "list"
}
```

**响应：**
```json
{
  "id": "69870cbe8f08b4a6770a38d3",
  "name": "My New Project",
  "sortOrder": 0,
  "viewMode": "list",
  "kind": "TASK"
}
```

**`viewMode` 可选值：**
- `list` - 列表视图
- `kanban` - 看板视图
- `timeline` - 时间轴视图

#### 删除项目

```bash
DELETE /ticktick/open/v1/project/{projectId}
```

成功时返回空响应（状态码 200）。

### 任务操作

#### 获取任务信息

```bash
GET /ticktick/open/v1/project/{projectId}/task/{taskId}
```

**响应：**
```json
{
  "id": "69847732b8e5e969f70e7464",
  "projectId": "69847732b8e5e969f70e7460",
  "sortOrder": -1099511627776,
  "title": "Task title",
  "content": "Task description/notes",
  "timeZone": "Asia/Shanghai",
  "isAllDay": true,
  "priority": 0,
  "status": 0,
  "tags": [],
  "columnId": "69847732b8e5e969f70e7461",
  "etag": "2sayfdsh",
  "kind": "TEXT"
}
```

#### 创建任务

```bash
POST /ticktick/open/v1/task
Content-Type: application/json

{
  "title": "New task",
  "projectId": "6984773291819e6d58b746a8",
  "content": "Task description",
  "priority": 0,
  "dueDate": "2026-02-15T10:00:00+0000",
  "isAllDay": false
}
```

**响应：**
```json
{
  "id": "69870cb08f08b86b38951175",
  "projectId": "6984773291819e6d58b746a8",
  "sortOrder": -1099511627776,
  "title": "New task",
  "timeZone": "America/Los_Angeles",
  "isAllDay": false,
  "priority": 0,
  "status": 0,
  "tags": [],
  "etag": "gl7ibhor",
  "kind": "TEXT"
}
```

**优先级值：**
- `0` - 无
- `1` - 低
- `3` - 中等
- `5` - 高

#### 更新任务

```bash
POST /ticktick/open/v1/task/{taskId}
Content-Type: application/json

{
  "id": "69870cb08f08b86b38951175",
  "projectId": "6984773291819e6d58b746a8",
  "title": "Updated task title",
  "priority": 1
}
```

**响应：**
```json
{
  "id": "69870cb08f08b86b38951175",
  "projectId": "6984773291819e6d58b746a8",
  "title": "Updated task title",
  "priority": 1,
  "status": 0,
  "etag": "hmb7uk8c",
  "kind": "TEXT"
}
```

#### 完成任务

```bash
POST /ticktick/open/v1/project/{projectId}/task/{taskId}/complete
```

成功时返回空响应（状态码 200）。

#### 删除任务

```bash
DELETE /ticktick/open/v1/project/{projectId}/task/{taskId}
```

成功时返回空响应（状态码 200）。

## 任务字段

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `id` | 字符串 | 任务 ID |
| `projectId` | 字符串 | 所属项目 ID |
| `title` | 字符串 | 任务标题 |
| `content` | 字符串 | 任务描述/备注（支持 Markdown 格式） |
| `priority` | 整数 | 优先级：0=无，1=低，3=中等，5=高 |
| `status` | 整数 | 0=活动状态，2=已完成 |
| `dueDate` | 字符串 | 截止日期（ISO 8601 格式） |
| `startDate` | 字符串 | 开始日期（ISO 8601 格式） |
| `isAllDay` | 布尔值 | 任务是否为全天任务 |
| `timeZone` | 字符串 | 时区（例如：`America/Los_Angeles`） |
| `tags` | 数组 | 标签列表 |
| `columnId` | 字符串 | 看板列 ID（如适用） |
| `sortOrder` | 数字 | 项目内的排序顺序 |
| `kind` | 字符串 | 任务类型：`TEXT`、`CHECKLIST` |

## 代码示例

### JavaScript

```javascript
// List all projects
const response = await fetch(
  'https://gateway.maton.ai/ticktick/open/v1/project',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const projects = await response.json();

// Create a task
const createResponse = await fetch(
  'https://gateway.maton.ai/ticktick/open/v1/task',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      title: 'New task',
      projectId: 'PROJECT_ID'
    })
  }
);
```

### Python

```python
import os
import requests

# List all projects
response = requests.get(
    'https://gateway.maton.ai/ticktick/open/v1/project',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
projects = response.json()

# Create a task
response = requests.post(
    'https://gateway.maton.ai/ticktick/open/v1/task',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'title': 'New task',
        'projectId': 'PROJECT_ID'
    }
)
```

## 注意事项

- Open API 仅提供对任务和项目的访问权限。
- 习惯管理、番茄工作法相关功能以及标签无法通过 Open API 调用。
- 任务状态值：`0` = 活动状态，`2` = 已完成。
- 优先级值：`0` = 无，`1` = 低，`3` = 中等，`5` = 高。
- 日期使用带有时区偏移的 ISO 8601 格式（例如：`2026-02-15T10:00:00+0000`）。
- 项目的 `viewMode` 可设置为 `list`、`kanban` 或 `timeline`。
- 在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境中可能无法正确解析环境变量 `$MATON_API_KEY`。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 TickTick 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 资源未找到 |
| 429 | 请求频率限制 |
| 4xx/5xx | 来自 TickTick API 的传递错误 |

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

### 故障排除：应用程序名称错误

1. 确保您的 URL 路径以 `ticktick` 开头。例如：
- 正确：`https://gateway.maton.ai/ticktick/open/v1/project`
- 错误：`https://gateway.maton.ai/open/v1/project`

## 资源

- [TickTick 开发者门户](https://developer.ticktick.com/)
- [TickTick 帮助中心](https://help.ticktick.com/)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持团队](mailto:support@maton.ai)