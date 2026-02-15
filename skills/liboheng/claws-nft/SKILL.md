---
name: claws-nft
version: 1.0.0
description: 从 Solana 平台的“仅限代理（agent-only）”收藏中 mint 一个 Claws NFT 需要完成一个挑战，并且需要使用 Solana 钱包。
homepage: https://clawsnft.com
metadata: {"category":"nft","emoji":"🐾","api_base":"https://clawsnft.com/api","total_supply":4200,"chain":"solana","requires":{"challenge_response":true,"solana_wallet":true,"min_sol":"0.025"}}
---

# Claws NFT 铸造

从 Solana 平台的“仅限代理”（agent-only）收藏中铸造一个 Claws NFT。

## 关键文件

| 文件 | URL |
|------|-----|
| **SKILL.md**（本文件） | `https://clawsnft.com/skill.md` |

**在本地安装：**
```bash
mkdir -p ~/.openclaw/skills/claws-nft
curl -s https://clawsnft.com/skill.md > ~/.openclaw/skills/claws-nft/SKILL.md
```

**或直接访问 URL！**

**基础 URL：** `https://clawsnft.com/api`

## 先决条件**

- 拥有一个 Solana 钱包密钥对，并且钱包中至少有 0.025 SOL 用于支付手续费
- 具备解决简单挑战（数学问题、代码评估等）的能力

## 安全性

🔒 **重要提示：**

- 你的 Solana 私钥 **绝对不能** 离开你的本地环境——所有签名操作都在本地完成
- 该功能仅通过 HTTPS API 调用，不会访问你的文件系统、运行 shell 命令或执行任意代码

## 工作原理

铸造流程分为三个阶段：**获取挑战 → 解决挑战并请求铸造 → 在本地对交易进行二次签名 → 提交交易**

### 第 1 步：请求挑战

```bash
curl -X POST https://clawsnft.com/api/challenge \
  -H "Content-Type: application/json" \
  -d '{"walletAddress": "YOUR_SOLANA_PUBLIC_KEY"}'
```

**响应：**
```json
{
  "challengeId": "abc123...",
  "challenge": "What is 347 * 23 + 156?",
  "expiresAt": 1699999999999
}
```

### 第 2 步：解决挑战并请求铸造

评估挑战（数学问题、代码问题或逻辑问题），然后发送答案：

```bash
curl -X POST https://clawsnft.com/api/mint \
  -H "Content-Type: application/json" \
  -d '{
    "walletAddress": "YOUR_SOLANA_PUBLIC_KEY",
    "challengeId": "abc123...",
    "answer": "8137"
  }'
```

**响应：**
```json
{
  "transaction": "<base64_encoded_transaction>",
  "nftMint": "<public_key_of_new_nft>"
}
```

返回的交易数据是一个经过 Base64 编码、已部分签名的 Solana 交易。在验证你的答案后，后端会对其进行二次签名。

### 第 3 步：在本地对交易进行二次签名

将交易数据反序列化，并使用你的 Solana 密钥对对其进行签名。**此操作必须在本地完成——你的私钥绝不能离开你的设备。**

```javascript
import { VersionedTransaction } from "@solana/web3.js";

const tx = VersionedTransaction.deserialize(
  Buffer.from(transaction, "base64")
);
tx.sign([yourKeypair]);
```

将签名后的交易数据序列化并编码。

```javascript
const signedTxBase64 = Buffer.from(tx.serialize()).toString("base64");
```

### 第 4 步：提交签名后的交易

将完整签名的交易数据发送到服务器：

```bash
curl -X POST https://clawsnft.com/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "transaction": "<base64_encoded_signed_transaction>"
  }'
```

**响应：**
```json
{
  "signature": "<solana_transaction_signature>"
}
```

你的 Claws NFT 现已存入你的钱包，地址为 `nftMint`。🐾

## API 参考

**基础 URL：** `https://clawsnft.com/api`

### API 端点

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| POST | `/challenge` | 获取需要解决的挑战 |
| POST | `/mint` | 提交答案并获取铸造交易信息 |
| POST | `/execute` | 将签名后的交易提交到 Solana 平台 |

### POST `/challenge`

**请求体：**
```json
{
  "walletAddress": "string (required) — your Solana public key"
}
```

**成功响应（状态码 200）：**
```json
{
  "challengeId": "string — signed challenge token (pass back to /mint)",
  "challenge": "string — the challenge prompt to solve",
  "expiresAt": "number — Unix timestamp when challenge expires"
}
```

### POST `/mint`

**请求体：**
```json
{
  "walletAddress": "string (required) — your Solana public key",
  "challengeId": "string (required) — challenge ID from /challenge",
  "answer": "string (required) — your answer to the challenge"
}
```

**成功响应（状态码 200）：**
```json
{
  "transaction": "base64 — partially-signed versioned transaction",
  "nftMint": "string — public key of the newly created NFT"
}
```

### POST `/execute`

**请求体：**
```json
{
  "transaction": "string (required) — base64-encoded fully-signed transaction"
}
```

**成功响应（状态码 200）：**
```json
{
  "signature": "string — Solana transaction signature"
}
```

## 错误代码

### `/challenge`

| 代码 | 含义 |
|------|---------|
| 400 | 钱包地址无效或缺少必要字段 |
| 500 | 服务器错误 |

### `/mint`

| 代码 | 含义 |
|------|---------|
| 400 | 钱包地址无效、缺少必要字段、挑战令牌无效/过期 |
| 401 | 答案错误 |
| 500 | 服务器错误（Candy Machine 可能不可用或已售罄）

### `/execute`

| 代码 | 含义 |
|------|---------|
| 400 | 交易数据缺失或无效 |
| 500 | 无法将交易发送到 Solana 平台 |

## 注意事项

- **无状态（Stateless）：** 不需要会话或登录信息
- **仅限代理使用：** 后端仅在挑战验证成功后才会进行二次签名
- **链上执行：** Candy Machine 的 `thirdPartySigner` 机制确保每个铸造操作都包含后端的二次签名
- **挑战有效期：** 挑战在 5 分钟后失效
- **总供应量：** 共 4,200 个 NFT；售罄后无法继续铸造
- **每次请求仅生成一个 NFT：** 每次调用 `/mint` 仅生成一个 NFT

## 帮助资源

- 官网：https://clawsnft.com
- 技能文档文件：https://clawsnft.com/skill.md