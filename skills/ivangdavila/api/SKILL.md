---
name: API (Stripe, OpenAI, Notion & 100+ more)
slug: api
version: 1.3.4
homepage: https://clawic.com/skills/api
description: 147项服务的REST API参考。包括认证方式、端点、速率限制以及常见的问题与注意事项。
changelog: Documentation-only skill with API reference files.
metadata: {"clawdbot":{"emoji":"🔌","requires":{"anyBins":["curl","jq"]},"os":["linux","darwin","win32"]}}
---
# API

本文档提供了REST API的参考信息，涵盖了147个服务，包括认证机制、API端点以及使用过程中需要注意的事项。

## 设置

首次使用时，请阅读`setup.md`以获取使用指南。

## 适用场景

当用户需要集成第三方API时，本文档可提供以下帮助：
- 认证相关的文档
- 带有curl示例的API端点参考
- 速率限制和分页策略
- 需避免的常见错误

## 架构

```
apis/                    # API reference files by category
  ├── ai-ml.md           # OpenAI, Anthropic, Cohere, etc.
  ├── payments.md        # Stripe, PayPal, Square, etc.
  ├── communication.md   # Twilio, SendGrid, Slack, etc.
  └── ...

~/api/                   # User preferences (optional)
  └── preferences.md     # Preferred language for examples
```

## 快速参考

| 文件 | 用途 |
|------|---------|
| `setup.md` | 使用指南 |
| `credentials.md` | 多账户凭证命名规则（格式为`{SERVICE}_{ACCOUNT}_{TYPE}`） |
| `auth.md` | 认证方式 |
| `pagination.md` | 分页策略 |
| `resilience.md` | 错误处理机制 |
| `webhooks.md` | Webhook配置指南 |

## API分类

| 分类 | 文件 | 支持的服务 |
|----------|------|----------|
| AI/ML | `apis/ai-ml.md` | anthropic, openai, cohere, groq, mistral, perplexity, huggingface, replicate, stability, elevenlabs, deepgram, assemblyai, together, anyscale |
| 支付 | `apis/payments.md` | stripe, paypal, square, plaid, chargebee, paddle, lemonsqueezy, recurly, wise, coinbase, binance, alpaca, polygon |
| 通信 | `apis/communication.md` | twilio, sendgrid, mailgun, postmark, resend, mailchimp, slack, discord, telegram, zoom |
| 实时通信 | `apis/realtime.md` | sendbird, stream-chat, pusher, ably, onesignal, courier, knock, novu |
| 客户关系管理（CRM） | `apis/crm.md` | salesforce, hubspot, pipedrive, attio, close, apollo, outreach, gong |
| 营销 | `apis/marketing.md` | drift, crisp, front, customer-io, braze, iterable, klaviyo |
| 开发者工具 | `apis/developer.md` | github, gitlab, bitbucket, vercel, netlify, railway, render, fly, digitalocean, heroku, cloudflare, circleci, pagerduty, launchdarkly, split, statsig |
| 数据库 | `apis/database.md` | supabase, firebase, planetscale, neon, upstash, mongodb, fauna, xata, convex, appwrite |
| 认证服务 | `apis/auth-providers.md` | clerk, auth0, workos, stytch |
| 媒体处理 | `apis/media.md` | cloudinary, mux, bunny, imgix, uploadthing, uploadcare, transloadit, vimeo, youtube, spotify, unsplash, pexels, giphy, tenor |
| 社交媒体 | `apis/social.md` | twitter, linkedin, instagram, tiktok, pinterest, reddit, twitch |
| 生产力工具 | `apis/productivity.md` | notion, airtable, google-sheets, google-drive, google-calendar, dropbox, linear, jira, asana, trello, monday, clickup, figma, calendly, cal, loom, typeform |
| 商业服务 | `apis/business.md` | shopify, docusign, hellosign, bitly, dub |
| 地理信息 | `apis/geo.md` | openweather, mapbox, google-maps |
| 客户支持 | `apis/support.md` | intercom, zendesk, freshdesk, helpscout |
| 分析工具 | `apis/analytics.md` | mixpanel, amplitude, posthog, segment, sentry, datadog, algolia |

## 如何导航API文件

每个分类文件中包含多个API。请按照以下步骤操作：
1. **先阅读文件顶部的索引**——每个文件都包含一个API名称和行号的索引表。
2. **直接跳转到特定API**——使用索引中的行号来阅读该API的相关内容（通常每段内容包含50-100行）。
3. **示例代码**——部分文件中提供了具体的API使用示例。

## 核心规则

1. **先找到正确的文件**——根据API分类来定位所需的服务。
2. **先阅读索引，再阅读具体内容**——每个文件都有索引，只需阅读你需要的部分。
3. **指定请求头`Content-Type`**——POST/PUT/PATCH请求必须设置`Content-Type: application/json`。
4. **处理速率限制**——检查`X-RateLimit-Remaining`头部信息，并在收到429错误时实现重试机制。
5. **验证响应内容**——有些API虽然返回200状态码，但响应体中可能包含错误信息，因此请检查响应内容。
6. **使用幂等性机制**——在处理支付请求或关键操作时，确保操作的幂等性。

## 常见错误

- POST请求中未设置`Content-Type: application/json`。
- 将API密钥放在URL查询参数中（应使用请求头）。
- 忽略分页功能（大多数API默认每页显示10-25条数据）。
- 对于429或5xx错误没有重试机制。
- 假设HTTP 200状态码就表示请求成功。

## 说明

本文档仅提供API的参考信息，包括：
- API端点信息
- 认证方式
- 可供参考的代码示例

用户需要自行管理他们的API密钥并执行相关操作。

## 外部API

本文档记录了外部API的详细信息。示例端点来自相应的服务提供商（如Stripe、OpenAI等）。

## 相关技能

如果用户需要，可以使用以下命令安装相关工具：
- `clawhub install http`：HTTP请求处理相关技能
- `clawhub install webhook`：Webhook处理相关技能
- `clawhub install json`：JSON数据处理相关技能

## 反馈

- 如果觉得本文档有用，请给它点赞（使用`clawhub star api`）。
- 如需获取最新信息，请使用`clawhub sync`命令。