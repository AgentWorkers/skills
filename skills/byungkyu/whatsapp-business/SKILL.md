---
name: whatsapp-business
description: |
  WhatsApp Business API integration with managed OAuth. Send messages, manage templates, and handle conversations. Use this skill when users want to interact with WhatsApp Business. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# WhatsApp Business

您可以使用托管的 OAuth 认证来访问 WhatsApp Business API。通过该 API，您可以发送消息、管理消息模板、处理媒体文件，并通过 WhatsApp 与客户进行互动。

## 快速入门

```bash
# Send a text message
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'messaging_product': 'whatsapp', 'to': '1234567890', 'type': 'text', 'text': {'body': 'Hello from WhatsApp Business!'}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/whatsapp-business/v21.0/PHONE_NUMBER_ID/messages', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/whatsapp-business/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 WhatsApp Business API 端点路径。该网关会将请求代理到 `graph.facebook.com` 并自动插入您的 OAuth 令牌。

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
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 WhatsApp Business OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=whatsapp-business&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'whatsapp-business'}).encode()
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
    "app": "whatsapp-business",
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

如果您有多个 WhatsApp Business 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'messaging_product': 'whatsapp', 'to': '1234567890', 'type': 'text', 'text': {'body': 'Hello!'}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/whatsapp-business/v21.0/PHONE_NUMBER_ID/messages', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活跃连接。

## API 参考

### 消息

#### 发送文本消息

```bash
POST /whatsapp-business/v21.0/{phone_number_id}/messages
Content-Type: application/json

{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "1234567890",
  "type": "text",
  "text": {
    "preview_url": true,
    "body": "Hello! Check out https://example.com"
  }
}
```

#### 发送模板消息

```bash
POST /whatsapp-business/v21.0/{phone_number_id}/messages
Content-Type: application/json

{
  "messaging_product": "whatsapp",
  "to": "1234567890",
  "type": "template",
  "template": {
    "name": "hello_world",
    "language": {
      "code": "en_US"
    },
    "components": [
      {
        "type": "body",
        "parameters": [
          {"type": "text", "text": "John"}
        ]
      }
    ]
  }
}
```

#### 发送图片消息

```bash
POST /whatsapp-business/v21.0/{phone_number_id}/messages
Content-Type: application/json

{
  "messaging_product": "whatsapp",
  "to": "1234567890",
  "type": "image",
  "image": {
    "link": "https://example.com/image.jpg",
    "caption": "Check out this image!"
  }
}
```

#### 发送文档消息

```bash
POST /whatsapp-business/v21.0/{phone_number_id}/messages
Content-Type: application/json

{
  "messaging_product": "whatsapp",
  "to": "1234567890",
  "type": "document",
  "document": {
    "link": "https://example.com/document.pdf",
    "caption": "Here's the document",
    "filename": "report.pdf"
  }
}
```

#### 发送视频消息

```bash
POST /whatsapp-business/v21.0/{phone_number_id}/messages
Content-Type: application/json

{
  "messaging_product": "whatsapp",
  "to": "1234567890",
  "type": "video",
  "video": {
    "link": "https://example.com/video.mp4",
    "caption": "Watch this video"
  }
}
```

#### 发送音频消息

```bash
POST /whatsapp-business/v21.0/{phone_number_id}/messages
Content-Type: application/json

{
  "messaging_product": "whatsapp",
  "to": "1234567890",
  "type": "audio",
  "audio": {
    "link": "https://example.com/audio.mp3"
  }
}
```

#### 发送位置信息

```bash
POST /whatsapp-business/v21.0/{phone_number_id}/messages
Content-Type: application/json

{
  "messaging_product": "whatsapp",
  "to": "1234567890",
  "type": "location",
  "location": {
    "latitude": 37.7749,
    "longitude": -122.4194,
    "name": "San Francisco",
    "address": "San Francisco, CA, USA"
  }
}
```

#### 发送联系人信息

```bash
POST /whatsapp-business/v21.0/{phone_number_id}/messages
Content-Type: application/json

{
  "messaging_product": "whatsapp",
  "to": "1234567890",
  "type": "contacts",
  "contacts": [
    {
      "name": {
        "formatted_name": "John Doe",
        "first_name": "John",
        "last_name": "Doe"
      },
      "phones": [
        {"phone": "+1234567890", "type": "MOBILE"}
      ]
    }
  ]
}
```

#### 发送交互式按钮消息

```bash
POST /whatsapp-business/v21.0/{phone_number_id}/messages
Content-Type: application/json

{
  "messaging_product": "whatsapp",
  "to": "1234567890",
  "type": "interactive",
  "interactive": {
    "type": "button",
    "body": {
      "text": "Would you like to proceed?"
    },
    "action": {
      "buttons": [
        {"type": "reply", "reply": {"id": "yes", "title": "Yes"}},
        {"type": "reply", "reply": {"id": "no", "title": "No"}}
      ]
    }
  }
}
```

#### 发送交互式列表消息

```bash
POST /whatsapp-business/v21.0/{phone_number_id}/messages
Content-Type: application/json

{
  "messaging_product": "whatsapp",
  "to": "1234567890",
  "type": "interactive",
  "interactive": {
    "type": "list",
    "header": {"type": "text", "text": "Select an option"},
    "body": {"text": "Choose from the list below"},
    "action": {
      "button": "View Options",
      "sections": [
        {
          "title": "Products",
          "rows": [
            {"id": "prod1", "title": "Product 1", "description": "First product"},
            {"id": "prod2", "title": "Product 2", "description": "Second product"}
          ]
        }
      ]
    }
  }
}
```

#### 将消息标记为已读

```bash
POST /whatsapp-business/v21.0/{phone_number_id}/messages
Content-Type: application/json

{
  "messaging_product": "whatsapp",
  "status": "read",
  "message_id": "wamid.xxxxx"
}
```

### 媒体文件

#### 上传媒体文件

```bash
POST /whatsapp-business/v21.0/{phone_number_id}/media
Content-Type: multipart/form-data

file=@/path/to/file.jpg
type=image/jpeg
messaging_product=whatsapp
```

#### 获取媒体文件的 URL

```bash
GET /whatsapp-business/v21.0/{media_id}
```

#### 删除媒体文件

```bash
DELETE /whatsapp-business/v21.0/{media_id}
```

### 消息模板

#### 列出所有模板

```bash
GET /whatsapp-business/v21.0/{whatsapp_business_account_id}/message_templates
```

查询参数：
- `limit` - 返回的模板数量
- `status` - 按状态过滤：`APPROVED`、`PENDING`、`REJECTED`

#### 创建模板

```bash
POST /whatsapp-business/v21.0/{whatsapp_business_account_id}/message_templates
Content-Type: application/json

{
  "name": "order_confirmation",
  "language": "en_US",
  "category": "UTILITY",
  "components": [
    {
      "type": "HEADER",
      "format": "TEXT",
      "text": "Order Confirmation"
    },
    {
      "type": "BODY",
      "text": "Hi {{1}}, your order #{{2}} has been confirmed!"
    },
    {
      "type": "FOOTER",
      "text": "Thank you for your purchase"
    }
  ]
}
```

模板类别：`AUTHENTICATION`、`MARKETING`、`UTILITY`

#### 删除模板

```bash
DELETE /whatsapp-business/v21.0/{whatsapp_business_account_id}/message_templates?name=template_name
```

### 手机号码

#### 获取电话号码

```bash
GET /whatsapp-business/v21.0/{phone_number_id}
```

#### 列出所有电话号码

```bash
GET /whatsapp-business/v21.0/{whatsapp_business_account_id}/phone_numbers
```

### 商业资料

#### 获取商业资料信息

```bash
GET /whatsapp-business/v21.0/{phone_number_id}/whatsapp_business_profile?fields=about,address,description,email,profile_picture_url,websites,vertical
```

#### 更新商业资料信息

```bash
POST /whatsapp-business/v21.0/{phone_number_id}/whatsapp_business_profile
Content-Type: application/json

{
  "messaging_product": "whatsapp",
  "about": "Your trusted partner",
  "address": "123 Business St",
  "description": "We provide excellent services",
  "email": "contact@example.com",
  "websites": ["https://example.com"],
  "vertical": "RETAIL"
}
```

## 代码示例

### JavaScript

```javascript
const headers = {
  'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
  'Content-Type': 'application/json'
};

// Send text message
await fetch(
  'https://gateway.maton.ai/whatsapp-business/v21.0/PHONE_NUMBER_ID/messages',
  {
    method: 'POST',
    headers,
    body: JSON.stringify({
      messaging_product: 'whatsapp',
      to: '1234567890',
      type: 'text',
      text: { body: 'Hello from WhatsApp!' }
    })
  }
);

// Send template message
await fetch(
  'https://gateway.maton.ai/whatsapp-business/v21.0/PHONE_NUMBER_ID/messages',
  {
    method: 'POST',
    headers,
    body: JSON.stringify({
      messaging_product: 'whatsapp',
      to: '1234567890',
      type: 'template',
      template: {
        name: 'hello_world',
        language: { code: 'en_US' }
      }
    })
  }
);
```

### Python

```python
import os
import requests

headers = {
    'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
    'Content-Type': 'application/json'
}

# Send text message
response = requests.post(
    'https://gateway.maton.ai/whatsapp-business/v21.0/PHONE_NUMBER_ID/messages',
    headers=headers,
    json={
        'messaging_product': 'whatsapp',
        'to': '1234567890',
        'type': 'text',
        'text': {'body': 'Hello from WhatsApp!'}
    }
)

# Send template message
response = requests.post(
    'https://gateway.maton.ai/whatsapp-business/v21.0/PHONE_NUMBER_ID/messages',
    headers=headers,
    json={
        'messaging_product': 'whatsapp',
        'to': '1234567890',
        'type': 'template',
        'template': {
            'name': 'hello_world',
            'language': {'code': 'en_US'}
        }
    }
)
```

## 注意事项：

- 电话号码必须采用国际格式，且不能包含 `+` 或前导零（例如：`1234567890`）。
- `messaging_product` 必须始终设置为 `whatsapp`。
- 发送消息时需要使用模板消息（24 小时消息发送窗口）。
- 媒体文件必须是公开可访问的 URL，或者通过 Media API 上传。
- 交互式消息最多支持 3 个按钮或 10 个列表项。
- 消息 ID（`wamid`）用于跟踪消息状态和回复。
- 当前使用的 API 版本为 `v21.0`；请查看 Meta 文档以获取最新版本信息。
- 重要提示：当使用 `curl` 命令时，如果 URL 中包含方括号（如 `fields[]`、`sort[]`、`records[]`），请使用 `curl -g` 以禁用全局解析。
- 重要提示：当将 `curl` 的输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 可能无法正确展开，这可能导致 “Invalid API key” 错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 WhatsApp Business 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 电话号码或资源未找到 |
| 429 | 每个账户的请求速率限制达到（每秒 10 次请求） |
| 4xx/5xx | 来自 WhatsApp Business API 的传递错误 |

常见的 WhatsApp 错误代码：
- `131030` - 电话号码未注册
- `131031` - 消息发送失败
- `132000` - 模板未找到或未获批准
- `133010` - 电话号码的请求速率限制已达到

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

1. 确保您的 URL 路径以 `whatsapp-business` 开头。例如：
- 正确格式：`https://gateway.maton.ai/whatsapp-business/v21.0/PHONE_NUMBER_ID/messages`
- 错误格式：`https://gateway.maton.ai/v21.0/PHONE_NUMBER_ID/messages`

## 资源

- [WhatsApp Business API 概述](https://developers.facebook.com/docs/whatsapp/cloud-api/overview)
- [发送消息](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages)
- [消息模板](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates)
- [媒体文件](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media)
- [电话号码](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/phone-numbers)
- [商业资料](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/business-profiles)
- [Webhook](https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks)
- [错误代码](https://developers.facebook.com/docs/whatsapp/cloud-api/support/error-codes)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)