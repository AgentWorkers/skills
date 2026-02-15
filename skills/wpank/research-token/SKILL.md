---
name: research-token
description: 研究某个代币在 Uniswap 平台上的流动性、交易量分布、交易池构成以及相关风险因素。当用户询问某个代币的可交易性、流动性情况或需要深入了解该代币时，可以使用这些信息来进行尽职调查。
model: opus
allowed-tools: [Task(subagent_type:token-analyst)]
---

# 研究令牌（Research Token）

## 概述

该功能从 Uniswap 协议的角度对令牌进行全面尽职调查。它会委托给 `token-analyst` 代理来分析所有交易池中的流动性、交易量趋势以及风险因素。

## 使用场景

当用户提出以下问题时，可以激活该功能：
- “研究 UNI 令牌”
- “X 令牌的流动性足够吗？”
- “对 PEPE 令牌进行分析”
- “对这个令牌进行尽职调查”
- “哪些交易池在交易 X 令牌？”
- “X 令牌在 Uniswap 上的流动性如何？”
- “交易 X 令牌安全吗？”

## 参数

| 参数          | 是否必填 | 默认值        | 说明                                      |
|---------------|--------|-------------|-----------------------------------------|
| token         | 是       | —           | 令牌名称、符号或合约地址                             |
| chain         | 否       | 所有链         | 指定链或“所有链”（用于跨链视图）                        |
| focus         | 否       | 全面分析       | “流动性”、“交易量”或“风险”                             |

## 工作流程

1. **从用户请求中提取参数**：确定要研究的令牌以及任何链或分析重点。
2. **委托给 `token-analyst` 代理**：使用令牌标识符调用 `Task(subagent_type:token-analyst)`。该代理会解析该令牌信息，查找所有交易池，分析其流动性及交易量，并生成风险评估报告。
3. **展示结果**：将 `token-analyst` 代理的报告格式化为用户易于理解的摘要。

## 输出格式

```text
Token Research: UNI (Uniswap)

  Address:  0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984
  Chains:   Ethereum, Arbitrum, Optimism, Polygon, Base
  Pools:    24 active pools across all chains

  Liquidity:
    Total TVL:   $85M across all pools
    Best pool:   WETH/UNI 0.3% (49.4% of liquidity)
    Depth (1%):  $2.5M trade size
    Fragmentation: Moderate

  Volume:
    24h: $15M | 7d: $95M | 30d: $380M
    Trend: Stable
    Turnover: 0.18x daily

  Risk Factors:
    - Moderate pool concentration (49.4% in one pool) — LOW severity

  Trading: Suitable for trades up to $2.5M with < 1% price impact
```

## 重要说明

- 所有分析工作完全委托给 `token-analyst` 代理，不直接调用 MCP 工具。
- 该分析仅基于 Uniswap 协议的数据，不提供一般性的投资建议。
- 风险因素仅基于链上的可观测指标，不包含价格预测。

## 错误处理

| 错误类型                | 显示给用户的消息                                      | 建议的操作                                      |
|-------------------|---------------------------------------------------------|-------------------------------------------|
| 未找到令牌             | “在 Uniswap 上未找到 X 令牌。”                             | 提供合约地址                                    |
| 未找到交易池             | “未找到该令牌的交易池。”                                 | 该令牌可能尚未在 Uniswap 上上市                         |
| 数据不足             | “该令牌的交易数据有限。”                                  | 该令牌可能发布时间较短                         |