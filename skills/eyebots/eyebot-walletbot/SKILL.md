---
name: eyebot-walletbot
description: 钱包操作与投资组合管理
version: 1.2.0
author: ILL4NE
metadata:
  chains: [base, ethereum, polygon, arbitrum]
  category: wallet-management
---

# WalletBot 👛

**全面的钱包管理功能**

支持管理多个钱包、追踪投资组合，并在多个区块链上执行交易。

## 主要功能

- **多链支持**：提供所有区块链的统一视图
- **投资组合追踪**：实时更新账户余额
- **交易历史**：完整的交易记录
- **代币管理**：添加/隐藏代币
- **gas费用优化**：智能估算交易所需的gas费用

## 主要功能

| 功能 | 说明 |
|----------|-------------|
| 查看余额 | 查看所有代币的余额 |
| 发送交易 | 转移代币或ETH |
| 查看交易历史 | 查看所有的交易记录 |
| 代币管理 | 管理代币列表 |
| gas费用估算 | 智能估算交易所需的gas费用 |

## 支持的区块链

Ethereum • Base • Polygon • Arbitrum • Optimism • BSC

## 投资组合功能

- 投资组合的总价值（以美元计）
- 24小时价值变化追踪
- 代币分配图表
- 历史表现分析
- 盈亏追踪

## 使用说明

```bash
# Check balances
eyebot walletbot balance <address>

# Send tokens
eyebot walletbot send ETH <to> 0.1

# View history
eyebot walletbot history <address> --limit 20
```

## 售后支持

Telegram: @ILL4NE