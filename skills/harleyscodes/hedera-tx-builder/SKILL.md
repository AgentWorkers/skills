---
name: hedera-tx-builder
description: Build and sign Hedera transactions. Use for: (1) Creating HBAR transfers, (2) Token operations, (3) Smart contract calls, (4) Submitting to Hedera network.
---

# Hedera 交易构建器

## 设置

```bash
npm install @hashgraph/sdk
```

## 客户端设置

```typescript
import { Client, AccountBalanceQuery, Hbar } from '@hashgraph/sdk';

const client = Client.forMainnet();
// Or for testnet:
const client = Client.forTestnet();
```

## 转移 HBAR

```typescript
import { TransferTransaction, Hbar } from '@hashgraph/sdk';

const tx = new TransferTransaction()
  .addHbarTransfer(fromAccountId, new Hbar(-100)) // send
  .addHbarTransfer(toAccountId, new Hbar(100))    // receive
  .setTransactionMemo("Payment for goods");

// Sign with hashpack or operator
const signTx = await tx.sign(operatorKey);
const result = await signTx.execute(client);
```

## 主要交易类型

### AccountCreate
```typescript
new AccountCreateTransaction()
  .setKey(publicKey)
  .setInitialBalance(new Hbar(10))
  .setAccountMemo("My account");
```

### TokenAssociate
```typescript
new TokenAssociateTransaction()
  .setAccountId(accountId)
  .setTokenIds([tokenId1, tokenId2]);
```

### TopicMessage
```typescript
new TopicMessageTransaction()
  .setTopicId(topicId)
  .setMessage("Hello Hedera!");
```

## 网络端点

- **主网**: `https://mainnet.hashio.io/api`
- **测试网**: `https://testnet.hashio.io/api`

## 重要概念

- **Hbar**: 1 HBAR = 100,000,000 tinybars
- **账户 ID**: 格式为 `shardrealm.num`（例如：`0.0.12345`）
- **交易费用**: 每笔交易需支付少量 HBAR
- **交易有效期限**: 默认为 180 秒