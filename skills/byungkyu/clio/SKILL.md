---
name: clio
description: |
  Clio API integration with managed OAuth. Legal practice management including matters, contacts, activities, tasks, documents, calendar entries, time entries, and billing.
  Use this skill when users want to manage legal practice data in Clio Manage.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
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

# Clio

您可以使用受管理的 OAuth 认证来访问 Clio Manage API，以管理法律实践中的案件、联系人、活动、任务、文档、日历条目、时间记录和账单。

## 快速入门

```bash
# List matters
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/clio/api/v4/matters?fields=id,display_number,description,status')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/clio/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Clio API 端点路径。该网关会将请求代理到 `app.clio.com` 并自动插入您的 OAuth 令牌。

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

您可以在 `https://ctrl.maton.ai` 上管理您的 Clio OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=clio&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'clio'}).encode()
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
    "app": "clio",
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

如果您有多个 Clio 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/clio/api/v4/matters')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略，则网关将使用默认的（最旧的）活动连接。

## API 参考

### 字段选择

默认情况下，Clio 仅返回最基本的字段（`id`、`etag`）。使用 `fields` 参数来请求特定的字段：

```bash
GET /clio/api/v4/matters?fields=id,display_number,description,status
```

对于嵌套资源，请使用大括号语法：

```bash
GET /clio/api/v4/activities?fields=id,type,matter{id,description}
```

### 案件

#### 列出案件

```bash
GET /clio/api/v4/matters?fields=id,display_number,description,status,client_reference
```

#### 获取案件信息

```bash
GET /clio/api/v4/matters/{id}?fields=id,display_number,description,status,open_date,close_date
```

#### 创建案件

```bash
POST /clio/api/v4/matters
Content-Type: application/json

{
  "data": {
    "description": "New Legal Matter",
    "status": "open",
    "client": {"id": 12345}
  }
}
```

#### 更新案件信息

```bash
PATCH /clio/api/v4/matters/{id}
Content-Type: application/json

{
  "data": {
    "description": "Updated Matter Description",
    "status": "closed"
  }
}
```

#### 删除案件

```bash
DELETE /clio/api/v4/matters/{id}
```

### 联系人

#### 列出联系人

```bash
GET /clio/api/v4/contacts?fields=id,name,type,primary_email_address,primary_phone_number
```

#### 获取联系人信息

```bash
GET /clio/api/v4/contacts/{id}?fields=id,name,type,first_name,last_name,company
```

#### 创建联系人（个人）

```bash
POST /clio/api/v4/contacts
Content-Type: application/json

{
  "data": {
    "type": "Person",
    "first_name": "John",
    "last_name": "Doe",
    "email_addresses": [
      {"name": "Work", "address": "john@example.com", "default_email": true}
    ]
  }
}
```

#### 创建联系人（公司）

```bash
POST /clio/api/v4/contacts
Content-Type: application/json

{
  "data": {
    "type": "Company",
    "name": "Acme Corporation"
  }
}
```

#### 更新联系人信息

```bash
PATCH /clio/api/v4/contacts/{id}
Content-Type: application/json

{
  "data": {
    "first_name": "Jane"
  }
}
```

#### 删除联系人

```bash
DELETE /clio/api/v4/contacts/{id}
```

### 活动

#### 列出活动

```bash
GET /clio/api/v4/activities?fields=id,type,date,quantity,matter{id,description}
```

#### 获取活动信息

```bash
GET /clio/api/v4/activities/{id}?fields=id,type,date,quantity,note
```

#### 创建活动

```bash
POST /clio/api/v4/activities
Content-Type: application/json

{
  "data": {
    "type": "TimeEntry",
    "date": "2026-02-11",
    "quantity": 3600,
    "matter": {"id": 12345},
    "note": "Legal research"
  }
}
```

#### 更新活动信息

```bash
PATCH /clio/api/v4/activities/{id}
Content-Type: application/json

{
  "data": {
    "note": "Updated note"
  }
}
```

#### 删除活动

```bash
DELETE /clio/api/v4/activities/{id}
```

### 任务

#### 列出任务

```bash
GET /clio/api/v4/tasks?fields=id,name,status,due_at,priority,matter{id,description}
```

#### 获取任务信息

```bash
GET /clio/api/v4/tasks/{id}?fields=id,name,description,status,due_at,priority
```

#### 创建任务

创建任务时需要提供 `assignee`，包括 `id` 和 `type`（“User”或“Contact”）：

```bash
POST /clio/api/v4/tasks
Content-Type: application/json

{
  "data": {
    "name": "Review contract",
    "due_at": "2026-02-15T17:00:00Z",
    "priority": "Normal",
    "assignee": {"id": 12345, "type": "User"},
    "matter": {"id": 67890}
  }
}
```

#### 更新任务信息

```bash
PATCH /clio/api/v4/tasks/{id}
Content-Type: application/json

{
  "data": {
    "status": "complete"
  }
}
```

#### 删除任务

```bash
DELETE /clio/api/v4/tasks/{id}
```

### 日历条目

#### 列出日历条目

```bash
GET /clio/api/v4/calendar_entries?fields=id,summary,start_at,end_at,matter{id,description}
```

#### 获取日历条目信息

```bash
GET /clio/api/v4/calendar_entries/{id}?fields=id,summary,description,start_at,end_at,location
```

#### 创建日历条目

创建日历条目时需要提供 `calendar_owner`，包括 `id` 和 `type`：

```bash
POST /clio/api/v4/calendar_entries
Content-Type: application/json

{
  "data": {
    "summary": "Client Meeting",
    "start_at": "2026-02-15T10:00:00Z",
    "end_at": "2026-02-15T11:00:00Z",
    "calendar_owner": {"id": 12345, "type": "User"}
  }
}
```

**注意：** 在创建日历条目时尝试将其与案件关联可能会返回 404 错误。要关联案件，请在创建后使用 `PATCH` 方法更新日历条目。

#### 更新日历条目

```bash
PATCH /clio/api/v4/calendar_entries/{id}
Content-Type: application/json

{
  "data": {
    "summary": "Updated Meeting Title"
  }
}
```

#### 删除日历条目

```bash
DELETE /clio/api/v4/calendar_entries/{id}
```

### 文档

#### 列出文档

```bash
GET /clio/api/v4/documents?fields=id,name,content_type,size,matter{id,description}
```

#### 获取文档信息

```bash
GET /clio/api/v4/documents/{id}?fields=id,name,content_type,size,created_at
```

#### 下载文档

```bash
GET /clio/api/v4/documents/{id}/download
```

### 用户

#### 获取当前用户信息

```bash
GET /clio/api/v4/users/who_am_i?fields=id,name,email,enabled
```

#### 列出用户信息

```bash
GET /clio/api/v4/users?fields=id,name,email,enabled,rate
```

### 账单

#### 列出账单信息

```bash
GET /clio/api/v4/bills?fields=id,number,issued_at,due_at,total,balance,state
```

#### 获取账单信息

```bash
GET /clio/api/v4/bills/{id}?fields=id,number,issued_at,due_at,total,balance,state
```

## 分页

Clio 使用基于游标的分页机制。响应中包含分页元数据：

```bash
GET /clio/api/v4/matters?fields=id,description&limit=50
```

响应中的 `meta` 对象包含分页信息：

```json
{
  "data": [...],
  "meta": {
    "paging": {
      "next": "https://app.clio.com/api/v4/matters?page_token=xyz123"
    },
    "records": 50
  }
}
```

使用 `page_token` 参数来获取下一页：

```bash
GET /clio/api/v4/matters?fields=id,description&page_token=xyz123
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/clio/api/v4/matters?fields=id,display_number,description',
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
    'https://gateway.maton.ai/clio/api/v4/matters',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'fields': 'id,display_number,description'}
)
data = response.json()
```

## 注意事项

- 字段选择非常重要——默认响应仅包含 `id` 和 `etag`。
- 嵌套资源使用大括号语法：`matter{id,description}`。
- 仅支持一层嵌套。
- 联系人类型为 `Person` 或 `Company`。
- 任务分配者需要提供 `id` 和 `type`（“User”或“Contact”）。
- 日历条目需要提供 `calendar_owner`，包括 `id` 和 `type`；在创建时尝试关联案件可能会失败——请使用 `PATCH` 方法进行关联。
- 活动的时间以秒为单位（3600 秒 = 1 小时）。
- 每个联系人记录最多只能包含 20 个电子邮件地址、电话号码和地址。
- 活动、文档和账单的 API 需要额外的 OAuth 权限。
- 重要提示：当 URL 中包含括号时，使用 `curl -g` 命令来禁用全局解析。
- 重要提示：当将 curl 输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确展开。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Clio 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 资源未找到 |
| 429 | 常规时间限制（高峰时段每分钟 50 次请求） |
| 4xx/5xx | 来自 Clio API 的传递错误 |

### 速率限制头信息

Clio 在响应中包含速率限制头信息：
- `X-RateLimit-Limit`：60 秒窗口内的最大请求次数。
- `X-RateLimit-Remaining`：当前窗口内剩余的请求次数。
- `X-RateLimit-Reset`：窗口重置的 Unix 时间戳。
- `Retry-After`：被限制时的等待时间（以秒为单位）。

## 资源

- [Clio API 文档](https://docs.developers.clio.com/api-reference/)
- [Clio 字段指南](https://docs.developers.clio.com/api-docs/clio-manage/fields/)
- [Clio 速率限制](https://docs.developers.clio.com/api-docs/clio-manage/rate-limits/)
- [Clio 权限](https://docs.developers.clio.com/api-docs/permissions/)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)