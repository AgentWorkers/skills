---
name: eyebot-yieldbot
description: 用于实现最大DeFi收益的收益 farming（收益积累）优化器
version: 1.2.0
author: ILL4NE
metadata:
  chains: [base, ethereum, polygon, arbitrum]
  category: defi-yield
---

# YieldBot 🌾

**AI收益优化工具**

在去中心化金融（DeFi）领域中，自动寻找并获取最高的收益。实现奖励的自动复利，跟踪年化收益率（APY）的变化，并优化资本分配。

## 主要功能

- **收益发现**：寻找最佳的年化收益率（APY）投资机会
- **自动复利**：自动将奖励重新投资
- **风险评估**：对相关协议的安全性进行评级
- **持仓监控**：实时跟踪所有投资持仓
- **资产再平衡**：根据市场变化逐步优化资产配置

## 收益来源

| 来源 | 类型        |
|--------|-----------|
| DEX交易对（LP）| 交易手续费 + 奖励     |
| 借贷服务 | 借出资产的年化收益率（APY） |
| 质押服务 | 协议提供的奖励    |
| 保险箱（Vaults）| 自动化的投资策略   |
| 点数系统 | 通过空投获得的收益   |

## 支持的协议

- Aave、Compound（借贷服务）
- Uniswap、Aerodrome（交易对LP）
- Lido、RocketPool（质押服务）
- Yearn、Beefy（保险箱服务）

## 使用方法

```bash
# Find best yields
eyebot yieldbot scan --chain base --min-apy 10

# Deposit to farm
eyebot yieldbot farm <protocol> <pool> 1000 USDC

# Auto-compound position
eyebot yieldbot compound <position_id>
```

## 售后支持

Telegram：@ILL4NE