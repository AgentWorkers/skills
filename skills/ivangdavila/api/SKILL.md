---
name: API (Stripe, OpenAI, Notion & 100+ more)
slug: api
version: 1.2.1
homepage: https://clawic.com/skills/api
description: 将100多个REST API与安全的多账户凭证管理系统集成起来。支持与GitHub、Twilio、Slack、HubSpot、Shopify等服务的集成。
changelog: Multi-account credential system, dynamic API discovery, 100+ documented APIs.
metadata: {"clawdbot":{"emoji":"🔌","requires":{"anyBins":["curl","jq"]},"os":["linux","darwin","win32"]}}
---
# API

您可以快速集成任何API。这里文档记录了100多种服务的相关信息，包括认证方式、接口端点以及使用注意事项。

## 设置

首次使用时，请阅读`setup.md`以获取集成指南和凭证设置信息。

## 使用场景

当您需要集成第三方API时，本技能可提供以下帮助：
- 支持多账户的认证设置
- 提供带有`curl`示例的接口端点文档
- 指导您了解速率限制、分页规则及使用技巧
- 为多个账户制定统一的凭证命名规范

## 架构

```
apis/                    # 100+ API reference files
  ├── stripe.md
  ├── openai.md
  ├── notion.md
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
| `resilience.md` | 重试与错误处理策略 |
| `webhooks.md` | Webhook的安全使用规范 |
| `apis/{service}.md` | 各API的具体文档 |

## 核心规则

1. **先查阅API文档** — 在发起任何请求之前，请务必阅读`apis/{service}.md`文件。该文件会详细说明该服务的认证方式、接口端点、速率限制及相关注意事项。
2. **使用多账户凭证** — 凭证应按照`{SERVICE}_{ACCOUNT}_{TYPE`的格式进行存储。例如：`STRIPE_PROD_API_KEY`、`STRIPE_TEST_API_KEY`、`STRIPE_CLIENT_ACME_API_KEY`。
3. **务必设置`Content-Type`头** — 对于POST/PUT/PATCH请求，必须添加`Content-Type: application/json`。忽略此头会导致许多API返回415错误。
4. **主动监控速率限制** — 关注`X-RateLimit-Remaining`头信息，在达到速率限制前主动限制请求频率，避免收到429错误。同时请遵守`Retry-After`头的设置。
5. **验证响应结构** — 有些API虽然返回200状态码，但响应体中可能包含错误信息。请务必检查响应内容。
6. **使用幂等性键** — 在处理支付或关键操作时，添加幂等性键以防止重复请求导致重复收费。
7. **严禁记录凭证信息** — 请直接使用环境变量来存储凭证，切勿将其输出到日志或文件中。

## 凭证管理

请使用以下多账户命名规范来管理凭证：

```bash
# Set for current session
export STRIPE_PROD_API_KEY="sk_live_xxx"

# Use in API call
curl https://api.stripe.com/v1/charges -H "Authorization: Bearer $STRIPE_PROD_API_KEY"
```

**命名格式：** `{SERVICE}_{ACCOUNT}_{TYPE}`
- `STRIPE_PROD_API_KEY` — 生产环境凭证
- `STRIPE_TEST_API_KEY` — 开发环境凭证
- `STRIPE_CLIENT_ACME_API_KEY` — 客户端项目凭证

有关凭证的持久化存储方式及多账户管理流程，请参阅`credentials.md`。

## 可用的API（共147个）

所有API的文档都存储在`apis/`目录下。API类别包括：

**AI/ML：** anthropic、openai、cohere、groq、mistral、perplexity、huggingface、replicate、stability、elevenlabs、deepgram、assemblyai、together、anyscale

**支付：** stripe、paypal、square、plaid、chargebee、paddle、lemonsqueezy、recurly、wise、coinbase、binance、alpaca、polygon

**通信：** twilio、sendgrid、mailgun、postmark、resend、mailchimp、slack、discord、telegram、zoom、sendbird、stream-chat、pusher、ably、onesignal、courier、knock、novu

**CRM/销售：** salesforce、hubspot、pipedrive、attio、close、apollo、outreach、gong、drift、crisp、front、customer-io、braze、iterable、klaviyo

**开发工具：** github、gitlab、bitbucket、vercel、netlify、railway、render、fly、digitalocean、heroku、cloudflare、circleci、pagerduty、launchdarkly、split、statsig

**数据库/认证：** supabase、firebase、planetscale、neon、upstash、mongodb、fauna、xata、convex、appwrite、clerk、auth0、workos、styutch

**媒体：** cloudinary、mux、bunny、imgix、uploadthing、uploadcare、transloadit、vimeo、youtube、spotify、unsplash、pexels、giphy、tenor

**社交：** twitter、linkedin、instagram、tiktok、pinterest、reddit、twitch

**生产力工具：** notion、airtable、google-sheets、google-drive、google-calendar、dropbox、linear、jira、asana、trello、monday、clickup、figma、calendly、cal、loom、typeform

**其他：** shopify、docusign、hellosign、bitly、openweather、mapbox、google-maps、intercom、zendesk、freshdesk、helpscout、mixpanel、amplitude、posthog、segment、sentry、datadog、algolia

```bash
# List all APIs
ls apis/

# Search by name
ls apis/ | grep -i payment

# Read specific API
cat apis/stripe.md
```

## 常见问题与注意事项

- **未设置`Content-Type`** — 如果POST请求缺少`Content-Type: application/json`，会导致415错误。
- **在URL中直接写入API密钥** — 请通过请求头传递API密钥，避免将其写入查询参数中。
- **忽略分页功能** — 大多数API默认返回10-25条数据，务必使用分页功能。
- **未处理429错误** — 实现带有延迟机制的指数级重试策略。
- **误将200状态码视为成功** — 请检查响应体中的错误信息。
- **未使用幂等性键** — 重复请求可能导致重复收费或操作重复。
- **硬编码凭证** — 请使用环境变量，切勿在源代码中直接编写凭证信息。

## 外部接口

本技能介绍了如何调用外部API。请求会直接从您的机器发送到API提供商，数据不会被中间代理或存储。

| 提供商 | 基本URL | 认证方式 |
|----------|----------|------|
| 多种API | 请参阅`apis/{service}.md` | API密钥 / OAuth |

## 安全与隐私

- 凭证信息存储在环境变量中，遵循`{SERVICE}_{ACCOUNT}_{TYPE`的命名规范。
- 每个账户使用唯一的环境变量名称，以避免命名冲突。
- 本技能**不**执行以下操作：
  - 将凭证存储在文件中
  - 代表用户发起请求
  - 将数据发送给第三方
  - 代理API请求

您可以直接控制所有的API调用。

## 相关技能

如果用户需要，可以使用以下命令安装相关工具：
- `clawhub install http` — 学习HTTP请求模式与调试技巧
- `clawhub install webhook` — 学习Webhook的处理与安全配置
- `clawhub install json` — 学习JSON处理及`jq`工具的使用

## 反馈建议

- 如果本技能对您有帮助，请给它点赞（star）：`clawhub star api`
- 为了获取最新更新，请执行`clawhub sync`命令