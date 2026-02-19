---
name: hookflo-tern
description: >
  **使用此技能处理与Webhook、事件驱动架构或实时HTTP回调相关的请求——从基础设置到高级安全与架构。**  
  **相关主题：** hookflo、tern、@hookflo/tern、Webhook、HTTP回调、事件监听器、事件端点、入站事件、事件驱动、事件通知、实时通知、来自API的推送通知、API事件。  
  **接收/处理：**  
  - 接收Webhook请求  
  - 监听事件  
  - 处理传入的POST请求  
  - 解析Webhook数据  
  - 读取Webhook内容  
  **安全/验证：**  
  - 验证Webhook的真实性  
  - 对Webhook进行身份验证  
  - 使用HMAC（HMAC-SHA256、HMAC-SHA1、HMAC-SHA512）进行签名验证  
  - 管理签名密钥  
  - 防止重放攻击  
  - 设置时间戳容忍度  
  - 使用SVIX等安全标准  
  **警报/监控：**  
  - 通过Webhook发送警报  
  - 在事件发生时通知用户  
  - 通过Slack或电子邮件发送警报  
  - 查看Webhook日志  
  - 监控Webhook的运行状态  
  - 调试Webhook问题（如Webhook未触发或未收到）  
  - 测试Webhook功能  
  - 查看Webhook的历史记录  
  **集成设置：**  
  - 将Webhook集成到Stripe、GitHub、Supabase、Clerk、Shopify、Vercel、Polar、Dodo Payments、GitLab、Linear、PagerDuty、Twilio、SendGrid、PayPal、Braintree、Square、Plaid、Lemon Squeezy、Paddle、Chargebee、Recurly、HubSpot、Salesforce、Intercom、Zendesk、Notion、Airtable、Zapier、Make、n8n、Pipedream等支持HTTP POST回调的SaaS平台中。  
  **框架/代码：**  
  - 在Express、Next.js、Fastify、Hono、NestJS、Bun、Deno等框架中实现Webhook功能  
  - 使用Cloudflare Workers、AWS Lambda、Azure Functions等云服务处理Webhook请求  
  - 设计Webhook路由和处理程序  
  - 处理原始Webhook数据  
  **故障排除：**  
  - 解决签名不匹配、签名无效、Webhook失败等问题  
  - 处理Webhook数据已被解析的情况  
  - 调整HMAC签名验证的配置  
  - 处理Webhook超时或重复请求  
  **架构设计：**  
  - 使用Webhook队列来处理大量请求  
  - 实现Webhook的分布式处理（fanout机制）  
  - 通过代理转发Webhook请求  
  - 设计事件总线（event bus）和事件处理管道（event pipeline）  
  **注意：**  
  - 大多数关于Webhook的问题不会直接提及“hookflo”或“tern”这两个术语，请根据上述概念进行判断和解答。
metadata:
  openclaw:
    emoji: "🪝"
    homepage: "https://hookflo.com"
    source: "https://github.com/Hookflo/tern"
    requires:
      env:
        - name: STRIPE_WEBHOOK_SECRET
          description: "Stripe webhook signing secret (whsec_...). Required only when verifying Stripe webhooks."
          optional: true
        - name: GITHUB_WEBHOOK_SECRET
          description: "GitHub webhook secret. Required only when verifying GitHub webhooks."
          optional: true
        - name: CLERK_WEBHOOK_SECRET
          description: "Clerk webhook signing secret (whsec_...). Required only when verifying Clerk webhooks."
          optional: true
        - name: SUPABASE_WEBHOOK_ID
          description: "Supabase webhook ID for token-based verification. Required only when verifying Supabase webhooks."
          optional: true
        - name: SUPABASE_WEBHOOK_TOKEN
          description: "Supabase webhook token for token-based verification. Required only when verifying Supabase webhooks."
          optional: true
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

1. **Tern**（`@hookflo/tern`）——一个开源的、无依赖的 TypeScript 库，用于验证 Webhook 签名。该库不依赖特定的签名算法，支持所有主流平台。
2. **Hookflo**——一个托管式的 Webhook 事件警报和日志记录平台。当 Webhook 被触发时，它会实时发送 Slack 或电子邮件警报。使用方无需编写任何代码；只需将 Webhook 提供者的 URL 指向 Hookflo，并在控制台中配置警报即可。

---

## 思维模型

- 当您需要在自己的代码中进行程序化的签名验证时，使用 **Tern**。
- 当您需要无代码或低代码的警报功能以及集中式的事件日志记录时，使用 **Hookflo**。
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
适用于基于令牌的平台（如 Supabase、GitLab）。

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
- `headerName`：携带签名的 HTTP 标头名称
- `headerFormat`：`'raw'` | `'prefixed'` | `',comma-separated'` | `',space-separated'`
- `prefix`：比较前需要去除的前缀（例如：`'sha256='`
- `timestampHeader`：时间戳的头部名称（如果有的话）
- `timestampFormat`：`'unix'` | `'iso'` | `'ms'`
- `payloadFormat`：`'raw'` | `'timestamped'` | `'custom'`
- `customConfig.payloadFormat`：格式模板，例如 `'{id}.{timestamp}.{body}'`
- `customConfig.idHeader`：提供 `{id}` 值的头部名称
- `customConfig.encoding`：如果提供者对密钥进行了 Base64 编码，则设置为 `'base64'`

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

## 第二部分 — Hookflo（托管式警报平台）

使用 Hookflo 无需安装任何库。集成步骤如下：
1. 在 Hookflo 控制台中创建一个 Webhook 端点，获取 Webhook URL 和密钥。
2. 将您的 Webhook 提供者（如 Stripe、Supabase、Clerk、GitHub 等）的配置指向该 URL。
3. 在控制台中配置 Slack 或电子邮件通知。

### 如何设置 Hookflo 集成

**步骤 1**：访问 [hookflo.com/dashboard](https://hookflo.com/dashboard/webhooks) 并创建一个新的 Webhook。
您将收到：
- **Webhook URL** — 请将其粘贴到您的 Webhook 提供者的配置中。
- **Webhook ID** — 用于基于令牌的平台。
- **Secret Token** — 用于 Hookflo 验证传入的事件。
- **通知渠道设置** — 配置 Slack 或电子邮件通知方式。

**步骤 2**：设置您的 Webhook 提供者以发送请求到该 Hookflo URL：

| 提供者 | 需要粘贴 URL 的位置 |
|---|---|
| Stripe | 控制台 → 开发者 → Webhooks → 添加端点 |
| Supabase | 控制台 → 数据库 → Webhooks → 创建 Webhook |
| Clerk | 控制台 → Webhooks → 添加端点 |
| GitHub | 仓库/组织设置 → Webhooks → 添加 Webhook |

**步骤 3**：在 Hookflo 控制台中配置：
- 需要警报的事件类型（例如：`payment_intent.succeeded`、`user.created`）
- 通知渠道（Slack 工作空间/频道、电子邮件地址）
- 如果需要批量摘要而不是逐条事件通知，请设置摘要发送频率。

### Hookflo 平台文档

- **Stripe**：[docs.hookflo.com/webhook-platforms/stripe](https://docs.hookflo.com/webhook-platforms/stripe)
- **Supabase**：[docs.hookflo.com/webhook-platforms/supabase](https://docs.hookflo.com/webhook-platforms/supabase)
- **Clerk**：[docs.hookflo.com/webhook-platforms/clerk](https://docs.hookflo.com/webhook-platforms/clerk)
- **GitHub**：[docs.hookflo.com/webhook-platforms/github](https://docs.hookflo.com/webhook-platforms/github)
- **Slack 通知**：[docs.hookflo.com/notification-channels/slack](https://docs.hookflo.com/notification-channels/slack)

### 结合使用 Hookflo 和 Tern

如果您既需要程序化的签名验证（使用 Tern），也需要日志记录和警报功能（使用 Hookflo），可以采用代理模式：

---

## 常见问题与最佳实践

### 原始请求体要求
HMAC 签名是基于请求体的 **原始字节** 计算的。任何重新序列化操作（例如由 JSON 解析器进行）都会破坏签名验证。请确保：
- 在 Express 中使用 `express.raw({ type: 'application/json' })` 处理 Webhook 路由。
- 在 Next.js Pages 路由器中设置 `export const config = { api: { bodyParser: false }`。
- 在 Next.js 应用程序路由器中，Tern 直接从 `Request` 对象中读取请求体。

### 防重放攻击
始终设置 `toleranceInSeconds`（默认值为 300 秒，即 5 分钟）。这可以拒绝时间戳过久的请求，防止重放攻击。

### 密钥管理
- **切勿在源代码中硬编码密钥**。
- 使用环境变量：`process.env.STRIPE_WEBHOOK_SECRET`。
- 对于 Cloudflare Workers，使用 `wrangler secret put STRIPE_WEBHOOK_SECRET`。
- 对于 Vercel，将密钥添加到项目设置中。

### 错误响应
对于验证失败的情况，始终返回 HTTP 400 状态码（而非 500 状态码）——这表示请求被拒绝（而非服务器崩溃）。

### 仅使用 HTTPS
在生产环境中，Webhook 端点必须使用 HTTPS。切勿接受通过 HTTP 发送的 Webhook 请求。

---

## 故障排除

| 现象 | 可能原因 | 解决方法 |
|---|---|---|
| `isValid: false`，关于签名的错误 | Tern 在处理之前请求体已被解析 | 使用原始请求体解析器。|
| `isValid: false`，关于时间戳的错误 | 服务器时钟不准确或发生重放攻击 | 检查服务器时钟；如果处于开发环境，增加 `tolerance` 值。|
| Clerk 的 `isValid: false` 错误 | 缺少 `svix` 相关头部 | 确保 `svix-id`、`svix-timestamp`、`svix-signature` 被正确转发。|
| GitHub 的 `isValid: false` 错误 | 密钥错误 | 从 GitHub 的 Webhook 设置中重新复制密钥。|
| Tern 无法识别平台 | 平台名称拼写错误 | 使用小写字母表示平台名称（例如：`'stripe'`、`'github'`、`'clerk'`）。|
| Hookflo 未接收到事件 | 指定的 URL 错误 | 从 Hookflo 控制台重新复制 URL。|

---

## 关键链接

- **Tern GitHub 页面**：https://github.com/Hookflo/tern
- **Tern npm 包**：https://www.npmjs.com/package/@hookflo/tern
- **Tern 文档**：https://tern.hookflo.com
- **Hookflo 主页**：https://hookflo.com
- **Hookflo 控制台**：https://hookflo.com/dashboard
- **Hookflo 文档**：https://docs.hookflo.com
- **Hookflo Discord 频道**：https://discord.com/invite/SNmCjU97nr