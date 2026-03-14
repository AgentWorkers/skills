---
name: vantage
description: "**Vantage**——专为Hyperliquid永续期货设计的自主交易代理。信号生成与执行过程在一个循环中完成，完全在用户本地机器上运行，无需依赖云基础设施，购买后无需支付任何额外费用。该工具包含以下功能：  
- 实时信号引擎（用于分析资金利率、市场动量及THORChain的交易量）；  
- 基于Kelly准则的仓位管理功能；  
- 支持EIP-712标准的订单执行；  
- 提供模拟交易模式（便于测试策略）；  
- 具备交易前设置验证功能；  
- 以及利润收割提醒功能（在达到预设收益时自动触发通知）。"
metadata:
  {
    "openclaw": {
      "emoji": "📈",
      "requires": { "bins": ["node"] }
    }
  }
---
# Vantage — HL 自动交易代理

**版本：** 1.0.0  
**作者：** MoreBetter Studios (@morebetterclaw)  
**产品页面：** https://morebetterstudios.com/products

---

## 功能介绍

Vantage 在 Hyperliquid 永续期货上运行一个连续的信号 → 决策 → 执行循环。

```
Every N minutes (configurable)
  Signal Engine  →  funding rates + momentum + THORChain volume
    Decision Layer  →  Qwen (local) | OpenAI | rule-based fallback
      Kelly Sizing  →  live account balance × confidence × fraction
        Hyperliquid  →  signed market order (your private key)
          Profit Alert  →  log when balance exceeds threshold
```

所有市场数据均通过 **公共 API** 获取，无需使用外部 API 密钥。

---

## 设置

```bash
npm install
cp .env.example .env
# Fill in your Hyperliquid private key + wallet address + trading limits
node src/setup-check.js   # validate before going live
```

---

## 使用方法

```bash
# Paper mode (no real orders)
node src/index.js start --paper

# Live trading
node src/index.js start

# Market data
node src/index.js hl-data RUNE
node src/index.js hl-arb BTC ETH RUNE

# Positions
node src/index.js hl-positions --paper
node src/index.js hl-positions 0xYourWallet

# Setup validator
node src/setup-check.js
```

---

## 配置文件（`.env`）

| 变量 | 是否必填 | 默认值 | 说明 |
|---|---|---|---|
| `HYPERLIQUID_PRIVATE_KEY` | 是 | — | 您的 HL 账户私钥 |
| `HYPERLIQUID_WALLET_ADDRESS` | 是 | — | 您的钱包地址 |
| `MAX_POSITION_SIZE_USD` | 是 | 500 | 每个头寸的最大金额限制（美元） |
| `MAX_OPEN_POSITIONS` | 是 | 3 | 同时可持有的最大头寸数量 |
| `MAX_ACCOUNT_RISK_PCT` | 是 | 2 | 每笔交易的最大风险占账户余额的比例（%） |
| `KELLY_FRACTION` | 是 | 0.25 | Kelly 系数（0.25 表示保守策略） |
| `CRON INTERVAL_MINUTES` | 是 | 60 | 数据扫描频率（分钟） |
| `OLLAMA_URL` | 否 | — | 本地 Ollama 服务器地址（推荐使用） |
| `OLLAMA_MODEL` | 否 | qwen3.5:35b | Ollama 模型 |
| `OPENAI_API_KEY` | 否 | — | OpenAI 作为备用选项 |
| `PROFIT_SWEEP_ENABLED` | 否 | false | 是否启用利润收割提醒 |
| `PROFIT_SWEEP_THRESHOLD_USD` | 否 | 100 | 利润收割触发金额（美元） |

---

## 跨链资金转移

- **加密货币兑换代理** — [链接待更新]  
- **THORChain 交换网站** — [链接待更新]

_(MoreBetter Studios 产品 — morebetterstudios.com/products)_