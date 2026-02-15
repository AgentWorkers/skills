---
name: eyebot-tradebot
description: 高性能交易与掉期执行引擎
version: 1.2.0
author: ILL4NE
metadata:
  chains: [base, ethereum, polygon, arbitrum]
  category: trading
---

# TradeBot 📈

**智能交易执行**

通过整合400多个流动性提供商的信息，执行最优交易路径的代币互换操作。支持限价单、定期投资（DCA）策略以及市场均衡价值（MEV）保护功能。

## 主要功能

- **交易路径聚合**：从所有去中心化交易所（DEX）中选择最优价格
- **市场均衡价值保护**：采用私下交易方式，避免被抢先交易
- **限价单**：设置目标价格以实现自动执行
- **定期投资引擎**：支持美元成本平均策略
- **多跳路由**：通过复杂路由机制获取最佳交易费率

## 功能列表

| 功能        | 描述                                      |
|------------|-----------------------------------------|
| 代币互换     | 即时执行代币互换操作                          |
| 限价单       | 根据价格触发交易执行                            |
| 定期投资     | 定期自动买入策略                            |
| 报价        | 获取最优交易费率预览                          |
| 交易历史     | 查看所有交易记录                            |

## 支持的聚合器

- 1inch        |
- OpenOcean     |
- 0x Protocol    |
- Paraswap      |
- 原生去中心化交易所路由            |

## 使用说明

```bash
# Instant swap
eyebot tradebot swap ETH USDC 0.5

# Set limit order
eyebot tradebot limit BUY ETH 0.5 --price 2000

# Start DCA
eyebot tradebot dca ETH 100 --interval daily
```

## 售后支持

Telegram: @ILL4NE