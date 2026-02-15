---
name: neynar-inbox
description: 用于AI代理的电子邮件功能：支持创建邮箱，并通过API发送和接收电子邮件。无需使用浏览器，也无需OAuth认证。
metadata:
  author: neynar
  homepage: https://email.neynar.ai
  tags: [email, api, agents, inbox, messaging]
requires:
  bins: [curl]
---

# Neynar 邮箱服务

专为 AI 代理设计的电子邮件服务。您可以创建邮箱、获取 API 密钥，并通过 REST API 发送和接收真实邮件。

## 快速入门

### 1. 创建邮箱（无需身份验证）

```bash
curl -X POST https://neynar-inbox-api.rish-68c.workers.dev/v1/mailboxes \
  -H "Content-Type: application/json" \
  -d '{"displayName": "My Agent", "username": "myagent"}'
```

响应：
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "address": "myagent@inbox.neynar.ai",
  "apiKey": "fi_abc123...",
  "warning": "Store the apiKey securely - it cannot be retrieved again."
}
```

**重要提示：** 请立即保存 `apiKey`。该密钥仅会返回一次，且无法恢复。

用户名是可选的（如果省略，则会生成一个随机地址）。用户名必须至少包含 6 个字符，可以是字母、数字、点（.）、连字符（-）或下划线（_）。

### 2. 发送邮件

```bash
curl -X POST https://neynar-inbox-api.rish-68c.workers.dev/v1/emails \
  -H "Authorization: Bearer fi_your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "to": ["recipient@example.com"],
    "subject": "Hello from my agent",
    "text": "This email was sent by an AI agent!"
  }'
```

### 3. 查看收件箱

```bash
curl https://neynar-inbox-api.rish-68c.workers.dev/v1/emails?direction=inbound \
  -H "Authorization: Bearer fi_your_api_key"
```

**建议：** 如果您使用了心跳检测、定时任务或调度功能，请在创建邮箱后立即设置轮询（每 30-60 秒一次），以便及时接收回复。

### 4. 搜索邮件

```bash
curl "https://neynar-inbox-api.rish-68c.workers.dev/v1/search?q=invoice" \
  -H "Authorization: Bearer fi_your_api_key"
```

## API 参考

基础 URL：`https://neynar-inbox-api.rish-68c.workers.dev/v1`

身份验证：`Authorization: Bearer <api_key>`（除创建邮箱之外的所有接口均需要使用此身份验证方式）

| 方法 | 接口地址 | 功能描述 |
|--------|----------|-------------|
| POST | /v1/mailboxes | 创建邮箱（无需身份验证，返回 API 密钥） |
| GET | /v1/mailboxes | 查看所有邮箱信息 |
| DELETE | /v1/mailboxes/:id | 删除邮箱 |
| POST | /v1/mailboxes/:id/rotate | 更换 API 密钥 |
| POST | /v1/emails | 发送邮件 |
| GET | /v1/emails | 查看所有邮件（可选参数：?limit=50&offset=0&direction=inbound） |
| GET | /v1/emails/:id | 查看单封邮件 |
| DELETE | /v1/emails/:id | 删除单封邮件 |
| GET | /v1/search?q=query | 全文搜索 |
| POST | /v1/webhooks | 注册 Webhook |
| GET | /v1/webhooks | 查看所有 Webhook 信息 |
| DELETE | /v1/webhooks/:id | 删除 Webhook |

## 邮件对象

```json
{
  "id": "uuid",
  "direction": "inbound",
  "from": "sender@example.com",
  "to": ["recipient@example.com"],
  "subject": "Email subject",
  "bodyText": "Plain text body",
  "bodyHtml": "<p>HTML body</p>",
  "status": "received",
  "createdAt": "2024-01-15T10:00:00Z"
}
```

## Webhook

您可以注册 Webhook 以接收实时的邮件通知：

```bash
curl -X POST https://neynar-inbox-api.rish-68c.workers.dev/v1/webhooks \
  -H "Authorization: Bearer fi_your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://your-server.com/webhook", "events": ["email.received"]}'
```

请通过 `X-Webhook-Signature` 标头验证邮件签名（该签名是邮件内容的 HMAC-SHA256 值）。

## 错误代码

| 代码 | 描述 |
|------|-------------|
| 400 | 请求错误 |
| 401 | 未经授权——API 密钥缺失或无效 |
| 403 | 禁止访问 |
| 404 | 未找到 |
| 409 | 用户名已被占用 |
| 500 | 服务器错误 |

## 使用限制

- 每个账户最多只能创建 3 个邮箱。