---
name: sendgrid
description: |
  SendGrid API integration with managed OAuth. Send emails, manage contacts, templates, suppressions, and view email statistics.
  Use this skill when users want to send transactional or marketing emails, manage email lists, handle bounces/unsubscribes, or analyze email performance.
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

# SendGrid

您可以使用托管的 OAuth 认证来访问 SendGrid API。该 API 支持发送交易邮件和营销邮件、管理联系人、模板以及分析邮件发送效果。

## 快速入门

```bash
# Get user profile
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/sendgrid/v3/user/profile')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/sendgrid/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 SendGrid API 端点路径。该代理会将请求转发到 `api.sendgrid.com`，并自动插入您的 OAuth 令牌。

## 认证

所有请求都需要在 `Authorization` 头中包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 上管理您的 SendGrid OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=sendgrid&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'sendgrid'}).encode()
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
    "connection_id": "943c6cd5-9a56-4f5b-8adf-ecd4a140049f",
    "status": "ACTIVE",
    "creation_time": "2026-02-11T10:53:41.817938Z",
    "last_updated_time": "2026-02-11T10:54:05.554084Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "sendgrid",
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

如果您有多个 SendGrid 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/sendgrid/v3/user/profile')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '943c6cd5-9a56-4f5b-8adf-ecd4a140049f')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头，代理将使用默认的（最旧的）活动连接。

## API 参考

所有 SendGrid API 端点都遵循以下格式：

```
/sendgrid/v3/{resource}
```

---

## 发送邮件

### 发送邮件

```bash
POST /sendgrid/v3/mail/send
Content-Type: application/json

{
  "personalizations": [
    {
      "to": [{"email": "recipient@example.com", "name": "Recipient"}],
      "subject": "Hello from SendGrid"
    }
  ],
  "from": {"email": "sender@example.com", "name": "Sender"},
  "content": [
    {
      "type": "text/plain",
      "value": "This is a test email."
    }
  ]
}
```

**使用 HTML 内容：**
```bash
POST /sendgrid/v3/mail/send
Content-Type: application/json

{
  "personalizations": [
    {
      "to": [{"email": "recipient@example.com"}],
      "subject": "HTML Email"
    }
  ],
  "from": {"email": "sender@example.com"},
  "content": [
    {
      "type": "text/html",
      "value": "<h1>Hello</h1><p>This is an HTML email.</p>"
    }
  ]
}
```

**使用模板：**
```bash
POST /sendgrid/v3/mail/send
Content-Type: application/json

{
  "personalizations": [
    {
      "to": [{"email": "recipient@example.com"}],
      "dynamic_template_data": {
        "first_name": "John",
        "order_id": "12345"
      }
    }
  ],
  "from": {"email": "sender@example.com"},
  "template_id": "d-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

---

## 用户信息

### 获取用户信息

```bash
GET /sendgrid/v3/user/profile
```

**响应：**
```json
{
  "type": "user",
  "userid": 59796657
}
```

### 获取账户详情

```bash
GET /sendgrid/v3/user/account
```

---

## 营销联系人

### 列出联系人

```bash
GET /sendgrid/v3/marketing/contacts
```

**响应：**
```json
{
  "result": [],
  "contact_count": 0,
  "_metadata": {
    "self": "https://api.sendgrid.com/v3/marketing/contacts"
  }
}
```

### 搜索联系人

```bash
POST /sendgrid/v3/marketing/contacts/search
Content-Type: application/json

{
  "query": "email LIKE '%@example.com%'"
}
```

### 添加/更新联系人

```bash
PUT /sendgrid/v3/marketing/contacts
Content-Type: application/json

{
  "contacts": [
    {
      "email": "contact@example.com",
      "first_name": "John",
      "last_name": "Doe"
    }
  ]
}
```

**响应：**
```json
{
  "job_id": "2387e363-4104-4225-8960-4a5758492351"
}
```

**注意：** 联人操作是异步的。请使用作业状态端点来检查进度。

### 获取导入作业状态

```bash
GET /sendgrid/v3/marketing/contacts/imports/{job_id}
```

**响应：**
```json
{
  "id": "2387e363-4104-4225-8960-4a5758492351",
  "status": "pending",
  "job_type": "upsert_contacts",
  "results": {
    "requested_count": 1,
    "created_count": 1
  },
  "started_at": "2026-02-11T11:00:14Z"
}
```

### 删除联系人

```bash
DELETE /sendgrid/v3/marketing/contacts?ids=contact_id_1,contact_id_2
```

### 通过 ID 获取联系人

```bash
GET /sendgrid/v3/marketing/contacts/{contact_id}
```

### 通过电子邮件获取联系人

```bash
POST /sendgrid/v3/marketing/contacts/search/emails
Content-Type: application/json

{
  "emails": ["contact@example.com"]
}
```

---

## 营销列表

### 列出所有列表

```bash
GET /sendgrid/v3/marketing/lists
```

**响应：**
```json
{
  "result": [],
  "_metadata": {
    "self": "https://api.sendgrid.com/v3/marketing/lists?page_size=100&page_token="
  }
}
```

### 创建列表

```bash
POST /sendgrid/v3/marketing/lists
Content-Type: application/json

{
  "name": "My Contact List"
}
```

**响应：**
```json
{
  "name": "My Contact List",
  "id": "b050f139-4231-47c8-bf32-94ad76376d3b",
  "contact_count": 0,
  "_metadata": {
    "self": "https://api.sendgrid.com/v3/marketing/lists/b050f139-4231-47c8-bf32-94ad76376d3b"
  }
}
```

### 通过 ID 获取列表

```bash
GET /sendgrid/v3/marketing/lists/{list_id}
```

### 更新列表

```bash
PATCH /sendgrid/v3/marketing/lists/{list_id}
Content-Type: application/json

{
  "name": "Updated List Name"
}
```

### 删除列表

```bash
DELETE /sendgrid/v3/marketing/lists/{list_id}
```

### 将联系人添加到列表

```bash
PUT /sendgrid/v3/marketing/contacts
Content-Type: application/json

{
  "list_ids": ["list_id"],
  "contacts": [
    {"email": "contact@example.com"}
  ]
}
```

---

## 分段

### 列出分段

```bash
GET /sendgrid/v3/marketing/segments
```

### 创建分段

```bash
POST /sendgrid/v3/marketing/segments
Content-Type: application/json

{
  "name": "Active Users",
  "query_dsl": "email_clicks > 0"
}
```

### 通过 ID 获取分段

```bash
GET /sendgrid/v3/marketing/segments/{segment_id}
```

### 删除分段

```bash
DELETE /sendgrid/v3/marketing/segments/{segment_id}
```

---

## 模板

### 列出模板

```bash
GET /sendgrid/v3/templates
```

**使用生成过滤器：**
```bash
GET /sendgrid/v3/templates?generations=dynamic
```

### 创建模板

```bash
POST /sendgrid/v3/templates
Content-Type: application/json

{
  "name": "My Template",
  "generation": "dynamic"
}
```

**响应：**
```json
{
  "id": "d-ffcdb43ed8a04beba48a702e1717ddb5",
  "name": "My Template",
  "generation": "dynamic",
  "updated_at": "2026-02-11 11:00:20",
  "versions": []
}
```

### 通过 ID 获取模板

```bash
GET /sendgrid/v3/templates/{template_id}
```

### 更新模板

```bash
PATCH /sendgrid/v3/templates/{template_id}
Content-Type: application/json

{
  "name": "Updated Template Name"
}
```

### 删除模板

```bash
DELETE /sendgrid/v3/templates/{template_id}
```

### 创建模板版本

```bash
POST /sendgrid/v3/templates/{template_id}/versions
Content-Type: application/json

{
  "name": "Version 1",
  "subject": "{{subject}}",
  "html_content": "<html><body><h1>Hello {{name}}</h1></body></html>",
  "active": 1
}
```

**响应：**
```json
{
  "id": "54230a99-1e89-4edf-821d-d4925b40c64b",
  "template_id": "d-ffcdb43ed8a04beba48a702e1717ddb5",
  "active": 1,
  "name": "Version 1",
  "html_content": "<html><body><h1>Hello {{name}}</h1></body></html>",
  "plain_content": "Hello {{name}}",
  "generate_plain_content": true,
  "subject": "{{subject}}",
  "editor": "code",
  "thumbnail_url": "//..."
}
```

---

## 发件人

### 列出发件人

```bash
GET /sendgrid/v3/senders
```

### 创建发件人

```bash
POST /sendgrid/v3/senders
Content-Type: application/json

{
  "nickname": "My Sender",
  "from": {"email": "sender@example.com", "name": "Sender Name"},
  "reply_to": {"email": "reply@example.com", "name": "Reply To"},
  "address": "123 Main St",
  "city": "San Francisco",
  "country": "USA"
}
```

**响应：**
```json
{
  "id": 8513177,
  "nickname": "My Sender",
  "from": {"email": "sender@example.com", "name": "Sender Name"},
  "reply_to": {"email": "reply@example.com", "name": "Reply To"},
  "address": "123 Main St",
  "city": "San Francisco",
  "country": "USA",
  "verified": {"status": false, "reason": null},
  "updated_at": 1770786031,
  "created_at": 1770786031,
  "locked": false
}
```

**注意：** 使用前需要验证发件人。请检查 `verified.status` 属性。

### 通过 ID 获取发件人

```bash
GET /sendgrid/v3/senders/{sender_id}
```

### 更新发件人

```bash
PATCH /sendgrid/v3/senders/{sender_id}
Content-Type: application/json

{
  "nickname": "Updated Sender Name"
}
```

### 删除发件人

```bash
DELETE /sendgrid/v3/senders/{sender_id}
```

---

## 邮件拦截

### 拒收邮件

```bash
# List bounces
GET /sendgrid/v3/suppression/bounces

# Get bounce by email
GET /sendgrid/v3/suppression/bounces/{email}

# Delete bounces
DELETE /sendgrid/v3/suppression/bounces
Content-Type: application/json

{
  "emails": ["bounce@example.com"]
}
```

### 阻止发送邮件

```bash
# List blocks
GET /sendgrid/v3/suppression/blocks

# Get block by email
GET /sendgrid/v3/suppression/blocks/{email}

# Delete blocks
DELETE /sendgrid/v3/suppression/blocks
Content-Type: application/json

{
  "emails": ["blocked@example.com"]
}
```

### 无效邮件

```bash
# List invalid emails
GET /sendgrid/v3/suppression/invalid_emails

# Delete invalid emails
DELETE /sendgrid/v3/suppression/invalid_emails
Content-Type: application/json

{
  "emails": ["invalid@example.com"]
}
```

### 垃圾邮件报告

```bash
# List spam reports
GET /sendgrid/v3/suppression/spam_reports

# Delete spam reports
DELETE /sendgrid/v3/suppression/spam_reports
Content-Type: application/json

{
  "emails": ["spam@example.com"]
}
```

### 全局取消订阅

```bash
# List global unsubscribes
GET /sendgrid/v3/suppression/unsubscribes

# Add to global unsubscribes
POST /sendgrid/v3/asm/suppressions/global
Content-Type: application/json

{
  "recipient_emails": ["unsubscribe@example.com"]
}
```

---

## 取消订阅组（ASM）

### 列出组

```bash
GET /sendgrid/v3/asm/groups
```

### 创建组

```bash
POST /sendgrid/v3/asm/groups
Content-Type: application/json

{
  "name": "Weekly Newsletter",
  "description": "Weekly newsletter updates"
}
```

**响应：**
```json
{
  "name": "Weekly Newsletter",
  "id": 122741,
  "description": "Weekly newsletter updates",
  "is_default": false
}
```

### 通过 ID 获取组

```bash
GET /sendgrid/v3/asm/groups/{group_id}
```

### 更新组

```bash
PATCH /sendgrid/v3/asm/groups/{group_id}
Content-Type: application/json

{
  "name": "Updated Group Name"
}
```

### 删除组

```bash
DELETE /sendgrid/v3/asm/groups/{group_id}
```

### 向组添加拦截规则

```bash
POST /sendgrid/v3/asm/groups/{group_id}/suppressions
Content-Type: application/json

{
  "recipient_emails": ["user@example.com"]
}
```

### 查看组内的拦截规则

```bash
GET /sendgrid/v3/asm/groups/{group_id}/suppressions
```

---

## 统计数据

### 获取全局统计信息

```bash
GET /sendgrid/v3/stats?start_date=2026-02-01
```

**指定结束日期：**
```bash
GET /sendgrid/v3/stats?start_date=2026-02-01&end_date=2026-02-28
```

**响应：**
```json
[
  {
    "date": "2026-02-01",
    "stats": [
      {
        "metrics": {
          "blocks": 0,
          "bounce_drops": 0,
          "bounces": 0,
          "clicks": 0,
          "deferred": 0,
          "delivered": 0,
          "invalid_emails": 0,
          "opens": 0,
          "processed": 0,
          "requests": 0,
          "spam_report_drops": 0,
          "spam_reports": 0,
          "unique_clicks": 0,
          "unique_opens": 0,
          "unsubscribe_drops": 0,
          "unsubscribes": 0
        }
      }
    ]
  }
]
```

### 类别统计信息

```bash
GET /sendgrid/v3/categories/stats?start_date=2026-02-01&categories=category1,category2
```

### 邮箱提供商统计信息

```bash
GET /sendgrid/v3/mailbox_providers/stats?start_date=2026-02-01
```

### 浏览器统计信息

```bash
GET /sendgrid/v3/browsers/stats?start_date=2026-02-01
```

---

## API 密钥

### 列出 API 密钥

```bash
GET /sendgrid/v3/api_keys
```

**响应：**
```json
{
  "result": [
    {
      "name": "MatonTest",
      "api_key_id": "WJBgv5EKR8y0nn2F8Qfk5w"
    }
  ]
}
```

### 创建 API 密钥

```bash
POST /sendgrid/v3/api_keys
Content-Type: application/json

{
  "name": "New API Key",
  "scopes": ["mail.send", "alerts.read"]
}
```

### 通过 ID 获取 API 密钥

```bash
GET /sendgrid/v3/api_keys/{api_key_id}
```

### 更新 API 密钥

```bash
PATCH /sendgrid/v3/api_keys/{api_key_id}
Content-Type: application/json

{
  "name": "Updated Key Name"
}
```

### 删除 API 密钥

```bash
DELETE /sendgrid/v3/api_keys/{api_key_id}
```

---

## 分页

SendGrid 的营销 API 端点使用基于令牌的分页机制：

```bash
GET /sendgrid/v3/marketing/lists?page_size=100&page_token={token}
```

**响应包含：**
```json
{
  "result": [...],
  "_metadata": {
    "self": "https://api.sendgrid.com/v3/marketing/lists?page_size=100&page_token=",
    "next": "https://api.sendgrid.com/v3/marketing/lists?page_size=100&page_token=abc123"
  }
}
```

对于邮件拦截端点，请使用 `limit` 和 `offset` 参数进行分页：

```bash
GET /sendgrid/v3/suppression/bounces?limit=100&offset=0
```

## 代码示例

### JavaScript

```javascript
// Send an email
const response = await fetch(
  'https://gateway.maton.ai/sendgrid/v3/mail/send',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      personalizations: [{
        to: [{email: 'recipient@example.com'}],
        subject: 'Hello'
      }],
      from: {email: 'sender@example.com'},
      content: [{type: 'text/plain', value: 'Hello World'}]
    })
  }
);
```

### Python

```python
import os
import requests

# Get email stats
response = requests.get(
    'https://gateway.maton.ai/sendgrid/v3/stats',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'start_date': '2026-02-01'}
)
data = response.json()
for day in data:
    metrics = day['stats'][0]['metrics']
    print(f"{day['date']}: {metrics['delivered']} delivered, {metrics['opens']} opens")
```

## 注意事项

- 所有请求都使用 JSON 格式的数据。
- 日期格式为 YYYY-MM-DD。
- 动态模板的 ID 以 `d-` 开头。
- 邮件发送成功时返回状态码 202（而非 200）。
- 营销联系人操作是异步的，请使用作业状态端点来查看进度。
- 邮件拦截端点支持使用 `start_time` 和 `end_time`（Unix 时间戳）进行日期过滤。
- **重要提示：** 当 URL 中包含括号时，使用 `curl -g` 选项来禁用全局解析。
- **重要提示：** 在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境中可能无法正确解析 `$MATON_API_KEY` 环境变量。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 请求错误或验证失败 |
| 401 | Maton API 密钥无效或缺失 |
| 403 | 权限不足 |
| 404 | 资源未找到 |
| 429 | 请求频率限制 |
| 500 | 服务器内部错误 |

### 故障排除：API 密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证 API 密钥的有效性：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用名称无效

1. 确保您的 URL 路径以 `sendgrid` 开头。例如：
- 正确格式：`https://gateway.maton.ai/sendgrid/v3/user/profile`
- 错误格式：`https://gateway.maton.ai/v3/user/profile`

## 资源

- [SendGrid API 文档](https://www.twilio.com/docs/sendgrid/api-reference)
- [发送邮件 API](https://www.twilio.com/docs/sendgrid/api-reference/mail-send)
- [营销活动 API](https://www.twilio.com/docs/sendgrid/api-reference/contacts)
- [邮件拦截概述](https://www.twilio.com/docs/sendgrid/api-reference/suppressions)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)