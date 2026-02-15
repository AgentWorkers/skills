---
name: eyebot-liquidbot
description: DEX（去中心化交易所）部署的流动性池管理专家
version: 1.2.0
author: ILL4NE
metadata:
  chains: [base, ethereum, polygon, arbitrum]
  category: defi-liquidity
---

# LiquidBot 💧

**智能流动性管理**

利用人工智能优化的策略，管理各大去中心化交易所（DEX）中的流动性提供者（LP）头寸。实时监控非永久性损失（impermanent loss），自动复利奖励，并提升资本使用效率。

## 主要功能

- **多DEX支持**：Uniswap、SushiSwap、PancakeSwap、Aerodrome
- **非永久性损失监控**：实时跟踪非永久性损失情况
- **头寸分析**：提供全面的LP性能指标
- **流动性优化**：优化流动性分布（V3版本）
- **自动复利**：自动将奖励再投资

## 功能说明

| 功能 | 详细描述 |
|---------|-------------|
| 添加流动性** | 将LP部署到任何支持的DEX中 |
| 提取流动性**：提供滑点保护机制的提取服务 |
| 重新平衡头寸**：优化LP头寸的分布 |
| 监控非永久性损失**：实时监测非永久性损失情况 |
- **获取奖励**：自动领取并复利奖励 |

## 支持的去中心化交易所

- Uniswap V2/V3
- SushiSwap
- PancakeSwap
- Aerodrome（基础版本）
- QuickSwap（Polygon）

## 使用说明

```bash
# Add liquidity
eyebot liquidbot add ETH/USDC 1.0 --dex uniswap

# Check position
eyebot liquidbot position <lp_address>

# Remove liquidity
eyebot liquidbot remove <lp_address> 50%
```

## 帮助支持

Telegram：@ILL4NE