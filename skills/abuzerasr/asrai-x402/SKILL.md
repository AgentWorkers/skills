---
name: asrai
description: 使用 Asrai API 进行加密货币市场分析。该分析涵盖技术分析、筛选工具、市场情绪监测、预测模型、智能资金流动分析、艾略特波浪理论（Elliott Wave）、现金流数据以及基于人工智能的洞察。使用前需确保已安装 asrai-mcp 并设置 PRIVATE_KEY 环境变量。每次 API 调用费用为 0.001 美元（USDC），费用将从您在 Base 主网上的钱包中扣除（通过 x402 协议进行支付）。
license: MIT
---
# Asrai — 通过 x402 进行加密货币分析

## 先决条件

使用此功能需要安装 **asrai-mcp**：
```bash
pip install asrai-mcp
```

同时需要一个包含您的钱包密钥的 `~/.env` 文件：
```env
PRIVATE_KEY=0x<your_private_key>
```

每次 API 调用会从您的钱包中扣除 **0.001 美元**（Base 主网费用）；`ask_ai` 的费用为 **0.002 美元**。`indicator_guide` 是免费的。

## 支付透明度

- 如果用户询问，请在调用 API 之前始终告知他们相关费用。
- 环境变量 `ASRAI_MAX_SPEND` 设置了每次会话的花费上限（默认为 2.00 美元）。
- 所有支付操作均由用户自己的钱包完成，绝不会使用共享密钥。

## 可用的 MCP 工具

| 工具 | 功能 | 费用 |
|---|---|---|
| `market_overview` | 市场趋势、盈利/亏损指标、RSI、价格高低点 | 0.004 美元（4 次调用） |
| `technical_analysis(symbol, timeframe)` | 技术分析指标（ALSAT、SuperALSAT、PSAR、MACD-DEMA、AlphaTrend、TD） | 0.007 美元（7 次调用） |
| `sentiment` | 市场情绪分析（CBBI、CMC 情绪指标） | 0.003 美元（3 次调用） |
| `forecast(symbol)` | 价格预测 | 0.001 美元 |
| `screener(type)` | 根据条件筛选加密货币 | 0.001 美元 |
| `smart_money(symbol, timeframe)` | 财务指标分析（SMC、订单信息、FVGs、支撑/阻力位） | 0.002 美元（2 次调用） |
| `elliott_wave(symbol, timeframe)` | 埃利奥特波浪分析 | 0.001 美元 |
| `ichimoku(symbol, timeframe)` | 一目均衡线分析 | 0.001 美元 |
| `cashflow(mode, symbol)` | 资本流动分析 | 0.001 美元 |
| `coin_info(symbol)` | 项目信息、价格、标签 | 0.004 美元（4 次调用） |
| `dexscreener(contract)` | DEX 数据查询 | 0.001 美元 |
| `chain_tokens(chain, max_mcap)` | 链上低市值代币信息 | 0.001 美元 |
| `portfolio` | 投资组合分析 | 0.001 美元 |
| `channel_summary` | 最新市场分析报告 | 0.001 美元 |
| `ask_aiquestion)` | 人工智能分析结果 | 0.002 美元 |
| `indicator_guide(name)` | Asrai 自定义指标使用指南（ALSAT、SuperALSAT、PMax、AlphaTrend 等） | 免费 |

## indicator_guide 的使用方法

仅在工具输出中出现不熟悉的指标名称时才使用 `indicator_guide`。标准指标（RSI、MACD、Ichimoku、BB、Elliott Wave）是众所周知的，可以跳过。

- `indicator_guide()` 或 `indicator_guide("list")`：获取所有自定义指标的简短概述。
- `indicator_guide("ALSAT")`：获取该指标的详细信息。
- `indicator_guide("all")`：获取所有自定义指标的完整使用指南（除非必要，否则无需使用）。

## 输出规则

- 既要从交易者的角度，也要从长期投资者的角度进行分析。默认采用投资者模式（宏观趋势、周期位置、积累区域分析）；仅在用户询问买入时机或策略时切换到交易者模式。
- 回答内容长度控制在 200–400 字之间，既详细又易于阅读。
- 使用表情符号来区分不同部分：📊 市场背景、🎯 目标/买入点、⚠️ 风险、📈📉 趋势、💡 见解。
- 绝不要直接列出原始指标数值，而是将其转化为通俗易懂的结论。
- 回答中不要使用用户的名字。

## 默认分析流程

1. **确定市场环境**：比特币/以太坊的趋势及整体市场情绪（CBBI 指标）。
2. **寻找交易信号**：利用 ALSAT/SuperALSAT 分析周期位置、PMax 指标及市场动能。
3. **制定行动方案**：给出明确的建议：是否买入、持有或避开当前市场。

## 参考资料

- 完整的 API 端点目录：`skills/asrai/references/endpoints.md`