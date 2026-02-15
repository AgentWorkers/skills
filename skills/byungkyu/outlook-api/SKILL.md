---
name: outlook
description: |
  Microsoft Outlook API integration with managed OAuth. Read, send, and manage emails, folders, calendar events, and contacts via Microsoft Graph. Use this skill when users want to interact with Outlook. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Outlook

您可以使用托管的 OAuth 认证方式访问 Microsoft Outlook API（通过 Microsoft Graph）。该 API 允许您读取、发送和管理电子邮件、文件夹、日历事件以及联系人信息。

## 快速入门

```bash
# Get user profile
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/outlook/v1.0/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/outlook/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Microsoft Graph API 端点路径。该网关会将请求代理到 `graph.microsoft.com` 并自动插入您的 OAuth 令牌。

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
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的 Microsoft OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=outlook&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'outlook'}).encode()
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
    "app": "outlook",
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

如果您有多个 Outlook 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/outlook/v1.0/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头部，网关将使用默认的（最旧的）活动连接。

## API 参考

### 用户资料

```bash
GET /outlook/v1.0/me
```

### 邮件文件夹

#### 列出邮件文件夹

```bash
GET /outlook/v1.0/me/mailFolders
```

#### 获取邮件文件夹信息

```bash
GET /outlook/v1.0/me/mailFolders/{folderId}
```

常见的文件夹名称：`Inbox`（收件箱）、`Drafts`（草稿）、`SentItems`（已发送项）、`DeletedItems`（已删除项）、`Archive`（归档）、`JunkEmail`（垃圾邮件）

#### 创建邮件文件夹

```bash
POST /outlook/v1.0/me/mailFolders
Content-Type: application/json

{
  "displayName": "My Folder"
}
```

#### 删除邮件文件夹

```bash
DELETE /outlook/v1.0/me/mailFolders/{folderId}
```

#### 列出子文件夹

```bash
GET /outlook/v1.0/me/mailFolders/{folderId}/childFolders
```

### 消息

#### 列出消息

```bash
GET /outlook/v1.0/me/messages
```

从特定文件夹中获取消息：

```bash
GET /outlook/v1.0/me/mailFolders/Inbox/messages
```

使用查询过滤器：

```bash
GET /outlook/v1.0/me/messages?$filter=isRead eq false&$top=10
```

#### 获取消息内容

```bash
GET /outlook/v1.0/me/messages/{messageId}
```

#### 创建草稿

```bash
POST /outlook/v1.0/me/messages
Content-Type: application/json

{
  "subject": "Hello",
  "body": {
    "contentType": "Text",
    "content": "This is the email body."
  },
  "toRecipients": [
    {
      "emailAddress": {
        "address": "recipient@example.com"
      }
    }
  ]
}
```

#### 发送消息

```bash
POST /outlook/v1.0/me/sendMail
Content-Type: application/json

{
  "message": {
    "subject": "Hello",
    "body": {
      "contentType": "Text",
      "content": "This is the email body."
    },
    "toRecipients": [
      {
        "emailAddress": {
          "address": "recipient@example.com"
        }
      }
    ]
  },
  "saveToSentItems": true
}
```

#### 发送现有草稿

```bash
POST /outlook/v1.0/me/messages/{messageId}/send
```

#### 更新消息

```bash
PATCH /outlook/v1.0/me/messages/{messageId}
Content-Type: application/json

{
  "isRead": true
}
```

#### 删除消息

```bash
DELETE /outlook/v1.0/me/messages/{messageId}
```

#### 移动消息

```bash
POST /outlook/v1.0/me/messages/{messageId}/move
Content-Type: application/json

{
  "destinationId": "{folderId}"
}
```

### 日历

#### 列出日历

```bash
GET /outlook/v1.0/me/calendars
```

#### 列出事件

```bash
GET /outlook/v1.0/me/calendar/events
```

使用日期过滤器：

```bash
GET /outlook/v1.0/me/calendar/events?$filter=start/dateTime ge '2024-01-01'&$top=10
```

#### 获取事件信息

```bash
GET /outlook/v1.0/me/events/{eventId}
```

#### 创建事件

```bash
POST /outlook/v1.0/me/calendar/events
Content-Type: application/json

{
  "subject": "Meeting",
  "start": {
    "dateTime": "2024-01-15T10:00:00",
    "timeZone": "UTC"
  },
  "end": {
    "dateTime": "2024-01-15T11:00:00",
    "timeZone": "UTC"
  },
  "attendees": [
    {
      "emailAddress": {
        "address": "attendee@example.com"
      },
      "type": "required"
    }
  ]
}
```

#### 删除事件

```bash
DELETE /outlook/v1.0/me/events/{eventId}
```

### 联系人

#### 列出联系人

```bash
GET /outlook/v1.0/me/contacts
```

#### 获取联系人信息

```bash
GET /outlook/v1.0/me/contacts/{contactId}
```

#### 创建联系人

```bash
POST /outlook/v1.0/me/contacts
Content-Type: application/json

{
  "givenName": "John",
  "surname": "Doe",
  "emailAddresses": [
    {
      "address": "john.doe@example.com"
    }
  ]
}
```

#### 删除联系人

```bash
DELETE /outlook/v1.0/me/contacts/{contactId}
```

## 查询参数

使用 OData 查询参数：

- `$top=10` - 限制结果数量
- `$skip=20` - 跳过指定数量的结果（分页）
- `$select=subject,from` - 选择特定字段
- `$filter=isRead eq false` - 过滤结果
- `$orderby=receivedDateTime desc` - 按接收时间降序排序结果
- `$search="keyword"` - 按内容搜索

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/outlook/v1.0/me/messages?$top=10',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/outlook/v1.0/me/messages',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'$top': 10, '$filter': 'isRead eq false'}
)
```

## 注意事项

- 使用 `me` 作为已认证用户的标识符。
- 消息正文的内容类型可以是 `Text` 或 `HTML`。
- 常见的文件夹名称可以直接用作文件夹 ID（例如：`Inbox`、`Drafts`、`SentItems` 等）。
- 日历事件使用 ISO 8601 日期时间格式。
- **重要提示：** 当 URL 中包含方括号（如 `fields[]`、`sort[]`、`records[]`）时，使用 `curl -g` 可以防止全局解析问题。
- **重要提示：** 在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境可能无法正确解析环境变量 `$MATON_API_KEY`，这可能导致 “无效 API 密钥” 错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立 Outlook 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 每个账户的请求速率限制（每秒 10 次请求） |
| 4xx/5xx | 来自 Microsoft Graph API 的传递错误 |

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

### 故障排除：应用名称错误

1. 确保您的 URL 路径以 `outlook` 开头。例如：
  - 正确的路径：`https://gateway.maton.ai/outlook/v1.0/me/messages`
  - 错误的路径：`https://gateway.maton.ai/v1.0/me/messages`

## 资源

- [Microsoft Graph API 概述](https://learn.microsoft.com/en-us/graph/api/overview)
- [邮件 API](https://learn.microsoft.com/en-us/graph/api/resources/mail-api-overview)
- [日历 API](https://learn.microsoft.com/en-us/graph/api/resources/calender)
- [联系人 API](https://learn.microsoft.com/en-us/graph/api/resources/contact)
- [查询参数](https://learn.microsoft.com/en-us/graph/query-parameters)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)