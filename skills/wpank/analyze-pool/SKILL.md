---
name: analyze-pool
description: 分析特定 Uniswap 池的运行表现、流动性深度、费用年化收益率（APY）以及风险因素。当用户询问池的指标、总价值锁定（TVL）、交易量，或者某个池是否适合进行锁定策略（LPing）时，可以使用此分析结果。
model: opus
allowed-tools: [Task(subagent_type:pool-researcher)]
---

# 分析交易池

## 概述

该功能通过委托给 `pool-researcher` 代理来提供对特定 Uniswap 交易池的详细分析。分析结果包括总价值（TVL）、交易量、费用年化收益率（fee APY）、流动性深度、集中度指标以及风险因素。

## 使用场景

当用户提出以下问题时，可激活此功能：
- “分析 ETH/USDC 交易池”
- “X/Y 交易池的总价值（TVL）是多少？”
- “WETH/USDC 交易池的交易量是多少？”
- “ETH/USDC 交易池的费用年化收益率（fee APY）是多少？”
- “这个交易池适合进行流动性提供（LP）操作吗？”
- “Base 平台上的 ETH/USDC 交易池信息”
- “这个交易池的流动性深度如何？”

## 参数

| 参数        | 是否必填 | 默认值       | 描述                                      |
|------------|--------|-----------|-----------------------------------------|
| token0      | 是      | —          | 第一种代币的名称、符号或地址                         |
| token1      | 是      | —          | 第二种代币的名称、符号或地址                         |
| chain       | 否       | ethereum    | 区块链名称（ethereum、base、arbitrum 等）                |
| feeTier     | 否       | 自动检测     | 费用等级（例如：“0.05%”、“30bp”、“3000”）                     |
| version     | 否       | 自动检测     | 协议版本（“v2”、“v3”或“v4”）                         |

## 工作流程

1. **从用户请求中提取参数**：确定 `token0`、`token1`、`chain`、`feeTier` 和 `version`。
2. **委托给 pool-researcher**：使用提取的参数调用 `Task(subagent_type:pool-researcher)`。`pool-researcher` 将收集链上数据，计算各项指标，并生成结构化的报告。
3. **展示结果**：将 `pool-researcher` 生成的报告整理成用户易于理解的摘要，内容包括：
   - 交易池信息（地址、协议版本、费用等级）
   - 当前状态（价格、总价值、流动性）
   - 绩效数据（过去 7 天/30 天的费用年化收益率、过去 24 小时/7 天的交易量、使用率）
   - 流动性深度（对价格影响小于 1% 的交易量）
   - 风险因素（如有）

## 输出格式

以简洁明了的摘要形式展示分析结果：

```text
Pool Analysis: WETH/USDC 0.05% (V3, Ethereum)

  Address: 0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640
  TVL:     $332M
  Price:   $1,963.52

  Performance:
    Fee APY (7d):  21.3%
    Fee APY (30d): 6.65%
    Volume (24h):  $610M
    Utilization:   1.84x

  Liquidity Depth:
    1% impact: $5M trade size
    5% impact: $25M trade size
    Concentration: 78.5% within ±2% of price

  Risk Factors: None identified
```

## 重要说明

- 该功能完全依赖 `pool-researcher` 代理来执行分析，不直接调用 MCP 工具。
- 如果指定的交易池不存在，代理会明确告知用户。
- 费用年化收益率（fee APY）为历史数据，不保证未来仍保持不变。输出结果会区分已实现的收益和预测的收益。

## 错误处理

| 错误类型                | 显示给用户的消息                                      | 建议的操作                                      |
|-------------------|--------------------------------------------|-----------------------------------------|
| 交易池未找到             | “在该区块链上未找到 X/Y 交易池。”                        | 尝试不同的费用等级或区块链                |
| 代币无法识别             | “无法解析代币 X。”                                      | 提供代币的合约地址                         |
| 数据不足             | “该交易池的数据有限。”                                      | 可能是因为交易池创建时间较短                         |