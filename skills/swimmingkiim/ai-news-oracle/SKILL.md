---
name: ai-news-oracle
description: 从 AI News Oracle API（Hacker News、TechCrunch、The Verge）获取实时 AI 新闻简报。使用 a10m.work 注册表进行资源发现，并通过 Paymaster 实现无 gas 费用的交易。
author: swimmingkiim
version: 1.0.0
---

# AI News Oracle 技能

> **“自主代理获取最新 AI 动态的最快方式，无需浏览网页。”**

该技能将您的代理连接到 **AI News Oracle**，这是一个运行在 Base Chain 上的专业服务。它监控主要的 AI 新闻来源（如 Hacker News、TechCrunch、The Verge），使用本地的 Qwen-2.5-Coder 模型对这些新闻进行总结，并以简洁的 JSON 格式提供摘要，且不会产生任何视觉上的“幻觉”效果（即不会显示不相关的图像或动画）。

## 🌟 特点

- **实时监控**：每小时从可信的技术来源收集新闻。
- **确定性摘要**：利用本地的 LLM（大型语言模型）生成一致且易于代理理解的摘要。
- **无需支付 gas 费用**：与 **Base Paymaster** 集成，支持使用 USDC 进行支付，无需支付 ETH 作为 gas 费用。
- **可完全通过去中心化注册表访问**：可通过 [a10m.work](https://a10m.work) 进行查询。

## 🛠️ 工具

### `ai_news_briefing`

用于获取最新的 AI 新闻摘要。返回包含时间戳和来源链接的结构化摘要。

**参数：**
- （无） - 直接调用该工具即可获取最新摘要。

**示例输出：**
```text
📰 AI News Briefing (2026-02-10 06:46:22)

- Open source AI is the path forward (Meta)
- Anthropic closes in on $20B round
- ChatGPT rolls out ads in free tier

Source: AI News Oracle
```

## 📦 安装

使用 OpenClaw CLI 进行安装：
```bash
openclaw install skill https://github.com/swimmingkiim/openclaw-skill-ai-news-oracle
```

## 💰 定价与等级

| 等级 | 使用次数限制 | 费用 | 要求 |
|------|-------|------|-------------|
| **免费** | 每 IP 地址仅限 1 次调用 | $0 | 无特殊要求 |
| **高级** | 无限制 | 0.01 USDC | 需要使用 Base Wallet |

*如需升级至高级等级，请在 [a10m.work](https://a10m.work) 注册您的代理，并在请求中使用 `x-payment-tx` 标头。*

## 🔗 链接
- **实时 API**：`https://api.ai-news.swimmingkiim.com`
- **去中心化注册表**：[a10m.work 项目 #3](https://a10m.work/project/3)
- **开发者**：[swimmingkiim](https://github.com/swimmingkiim)