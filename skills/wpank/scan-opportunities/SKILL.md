---
name: scan-opportunities
description: 扫描所有 Uniswap 部署中的低价格买入（LP）机会、套利机会以及高收益投资池。当用户询问最佳投资机会、高收益投资池或套利方案时，可使用此功能。
model: opus
allowed-tools: [Task(subagent_type:opportunity-scanner)]
---

# 扫描投资机会

## 概述

该功能会扫描所有Uniswap平台上的锁定收益（LP）机会、价格差异以及高收益投资池，然后将分析结果委托给`opportunity-scanner`代理进行处理。该代理会分析这些投资池，比较价格，并评估潜在的投资机会。

## 使用场景

当用户提出以下请求时，可激活此功能：
- “寻找最佳锁定收益投资机会”
- “有套利机会吗？”
- “显示高收益的投资池”
- “哪些投资池的交易量较大？”
- “我应该把资金投入哪些投资池？”
- “目前有哪些最佳的投资机会？”

## 参数

| 参数                | 是否必填 | 默认值       | 说明                                                  |
|------------------|---------|-------------|---------------------------------------------------------|
| type                | 否       | all         | 可选值：`lp`（锁定收益）、`arb`（套利）、`new-pools`（新投资池）或`all`           |
| chains              | 否       | all         | 可选值：特定链或`all`                                        |
| riskTolerance       | 否       | moderate     | 可选值：`conservative`（保守）、`moderate`（中等）、`aggressive`（激进）       |
| minTvl             | 否       | $50,000       | 投资池被考虑的最小交易量（TVL）阈值                        |

## 工作流程

1. 从用户请求中提取参数：确定投资机会的类型、目标链、风险承受能力和最小交易量（TVL）。
2. 委托`opportunity-scanner`代理执行任务：使用`Task(subagent_type:opportunity-scanner)`并传递相关参数。该代理会扫描高年化收益率（APY）的投资池、套利机会（交易费用后的收益差大于0.5%），以及交易量在7天内增长超过100%的新投资池。
3. 以排名列表的形式呈现结果，并附上每个投资机会的风险评级。

## 输出格式

```text
Opportunities Found: 5

  1. LP: WETH/USDC 0.05% (Ethereum)
     APY: 21.3% | TVL: $332M | Risk: LOW
     Why: Highest volume-to-TVL ratio on mainnet

  2. LP: ARB/WETH 0.30% (Arbitrum)
     APY: 35.2% | TVL: $12M | Risk: MEDIUM
     Why: Growing volume trend (+45% 7d)

  3. New Pool: AGENT/WETH 0.30% (Base)
     APY: 120%* | TVL: $500K | Risk: HIGH
     Why: New pool with strong early volume (*projected, limited data)
```

## 重要说明

- 所有年化收益率（APY）数据均为历史估算值，不代表实际收益。
- 高收益投资池通常伴随较高风险（如代币流动性低、交易量小或为新发行的代币）。
- 每个投资机会的风险评级由代理根据其内部风险评估系统生成。
- 套利机会具有时效性，可能在执行前就消失。

## 错误处理

| 错误类型                | 显示给用户的消息                                      | 建议的操作                                      |
|------------------|--------------------------------------------------|---------------------------------------------------------|
| 未找到符合条件的投资机会    | “未找到符合您条件的投资机会。”                          | 调整风险承受能力或最小交易量阈值                         |
| 无法访问目标链            | “无法扫描[目标链]。数据可能不完整。”                         | 重新尝试或缩小搜索范围                                   |