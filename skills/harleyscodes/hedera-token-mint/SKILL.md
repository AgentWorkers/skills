---
name: hedera-token-mint
description: Create and manage tokens on Hedera (HTS). Use for: (1) Minting fungible tokens, (2) Creating NFTs (HTS), (3) Setting up token supplies, (4) Configuring token permissions.
---

# Hedera Token Minting (HTS)

## 设置

```bash
npm install @hashgraph/sdk
```

## 创建可互换代币（Fungible Token）

```typescript
import { 
  TokenCreateTransaction, 
  TokenSupplyType,
  TokenType 
} from '@hashgraph/sdk';

const tx = await new TokenCreateTransaction()
  .setTokenName("My Token")
  .setTokenSymbol("MTK")
  .setTokenType(TokenType.FungibleCommon)
  .setSupplyType(TokenSupplyType.Infinite)
  .setDecimals(2)
  .setInitialSupply(1000000) // Total supply = 1,000,000
  .setTreasuryAccountId(treasuryId)
  .setAdminKey(adminKey)
  .setSupplyKey(supplyKey)
  .freezeWith(client)
  .sign(treasuryKey);

const result = await tx.execute(client);
const tokenId = result.receipt.tokenId;
```

## 创建非同质化代币（NFT）集合

```typescript
const tx = await new TokenCreateTransaction()
  .setTokenName("My NFT Collection")
  .setTokenSymbol("MNFT")
  .setTokenType(TokenType.NonFungibleUnique)
  .setTreasuryAccountId(treasuryId)
  .setAdminKey(adminKey)
  .setSupplyKey(supplyKey)
  .freezeWith(client)
  .sign(treasuryKey);
```

## 铸造 NFT

```typescript
import { TokenMintTransaction } from '@hashgraph/sdk';

const tx = await new TokenMintTransaction()
  .setTokenId(tokenId)
  .addMetadata(Buffer.from("NFT #1 metadata"))
  .addMetadata(Buffer.from("NFT #2 metadata"))
  .freezeWith(client)
  .sign(supplyKey);

const result = await tx.execute(client);
```

## 代币操作

### 转移代币
```typescript
import { TransferTransaction } from '@hashgraph/sdk';

await new TransferTransaction()
  .addTokenTransfer(tokenId, fromAccount, -10)
  .addTokenTransfer(tokenId, toAccount, 10)
  .execute(client);
```

### 烧毁代币（Burn Tokens）
```typescript
import { TokenBurnTransaction } from '@hashgraph/sdk';

await new TokenBurnTransaction()
  .setTokenId(tokenId)
  .setAmount(100)
  .execute(client);
```

## 关键要点

- **代币供应量类型**：`无限`（Infinite）或`有限`（Finite）
- **代币类型**：`可互换代币`（FungibleCommon）或`非同质化代币`（NonFungibleUnique）
- **版税设置**：可以为 NFT 设置自定义的版税费用
- **代币 ID 格式**：`0.0.12345`