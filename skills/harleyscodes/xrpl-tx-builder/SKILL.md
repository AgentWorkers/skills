---
name: xrpl-tx-builder
description: Build and sign XRP Ledger transactions. Use for: (1) Creating payment transactions, (2) Building NFT mint/burn transactions, (3) Signing with Xaman wallet, (4) Submitting to XRPL.
---

# XRPL 交易构建器

## 设置

```bash
npm install xrpl
```

## 基本支付

```typescript
import { Client, Wallet, Payment } from 'xrpl';

const client = new Client('wss://xrplcluster.com');

// Build payment tx
const tx: Payment = {
  TransactionType: 'Payment',
  Account: wallet.address,
  Destination: 'rDestinationAddress...',
  Amount: '1000000', // drops (1 XRP = 1,000,000 drops)
  DestinationTag: 12345 // optional
};
```

## 提交交易（Xaman签名）

```typescript
// After user signs with Xaman, submit:
const txBlob = signedTransactionBlob; // from Xaman payload
const result = await client.submit(txBlob);
```

## 常见交易类型

### 支付
```typescript
{
  TransactionType: 'Payment',
  Account: 'r...',
  Destination: 'r...',
  Amount: '1000000', // drops
  DestinationTag: 123
}
```

### NFTokenMint
```typescript
{
  TransactionType: 'NFTokenMint',
  Account: 'r...',
  NFTokenTaxon: 0,
  Issuer: 'r...',
  TransferFee: 5000, // 5% royalty
  Flags: 8, // burnable
  URI: 'ipfs://...'
}
```

### SetAccountRoot
```typescript
{
  TransactionType: 'SetAccountRoot',
  Account: 'r...',
  EmailHash: 'abc123...',
  Domain: 'example.com'
}
```

## 关键概念

- **Drops**：1 XRP = 1,000,000 drops
- **地址**：经典的r-address（以‘r’开头）
- **目标标签**：支付时的可选备注信息
- **标志**：特定于交易的选项（请参阅XRPL文档）

## RPC端点

- `wss://xrplcluster.com`（公共端点）
- `wss://s1.ripple.com`（Ripple官方端点）