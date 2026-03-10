---
name: binance-coach
description: AI-powered crypto trading behavior coach for Binance users. Analyzes live portfolio health, detects emotional trading patterns (FOMO, panic selling, overtrading), provides smart DCA recommendations based on RSI + Fear & Greed index, and delivers personalized AI coaching via Claude. Use when a user asks to: analyze their crypto portfolio, get DCA advice, check market conditions (RSI, Fear & Greed, SMA200), review trading behavior/FOMO/panic sells, get AI coaching on their holdings, set price/RSI alerts, learn about crypto concepts (RSI, DCA, SMA200), start a Telegram trading coach bot, or ask anything about their Binance portfolio.
license: MIT
homepage: https://github.com/UnrealBNB/BinanceCoachAI
metadata: {"openclaw":{"emoji":"📊","homepage":"https://github.com/UnrealBNB/BinanceCoachAI","requires":{"bins":["python3","pip3"],"env":["BINANCE_API_KEY","BINANCE_API_SECRET"]},"primaryEnv":"BINANCE_API_KEY","install":[{"id":"setup","kind":"download","url":"https://github.com/UnrealBNB/BinanceCoachAI/archive/refs/heads/main.zip","label":"Download BinanceCoach source (then run scripts/setup.sh)"}]}}
---

# 📊 BinanceCoach

> 你的AI驱动的加密货币交易行为教练——直接连接到你的Binance账户。

BinanceCoach会分析你实时的Binance投资组合，识别出诸如“害怕错过机会”（FOMO）和恐慌性抛售等情绪化交易行为，并根据RSI指标以及“恐惧与贪婪”指数为你提供智能的定期定额投资（DCA）买入建议——所有这些功能都通过你的OpenClaw助手实现。

---

## ✨ 主要功能

| 功能 | 描述 |
|---|---|
| 💼 投资组合健康状况 | 评分0–100分，包含投资组合集中度警告及稳定币种检查 |
| 📐 智能DCA | 每种货币的每周买入金额，根据RSI和“恐惧与贪婪”指数进行调整（共25种组合） |
| 🧠 行为分析 | FOMO评分、过度交易指数、恐慌性抛售检测器、连续交易记录追踪 |
| 📈 市场状况 | 每种货币的实时价格、RSI指标、SMA50/200移动平均线以及趋势方向 |
| 😱 恐惧与贪婪指数 | 实时指数，附带买入/持有建议 |
| 🔔 价格警报 | 设置价格或RSI警报，可查看触发情况 |
| 📚 教育资源 | 7个课程：RSI、DCA、SMA200、恐惧与贪婪指数、投资集中度风险、恐慌性抛售 |
| 📅 预测 | 每种货币的12个月DCA投资累计预测 |

---

## 🚀 快速入门

**使用OpenClaw时仅需一个凭证：**

```
Binance API key + secret (read-only)
```

> OpenClaw已经内置了Claude功能，可以处理消息传递——无需Anthropic密钥或Telegram机器人。

只需输入：“**分析我的投资组合**”或“**设置BinanceCoach**”，其余工作都由助手完成。

---

## 🗣️ 常见问题

- *"分析我的投资组合"*
- *"当前的恐惧与贪婪指数是多少？"*
- *"给我DOGE和ADA的DCA投资建议"*
- *"检查我的交易行为"*
- *"如果BTC价格跌至60,000美元以下，请设置警报"*
- *"显示ETH的市场状况"*
- *"预测BTC的12个月DCA投资结果"*
- *"解释一下什么是定期定额投资（DCA）"*

---

## 🔐 安全性

- **仅使用Binance的只读API**——无法进行交易或提款 |
- 秘密信息仅存储在`~/workspace/binance-coach/.env`文件中 |
- `.env`文件被Git忽略，不会被提交到代码仓库 |
- 源代码完全公开可审计：[github.com/UnrealBNB/BinanceCoachAI](https://github.com/UnrealBNB/BinanceCoachAI)

详细的安全性指南请参阅[SECURITY.md]文件。

---

## ⚙️ 可选：独立Telegram机器人

想要一个独立的Telegram机器人吗？

1. 通过[@BotFather](https://t.me/BotFather)创建一个新的机器人 |
2. 从[@userinfobot](https://t.me/userinfobot)获取你的Telegram用户ID |
3. 告诉你的OpenClaw助手：“**为BinanceCoach设置Telegram账户**”

助手会请求你的Token和用户ID，然后为你启动相应的Telegram机器人。

---

## 🌍 语言支持

支持**英语**和**荷兰语（Nederlands）**。随时可以切换语言：

> *"将BinanceCoach的语言切换为荷兰语"*

---

*专为2026年Binance OpenClaw AI助手活动开发 · [在GitHub上查看项目](https://github.com/UnrealBNB/BinanceCoachAI)*

---

<!-- 代理使用说明——请参阅references/agent-guide.md以获取完整的操作指南