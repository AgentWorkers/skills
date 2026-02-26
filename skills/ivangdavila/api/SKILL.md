---
name: API (Stripe, OpenAI, Notion & 100+ more)
slug: api
version: 1.3.0
homepage: https://clawic.com/skills/api
description: 将147个REST API与多账户凭证管理系统集成。这些API涵盖了支付、人工智能（AI）、客户关系管理（CRM）、DevOps等多个领域。
changelog: Consolidated 147 APIs into category files for easier discovery.
metadata: {"clawdbot":{"emoji":"🔌","requires":{"anyBins":["curl","jq"]},"os":["linux","darwin","win32"]}}
---
# API

您可以快速集成任何API。这里文档记录了147个API的服务信息，包括认证方式、端点以及使用时的注意事项。

## 设置

首次使用时，请阅读`setup.md`文件以获取集成指南和凭证设置信息。

## 适用场景

当您需要集成第三方API时，本工具可为您提供以下帮助：
- 支持多账户的认证设置
- 提供带有`curl`示例的端点文档
- 指导您了解速率限制、分页规则及使用技巧
- 说明多账户的凭证命名规则

## 架构

```
apis/                    # API reference files by category
  ├── ai-ml.md           # OpenAI, Anthropic, Cohere, etc.
  ├── payments.md        # Stripe, PayPal, Square, etc.
  ├── communication.md   # Twilio, SendGrid, Slack, etc.
  └── ...

~/api/                   # User preferences (created on first use)
  ├── preferences.md     # Default account selection, language
  └── accounts.md        # Registry of configured accounts
```

## 快速参考

| 文件 | 用途 |
|------|---------|
| `setup.md` | 首次使用时的设置指南 |
| `credentials.md` | 多账户凭证管理系统 |
| `memory-template.md` | 用于存储偏好设置的内存模板 |
| `auth.md` | 认证相关的问题与注意事项 |
| `pagination.md` | 分页相关的问题与注意事项 |
| `resilience.md` | 重试机制与错误处理 |
| `webhooks.md` | Webhook的安全使用规范 |

## API分类

| 分类 | 文件 | API列表 |
|----------|------|------|
| AI/ML | `apis/ai-ml.md` | anthropic, openai, cohere, groq, mistral, perplexity, huggingface, replicate, stability, elevenlabs, deepgram, assemblyai, together, anyscale |
| 支付 | `apis/payments.md` | stripe, paypal, square, plaid, chargebee, paddle, lemonsqueezy, recurly, wise, coinbase, binance, alpaca, polygon |
| 通信 | `apis/communication.md` | twilio, sendgrid, mailgun, postmark, resend, mailchimp, slack, discord, telegram, zoom |
| 实时通信 | `apis/realtime.md` | sendbird, stream-chat, pusher, ably, onesignal, courier, knock, novu |
| 客户关系管理 | `apis/crm.md` | salesforce, hubspot, pipedrive, attio, close, apollo, outreach, gong |
| 营销 | `apis/marketing.md` | drift, crisp, front, customer-io, braze, iterable, klaviyo |
| 开发者工具 | `apis/developer.md` | github, gitlab, bitbucket, vercel, netlify, railway, render, fly, digitalocean, heroku, cloudflare, circleci, pagerduty, launchdarkly, split, statsig |
| 数据库 | `apis/database.md` | supabase, firebase, planetscale, neon, upstash, mongodb, fauna, xata, convex, appwrite |
| 认证 | `apis/auth-providers.md` | clerk, auth0, workos, stytch |
| 媒体 | `apis/media.md` | cloudinary, mux, bunny, imgix, uploadthing, uploadcare, transloadit, vimeo, youtube, spotify, unsplash, pexels, giphy, tenor |
| 社交媒体 | `apis/social.md` | twitter, linkedin, instagram, tiktok, pinterest, reddit, twitch |
| 生产力工具 | `apis/productivity.md` | notion, airtable, google-sheets, google-drive, google-calendar, dropbox, linear, jira, asana, trello, monday, clickup, figma, calendly, cal, loom, typeform |
| 商业服务 | `apis/business.md` | shopify, docusign, hellosign, bitly, dub |
| 地理信息 | `apis/geo.md` | openweather, mapbox, google-maps |
| 支持服务 | `apis/support.md` | intercom, zendesk, freshdesk, helpscout |
| 分析工具 | `apis/analytics.md` | mixpanel, amplitude, posthog, segment, sentry, datadog, algolia |

## 如何导航API文件

每个分类文件中包含多个API，文件可能体积较大。**请不要阅读整个文件**。请采用以下高效的方法：
1. **先阅读索引**——每个文件开头都有索引表，列出了API名称及其在文件中的行号。
2. **直接跳转到特定API**——使用行号直接阅读该API的相关内容（通常为50-100行）。
3. **示例工作流程：**
   ```bash
   # 1. Find which file has the API (use API Categories table above)
   # 2. Read just the index (first 20 lines)
   head -20 apis/ai-ml.md
   # 3. Read specific API section using line numbers from index
   sed -n '119,230p' apis/ai-ml.md  # OpenAI starts at line 119
   ```

**重要提示：****切勿阅读整个分类文件。始终使用索引和直接跳转的方法。

## 核心规则

1. **先查阅API文档**——在分类表中找到目标API，然后阅读该文件的索引以定位具体内容。
2. **使用多账户凭证**——凭证的命名格式为`{SERVICE}_{ACCOUNT}_{TYPE}`。例如：`STRIPE_PROD_API_KEY`、`STRIPE_TEST_API_KEY`、`STRIPE_CLIENT_ACME_API_KEY`。
3. **务必添加`Content-Type`头**——POST/PUT/PATCH请求需要添加`Content-Type: application/json`。省略此头会导致许多API返回415错误。
4. **主动处理速率限制**——监控`X-RateLimit-Remaining`头信息。在达到速率限制前主动减速请求，不要等到收到429错误。同时遵守`Retry-After`头信息。
5. **验证响应结构**——某些API虽然返回200状态码，但响应体中可能包含错误信息。请务必检查响应内容。
6. **使用幂等性标识**——对于支付和关键操作，添加幂等性标识以防止重复请求导致重复收费/操作。
7. **切勿记录凭证信息**——直接使用环境变量存储凭证，切勿将凭证内容输出到日志或文件中。

## 凭证管理

请使用以下命名规则通过环境变量管理凭证：

```bash
# Set for current session
export STRIPE_PROD_API_KEY="sk_live_xxx"

# Use in API call
curl https://api.stripe.com/v1/charges -H "Authorization: Bearer $STRIPE_PROD_API_KEY"
```

**命名格式：`{SERVICE}_{ACCOUNT}_{TYPE}`  
- `STRIPE_PROD_API_KEY` — 生产环境凭证  
- `STRIPE_TEST_API_KEY` — 开发环境凭证  
- `STRIPE_CLIENT_ACME_API_KEY` — 客户端项目凭证  

有关凭证的持久化存储方式及多账户管理流程，请参阅`credentials.md`文件。

## 常见问题

- **缺少`Content-Type`头**——POST请求若未添加`Content-Type: application/json`会导致415错误。
- **URL中包含API密钥**——查询参数会记录在访问日志中，务必使用请求头传递密钥。
- **忽略分页功能**——大多数API默认返回10-25条数据，请务必使用分页功能。
- **未处理429错误**——实现带有延迟的重试机制。
- **误将200状态码视为成功**——请检查响应体中的错误信息。
- **未使用幂等性标识**——重复请求可能导致重复收费或操作。
- **硬编码凭证**——请使用环境变量，切勿在源代码中直接编写凭证。

## 外部端点

本文档介绍了如何调用外部API。请求会直接从您的机器发送到API提供者，数据不会被中间代理或存储。

| 提供者 | 基本URL | 认证方式 |
|----------|----------|------|
| 多种API | 详见相应分类文件 | API密钥 / OAuth |

## 安全与隐私

**凭证存储**：凭证存储在环境变量中，命名格式为`{SERVICE}_{ACCOUNT}_{TYPE}`。
**多账户管理**：每个账户使用唯一的环境变量名，避免命名冲突。

**本工具不执行以下操作：**
- 将凭证存储在文件中  
- 代表用户发起请求  
- 向第三方发送数据  
- 代理API请求  

您可以直接控制所有API调用。

## 相关技能

如果用户需要，可以使用`clawhub install <slug>`命令安装以下相关工具：
- `http`：HTTP请求模式与调试工具  
- `webhook`：Webhook处理与安全功能  
- `json`：JSON处理与`jq`工具  

## 反馈建议

- 如对本文档有帮助，请点赞：`clawhub star api`  
- 保持更新：`clawhub sync`