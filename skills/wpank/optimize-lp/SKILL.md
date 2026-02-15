---
name: optimize-lp
description: 根据代币对的特征、历史数据以及用户的风险承受能力，为用户推荐最佳的长期持有（LP, Long Position）策略。该策略会考虑版本（V2/V3/V4）、费用等级、价格波动范围以及再平衡方法等因素。适用于用户询问如何进行长期持有、应选择何种价格波动范围或哪种版本/费用等级的情况。
model: opus
allowed-tools: [Task(subagent_type:lp-strategist)]
---

# 优化流动性提供（LP Optimization）

## 概述

本技能为特定的代币对提供针对性的、可执行的流动性提供（LP）策略建议。该建议由 `lp-strategist` 代理负责执行，该代理会分析代币对的波动性、评估不同版本的费用结构、选择最优的费用等级、计算最佳的价格波动范围，并设计相应的再平衡策略——所有这些决策都基于链上数据和风险分析。

本技能能够回答如下问题：“我应该如何将 **X** 代币转换为 **Y** 代币以实现流动性提供？” 并给出具体、可操作的解决方案。

## 使用场景

当用户提出以下问题时，可激活此技能：
- “ETH/USDC 的最佳流动性提供策略是什么？”
- “我应该如何将 1 万美元转换为 ETH/USDC？”
- “WETH/USDC 的价格波动范围应该设置得窄还是宽？”
- “对于这个代币对，应该选择 V2 版本还是 V3 版本？”
- “UNI/ETH 的费用等级应该设为多少？”
- “如何优化我的 ETH/USDC 流动性提供策略？”
- “我应该为我的 ETH/USDC 持仓设置多大的价格波动范围？”
- “对于这个代币对，是否应该使用集中式流动性提供方式？”

## 参数

| 参数                          | 是否必填 | 默认值         | 提取方式                                      |
| --------------------------- | -------- | ------------ | ------------------------------------------------------- |
| token0         | 是       | —            | 第一个代币：ETH、WETH、USDC 或者 0x 地址                       |
| token1         | 是       | —            | 第二个代币                                      |
| capital        | 否       | —            | 流动性提供金额：例如 “1 万美元”、“5 个 ETH” 或 “5 万美元”                |
| chain          | 否       | ethereum      | 交易链，例如 “ethereum”、“base”、“arbitrum” 等                    |
| riskTolerance  | 否       | 中等（moderate）     | 风险容忍度：保守（conservative）、中等（moderate）、激进（aggressive）           |

## 工作流程

1. **从用户请求中提取参数**：确定代币对、流动性提供金额（如果已提供）、交易链以及风险容忍度。
2. **委托给 `lp-strategist` 代理**：使用相关参数调用 `Task(subagent_type:lp-strategist)`。代理将执行以下 7 个步骤的分析：
   - 对代币对进行分类（稳定-稳定、稳定-波动、波动-波动）
   - 评估 V2、V3 和 V4 版本之间的优缺点
   - 根据数据选择最优的费用等级
   - 计算价格波动范围，确保该范围在 80% 的时间内处于指定范围内
   - 设计再平衡策略，并考虑交易手续费成本
   | 获取独立的风险评估结果
   | 提供保守/中等/乐观的策略建议

3. **以清晰、可操作的形式呈现策略**：将分析结果以具体的数字和步骤形式呈现给用户。

## 输出格式

```text
LP Strategy for WETH/USDC

  Recommendation: V3, 0.05% fee tier
  Pool: 0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640 (Ethereum)

  Range: $1,668 - $2,258 (±15%, medium strategy)
  Expected time-in-range: ~82%

  Expected Returns (annualized):
    Conservative: 8.5% APY (after IL)
    Moderate:     15.2% APY (after IL)
    Optimistic:   24.1% APY (after IL)

  Expected IL:
    Conservative: 2.1%
    Moderate:     5.8%
    Worst case:   12.3%

  Rebalance Strategy:
    Trigger: Price within 10% of range boundary
    Frequency: Every 2-3 weeks (estimated)
    Gas cost: ~$15 per rebalance

  Risk Assessment: MEDIUM (approved by risk-assessor)

  Alternatives Considered:
    V3 0.3%: Lower APY (8%) but less competition
    V2: No range management, ~4% APY — good for passive
    Narrow range (±5%): Higher APY but needs weekly rebalancing

  Ready to add liquidity? Say "Add liquidity to WETH/USDC"
```

## 重要说明

- 本技能仅提供策略建议，不负责实际的执行。如需执行该策略，请使用 `manage-liquidity` 技能。
- 所有的年化收益率（APY）估计值均基于历史数据。过去的表现并不能保证未来的回报。
- 在显示年化收益率时，会同时显示手续费年化收益率（IL）和费用年化收益率（fee APY），绝不会单独显示其中一项。
- 对于小额持仓（<1 万美元），建议会考虑手续费对回报的影响。
- `lp-strategist` 代理内部会委托 `pool-researcher` 负责数据收集，委托 `risk-assessor` 进行风险评估。

## 错误处理

| 错误类型                | 用户看到的提示信息                                      | 建议采取的措施                                      |
| ---------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| 代币未找到                | “在 Uniswap 上找不到 X 代币。”                                      | 提供代币的合约地址                              |
| 未找到合适的流动性提供池         | “在该交易链上找不到 X/Y 代币的流动性提供池。”                        | 尝试其他交易链或检查代币是否可用                        |
| 数据不足                | “历史数据不足，无法生成可靠的策略。”                                  | 可能是因为流动性提供池成立时间较短                          |
| 代理不可用                | “流动性提供策略代理当前不可用。”                                    | 检查代理的配置是否正常                            |