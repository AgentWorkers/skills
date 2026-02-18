---
name: solana-connect
description: OpenClaw Solana Connect — 一款专为AI代理设计的安全工具包，用于与Solana区块链进行交互。该工具包提供了私钥保护功能、交易上限设置、模拟运行模式（dry-run mode），以及对大额交易的人工确认机制。
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "env": ["SOLANA_RPC_URL", "MAX_SOL_PER_TX", "MAX_TOKENS_PER_TX", "HUMAN_CONFIRMATION_THRESHOLD"],
          },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "@solana/web3.js",
              "label": "Install Solana Web3.js",
            },
            {
              "id": "npm",
              "kind": "npm", 
              "package": "tweetnacl",
              "label": "Install TweetNaCl",
            },
            {
              "id": "npm",
              "kind": "npm",
              "package": "bs58",
              "label": "Install bs58",
            },
          ],
      },
  }
---
# 🔗 OpenClaw Solana Connect v3.0

> 一个安全的工具包，用于AI代理与Solana区块链进行交互

## 🛡️ 安全特性

- **私钥保护** - 私钥永远不会被暴露给代理程序
- **交易限额** - 可配置的交易限额
- **模拟模式** - 在发送交易前进行模拟（默认设置）
- **人工确认** - 大额交易需要人工确认
- **默认使用测试网** - 默认情况下使用测试网以确保安全

## 功能说明

| 功能 | 是否可用 | 说明 |
|----------|--------|-------------|
| `generateWallet()` | ✅ 可用 | 生成钱包地址 |
| `connectWallet()` | ✅ 可用 | 验证钱包地址 |
| `getBalance()` | ✅ 可用 | 读取SOL/代币余额 |
| `getTransactions()` | ✅ 可用 | 读取交易历史记录 |
| `getTokenAccounts()` | ✅ 可用 | 读取代币持有情况 |
| `sendSol()` | ✅ 可用 | 安全地发送SOL |

## 安装

```bash
clawhub install solana-connect
```

## 环境变量

- `SOLANA_RPC_URL` - RPC端点（默认：测试网）
- `MAX_SOL_PER_TX` - 每笔交易的SOL最大数量（默认：10）
- `MAX_TOKENS_PER_TX` - 每笔交易的代币最大数量（默认：10000）
- `HUMAN_CONFIRMATION_THRESHOLD` - 需要人工确认的SOL金额阈值（默认：1）

## 使用方法

```javascript
const { generateWallet, getBalance, sendSol, getConfig } = require('./scripts/solana.js');

// Generate wallet (address only - private key protected)
const wallet = generateWallet();
console.log('Address:', wallet.address);

// Check balance
const balance = await getBalance(wallet.address);

// Send SOL (DRY-RUN by default - simulation only)
const result = await sendSol(privateKey, toAddress, 0.5, { dryRun: true });
console.log('Simulation:', result);

// Send real transaction
const tx = await sendSol(privateKey, toAddress, 0.5, { dryRun: false, skipConfirmation: true });
console.log('Signature:', tx.signature);
```

## 安全设置

```javascript
// Dry-run (simulation) - safe, doesn't send
await sendSol(key, to, amount, { dryRun: true });

// Real transaction - requires explicit flag
await sendSol(key, to, amount, { dryRun: false });

// Skip human confirmation (for automated agents)
await sendSol(key, to, amount, { dryRun: false, skipConfirmation: true });
```

---

**安全提示：** 请勿将私钥硬编码在代码中。建议使用环境变量来管理私钥信息。