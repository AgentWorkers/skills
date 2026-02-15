---
name: podio
description: |
  Podio API integration with managed OAuth. Manage workspaces, apps, items, tasks, and comments.
  Use this skill when users want to read, create, update, or delete Podio items, manage tasks, or interact with Podio apps and workspaces.
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

# Podio

您可以使用受管理的OAuth认证来访问Podio API，从而管理组织、工作空间（spaces）、应用程序（apps）、项目（items）、任务（tasks）、评论（comments）和文件（files）。

## 快速入门

```bash
# List organizations
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/podio/org/')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/podio/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的Podio API端点路径。该网关会将请求代理到 `api.podio.com` 并自动插入您的OAuth令牌。

## 认证

所有请求都需要在 `Authorization` 标头中包含Maton API密钥：

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

您可以在 `https://ctrl.maton.ai` 上管理您的Podio OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=podio&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'podio'}).encode()
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
    "app": "podio",
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

如果您有多个Podio连接，请使用 `Maton-Connection` 标头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/podio/org/')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API参考

### 组织操作

#### 列出组织

返回用户所属的所有组织和工作空间。

```bash
GET /podio/org/
```

**响应：**
```json
[
  {
    "org_id": 123456,
    "name": "My Organization",
    "url": "https://podio.com/myorg",
    "url_label": "myorg",
    "type": "premium",
    "role": "admin",
    "status": "active",
    "spaces": [
      {
        "space_id": 789,
        "name": "Project Space",
        "url": "https://podio.com/myorg/project-space",
        "role": "admin"
      }
    ]
  }
]
```

#### 获取组织信息

```bash
GET /podio/org/{org_id}
```

### 工作空间（Workspace）操作

#### 获取工作空间信息

```bash
GET /podio/space/{space_id}
```

**响应：**
```json
{
  "space_id": 789,
  "name": "Project Space",
  "privacy": "closed",
  "auto_join": false,
  "url": "https://podio.com/myorg/project-space",
  "url_label": "project-space",
  "role": "admin",
  "created_on": "2025-01-15T10:30:00Z",
  "created_by": {
    "user_id": 12345,
    "name": "John Doe"
  }
}
```

#### 创建工作空间

```bash
POST /podio/space/
Content-Type: application/json

{
  "org_id": 123456,
  "name": "New Project Space",
  "privacy": "closed",
  "auto_join": false,
  "post_on_new_app": true,
  "post_on_new_member": true
}
```

**响应：**
```json
{
  "space_id": 790,
  "url": "https://podio.com/myorg/new-project-space"
}
```

### 应用程序操作

#### 按工作空间获取应用程序

```bash
GET /podio/app/space/{space_id}/
```

可选查询参数：
- `includeinactive` - 包括非活动应用程序（默认值：false）

#### 获取应用程序信息

```bash
GET /podio/app/{app_id}
```

**响应：**
```json
{
  "app_id": 456,
  "status": "active",
  "space_id": 789,
  "config": {
    "name": "Tasks",
    "item_name": "Task",
    "description": "Track project tasks",
    "icon": "list"
  },
  "fields": [...]
}
```

### 项目操作

#### 获取项目信息

```bash
GET /podio/item/{item_id}
```

可选查询参数：
- `mark_as_viewed` - 将通知标记为已查看（默认值：true）

**响应：**
```json
{
  "item_id": 123,
  "title": "Complete project plan",
  "app": {
    "app_id": 456,
    "name": "Tasks"
  },
  "fields": [
    {
      "field_id": 1,
      "external_id": "status",
      "type": "category",
      "values": [{"value": {"text": "In Progress"}}]
    }
  ],
  "created_on": "2025-01-20T14:00:00Z",
  "created_by": {
    "user_id": 12345,
    "name": "John Doe"
  }
}
```

#### 过滤项目

```bash
POST /podio/item/app/{app_id}/filter/
Content-Type: application/json

{
  "sort_by": "created_on",
  "sort_desc": true,
  "filters": {
    "status": [1, 2]
  },
  "limit": 30,
  "offset": 0
}
```

**响应：**
```json
{
  "total": 150,
  "filtered": 45,
  "items": [
    {
      "item_id": 123,
      "title": "Complete project plan",
      "fields": [...],
      "comment_count": 5,
      "file_count": 2
    }
  ]
}
```

#### 添加新项目

```bash
POST /podio/item/app/{app_id}/
Content-Type: application/json

{
  "fields": {
    "title": "New task",
    "status": 1,
    "due-date": {"start": "2025-02-15"}
  },
  "tags": ["urgent", "project-alpha"],
  "file_ids": [12345]
}
```

可选查询参数：
- `hook` - 执行钩子（default: true）
- `silent` - 抑制通知（default: false）

**响应：**
```json
{
  "item_id": 124,
  "title": "New task"
}
```

#### 更新项目信息

```bash
PUT /podio/item/{item_id}
Content-Type: application/json

{
  "fields": {
    "status": 2
  },
  "revision": 5
}
```

可选查询参数：
- `hook` - 执行钩子（default: true）
- `silent` - 抑制通知（default: false）

**响应：**
```json
{
  "revision": 6,
  "title": "New task"
}
```

#### 删除项目

```bash
DELETE /podio/item/{item_id}
```

可选查询参数：
- `hook` - 执行钩子（default: true）
- `silent` - 抑制通知（default: false）

### 任务操作

#### 获取任务信息

**注意：** 任务至少需要一个过滤条件：`org`、`space`、`app`、`responsible`、`reference`、`created_by` 或 `completed_by`。

```bash
GET /podio/task/?org={org_id}
GET /podio/task/?space={space_id}
GET /podio/task/?app={app_id}&completed=false
```

查询参数：
- `org` - 按组织ID过滤（如果没有其他过滤条件，则此参数为必填）
- `space` - 按工作空间ID过滤
- `app` - 按应用程序ID过滤
- `completed` - 按完成状态过滤（`true` 或 `false`）
- `responsible` - 按负责用户ID过滤
- `created_by` - 按创建者过滤
- `due_date` - 日期范围（YYYY-MM-DD-YYYY-MM-DD）
- `limit` - 最大结果数量
- `offset` - 结果偏移量
- `sort_by` - 排序方式：created_on, completed_on, rank（默认值：rank）
- `grouping` - 分组方式：due_date, created_by, responsible, app, space, org

#### 获取任务信息

```bash
GET /podio/task/{task_id}
```

**响应：**
```json
{
  "task_id": 789,
  "text": "Review project proposal",
  "description": "Detailed review of the Q1 proposal",
  "status": "active",
  "due_date": "2025-02-15",
  "due_time": "17:00:00",
  "responsible": {
    "user_id": 12345,
    "name": "John Doe"
  },
  "created_on": "2025-01-20T10:00:00Z",
  "labels": [
    {"label_id": 1, "text": "High Priority", "color": "red"}
  ]
}
```

#### 创建任务

```bash
POST /podio/task/
Content-Type: application/json

{
  "text": "Review project proposal",
  "description": "Detailed review of the Q1 proposal",
  "due_date": "2025-02-15",
  "due_time": "17:00:00",
  "responsible": 12345,
  "private": false,
  "ref_type": "item",
  "ref_id": 123,
  "labels": [1, 2]
}
```

可选查询参数：
- `hook` - 执行钩子（default: true）
- `silent` - 抑制通知（default: false）

**响应：**
```json
{
  "task_id": 790,
  ...
}
```

### 评论操作

#### 获取对象的评论信息

```bash
GET /podio/comment/{type}/{id}/
```

其中 `{type}` 是对象类型（例如 "item"、"task"），`{id}` 是对象ID。

可选查询参数：
- `limit` - 最多显示的评论数量（默认值：100）
- `offset` - 分页偏移量（默认值：0）

**响应：**
```json
[
  {
    "comment_id": 456,
    "value": "This looks great!",
    "created_on": "2025-01-20T15:30:00Z",
    "created_by": {
      "user_id": 12345,
      "name": "John Doe"
    },
    "files": []
  }
]
```

#### 向对象添加评论

```bash
POST /podio/comment/{type}/{id}
Content-Type: application/json

{
  "value": "Great progress on this task!",
  "file_ids": [12345],
  "embed_url": "https://example.com/doc"
}
```

可选查询参数：
- `alertInvite` - 自动邀请被提及的用户（default: false）
- `hook` - 执行钩子（default: true）
- `silent` - 抑制通知（default: false）

**响应：**
```json
{
  "comment_id": 457,
  ...
}
```

## 分页

Podio使用基于偏移量的分页机制，通过 `limit` 和 `offset` 参数实现分页：

```bash
POST /podio/item/app/{app_id}/filter/
Content-Type: application/json

{
  "limit": 30,
  "offset": 0
}
```

响应中包含总记录数：
```json
{
  "total": 150,
  "filtered": 45,
  "items": [...]
}
```

要查看后续页面，请增加 `offset` 值：
```json
{
  "limit": 30,
  "offset": 30
}
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/podio/org/',
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
    'https://gateway.maton.ai/podio/org/',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
```

## 注意事项

- 组织ID、工作空间ID、应用程序ID和项目ID均为整数。
- 字段值可以通过 `field_id` 或 `external_id` 来指定。
- 分类字段使用选项ID（整数），而不是文本值。
- 删除项目时会同时删除关联的任务（级联删除）。
- 任务操作至少需要一个过滤条件（org、space、app、responsible、reference、created_by 或 completed_by）。
- 对于批量操作，使用 `silent=true` 可以抑制通知。
- 使用 `hook=false` 可以跳过Webhook触发。
- 在更新请求中包含 `revision` 以检测冲突（如果发生冲突，返回409状态码）。
- **重要提示：** 当URL包含括号时，使用 `curl -g` 可以防止glob解析。
- **重要提示：** 当将curl输出传递给 `jq` 或其他命令时，在某些shell环境中环境变量 `$MATON_API_KEY` 可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立Podio连接或请求无效 |
| 401 | Maton API密钥无效或缺失 |
| 403 | 禁止访问 - 权限不足 |
| 404 | 资源未找到 |
| 409 | 更新时发生冲突（版本号不匹配） |
| 410 | 资源已被删除 |
| 429 | 请求频率受限 |
| 4xx/5xx | 来自Podio API的传递错误 |

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

1. 确保您的URL路径以 `podio` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/podio/org/`
- 错误的路径：`https://gateway.maton.ai/org/`

## 资源

- [Podio API文档](https://developers.podio.com/doc)
- [Podio API认证](https://developers.podio.com/authentication)
- [Podio项目API](https://developers.podio.com/doc/items)
- [Podio任务API](https://developers.podio.com/doc/tasks)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)