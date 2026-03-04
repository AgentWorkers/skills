---
name: asrai-x402
description: 使用 Asrai API 进行加密货币市场分析。该分析涵盖技术分析、筛选工具、市场情绪监测、预测模型、智能资金流动分析、艾略特波浪理论（Elliott Wave）的应用、现金流分析以及基于人工智能的洞察。使用前需确保已安装 asrai-mcp 并设置 ASRAI_PRIVATE_KEY 环境变量。每次 API 调用费用为 0.005 美元（USDC），费用将从您在 Base 主网上的钱包中扣除（通过 x402 协议进行支付）。
license: MIT
---
# Asrai — 通过 x402 进行加密货币分析

## 先决条件

使用此功能需要 **asrai-mcp**（基于 Node.js，无需安装）。请将其添加到 Claude Desktop 的配置文件中：

```json
{
  "mcpServers": {
    "asrai": {
      "command": "npx",
      "args": ["-y", "asrai-mcp"],
      "env": { "ASRAI_PRIVATE_KEY": "0x<your_private_key>" }
    }
  }
}
```

或者将密钥存储在 `~/.env` 文件中，此时可以省略 `env` 配置块：
```
ASRAI_PRIVATE_KEY=0x<your_private_key>
```

配置文件的位置：macOS — `~/Library/Application Support/Claude/claude_desktop_config.json`；Windows — `%APPDATA%\Claude\claude_desktop_config.json`；Linux — `~/.config/Claude/claude_desktop_config.json`。

对于 **n8n** 或 **远程连接**，可以使用托管的 SSE 服务器（无需安装）：
- HTTP Streamable：`https://mcp.asrai.me/mcp?key=0x<your_private_key>`
- SSE（旧版本）：`https://mcp.asrai.me/sse?key=0x<your_private_key>`

每次 API 调用会从用户的钱包中扣除 **0.005 美元 USD**（`ask_ai` 为 0.01 美元）。`indicator_guide` 服务是免费的。

## 支付透明度

- 如果用户询问，务必在调用服务前告知他们所需的费用。
- 环境变量 `ASRAI_MAX_SPEND` 可设置每次会话的支出上限（默认为 2.00 美元）。
- 所有支付操作均由用户自己的钱包完成，绝不使用共享密钥。

## MCP 提供的工具及其费用

| 工具 | 功能 | 费用 |
|---|---|---|
| `market_overview` | 提供市场趋势、涨跌情况、RSI 指数、价格区间、CMC AI 分析、CBBI 指数、市场情绪分析以及 9 种筛选器（包括 ATH、Ichimoku-Trend、SAR、MACD 交叉点、技术评级、成交量、高波动率低市值股票等） | 19 次调用，每次 0.095 美元 |
| `technical_analysis(symbol, timeframe)` | 提供技术分析信号（ALSAT、SuperALSAT、PSAR、MACD-DEMA、AlphaTrend、TD 指数等） | 12 次调用，每次 0.06 美元 |
| `sentiment` | 提供市场情绪分析（CBBI、CMC 指数等） | 3 次调用，每次 0.015 美元 |
| `forecast(symbol)` | 提供价格预测 | 1 次调用，每次 0.005 美元 |
| `screener(type)` | 根据指定条件筛选加密货币 | 1 次调用，每次 0.005 美元 |
| `smart_money(symbol, timeframe)` | 提供市场情绪分析、订单信息、FVG（资金流动图）以及支撑/阻力位信息 | 2 次调用，每次 0.01 美元 |
| `elliott_wave(symbol, timeframe)` | 提供艾略特波浪分析 | 1 次调用，每次 0.005 美元 |
| `ichimoku(symbol, timeframe)` | 提供 Ichimoku 图表分析 | 1 次调用，每次 0.005 美元 |
| `cashflow(mode, symbol)` | 提供资金流动分析 | 1 次调用，每次 0.005 美元 |
| `coin_info(symbol)` | 提供加密货币的统计信息、价格、标签以及通过合约地址获取的 CMC AI 分析结果（如可用） | 5–6 次调用，每次 0.025–0.03 美元 |
| `dexscreener(contract)` | 提供去中心化交易所（DEX）的数据 | 1 次调用，每次 0.005 美元 |
| `chain_tokens(chain, max_mcap)` | 列出链上的低市值代币 | 1 次调用，每次 0.005 美元 |
| `portfolio` | 提供 Abu 为您精选的投资组合建议（适用于咨询投资策略或“应该购买哪些加密货币”时）；若未指定代币，则显示完整投资组合；若指定了代币，则显示该代币的持仓情况 | 1 次调用，每次 0.005 美元 |
| `channel_summary` | 提供最新的市场分析报告 | 1 次调用，每次 0.005 美元 |
| `ask_aiquestion)` | 提供 AI 分析师的回答 | 1 次调用，每次 0.01 美元 |
| `indicator_guide(name)` | 提供 Asrai 自定义指标（如 ALSAT、SuperALSAT、PMax、AlphaTrend 等）的使用指南 | 免费 |

## indicator_guide 的使用方法

仅在工具输出中出现不熟悉的指标名称时才使用 `indicator_guide()` 函数。常见的指标（如 RSI、MACD、Ichimoku、BB、Elliott Wave）可忽略。

- `indicator_guide()` 或 `indicator_guide("list")`：获取所有自定义指标的简明摘要 |
- `indicator_guide("ALSAT")`：获取该指标的详细信息 |
- `indicator_guide("all")`：获取所有指标的完整使用指南（除非必要，否则无需使用）

## 输出格式要求

- 以经验丰富的交易者的方式向朋友解释信息，语言应自然、自信且直接，避免使用报告式的模板。
- 既要考虑交易者的视角，也要考虑长期投资者的需求。默认采用投资者模式（分析市场趋势、周期位置、积累区域等）；只有在用户询问买入时机时才切换到交易者模式。
- 回答内容长度控制在 200–400 字之间，内容应详尽且易于理解。各部分之间使用简洁的段落分隔。
- 适当使用表情符号来区分不同部分，但不要强行遵循固定的格式；根据重点内容调整回答的结构。
- 绝不要直接列出原始的指标数值，而是将其转化为通俗易懂的结论。
- 应避免使用流动性较低的指标；优先选择在多个指标中都出现、成交量较大或具有明确市场催化因素的信号。
- 回答中不要提及工具名称、API 端点或具体的 API 调用细节。
- 最后应明确给出一个具体的操作建议（如“积累”、“等待”或“避免购买”），并说明原因。

## 默认的分析流程

1. **分析市场环境**：判断 BTC/ETH 的整体趋势及市场情绪（使用 CBBI 指数）。
2. **寻找交易信号**：分析市场周期、趋势及动量（使用 ALSAT/SuperALSAT、PMax 指数）。
3. **制定行动方案**：根据分析结果给出明确的建议（如“积累”、“等待”或“避免购买”），并指出相应的价格区间。

## 参考资料

- 完整的 API 端点目录：`skills/asrai/references/endpoints.md`