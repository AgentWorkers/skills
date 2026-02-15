---
name: portfolio-report
description: 生成一份全面的钱包在所有链上Uniswap持仓的报表——涵盖总价值、盈亏（PnL）、手续费收入、非永久性损失以及持仓构成。当用户询问其持仓情况、收益或投资组合概览时，可使用此报表。
model: opus
allowed-tools: [Task(subagent_type:portfolio-analyst)]
---

# 投资组合报告

## 概述

该功能会生成一个全面的投資组合报告，展示钱包在所有支持的网络（chain）上的 Uniswap 持仓情况。具体工作由 `portfolio-analyst` 代理负责：发现持仓、计算盈亏（PnL）、追踪手续费收入以及分析持仓构成。

## 使用场景

当用户提出以下请求时，可激活此功能：
- “显示我的持仓”
- “生成投资组合报告”
- “我的 Uniswap 盈亏是多少？”
- “我通过手续费赚了多少钱？”
- “哪些持仓超出了预设范围？”
- “我的投资组合总价值是多少？”
- “汇总我的 LP 持仓情况”

## 参数

| 参数                | 是否必填 | 默认值                | 说明                                      |
|------------------|--------|------------------|-----------------------------------------|
| wallet            | 否       | 配置好的代理钱包地址        | 需要分析的钱包地址                          |
| chains             | 否       | 所有网络               | 可选择特定网络或“所有网络”                         |
| focus              | 否       | “全部信息”             | 可选择“持仓”、“盈亏”、“手续费”或“全部信息”                   |

## 工作流程

1. **从用户请求中提取参数**：确定钱包地址、网络筛选条件以及关注的重点（持仓、盈亏、手续费或全部信息）。
2. **委托给 `portfolio-analyst` 代理**：调用 `Task(subagent_type:portfolio-analyst)` 并传递相关参数。代理会查询所有网络上的持仓信息，计算盈亏并分析持仓构成。
3. **展示结果**：将分析结果以用户友好的格式呈现。

## 输出格式

```text
Portfolio Report: 0xf39F...2266

  Total Value: $125,000
    LP Positions: $95,000
    Idle Tokens:  $28,000
    Uncollected:  $2,000

  PnL Summary:
    Realized:    +$5,200
    Unrealized:  +$3,800
    Gas Costs:   -$450
    Net PnL:     +$8,550 (+7.3%)

  Positions (2):
    1. USDC/WETH 0.05% (V3, Ethereum) — IN RANGE
       Value: $50,000 | PnL: +$2,000 | Fees: $800 uncollected
    2. UNI/WETH 0.30% (V3, Ethereum) — OUT OF RANGE
       Value: $45,000 | PnL: +$2,000 | Fees: $1,200 uncollected

  Recommendations:
    - Collect $1,200 in fees from UNI/WETH position
    - Rebalance UNI/WETH position (currently out of range)
```

## 重要说明

- 所有处理工作均由 `portfolio-analyst` 代理完成，无需直接调用 MCP 工具。
- 盈亏（PnL）包含网络交易产生的 Gas 费用；某个持仓在交易前可能盈利，但在交易后可能转为亏损。
- 持仓的收益以绝对美元价值和百分比两种方式显示。
- 由于 RPC 请求或子图同步问题，数据可能存在轻微延迟。

## 错误处理

| 错误类型                | 用户可见的提示信息 | 建议的操作                         |
|------------------|------------------|----------------------------------------|
| 未配置钱包            | “未配置钱包。”                 | 请设置 WALLET_TYPE 和 PRIVATE_KEY                |
| 未找到持仓            | “未找到该钱包的 Uniswap 持仓。”             | 可能该钱包未参与 LP 活动                   |
| 无法连接目标网络        | “无法连接到 X 网络。”                | 请稍后重试                        |