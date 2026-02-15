---
name: track-performance
description: 跟踪 Uniswap 的长期锁定池（LP）头寸表现——检查哪些头寸需要关注、是否超出正常范围，或者是否有未收取的费用。当用户询问其头寸状况时，可以使用此功能。
model: opus
allowed-tools: [Task(subagent_type:portfolio-analyst)]
---

# 性能跟踪

## 概述

该功能用于跟踪Uniswap流动性提供者（LP）头寸的性能，重点关注自上次检查以来的变化和异常情况。具体操作由`portfolio-analyst`代理负责，该代理会检查头寸状态、费用累积情况，并识别需要关注的头寸。

## 使用场景

当用户提出以下问题时，可激活此功能：

- “我的头寸表现如何？”
- “请查看我的LP投资表现”
- “是否有需要关注的头寸？”
- “哪些头寸超出了预设范围？”
- “我今天赚了多少钱？”
- “请更新头寸状态”

## 参数

| 参数          | 是否必填 | 默认值                | 说明                                      |
|--------------|--------|-------------------|-----------------------------------------|
| wallet       | 否      | 配置好的代理钱包地址         | 需要跟踪的钱包地址                          |
| chains        | 否      | 所有链                 | 指定链或“所有链”                             |
| since        | 否      | 上次检查时间             | 时间范围：24小时、7天、30天                          |

## 工作流程

1. 从用户请求中提取参数：确定钱包地址、链筛选条件以及时间范围。
2. 调用`portfolio-analyst`代理：执行`Task(subagent_type:portfolio-analyst)`任务，重点关注性能跟踪和异常情况处理。代理会检查所有头寸，识别状态变化，并标记需要关注的头寸。
3. 呈现结果：以性能总结的形式展示结果，并附带可操作的提醒信息。

## 输出格式

```text
Performance Update (last 24h)

  Overall: +$320 (+0.26%)

  Positions:
    USDC/WETH 0.05% (Ethereum) — IN RANGE ✓
      Fees earned (24h): $180
      Value change:      +$120
      Status: Healthy

    UNI/WETH 0.30% (Ethereum) — OUT OF RANGE ⚠
      Fees earned (24h): $0 (not earning — out of range)
      Value change:      -$50
      Status: Needs rebalance

  Action Items:
    1. Rebalance UNI/WETH position (out of range since 6h ago)
    2. Consider collecting $1,200 in accumulated fees from UNI/WETH
```

## 重要说明

- 全部功能由`portfolio-analyst`代理负责处理，不涉及直接调用MCP工具。
- 超出预设范围的头寸无法产生费用，可能需要重新平衡。
- 提出的操作建议仅供参考，并非自动执行。
- 由于RPC或子图同步的原因，性能数据可能会有轻微延迟。

## 错误处理

| 错误类型           | 显示给用户的消息                                      | 建议的操作                                      |
|------------------|--------------------------------------------------|-------------------------------------------|
| 未配置钱包       | “未配置钱包。”                                      | 请设置WALLET_TYPE和PRIVATE_KEY                   |
| 未找到头寸       | “未找到Uniswap头寸。”                                    | 可能是因为钱包未进行LP投资                     |
| 数据延迟         | “头寸数据可能存在延迟。”                                    | 请稍后再试                         |