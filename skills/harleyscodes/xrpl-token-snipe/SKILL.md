---
name: firstledger-snipe
description: Snipe new token launches on XRPL via FirstLedger. Use for: (1) Detecting new token issuances, (2) Monitoring mempool for fresh offers, (3) Front-running token buys, (4) Managing XRP reserves.
---

# FirstLedger 抢购新代币

## 概述

实时监控 XRPL 平台上的新代币发行，并在其他用户之前迅速完成购买。

## FirstLedger 的 API 端点

- **WebSocket**: `wss://xlrps-1.xrpl.link/`
- **REST**: `https://xlrps-1.xrpl.link/api/v1/`

## 检测新代币

### 订阅交易信息
```typescript
const ws = new WebSocket('wss://xlrps-1.xrpl.link/');

ws.send(JSON.stringify({
  command: 'subscribe',
  transactions: true
}));

// Watch for Payment transactions with new tokens
ws.onmessage = (msg) => {
  const tx = JSON.parse(msg.data);
  if (tx.TransactionType === 'Payment' && tx.Amount?.currency) {
    console.log('New token:', tx.Amount);
  }
};
```

### 检查代币发行者的相关标志
```typescript
// Key flags to audit before buying:
const flags = {
  lsfDisableMaster: 0x00080000,  // CANNOT mint more - SAFE
  lsfRipple: 0x00020000,         // Default ripple
  lsfDefaultRipple: 0x00040000,  // Trustline default
  lsfRequireAuth: 0x00010000      // Must be authorized
};

// SKIP if:
- lsfDisableMaster is NOT set (issuer can rug)
- No requireAuth (anyone can hold)
```

## 执行购买操作
```typescript
const { Client, Wallet } = require('xrpl');
const client = new Client('wss://xrplcluster.com');

const tx = {
  TransactionType: 'Payment',
  Account: wallet.address,
  Destination: issuerAddress,
  Amount: {
    currency: tokenCode, // e.g., 'SYM123'
    issuer: issuerAddress,
    value: '100' // Amount to buy
  },
  DestinationTag: 1 // For tracking
};

const result = await client.submit(tx, { wallet });
```

## 安全性检查

✅ **必须验证的条件**：
1. `lsfDisableMaster` 标志已设置（表示不再进行代币铸造）
2. 合同所有权已转让
3. 代币具有足够的流动性（通过检查信任线确认）
4. 该代币不是“蜜罐”（购买后可以立即出售）

❌ **如果满足以下条件，则跳过此步骤**：
- 代币未经过审计
- 代币缺乏流动性
- 合同所有权尚未转让

## 风险评估

- **高风险**：仅交易你能够承受损失的资金
- 购买前务必对代币的相关信息进行审计
- 保留至少 10 个 XRP 作为交易费用