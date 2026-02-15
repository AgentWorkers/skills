---
name: clicksend
description: |
  ClickSend API integration with managed authentication. Send SMS, MMS, and voice messages, manage contacts and lists.
  Use this skill when users want to send text messages, make voice calls, manage contact lists, or track message delivery.
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

# ClickSend

通过管理认证方式访问 ClickSend API。支持发送 SMS、MMS 和语音消息，管理联系人及联系人列表，并追踪消息的送达情况。

## 快速入门

```bash
# Get account info
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/clicksend/v3/account')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/clicksend/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 ClickSend API 端点路径。该网关会将请求代理到 `rest.clicksend.com` 并自动插入您的认证信息。

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

1. 在 [maton.ai](https://maton.ai) 注册或登录账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的 ClickSend 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=clicksend&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'clicksend'}).encode()
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

**响应格式：**
```json
{
  "connection": {
    "connection_id": "37beee67-29f7-43b6-b0b2-5f0f7a5d6440",
    "status": "ACTIVE",
    "creation_time": "2026-02-10T10:04:12.418030Z",
    "last_updated_time": "2026-02-10T10:06:17.059090Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "clicksend",
    "metadata": {}
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

如果您有多个 ClickSend 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/clicksend/v3/account')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '37beee67-29f7-43b6-b0b2-5f0f7a5d6440')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果未指定，网关将使用默认的（最旧的）活动连接。

## API 参考

### 响应格式

所有 ClickSend API 的响应都遵循以下格式：

```json
{
  "http_code": 200,
  "response_code": "SUCCESS",
  "response_msg": "Description of the result",
  "data": { ... }
}
```

---

## 账户

### 获取账户信息

```bash
GET /clicksend/v3/account
```

**响应格式：**
```json
{
  "http_code": 200,
  "response_code": "SUCCESS",
  "response_msg": "Here's your account",
  "data": {
    "user_id": 672721,
    "username": "user@example.com",
    "user_email": "user@example.com",
    "balance": "2.005718",
    "user_phone": "+18019234886",
    "user_first_name": "John",
    "user_last_name": "Doe",
    "country": "US",
    "default_country_sms": "US",
    "timezone": "America/Chicago",
    "_currency": {
      "currency_name_short": "USD",
      "currency_prefix_d": "$"
    }
  }
}
```

---

## SMS

### 发送 SMS

```bash
POST /clicksend/v3/sms/send
Content-Type: application/json

{
  "messages": [
    {
      "to": "+15551234567",
      "body": "Hello from ClickSend!",
      "source": "api"
    }
  ]
}
```

**参数：**

| 参数 | 类型 | 说明 |
|-------|------|-------------|
| `to` | string | 收件人电话号码（E.164 格式） |
| `body` | string | SMS 消息内容 |
| `source` | string | 来源标识符（例如：“api”、“sdk”） |
| `from` | string | 发件人 ID（可选） |
| `schedule` | int | 预定发送的 Unix 时间戳（可选） |
| `custom_string` | string | 自定义参考信息（可选） |

### 获取 SMS 发送价格

```bash
POST /clicksend/v3/sms/price
Content-Type: application/json

{
  "messages": [
    {
      "to": "+15551234567",
      "body": "Test message",
      "source": "api"
    }
  ]
}
```

### SMS 历史记录

```bash
GET /clicksend/v3/sms/history
```

**查询参数：**

| 参数 | 说明 |
|-----------|-------------|
| `date_from` | 开始日期的 Unix 时间戳 |
| `date_to` | 结束日期的 Unix 时间戳 |
| `page` | 页码（默认：1） |
| `limit` | 每页显示的结果数量（默认：15） |

### 收到的 SMS

```bash
GET /clicksend/v3/sms/inbound
```

### SMS 收件报告

```bash
GET /clicksend/v3/sms/receipts
```

### 取消预定的 SMS

```bash
PUT /clicksend/v3/sms/{message_id}/cancel
```

### 取消所有预定的 SMS

```bash
PUT /clicksend/v3/sms/cancel-all
```

---

## SMS 模板

### 列出模板

```bash
GET /clicksend/v3/sms/templates
```

**响应格式：**
```json
{
  "http_code": 200,
  "response_code": "SUCCESS",
  "response_msg": "Here are your templates.",
  "data": {
    "total": 1,
    "per_page": 15,
    "current_page": 1,
    "data": [
      {
        "template_id": 632497,
        "body": "Hello {name}, this is a test message.",
        "template_name": "Test Template"
      }
    ]
  }
}
```

### 创建模板

```bash
POST /clicksend/v3/sms/templates
Content-Type: application/json

{
  "template_name": "Welcome Message",
  "body": "Hello {name}, welcome to our service!"
}
```

### 更新模板

```bash
PUT /clicksend/v3/sms/templates/{template_id}
Content-Type: application/json

{
  "template_name": "Updated Template",
  "body": "Updated message content"
}
```

### 删除模板

```bash
DELETE /clicksend/v3/sms/templates/{template_id}
```

---

## MMS

### 发送 MMS

```bash
POST /clicksend/v3/mms/send
Content-Type: application/json

{
  "messages": [
    {
      "to": "+15551234567",
      "body": "Check out this image!",
      "media_file": "https://example.com/image.jpg",
      "source": "api"
    }
  ]
}
```

### MMS 历史记录

```bash
GET /clicksend/v3/mms/history
```

### 获取 MMS 发送价格

```bash
POST /clicksend/v3/mms/price
Content-Type: application/json

{
  "messages": [...]
}
```

### MMS 收件报告

```bash
GET /clicksend/v3/mms/receipts
```

---

## 语音

### 发送语音消息

```bash
POST /clicksend/v3/voice/send
Content-Type: application/json

{
  "messages": [
    {
      "to": "+15551234567",
      "body": "Hello, this is a voice message.",
      "voice": "female",
      "lang": "en-us",
      "source": "api"
    }
  ]
}
```

**语音参数：**

| 参数 | 说明 |
|-------|-------------|
| `to` | 收件人电话号码 |
| `body` | 要朗读的文本 |
| `voice` | 语音性别：`male` 或 `female` |
| `lang` | 语言代码（例如：`en-us`、`en-gb`、`de-de` |
| `schedule` | 预定通话的 Unix 时间戳 |
| `require_input` | 是否需要按键输入（0-1） |
| `machine_detection` | 是否检测答录机（0-1） |

### 支持的语言

```bash
GET /clicksend/v3/voice/lang
```

返回支持的语言列表及其代码。

### 语音历史记录

```bash
GET /clicksend/v3/voice/history
```

**注意：** 需要在账户中启用语音功能。

### 获取语音服务价格

```bash
POST /clicksend/v3/voice/price
```

### 取消语音消息

```bash
PUT /clicksend/v3/voice/{message_id}/cancel
```

---

## 联系人列表

### 列出所有联系人列表

```bash
GET /clicksend/v3/lists
```

**响应格式：**
```json
{
  "http_code": 200,
  "response_code": "SUCCESS",
  "response_msg": "Here are your contact lists.",
  "data": {
    "total": 2,
    "data": [
      {
        "list_id": 3555277,
        "list_name": "Opt-Out List",
        "_contacts_count": 0
      },
      {
        "list_id": 3555278,
        "list_name": "Example List",
        "_contacts_count": 10
      }
    ]
  }
}
```

### 获取联系人列表

```bash
GET /clicksend/v3/lists/{list_id}
```

### 创建联系人列表

```bash
POST /clicksend/v3/lists
Content-Type: application/json

{
  "list_name": "My New List"
}
```

### 更新联系人列表

```bash
PUT /clicksend/v3/lists/{list_id}
Content-Type: application/json

{
  "list_name": "Updated List Name"
}
```

### 删除联系人列表

```bash
DELETE /clicksend/v3/lists/{list_id}
```

### 删除重复联系人

```bash
PUT /clicksend/v3/lists/{list_id}/remove-duplicates
```

---

## 联系人

### 在列表中列出联系人

```bash
GET /clicksend/v3/lists/{list_id}/contacts
```

**查询参数：**

| 参数 | 说明 |
|-----------|-------------|
| `page` | 页码 |
| `limit` | 每页显示的结果数量 |
| `updated_after` | 过滤在指定时间之后更新的联系人 |

### 获取联系人信息

```bash
GET /clicksend/v3/lists/{list_id}/contacts/{contact_id}
```

**响应格式：**
```json
{
  "http_code": 200,
  "response_code": "SUCCESS",
  "data": {
    "contact_id": 1581565666,
    "list_id": 3555278,
    "phone_number": "+18019234886",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "custom_1": "",
    "custom_2": "",
    "custom_3": "",
    "custom_4": "",
    "organization_name": "",
    "address_city": "",
    "address_state": "",
    "address_country": "US"
  }
}
```

### 创建联系人

```bash
POST /clicksend/v3/lists/{list_id}/contacts
Content-Type: application/json

{
  "phone_number": "+15551234567",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com"
}
```

**联系人字段：**

| 参数 | 说明 |
|-------|-------------|
| `phone_number` | 电话号码（E.164 格式） |
| `first_name` | 名 |
| `last_name` | 姓 |
| `email` | 电子邮件地址 |
| `fax_number` | 传真号码 |
| `organization_name` | 公司名称 |
| `custom_1` - `custom_4` | 自定义字段 |
| `address_line_1`, `address_line_2` | 地址 |
| `address_city`, `address_state`, `address_postal_code`, `address_country` | 地址信息 |

### 更新联系人信息

```bash
PUT /clicksend/v3/lists/{list_id}/contacts/{contact_id}
Content-Type: application/json

{
  "first_name": "Jane",
  "last_name": "Smith"
}
```

### 删除联系人

```bash
DELETE /clicksend/v3/lists/{list_id}/contacts/{contact_id}
```

### 将联系人复制到另一个列表

```bash
PUT /clicksend/v3/lists/{from_list_id}/contacts/{contact_id}/copy/{to_list_id}
```

### 将联系人转移到另一个列表

```bash
PUT /clicksend/v3/lists/{from_list_id}/contacts/{contact_id}/transfer/{to_list_id}
```

---

## 电子邮件地址

### 列出已验证的电子邮件地址

```bash
GET /clicksend/v3/email/addresses
```

### 添加电子邮件地址

```bash
POST /clicksend/v3/email/addresses
Content-Type: application/json

{
  "email_address": "sender@example.com"
}
```

### 删除电子邮件地址

```bash
DELETE /clicksend/v3/email/addresses/{email_address_id}
```

---

## 实用端点

### 列出所有国家

```bash
GET /clicksend/v3/countries
```

返回所有支持国家的列表及其代码。

---

## 分页

ClickSend 使用基于页码的分页机制：

```bash
GET /clicksend/v3/lists?page=2&limit=50
```

**响应包含：**
```json
{
  "data": {
    "total": 100,
    "per_page": 50,
    "current_page": 2,
    "last_page": 2,
    "next_page_url": null,
    "prev_page_url": "...?page=1",
    "from": 51,
    "to": 100,
    "data": [...]
  }
}
```

**参数：**
- `page` - 页码（默认：1）
- `limit` - 每页显示的结果数量（默认：15）

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/clicksend/v3/sms/send',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      messages: [
        {
          to: '+15551234567',
          body: 'Hello from ClickSend!',
          source: 'api'
        }
      ]
    })
  }
);
const data = await response.json();
console.log(data);
```

### Python

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/clicksend/v3/sms/send',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'messages': [
            {
                'to': '+15551234567',
                'body': 'Hello from ClickSend!',
                'source': 'api'
            }
        ]
    }
)
data = response.json()
print(f"Status: {data['response_code']}")
```

## 注意事项：

- 电话号码必须使用 E.164 格式（例如：`+15551234567`）。
- 所有时间戳均为 Unix 时间戳（自纪元以来的秒数）。
- 使用 `source` 字段在分析中标识您的应用程序。
- 模板支持 `{name}`、`{custom_1}` 等占位符。
- 超过 160 个字符的 SMS 消息会被分割成多个部分发送。
- 使用语音服务需要账户级别的权限。
- 重要提示：当 URL 中包含括号时，使用 `curl -g` 命令来禁用全局解析。
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，环境变量（如 `$MATON_API_KEY`）在某些 shell 环境中可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 200 | 操作成功 |
| 400 | 请求错误 |
| 401 | 未经授权 - 凭据无效 |
| 403 | 禁止访问 - 权限不足 |
| 404 | 资源未找到 |
| 429 | 请求次数限制 |
| 500 | 服务器内部错误 |

**响应代码：**
- `SUCCESS`：操作成功完成 |
- `FORBIDDEN`：访问资源被拒绝 |
- `BAD_REQUEST`：请求参数无效 |
- `INVALID_RECIPIENT`：电话号码无效 |

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

1. 确保您的 URL 路径以 `clicksend` 开头。例如：
- 正确：`https://gateway.maton.ai/clicksend/v3/account`
- 错误：`https://gateway.maton.ai/v3/account`

## 资源

- [ClickSend 开发者门户](https://developers.clicksend.com/)
- [ClickSend REST API v3 文档](https://developers.clicksend.com/docs)
- [ClickSend PHP SDK](https://github.com/ClickSend/clicksend-php)
- [ClickSend 帮助中心](https://help.clicksend.com/)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持团队](mailto:support@maton.ai)