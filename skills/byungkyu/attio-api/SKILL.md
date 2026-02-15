---
name: attio
description: |
  Attio API integration with managed OAuth. Manage CRM data including people, companies, and custom objects.
  Use this skill when users want to create, read, update, or delete records in Attio, manage tasks, or query CRM data.
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

# Attio

通过管理的 OAuth 认证来访问 Attio REST API。您可以管理 CRM 对象、记录、任务、评论和工作区数据。

## 快速入门

```bash
# List all objects in workspace
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/attio/v2/objects')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/attio/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Attio API 端点路径。该网关会将请求代理到 `api.attio.com` 并自动插入您的 OAuth 令牌。

## 认证

所有请求都必须在 `Authorization` 头中包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 管理您的 Attio OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=attio&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'attio'}).encode()
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
    "connection_id": "67b77f19-206e-494c-82c2-8668396fc1f1",
    "status": "ACTIVE",
    "creation_time": "2026-02-06T03:13:17.061608Z",
    "last_updated_time": "2026-02-06T03:13:17.061617Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "attio",
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

如果您有多个 Attio 连接，请使用 `Maton-Connection` 头指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/attio/v2/objects')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '67b77f19-206e-494c-82c2-8668396fc1f1')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略，则网关将使用默认的（最旧的）活动连接。

## API 参考

### 对象

对象是数据结构的定义（例如人员、公司或自定义对象）。

#### 列出对象

```bash
GET /attio/v2/objects
```

返回工作区中所有系统定义和自定义的对象。

#### 获取对象信息

```bash
GET /attio/v2/objects/{object}
```

通过 slug（例如 `people`、`companies`）或 UUID 获取特定对象。

### 属性

属性定义了对象上的字段。

#### 列出属性

```bash
GET /attio/v2/objects/{object}/attributes
```

返回对象的所有属性。

### 记录

记录是实际的数据条目（例如人员、公司等）。

#### 查询记录

```bash
POST /attio/v2/objects/{object}/records/query
Content-Type: application/json

{
  "limit": 50,
  "offset": 0,
  "filter": {},
  "sorts": []
}
```

查询参数：
- `limit`：最大结果数量（默认为 500）
- `offset`：要跳过的记录数量
- `filter`：过滤条件对象
- `sorts`：排序规则数组

#### 获取记录信息

```bash
GET /attio/v2/objects/{object}/records/{record_id}
```

#### 创建记录

```bash
POST /attio/v2/objects/{object}/records
Content-Type: application/json

{
  "data": {
    "values": {
      "name": [{"first_name": "John", "last_name": "Doe", "full_name": "John Doe"}],
      "email_addresses": ["john@example.com"]
    }
  }
}
```

注意：对于 `personal-name` 类型的属性（例如人员中的 `name`），在创建记录时必须同时提供 `full_name`、`first_name` 和 `last_name`。

#### 更新记录

```bash
PATCH /attio/v2/objects/{object}/records/{record_id}
Content-Type: application/json

{
  "data": {
    "values": {
      "job_title": "Software Engineer"
    }
  }
}
```

#### 删除记录

```bash
DELETE /attio/v2/objects/{object}/records/{record_id}
```

### 任务

#### 列出任务

```bash
GET /attio/v2/tasks?limit=50
```

查询参数：
- `limit`：最大结果数量（默认为 500）
- `offset`：要跳过的记录数量
- `sort`：`created_at:asc` 或 `created_at:desc`
- `linked_object`：按对象类型过滤（例如 `people`）
- `linked_record_id`：按特定记录过滤
- `assignee`：按分配者的电子邮件/ID 过滤
- `is_completed`：按完成状态过滤（true/false）

#### 获取任务信息

```bash
GET /attio/v2/tasks/{task_id}
```

#### 创建任务

```bash
POST /attio/v2/tasks
Content-Type: application/json

{
  "data": {
    "content": "Follow up with customer",
    "format": "plaintext",
    "deadline_at": "2026-02-15T00:00:00.000000000Z",
    "is_completed": false,
    "assignees": [],
    "linked_records": [
      {
        "target_object": "companies",
        "target_record_id": "16f2fc57-5d22-48b8-b9db-8b0e6d99e9bc"
      }
    ]
  }
}
```

必填字段：`content`、`format`、`assignees`

#### 更新任务

```bash
PATCH /attio/v2/tasks/{task_id}
Content-Type: application/json

{
  "data": {
    "is_completed": true
  }
}
```

#### 删除任务

```bash
DELETE /attio/v2/tasks/{task_id}
```

### 工作区成员

#### 列出工作区成员

```bash
GET /attio/v2/workspace_members
```

#### 获取工作区成员信息

```bash
GET /attio/v2/workspace_members/{workspace_member_id}
```

### 自我（令牌信息）

#### 识别当前令牌

```bash
GET /attio/v2/self
```

返回当前访问令牌的工作区信息和 OAuth 权限范围。

### 评论

#### 创建评论

```bash
POST /attio/v2/comments
Content-Type: application/json

{
  "data": {
    "format": "plaintext",
    "content": "This is a comment",
    "author": {
      "type": "workspace-member",
      "id": "{workspace_member_id}"
    },
    "record": {
      "object": "companies",
      "record_id": "{record_id}"
    }
  }
}
```

### 列表（需要 `list_configuration:read` 权限范围）

#### 列出所有列表

```bash
GET /attio/v2/lists
```

### 备注（需要 `note:read` 权限范围）

#### 列出备注

```bash
GET /attio/v2/notes?limit=50
```

查询参数：
- `limit`：最大结果数量（默认为 10，最大为 50）
- `offset`：要跳过的记录数量
- `parent_object`：包含备注的对象的 slug
- `parent_record_id`：按特定记录过滤

## 分页

Attio 支持两种分页方法：

### Limit/Offset 分页

```bash
GET /attio/v2/tasks?limit=50&offset=0
GET /attio/v2/tasks?limit=50&offset=50
GET /attio/v2/tasks?limit=50&offset=100
```

### 基于游标的分页（针对某些端点）

```bash
GET /attio/v2/meetings?limit=50
GET /attio/v2/meetings?limit=50&cursor={next_cursor}
```

当还有更多结果时，响应中会包含 `pagination.next_cursor`。

## 代码示例

### JavaScript

```javascript
// Query company records
const response = await fetch(
  'https://gateway.maton.ai/attio/v2/objects/companies/records/query',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ limit: 10 })
  }
);
const data = await response.json();
```

### Python

```python
import os
import requests

# Query company records
response = requests.post(
    'https://gateway.maton.ai/attio/v2/objects/companies/records/query',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={'limit': 10}
)
data = response.json()
```

## 注意事项

- 对象的 slug 采用小写蛇形命名法（例如 `people`、`companies`）。
- 记录 ID 和其他 ID 都是 UUID。
- 对于 `personal-name` 类型的属性，在创建记录时必须包含 `full_name`。
- 创建任务时需要指定 `format: "plaintext"` 和 `assignees` 数组（可以为空）。
- 某些端点需要额外的 OAuth 权限范围（列表、备注、Webhook）。
- 请求速率限制：每秒 100 次读取请求，25 次写入请求。
- 重要提示：当 URL 包含括号时，使用 `curl -g` 以禁用全局解析。
- 重要提示：当将 curl 输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确展开。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 未找到 Attio 连接或验证错误 |
| 401 | Maton API 密钥无效或缺失 |
| 403 | OAuth 权限范围不足 |
| 404 | 资源未找到 |
| 429 | 请求速率受限 |
| 4xx/5xx | 来自 Attio API 的传递错误 |

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

### 故障排除：权限范围不足

如果收到关于权限范围不足的 403 错误，请联系 Maton 支持团队（support@maton.ai），并提供您需要的具体操作/API 和使用场景。

### 故障排除：应用程序名称无效

1. 确保您的 URL 路径以 `attio` 开头。例如：
- 正确：`https://gateway.maton.ai/attio/v2/objects`
- 错误：`https://gateway.maton.ai/v2/objects`

## 资源

- [Attio API 概述](https://docs.attio.com/rest-api/overview)
- [Attio API 参考](https://docs.attio.com/rest-api/endpoint-reference)
- [记录 API](https://docs.attio.com/rest-api/endpoint-reference/records)
- [对象 API](https://docs.attio.com/rest-api/endpoint-reference/objects)
- [任务 API](https://docs.attio.com/rest-api/endpoint-reference/tasks)
- [速率限制](https://docs.attio.com/rest-api/guides/rate-limiting)
- [分页](https://docs.attio.com/rest-api/guides/pagination)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)