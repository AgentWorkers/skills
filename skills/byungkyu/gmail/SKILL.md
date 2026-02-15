---
name: gmail
description: |
  Gmail API integration with managed OAuth. Read, send, and manage emails, threads, labels, and drafts. Use this skill when users want to interact with Gmail. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Gmail

您可以使用托管的 OAuth 认证来访问 Gmail API，从而读取、发送和管理电子邮件、邮件线程、标签以及草稿。

## 快速入门

```bash
# List messages
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages?maxResults=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/google-mail/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Gmail API 端点路径。该网关会将请求代理到 `gmail.googleapis.com` 并自动插入您的 OAuth 令牌。

## 认证

所有请求都必须在 `Authorization` 头中包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取您的 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Google OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-mail&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-mail'}).encode()
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
    "app": "google-mail",
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

如果您有多个 Gmail 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头，网关将使用默认的（最旧的）活动连接。

## API 参考

### 列出邮件

```bash
GET /google-mail/gmail/v1/users/me/messages?maxResults=10
```

可以使用查询过滤器：

```bash
GET /google-mail/gmail/v1/users/me/messages?q=is:unread&maxResults=10
```

### 获取邮件

```bash
GET /google-mail/gmail/v1/users/me/messages/{messageId}
```

仅获取邮件的元数据：

```bash
GET /google-mail/gmail/v1/users/me/messages/{messageId}?format=metadata&metadataHeaders=From&metadataHeaders=Subject&metadataHeaders=Date
```

### 发送邮件

```bash
POST /google-mail/gmail/v1/users/me/messages/send
Content-Type: application/json

{
  "raw": "BASE64_ENCODED_EMAIL"
}
```

### 列出标签

```bash
GET /google-mail/gmail/v1/users/me/labels
```

### 列出邮件线程

```bash
GET /google-mail/gmail/v1/users/me/threads?maxResults=10
```

### 获取邮件线程信息

```bash
GET /google-mail/gmail/v1/users/me/threads/{threadId}
```

### 修改邮件标签

```bash
POST /google-mail/gmail/v1/users/me/messages/{messageId}/modify
Content-Type: application/json

{
  "addLabelIds": ["STARRED"],
  "removeLabelIds": ["UNREAD"]
}
```

### 将邮件移至回收站

```bash
POST /google-mail/gmail/v1/users/me/messages/{messageId}/trash
```

### 创建草稿

```bash
POST /google-mail/gmail/v1/users/me/drafts
Content-Type: application/json

{
  "message": {
    "raw": "BASE64URL_ENCODED_EMAIL"
  }
}
```

### 发送草稿

```bash
POST /google-mail/gmail/v1/users/me/drafts/send
Content-Type: application/json

{
  "id": "{draftId}"
}
```

### 获取用户信息

```bash
GET /google-mail/gmail/v1/users/me/profile
```

## 查询操作符

在 `q` 参数中使用以下操作符：
- `is:unread` - 未读邮件
- `is:starred` - 被标记为星号的邮件
- `from:email@example.com` - 来自特定发件人的邮件
- `to:email@example.com` - 收件人为特定收件人的邮件
- `subject:keyword` - 主题包含关键词的邮件
- `after:2024/01/01` - 发送日期在 2024 年 1 月 1 日之后的邮件
- `before:2024/12/31` - 发送日期在 2024 年 12 月 31 日之前的邮件
- `has:attachment` - 包含附件的邮件

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages?maxResults=10',
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
    'https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'maxResults': 10, 'q': 'is:unread'}
)
```

## 注意事项

- 使用 `me` 作为已认证用户的用户 ID。
- 邮件正文在 `raw` 字段中以 Base64URL 格式编码。
- 常见的标签有：`INBOX`（收件箱）、`SENT`（已发送）、`DRAFT`（草稿）、`STARRED`（被标记为星号）、`UNREAD`（未读）、`TRASH`（回收站）。
- 重要提示：当 URL 包含方括号（如 `fields[]`、`sort[]`、`records[]`）时，使用 `curl -g` 可以避免全局解析问题。
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境可能无法正确解析 `$MATON_API_KEY` 环境变量，这可能导致“无效 API 密钥”的错误。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Gmail 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 每个账户的请求速率限制（每秒 10 次请求） |
| 4xx/5xx | 来自 Gmail API 的传递错误 |

### 故障排除：API 密钥问题

1. 确保已设置 `MATON_API_KEY` 环境变量：

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

1. 确保您的 URL 路径以 `google-mail` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages`
- 错误的路径：`https://gateway.maton.ai/gmail/v1/users/me/messages`

## 资源

- [Gmail API 概述](https://developers.google.com/gmail/api/reference/rest)
- [列出邮件](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/list)
- [获取邮件](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/get)
- [发送邮件](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/send)
- [列出邮件线程](https://developers.google.com/gmail/api/reference/rest/v1/users.threads/list)
- [列出标签](https://developers.google.com/gmail/api/reference/rest/v1/users.labels/list)
- [创建草稿](https://developers.google.com/gmail/api/reference/rest/v1/users.drafts/create)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)