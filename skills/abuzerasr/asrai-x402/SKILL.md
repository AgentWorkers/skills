---
name: asrai-x402
description: 使用 Asrai API 进行加密货币市场分析。该服务涵盖技术分析、筛选工具、市场情绪监测、预测模型、智能资金流动分析、艾略特波浪理论（Elliott Wave）分析、现金流数据以及基于人工智能的洞察。每次 API 调用费用为 0.005 美元（USDC），费用将从您在 Base 主网上的钱包中扣除（使用 x402 账户进行支付）。
license: MIT
metadata: {"openclaw":{"emoji":"📈","requires":{"env":["ASRAI_PRIVATE_KEY"]}},"clawdbot":{"emoji":"📈","requires":{"env":["ASRAI_PRIVATE_KEY"]}}}
---
# Asrai — 通过 x402 进行加密货币分析

当用户询问加密货币价格、市场分析、交易信号、市场情绪或投资建议时，可以使用 Asrai 工具。

## 使用场景

- 加密货币价格/图表/技术分析 → 使用 Asrai 工具
- 市场情绪、CBBI（Fear/Bear Index）、恐惧/贪婪情绪 → 使用 Asrai 工具
- “我应该买什么？”/投资组合建议 → 使用 `portfolio` 工具
- 情浪分析、智能资金流动、订单信息 → 使用 Asrai 工具
- DEX（去中心化交易所）数据、小市值代币 → 使用 Asrai 工具
- 用户已经掌握的通用知识 → 直接回答（每次咨询费用为 0.005 美元）

## 使用方法

### 如果可用 Asrai MCP 工具（Cursor、Cline、Claude Desktop）

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

通过 bash 调用相同的工具：
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

请确保在 `~/.env` 文件中设置了 `ASRAI_PRIVATE_KEY`。支付过程会自动完成签名。

## MCP 工具列表

| 工具 | 功能 | 费用 |
|---|---|---|
| `market_overview` | 市场趋势、盈利/亏损情况、RSI 指数、市场情绪分析、筛选器 | 0.095 美元 |
| `technical_analysis(symbol, timeframe)` | 交易信号、ALSAT、SuperALSAT、情浪分析、一目均衡线 | 0.06 美元 |
| `sentiment` | CBBI 指数、CMC 市场情绪分析、人工智能洞察 | 0.015 美元 |
| `forecast(symbol)` | 人工智能价格预测 | 0.005 美元 |
| `screener(type)` | 根据条件筛选加密货币 | 0.005 美元 |
| `smart_money(symbol, timeframe)` | 智能资金流动分析、订单信息、支撑/阻力位 | 0.01 美元 |
| `elliott_wave(symbol, timeframe)` | 情浪分析 | 0.005 美元 |
| `ichimoku(symbol, timeframe)` | 一目均衡线分析 | 0.005 美元 |
| `cashflow(mode, symbol)` | 资本流动分析 | 0.005 美元 |
| `coin_info(symbol)` | 代币信息、价格数据、CMC 人工智能分析、DEX 数据 | 0.025–0.03 美元 |
| `dexscreener(contract)` | DEX 数据分析 | 0.005 美元 |
| `chain_tokens(chain, max_mcap)` | 链上小市值代币分析 | 0.005 美元 |
| `portfolio` | Abu 为您精选的投资组合 | 0.005 美元 |
| `channel_summary` | 最新市场动态 | 0.005 美元 |
| `ask_aiquestion)` | 人工智能分析师的回答 | 0.01 美元 |
| `indicator_guide(name)` | 自定义指标使用指南 | 免费 |

## 回答格式

- 以经验丰富的交易者的方式回答，语言简洁明了、自信且直接
- 既要考虑交易者的需求，也要兼顾长期投资者的视角。默认采用投资者模式；只有在用户请求具体交易建议时才切换到交易者模式
- 回答内容控制在 200–400 字之间，段落之间适当留白
- 不要直接列出原始指标数值，而是将其转化为通俗易懂的结论
- 每条回复都要明确给出一个行动建议（买入/持有/卖出），并说明原因
- 回答中不要提及工具名称、API 调用方式或支付细节

## 费用

- 大多数工具的每次咨询费用为 0.005 美元
- `ask_ai` 服务费用为 0.01 美元
- `indicator_guide` 免费提供

支付过程通过用户自己的 Base 主网钱包完成签名。如有需要，可告知用户相关细节。

## 安装方法

```bash
npx -y -p asrai-mcp install-skill
```

系统会自动检测 OpenClaw、Cursor、Cline 等代理程序。之后请设置您的私钥：
```
ASRAI_PRIVATE_KEY=0x<your_private_key>  # add to ~/.env
```

对于 MCP 代理（Cursor、Cline、Claude Desktop），还需在配置文件中进行相应设置：
```json
{
  "mcpServers": {
    "asrai": { "command": "npx", "args": ["-y", "asrai-mcp"] }
  }
}
```