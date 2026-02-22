---
name: defi-yield-scanner
version: 1.0.0
description: 扫描去中心化金融（DeFi）协议，寻找最佳的收益机会。涵盖 Aave、Compound、Curve、Yearn、Uniswap v3 以及新兴的第二层（L2）协议。比较各协议的年化收益率（APY）与风险水平，追踪锁定资金（TVL）的变化，并及时发现新的收益 farming 机会。适用于需要寻找 DeFi 收益 farming 机会、比较不同协议的 APY、获取流动性挖矿提醒或优化稳定币收益的场景。
author: JamieRossouw
tags: [defi, yield, farming, aave, curve, uniswap, crypto, passive-income]
---
# DeFi 收益扫描器

这是一个自动化的扫描工具，用于查找超过 10 种 DeFi 协议中的收益机会。

## 扫描内容

- **Aave v3**（Polygon、Arbitrum、Base）：供应量年化收益率（APY）、借款量年化收益率（APY）、利用率
- **Compound v3**：USDC/USDT 的供应量利率、COMP 奖励的年利率（APR）
- **Curve Finance**：稳定币池、CRV 的发行量、权重计算
- **Uniswap v3**：高流动性头寸的交易费用等级及年化收益率
- **Yearn Finance**：Yearn 金融产品的年化收益率，包括收益收割策略的回报

## 收益排名

每个收益机会的评分标准包括：
1. **年化收益率（APY）**：原始收益率 + 经过代币发行量调整后的收益率
2. **风险**：智能合约的运行时间、审计状态、总价值（TVL）
3. **可持续性**：经过代币发行量调整后的实际年化收益率（与原始收益率的对比）
4. ** gas 使用效率**：在 Polygon/L2 网络上的使用效率（与主网相比）

## 使用方法

您可以输入如下指令：
- “查找 Polygon 上当前最高的稳定币收益”
- “比较 Aave、Compound、Curve 三种协议中的 USDC 收益”

该工具会获取实时的年化收益率数据，应用风险筛选条件，并返回经过排名的收益机会以及相应的操作指南。

## 数据来源

- DeFiLlama API (`api.llama.fi`)：总价值（TVL）、年化收益率（APY）、协议元数据
- Aave 子图（The Graph）
- Curve Registry (`curve.fi/api`)
- Yearn Finance API (`yearn.fi/api`)

## 输出格式

```
Protocol | Pool          | APY (base) | APY (rewards) | TVL    | Risk  | Rec
---------|---------------|------------|---------------|--------|-------|-----
Aave v3  | USDC (Polygon)| 2.71%      | 0.00%         | $841M  | LOW   | ✅
Curve    | 3pool         | 1.80%      | 4.20% CRV     | $432M  | LOW   | ✅
Yearn    | USDC vault    | 4.50%      | 0.00%         | $120M  | MED   | ⚠️
```