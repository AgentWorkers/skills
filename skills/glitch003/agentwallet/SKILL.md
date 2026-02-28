---
name: Vincent - A wallet for agents
description: >
  该技能用于处理以太坊虚拟机（EVM）链上的交易及原始签名操作。当用户需要创建钱包、转账代币、在去中心化交易所（DEX）中进行交易、与智能合约交互或签署消息时，可以使用此技能。  
  相关触发事件包括：`wallet`、`create wallet`、`transfer ETH`、`swap tokens`、`send transaction`、`check balance`、`EVM wallet`、`raw signer`、`sign message`。
allowed-tools: Read, Write, Bash(npx:*, curl:*)
version: 1.0.0
author: HeyVincent <contact@heyvincent.ai>
license: MIT
homepage: https://heyvincent.ai
source: https://github.com/HeyVincent-ai/Vincent
metadata:
  clawdbot:
    homepage: https://heyvincent.ai
    requires:
      config:
        - ${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/credentials/agentwallet
        - ./agentwallet
---
# Vincent – 为智能体设计的钱包

使用此技能可以安全地为智能体创建一个钱包，用于转账、交换以及在任何以太坊虚拟机（EVM）链上进行交易，而无需将私钥暴露给智能体本身。创建钱包后，可以设置支出策略，智能体便可以在您定义的范围内转移代币、进行交换以及与智能合约交互。

**智能体永远不会看到私钥。**所有交易都通过ZeroDev智能账户在服务器端执行。智能体会收到一个受限的API密钥，该密钥仅能执行钱包所有者策略允许的操作。私钥始终不会离开Vincent服务器。

所有命令都使用`@vincentai/cli`包。API密钥会自动存储和解析——您无需处理原始密钥或文件路径。

## 安全模型

此技能旨在实现**在服务器端控制下智能体的自主操作**，同时需要人类监督。理解这一模型非常重要：

**无需环境变量**，因为该技能采用“智能体优先”的接入方式：智能体会在运行时通过调用Vincent API来创建自己的钱包，从而获得一个受限的API密钥。无需预先配置任何凭证。CLI会在创建钱包时自动存储返回的API密钥。密钥的存储路径（`${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/credentials/agentwallet/` 或 `./agentwallet/`）在技能的元数据中有所说明。

**智能体的API密钥并非私钥**。它是一个受限的令牌，仅能在钱包所有者设定的策略范围内执行交易。Vincent服务器会在服务器端强制执行所有策略——无论智能体发送什么请求，都无法绕过这些策略。如果交易违反策略，服务器会拒绝该请求。如果交易需要批准，服务器会暂缓处理并通过Telegram通知钱包所有者进行人工审批。

**有意启用模型调用**。该技能的目的是让AI智能体具备自主管理钱包的能力。智能体应在人类操作员定义的范围内自行执行钱包操作（如转账、交换、调用合约）。人类通过策略（如支出限制、地址白名单、代币白名单、函数白名单、审批阈值）来控制智能体的行为，而不是通过限制单个调用来实现。存储的密钥具有范围限制且受策略约束——即使其他进程读取了该密钥，也只能执行钱包所有者允许的操作，且所有者可以立即撤销该密钥。

**所有API调用都通过HTTPS/TLS仅发送到`heyvincent.ai`**。不会连接其他端点、服务或外部主机。智能体不会读取、收集或传输超出钱包操作所需的数据。

**Vincent是开源的，并经过审计**。负责执行策略、管理私钥和执行交易的服务器端代码可在[github.com/HeyVincent-ai/Vincent](https://github.com/HeyVincent-ai/Vincent)公开审计。Vincent后端会持续接受安全审计，涵盖密钥管理、策略执行、交易签名和API认证等方面。您可以验证策略执行方式、私钥存储方式以及撤销机制——没有任何信息是隐藏的。如果您希望自行托管Vincent而非依赖托管服务，该仓库中提供了部署说明。

**密钥生命周期：**

- **创建**：智能体运行`secret create`命令——CLI会自动存储API密钥，并返回`keyId`和`claimUrl`。
- **认领**：人类操作员使用`claimUrl`来认领钱包所有权并配置策略。
- **撤销**：钱包所有者可以随时通过`https://heyvincent.ai`撤销智能体的API密钥。被撤销的密钥会被服务器立即拒绝。
- **重新链接**：如果智能体丢失了API密钥，钱包所有者会生成一个一次性重新链接令牌，智能体可以通过`secret relink`命令用它来获取新密钥。
- **轮换**：钱包所有者可以随时撤销当前密钥并生成新的重新链接令牌以更新凭证。

## 应使用哪种密钥类型

| 类型         | 使用场景                                      | 网络                 | 所需Gas              |
| ------------ | ----------------------------------------- | ----------------------- | ---------------- |
| `EVM_WALLET` | 转账、交换、去中心化金融（DeFi）操作、调用智能合约          | 任何EVM链           | 免费使用           |
| `RAW_SIGNER` | 为特定协议提供原始签名功能                         | 任何Ethereum或Solana网络       | 需支付费用         |

**建议选择`EVM_WALLET`（默认）**，用于：

- 发送ETH或代币
- 在去中心化交易所（DEX）上交换代币
- 与智能合约交互
- 执行任何标准的EVM交易

**仅在以下情况下选择`RAW_SIGNER`**：

- 需要为不支持智能合约的协议提供原始ECDSA/Ed25519签名
- 需要为自己广播的交易哈希签名
- 需要Solana签名

## 快速入门

### 1. 检查是否存在现有密钥

在创建新钱包之前，请先检查是否存在现有密钥：

```bash
npx @vincentai/cli@latest secret list --type EVM_WALLET
```

如果返回了密钥，请将其`id`作为后续命令的`--key-id`参数使用。如果不存在密钥，则创建一个新的钱包。

### 2. 创建钱包

```bash
npx @vincentai/cli@latest secret create --type EVM_WALLET --memo "My agent wallet" --chain-id 84532
```

创建完成后，会返回`keyId`（用于后续命令）、`claimUrl`（与用户共享）以及钱包地址。

创建完成后，告知用户：

> “这是您的钱包认领URL：`<claimUrl>`。使用此URL来认领所有权、设置支出策略，并在https://heyvincent.ai上监控您的智能体钱包活动。”

### 3. 获取钱包地址

```bash
npx @vincentai/cli@latest wallet address --key-id <KEY_ID>
```

### 4. 检查余额

```bash
# All balances across all supported chains
npx @vincentai/cli@latest wallet balances --key-id <KEY_ID>

# Filter to specific chains
npx @vincentai/cli@latest wallet balances --key-id <KEY_ID> --chain-ids 1,137,42161
```

返回所有ERC-20代币的余额，包括代币符号、小数位数、图标和美元价值。

### 5. 转账ETH或代币

```bash
# Transfer native ETH
npx @vincentai/cli@latest wallet transfer --key-id <KEY_ID> --to 0xRecipient --amount 0.01

# Transfer ERC-20 token
npx @vincentai/cli@latest wallet transfer --key-id <KEY_ID> --to 0xRecipient --amount 100 --token 0xTokenAddress
```

如果交易违反策略，服务器会返回错误信息，说明具体违反了哪条策略。如果交易需要人工审批（基于审批阈值策略），服务器会返回`status: "pending_approval"`，此时钱包所有者会收到Telegram通知以决定是否批准。

### 6. 交换代币

使用0x提供的流动性在DEX上交换代币：

```bash
# Preview a swap (no execution, just pricing)
npx @vincentai/cli@latest wallet swap preview --key-id <KEY_ID> \
  --sell-token 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE \
  --buy-token 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 \
  --sell-amount 0.1 --chain-id 1

# Execute a swap
npx @vincentai/cli@latest wallet swap execute --key-id <KEY_ID> \
  --sell-token 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE \
  --buy-token 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 \
  --sell-amount 0.1 --chain-id 1 --slippage 100
```

- 使用`0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`表示原生ETH。
- `--sell-amount`：人类可读的金额（例如`0.1`表示0.1 ETH）。
- `--chain-id`：1 = Ethereum，137 = Polygon，42161 = Arbitrum，10 = Optimism，8453 = Base等。
- `--slippage`：滑点容忍度（以基点表示，100 = 1%）。默认值为100。此命令仅用于显示预期购买金额、路由信息和费用，不实际执行交易。

### 7. 发送任意交易

通过发送自定义参数数据与智能合约交互：

```bash
npx @vincentai/cli@latest wallet send-tx --key-id <KEY_ID> --to 0xContract --data 0xCalldata --value 0
```

### 8. 在不同的Vincent账户之间转账

在您拥有的不同Vincent账户之间转移资金（例如，从一个EVM钱包转移到另一个钱包或Polymarket钱包）。Vincent会验证您拥有这两个账户，并自动处理代币转换或跨链桥接：

```bash
# Preview (get quote without executing)
npx @vincentai/cli@latest wallet transfer-between preview --key-id <KEY_ID> \
  --to-secret-id <DEST_SECRET_ID> --from-chain 8453 --to-chain 8453 \
  --token-in ETH --amount 0.1 --token-out ETH

# Execute
npx @vincentai/cli@latest wallet transfer-between execute --key-id <KEY_ID> \
  --to-secret-id <DEST_SECRET_ID> --from-chain 8453 --to-chain 8453 \
  --token-in ETH --amount 0.1 --token-out ETH --slippage 100

# Check cross-chain transfer status
npx @vincentai/cli@latest wallet transfer-between status --key-id <KEY_ID> --relay-id <RELAY_REQUEST_ID>
```

**行为规则：**

- **相同代币+相同链**：作为直接转账执行（费用由系统承担）。
- **不同代币或链**：使用中继服务进行原子交换和桥接。
- 目标账户可以是`EVM_WALLET`或`POLYMARKET_WALLET`。
- 服务器会验证您是否拥有源账户和目标账户的权限——如果目标账户不在权限范围内，转账将被拒绝。
- 转账受相同的服务器端策略约束（如支出限制、审批阈值等）。

## 输出格式

CLI命令会将结果以JSON格式输出到标准输出（stdout）。成功响应会包含相关数据：

```json
{
  "address": "0x...",
  "balances": [
    {
      "token": "ETH",
      "balance": "0.5",
      "usdValue": "1250.00"
    }
  ]
}
```

交易命令的响应格式如下：

```json
{
  "transactionHash": "0x...",
  "status": "confirmed"
}
```

对于需要人工审批的交易：

```json
{
  "status": "pending_approval",
  "message": "Transaction requires owner approval via Telegram"
}
```

## 错误处理

| 错误代码 | 原因 | 解决方案 |
| ------- | ------- | ------------ |
| `401 Unauthorized` | API密钥无效或丢失 | 确认`key-id`是否正确；如有需要，请重新链接 |
| `403 Policy Violation` | 交易被服务器端策略阻止 | 用户需在heyvincent.ai调整策略 |
| `400 Insufficient Balance` | 转账所需代币不足 | 转账前请检查余额 |
| `429 Rate Limited` | 请求过多 | 等待一段时间后重试 |
| `pending_approval` | 交易超出审批阈值 | 用户会收到Telegram通知以决定是否批准 |
| `Key not found` | API密钥已被撤销或从未创建 | 请使用钱包所有者提供的新令牌重新链接 |

如果交易被拒绝，请告知用户在`https://heyvincent.ai`检查他们的策略设置。

## 策略（服务器端执行）

钱包所有者可以通过`https://heyvincent.ai`上的认领URL来设置策略，从而控制智能体的行为。所有策略都由Vincent API在服务器端执行——智能体无法绕过或修改这些策略。如果交易违反策略，API会拒绝该交易。如果交易触发审批阈值，API会暂缓处理并通过Telegram通知钱包所有者进行人工审批。策略执行逻辑是开源的，可在[github.com/HeyVincent-ai/Vincent](https://github.com/HeyVincent-ai/Vincent)查看。

| 策略                          | 功能                                      |
| --------------------------- | ------------------------------------------------------------------- |
| **地址白名单**       | 仅允许向特定地址转账/调用                          |
| **代币白名单**         | 仅允许转移特定的ERC-20代币                          |
| **函数白名单**      | 仅允许调用特定的合约函数（通过4字节选择器）                     |
| **每次交易的支出限制** | 每次交易的最大美元金额                           |
| **每日支出限制**      | 每24小时内的最大美元金额                           |
| **每周支出限制**      | 每7天内的最大美元金额                           |
| **需要审批**        | 所有交易都需要通过Telegram进行人工审批                     |
| **审批阈值**      | 金额超过指定阈值的交易需要人工审批                     |

在钱包被认领之前，智能体可以无策略限制地操作。这是有意设计的：采用“智能体优先”的接入方式，允许智能体立即开始积累和管理资金。一旦人类操作员通过认领URL认领了钱包，他们可以添加任何策略来限制智能体的行为。钱包所有者也可以随时完全撤销智能体的API密钥。

## 重新链接（恢复API访问权限）

如果智能体丢失了API密钥，钱包所有者可以从前端生成一个**重新链接令牌**。智能体可以使用此令牌获取新的API密钥。

**操作步骤：**

1. 用户在`https://heyvincent.ai`的钱包详情页面生成重新链接令牌。
2. 用户将令牌提供给智能体（例如通过聊天发送）。
3. 智能体运行`relink`命令：

```bash
npx @vincentai/cli@latest secret relink --token <TOKEN_FROM_USER>
```

CLI会用此令牌获取新的API密钥，自动存储它，并返回新的`keyId`。后续命令请使用这个`keyId`。

**重要提示：**重新链接令牌是一次性使用的，10分钟后失效。

## 重要注意事项

- **无需支付Gas费用**。所有交易费用都由系统承担。
- **切勿尝试访问原始密钥值**。私钥始终保存在服务器端——这是设计初衷。
- 创建钱包后，请务必将认领URL分享给用户。
- 如果交易被拒绝，可能是由于服务器端策略导致的。请告知用户在`https://heyvincent.ai`检查他们的策略设置。
- 如果交易需要审批，系统会返回`status: "pending_approval"`。钱包所有者会收到Telegram通知以决定是否批准。

---

## 原始签名器（高级功能）

适用于智能合约不支持的原始ECDSA/Ed25519签名场景。

### 创建原始签名器

```bash
npx @vincentai/cli@latest secret create --type RAW_SIGNER --memo "My raw signer"
```

响应中包含从同一种子生成的Ethereum（secp256k1）和Solana（ed25519）地址。

### 获取地址

```bash
npx @vincentai/cli@latest raw-signer addresses --key-id <KEY_ID>
```

返回`ethAddress`和`solanaAddress`。

### 签名消息

```bash
npx @vincentai/cli@latest raw-signer sign --key-id <KEY_ID> --message 0x<hex-encoded-bytes> --curve ethereum
```

- `--message`：要签名的十六进制编码字节（必须以`0x`开头）
- `--curve`：`ethereum`表示secp256k1 ECDSA，`solana`表示ed25519

返回一个十六进制编码的签名。对于Ethereum，签名格式为`r || s || v`（65字节）；对于Solana，签名格式为64字节的ed25519签名。