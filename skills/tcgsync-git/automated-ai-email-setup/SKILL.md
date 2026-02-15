---
name: ai-email-service
description: AI代理的仅接收邮件地址可通过 aiemailservice.com 获得。当代理需要注册服务、接收验证码/一次性密码（OTP）、获取密码重置链接或阅读传入的邮件时，可以使用该地址。该服务提供免费的邮箱创建功能、消息阅读功能、对新邮件的长轮询机制以及自动提取 OTP 的功能。由于设计初衷，该服务仅支持接收邮件，不支持发送邮件。
---

# 人工智能邮件服务

在 `aiemailservice.com` 为人工智能代理提供免费的仅接收邮件地址。

## 基本URL

```
https://aiemailservice.com
```

## 快速入门

### 1. 获取API密钥

```
POST /v1/api-key/create
Content-Type: application/json

{}
```

返回 `{ "api_key": "ak_..." }` — 请保存此密钥，这是您唯一的身份验证凭证。

### 2. 创建邮箱

```
POST /v1/mailbox/create
x-api-key: ak_your_key
Content-Type: application/json

{}
```

返回 `{ "mailbox_id": "mbx_...", "email": "agent-xyz@aiemailservice.com", "status": "active" }`。

如果省略 `{"username": "preferred-name"}`，系统会自动分配一个随机用户名。

### 3. 使用邮件地址

使用该邮件地址注册任何服务，然后通过API读取收到的邮件。

### 4. 读取邮件

```
GET /v1/mailbox/{mailbox_id}/messages
x-api-key: ak_your_key
```

### 5. 等待特定邮件（长轮询）

```
GET /v1/mailbox/{mailbox_id}/wait?timeout=30&from=noreply@github.com
x-api-key: ak_your_key
```

系统会持续等待匹配的邮件到达，直到超时。这比频繁调用 `/messages` 更高效。

### 6. 提取验证码

```
GET /v1/mailbox/{mailbox_id}/codes
x-api-key: ak_your_key
```

自动提取OTP码、验证码和确认链接。

## 身份验证

所有请求都需要包含 `x-api-key: ak_your_key` 头部（`POST /v1/api-key/create` 除外）。

另一种方式：`Authorization: Bearer ak_your_key`

## 所有端点

| 方法 | 路径 | 是否需要身份验证 | 描述 |
|--------|------|------|-------------|
| POST | `/v1/api-key/create` | 否 | 创建API密钥 |
| POST | `/v1/mailbox/create` | 是 | 创建邮箱（每个API密钥最多创建5个邮箱） |
| GET | `/v1/mailboxes` | 是 | 列出您的邮箱 |
| GET | `/v1/mailbox/{id}/status` | 是 | 查看邮箱状态 |
| GET | `/v1/mailbox/{id}/messages` | 是 | 列出邮件（`?limit=50&since=ISO`） |
| GET | `/v1/mailbox/{id}/messages/{msgId}` | 是 | 查看完整邮件内容（文本+HTML） |
| GET | `/v1/mailbox/{id}/latest` | 是 | 查看最新邮件 |
| GET | `/v1/mailbox/{id}/wait` | 是 | 长轮询新邮件（`?timeout=30&from=&subject_contains=`） |
| GET | `/v1/mailbox/{id}/codes` | 是 | 自动提取OTP码/验证码 |
| DELETE | `/v1/mailbox/{id}` | 是 | 删除邮箱及其中的邮件 |
| GET | `/v1/username/check/{username}` | 否 | 检查自定义用户名是否可用 |
| GET | `/v1/ai-prompt` | 否 | 为人工智能代理提供结构化的JSON提示 |

## 示例：完整的注册流程

```javascript
// 1. Get API key
const { api_key } = await fetch('https://aiemailservice.com/v1/api-key/create', {
  method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}'
}).then(r => r.json());

// 2. Create mailbox
const { mailbox_id, email } = await fetch('https://aiemailservice.com/v1/mailbox/create', {
  method: 'POST',
  headers: { 'x-api-key': api_key, 'Content-Type': 'application/json' },
  body: '{}'
}).then(r => r.json());

// 3. Sign up for a service using `email`
// ... (browser automation, API call, etc.)

// 4. Wait for verification email
const { message } = await fetch(
  `https://aiemailservice.com/v1/mailbox/${mailbox_id}/wait?timeout=30&from=noreply@github.com`,
  { headers: { 'x-api-key': api_key } }
).then(r => r.json());

// 5. Get extracted code
const codes = await fetch(
  `https://aiemailservice.com/v1/mailbox/${mailbox_id}/codes`,
  { headers: { 'x-api-key': api_key } }
).then(r => r.json());

console.log('Verification code:', codes[0]?.codes[0]);
```

## 示例：cURL请求

```bash
# Create API key
KEY=$(curl -s -X POST https://aiemailservice.com/v1/api-key/create -H 'Content-Type: application/json' -d '{}' | jq -r '.api_key')

# Create mailbox
curl -s -X POST https://aiemailservice.com/v1/mailbox/create \
  -H "x-api-key: $KEY" -H 'Content-Type: application/json' -d '{}'

# Read messages
curl -s https://aiemailservice.com/v1/mailbox/mbx_xxx/messages -H "x-api-key: $KEY"

# Wait for email from specific sender
curl -s "https://aiemailservice.com/v1/mailbox/mbx_xxx/wait?timeout=30&from=noreply@github.com" \
  -H "x-api-key: $KEY"

# Get verification codes
curl -s https://aiemailservice.com/v1/mailbox/mbx_xxx/codes -H "x-api-key: $KEY"
```

## 价格

- **免费**：每个API密钥最多可创建5个邮箱，包含所有功能（邮件、长轮询、验证码提取）。
- **自定义用户名**：每年99英镑，可预订特定用户名（例如 `yourname@aiemailservice.com`）。随机生成的用户名是免费的。

## 重要规则

1. **仅接收邮件**——不支持发送邮件。请勿尝试发送邮件。
2. 每个API密钥最多可创建5个免费邮箱。如需更多邮箱，请创建额外的API密钥。
3. 请求速率限制：每分钟60次。
4. 邮件保留期限：30天。
5. 每个邮箱每天最多接收100封邮件。
6. 使用 `/wait` 进行长轮询，避免频繁调用 `/messages`。
7. 使用 `/codes` 端点提取验证码，比手动解析邮件更高效。