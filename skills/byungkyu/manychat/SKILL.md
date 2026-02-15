---
name: manychat
description: |
  ManyChat API integration with managed authentication. Manage subscribers, tags, custom fields, and send messages through Facebook Messenger.
  Use this skill when users want to manage ManyChat subscribers, send messages, add/remove tags, or work with custom fields and bot automation.
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

# ManyChat

通过托管的认证方式访问ManyChat API。您可以管理订阅者、标签、自定义字段、自动化流程，并通过聊天自动化功能发送消息。

## 快速入门

```bash
# Get page info
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/manychat/fb/page/getInfo')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/manychat/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的ManyChat API端点路径。该网关会将请求代理到 `api.manychat.com` 并自动插入您的API密钥。

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

1. 在 [maton.ai](https://maton.ai) 登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的ManyChat连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=manychat&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'manychat'}).encode()
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
    "app": "manychat",
    "metadata": {}
  }
}
```

通过提供您的ManyChat API密钥来完成连接设置。

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

如果您有多个ManyChat连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/manychat/fb/page/getInfo')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API参考

### 页面操作

#### 获取页面信息

```bash
GET /manychat/fb/page/getInfo
```

请求速率限制：每秒100次

**响应：**
```json
{
  "status": "success",
  "data": {
    "id": 123456789,
    "name": "Page Name",
    "category": "Business",
    "avatar_link": "https://...",
    "username": "pagename",
    "about": "About text",
    "description": "Page description",
    "is_pro": true,
    "timezone": "America/New_York"
  }
}
```

### 标签操作

#### 列出标签

```bash
GET /manychat/fb/page/getTags
```

请求速率限制：每秒100次

**响应：**
```json
{
  "status": "success",
  "data": [
    {"id": 1, "name": "VIP"},
    {"id": 2, "name": "Customer"}
  ]
}
```

#### 创建标签

```bash
POST /manychat/fb/page/createTag
Content-Type: application/json

{
  "name": "New Tag"
}
```

请求速率限制：每秒10次

#### 从页面中删除标签

```bash
POST /manychat/fb/page/removeTag
Content-Type: application/json

{
  "tag_id": 123
}
```

请求速率限制：每秒10次。该操作会从页面和所有订阅者中删除标签。

#### 按名称删除标签

```bash
POST /manychat/fb/page/removeTagByName
Content-Type: application/json

{
  "tag_name": "Old Tag"
}
```

请求速率限制：每秒10次

### 自定义字段操作

#### 列出自定义字段

```bash
GET /manychat/fb/page/getCustomFields
```

请求速率限制：每秒100次

**响应：**
```json
{
  "status": "success",
  "data": [
    {"id": 1, "name": "phone_number", "type": "text"},
    {"id": 2, "name": "purchase_count", "type": "number"}
  ]
}
```

#### 创建自定义字段

```bash
POST /manychat/fb/page/createCustomField
Content-Type: application/json

{
  "caption": "Phone Number",
  "type": "text",
  "description": "Customer phone number"
}
```

请求速率限制：每秒10次

**字段类型：** `text`、`number`、`date`、`datetime`、`boolean`

### 机器人字段操作

#### 列出机器人字段

```bash
GET /manychat/fb/page/getBotFields
```

请求速率限制：每秒100次

#### 创建机器人字段

```bash
POST /manychat/fb/page/createBotField
Content-Type: application/json

{
  "name": "counter",
  "type": "number",
  "description": "Global counter",
  "value": 0
}
```

请求速率限制：每秒10次

#### 设置机器人字段

```bash
POST /manychat/fb/page/setBotField
Content-Type: application/json

{
  "field_id": 123,
  "field_value": 42
}
```

请求速率限制：每秒10次

#### 按名称设置机器人字段

```bash
POST /manychat/fb/page/setBotFieldByName
Content-Type: application/json

{
  "field_name": "counter",
  "field_value": 42
}
```

请求速率限制：每秒10次

#### 设置多个机器人字段

```bash
POST /manychat/fb/page/setBotFields
Content-Type: application/json

{
  "fields": [
    {"field_id": 123, "field_value": "value1"},
    {"field_name": "field2", "field_value": "value2"}
  ]
}
```

请求速率限制：每秒10次。每次请求最多设置20个字段。

### 流程操作

#### 列出流程

```bash
GET /manychat/fb/page/getFlows
```

请求速率限制：每秒100次

**响应：**
```json
{
  "status": "success",
  "data": {
    "flows": [
      {"ns": "content123456", "name": "Welcome Flow", "folder_id": 1}
    ],
    "folders": [
      {"id": 1, "name": "Main Folder"}
    ]
  }
}
```

### 成长工具

#### 列出成长工具

```bash
GET /manychat/fb/page/getGrowthTools
```

请求速率限制：每秒100次

### OTN主题

#### 列出OTN主题

```bash
GET /manychat/fb/page/getOtnTopics
```

请求速率限制：每秒100次

### 订阅者操作

#### 获取订阅者信息

```bash
GET /manychat/fb/subscriber/getInfo?subscriber_id=123456789
```

请求速率限制：每秒10次

**响应：**
```json
{
  "status": "success",
  "data": {
    "id": 123456789,
    "name": "John Doe",
    "first_name": "John",
    "last_name": "Doe",
    "gender": "male",
    "profile_pic": "https://...",
    "subscribed": "2025-01-15T10:30:00Z",
    "last_interaction": "2025-02-01T14:20:00Z",
    "tags": [{"id": 1, "name": "VIP"}],
    "custom_fields": [{"id": 1, "name": "phone", "value": "+1234567890"}]
  }
}
```

#### 按名称查找订阅者

```bash
GET /manychat/fb/subscriber/findByName?name=John%20Doe
```

请求速率限制：每秒10次。最多返回100个结果。

#### 按自定义字段查找订阅者

```bash
GET /manychat/fb/subscriber/findByCustomField?field_id=123&field_value=value
```

请求速率限制：每秒10次。支持使用 `text` 和 `number` 字段。最多返回100个结果。

#### 按系统字段查找订阅者

```bash
GET /manychat/fb/subscriber/findBySystemField?email=john@example.com
```

```bash
GET /manychat/fb/subscriber/findBySystemField?phone=+1234567890
```

请求速率限制：每秒50次。需要设置 `email` 或 `phone` 参数。

#### 根据用户引用查找订阅者

```bash
GET /manychat/fb/subscriber/getInfoByUserRef?user_ref=123456
```

#### 创建订阅者

```bash
POST /manychat/fb/subscriber/createSubscriber
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "email": "john@example.com",
  "gender": "male",
  "has_opt_in_sms": true,
  "has_opt_in_email": true,
  "consent_phrase": "I agree to receive messages"
}
```

请求速率限制：每秒10次

**注意：** 使用电话或电子邮件导入订阅者需要ManyChat的特别权限。请联系ManyChat支持以为您的账户启用此功能。

#### 更新订阅者信息

```bash
POST /manychat/fb/subscriber/updateSubscriber
Content-Type: application/json

{
  "subscriber_id": 123456789,
  "first_name": "John",
  "last_name": "Smith",
  "phone": "+1234567890",
  "email": "john.smith@example.com"
}
```

请求速率限制：每秒10次

#### 为订阅者添加标签

```bash
POST /manychat/fb/subscriber/addTag
Content-Type: application/json

{
  "subscriber_id": 123456789,
  "tag_id": 1
}
```

请求速率限制：每秒10次

#### 按名称添加标签

```bash
POST /manychat/fb/subscriber/addTagByName
Content-Type: application/json

{
  "subscriber_id": 123456789,
  "tag_name": "VIP"
}
```

请求速率限制：每秒10次

#### 从订阅者中删除标签

```bash
POST /manychat/fb/subscriber/removeTag
Content-Type: application/json

{
  "subscriber_id": 123456789,
  "tag_id": 1
}
```

请求速率限制：每秒10次

#### 按名称删除标签

```bash
POST /manychat/fb/subscriber/removeTagByName
Content-Type: application/json

{
  "subscriber_id": 123456789,
  "tag_name": "VIP"
}
```

请求速率限制：每秒10次

#### 设置自定义字段

```bash
POST /manychat/fb/subscriber/setCustomField
Content-Type: application/json

{
  "subscriber_id": 123456789,
  "field_id": 1,
  "field_value": "+1234567890"
}
```

请求速率限制：每秒10次

#### 按名称设置自定义字段

```bash
POST /manychat/fb/subscriber/setCustomFieldByName
Content-Type: application/json

{
  "subscriber_id": 123456789,
  "field_name": "phone_number",
  "field_value": "+1234567890"
}
```

请求速率限制：每秒10次

#### 设置多个自定义字段

```bash
POST /manychat/fb/subscriber/setCustomFields
Content-Type: application/json

{
  "subscriber_id": 123456789,
  "fields": [
    {"field_id": 1, "field_value": "value1"},
    {"field_name": "field2", "field_value": "value2"}
  ]
}
```

请求速率限制：每秒10次。每次请求最多设置20个字段。

#### 通过签名请求验证订阅者

```bash
POST /manychat/fb/subscriber/verifyBySignedRequest
Content-Type: application/json

{
  "subscriber_id": 123456789,
  "signed_request": "signed_request_token"
}
```

请求速率限制：每秒10次

### 发送操作

#### 发送内容

```bash
POST /manychat/fb/sending/sendContent
Content-Type: application/json

{
  "subscriber_id": 123456789,
  "data": {
    "version": "v2",
    "content": {
      "messages": [
        {
          "type": "text",
          "text": "Hello! How can I help you today?"
        }
      ]
    }
  },
  "message_tag": "CONFIRMED_EVENT_UPDATE"
}
```

请求速率限制：每秒25次

**消息标签：** 在24小时消息发送窗口之外发送消息时需要使用以下标签：
- `CONFIRMED_EVENT_UPDATE`
- `POST_PURCHASE_UPDATE`
- `ACCOUNT_UPDATE`

**OTN（一次性通知）：**
```json
{
  "subscriber_id": 123456789,
  "data": {...},
  "otn_topic_name": "Price Drop Alert"
}
```

#### 根据用户引用发送内容

```bash
POST /manychat/fb/sending/sendContentByUserRef
Content-Type: application/json

{
  "user_ref": 123456,
  "data": {
    "version": "v2",
    "content": {
      "messages": [
        {
          "type": "text",
          "text": "Welcome!"
        }
      ]
    }
  }
}
```

请求速率限制：每秒25次

#### 发送流程

```bash
POST /manychat/fb/sending/sendFlow
Content-Type: application/json

{
  "subscriber_id": 123456789,
  "flow_ns": "content123456"
}
```

请求速率限制：每秒20次，每小时每个订阅者最多发送100条消息

## 消息内容格式

ManyChat使用结构化内容格式来发送消息：

### 文本消息

```json
{
  "version": "v2",
  "content": {
    "messages": [
      {
        "type": "text",
        "text": "Your message here"
      }
    ]
  }
}
```

### 图片消息

```json
{
  "version": "v2",
  "content": {
    "messages": [
      {
        "type": "image",
        "url": "https://example.com/image.jpg"
      }
    ]
  }
}
```

### 快速回复

```json
{
  "version": "v2",
  "content": {
    "messages": [
      {
        "type": "text",
        "text": "Choose an option:",
        "quick_replies": [
          {"type": "node", "caption": "Option 1", "target": "content123"},
          {"type": "node", "caption": "Option 2", "target": "content456"}
        ]
      }
    ]
  }
}
```

### 按钮

```json
{
  "version": "v2",
  "content": {
    "messages": [
      {
        "type": "text",
        "text": "Click a button:",
        "buttons": [
          {"type": "url", "caption": "Visit Website", "url": "https://example.com"},
          {"type": "flow", "caption": "Start Flow", "target": "content123"}
        ]
      }
    ]
  }
}
```

## 代码示例

### JavaScript

```javascript
// Get page info
const response = await fetch(
  'https://gateway.maton.ai/manychat/fb/page/getInfo',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();

// Send a message
const sendResponse = await fetch(
  'https://gateway.maton.ai/manychat/fb/sending/sendContent',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      subscriber_id: 123456789,
      data: {
        version: 'v2',
        content: {
          messages: [{ type: 'text', text: 'Hello!' }]
        }
      }
    })
  }
);
```

### Python

```python
import os
import requests

# Get page info
response = requests.get(
    'https://gateway.maton.ai/manychat/fb/page/getInfo',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()

# Send a message
send_response = requests.post(
    'https://gateway.maton.ai/manychat/fb/sending/sendContent',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={
        'subscriber_id': 123456789,
        'data': {
            'version': 'v2',
            'content': {
                'messages': [{'type': 'text', 'text': 'Hello!'}]
            }
        }
    }
)
```

## 注意事项

- 订阅者ID在您的ManyChat页面中是唯一的。
- 流程命名空间（`flow_ns`）用于标识特定的自动化流程。
- 在24小时消息发送窗口之外发送消息时，必须使用 `message_tag` 参数。
- OTN（一次性通知）允许每个主题订阅者发送一条消息。
- 大多数POST端点在成功时会返回 `{"status": "success"}`。
- **重要提示：** 当使用 `curl` 命令时，如果URL包含括号，请使用 `curl -g` 以禁用全局解析。
- **重要提示：** 当将 `curl` 的输出传递给 `jq` 或其他命令时，在某些shell环境中，环境变量（如 `$MATON_API_KEY`）可能无法正确展开。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 未找到ManyChat连接 |
| 401 | Maton API密钥无效或缺失 |
| 429 | 请求速率受限 |
| 4xx/5xx | 来自ManyChat API的传递错误 |

### ManyChat错误代码

| 代码 | 含义 |
|------|---------|
| 2011 | 未找到订阅者 |
| 2012 | 未找到用户引用 |
| 3011 | 消息内容无效 |
| 3021 | 需要`message_tag` |
| 3031 | 未找到OTN主题 |

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

### 故障排除：应用名称无效

1. 确保您的URL路径以 `manychat` 开头。例如：
- 正确：`https://gateway.maton.ai/manychat/fb/page/getInfo`
- 错误：`https://gateway.maton.ai/fb/page/getInfo`

## 资源

- [ManyChat API文档](https://api.manychat.comswagger)
- [ManyChat API密钥生成指南](https://help.manychat.com/hc/en-us/articles/14959510331420)
- [ManyChat开发者计划](https://help.manychat.com/hc/en-us/articles/14281269835548)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)