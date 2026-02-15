---
name: usdc-escrow
description: "在 Base 平台上，实现一种无信任机制的 USDC 代管服务，用于代理之间的支付。用户可以通过简单的命令来创建、释放或处理代管交易（即资金托管）。"
metadata:
  openclaw:
    emoji: "🔐"
    requires:
      bins: [curl, jq]
---

# USDC托管服务

## 概述
该服务为Base平台上的代理之间进行无信任支付提供了USDC托管功能。它允许AI代理通过智能合约来创建、管理和解决支付托管问题。

## API
所有脚本默认指向`https://api.payclawback.xyz`。如需使用其他后端，请设置：
- `ESCROW_API_URL` - 替换API地址（可选）

## 可用命令

### 创建托管
创建一个新的托管账户，用于存放受益人的USDC。
```bash
./scripts/create-escrow.sh <beneficiary_address> <amount_usdc> "<description>" <deadline_hours>
```
示例：`./scripts/create-escrow.sh 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD28 10 "数据分析师费用" 48`

### 列出托管账户
列出所有托管账户，可选择按状态或存款人进行过滤。
```bash
./scripts/list-escrows.sh [--state active|released|disputed|refunded|expired] [--depositor 0x...]
```

### 获取托管详情
通过ID获取特定托管账户的详细信息。
```bash
./scripts/get-escrow.sh <escrow_id>
```

### 释放托管资金
将托管的资金释放给受益人。
```bash
./scripts/release-escrow.sh <escrow_id>
```

### 争议处理
对活跃的托管账户开启争议处理。
```bash
./scripts/dispute-escrow.sh <escrow_id>
```

### 争议解决
作为仲裁者解决争议。
```bash
./scripts/resolve-dispute.sh <escrow_id> <true|false>
```
- `true`：将资金释放给受益人
- `false`：将资金退还给存款人

### 收回过期托管账户的资金
从过期的托管账户中收回资金。
```bash
./scripts/claim-expired.sh <escrow_id>
```

## 工作流程示例
1. 代理A希望向代理B支付服务费用。
2. 代理A创建托管账户：`./scripts/create-escrow.sh 0xAgentB 50 "情感分析任务" 24`
3. 代理B完成服务。
4. 代理A释放支付款项：`./scripts/release-escrow.sh 1`

## 工作原理
- USDC被锁定在Base平台上的[经过验证的智能合约中](https://sepolia.basescan.org/address/0x2a27844f3775c3a446d32c06f4ebc3a02bb52e04)。
- 托管账户有截止日期——逾期后资金将退还给存款人。
- 任何一方都可以提交争议以供仲裁解决。
- AI仲裁代理将公正地解决争议。
- 所有交易均记录在链上且可验证。

## API参考
请参阅`references/api-docs.md`以获取完整的API文档。