---
name: asrai-x402
description: 使用 Asrai API 进行加密货币市场分析。该服务涵盖技术分析、筛选工具、市场情绪监测、预测模型、智能资金流动分析、艾略特波浪理论（Elliott Wave）分析、现金流数据以及基于人工智能的洞察。每次 API 调用费用为 0.005 美元（USDC），费用将从您在 Base 主网上的钱包中扣除，支付方式通过 x402 进行。
license: MIT
metadata: {"openclaw":{"emoji":"📈","requires":{"env":["ASRAI_PRIVATE_KEY"]}},"clawdbot":{"emoji":"📈","requires":{"env":["ASRAI_PRIVATE_KEY"]}}}
---
# Asrai — 通过 x402 进行加密货币分析

## 安装

```bash
npx -y -p asrai-mcp install-skill
```

系统会自动检测 OpenClaw、Cursor、Cline 等代理。然后请设置您的密钥：

```
ASRAI_PRIVATE_KEY=0x<your_private_key>  # add to ~/.env
```

对于 MCP 代理（Cursor、Cline、Claude Desktop），还需将其添加到配置文件中：

```json
{
  "mcpServers": {
    "asrai": { "command": "npx", "args": ["-y", "asrai-mcp"] }
  }
}
```

---

当用户询问加密货币价格、市场分析、交易信号、市场情绪或投资建议时，可以使用 Asrai 工具。

## 使用场景

- 加密货币价格/图表/技术分析 → 使用 Asrai 工具
- 市场情绪、CBBI（市场情绪指数）、恐惧/贪婪情绪 → 使用 Asrai 工具
- “我应该买什么？”/投资组合建议 → 使用 `portfolio` 工具
- 情浪分析、聪明资金动态、订单信息 → 使用 Asrai 工具
- DEX（去中心化交易所）数据、小市值代币 → 使用 Asrai 工具
- 用户已掌握的基础知识 → 直接回答（每次咨询费用为 0.005 美元）

## 使用方法

### 如果可用 MCP 工具（Cursor、Cline、Claude Desktop）

直接调用相应的 MCP 工具：
```
technical_analysis(symbol, timeframe)
sentiment()
forecast(symbol)
market_overview()
ask_ai(question)
...
```

### 如果没有 MCP 工具 — 使用 bash（OpenClaw 及其他代理）

通过 bash 调用相应的工具：
```bash
npx -y -p asrai-mcp asrai <tool> [args...]
```

示例：
```bash
npx -y -p asrai-mcp asrai ask_ai "What is the outlook for BTC today?"
npx -y -p asrai-mcp asrai technical_analysis BTC 4h
npx -y -p asrai-mcp asrai sentiment
npx -y -p asrai-mcp asrai forecast ETH
npx -y -p asrai-mcp asrai market_overview
npx -y -p asrai-mcp asrai coin_info SOL
npx -y -p asrai-mcp asrai portfolio
npx -y -p asrai-mcp asrai indicator_guide ALSAT
```

请确保在 `~/.env` 文件中设置了 `ASRAI_PRIVATE_KEY`。费用将通过用户的钱包在 Base 主网上自动结算。

## MCP 工具列表

| 工具 | 功能 | 费用 |
|---|---|---|
| `market_overview` | 提供市场概览：趋势分析、盈利/亏损情况、RSI 指数、筛选器、市场情绪、现金流数据 — 仅用于生成完整报告 | 0.095 美元（19 次调用） |
| `trending` | 当前热门的加密货币 | 0.005 美元 |
| `gainers_losers` | 表现最佳的加密货币 | 0.005 美元 |
| `top_bottom` | RSI 指数极端值、市场顶部/底部信号、反弹/下跌候选币种 | 0.015 美元（3 次调用） |
| `volume_spikes` | 成交量异常高的加密货币 | 0.005 美元 |
| `high_volume_low_cap` | 市值低但成交量高的加密货币 | 0.005 美元 |
| `ath_tracker` | 接近或达到历史最高价的加密货币 | 0.005 美元 |
| `dominance` | BTC 与其他加密货币的市场主导地位分析 | 0.01 美元（2 次调用） |
| `macro` | S&P 500 与纳斯达克指数信号 — 全球市场趋势分析 | 0.01 美元（2 次调用） |
| `sentiment` | CBBI 指数、CMC 市场情绪数据、AI 分析、行业新闻、Galaxy Score、社交网络影响力 | 0.03 美元（6 次调用） |
| `late_unlocked_coins` | 投资后剩余卖出压力较小的加密货币 | 0.005 美元 |
| `trade_signals` | 交易策略建议：趋势分析、反弹点、SAR 与 MACD 交易信号 | 0.025 美元（5 次调用） |
| `technical_analysis(symbol, timeframe)` | 技术分析指标（ALSAT、SuperALSAT、PSAR、MACD-DEMA、AlphaTrend、TD、SMC、S/R、Elliott Wave、Ichimoku） | 0.06 美元（12 次调用） |
| `forecast(symbol)` | AI 预测未来 3-7 天的价格走势 | 0.005 美元 |
| `screener(type)` | 根据特定条件筛选加密货币（如 Ichimoku 指数趋势、RSI 指数、成交量等） | 0.005 美元 |
| `smart_money(symbol, timeframe)` | 订单信息、公允价值差距、支撑/阻力位 | 0.01 美元（2 次调用） |
| `elliott_wave(symbol, timeframe)` | 情浪分析 | 0.005 美元 |
| `ichimoku(symbol, timeframe)` | Ichimoku 云图分析 | 0.005 美元 |
| `cashflow(mode, symbol)` | 资金流动数据 | 0.005 美元 |
| `coin_info(symbol)` | 加密货币基本信息、价格数据、标签、CMC AI 分析结果及 DEX 数据 | 0.025–0.03 美元（5–6 次调用） |
| `dexscreener CONTRACT)` | DEX 交易数据 | 0.005 美元 |
| `chain_tokens(chain, max_mcap)` | 特定链上的小市值代币 | 0.005 美元 |
| `portfolio` | Abu 为您精选的投资组合模型 | 0.005 美元 |
| `ask_aiquestion` | AI 分析师的自由形式回答 | 0.01 美元 |
| `indicator_guide(name)` | Asrai 特定指标的使用指南 | 免费 |

## 输出要求

- 以经验丰富的交易者的方式撰写，用通俗易懂的语言进行解释
- 既要考虑交易者的需求，也要兼顾长期投资者的视角。默认采用投资者模式；只有在用户请求具体交易建议时才切换到交易者模式
- 每条回复长度控制在 200–400 字之间，各部分之间适当留白
- 不要直接列出原始指标数值，而是将其转化为易于理解的结论
- 每条回复都要明确给出一个行动建议（买入/持有/观望），并说明原因
- 回复中不要提及工具名称、API 调用方式或支付细节

## 费用标准

大多数工具的每次调用费用为 0.005 美元；`ask_ai` 服务费用为 0.01 美元；`indicator_guide` 免费提供。费用从用户自己的钱包在 Base 主网上自动扣除。如有需要，可告知用户相关费用信息。