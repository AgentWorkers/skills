---
name: asrai-x402
description: 使用 Asrai API 进行加密货币市场分析。涵盖技术分析、筛选工具、市场情绪监测、预测模型、机构投资者的投资行为、艾略特波浪理论（Elliott Wave）、现金流分析、去中心化交易所（DEX）数据以及基于人工智能的洞察。需要先安装 asrai-mcp 并设置 PRIVATE_KEY 环境变量。每次 API 调用费用为 0.001 美元（USDC），费用将从您在 Base 主网上的钱包中扣除，支付方式通过 x402 进行。
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

或者，您可以将密钥存储在 `~/.env` 文件中，从而省略 `env` 部分：

```env
PRIVATE_KEY=0x<your_private_key>
```

配置文件的位置如下：
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

对于 **n8n** 或 **远程连接**，可以使用托管的 SSE 服务器（无需安装）：
- HTTP Streamable: `https://mcp.asrai.me/mcp?key=0x<your_private_key>`
- SSE (legacy): `https://mcp.asrai.me/sse?key=0x<your_private_key>`

每次 API 调用会从您的钱包中扣除 **0.001 美元 USD**（`ask_ai` 为 0.002 美元）。`indicator_guide` 是免费提供的。

## 支付透明度

- 如果用户询问，请在调用 API 之前告知他们相关费用。
- 环境变量 `ASRAI_MAX_SPEND` 用于设置单次会话的支出上限（默认为 2.00 美元）。
- 所有支付操作均由用户自己的钱包完成，绝不使用共享密钥。

## 可用的 MCP 工具

| 工具 | 功能 | 费用 |
|---|---|---|
| `market_overview` | 趋势分析、收益/亏损情况、RSI 指数、价格高低点 | $0.004（4 次调用） |
| `technical_analysis(symbol, timeframe)` | 信号分析、ALSAT、SuperALSAT、PSAR、MACD-DEMA、AlphaTrend、TD | $0.007（7 次调用） |
| `sentiment` | 市场情绪分析（CBBI、CMC 指标） | $0.003（3 次调用） |
| `forecast(symbol)` | 价格预测 | $0.001 |
| `screener(type)` | 根据条件筛选加密货币 | $0.001 |
| `smart_money(symbol, timeframe)` | 财务分析、订单信息、支撑/阻力位 | $0.002（2 次调用） |
| `elliott_wave(symbol, timeframe)` | 埃利奥特波浪理论分析 | $0.001 |
| `ichimoku(symbol, timeframe)` | 一目均衡线分析 | $0.001 |
| `cashflow(mode, symbol)` | 资本流动分析 | $0.001 |
| `coin_info(symbol)` | 信息查询、价格数据、标签 | $0.004（4 次调用） |
| `dexscreener CONTRACT)` | DEX 数据分析 | $0.001 |
| `chain_tokens(chain, max_mcap)` | 链上低市值代币分析 | $0.001 |
| `portfolio` | 投资组合分析 | $0.001 |
| `channel_summary` | 最新市场分析报告 | $0.001 |
| `ask_aiquestion)` | 人工智能分析结果 | $0.002 |
| `indicator_guide(name)` | Asrai 自定义指标使用指南（ALSAT、SuperALSAT、PMax、AlphaTrend 等） | 免费 |

## indicator_guide 的使用方法

仅在工具输出中出现不熟悉的指标名称时才使用 `indicator_guide`。常见的指标（如 RSI、MACD、Ichimoku、BB、Elliott Wave）可忽略。

- `indicator_guide()` 或 `indicator_guide("list")`：获取所有自定义指标的简要概述。
- `indicator_guide("ALSAT")`：获取该指标的详细信息。
- `indicator_guide("all")`：获取所有指标的完整使用指南（除非必要，否则可省略）。

## 输出格式建议

- 以经验丰富的交易者的方式撰写，用简洁明了的语言进行解释。
- 既要考虑交易者的需求，也要兼顾长期投资者的视角。默认采用投资者模式（宏观趋势分析、周期位置、积累区域等）；仅在用户询问买入/卖出策略时切换到交易者模式。
- 每条回复长度控制在 200–400 字之间，内容详尽且易于阅读。使用短句，并在各个部分之间留出适当的间隔。
- 适当使用表情符号来区分不同部分，但不要拘泥于固定的格式。根据重点内容灵活调整回复结构。
- 绝不要直接列出原始的指标数值，而是将其转化为易于理解的结论。
- 避免分析那些流动性较低、缺乏明确交易信号的指标；优先选择在多个指标中都出现、成交量较大或具有明确交易催化因素的信号。
- 回复中不要提及工具名称、API 端点或具体的 API 调用细节。
- 每条回复都要明确给出一个行动建议（例如：积累、等待或避开），并说明原因。

## 默认的分析流程

1. **确定市场环境**：分析 BTC/ETH 的整体趋势及市场情绪（使用 CBBI 指标）。
2. **寻找交易信号**：利用 ALSAT/SuperALSAT 分析周期位置、PMax 指数及市场动能。
3. **制定行动方案**：根据分析结果给出明确的建议（例如：积累、等待或避开特定价格区间）。

## 参考资料

- 完整的 API 端点目录：`skills/asrai/references/endpoints.md`