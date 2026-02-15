# Stable Layer SDK

这是一个TypeScript SDK，用于与Sui区块链上的Stable Layer协议进行交互。它支持铸造和销毁稳定币（stablecoins），以及领取收益 farming的奖励。

## 安装

```bash
npm install stable-layer-sdk @mysten/sui @mysten/bcs
```

## API参考

### StableLayerClient

```typescript
import { StableLayerClient } from "stable-layer-sdk";

const client = new StableLayerClient({
  network: "mainnet" | "testnet",
  sender: "0xYOUR_SUI_ADDRESS",
});
```

### 交易方法

#### `buildMintTx(options)`

通过存入USDC来铸造稳定币。铸造后的稳定币会自动存入保险库（vault）进行收益 farming。

| 参数               | 类型           | 描述                                      |
| ------------------- | ------------ | ------------------------------------------------ |
| `tx`            | `Transaction`     | Sui交易对象                             |
| `stableCoinType`     | `string`       | 目标稳定币类型（例如：`0x...::btc_usdc::BtcUSDC`）         |
| `usdcCoin`        | `Coin`         | 输入的USDC币种参考                         |
| `amount`         | `bigint`        | 铸造的数量                               |
| `autoTransfer`      | `boolean?`     | 如果设置为`false`，则返回铸造后的Coin对象         |

#### `buildBurnTx(options)`

销毁稳定币以兑换USDC。

| 参数               | 类型           | 描述                                      |
| ------------------- | ------------ | ------------------------------------ |
| `tx`            | `Transaction`     | Sui交易对象                             |
| `stableCoinType`     | `string`       | 需要销毁的稳定币类型                         |
| `amount`         | `bigint?`      | 需要销毁的具体数量                         |
| `all`            | `boolean?`     | 如果设置为`true`，则销毁所有余额                     |

#### `buildClaimTx(options)`

领取累积的收益 farming奖励。

| 参数               | 类型           | 描述                                      |
| ------------------- | ------------ | ------------------------------------ |
| `tx`            | `Transaction`     | Sui交易对象                             |
| `stableCoinType`     | `string`       | 需要领取奖励的稳定币类型                         |

### 查询方法

#### `getTotalSupply()`

返回所有稳定币类型的总供应量。

#### `getTotalSupplyByCoinType(type: string)`

返回特定稳定币类型的供应量。

## 使用示例

### 铸造稳定币

```typescript
import { Transaction, coinWithBalance } from "@mysten/sui/transactions";
import { SuiClient, getFullnodeUrl } from "@mysten/sui/client";
import { Ed25519Keypair } from "@mysten/sui/keypairs/ed25519";
import { StableLayerClient } from "stable-layer-sdk";

const client = new StableLayerClient({
  network: "mainnet",
  sender: "0xYOUR_ADDRESS",
});

const suiClient = new SuiClient({ url: getFullnodeUrl("mainnet") });
const keypair = Ed25519Keypair.fromSecretKey(YOUR_PRIVATE_KEY);

const tx = new Transaction();
await client.buildMintTx({
  tx,
  stableCoinType: "0x6d9fc...::btc_usdc::BtcUSDC",
  usdcCoin: coinWithBalance({
    balance: BigInt(1_000_000),
    type: "0xdba34...::usdc::USDC",
  })(tx),
  amount: BigInt(1_000_000),
});

const result = await suiClient.signAndExecuteTransaction({
  transaction: tx,
  signer: keypair,
});
```

### 销毁稳定币

```typescript
const tx = new Transaction();
await client.buildBurnTx({
  tx,
  stableCoinType: "0x6d9fc...::btc_usdc::BtcUSDC",
  amount: BigInt(500_000),
});

await suiClient.signAndExecuteTransaction({ transaction: tx, signer: keypair });
```

### 领取奖励

```typescript
const tx = new Transaction();
await client.buildClaimTx({
  tx,
  stableCoinType: "0x6d9fc...::btc_usdc::BtcUSDC",
});

await suiClient.signAndExecuteTransaction({ transaction: tx, signer: keypair });
```

### 查询供应量

```typescript
const totalSupply = await client.getTotalSupply();
const btcUsdcSupply = await client.getTotalSupplyByCoinType("0x6d9fc...::btc_usdc::BtcUSDC");
```