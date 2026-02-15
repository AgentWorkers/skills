---
name: solpaw
description: 通过 SolPaw 平台在 Pump.fun 上发布 Solana 代币。只需支付 0.1 SOL 的一次性费用。您的钱包将作为代币的在线创建者（即代币的发行者）。
homepage: https://solpaw.fun
user-invocable: true
disable-model-invocation: true
command-dispatch: tool
command-tool: exec
command-arg-mode: raw
metadata: {"openclaw": {"emoji": "🐾", "requires": {"bins": ["curl"], "env": ["SOLPAW_API_KEY", "SOLPAW_CREATOR_WALLET", "SOLANA_PRIVATE_KEY", "SOLPAW_API_URL"], "config": []}, "primaryEnv": "SOLPAW_API_KEY", "install": []}}
---

# SolPaw — 通过Pump.fun在Solana上发布代币

## 使用场景

当用户明确要求以下操作时，可以使用此功能：
- 通过Pump.fun在Solana上发布新的表情币（memecoin）或代币
- 部署具有名称、符号、描述和图片的代币
- 为某个社区、项目或表情币创建Pump.fun上的代币列表

**此功能必须由用户本人触发，切勿自动执行代币发布操作。**

## 概述

SolPaw是首个专为自动化代理（automated agents）设计的Solana代币发布平台，它负责处理IPFS元数据的上传、交易构建以及代币在Pump.fun平台上的部署：
- **费用**：一次性平台费用0.1 SOL，每次代币发布还需支付约0.02 SOL的Pump.fun创建费用
- **实际创建者**：用户的Solana钱包是Pump.fun平台上的实际代币创建者
- **限制**：每个代理24小时内只能发布1次代币
- **平台钱包地址**：`GosroTTvsbgc8FdqSdNtrmWxGbZp2ShH5NP5pK1yAR4K`
- **官方文档**：https://solpaw.fun

## 安全性注意事项：
- **建议使用临时钱包**：请使用仅包含所需金额（约0.15 SOL）的专用钱包，切勿使用主钱包的私钥。
- `SOLANA_PRIVATE_KEY` 仅用于本地交易签名，不会被传输到SolPaw API服务器——签名操作在客户端完成。
- **API密钥（SOLPAW_API_KEY）** 用于验证请求，但无法用于签署交易或转移资金。
- **CSRF令牌** 为一次性使用，有效期30分钟，可防止重放攻击。
- **费用签名** 会在链上验证，不可重复使用。
- **每日限制**：每个代理24小时内只能发布1次代币。
- **所有敏感信息（SOLPAW_API_KEY、SOLANA_PRIVATE_KEY）必须存储在环境变量中，严禁写入代码或聊天记录中。

## 前提条件：
1. 拥有一个至少包含0.15 SOL的Solana钱包（包含0.1 SOL的平台费用、Pump.fun创建费用及交易手续费）。
2. 拥有SolPaw API密钥（需在API页面注册）。
3. 确保环境变量已设置正确：
   - `SOLPAW_API_KEY`：您的SolPaw API密钥
   - `SOLPAW_CREATOR_WALLET`：您的Solana钱包公钥
   - `SOLANA_PRIVATE_KEY`：您的钱包私钥（以base58格式编码，仅用于本地签名，切勿发送给服务器）
   - `SOLPAW_API_URL`：API基础地址（默认：`https://api.solpaw.fun/api/v1`）

## 操作步骤：
### 第1步：注册（仅一次）
```bash
curl -s -X POST https://api.solpaw.fun/api/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{"agent_name":"MyAgent","default_fee_wallet":"YOUR_WALLET_ADDRESS"}' | jq .
```

从响应中保存`api_key`，该密钥后续不会再显示。

### 第2步：获取CSRF令牌
```bash
CSRF=$(curl -s -H "Authorization: Bearer $SOLPAW_API_KEY" \
  https://api.solpaw.fun/api/v1/agents/csrf | jq -r '.data.csrf_token')
```

### 第3步：支付0.1 SOL的发布费用
向平台钱包（`GosroTTvsbgc8FdqSdNtrmWxGbZp2ShH5NP5pK1yAR4K`）转账0.1 SOL（100,000,000 lamports）。
保存交易签名。

### 第4步：上传代币图片（可选，但推荐）
```bash
IMAGE_ID=$(curl -s -X POST https://api.solpaw.fun/api/v1/tokens/upload-image \
  -H "Authorization: Bearer $SOLPAW_API_KEY" \
  -F "file=@token-logo.png" | jq -r '.data.image_id')
```

### 第5步：发布代币（本地模式——用户的钱包作为创建者）
```bash
# Build unsigned transaction
TX_DATA=$(curl -s -X POST https://api.solpaw.fun/api/v1/tokens/launch-local \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SOLPAW_API_KEY" \
  -d '{
    "name": "MyCoolToken",
    "symbol": "MCT",
    "description": "An awesome token launched by an AI agent on SolPaw",
    "creator_wallet": "'$SOLPAW_CREATOR_WALLET'",
    "signer_public_key": "'$SOLPAW_CREATOR_WALLET'",
    "launch_fee_signature": "YOUR_FEE_TX_SIGNATURE",
    "image_id": "'$IMAGE_ID'",
    "initial_buy_sol": 0,
    "slippage": 10,
    "priority_fee": 0.0005,
    "csrf_token": "'$CSRF'"
  }')

# Sign the transaction with your private key, then submit
SIGNED_TX="..." # sign the base64 transaction from TX_DATA
curl -s -X POST https://api.solpaw.fun/api/v1/tokens/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SOLPAW_API_KEY" \
  -d '{"signed_transaction": "'$SIGNED_TX'", "mint": "MINT_FROM_TX_DATA"}'
```

### 使用TypeScript SDK（更便捷的方式）
```typescript
import SolPawSkill from './solpaw-skill';
import { Keypair } from '@solana/web3.js';

const solpaw = new SolPawSkill({
  apiEndpoint: 'https://api.solpaw.fun/api/v1',
  apiKey: process.env.SOLPAW_API_KEY,
  defaultCreatorWallet: process.env.SOLPAW_CREATOR_WALLET,
});

const keypair = Keypair.fromSecretKey(bs58.decode(process.env.SOLANA_PRIVATE_KEY));

// One-call launch: pays fee + uploads + signs + submits
const result = await solpaw.payAndLaunch({
  name: 'MyCoolToken',
  symbol: 'MCT',
  description: 'Launched by an AI agent on SolPaw',
  image_url: 'https://example.com/logo.png',
  initial_buy_sol: 0.5,
}, keypair);

console.log(result.pumpfun_url); // https://pump.fun/coin/...
```

## 注意事项：
- **未经用户明确授权，严禁发布代币**——务必先确认代币的名称、符号和描述。
- 每24小时内最多只能发布1个代币（服务器端会进行限制）。
- 代币名称和描述不得包含攻击性或误导性内容。
- 请务必上传代币图片——没有图片的代币在Pump.fun平台上的表现较差。
- 请始终使用“本地模式”（传递`signer_keypair`），以确保用户的钱包作为链上的实际创建者。
- 一旦发布成功，0.1 SOL的平台费用不予退还。
- CSRF令牌有效期为30分钟，且为一次性使用。
- 上传的图片也会在30分钟后失效。
- 严禁记录、显示或传输`SOLANA_PRIVATE_KEY`——该密钥仅用于本地签名。

## 示例：
### 成功发布代币的示例
```
Agent: I'll launch the DOGE2 token on Pump.fun for you.
> Uploading token image...
> Paying 0.1 SOL launch fee...
> Building transaction...
> Signing and submitting...
> Token launched successfully!
> Pump.fun: https://pump.fun/coin/So1...
> Mint: So1...
> Your wallet is the onchain creator.
```

### 错误示例：余额不足
```
Agent: Your wallet only has 0.05 SOL. You need at least 0.15 SOL to launch:
- 0.1 SOL platform fee
- ~0.02 SOL Pump.fun creation fee
- ~0.01 SOL for gas
```