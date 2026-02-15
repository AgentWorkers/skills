---
name: solana-easy-swap
description: 在聊天中，您可以随时交换任何Solana代币。只需输入“swap 1 SOL for USDC”，系统会自动完成所有操作——包括报价、签名、发送和确认交易。无需使用API密钥，也无需安装任何钱包扩展程序，只需提供一对公钥和私钥即可。该功能由Jupiter技术支持，适用于用户进行Solana SPL代币、SOL代币、USDC代币、memecoins或其他任何代币对的交易、兑换、购买或出售。
metadata: { "openclaw": { "emoji": "🔄", "requires": { "bins": ["node"], "env": ["SOLANA_KEYPAIR_PATH"] }, "install": [{ "id": "npm", "kind": "command", "command": "cd {baseDir} && npm install --production", "label": "Install dependencies" }] } }
---

# Solana简易交换功能

您可以在聊天中随时请求交换Solana代币。只需输入“swap 1 SOL for USDC”，系统会自动完成所有步骤——包括报价、签名、发送和确认交易。无需API密钥，也无需任何额外的钱包扩展功能，只需提供密钥对即可。该功能由Jupiter技术支持。

## 设置

**首次使用：** 安装所需依赖项（如果支持自动安装方式，则会自动完成；否则需手动安装）：
```bash
cd {baseDir} && npm install --production
```

**必填环境变量：**
- `SOLANA_KEYPAIR_PATH`：Solana密钥对的JSON文件路径（标准格式为`solana-keygen`生成）。**该功能会使用此密钥对来签署交易。**请仅使用您信任的密钥对。

**可选环境变量：**
- `SOLANA_RPC_URL`：自定义RPC端点（默认值：`https://api.mainnet-beta.solana.com`）
- `OSS_DEFAULT_SLIPPAGE_BPS`：默认的滑点（以基点为单位，默认值为`100`，即1%）
- `OSS_PRIORITY_FEE_FLOOR`：最低优先级费用（以lamports为单位，默认值为`50000`）

无需API密钥。Jupiter功能采用无认证方式运行。

## 常见可交换的代币

| 代币 | 发行地址 |
|---|---|
| SOL（封装形式） | `So11111111111111111111111111111111111111112` |
| USDC | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |
| USDT | `Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB` |

对于其他代币，请用户提供相应的发行地址。

## 功能流程

### 1. 准备工作

```bash
node {baseDir}/scripts/swap.mjs prepare \
  --from So11111111111111111111111111111111111111112 \
  --to EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v \
  --amount 1000000000 \
  --slippage 100
```

**系统会返回JSON格式的准备工作结果：**  
```json
{
  "prepareId": "abc123",
  "expectedOut": "150230000",
  "minOut": "148727700",
  "priceImpact": "0.01",
  "expiresAt": "2025-02-13T20:00:00Z",
  "summary": {
    "from": "1 SOL",
    "to": "~150.23 USDC",
    "minReceived": "148.73 USDC",
    "slippage": "1%",
    "priceImpact": "0.01%",
    "destination": "owner"
  }
}
```

**在执行操作前，请务必向用户展示交易摘要并等待其确认。**  
如果交易价格变动超过1%，请明确提醒用户。

### 2. 执行交易

用户确认后，系统将执行交换操作：
```bash
node {baseDir}/scripts/swap.mjs execute --prepareId abc123
```

**执行完成后，系统会返回JSON格式的结果：**  
```json
{
  "signature": "5UzV...",
  "submittedAt": "2025-02-13T19:58:12Z"
}
```

### 3. 状态监控（持续查询直至交易确认）

```bash
node {baseDir}/scripts/swap.mjs status --signature 5UzV...
```

**系统会返回交易状态：**  
`submitted` → `confirmed` | `failed` | `expired` | `unknown`

### 4. 交易完成通知

```bash
node {baseDir}/scripts/swap.mjs receipt --signature 5UzV...
```

**系统会返回交易详细信息，包括实际交换的代币数量、费用以及Solscan链接：**  
```json
{
  "state": "confirmed",
  "slot": 123456789,
  "confirmationStatus": "finalized"
}
```

### 错误处理

所有操作在失败时都会返回包含`error`字段的JSON响应：

```json
{
  "error": {
    "code": "INSUFFICIENT_SOL",
    "message": "Not enough SOL for fees. Have 0.001, need ~0.006",
    "retryable": false
  }
}
```

**错误代码及处理建议：**
| 代码 | 是否需要重试 | 处理方式 |
|---|---|---|
| `INVALID_INPUT` | 不需要 | 请检查输入内容是否正确 |
| `INSUFFICIENT_SOL` | 不需要 | 通知用户需要更多Solana代币 |
| `KEYPAIR_NOT_FOUND` | 不需要 | 确保`SOLANA_KEYPAIR_PATH`设置正确 |
| `KEYPAIR_INVALID` | 不需要 | 检查密钥对文件的格式是否正确 |
| `PREPARE_EXPIRED` | 需要 | 重新执行准备步骤，并再次获取用户确认 |
| `PREPARE_ALREADY_EXECUTED` | 不需要 | 该交易已发送，无法重试 |
| `BACKEND_UNAVAILABLE` | 需要 | 等待3秒后重试准备步骤（最多尝试2次） |
| `BACKEND_QUOTE_FAILED` | 不需要 | 说明无法找到合适的交易路径或市场流动性不足 |
| `TX_EXPIRED` | 需要 | 重新执行准备步骤，并再次获取用户确认 |
| `TX_BROADCAST_FAILED` | 不需要 | 如果交易尚未过期，可尝试重新执行一次 |
| `TX_FAILED_ONCHAIN` | 不需要 | 交易在链上执行失败（例如因滑点问题），请勿重试 |
| `RPC_UNAVAILABLE` | 需要 | 等待3秒后重试（最多尝试2次） |

## 使用指南

1. **执行任何操作前务必确认。** 向用户展示准备阶段的交易摘要，并等待其明确表示“同意”或“开始”。
2. **切勿自动重试在链上执行失败的交易。** 如果交易在链上执行失败，系统会尝试重新发送交易。
3. 在重新准备交易时，请再次确认用户意愿。如果报价信息已过期，请重新展示最新的报价信息（价格可能已发生变化）。
4. 所有金额均以基本单位计算：1 SOL = 1000000000，1 USDC = 1000000。
5. 如果用户请求交换的代币不在支持列表中，请询问其发行地址，切勿自行猜测。
6. 交易完成后，请提供Solscan链接：`https://solscan.io/tx/{signature}`

## 安全性说明

- 该功能使用用户配置的密钥对来签署交易，不会创建、导入或管理任何密钥。
- 密钥对相关信息不会被记录或公开。
- 如果需要连接到第三方地址，请使用`--allowThirdParty`参数。
- 所有交易均会应用滑点保护机制（通过`minOut`参数设置）。
- 准备好的交易默认在120秒后失效。

## 限制事项（v1）

- 由于Jupiter采用无认证方式，某些代币（如Token2022和pump.fun）可能无法使用。
- 该功能不提供最优价格匹配服务，会直接使用Jupiter提供的交易路径。
- 交易金额的计算基于交易前后的账户余额差值（尽力提供最准确的结果）。
- 仅支持Solana主网交易。