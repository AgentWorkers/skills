---
name: solpaw
description: 通过 SolPaw 平台在 Pump.fun 上发布 Solana 代币。只需支付 0.1 SOL 的一次性费用。您的钱包将作为代币的链上创建者。
homepage: https://solpaw.fun
user-invocable: true
disable-model-invocation: false
command-dispatch: tool
command-tool: exec
command-arg-mode: raw
metadata: {"openclaw": {"emoji": "🐾", "requires": {"bins": ["curl"], "env": ["SOLPAW_API_KEY", "SOLPAW_CREATOR_WALLET", "SOLANA_PRIVATE_KEY"], "config": []}, "primaryEnv": "SOLPAW_API_KEY", "install": []}}
---

# SolPaw — 通过 Pump.fun 在 Solana 上发布代币

## 使用场景

当代理需要执行以下操作时，可以使用此技能：
- 通过 Pump.fun 在 Solana 上发布新的表情币（memecoin）或代币
- 部署具有名称、符号、描述和图片的代币
- 为社区、项目或表情币创建 Pump.fun 代币列表

## 概述

SolPaw 是首个专为自主代理设计的 Solana 代币发布平台，它负责处理 IPFS 元数据上传、交易构建以及 Pump.fun 的部署工作。

- **费用**：一次性平台费用 0.1 SOL + 每次发布约 0.02 SOL 的 Pump.fun 创建费用
- **创建者**：你的代理钱包是 Pump.fun 上的实际链上创建者
- **限制**：每个代理每天最多只能发布 1 个代币
- **平台钱包地址**：`6SoPUBp68Eqhvs3fdx6GdKu5EP44ykqsjh359LyY3ZiS`
- **文档**：https://solpaw.fun

## 先决条件

1. 拥有一个至少包含 0.15 SOL 的 Solana 钱包（用于支付平台费用和 Pump.fun 创建费用）
2. 拥有 SolPaw API 密钥（请在 API 端注册）
3. 设置以下环境变量：
   - `SOLPAW_API_KEY`：你的 SolPaw API 密钥
   - `SOLPAW_CREATOR_WALLET`：你的 Solana 钱包公钥
   - `SOLANA_PRIVATE_KEY`：你的钱包私钥（需使用 base58 编码格式）

## 步骤

### 第 1 步：注册（仅一次）

```bash
curl -s -X POST https://api.solpaw.fun/api/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{"agent_name":"MyAgent","default_fee_wallet":"YOUR_WALLET_ADDRESS"}' | jq .
```

从响应中保存 `api_key`。此密钥将不再显示。

### 第 2 步：获取 CSRF 令牌

```bash
CSRF=$(curl -s -H "Authorization: Bearer $SOLPAW_API_KEY" \
  https://api.solpaw.fun/api/v1/agents/csrf | jq -r '.data.csrf_token')
```

### 第 3 步：支付 0.1 SOL 的发布费用

向平台钱包 `6SoPUBp68Eqhvs3fdx6GdKu5EP44ykqsjh359LyY3ZiS` 支付 0.1 SOL（100,000,000 lamports）。
保存该交易的签名。

### 第 4 步：上传代币图片（可选，但推荐）

```bash
IMAGE_ID=$(curl -s -X POST https://api.solpaw.fun/api/v1/tokens/upload-image \
  -H "Authorization: Bearer $SOLPAW_API_KEY" \
  -F "file=@token-logo.png" | jq -r '.data.image_id')
```

### 第 5 步：发布代币（本地模式——你的钱包作为创建者）

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

### 使用 TypeScript SDK（更简单）

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

## 限制事项

- 未经用户同意，严禁发布代币——务必先确认代币的名称、符号和描述。
- 每天最多只能发布 1 个代币（服务器端会进行限制）。
- 代币的名称和描述不得包含攻击性或误导性内容。
- 必须上传代币图片——没有图片的代币在 Pump.fun 上的表现较差。
- 必须使用本地模式（传递 `signer_keypair`），以确保代理钱包作为链上创建者。
- 一旦发布成功，0.1 SOL 的平台费用将不予退还。
- CSRF 令牌的有效期为 30 分钟，且为一次性使用。
- 上传的图片也会在 30 分钟后失效。

## 示例

### 成功发布代币
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

### 错误：余额不足
```
Agent: Your wallet only has 0.05 SOL. You need at least 0.15 SOL to launch:
- 0.1 SOL platform fee
- ~0.02 SOL Pump.fun creation fee
- ~0.01 SOL for gas
```