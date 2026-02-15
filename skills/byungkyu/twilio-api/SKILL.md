---
name: twilio
description: |
  Twilio API integration with managed OAuth. SMS, voice calls, phone numbers, and communications.
  Use this skill when users want to send SMS messages, make voice calls, manage phone numbers, or work with Twilio resources.
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

# Twilio

使用托管的OAuth认证来访问Twilio API。您可以发送短信、发起语音通话、管理电话号码以及操作Twilio的各种资源。

## 快速入门

```bash
# List all accounts
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/twilio/2010-04-01/Accounts.json')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/twilio/2010-04-01/Accounts/{AccountSid}/{resource}.json
```

网关会将请求代理到`api.twilio.com`，并自动插入您的OAuth令牌。

**重要提示：** 大多数Twilio端点需要在路径中包含您的账户SID。您可以从 `/Accounts.json` 端点获取账户SID。

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

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的Twilio OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=twilio&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'twilio'}).encode()
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
    "connection_id": "ebe566b1-3eaf-4926-bc92-0d8d47445f12",
    "status": "ACTIVE",
    "creation_time": "2026-02-09T23:18:44.243582Z",
    "last_updated_time": "2026-02-09T23:19:55.176687Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "twilio",
    "metadata": {}
  }
}
```

在浏览器中打开返回的`url`以完成OAuth认证。

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

如果您有多个Twilio连接，请使用`Maton-Connection`头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/twilio/2010-04-01/Accounts.json')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'ebe566b1-3eaf-4926-bc92-0d8d47445f12')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活跃连接。

## API参考

### 账户

#### 列出账户

```bash
GET /twilio/2010-04-01/Accounts.json
```

**响应：**
```json
{
  "accounts": [
    {
      "sid": "ACf5d980cd4b3f7604a464afaec191fc60",
      "friendly_name": "My first Twilio account",
      "status": "active",
      "date_created": "Mon, 09 Feb 2026 20:19:55 +0000",
      "date_updated": "Mon, 09 Feb 2026 20:20:05 +0000"
    }
  ]
}
```

#### 获取账户信息

```bash
GET /twilio/2010-04-01/Accounts/{AccountSid}.json
```

### 消息（短信/MMS）

#### 列出消息

```bash
GET /twilio/2010-04-01/Accounts/{AccountSid}/Messages.json
```

**查询参数：**
- `PageSize` - 每页显示的结果数量（默认：50）
- `To` - 按接收者电话号码过滤
- `From` - 按发送者电话号码过滤
- `DateSent` - 按发送日期过滤

**响应：**
```json
{
  "messages": [
    {
      "sid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "body": "Hello!",
      "from": "+15551234567",
      "to": "+15559876543",
      "status": "delivered",
      "date_sent": "Mon, 09 Feb 2026 21:00:00 +0000"
    }
  ],
  "page": 0,
  "page_size": 50
}
```

#### 获取消息详情

```bash
GET /twilio/2010-04-01/Accounts/{AccountSid}/Messages/{MessageSid}.json
```

#### 发送消息

```bash
POST /twilio/2010-04-01/Accounts/{AccountSid}/Messages.json
Content-Type: application/x-www-form-urlencoded

To=+15559876543&From=+15551234567&Body=Hello%20from%20Twilio!
```

**必填参数：**
- `To` - 收件人电话号码（E.164格式）
- `From` - Twilio电话号码或消息服务SID
- `Body` - 消息内容（最多1600个字符）

**可选参数：**
- `MessagingServiceSid` - 用于替代`From`以进行消息路由
- `MediaUrl` - 要发送的媒体文件URL（MMS）
- `StatusCallback` - 状态更新的通知URL

**响应：**
```json
{
  "sid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "body": "Hello from Twilio!",
  "from": "+15551234567",
  "to": "+15559876543",
  "status": "queued",
  "date_created": "Mon, 09 Feb 2026 21:00:00 +0000"
}
```

#### 更新消息内容

```bash
POST /twilio/2010-04-01/Accounts/{AccountSid}/Messages/{MessageSid}.json
Content-Type: application/x-www-form-urlencoded

Body=
```

将`Body`设置为空字符串即可隐藏消息内容。

#### 删除消息

```bash
DELETE /twilio/2010-04-01/Accounts/{AccountSid}/Messages/{MessageSid}.json
```

成功时返回204（表示“无内容”）。

### 通话（语音）

#### 列出通话记录

```bash
GET /twilio/2010-04-01/Accounts/{AccountSid}/Calls.json
```

**查询参数：**
- `PageSize` - 每页显示的结果数量
- `Status` - 按通话状态过滤（排队中、正在响铃、进行中、已完成等）
- `To` - 按接收者过滤
- `From` - 按呼叫者过滤

**响应：**
```json
{
  "calls": [
    {
      "sid": "CAxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "from": "+15551234567",
      "to": "+15559876543",
      "status": "completed",
      "duration": "60",
      "direction": "outbound-api"
    }
  ],
  "page": 0,
  "page_size": 50
}
```

#### 获取通话详情

```bash
GET /twilio/2010-04-01/Accounts/{AccountSid}/Calls/{CallSid}.json
```

#### 发起通话

```bash
POST /twilio/2010-04-01/Accounts/{AccountSid}/Calls.json
Content-Type: application/x-www-form-urlencoded

To=+15559876543&From=+15551234567&Url=https://example.com/twiml
```

**必填参数：**
- `To` - 接收者电话号码
- `From` - Twilio电话号码
- `Url` - TwiML应用程序URL

**可选参数：**
- `StatusCallback` - 通话状态更新的通知URL
- `StatusCallbackEvent` - 需要接收的事件（开始、响铃、接听、完成）
- `Timeout` - 等待接听的超时时间（默认：60秒）
- `Record` - 设置为`true`以录制通话

#### 更新通话状态

```bash
POST /twilio/2010-04-01/Accounts/{AccountSid}/Calls/{CallSid}.json
Content-Type: application/x-www-form-urlencoded

Status=completed
```

使用`Status=completed`来结束正在进行的通话。

#### 删除通话记录

```bash
DELETE /twilio/2010-04-01/Accounts/{AccountSid}/Calls/{CallSid}.json
```

### 电话号码

#### 列出来电号码

```bash
GET /twilio/2010-04-01/Accounts/{AccountSid}/IncomingPhoneNumbers.json
```

**响应：**
```json
{
  "incoming_phone_numbers": [
    {
      "sid": "PNxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "phone_number": "+15551234567",
      "friendly_name": "My Number",
      "capabilities": {
        "voice": true,
        "sms": true,
        "mms": true
      }
    }
  ]
}
```

#### 获取电话号码信息

```bash
GET /twilio/2010-04-01/Accounts/{AccountSid}/IncomingPhoneNumbers/{PhoneNumberSid}.json
```

#### 更新电话号码信息

```bash
POST /twilio/2010-04-01/Accounts/{AccountSid}/IncomingPhoneNumbers/{PhoneNumberSid}.json
Content-Type: application/x-www-form-urlencoded

FriendlyName=Updated%20Name&VoiceUrl=https://example.com/voice
```

#### 删除电话号码

```bash
DELETE /twilio/2010-04-01/Accounts/{AccountSid}/IncomingPhoneNumbers/{PhoneNumberSid}.json
```

### 应用程序

#### 列出应用程序

```bash
GET /twilio/2010-04-01/Accounts/{AccountSid}/Applications.json
```

**响应：**
```json
{
  "applications": [
    {
      "sid": "APxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "friendly_name": "My App",
      "voice_url": "https://example.com/voice",
      "sms_url": "https://example.com/sms"
    }
  ]
}
```

#### 获取应用程序信息

```bash
GET /twilio/2010-04-01/Accounts/{AccountSid}/Applications/{ApplicationSid}.json
```

#### 创建应用程序

```bash
POST /twilio/2010-04-01/Accounts/{AccountSid}/Applications.json
Content-Type: application/x-www-form-urlencoded

FriendlyName=My%20App&VoiceUrl=https://example.com/voice
```

**响应：**
```json
{
  "sid": "APxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "friendly_name": "My App",
  "voice_url": "https://example.com/voice",
  "date_created": "Tue, 10 Feb 2026 00:20:15 +0000"
}
```

#### 更新应用程序信息

```bash
POST /twilio/2010-04-01/Accounts/{AccountSid}/Applications/{ApplicationSid}.json
Content-Type: application/x-www-form-urlencoded

FriendlyName=Updated%20App%20Name
```

#### 删除应用程序

```bash
DELETE /twilio/2010-04-01/Accounts/{AccountSid}/Applications/{ApplicationSid}.json
```

成功时返回204（表示“无内容”）。

### 队列

#### 列出队列

```bash
GET /twilio/2010-04-01/Accounts/{AccountSid}/Queues.json
```

**响应：**
```json
{
  "queues": [
    {
      "sid": "QUxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "friendly_name": "Support Queue",
      "current_size": 0,
      "max_size": 1000,
      "average_wait_time": 0
    }
  ]
}
```

#### 创建队列

```bash
POST /twilio/2010-04-01/Accounts/{AccountSid}/Queues.json
Content-Type: application/x-www-form-urlencoded

FriendlyName=Support%20Queue&MaxSize=100
```

#### 更新队列

```bash
POST /twilio/2010-04-01/Accounts/{AccountSid}/Queues/{QueueSid}.json
Content-Type: application/x-www-form-urlencoded

FriendlyName=Updated%20Queue%20Name
```

#### 删除队列

```bash
DELETE /twilio/2010-04-01/Accounts/{AccountSid}/Queues/{QueueSid}.json
```

### 地址

#### 列出地址信息

```bash
GET /twilio/2010-04-01/Accounts/{AccountSid}/Addresses.json
```

#### 创建地址信息

```bash
POST /twilio/2010-04-01/Accounts/{AccountSid}/Addresses.json
Content-Type: application/x-www-form-urlencoded

FriendlyName=Office&Street=123%20Main%20St&City=San%20Francisco&Region=CA&PostalCode=94105&IsoCountry=US&CustomerName=Acme%20Inc
```

### 使用记录

#### 列出使用记录

```bash
GET /twilio/2010-04-01/Accounts/{AccountSid}/Usage/Records.json
```

**查询参数：**
- `Category` - 按使用类别过滤（通话、短信等）
- `StartDate` - 开始日期（YYYY-MM-DD）
- `EndDate` - 结束日期（YYYY-MM-DD）

**响应：**
```json
{
  "usage_records": [
    {
      "category": "sms",
      "description": "SMS Messages",
      "count": "100",
      "price": "0.75",
      "start_date": "2026-02-01",
      "end_date": "2026-02-28"
    }
  ]
}
```

## 分页

Twilio使用基于页面的分页机制：

```bash
GET /twilio/2010-04-01/Accounts/{AccountSid}/Messages.json?PageSize=50&Page=0
```

**参数：**
- `PageSize` - 每页显示的结果数量（默认：50）
- `Page` - 页码（从0开始计数）

**响应包含：**
```json
{
  "messages": [...],
  "page": 0,
  "page_size": 50,
  "first_page_uri": "/2010-04-01/Accounts/{AccountSid}/Messages.json?PageSize=50&Page=0",
  "next_page_uri": "/2010-04-01/Accounts/{AccountSid}/Messages.json?PageSize=50&Page=1",
  "previous_page_uri": null
}
```

使用`next_page_uri`来获取下一页的结果。

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/twilio/2010-04-01/Accounts.json',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
const accountSid = data.accounts[0].sid;
console.log(`Account SID: ${accountSid}`);
```

### Python

```python
import os
import requests

# Get account SID
response = requests.get(
    'https://gateway.maton.ai/twilio/2010-04-01/Accounts.json',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
account_sid = response.json()['accounts'][0]['sid']
print(f"Account SID: {account_sid}")
```

### Python（发送短信）

```python
import os
import requests

account_sid = 'ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

response = requests.post(
    f'https://gateway.maton.ai/twilio/2010-04-01/Accounts/{account_sid}/Messages.json',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    data={
        'To': '+15559876543',
        'From': '+15551234567',
        'Body': 'Hello from Python!'
    }
)
message = response.json()
print(f"Message SID: {message['sid']}")
print(f"Status: {message['status']}")
```

### Python（发起通话）

```python
import os
import requests

account_sid = 'ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

response = requests.post(
    f'https://gateway.maton.ai/twilio/2010-04-01/Accounts/{account_sid}/Calls.json',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    data={
        'To': '+15559876543',
        'From': '+15551234567',
        'Url': 'https://demo.twilio.com/docs/voice.xml'
    }
)
call = response.json()
print(f"Call SID: {call['sid']}")
print(f"Status: {call['status']}")
```

## 注意事项

- 所有端点都需要在路径前加上`/2010-04-01/`作为API版本前缀。
- 大多数端点需要在路径中包含您的账户SID。
- 请求正文使用`application/x-www-form-urlencoded`格式（而非JSON）。
- 电话号码必须采用E.164格式（例如：+15551234567）。
- SID是唯一的标识符：
  - 账户SID以`AC`开头
  - 消息SID以`SM`（短信）或`MM`（MMS）开头
  - 通话SID以`CA`开头
  - 电话号码SID以`PN`开头
  - 应用程序SID以`AP`开头
  - 队列SID以`QU`开头。
- 使用`POST`方法进行资源的创建和更新。
- 删除操作成功时返回204（表示“无内容”）。
- **重要提示：** 当将curl的输出传递给`jq`或其他命令时，在某些shell环境中，环境变量`$MATON_API_KEY`可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立Twilio连接或请求无效 |
| 401 | Maton API密钥无效或缺失 |
| 404 | 资源未找到 |
| 429 | 超过使用频率限制 |
| 4xx/5xx | 来自Twilio API的传递错误 |

Twilio的错误响应包括：
```json
{
  "code": 20404,
  "message": "The requested resource was not found",
  "more_info": "https://www.twilio.com/docs/errors/20404",
  "status": 404
}
```

### 故障排除：API密钥无效

**当收到“API密钥无效”的错误时，请务必按照以下步骤操作，再判断是否存在问题：**

1. 确保`MATON_API_KEY`环境变量已设置：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接信息来验证API密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 资源链接

- [Twilio API概述](https://www.twilio.com/docs/usage/api)
- [消息API](https://www.twilio.com/docs/messaging/api/message-resource)
- [通话API](https://www.twilio.com/docs/voice/api/call-resource)
- [电话号码API](https://www.twilio.com/docs/phone-numbers/api/incomingphonenumber-resource)
- [应用程序API](https://www.twilio.com/docs/usage/api/applications)
- [使用记录API](https://www.twilio.com/docs/usage/api/usage-record)