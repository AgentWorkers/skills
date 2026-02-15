---
name: find-yield
description: 在 Uniswap 上，根据风险承受能力和最低 TVL（Total Value Locked，锁定总价值）筛选出收益率最高的 LP（Liquidated Pool）池。当用户询问最佳收益率、最高年化收益率（APY）的池，或者希望了解在哪里可以获得费用收益时，可以使用这些信息。
model: opus
allowed-tools: [Task(subagent_type:opportunity-scanner)]
---

# 查找最高收益的流动性池（LP）机会

## 概述

该功能用于在 Uniswap 平台上查找收益最高的流动性池（LP）机会，支持根据风险承受能力、最低 TVL（Total Value Locked，锁定总价值）以及可选的资本金额进行筛选。这是 `scan-opportunities` 功能的简化版本，仅返回与流动性池相关的收益信息（不包括套利或新池的扫描结果）。

该功能通过 `opportunity-scanner` 代理来执行筛选操作，该代理专门用于处理流动性池相关的查询。

## 使用场景

当用户提出以下问题时，可激活此功能：
- “Uniswap 上收益最高的 LP 机会”
- “APY（年化收益率）最高的流动性池”
- “在哪里可以获得费用收益”
- “回报最高的流动性池”
- “在哪里能获得最多的收益”

## 参数

| 参数                | 是否必填 | 默认值    | 说明                                              |
|------------------|--------|---------|---------------------------------------------------------|
| chains             | 否       | 所有链    | 指定链或“所有链”                                        |
| riskTolerance     | 否       | 中等     | “保守”、“中等”、“激进”                                        |
| capital           | 否       | —        | 可用资本（用于合理排序）                                      |
| minTvl            | 否       | 100,000 美元 | 考虑纳入筛选的流动性池的最低 TVL                                   |

## 工作流程

1. 从用户请求中提取相关参数。
2. 调用 `opportunity-scanner` 代理：执行 `Task(subagent_type: opportunity-scanner)`，并传入 `type: "lp"` 以及用户的筛选条件。该代理会扫描所有流动性池，根据风险调整后的年化收益率（APY）对结果进行排序，并返回排名最高的几个机会。
3. 将筛选结果以表格形式呈现。

## 输出格式

```text
Top LP Yields (moderate risk, min $100K TVL):

  | Rank | Pool                | Chain    | APY 7d | TVL    | Risk   |
  | ---- | ------------------- | -------- | ------ | ------ | ------ |
  | 1    | WETH/USDC 0.05%     | Ethereum | 21.3%  | $332M  | LOW    |
  | 2    | ARB/WETH 0.30%      | Arbitrum | 18.5%  | $15M   | MEDIUM |
  | 3    | WETH/USDC 0.05%     | Base     | 15.2%  | $45M   | LOW    |
  | 4    | WBTC/WETH 0.30%     | Ethereum | 12.1%  | $120M  | LOW    |
  | 5    | OP/WETH 0.30%       | Optimism | 11.8%  | $8M    | MEDIUM |

  Note: APY is based on 7-day historical fee revenue. Past performance
  does not guarantee future returns. IL risk not included in APY figures.
```

## 重要说明

- 年化收益率（APY）数据为历史数据，不具保障性。使用前请务必考虑潜在风险。
- 较高的年化收益率通常伴随着较高的风险。
- 保守的风险筛选策略会排除 TVL 低于 100 万美元的流动性池以及价格波动较大的交易对。
- 经风险调整后的收益率已考虑到了潜在的非永久性损失。

## 错误处理

| 错误类型                | 显示给用户的提示信息 | 建议的操作                                      |
|------------------|------------------|----------------------------------------|
| 未找到符合条件的流动性池     | “没有符合您风险/TVL 策略的流动性池。”         | 提高最低 TVL 要求或调整风险承受能力                         |
| 无法访问目标链           | “无法扫描 [链名]。数据可能不完整。”         | 请重试或缩小搜索范围                                   |