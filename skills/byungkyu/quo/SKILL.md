---
name: quo
description: |
  Quo API integration with managed OAuth. Manage calls, messages, contacts, and conversations for your business phone system.
  Use this skill when users want to send SMS, list calls, manage contacts, or retrieve call recordings/transcripts.
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

# Quo

您可以使用管理的 OAuth 认证来访问 Quo API。该 API 支持发送短信、管理通话和联系人信息，以及检索通话记录和通话录音。

## 快速入门

```bash
# List phone numbers
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/quo/v1/phone-numbers')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('User-Agent', 'Maton/1.0')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/quo/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Quo API 端点路径。该网关会将请求代理到 `api.openphone.com`，并自动插入您的 OAuth 令牌。

## 认证

所有请求都需要在 `Authorization` 头部包含 Maton API 密钥，并在 `User-Agent` 头部指定用户代理：

```
Authorization: Bearer $MATON_API_KEY
User-Agent: Maton/1.0
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

您可以在 `https://ctrl.maton.ai` 上管理您的 Quo OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=quo&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'quo'}).encode()
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
    "app": "quo",
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

如果您有多个 Quo 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/quo/v1/phone-numbers')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('User-Agent', 'Maton/1.0')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头部，网关将使用默认的（最旧的）活动连接。

## API 参考

### 电话号码

#### 列出电话号码

```bash
GET /quo/v1/phone-numbers
```

可选查询参数：
- `userId` - 按用户 ID 过滤（模式：`^US(.*)$`）

**响应：**
```json
{
  "data": [
    {
      "id": "PN123abc",
      "number": "+15555555555",
      "formattedNumber": "(555) 555-5555",
      "name": "Main Line",
      "users": [
        {
          "id": "US123abc",
          "email": "user@example.com",
          "firstName": "John",
          "lastName": "Doe",
          "role": "admin"
        }
      ],
      "createdAt": "2022-01-01T00:00:00Z",
      "updatedAt": "2022-01-01T00:00:00Z"
    }
  ]
}
```

### 用户

#### 列出用户

```bash
GET /quo/v1/users?maxResults=50
```

查询参数：
- `maxResults`（必填）- 每页显示的结果数量（1-50，默认：10）
- `pageToken` - 分页令牌

**响应：**
```json
{
  "data": [
    {
      "id": "US123abc",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "role": "owner",
      "createdAt": "2022-01-01T00:00:00Z",
      "updatedAt": "2022-01-01T00:00:00Z"
    }
  ],
  "totalItems": 10,
  "nextPageToken": null
}
```

#### 根据 ID 获取用户信息

```bash
GET /quo/v1/users/{userId}
```

### 消息

#### 发送短信

```bash
POST /quo/v1/messages
Content-Type: application/json

{
  "content": "Hello, world!",
  "from": "PN123abc",
  "to": ["+15555555555"]
}
```

请求体：
- `content`（必填）- 消息内容（1-1600 个字符）
- `from`（必填）- 电话号码 ID（格式：`PN*`）或 E.164 格式
- `to`（必填）- 收件人电话号码数组（格式：E.164）
- `userId` - 用户 ID（默认为电话号码所有者）
- `setInboxStatus` - 设置为 `"done"` 以标记对话完成

**响应（202）：**
```json
{
  "id": "AC123abc",
  "to": ["+15555555555"],
  "from": "+15555555555",
  "text": "Hello, world!",
  "phoneNumberId": "PN123abc",
  "direction": "outgoing",
  "userId": "US123abc",
  "status": "queued",
  "createdAt": "2022-01-01T00:00:00Z",
  "updatedAt": "2022-01-01T00:00:00Z"
}
```

#### 列出消息

```bash
GET /quo/v1/messages?phoneNumberId=PN123abc&participants[]=+15555555555&maxResults=100
```

查询参数：
- `phoneNumberId`（必填）- 电话号码 ID
- `participants`（必填）- 参与者电话号码数组（格式：E.164）
- `maxResults`（必填）- 每页显示的结果数量（1-100，默认：10）
- `userId` - 按用户 ID 过滤
- `createdAfter` - ISO 8601 时间戳
- `createdBefore` - ISO 8601 时间戳
- `pageToken` - 分页令牌

#### 根据 ID 获取消息

```bash
GET /quo/v1/messages/{messageId}
```

### 通话

#### 列出通话记录

```bash
GET /quo/v1/calls?phoneNumberId=PN123abc&participants[]=+15555555555&maxResults=100
```

查询参数：
- `phoneNumberId`（必填）- 电话号码 ID
- `participants`（必填）- 参与者电话号码数组（格式：E.164）
- `maxResults`（必填）- 每页显示的结果数量（1-100，默认：10）
- `userId` - 按用户 ID 过滤
- `createdAfter` - ISO 8601 时间戳
- `createdBefore` - ISO 8601 时间戳
- `pageToken` - 分页令牌

**响应：**
```json
{
  "data": [
    {
      "id": "AC123abc",
      "phoneNumberId": "PN123abc",
      "userId": "US123abc",
      "direction": "incoming",
      "status": "completed",
      "duration": 120,
      "participants": ["+15555555555"],
      "answeredAt": "2022-01-01T00:00:00Z",
      "completedAt": "2022-01-01T00:02:00Z",
      "createdAt": "2022-01-01T00:00:00Z",
      "updatedAt": "2022-01-01T00:02:00Z"
    }
  ],
  "totalItems": 50,
  "nextPageToken": "..."
}
```

#### 根据 ID 获取通话记录

```bash
GET /quo/v1/calls/{callId}
```

#### 获取通话录音

```bash
GET /quo/v1/call-recordings/{callId}
```

**响应：**
```json
{
  "data": [
    {
      "id": "REC123abc",
      "duration": 120,
      "startTime": "2022-01-01T00:00:00Z",
      "status": "completed",
      "type": "voicemail",
      "url": "https://..."
    }
  ]
}
```

录音状态值：`absent`、`completed`、`deleted`、`failed`、`in-progress`、`paused`、`processing`、`stopped`、`stopping`

#### 获取通话摘要

```bash
GET /quo/v1/call-summaries/{callId}
```

#### 获取通话录音文本

```bash
GET /quo/v1/call-transcripts/{callId}
```

#### 获取通话语音邮件

```bash
GET /quo/v1/call-voicemails/{callId}
```

### 联系人

#### 列出联系人

```bash
GET /quo/v1/contacts?maxResults=50
```

查询参数：
- `maxResults`（必填）- 每页显示的结果数量（1-50，默认：10）
- `externalIds` - 外部标识符数组
- `sources` - 来源指示器数组
- `pageToken` - 分页令牌

**响应：**
```json
{
  "data": [
    {
      "id": "CT123abc",
      "externalId": null,
      "source": null,
      "defaultFields": {
        "company": "Acme Corp",
        "firstName": "Jane",
        "lastName": "Doe",
        "role": "Manager",
        "emails": [{"name": "work", "value": "jane@example.com", "id": "EM1"}],
        "phoneNumbers": [{"name": "mobile", "value": "+15555555555", "id": "PH1"}]
      },
      "customFields": [],
      "createdAt": "2022-01-01T00:00:00Z",
      "updatedAt": "2022-01-01T00:00:00Z",
      "createdByUserId": "US123abc"
    }
  ],
  "totalItems": 100,
  "nextPageToken": "..."
}
```

#### 根据 ID 获取联系人信息

```bash
GET /quo/v1/contacts/{contactId}
```

#### 创建联系人

```bash
POST /quo/v1/contacts
Content-Type: application/json

{
  "defaultFields": {
    "firstName": "Jane",
    "lastName": "Doe",
    "company": "Acme Corp",
    "phoneNumbers": [{"name": "mobile", "value": "+15555555555"}],
    "emails": [{"name": "work", "value": "jane@example.com"}]
  }
}
```

#### 更新联系人信息

```bash
PATCH /quo/v1/contacts/{contactId}
Content-Type: application/json

{
  "defaultFields": {
    "company": "New Company"
  }
}
```

#### 删除联系人

```bash
DELETE /quo/v1/contacts/{contactId}
```

#### 获取联系人自定义字段

```bash
GET /quo/v1/contact-custom-fields
```

### 对话

#### 列出对话记录

```bash
GET /quo/v1/conversations?maxResults=100
```

查询参数：
- `maxResults`（必填）- 每页显示的结果数量（1-100，默认：10）
- `phoneNumbers` - 电话号码 ID 或 E.164 格式的电话号码数组
- `userId` - 按用户 ID 过滤
- `createdAfter` - ISO 8601 时间戳
- `createdBefore` - ISO 8601 时间戳
- `updatedAfter` - ISO 8601 时间戳
- `updatedBefore` - ISO 8601 时间戳
- `excludeInactive` - 布尔值，用于排除不活跃的对话
- `pageToken` - 分页令牌

**响应：**
```json
{
  "data": [
    {
      "id": "CV123abc",
      "phoneNumberId": "PN123abc",
      "name": "Jane Doe",
      "participants": ["+15555555555"],
      "assignedTo": "US123abc",
      "lastActivityAt": "2022-01-01T00:00:00Z",
      "createdAt": "2022-01-01T00:00:00Z",
      "updatedAt": "2022-01-01T00:00:00Z"
    }
  ],
  "totalItems": 50,
  "nextPageToken": "..."
}
```

## 分页

Quo 使用基于令牌的分页机制。请使用 `maxResults` 设置每页显示的数量，并使用 `pageToken` 获取后续页面。

```bash
GET /quo/v1/contacts?maxResults=50&pageToken=eyJsYXN0SWQiOi...
```

响应中包含分页信息：

```json
{
  "data": [...],
  "totalItems": 150,
  "nextPageToken": "eyJsYXN0SWQiOi..."
}
```

当 `nextPageToken` 为 `null` 时，表示已到达最后一页。

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/quo/v1/phone-numbers',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'User-Agent': 'Maton/1.0'
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
    'https://gateway.maton.ai/quo/v1/phone-numbers',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'User-Agent': 'Maton/1.0'
    }
)
data = response.json()
```

### 发送短信示例

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/quo/v1/messages',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'User-Agent': 'Maton/1.0',
        'Content-Type': 'application/json'
    },
    json={
        'content': 'Hello from Quo!',
        'from': 'PN123abc',
        'to': ['+15555555555']
    }
)
data = response.json()
```

## 注意事项

- 电话号码 ID 以 `PN` 开头。
- 用户 ID 以 `US` 开头。
- 通话/消息 ID 以 `AC` 开头。
- 电话号码必须采用 E.164 格式（例如：`+15555555555`）。
- 短信费用：每条消息 $0.01（美国/加拿大）；国际费率适用。
- 每条消息最多 1600 个字符。
- 列出通话记录时只能包含一个参与者（仅支持 1:1 对话）。
- 重要提示：所有 API 请求都需要包含 `User-Agent` 头部（例如：`User-Agent: Maton/1.0`）。缺少此头部的请求将被拒绝。
- 重要提示：当使用 `curl` 命令时，如果 URL 中包含方括号（`participants[]`），请使用 `curl -g` 以禁用全局解析。
- 重要提示：当将 `curl` 的输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 请求错误（例如：参与者过多、格式无效） |
| 401 | Maton API 密钥无效或缺失 |
| 402 | 短信信用不足 |
| 403 | 无权限访问该电话号码 |
| 404 | 资源未找到 |
| 429 | 调用次数限制 |
| 500 | 服务器错误 |

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

1. 确保您的 URL 路径以 `quo` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/quo/v1/phone-numbers`
- 错误的路径：`https://gateway.maton.ai/openphone/v1/phone-numbers`

## 资源

- [Quo API 介绍](https://www.quo.com/docs/mdx/api-reference/introduction)
- [Quo API 认证](https://www.quo.com/docs/mdx/api-reference/authentication)
- [Quo 支持中心](https://support.quo.com/core-concepts/integrations/api)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)