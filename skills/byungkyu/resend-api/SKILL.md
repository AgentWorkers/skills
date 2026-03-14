---
name: resend
description: >
  **API集成（支持管理式认证）**  
  该功能允许用户通过API发送交易性电子邮件、管理域名、联系人信息、邮件模板以及执行邮件广播操作。  
  当用户需要发送电子邮件、管理邮件模板、创建联系人列表或设置邮件广播时，可使用此功能。  
  对于其他第三方应用程序，建议使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。
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
# 重发（Resend）

通过管理认证方式访问重发（Resend）API，可以发送交易型电子邮件、管理域名、联系人信息、模板、广播消息以及配置Webhook。

## 快速入门

```bash
# List sent emails
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/resend/emails')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/resend/{endpoint}
```

该网关会将请求代理到`api.resend.com`，并自动插入您的API密钥。

## 认证

所有请求都必须在`Authorization`头部包含Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为`MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在[maton.ai](https://maton.ai)登录或创建账户。
2. 访问[maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在`https://ctrl.maton.ai`管理您的重发连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=resend&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'resend'}).encode()
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
    "connection_id": "528c8f70-23f4-46d5-bd9f-01d0d043e573",
    "status": "ACTIVE",
    "creation_time": "2026-03-13T00:19:36.809599Z",
    "last_updated_time": "2026-03-13T09:59:08.443568Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "resend",
    "metadata": {},
    "method": "API_KEY"
  }
}
```

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

如果您有多个重发连接，请使用`Maton-Connection`头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/resend/emails')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '528c8f70-23f4-46d5-bd9f-01d0d043e573')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API参考

### 电子邮件（Emails）

发送和管理交易型电子邮件。

#### 发送电子邮件

```bash
POST /resend/emails
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    'from': 'you@yourdomain.com',
    'to': ['recipient@example.com'],
    'subject': 'Hello from Resend',
    'html': '<p>Welcome to our service!</p>'
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/resend/emails', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**请求体：**
| 字段 | 类型 | 是否必填 | 说明 |
|-------|------|----------|-------------|
| `from` | string | 是 | 发件人邮箱（必须来自已验证的域名） |
| `to` | string[] | 是 | 收件人邮箱地址 |
| `subject` | string | 是 | 邮件主题 |
| `html` | string | 否 | HTML内容 |
| `text` | string | 否 | 纯文本内容 |
| `cc` | string[] | 否 | 抄送收件人 |
| `bcc` | string[] | 否 | 密件抄送收件人 |
| `reply_to` | string[] | 否 | 回复收件人地址 |
| `attachments` | object[] | 否 | 附件 |
| `tags` | object[] | 否 | 用于追踪的邮件标签 |
| `scheduled_at` | string | 否 | 预定发送时间的ISO 8601格式日期 |

**响应：**
```json
{
  "id": "a52ac168-338f-4fbc-9354-e6049b193d99"
}
```

#### 批量发送电子邮件

```bash
POST /resend/emails/batch
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps([
    {'from': 'you@yourdomain.com', 'to': ['a@example.com'], 'subject': 'Email 1', 'text': 'Content 1'},
    {'from': 'you@yourdomain.com', 'to': ['b@example.com'], 'subject': 'Email 2', 'text': 'Content 2'}
]).encode()
req = urllib.request.Request('https://gateway.maton.ai/resend/emails/batch', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 列出电子邮件

```bash
GET /resend/emails
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/resend/emails')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": [
    {
      "id": "a52ac168-338f-4fbc-9354-e6049b193d99",
      "from": "you@yourdomain.com",
      "to": ["recipient@example.com"],
      "subject": "Hello from Resend",
      "created_at": "2026-03-13T10:00:00.000Z"
    }
  ]
}
```

#### 获取电子邮件信息

```bash
GET /resend/emails/{email_id}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/resend/emails/{email_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 更新电子邮件信息

```bash
PATCH /resend/emails/{email_id}
```

#### 取消已安排的电子邮件

```bash
DELETE /resend/emails/{email_id}
```

### 域名（Domains）

管理用于发送电子邮件的域名。

#### 列出域名

```bash
GET /resend/domains
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/resend/domains')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": [
    {
      "id": "5eb93a2e-e849-40a1-81b7-ed0fb574ddd8",
      "name": "yourdomain.com",
      "status": "verified",
      "created_at": "2026-03-13T10:00:00.000Z"
    }
  ]
}
```

#### 创建域名

```bash
POST /resend/domains
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'name': 'yourdomain.com'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/resend/domains', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "id": "5eb93a2e-e849-40a1-81b7-ed0fb574ddd8",
  "name": "yourdomain.com",
  "status": "pending",
  "records": [
    {"type": "MX", "name": "...", "value": "..."},
    {"type": "TXT", "name": "...", "value": "..."}
  ]
}
```

#### 获取域名信息

```bash
GET /resend/domains/{domain_id}
```

#### 更新域名信息

```bash
PATCH /resend/domains/{domain_id}
```

#### 删除域名

```bash
DELETE /resend/domains/{domain_id}
```

#### 验证域名

```bash
POST /resend/domains/{domain_id}/verify
```

### 联系人（Contacts）

管理联系人列表。

#### 列出联系人

```bash
GET /resend/contacts
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/resend/contacts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建联系人

```bash
POST /resend/contacts
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    'email': 'contact@example.com',
    'first_name': 'John',
    'last_name': 'Doe'
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/resend/contacts', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "id": "3cdc4bbb-0c79-46e5-be2a-48a89c29203d"
}
```

#### 获取联系人信息

```bash
GET /resend/contacts/{contact_id}
```

#### 更新联系人信息

```bash
PATCH /resend/contacts/{contact_id}
```

#### 删除联系人

```bash
DELETE /resend/contacts/{contact_id}
```

### 模板（Templates）

管理电子邮件模板。

#### 列出模板

```bash
GET /resend/templates
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/resend/templates')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建模板

```bash
POST /resend/templates
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    'name': 'Welcome Email',
    'subject': 'Welcome to our service!',
    'html': '<h1>Welcome!</h1><p>Thanks for signing up.</p>'
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/resend/templates', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "id": "9b84737c-8a80-448a-aca1-c6e1fddd0f23"
}
```

#### 获取模板信息

```bash
GET /resend/templates/{template_id}
```

#### 更新模板信息

```bash
PATCH /resend/templates/{template_id}
```

#### 删除模板

```bash
DELETE /resend/templates/{template_id}
```

#### 发布模板

```bash
POST /resend/templates/{template_id}/publish
```

#### 复制模板

```bash
POST /resend/templates/{template_id}/duplicate
```

### 分段（Segments）

创建用于定向发送的受众分段。

#### 列出分段

```bash
GET /resend/segments
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/resend/segments')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建分段

```bash
POST /resend/segments
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    'name': 'Active Users',
    'filter': {
        'and': [
            {'field': 'email', 'operator': 'contains', 'value': '@'}
        ]
    }
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/resend/segments', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取分段信息

```bash
GET /resend/segments/{segment_id}
```

#### 删除分段

```bash
DELETE /resend/segments/{segment_id}
```

### 广播消息（Broadcasts）

向指定分段发送电子邮件。

#### 列出广播消息

```bash
GET /resend/broadcasts
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/resend/broadcasts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建广播消息

```bash
POST /resend/broadcasts
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    'name': 'Weekly Newsletter',
    'from': 'newsletter@yourdomain.com',
    'subject': 'This Week\'s Update',
    'html': '<h1>Weekly Update</h1><p>Here\'s what happened...</p>',
    'segment_id': 'segment-uuid'
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/resend/broadcasts', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取广播消息信息

```bash
GET /resend/broadcasts/{broadcast_id}
```

#### 更新广播消息

```bash
PATCH /resend/broadcasts/{broadcast_id}
```

#### 删除广播消息

```bash
DELETE /resend/broadcasts/{broadcast_id}
```

#### 发送广播消息

```bash
POST /resend/broadcasts/{broadcast_id}/send
```

### Webhook

配置事件通知。

#### 列出Webhook

```bash
GET /resend/webhooks
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/resend/webhooks')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建Webhook

```bash
POST /resend/webhooks
```

**示例：**

**Webhook事件：**
- `email.sent` - 电子邮件已发送
- `email.delivered` - 电子邮件已送达
- `email.opened` - 电子邮件已被打开
- `email.clicked` - 电子邮件中的链接已被点击
- `email.bounced` - 电子邮件被退回
- `email.complained` - 收件人将邮件标记为垃圾邮件

#### 获取Webhook信息

```bash
GET /resend/webhooks/{webhook_id}
```

#### 更新Webhook配置

```bash
PATCH /resend/webhooks/{webhook_id}
```

#### 删除Webhook

```bash
DELETE /resend/webhooks/{webhook_id}
```

### API密钥（API Keys）

管理API密钥。

#### 列出API密钥

```bash
GET /resend/api-keys
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/resend/api-keys')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建API密钥

```bash
POST /resend/api-keys
```

**示例：**

**注意：** API密钥的值仅在创建时返回一次。

#### 删除API密钥

```bash
DELETE /resend/api-keys/{api_key_id}
```

### 主题（Topics）

管理订阅主题。

#### 列出主题

```bash
GET /resend/topics
```

#### 创建主题

```bash
POST /resend/topics
```

**示例：**

**注意：** 必须指定`default_subscription`字段，可选值为`subscribed`或`unsubscribed`。

#### 获取主题信息

```bash
GET /resend/topics/{topic_id}
```

#### 更新主题信息

```bash
PATCH /resend/topics/{topic_id}
```

#### 删除主题

```bash
DELETE /resend/topics/{topic_id}
```

### 联系人属性（Contact Properties）

管理联系人的自定义属性。

#### 列出联系人属性

```bash
GET /resend/contact-properties
```

#### 创建联系人属性

```bash
POST /resend/contact-properties
```

#### 获取联系人属性信息

```bash
GET /resend/contact-properties/{property_id}
```

#### 更新联系人属性信息

```bash
PATCH /resend/contact-properties/{property_id}
```

#### 删除联系人属性

```bash
DELETE /resend/contact-properties/{property_id}
```

## 代码示例

### JavaScript

```javascript
// Send an email
const response = await fetch('https://gateway.maton.ai/resend/emails', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    from: 'you@yourdomain.com',
    to: ['recipient@example.com'],
    subject: 'Hello!',
    html: '<p>Welcome!</p>'
  })
});
const data = await response.json();
console.log(data.id);
```

### Python

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/resend/emails',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'from': 'you@yourdomain.com',
        'to': ['recipient@example.com'],
        'subject': 'Hello!',
        'html': '<p>Welcome!</p>'
    }
)
email = response.json()
print(f"Email sent: {email['id']}")
```

## 注意事项：

- 发送电子邮件需要使用已验证的域名。
- 请求速率限制：每秒2次请求。
- 批量发送电子邮件时，每次请求最多可包含100封邮件。
- 预安排的电子邮件最多可提前7天设置发送时间。
- 附件支持Base64编码的内容或URL。
- `from`字段的地址必须来自已验证的域名。
- **重要提示：** 当将curl的输出传递给`jq`或其他命令时，在某些Shell环境中，环境变量`$MATON_API_KEY`可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 请求错误或未找到重发连接 |
| 401 | Maton API密钥无效或缺失 |
| 403 | 域名未验证或权限被拒绝 |
| 404 | 资源未找到 |
| 422 | 验证错误（缺少必填字段） |
| 429 | 请求速率限制（每秒2次） |
| 4xx/5xx | 来自重发API的传递错误 |

### 故障排除：API密钥问题

1. 确保`MATON_API_KEY`环境变量已设置：

```bash
echo $MATON_API_KEY
```

2. 通过列出所有连接来验证API密钥的有效性：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：域名未验证

要发送电子邮件，您必须先添加并验证域名：

1. 创建域名：`POST /resend/domains`
2. 添加响应中提供的DNS记录。
3. 验证域名：`POST /resend/domains/{id}/verify`

## 资源

- [重发API文档](https://resend.com/docs/api-reference/introduction)
- [重发控制面板](https://resend.com)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)