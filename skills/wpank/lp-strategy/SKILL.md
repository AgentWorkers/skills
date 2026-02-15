---
name: lp-strategy
description: **代币对的全面LP策略对比**  
该工具会同时评估各种LP（Lending Protocol）策略的多个方面，包括不同版本、费用等级、交易范围宽度以及再平衡机制，并对比分析年化收益率（APY）、利息率（IL）、交易手续费（gas costs）和风险等级。当用户需要比较不同的LP选项或深入了解各种策略的详细信息时，可使用该工具。
model: opus
allowed-tools: [Task(subagent_type:lp-strategist), Task(subagent_type:pool-researcher)]
---

# LP策略比较

## 概述

该功能会针对某个代币对生成一份全面的、多策略的比较报告。与`optimize-lp`仅提供一个推荐方案不同，该功能会并列展示所有可行的策略，并详细分析各自的优缺点，帮助用户做出明智的决策。

这属于“深度分析”版本——适用于用户希望了解所有选项的情况，而不仅仅是最佳选择。

## 使用场景

当用户提出以下问题时，请激活此功能：

- “比较ETH/USDC的LP策略”
- “我可以将X/Y代币用于LP投资有哪些选择？”
- “WETH/USDC的LP投资详细分析”
- “展示这个代币对的所有费用等级”
- “X/Y的V2、V3和V4版本之间的比较”
- “提供LP投资选项的完整分解”
- “我想在投资LP之前了解其中的权衡”

## 参数

| 参数                | 是否必需 | 默认值       | 获取方式                                      |
| ---------------------- | -------- | ------------ | ----------------------------------------- |
| token0              | 是       | —          | 第一个代币                                      |
| token1              | 是       | —          | 第二个代币                                      |
| capital             | 否        | —          | 可用于LP投资的资金总额                         |
| chain                | 否        | 所有链       | 特定链或“所有链”（用于跨链比较）                   |
| strategies          | 否        | 所有策略       | 需要比较的具体策略（通常为“所有策略”）                   |

## 工作流程

1. 从用户请求中提取相关参数。
2. **委托给pool-researcher**：首先通过`Task(subagent_type:pool-researcher)`获取所有费用等级和版本下的池信息（包括TVL、交易量和每个池的APY）。
3. **委托给lp-strategist**：以“全面比较”模式调用`Task(subagent_type:lp-strategist)`。该代理会评估所有可行的策略组合：
   - V2全范围策略（被动策略）
   - V3特定费用等级下的策略
   - V3中等费用等级下的策略
   - V3宽费用等级下的策略
   - V4版本下的策略（如果可用）
   - 跨链投资机会（如果选择“all”链）
4. 展示一份包含所有策略的比较表格，并标注各自的优缺点。

## 输出格式

```text
LP Strategy Comparison: WETH/USDC

  Pair Type: Stable-Volatile (moderate volatility)
  Best Overall: V3 0.05%, Medium Range (see row 2 below)

  ┌────┬──────────────────┬────────┬──────────┬───────┬──────────┬──────────┬────────┐
  │ #  │ Strategy         │ Chain  │ Fee APY  │ IL    │ Net APY  │ Rebal.   │ Risk   │
  ├────┼──────────────────┼────────┼──────────┼───────┼──────────┼──────────┼────────┤
  │ 1  │ V3 0.05% Narrow  │ ETH    │ 35%      │ -12%  │ 23%      │ Weekly   │ HIGH   │
  │ 2  │ V3 0.05% Medium  │ ETH    │ 21%      │ -6%   │ 15%      │ Bi-weekly│ MEDIUM │
  │ 3  │ V3 0.05% Wide    │ ETH    │ 12%      │ -2%   │ 10%      │ Monthly  │ LOW    │
  │ 4  │ V3 0.30% Medium  │ ETH    │ 8%       │ -6%   │ 2%       │ Bi-weekly│ MEDIUM │
  │ 5  │ V3 0.05% Medium  │ Base   │ 18%      │ -5%   │ 13%      │ Bi-weekly│ MEDIUM │
  │ 6  │ V2 0.30% Full    │ ETH    │ 4%       │ -1%   │ 3%       │ Never    │ LOW    │
  └────┴──────────────────┴────────┴──────────┴───────┴──────────┴──────────┴────────┘

  Strategy Details:

  #1 V3 0.05% Narrow (±5%) — HIGH RISK, HIGH REWARD
    Pros: Highest fee capture, maximum capital efficiency
    Cons: Frequent rebalancing ($15/rebalance on mainnet), high IL risk
    Best for: Active managers with >$10K positions
    Gas warning: Break-even ~3 days per rebalance

  #2 V3 0.05% Medium (±15%) — RECOMMENDED
    Pros: Strong APY with manageable rebalancing, 80%+ time-in-range
    Cons: Moderate IL during large moves
    Best for: Most LPs with $1K+ positions
    Gas warning: Break-even ~1 day per rebalance

  #3 V3 0.05% Wide (±50%) — LOW MAINTENANCE
    Pros: Rarely needs rebalancing, low IL, almost passive
    Cons: Lower capital efficiency, lower APY
    Best for: Passive LPs, small positions where gas matters

  #6 V2 0.30% Full Range — SET AND FORGET
    Pros: Zero maintenance, no range management, battle-tested
    Cons: Lowest returns, less capital efficient
    Best for: First-time LPs, long-term holders who don't want to manage

  Ready to proceed? Choose a strategy and say "Add liquidity with strategy #2"
```

## 重要说明

- 该功能仅提供分析结果，不执行任何操作。如需实施某个策略，请使用`manage-liquidity`。
- 净APY = 费用APY - 预期利息损失（IL）。务必同时显示这两个数值。
- 每个链的重新平衡所需Gas费用都会被纳入比较结果中。
- 当选择“all”链进行跨链比较时，会突出显示L2网络的Gas优势。
- lp-strategist内部会使用`pool-researcher`获取数据，并通过`risk-assessor`进行风险评估。

## 错误处理

| 错误类型                | 用户可见的消息                                      | 建议的操作                                      |
| ---------------------- | --------------------------------------------------------- | ----------------------------------- |
| 代币未找到              | “无法找到代币X。”                                      | 提供代币的合约地址                         |
| 未找到对应的池             | “未找到X/Y的池。”                                      | 尝试其他代币或链                        |
| 数据不足                | “数据不足，无法进行可靠比较。”                               | 可能是因为相关池太新                         |
| 代理不可用              | “LP策略专家当前不可用。”                                  | 检查代理的配置                         |