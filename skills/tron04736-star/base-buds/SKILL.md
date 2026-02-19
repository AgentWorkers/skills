---
name: base-buds
version: 1.0.0
description: 从 Base 主网上的“仅限代理”（agent-only）收藏中创建一个基础 Bud NFT。需要完成一个挑战任务，支付 1 个 USDC（x402），并且需要使用 EVM 钱包。
homepage: https://budsbase.xyz
metadata: {"category":"nft","emoji":"🌿","api_base":"https://budsbase.xyz/api","total_supply":6000,"chain":"base","chain_id":8453,"mint_price":"1 USDC","payment_protocol":"x402","requires":{"challenge_response":true,"evm_wallet":true,"min_eth":"0.001","usdc":"1.00"}}
---
# Base Buds Mint

从 Base 主网上的仅限代理（agent-only）收藏中 mint 一个 Base Bud NFT。

## 关键文件

| 文件 | URL |
|------|-----|
| **SKILL.md** （本文件） | `https://budsbase.xyz/skill.md` |

**在本地安装：**
```bash
mkdir -p ~/.openclaw/skills/base-buds
curl -s https://budsbase.xyz/skill.md > ~/.openclaw/skills/base-buds/SKILL.md
```

**或直接访问 URL！**

**基础 URL：** `https://budsbase.xyz/api`

## 先决条件

- 拥有一个 **EVM 钱包密钥对**，并在 Base 主网上至少有 **0.001 ETH** 用于支付 gas 费用，以及 **1 USDC**（链 ID 8453）。
- 具备解决挑战（数学问题、编写代码或逻辑问题）的能力。

## 安全性

- 你的 EVM 私钥 **绝不能** 离开你的本地环境——签名操作仅在本地完成。
- 该技能仅使用 HTTP API 调用，不会访问你的文件系统、运行 shell 命令或执行任意代码。

## 工作原理

整个 mint 流程分为四个步骤：**请求挑战 → 准备 → 完成（支付并获取交易）→ 广播**。

### 第 1 步：请求挑战

```bash
curl -X POST https://budsbase.xyz/api/challenge \
  -H "Content-Type: application/json" \
  -d '{"wallet": "YOUR_EVM_ADDRESS"}'
```

响应：
```json
{
  "challengeId": "0xabc123...",
  "puzzle": "What is 347 * 23 + 156?",
  "expiresAt": 1699999999999
}
```

### 第 2 步：准备并签名支付

使用一个单节点脚本将挑战答案提交到 `/prepare`，然后在本地签名 USDC 支付。**你的私钥永远不会离开你的机器。**

注意：`/prepare` 仅返回支付信息，实际的 mint 交易信息会在第 3 步支付完成后提供。

```javascript
import { ethers } from "ethers";

const PK = "YOUR_PRIVATE_KEY";
if (!/^0x[0-9a-fA-F]{64}$/.test(PK)) throw new Error("Invalid private key — must be 0x + 64 hex chars");
const wallet = new ethers.Wallet(PK);

// 2a. Submit challenge answer, get payment data
const res = await fetch("https://budsbase.xyz/api/prepare", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ wallet: wallet.address, challengeId: "CHALLENGE_ID", answer: "ANSWER" }),
});
const { prepareId, payment } = await res.json();

// 2b. Sign USDC payment (EIP-712)
const paymentSignature = await wallet.signTypedData(payment.domain, payment.types, payment.values);

console.log(JSON.stringify({ prepareId, paymentSignature }));
```

### 第 3 步：完成（支付并获取未签名的 mint 交易）

提交支付签名。后端首先在链上完成 1 USDC 的支付，然后返回未签名的 mint 交易。

```bash
curl -X POST https://budsbase.xyz/api/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prepareId": "0x<from_step_2>",
    "paymentSignature": "0x<from_step_2>"
  }'
```

响应：
```json
{
  "success": true,
  "settleTxHash": "0x...",
  "transaction": { "to": "0x...", "data": "0x...", "chainId": 8453, "nonce": 5, "type": 2, "..." : "..." },
  "message": "Payment settled. Sign the transaction and POST to /api/broadcast."
}
```

### 第 4 步：签名并广播

在本地签名 mint 交易，然后将其提交。

```javascript
import { ethers } from "ethers";

const PK = "YOUR_PRIVATE_KEY";
if (!/^0x[0-9a-fA-F]{64}$/.test(PK)) throw new Error("Invalid private key — must be 0x + 64 hex chars");
const wallet = new ethers.Wallet(PK);
const transaction = /* transaction object from Step 3 */;

const signedTransaction = await wallet.signTransaction(transaction);
console.log(JSON.stringify({ signedTransaction }));
```

```bash
curl -X POST https://budsbase.xyz/api/broadcast \
  -H "Content-Type: application/json" \
  -d '{"signedTransaction": "0x<from_above>"}'
```

响应：
```json
{
  "success": true,
  "tokenId": 9,
  "minter": "0x...",
  "txHash": "0x...",
  "minted": 2,
  "remaining": 18,
  "message": "Successfully minted Base Bud #9! You have minted 2 Base Buds. You can mint up to 18 more."
}
```

## 代理行为

- 用户需要提供他们的 **钱包地址** 和 **私钥**。之后，代理会负责完成整个 mint 流程，无需用户进一步操作。
- **第 1 步（请求挑战）**：使用 `curl`。
- **第 2 步（准备并签名支付）**：使用一个单节点脚本来获取 `/prepare` 的结果并签名 USDC 支付。**不要将这个过程拆分为多个 curl 和 node 操作**。
  - **ethers 的依赖检查**：在运行脚本之前，检查是否已安装 ethers：`node -e "require('ethers')`。如果未安装，先将其安装到临时目录（`/tmp`）：`npm install --prefix /tmp/node_modules`，然后再使用 `NODE_PATH=/tmp/node_modules` 运行脚本。
- **第 3 步（完成）**：使用 `curl` 完成支付并获取未签名的 mint 交易。
- **第 4 步（签名并广播）**：使用一个单节点脚本对第 3 步中的交易进行签名，然后使用 `curl` 将签名后的交易提交到 `/broadcast`。
- 在每个步骤完成后，简要告知用户操作结果，再进入下一步。
- 优雅地处理错误：如果某个步骤失败，解释原因并尝试重试或停止操作。
- **达到 mint 限制（409）**：如果 `/challenge` 返回 409 错误代码，要求用户提供新的钱包地址和私钥，然后使用新的钱包重新开始流程。
- **切勿在输出或日志中泄露用户的私钥**。
- 签名操作必须在本地完成——绝不要通过网络传输私钥。

## 错误代码

### `/challenge`

| 代码 | 含义 |
|------|---------|
| 400 | 钱包地址无效或缺少必要字段 |
| 409 | 钱包的 mint 数量已达到上限（20 个） |
| 410 | 收藏已全部被 mint 完成 |
| 500 | 服务器错误 |

### `/prepare`

| 代码 | 含义 |
|------|---------|
| 400 | 钱包地址无效或缺少必要字段 |
| 403 | 挑战答案错误或已过期 |
| 500 | 服务器错误 |

### `/complete`

所有错误都会包含一个 `code` 字段，你可以根据这些代码来识别问题：

| `code` | HTTP 状态码 | 含义 |
|--------|------|---------|
| `missing_prepare_id` | 400 | 未提供 `prepareId` |
| `missing_payment_signature` | 400 | 未提供 `paymentSignature` |
| `prepare_session_expired` | 400 | 会话未找到或已过期——请重新调用 `/prepare` |
| `authorization_expired` | 400 | USDC 的授权期限已过 |
| `authorization_not_yet_valid` | 400 | USDC 的授权期限尚未到来 |
| `insufficient_usdc_balance` | 400 | 钱包中的 USDC 不足 |
| `paymentverification_failed` | 402 | 中间机构（facilitator）拒绝了支付签名 |
| `payment_settlement_failed` | 402 | 中间机构无法完成 USDC 的转账 |

### `/broadcast`

| `code` | HTTP 状态码 | 含义 |
|--------|------|---------|
| `missing_signed_transaction` | 400 | 未提供签名后的交易信息 |
| `nonce_too_low` | 400 | 钱包有未完成的交易——请重新调用 `/complete` |
| `insufficient_eth` | 400 | 缺乏足够的 ETH 用于支付 gas 费用 |
| `already_known` | 409 | 该交易已被提交 |
| `mint_reverted` | 400 | mint 交易在链上被撤销 |
| `broadcast_failed` | 500 | 交易广播失败 |

## 注意事项

- **链路**：Base 主网（链 ID 8453）
- **支付方式**：每次 mint 需支付 1 USDC，通过 EIP-712 进行签名后的 USDC 转账。
- **两次签名操作**：EIP-712 用于 USDC 支付（第 2 步），EIP-1559 用于 mint 交易（第 4 步）。
- **挑战有效期**：挑战在 5 分钟后失效。
- **总发行量**：6,000 个 NFT。
- **每个钱包最多可 mint 20 个 NFT**。
- **Gas 费用**：在 Base 主网上，每次 mint 的费用约为 0.0001–0.0005 ETH。