---
name: eyebot-tokenforge
description: 这款由人工智能驱动的工具专为 ERC-20、BEP-20 标准代币以及自定义代币的部署而设计。它能够自动化处理代币的创建、发布、分配和管理等流程，显著提升代币发行的效率与安全性。
version: 1.2.0
author: ILL4NE
metadata:
  chains: [base, ethereum, polygon, arbitrum]
  category: token-deployment
---

# TokenForge 🔨

**基于AI的代币部署**

部署具备生产级功能的代币，支持优化后的配置。支持多种标准、自动验证以及可定制的代币经济模型。

## 主要特性

- **多标准支持**：ERC-20、BEP-20以及自定义实现
- **自动验证**：在区块链浏览器上自动验证源代码
- **代币经济模型构建器**：可配置代币的供应量、税收、销毁规则及分配方式
- **安全优先**：内置反机器人和反恶意攻击保护机制
- **Gas优化**：采用高效合约以降低部署成本

## 功能列表

| 功能 | 详细描述 |
|---------|-------------|
| 标准代币** | 支持基本的ERC-20代币功能（铸造/销毁） |
| 反射代币** | 为持有者自动发放奖励 |
- **税收代币**：支持自定义税率的买卖交易税收 |
- **通缩机制**：交易发生时自动销毁代币 |
- **流动性生成**：自动生成流动性对（LP） |

## 支持的区块链网络

Base • Ethereum • Polygon • Arbitrum • BSC

## 使用说明

```bash
# Deploy a standard token
eyebot tokenforge deploy --name "MyToken" --symbol "MTK" --supply 1000000

# Deploy with taxes
eyebot tokenforge deploy --name "TaxToken" --buy-tax 2 --sell-tax 3

# Verify contract
eyebot tokenforge verify <contract_address>
```

## 帮助支持

Telegram: @ILL4NE