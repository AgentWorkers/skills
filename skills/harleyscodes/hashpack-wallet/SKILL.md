---
name: hashpack-wallet
description: Integrate HashPack wallet for Hedera blockchain authentication. Use for: (1) Adding HashPack login to webapps, (2) Signing Hbar transactions, (3) Connecting to Hedera DApps, (4) Getting account balance.
---

# HashPack钱包集成

## 快速入门

```typescript
// Detect HashPack
const hashpack = (window as any).hashpack;

// Connect
const result = await hashpack.connect();

// Get account ID
const accountId = result.accountId; // e.g., "0.0.12345"
```

## 账户ID格式

Hedera账户ID的格式为：`0.0.12345`（其中`0`表示主节点，`0.12345`表示账户ID）

## 主要方法

```typescript
// Connect (opens popup)
await hashpack.connect();

// Sign and submit transaction
const tx = new TransferTransaction()
  .addHbarTransfer(from, -10)
  .addHbarTransfer(to, 10);
await hashpack.signTransaction(tx);

// Get balance
const balance = await new AccountBalanceQuery()
  .setAccountId(accountId)
  .execute(client);

// Disconnect
hashpack.disconnect();
```

## 环境配置

- **主网**：`https://mainnet.hashio.io/api`
- **测试网**：`https://testnet.hashio.io/api`
- **预览网**：`https://previewnet.hashio.io/api`

## 交易类型

- `TransferTransaction` - 发送HBAR/代币
- `ContractExecuteTransaction` - 调用合约
- `TokenAssociateTransaction` - 将账户与代币关联
- `TokenMintTransaction` - 铸造代币
- `TopicCreateTransaction` - 创建HCS主题