---
name: linkedin-post-generator
description: 一款由人工智能驱动的 LinkedIn 帖子生成工具，专为专业人士设计。通过使用 Sloan Agent，您可以轻松创建引人入胜的帖子、具有思想引领力的内容以及职业发展相关的更新。
version: 1.0.7
author: Matt
tags:
  - linkedin
  - professional
  - content-generation
  - social-media
pricing:
  type: pay-per-use
  price: 0.002
  currency: USDT
  payment_provider: skillpay.me
---
# LinkedIn 帖子生成器

生成能够吸引互动的专业 LinkedIn 帖子，非常适合专业人士、思想领袖和求职者使用。

## 特点

- **专业语气**：使用符合行业规范的语言
- **吸引注意的开头**：能够抓住读者的注意力
- **多种类型**：普通帖子、思想领袖类帖子、庆祝帖子、公告类帖子
- **号召行动**：鼓励读者发表评论和分享

## 使用方法

```bash
# Generate a LinkedIn post
linkedin-post-generator "career growth tips"

# Generate a thought leadership post
linkedin-post-generator "AI trends" --type thought-leadership

# Generate a celebration post
linkedin-post-generator "got promoted" --type celebration
```

## 选项

| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `--tone` | 语气（专业、随意、鼓舞人心） | professional |
| `--type` | 帖子类型（普通、思想领袖、庆祝、公告） | general |
| `--no-emoji` | 禁用表情符号 | - |
| `--no-hashtags` | 禁用标签 | - |

## 价格

- **按使用次数计费**：每次生成帖子收费 0.002 美元（USDT）

## 环境变量

| 变量 | 描述 | 是否必需 |
|----------|-------------|----------|
| `SKILLPAY_MERCHANT_KEY` | 支付商密钥（可选，默认使用内置密钥） | 否 |
| `OPENCLAW_GATEWAY_TOKEN` | 用于本地 API 替代的网关认证令牌 | 否 |

## 系统要求

- 需要安装带有 Sloan 代理（AI 写作工具）的 OpenClaw 工具
- OpenClaw Gateway 需要运行在本地（作为 API 替代方案）

## 关于 Sloan

Sloan 是您的 AI 写作助手——一位专注于在 LinkedIn 上创作专业内容、分享思想领袖观点的专业内容创作者。

## 支持方式

- GitHub：https://github.com/icepopma/linkedin-post-generator
- Discord：https://discord.gg/clawd
- 电子邮件：icepopma@hotmail.com

## 许可证

MIT © Matt