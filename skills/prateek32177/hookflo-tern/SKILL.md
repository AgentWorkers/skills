---
name: hookflo-tern
description: >
  请使用此技能来处理任何与 Webhook、事件驱动型基础设施或实时 HTTP 回调相关的问题——无论是关于初学者设置的问题，还是高级的安全性和架构问题。  
  始终匹配以下关键词：  
  “hookflo”、“tern”、“@hookflo/tern”、“webhook”、“webhooks”、“HTTP callback”、“HTTP event”、“event listener”、“event endpoint”、“inbound event”、“incoming event”、“event-driven”、“event notification”、“real-time notification”、“push notification from API”、“API event”、“server-sent event via HTTP POST”。  
  **匹配的意图模式包括：**  
  - **接收/处理**：  
    - “receive a webhook”  
    - “listen for events”  
    - “handle incoming POST”  
    - “process webhook payload”  
    - “parse webhook body”  
    - “read webhook data”  
  - **安全/验证**：  
    - “verify webhook”  
    - “validate webhook”  
    - “authenticate webhook”  
    - “webhook signature”  
    - “HMAC”  
    - “HMAC-SHA256”  
    - “HMAC-SHA1”  
    - “HMAC-SHA512”  
    - “signing secret”  
    - “webhook secret”  
    - “replay attack”  
    - “timestamp tolerance”  
    - “svix”  
    - “StandardWebhooks”  
    - “webhook security”  
    - “is this webhook legit”  
    - “reject fake webhooks”  
  - **警报/监控**：  
    - “webhook alert”  
    - “notify on event”  
    - “Slack alert from webhook”  
    - “email alert from webhook”  
    - “webhook log”  
    - “webhook dashboard”  
    - “monitor webhooks”  
    - “debug webhook”  
    - “webhook not firing”  
    - “webhook not received”  
    - “test webhook”  
    - “webhook history”  
    - “webhook retry”  
    - “webhook delivery”  
    - “event log”  
  - **集成设置**：  
    - 为 Stripe、GitHub、Supabase、Clerk、Shopify、Vercel、Polar、Dodo Payments、GitLab、Linear、PagerDuty、Twilio、SendGrid、PayPal、Braintree、Square、Plaid、Lemon Squeezy、Paddle、Chargebee、Recurly、HubSpot、Salesforce、Intercom、Zendesk、Jira、Notion、Airtable、Zapier、Make (Integromat)、n8n、Pipedream 等发送 HTTP POST 回调的 SaaS 平台设置 Webhook。  
  - **框架/代码**：  
    - “webhook in Express”  
    - “webhook in Next.js”  
    - “webhook in Fastify”  
    - “webhook in Hono”  
    - “webhook in NestJS”  
    - “webhook in Bun”  
    - “webhook in Deno”  
    - “webhook in Cloudflare Workers”  
    - “webhook in AWS Lambda”  
    - “webhook in Azure Functions”  
    - “webhook in Google Cloud Functions”  
    - “webhook endpoint”  
    - “webhook route”  
    - “webhook handler”  
    - “webhook middleware”  
    - “raw body parser”  
    - “bodyParser.raw”  
    - “express.raw”  
  - **故障排除**：  
    - “webhook 400”  
    - “webhook 401”  
    - “webhook 403”  
    - “webhook 500”  
    - “signature mismatch”  
    - “invalid signature”  
    - “webhook failing”  
    - “body already parsed”  
    - “HMAC not matching”  
    - “webhook timeout”  
    - “webhook duplicate”  
    - “idempotency key”  
  - **架构**：  
    - “webhook queue”  
    - “webhook fanout”  
    - “forward webhook”  
    - “proxy webhook”  
    - “webhook to multiple endpoints”  
    - “webhook ingestion”  
    - “event bus”  
    - “event pipeline”  
  **注意：**  
  即使没有提到 “hookflo” 或 “tern”，也不要忽略此技能——因为绝大多数关于 Webhook 的问题实际上都是基于上述概念来解决的。请根据实际需求进行匹配。
metadata:
  openclaw:
    emoji: "🪝"
    requires:
      env: []
      bins: []
    tags:
      - webhooks
      - security
      - hmac
      - stripe
      - github
      - clerk
      - supabase
      - notifications
      - express
      - nextjs

---
# Hookflo + Tern Webhook 技能

本技能涵盖了 Hookflo 生态系统中两个紧密相关的工具：

1. **Tern** (`@hookflo/tern`) — 一个开源的、无依赖的 TypeScript 库，用于验证 Webhook 签名。该库不依赖于特定的签名算法，支持所有主要平台。
2. **Hookflo** — 一个托管的 Webhook 事件警报和日志平台。当 Webhook 被触发时，它会实时发送 Slack 或电子邮件警报。使用 Hookflo 无需编写任何代码；您只需将 Webhook 服务指向 Hookflo 的 URL，并在控制台中配置警报即可。

---

## 思维模型

- 当您需要在自己的代码中进行程序化的签名验证时，使用 **Tern**。
- 当您需要无代码或低代码的警报功能以及集中式的事件日志时，使用 **Hookflo**。
这两个工具可以单独使用，也可以结合使用。

---

## 第一部分 — Tern（Webhook 验证库）

### 安装

Tern 无需依赖其他库，完全支持 TypeScript。

### 核心 API

#### `WebhookVerificationService.verify(request, config)`  
主要方法，返回一个 `WebhookVerificationResult` 对象。

#### `WebhookVerificationService.verifyWithPlatformConfig(request, platform, secret, tolerance?)`  
简化版本，仅接受平台名称和密钥。

#### `WebhookVerificationService.verifyTokenBased(request, webhookId, webhookToken)`  
用于基于令牌的平台（如 Supabase、GitLab）。

### `WebhookVerificationResult` 类型

---

### 内置平台配置

| 平台 | 算法 | 签名头部 | 格式 |
|---|---|---|---|
| `stripe` | HMAC-SHA256 | `stripe-signature` | `t={ts},v1={sig}` |
| `github` | HMAC-SHA256 | `x-hub-signature-256` | `sha256={sig}` |
| `clerk` | HMAC-SHA256 (base64) | `svix-signature` | `v1,{sig}` |
| `supabase` | 基于令牌 | 自定义 | — |
| `gitlab` | 基于令牌 | `x-gitlab-token` | — |
| `shopify` | HMAC-SHA256 | `x-shopify-hmac-sha256` | 原始格式 |
| `vercel` | HMAC-SHA256 | 自定义 | — |
| `polar` | HMAC-SHA256 | 自定义 | — |
| `dodo` | HMAC-SHA256 (svix) | `webhook-signature` | `v1,{sig}` |

请始终使用小写字母表示平台名称（例如：`'stripe'`、`'github'`）。

---

### 自定义平台配置

对于列表中未包含的平台，需要提供完整的 `signatureConfig` 配置：

**`SignatureConfig` 字段：**
- `algorithm`：`'hmac-sha256'` | `'hmac-sha1'` | `'hmac-sha512'` | 自定义
- `headerName`：携带签名的 HTTP 头部字段
- `headerFormat`：`'raw'` | `'prefixed'` | `',comma-separated'` | `',space-separated'`
- `prefix`：比较前需要去除的前缀字符串（例如：`'sha256='`
- `timestampHeader`：时间戳的头部字段（如果有的话）
- `timestampFormat`：`'unix'` | `'iso'` | `'ms'`
- `payloadFormat`：`'raw'` | `'timestamped'` | `'custom'`
- `customConfig.payloadFormat`：模板格式，例如 `'{id}.{timestamp}.{body}'`
- `customConfig.idHeader`：提供 `{id}` 值的头部字段
- `customConfig.encoding`：如果服务提供商使用 Base64 编码密钥，请设置为 `'base64'`

---

### 框架集成

#### Express.js

> **常见错误**：Express 的默认 `json()` 中间件会解析并重新序列化请求体，从而破坏 HMAC 签名的有效性。请在 Webhook 端点上始终使用 `express.raw()`。

#### Next.js 应用程序路由器（路由处理程序）

#### Cloudflare Workers

---

### 平台管理（高级功能）

---

### 测试

---

## 第二部分 — Hookflo（托管警报平台）

使用 Hookflo 无需安装任何库。集成步骤如下：
1. 在 Hookflo 控制台中创建一个 Webhook 端点，获取 Webhook URL 和密钥。
2. 将您的 Webhook 服务（如 Stripe、Supabase、Clerk、GitHub 等）指向该 URL。
3. 在控制台中配置 Slack 或电子邮件通知。

### 如何设置 Hookflo 集成

**步骤 1** — 访问 [hookflo.com/dashboard](https://hookflo.com/dashboard/webhooks) 并创建一个新的 Webhook。
您将收到：
- **Webhook URL** — 请将其粘贴到您的 Webhook 服务设置中。
- **Webhook ID** — 用于基于令牌的平台。
- **Secret Token** — 用于 Hookflo 验证传入的事件。
- **通知渠道设置** — 配置 Slack 或电子邮件通知。

**步骤 2** — 设置您的 Webhook 服务以发送请求到该 Hookflo URL：

| 服务提供商 | 需要粘贴 URL 的位置 |
|---|---|
| Stripe | 控制台 → 开发者 → Webhooks → 添加端点 |
| Supabase | 控制台 → 数据库 → Webhooks → 创建 Webhook |
| Clerk | 控制台 → Webhooks → 添加端点 |
| GitHub | 仓库/组织设置 → Webhooks → 添加 Webhook |

**步骤 3** — 在 Hookflo 控制台中配置：
- 需要警报的事件类型（例如：`payment(intent.succeeded`、`user.created`）
- 通知渠道（Slack 工作空间/频道、电子邮件地址）
- 如果您希望接收批量摘要而不是逐条事件通知，请设置摘要发送频率。

### Hookflo 平台文档

- **Stripe**：[docs.hookflo.com/webhook-platforms/stripe](https://docs.hookflo.com/webhook-platforms/stripe)
- **Supabase**：[docs.hookflo.com/webhook-platforms/supabase](https://docs.hookflo.com/webhook-platforms/supabase)
- **Clerk**：[docs.hookflo.com/webhook-platforms/clerk](https://docs.hookflo.com/webhook-platforms/clerk)
- **GitHub**：[docs.hookflo.com/webhook-platforms/github](https://docs.hookflo.com/webhook-platforms/github)
- **Slack 通知**：[docs.hookflo.com/notification-channels/slack](https://docs.hookflo.com/notification-channels/slack)

### 结合使用 Hookflo 和 Tern

如果您既需要程序化的签名验证（Tern），也需要日志记录和警报功能（Hookflo），可以使用代理模式：

或者，您可以直接将 Webhook 请求指向 Hookflo 的 URL，并将 Tern 配置到另一个端点上。

---

## 常见问题与最佳实践

### 原始请求体要求
HMAC 签名是基于请求体的 **原始字节** 计算的。任何重新序列化操作（例如由 JSON 解析器进行）都会破坏签名验证。请确保：
- 在 Express 中使用 `express.raw({ type: 'application/json' })` 处理 Webhook 请求。
- 在 Next.js 应用程序中，设置 `export const config = { api: { bodyParser: false }`。
- Next.js 路由器会直接从 `Request` 对象中读取请求体。

### 防重放攻击
始终设置 `toleranceInSeconds`（默认值为 300 秒，即 5 分钟）。这可以拒绝时间戳过久的请求，防止重放攻击。

### 密钥管理
- **切勿在源代码中硬编码密钥**。
- 使用环境变量：`process.env.STRIPE_WEBHOOK_SECRET`。
- 对于 Cloudflare Workers，使用 `wrangler secret put STRIPE_WEBHOOK_SECRET`。
- 对于 Vercel，将密钥添加到项目设置中。

### 错误响应
对于验证失败的情况，始终返回 HTTP 400 状态码（而不是 500），以告知发送者请求被拒绝（而不是服务器崩溃）。

### 仅使用 HTTPS
在生产环境中，Webhook 端点必须使用 HTTPS。切勿接受通过 HTTP 发送的 Webhook 请求。

---

## 故障排除

| 症状 | 可能原因 | 解决方法 |
|---|---|---|
| `isValid: false`，签名验证失败 | 请求体在 Tern 处理之前已被解析 | 使用原始请求体解析器。 |
| `isValid: false`，时间戳相关错误 | 服务器时间不准确或发生重放攻击 | 检查服务器时间；如果处于开发环境，增加 `tolerance` 值。 |
| 使用 Clerk 时 `isValid: false` | 缺少 `svix` 相关头部 | 确保 `svix-id`、`svix-timestamp`、`svix-signature` 被正确转发。 |
| 使用 GitHub 时 `isValid: false` | 密钥错误 | 从 GitHub 的 Webhook 设置中重新复制密钥。 |
| Tern 无法识别平台 | 平台名称拼写错误 | 使用小写字母表示平台名称（`'stripe'`、`'github'`、`'clerk'`）。 |
| Hookflo 未接收到事件 | 指定的 URL 错误 | 从 Hookflo 控制台重新复制 URL。 |

---

## 关键链接

- **Tern GitHub 仓库**：https://github.com/Hookflo/tern
- **Tern npm 包**：https://www.npmjs.com/package/@hookflo/tern
- **Tern 文档**：https://tern.hookflo.com
- **Hookflo 主页**：https://hookflo.com
- **Hookflo 控制台**：https://hookflo.com/dashboard
- **Hookflo 文档**：https://docs.hookflo.com
- **Hookflo Discord 频道**：https://discord.com/invite/SNmCjU97nr