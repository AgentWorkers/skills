---
name: asrai
description: 使用 Asrai API 进行加密货币市场分析。该服务涵盖技术分析、筛选工具、市场情绪监测、预测模型、智能资金流动分析、艾略特波浪理论（Elliott Wave）分析、现金流数据以及基于人工智能的市场洞察。当需要获取加密货币交易信号、市场概况、特定币种分析或任何与加密货币相关的数据时，均可使用该服务。所有 API 接口均采用按次计费的模式（通过 Base 主网上的 x402 协议，每次调用费用为 0.05 美元 USD）。
---
# Asrai — 通过 x402 进行加密货币分析

## 如何调用 API 端点

- 基本 URL：`https://x402.asrai.me`
- 支付方式：通过已安装的 `asrai-mcp` MCP 工具进行自动支付
- 每个 API 端点的费用为 **0.05 美元（USDC）**（在主网环境下）；`/ai` 端点的费用为 0.10 美元

## 使用 MCP 工具

请使用已安装的 `asrai` MCP 工具，它们会自动处理 x402 支付：

| 问题类型 | 使用的工具 |
|---|---|
| 市场概览 | `market_overview` |
| 某种加密货币的技术分析（信号、指标） | `technical_analysis(symbol, timeframe)` |
| 市场情绪（恐惧/贪婪） | `sentiment` |
| 某种加密货币的价格预测 | `forecast(symbol)` |
| 根据条件查找加密货币 | `screener(type)` |
| 智能资金流动、订单信息 | `smart_money(symbol, timeframe)` |
| 惠勒波浪分析 | `elliott_wave(symbol, timeframe)` |
| 一目均衡线分析 | `ichimoku(symbol, timeframe)` |
| 资本流动情况 | `cashflow(mode, symbol)` |
| 加密货币信息 | `coin_info(symbol)` |
| DEX 代币数据 | `dexscreener(contract_address)` |
| 链上市值较低的代币 | `chain_tokens(chain, max_mcap)` |
| 投资组合分析 | `portfolio(symbol)` |
| 最新市场动态/新闻 | `channel_summary` |
| 自由形式的加密货币相关问题 | `ask_aiquestion)` |

## 输出规则

- 保持输出内容易于阅读：使用简短的行、适当的空白以及表情符号作为章节标题。
- 在面向用户的输出中，不要提及工具、API 端点或 x402 支付的相关信息。
- 避免使用流动性较低的加密货币作为分析对象；优先选择在多个榜单中出现且交易量较大的加密货币。
- 作为市场参考，可以使用 BTC/ETH 的每日信号作为参考指标。

## 默认的分析流程

1. **确定分析范围**：分析 BTC/ETH 的趋势及市场情绪。
2. **发现市场信号**：识别市场中的重要因素（如价格波动、交易量异常等）及情绪极端情况。
3. **转化为实际行动**：根据分析结果提供 1–2 条实用的建议或操作建议。

## 参考资料

- 完整的 API 端点目录：`skills/asrai/references/endpoints.md`