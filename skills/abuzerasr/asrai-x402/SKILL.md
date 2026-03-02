---
name: asrai-x402
description: 使用 Asrai API 进行加密货币市场分析。该分析涵盖技术分析、筛选工具、市场情绪监测、预测模型、智能资金流动分析、艾略特波浪理论（Elliott Wave）分析、现金流数据以及基于人工智能的洞察。请确保已安装 asrai-mcp 并设置 PRIVATE_KEY 环境变量。每次 API 调用费用为 0.001 美元（USDC），费用将从您在 Base 主网上的钱包中通过 x402 协议扣除。
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
      "env": { "PRIVATE_KEY": "0x<your_private_key>" }
    }
  }
}
```

或者，您可以将私钥保存在 `~/.env` 文件中，从而省略 `env` 部分：

```env
PRIVATE_KEY=0x<your_private_key>
```

配置文件的位置如下：
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

对于 **n8n/远程连接**，可以使用托管的 SSE 服务器（无需安装）：
- HTTP Streamable: `https://mcp.asrai.me/mcp?key=0x<your_private_key>`
- SSE (legacy): `https://mcp.asrai.me/sse?key=0x<your_private_key>`

每次 API 调用会从您的钱包中扣除 **0.001 美元 USD**（`ask_ai` 为 0.002 美元）。`indicator_guide` 是免费的。

## 支付透明度

- 如果用户询问，请在调用 API 之前始终告知他们相关费用。
- 环境变量 `ASRAI_MAX_SPEND` 用于设置会话内的消费上限（默认为 2.00 美元）。
- 所有支付操作均由用户自己的钱包完成，绝不会使用共享密钥。

## 可用的 MCP 工具

| 工具 | 功能 | 费用 |
|---|---|---|
| `market_overview` | 趋势分析、盈利/亏损情况、RSI 指数、价格区间、CMC AI、CBBI 指数、市场情绪分析、现金流分析、社会影响力评估以及 9 种筛选条件（包括 ATH、Ichimoku 趋势线、SAR、MACD 交叉点、技术评级、成交量分析、高波动率低市值股票） | 0.019 美元（19 次调用） |
| `technical_analysis(symbol, timeframe)` | 信号分析、ALSAT 指数、SuperALSAT 指数、PSAR 指数、MACD-DEMA 指数、AlphaTrend 指数、TD 指数、智能资金流动分析、支撑/阻力位分析、艾略特波浪理论分析、Ichimoku 趋势线分析 | 0.012 美元（12 次调用） |
| `sentiment` | CBBI 指数、CMC 情绪分析、CMC AI | 0.003 美元（3 次调用） |
| `forecast(symbol)` | 价格预测 | 0.001 美元 |
| `screener(type)` | 根据特定条件筛选加密货币 | 0.001 美元 |
| `smart_money(symbol, timeframe)` | SMC 指数分析、订单信息、FVG（资金流动分析）以及支撑/阻力位分析 | 0.002 美元（2 次调用） |
| `elliott_wave(symbol, timeframe)` | 艾略特波浪理论分析 | 0.001 美元 |
| `ichimoku(symbol, timeframe)` | Ichimoku 趋势线分析 | 0.001 美元 |
| `cashflow(mode, symbol)` | 资本流动分析 | 0.001 美元 |
| `coin_info(symbol)` | 项目信息、价格数据、标签信息；如果可用，还包括通过合约地址获取的 CMC AI 数据 | 0.005–0.006 美元（5–6 次调用） |
| `dexscreener(contract)` | DEX（去中心化交易所）数据 | 0.001 美元 |
| `chain_tokens(chain, max_mcap)` | 链路上的低市值代币信息 | 0.001 美元 |
| `portfolio` | Abu 为您精选的投资组合推荐（适用于寻求投资建议或了解“应该购买哪些代币”的情况）；未指定代币时显示完整投资组合；指定代币时显示该代币的持仓情况 | 0.001 美元 |
| `channel_summary` | 最新的市场分析报告 | 0.001 美元 |
| `ask_aiquestion)` | 人工智能分析师的回答 | 0.002 美元 |
| `indicator_guide(name)` | Asrai 的自定义指标使用指南（如 ALSAT、SuperALSAT、PMax、AlphaTrend 等） | 免费 |

## indicator_guide 的使用方法

仅当在工具输出中遇到不熟悉的指标名称时才使用 `indicator_guide()`。常见的指标（如 RSI、MACD、Ichimoku、BB、艾略特波浪理论）可忽略。

- `indicator_guide()` 或 `indicator_guide("list")`：提供所有自定义指标的简洁摘要。
- `indicator_guide("ALSAT")`：获取该指标的详细信息。
- `indicator_guide("all")`：获取所有自定义指标的完整使用指南（除非有必要，否则无需使用）。

## 输出格式要求

- 以经验丰富的交易者的方式撰写，用通俗易懂的语言进行解释，避免使用正式的报告模板。
- 既要考虑交易者的需求，也要兼顾长期投资者的视角。默认采用投资者模式（分析宏观趋势、市场周期及买入/持有区间）；仅在用户询问买入时机时切换到交易者模式。
- 每条回复长度控制在 200–400 字之间，内容详尽但易于阅读。使用简短的段落，并在各个部分之间留出适当的间隔。
- 适当使用表情符号来区分不同部分，但不要强行遵循固定的格式。根据重点内容灵活调整回复结构。
- 绝不要直接列出原始的指标数值，而是将其转化为易于理解的结论。
- 避免分析那些流动性较低、缺乏市场验证的指标；优先选择在多个指标中都出现、具有显著成交量或明确市场催化因素的信号。
- 回复中不要提及工具名称、API 端点或具体的 API 调用细节。
- 每条回复都要明确给出一个行动建议（例如：继续持有、等待时机或避免交易），并说明原因。

## 默认的分析流程

1. **分析市场环境**：判断 BTC/ETH 的整体趋势及市场情绪（使用 CBBI 指数）。
2. **寻找交易信号**：分析 ALSAT/SuperALSAT 指数、PMax 指数、MACD 指数的趋势及动量情况。
3. **制定行动方案**：根据分析结果给出明确的建议（继续持有、等待时机或避免交易），并标注相应的价格区间。

## 参考资料

- 完整的 API 端点目录：`skills/asrai/references/endpoints.md`