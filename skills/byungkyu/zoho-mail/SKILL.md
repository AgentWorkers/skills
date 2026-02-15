---
name: zoho-mail
description: |
  Zoho Mail API integration with managed OAuth. Send, receive, and manage emails, folders, and labels.
  Use this skill when users want to send emails, read messages, manage folders, or work with email labels in Zoho Mail.
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

# Zoho Mail

您可以使用受管理的 OAuth 认证来访问 Zoho Mail API。该 API 允许您发送、接收、搜索电子邮件，并对电子邮件及其文件夹和标签进行完整的管理。

## 快速入门

```bash
# List all accounts
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-mail/api/accounts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/zoho-mail/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Zoho Mail API 端点路径。Maton 代理会将请求转发到 `mail.zoho.com` 并自动插入您的 OAuth 令牌。

## 认证

所有请求都必须在 `Authorization` 标头中包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 上管理您的 Zoho Mail OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=zoho-mail&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'zoho-mail'}).encode()
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
    "app": "zoho-mail",
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

如果您有多个 Zoho Mail 连接，请使用 `Maton-Connection` 标头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-mail/api/accounts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此参数，Maton 代理将使用默认的（最旧的）活动连接。

## API 参考

### 账户操作

#### 获取所有账户

检索已认证用户的所有邮件账户。

```bash
GET /zoho-mail/api/accounts
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-mail/api/accounts')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取账户详情

```bash
GET /zoho-mail/api/accounts/{accountId}
```

### 文件夹操作

#### 列出所有文件夹

```bash
GET /zoho-mail/api/accounts/{accountId}/folders
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-mail/api/accounts/{accountId}/folders')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "status": {
    "code": 200,
    "description": "success"
  },
  "data": [
    {
      "folderId": "1367000000000008014",
      "folderName": "Inbox",
      "folderType": "Inbox",
      "path": "/Inbox",
      "imapAccess": true,
      "isArchived": 0,
      "URI": "https://mail.zoho.com/api/accounts/1367000000000008002/folders/1367000000000008014"
    },
    {
      "folderId": "1367000000000008016",
      "folderName": "Drafts",
      "folderType": "Drafts",
      "path": "/Drafts",
      "imapAccess": true,
      "isArchived": 0
    }
  ]
}
```

#### 创建文件夹

```bash
POST /zoho-mail/api/accounts/{accountId}/folders
Content-Type: application/json

{
  "folderName": "My Custom Folder"
}
```

#### 重命名文件夹

```bash
PUT /zoho-mail/api/accounts/{accountId}/folders/{folderId}
Content-Type: application/json

{
  "folderName": "Renamed Folder"
}
```

#### 删除文件夹

```bash
DELETE /zoho-mail/api/accounts/{accountId}/folders/{folderId}
```

### 标签操作

#### 列出标签

```bash
GET /zoho-mail/api/accounts/{accountId}/labels
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-mail/api/accounts/{accountId}/labels')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建标签

```bash
POST /zoho-mail/api/accounts/{accountId}/labels
Content-Type: application/json

{
  "labelName": "Important"
}
```

#### 更新标签

```bash
PUT /zoho-mail/api/accounts/{accountId}/labels/{labelId}
Content-Type: application/json

{
  "labelName": "Updated Label"
}
```

#### 删除标签

```bash
DELETE /zoho-mail/api/accounts/{accountId}/labels/{labelId}
```

### 邮件操作

#### 列出文件夹中的邮件

```bash
GET /zoho-mail/api/accounts/{accountId}/messages/view?folderId={folderId}
```

**查询参数：**

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `folderId` | long | 要列出邮件的文件夹 ID |
| `limit` | integer | 返回的邮件数量（默认：50） |
| `start` | integer | 分页偏移量 |
| `sortBy` | string | 排序字段（例如：`date`） |
| `sortOrder` | boolean | `true` 表示升序，`false` 表示降序 |

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-mail/api/accounts/{accountId}/messages/view?folderId={folderId}&limit=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 搜索邮件

```bash
GET /zoho-mail/api/accounts/{accountId}/messages/search?searchKey={query}
```

**查询参数：**

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `searchKey` | string | 搜索关键字 |
| `limit` | integer | 返回的结果数量 |
| `start` | integer | 分页偏移量 |

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
import urllib.parse
query = urllib.parse.quote('from:sender@example.com')
req = urllib.request.Request(f'https://gateway.maton.ai/zoho-mail/api/accounts/{{accountId}}/messages/search?searchKey={query}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取邮件内容

```bash
GET /zoho-mail/api/accounts/{accountId}/folders/{folderId}/messages/{messageId}/content
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-mail/api/accounts/{accountId}/folders/{folderId}/messages/{messageId}/content')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取邮件头部信息

```bash
GET /zoho-mail/api/accounts/{accountId}/folders/{folderId}/messages/{messageId}/header
```

#### 获取邮件元数据

```bash
GET /zoho-mail/api/accounts/{accountId}/folders/{folderId}/messages/{messageId}/details
```

#### 获取原始邮件（MIME 格式）

```bash
GET /zoho-mail/api/accounts/{accountId}/messages/{messageId}/originalmessage
```

#### 发送邮件

```bash
POST /zoho-mail/api/accounts/{accountId}/messages
Content-Type: application/json

{
  "fromAddress": "sender@yourdomain.com",
  "toAddress": "recipient@example.com",
  "subject": "Email Subject",
  "content": "Email body content",
  "mailFormat": "html"
}
```

**请求体字段：**

| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `fromAddress` | string | 是 | 发件人邮箱地址 |
| `toAddress` | string | 是 | 收件人邮箱地址 |
| `subject` | string | 是 | 邮件主题 |
| `content` | string | 是 | 邮件正文内容 |
| `ccAddress` | string | 否 | 抄送收件人邮箱 |
| `bccAddress` | string | 否 | 密件抄送收件人邮箱 |
| `mailFormat` | string | 否 | `html` 或 `plaintext`（默认：`html`） |
| `askReceipt` | string | 否 | 是否要求发送阅读回执 |
| `encoding` | string | 否 | 字符编码（默认：`UTF-8` |

**示例 - 发送邮件：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "fromAddress": "sender@yourdomain.com",
    "toAddress": "recipient@example.com",
    "subject": "Hello from Zoho Mail API",
    "content": "<h1>Hello!</h1><p>This is a test email.</p>",
    "mailFormat": "html"
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/zoho-mail/api/accounts/{accountId}/messages', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**调度参数（可选）：**

| 参数 | 类型 | 描述 |
|-------|------|-------------|
| `isSchedule` | boolean | 是否启用调度 |
| `scheduleType` | integer | 1-5 表示预设时间；6 表示自定义时间 |
| `timeZone` | string | 如果 `scheduleType` 为 6 时必填（例如：`GMT 5:30`） |
| `scheduleTime` | string | 如果 `scheduleType` 为 6 时必填（格式：`MM/DD/YYYY HH:MM:SS`） |

#### 回复邮件

```bash
POST /zoho-mail/api/accounts/{accountId}/messages/{messageId}
Content-Type: application/json

{
  "fromAddress": "sender@yourdomain.com",
  "toAddress": "recipient@example.com",
  "subject": "Re: Original Subject",
  "content": "Reply content"
}
```

#### 保存草稿

```bash
POST /zoho-mail/api/accounts/{accountId}/messages
Content-Type: application/json

{
  "fromAddress": "sender@yourdomain.com",
  "toAddress": "recipient@example.com",
  "subject": "Draft Subject",
  "content": "Draft content",
  "mode": "draft"
}
```

#### 更新邮件（标记为已读/未读、移动、设置标记）

```bash
PUT /zoho-mail/api/accounts/{accountId}/updatemessage
Content-Type: application/json

{
  "messageId": ["messageId1", "messageId2"],
  "folderId": "folderId",
  "mode": "markAsRead"
}
```

**操作选项：**
- `markAsRead` - 将邮件标记为已读
- `markAsUnread` - 将邮件标记为未读
- `moveMessage` - 移动邮件（需要 `destfolderId`）
- `flag` - 设置标记（需要 `flagid`：1-4）
- `archive` - 将邮件归档
- `unArchive` - 解压邮件
- `spam` - 将邮件标记为垃圾邮件
- `notSpam` - 将邮件标记为非垃圾邮件

**示例 - 标记为已读：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "messageId": ["1234567890123456789"],
    "folderId": "9876543210987654321",
    "mode": "markAsRead"
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/zoho-mail/api/accounts/{accountId}/updatemessage', data=data, method='PUT')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 删除邮件

```bash
DELETE /zoho-mail/api/accounts/{accountId}/folders/{folderId}/messages/{messageId}
```

### 附件操作

#### 上传附件

```bash
POST /zoho-mail/api/accounts/{accountId}/messages/attachments
Content-Type: multipart/form-data
```

#### 获取附件信息

```bash
GET /zoho-mail/api/accounts/{accountId}/folders/{folderId}/messages/{messageId}/attachmentinfo
```

#### 下载附件

```bash
GET /zoho-mail/api/accounts/{accountId}/folders/{folderId}/messages/{messageId}/attachments/{attachmentId}
```

## 分页

Zoho Mail 使用基于偏移量的分页机制：

```bash
GET /zoho-mail/api/accounts/{accountId}/messages/view?folderId={folderId}&start=0&limit=50
```

- `start`：偏移量索引（默认：0）
- `limit`：返回的记录数量（默认：50）

对于后续页面，将 `start` 增加 `limit`：
- 第 1 页：`start=0&limit=50`
- 第 2 页：`start=50&limit=50`
- 第 3 页：`start=100&limit=50`

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/zoho-mail/api/accounts',
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
    'https://gateway.maton.ai/zoho-mail/api/accounts',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
```

## 注意事项

- 大多数操作都需要账户 ID——首次调用 `/api/accounts` 以获取您的账户 ID。
- 邮件 ID 和文件夹 ID 是数字字符串。
- `fromAddress` 必须与已认证的账户关联。
- 默认文件夹包括：收件箱、草稿箱、模板、待办事项、已发送邮件、垃圾邮件、收件箱外。
- 支持的编码格式：Big5、EUC-JP、EUC-KR、GB2312、ISO-2022-JP、ISO-8859-1、KOI8-R、Shift_JIS、US-ASCII、UTF-8、WINDOWS-1251。
- 某些操作（如标签管理、文件夹操作、发送邮件）需要额外的 OAuth 权限范围。如果您收到 `INVALID_OAUTHSCOPE` 错误，请联系 Maton 支持团队（support@maton.ai），并提供所需的操作、API 以及使用场景。
- 重要提示：当 URL 包含括号时，使用 `curl -g` 以禁用全局解析。
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确展开。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Zoho Mail 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 请求频率限制 |
| 4xx/5xx | 来自 Zoho Mail API 的传递错误 |

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

### 故障排除：应用程序名称无效

1. 确保您的 URL 路径以 `zoho-mail` 开头。例如：

- 正确：`https://gateway.maton.ai/zoho-mail/api/accounts`
- 错误：`https://gateway.maton.ai/api/accounts`

## 资源

- [Zoho Mail API 概述](https://www.zoho.com/mail/help/api/overview.html)
- [Zoho Mail API 索引](https://www.zoho.com/mail/help/api/)
- [电子邮件 API](https://www.zoho.com/mail/help/api/email-api.html)
- [开始使用 Zoho Mail API](https://www.zoho.com/mail/help/api/getting-started-with-api.html)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)