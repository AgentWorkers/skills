---
name: binance-coach
description: AI-powered crypto trading behavior coach for Binance users. Analyzes live portfolio health, detects emotional trading patterns (FOMO, panic selling, overtrading), provides smart DCA recommendations based on RSI + Fear & Greed index, and delivers personalized AI coaching via Claude. Use when a user asks to: analyze their crypto portfolio, get DCA advice, check market conditions (RSI, Fear & Greed, SMA200), review trading behavior/FOMO/panic sells, get AI coaching on their holdings, set price/RSI alerts, learn about crypto concepts (RSI, DCA, SMA200), start a Telegram trading coach bot, or ask anything about their Binance portfolio.
license: MIT
metadata:
  {
    "openclaw": {
      "emoji": "📊",
      "homepage": "https://github.com/UnrealBNB/BinanceCoachAI",
      "requires": { "bins": ["python3", "pip3"] },
      "setup": "scripts/setup.sh",
      "source": {
        "type": "github",
        "repo": "https://github.com/UnrealBNB/BinanceCoachAI",
        "branch": "main",
        "install_path": "~/workspace/binance-coach"
      },
      "security": {
        "api_access": "read-only",
        "no_trading": true,
        "no_withdrawal": true,
        "data_stored": "local .env + local SQLite DB only",
        "network_calls": [
          "api.binance.com (read-only portfolio/market data)",
          "api.alternative.me (Fear & Greed index)",
          "api.anthropic.com (optional, standalone mode only)",
          "api.telegram.org (optional, standalone bot only)"
        ]
      },
      "env_vars": [
        { "name": "BINANCE_API_KEY", "description": "Binance read-only API key.", "required": true, "sensitive": true },
        { "name": "BINANCE_API_SECRET", "description": "Binance read-only API secret for HMAC signing.", "required": true, "sensitive": true },
        { "name": "ANTHROPIC_API_KEY", "description": "Claude API key — standalone mode only, not needed with OpenClaw.", "required": false, "sensitive": true },
        { "name": "TELEGRAM_BOT_TOKEN", "description": "Telegram bot token from @BotFather — standalone bot only.", "required": false, "sensitive": true },
        { "name": "TELEGRAM_USER_ID", "description": "Your Telegram user ID — restricts bot to one authorized user.", "required": false, "sensitive": false },
        { "name": "LANGUAGE", "description": "en or nl. Default: en.", "required": false, "sensitive": false },
        { "name": "RISK_PROFILE", "description": "conservative, moderate, or aggressive. Default: moderate.", "required": false, "sensitive": false },
        { "name": "DCA_BUDGET_MONTHLY", "description": "Monthly DCA budget in USD. Default: 500.", "required": false, "sensitive": false }
      ]
    }
  }
---

# 📊 BinanceCoach

> 这是一款由人工智能驱动的加密货币交易行为辅导工具，可直接连接到您的 Binance 账户。

BinanceCoach 会实时分析您的 Binance 投资组合，识别出诸如“害怕错过机会”（FOMO）和恐慌性抛售等情绪化交易行为，并根据相对强弱指数（RSI）以及“恐惧与贪婪”指数为您提供智能的定期定额投资（DCA）买入建议——所有这些功能都通过您的 OpenClaw 助手来实现。

---

## ✨ 主要功能

| 功能 | 说明 |
|---|---|
| 💼 投资组合健康状况 | 评分范围为 0–100 分，包含投资组合集中度警告及稳定币种检测 |
| 📐 智能定期定额投资 | 每种币种的每周买入金额，根据 RSI 和“恐惧与贪婪”指数进行动态调整（共 25 种组合） |
| 🧠 行为分析 | 识别 FOMO 行为、过度交易指标、恐慌性抛售行为，并跟踪连续交易记录 |
| 📈 市场状况 | 实时价格、RSI 指数、SMA50/200 移动平均线以及每种币种的趋势方向 |
| 😱 恐惧与贪婪指数 | 实时显示指数，并提供买入/持有建议 |
| 🔔 价格警报 | 可设置价格或 RSI 指数警报，触发时立即通知 |
| 📚 教育资源 | 包含 7 个课程：RSI、DCA、SMA200、恐惧与贪婪指数、投资集中度风险及恐慌性抛售行为 |
| 📅 预测 | 提供每种币种 12 个月的定期定额投资累积预测 |

---

## 🚀 快速入门

**使用 OpenClaw 时仅需提供一个凭证：**

```
Binance API key + secret (read-only)
```

> OpenClaw 已内置 Claude 功能，可处理所有消息交互——无需使用 Anthropic 或 Telegram 聊天机器人。

只需输入：“**分析我的投资组合**”或“**设置 BinanceCoach**”，其余操作均由您的助手完成。

---

## 🗣️ 常见问题

- *"分析我的投资组合"*
- *"当前的恐惧与贪婪指数是多少？"*
- *"请为 DOGE 和 ADA 提供定期定额投资建议"*
- *"检查我的交易行为"*
- *"如果 BTC 价格跌至 60,000 美元以下，请设置警报"*
- *"显示 ETH 的市场状况"*
- *"请预测 BTC 12 个月的定期定额投资结果"*
- *"解释一下定期定额投资（DCA）的原理"*

---

## 🔐 安全性

- **仅使用 Binance 的只读 API**——无法进行任何交易或提款操作 |
- 保密信息仅存储在 `~/workspace/binance-coach/.env` 文件中 |
- `.env` 文件被 Git 忽略，不会被提交到代码仓库 |
- 源代码完全公开透明：[github.com/UnrealBNB/BinanceCoachAI](https://github.com/UnrealBNB/BinanceCoachAI)

详细的安全性指南请参阅 [SECURITY.md](SECURITY.md)。

---

## ⚙️ 可选：独立使用的 Telegram 聊天机器人

如果您希望拥有一个独立的 Telegram 聊天机器人（与 OpenClaw 分离使用）：

1. 通过 [@BotFather](https://t.me/BotFather) 创建一个新的聊天机器人 |
2. 从 [@userinfobot](https://t.me/userinfobot) 获取您的 Telegram 用户 ID |
3. 告诉您的 OpenClaw 助手：“**为 BinanceCoach 设置 Telegram 聊天机器人**”

助手会请求您的 Telegram 用户 ID 和相关权限，随后会为您启动聊天机器人。

---

## 🌍 语言支持

支持 **英语** 和 **荷兰语（Nederlands）**。您可以随时切换语言：

> *"将 BinanceCoach 切换为荷兰语"*

---

*本工具专为 Binance OpenClaw AI 助手项目 2026 年度活动开发 · [查看源代码](https://github.com/UnrealBNB/BinanceCoachAI)*

---

<!-- 代理使用说明 — 请参阅 references/agent-guide.md 以获取完整的使用指南