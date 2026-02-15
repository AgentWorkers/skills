---
name: eyebot-vaultbot
description: 安全钱包管理及多签名保管库
version: 1.2.0
author: ILL4NE
metadata:
  chains: [base, ethereum, polygon, arbitrum]
  category: wallet-security
---

# VaultBot 🔐

**安全资产管理**

创建并管理具有细粒度访问控制的多签名保险库，保护团队资金并自动化财务操作。

## 主要功能

- **多签名保险库**：2-of-3、3-of-5等多种签名机制；可自定义签名数量阈值
- **时间锁定**：延迟执行交易以确保安全
- **支出限制**：设置每日/每周的支出上限
- **角色管理**：为不同用户分配精细的权限
- **审计追踪**：记录所有交易明细

## 保险库类型

| 保险库类型 | 使用场景 |
|------|----------|
| 团队财务保险库 | 公司资金管理 |
| DAO保险库 | 受治理结构控制的资产 |
| 个人安全存储空间 | 用于存储冷存储数据（数据可恢复） |
| 代管账户 | 用于无信任交易场景 |

## 安全特性

- 支持硬件钱包集成
- 提供多种社交账号恢复方式
- 支持交易模拟功能
- 允许设置资产访问白名单
- 具有紧急暂停交易的功能

## 使用说明

```bash
# Create a vault
eyebot vaultbot create --signers 3 --threshold 2

# Add signer
eyebot vaultbot add-signer <vault> <address>

# Propose transaction
eyebot vaultbot propose <vault> send 1 ETH <to>
```

## 帮助支持

Telegram: @ILL4NE