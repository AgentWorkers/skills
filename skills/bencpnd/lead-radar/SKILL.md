---
name: Lead Radar
version: 1.3.5
description: 每天早上，我会扫描 Reddit、Hacker News、Indie Hackers、Stack Overflow、Quora、Hashnode、Dev.to、GitHub 和 Lobsters 等平台，寻找那些正在积极询问你所销售产品的人。然后将其中 10 个有购买意向的用户信息，连同预先准备好的回复内容，发送到你的 Telegram 账户。该系统由 Gemini 2.5 Flash 技术支持。
author: bencpnd
category: marketing
tags: [leads, sales, marketing, reddit, prospecting, automation, daily, telegram]
entry: index.js
cron: "0 8 * * *"
channels:
  - telegram
install: "npm install"
config:
  - key: OFFER_DESCRIPTION
    label: "What do you sell? (1-2 sentences)"
    type: text
    required: true
    example: "I sell a CRM tool for freelance designers. Target: freelancers struggling to track clients and invoices."
  - key: LEAD_RADAR_LICENSE_KEY
    label: "License Key (get one at lead-radar.pro)"
    type: secret
    required: true
  - key: TELEGRAM_CHAT_ID
    label: "Your Telegram Chat ID"
    type: text
    required: true
  - key: TELEGRAM_BOT_TOKEN
    label: "Telegram Bot Token (from @BotFather)"
    type: secret
    required: true
trial_days: 3
---
# Lead Radar

**停止冷启动式的营销方式，开始进行暖性的对话吧。**

Lead Radar 每天早上会扫描 9 个社交媒体平台，寻找那些主动询问您所销售产品的人，并将最具购买意向的前 10 个潜在客户直接发送到您的 Telegram 账号中，每个潜在客户都附带一条预先准备好的回复内容。

## 工作原理

1. **您描述您的产品或服务**——例如：“我为自由设计师提供 CRM（客户关系管理）软件。”
2. **Gemini 2.5 Flash 会根据您的业务领域生成合适的关键词。**
3. **系统会扫描 9 个平台（Reddit、Hacker News、Indie Hackers、Stack Overflow、Quora、Hashnode、Dev.to 和 Lobsters）上包含这些关键词的帖子。**
4. **利用人工智能对每个帖子的购买意向进行评分（0-10 分），过滤掉无关信息，只保留真正有购买意向的帖子。**
5. **每天早上 8 点，系统会将前 10 个潜在客户的信息发送到您的 Telegram 账号，内容包括：**
   - 原帖子的标题和摘要
   - 直接链接到相关对话的页面
   - 评分结果及解释
   - 一条您可以复制粘贴的回复内容

## 系统能检测到哪些类型的帖子？

Lead Radar 可以识别以下类型的帖子：
- “正在寻找能够完成某项任务的工具”——表示有明确的购买意向
- “你们是如何处理某问题的？”——表明用户遇到了您的产品可以解决的痛点
- “我们之前使用的是 Z 产品，现在需要替代品”——表示用户正在比较不同产品
- “有什么推荐吗？”——表示用户愿意听取建议

## 数据来源

| 平台 | 数据获取方式 |
|----------|--------|
| Reddit | 通过 API 获取数据，并使用自动切换策略（三种方法） |
| Hacker News | 使用 Algolia 搜索 API |
| Indie Hackers | 通过 Jina 进行网页抓取 |
| Stack Overflow | 使用公开 API |
| Quora | 通过 Jina 进行网页抓取 |
| Hashnode | 使用 GraphQL API |
| Dev.to | 使用公开 API |
| Lobsters | 通过 JSON 数据源获取数据 |

## 数据源健康状况监控

如果某个数据源出现故障（例如被限制访问或暂时不可用），Lead Radar 会：
- 继续正常扫描其他数据源
- 在发送给您的 Telegram 消息中注明哪些数据源出现了问题
- 显示扫描统计信息：扫描了多少帖子以及来自多少个活跃的数据源

## 智能预过滤机制

在运行人工智能评分之前，Lead Radar 会先根据关键词的相关性对帖子进行预过滤。这样只有真正相关的帖子才会被纳入评分范围，确保整个流程的效率（评分时间不超过 60 秒）。人工智能评分功能包含在您的订阅服务中，无需额外购买 API 密钥。

## 设置步骤（2 分钟完成）

### 1. 获取许可证密钥
访问 [lead-radar.pro](https://lead-radar.pro) 开始 3 天的免费试用（之后费用为每月 $9）。您的许可证密钥会立即通过电子邮件发送给您。

### 2. 创建 Telegram 机器人
打开 Telegram，搜索 [@BotFather](https://t.me/BotFather)，发送 `/newbot`，然后按照提示操作。复制机器人提供的令牌（格式类似 `123456:ABC-DEF...`）。

### 3. 获取您的 Telegram 聊天 ID
在 Telegram 中搜索 [@userinfobot](https://t.me/userinfobot)，向其发送任意消息，它会回复您的聊天 ID（例如 `123456789`）。复制该 ID。

### 4. 填写设置信息
在 OpenClaw 中安装该插件后，进入 Lead Radar 的设置页面，填写以下信息：
| 字段 | 需要输入的内容 |
|-------|---------------|
| `LEAD_RADAR_LICENSE_KEY` | 第 1 步中获取的许可证密钥 |
| `TELEGRAM_BOT_TOKEN` | 第 2 步中获取的机器人令牌 |
| `TELEGRAMCHAT_ID` | 第 3 步中获取的聊天 ID |
| `OFFER_DESCRIPTION` | 用 1-2 句话描述您的产品或服务（例如：“我为自由设计师提供 CRM 软件” |

您无需购买额外的 AI API 密钥，因为 Gemini 评分功能已包含在您的订阅服务中。

### 5. 等待早上 8 点
Lead Radar 会每天早上 8 点自动开始扫描。您明天就会收到第一批潜在客户的消息。

## 价格信息

- **3 天免费试用**——可完全使用所有功能，无需支付信用卡费用 |
- **每月 $9**——您可以在 [billing.stripe.com/p/login/3cI4gy83O4xoaKp431bZe00](https://billing.stripe.com/p/login/3cI4gy83O4xoaKp431bZe00) 注销订阅。

## 常见问题解答

**我每天能收到多少个潜在客户？**
这取决于您的业务领域。大多数用户每天能收到 3-10 个具有购买意向的潜在客户。业务领域较宽的用户（如项目管理）收到的潜在客户数量更多；而业务领域较窄的用户（如宠物美容师使用的 CRM 软件）收到的潜在客户数量较少，但质量更高。

**我可以自定义扫描时间吗？**
默认扫描时间为每天早上 8 点。您可以在 OpenClaw 的配置中更改定时任务。

**如果 Reddit 封锁了我的 IP 地址怎么办？**
Lead Radar 为 Reddit 设计了三种数据获取策略。如果一种方法被封锁，系统会自动切换到另一种方法。如果某个数据源出现故障，系统会通过 Telegram 通知您。

**哪些数据会离开我的设备？**
Lead Radar 通过 OpenClaw 在您的设备上运行，但依赖外部服务来完成数据获取。它执行的操作包括：
- **数据来源平台**：从 Reddit (old.reddit.com, Pullpush.io)、Hacker News (Algolia API)、Indie Hackers & Quora (r.jina.ai 代理)、Stack Overflow (Stack Exchange API)、Hashnode (GraphQL API)、Dev.to (公开 API) 和 Lobsters (JSON 数据源) 获取公开可用的帖子。这些请求均为只读操作，不会包含任何用户凭证或个人数据。
- **许可证服务器**：验证您的 `LEAD_RADAR_license_KEY`，并返回由供应商提供的 `GEMINI_API_KEY`（用户无需自行提供 API 密钥）。只有您的许可证密钥会被发送到许可证服务器，您的产品描述不会被发送。
- **Google Gemini API**：使用供应商提供的 API 密钥，将您的产品描述和帖子摘要发送给 Google 的生成式人工智能进行评分。这意味着您的产品描述和抓取的帖子内容会在供应商的 API 账户下由 Google 处理。
- **Telegram API**：使用您的 `TELEGRAM_BOT_TOKEN` 将每日潜在客户信息发送到您的 Telegram 账号。

**通过安装和运行 Lead Radar，您同意：**
- 您的产品描述和抓取的帖子摘要会被发送到 Google 的 Gemini API 进行评分；
- 每次运行时，您的许可证密钥会在我们的许可证服务器上进行验证；
- 您的潜在客户信息会被发送到 Telegram API。

请注意：所有必要的敏感信息（许可证密钥、机器人令牌、聊天 ID 和产品描述）都仅存储在您的 OpenClaw 环境中，不会被发送到任何远程服务器。