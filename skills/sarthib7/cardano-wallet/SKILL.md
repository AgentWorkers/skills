---
name: cardano-wallet
description: 为 OpenClaw 代理生成、管理和资助 Cardano 钱包
homepage: https://masumi.network
user-invocable: true
metadata: {"openclaw": {"requires": {"bins": ["node"], "env": []}, "emoji": "💳"}}
---

# OpenClaw的Cardano钱包功能

**支持通过二维码进行Cardano钱包的生成、恢复和管理**

## 概述

Cardano钱包功能为AI代理提供了以下工具：
- 生成新的Cardano钱包（包含24个单词的助记词）
- 从现有的助记词中恢复钱包
- 生成用于便捷入金的二维码
- 查看钱包余额（需要Blockfrost API密钥）
- 安全地备份钱包凭证

## 工具

### `cardano_generate_wallet`
生成一个新的Cardano钱包，包含24个单词的助记词。

**参数：**
- `network`（可选）："Preprod" 或 "Mainnet"（默认值："Preprod")

**返回值：**
- `address`：Cardano钱包地址（格式为addr1...）
- `vkey`：支付验证密钥
- `credentialsPath`：加密后的钱包凭证文件路径

**示例：**
```typescript
const wallet = await cardano_generate_wallet({ network: 'Preprod' });
console.log('Address:', wallet.address);
```

### `cardano_restore_wallet`
从现有的助记词中恢复钱包。

**参数：**
- `mnemonic`（必需）：24个单词的助记词
- `network`（可选）："Preprod" 或 "Mainnet"
- `agentIdentifier`（可选）：用于保存凭证的标识符

**示例：**
```typescript
const wallet = await cardano_restore_wallet({
  mnemonic: 'word1 word2 ... word24',
  network: 'Preprod'
});
```

### `cardano_generate_funding_qr`
生成用于入金的二维码。返回二维码的数据URL。

**参数：**
- `address`（可选）：Cardano钱包地址
- `agentIdentifier`（可选）：钱包标识符
- `network`（可选）："Preprod" 或 "Mainnet"

**返回值：**
- `qrDataUrl`：二维码的数据URL（可显示为图片）
- `address`：钱包地址
- `faucetUrl`：Preprod网络的入金接口URL（仅限Preprod网络使用）

**示例：**
```typescript
const qr = await cardano_generate_funding_qr({
  agentIdentifier: 'my-wallet',
  network: 'Preprod'
});
// Display qr.qrDataUrl as image
```

### `cardano_get_wallet_balance`
查询钱包中的ADA和lovelace余额。需要Blockfrost API密钥。

**参数：**
- `agentIdentifier`（必需）：钱包标识符
- `network`（可选）："Preprod" 或 "Mainnet"
- `blockfrostApiKey`（可选）：Blockfrost API密钥（或使用环境变量）

**环境变量：**
- `BLOCKFROST_API_KEY`：Blockfrost API密钥
- `BLOCKFROST_PREPROD_API_KEY`：Preprod API密钥
- `BLOCKFROST_MAINNET_API_KEY`：Mainnet API密钥

**示例：**
```typescript
const balance = await cardano_get_wallet_balance({
  agentIdentifier: 'my-wallet',
  network: 'Preprod'
});
console.log('Balance:', balance.ada, 'ADA');
```

### `cardano_backup_wallet`
安全地备份钱包凭证（已加密）。

**参数：**
- `agentIdentifier`（必需）：钱包标识符
- `network`（可选）："Preprod" 或 "Mainnet"

**返回值：**
- `backupData`：加密后的钱包凭证文件

## 钱包入金流程：
1. **生成钱包：**
   ```typescript
   const wallet = await cardano_generate_wallet({ network: 'Preprod' });
   ```

2. **生成二维码：**
   ```typescript
   const qr = await cardano_generate_funding_qr({
     address: wallet.address,
     network: 'Preprod'
   });
   ```

3. **显示二维码**（供用户扫描并入金）

4. **在Preprod网络中：** 使用以下网址进行入金：https://docs.cardano.org/cardano-testnet/tools/faucet

5. **查看余额：**
   ```typescript
   const balance = await cardano_get_wallet_balance({
     agentIdentifier: 'wallet-id',
     network: 'Preprod',
     blockfrostApiKey: 'your-api-key'
   });
   ```

## 凭证存储

钱包凭证存储在以下位置（已加密）：
- `~/.openclaw/credentials/cardano-wallet/`

文件使用AES-256-GCM算法加密，权限设置为600（仅允许所有者读写）。

## 安全提示：
- **切勿分享您的助记词**——否则他人将能够完全控制您的钱包。
- **安全备份您的助记词**——使用`cardano_backup_wallet`功能或手动保存。
- **在Preprod网络中进行测试**——Mainnet网络会使用真实的ADA币。
- **加密密钥**：设置`MASUMI_ENCRYPTION_KEY`环境变量以确保数据安全。

## 依赖项：
- `@meshsdk/core`：用于钱包操作
- `qrcode`：用于生成二维码
- `@blockfrost/blockfrost-js`：用于查询钱包余额（可选）

## 示例代码：
完整的示例代码请参见`examples/wallet-generation.ts`文件。