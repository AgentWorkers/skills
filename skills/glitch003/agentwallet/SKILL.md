---
name: Vincent - A wallet for agents
description: >
  该技能用于管理EVM（以太坊虚拟机）链上的交易以及原始签名操作。当用户需要创建钱包、转账代币、在去中心化交易所（DEX）中进行交易、与智能合约交互或签署消息时，可以使用此技能。  
  相关触发事件包括：`wallet`、`create wallet`、`transfer ETH`、`swap tokens`、`send transaction`、`check balance`、`EVM wallet`、`raw signer`、`sign message`。
allowed-tools: Read, Write, Bash(npx:@vincentai/cli*)
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
# Vincent – 一个专为代理设计的钱包

使用此技能可以安全地为代理创建一个钱包，用于转账、交换以及在任何EVM链上进行交易，而无需向代理暴露私钥。创建钱包后，设置支出策略，代理就可以在您定义的范围内转移代币、进行交换和与智能合约交互。

**代理永远不会看到私钥。**所有交易都在服务器端通过ZeroDev智能账户执行。代理会收到一个受限的API密钥，该密钥仅能执行钱包所有者策略允许的操作。私钥永远不会离开Vincent服务器。

所有命令都使用`@vincentai/cli`包。API密钥会自动存储和解析——您无需处理原始密钥或文件路径。

## 安全模型

此技能旨在实现**在服务器端控制下的自主代理操作**。理解这一模型非常重要：

**不需要环境变量**，因为此技能采用“代理优先”的接入方式：代理在运行时通过调用Vincent API来创建自己的钱包，API会返回一个受限的API密钥。无需预先配置任何凭证。CLI会在创建钱包时自动存储返回的API密钥。密钥的存储路径（`${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/credentials/agentwallet/` 或 `./agentwallet/`）在技能的元数据中进行了声明。

**代理的API密钥并非私钥。**它是一个受限的令牌，仅能在钱包所有者设定的策略范围内执行交易。Vincent服务器会在服务器端强制执行所有策略——无论代理发送什么，都无法绕过这些策略。如果交易违反策略，服务器会拒绝该交易。如果交易需要批准，服务器会暂停交易并通过Telegram通知钱包所有者进行人工审批。

**有意启用模型调用。**此技能的目的是让AI代理具备自主管理钱包的能力。代理应在人类操作员定义的范围内自行执行钱包操作（转账、交换、调用合约）。人类通过策略（支出限制、地址白名单、代币白名单、函数白名单、审批阈值）来控制代理的行为——而不是通过限制单个调用来实现。存储的密钥是受限的，并受策略约束——即使其他进程读取了密钥，也只能执行钱包所有者允许的操作，且所有者可以立即撤销该密钥。

**所有API调用都通过HTTPS/TLS仅发送到`heyvincent.ai`。**不会接触其他端点、服务或外部主机。代理不会读取、收集或传输超出钱包操作所需的数据。

**Vincent是开源的，并经过了审计。**执行策略、管理私钥和执行交易的服务器端代码在[github.com/HeyVincent-ai/Vincent](https://github.com/HeyVincent-ai/Vincent)上公开可审计。Vincent后端会定期进行安全审计，涵盖密钥管理、策略执行、交易签名和API认证等方面。您可以验证策略执行的方式、私钥的存储方式、受限API密钥的验证方式以及撤销机制——没有任何信息是隐藏的。如果您希望自行托管Vincent而不是依赖托管服务，仓库中提供了部署说明。

**密钥生命周期：**

- **创建**：代理运行`secret create`命令——CLI会自动存储API密钥，并返回`keyId`和`claimUrl`。
- **声明所有权**：人类操作员使用`claimUrl`来声明所有权并配置策略。
- **撤销**：钱包所有者可以随时通过`https://heyvincent.ai`撤销代理的API密钥。被撤销的密钥会被服务器立即拒绝。
- **重新链接**：如果代理丢失了API密钥，钱包所有者可以生成一个一次性重新链接令牌，代理通过`secret relink`命令用它来获取新的密钥。
- **轮换**：钱包所有者可以随时撤销当前密钥并生成一个新的重新链接令牌以更换凭证。

## 应使用哪种Secret类型

| 类型         | 使用场景                                      | 网络                 | Gas              |
| ------------ | ----------------------------------------- | ----------------------- | ---------------- |
| `EVM_WALLET` | 转账、交换、DeFi、调用智能合约                    | 任何EVM链           | 免费（由赞助商提供） |
| `RAW_SIGNER` | 为特殊协议提供原始消息签名                         | 任何（以太坊 + Solana）         | 需要付费          |

**建议选择`EVM_WALLET`（默认）**，用于：**

- 发送ETH或代币
- 在DEX上进行代币交换
- 与智能合约交互
- 执行任何标准的EVM交易

**仅在以下情况下选择`RAW_SIGNER`：**

- 需要为不支持智能账户的协议提供原始ECDSA/Ed25519签名
- 需要为自己广播的交易哈希签名
- 需要Solana签名

## 快速入门

### 1. 检查是否存在现有密钥

在创建新钱包之前，先检查是否已经存在密钥：

```bash
npx @vincentai/cli@latest secret list --type EVM_WALLET
```

如果返回了密钥，请将其`id`作为后续命令的`--key-id`参数。如果没有密钥，则创建一个新的钱包。

### 2. 创建钱包

```bash
npx @vincentai/cli@latest secret create --type EVM_WALLET --memo "My agent wallet" --chain-id 84532
```

创建完成后，告知用户：

> “这是您的钱包声明URL：`<claimUrl>`。使用此URL来声明所有权、设置支出策略，并在https://heyvincent.ai上监控代理的钱包活动。”

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

返回所有ERC-20代币及其符号、小数位数、图标和USD价值的余额。

### 5. 转移ETH或代币

```bash
# Transfer native ETH
npx @vincentai/cli@latest wallet transfer --key-id <KEY_ID> --to 0xRecipient --amount 0.01

# Transfer ERC-20 token
npx @vincentai/cli@latest wallet transfer --key-id <KEY_ID> --to 0xRecipient --amount 100 --token 0xTokenAddress
```

如果交易违反策略，服务器会返回错误信息，说明触发了哪条策略。如果交易需要人工批准（基于审批阈值策略），服务器会返回`status: "pending_approval"`，钱包所有者会收到Telegram通知以进行批准或拒绝。

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
- `--chain-id`：1 = 以太坊，137 = Polygon，42161 = Arbitrum，10 = Optimism，8453 = Base等。
- `--slippage`：滑点容忍度（以基点为单位，100 = 1%）。默认值为100。此命令仅用于预览，不执行实际操作。

预览会显示预期的购买金额、路由信息和费用，而不会执行实际交换。执行命令则会完成交换，并自动处理ERC20的审批流程。

### 7. 发送任意交易

通过发送自定义的calldata与任何智能合约交互：

```bash
npx @vincentai/cli@latest wallet send-tx --key-id <KEY_ID> --to 0xContract --data 0xCalldata --value 0
```

### 8. 在不同的Secret之间转移资金

在您拥有的Vincent Secret之间转移资金（例如，从一个EVM钱包转移到另一个钱包，或转移到Polymarket钱包）。Vincent会验证您是否拥有这两个Secret，并自动处理任何代币转换或跨链桥接：

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

**行为：**

- **相同代币+相同链**：作为直接转账执行（费用由赞助商承担）。
- **不同代币或链**：使用中继服务进行原子交换和桥接。
- 目标Secret可以是`EVM_WALLET`或`POLYMARKET_WALLET`。
- 服务器会验证您是否拥有源Secret和目标Secret——如果目标Secret不在您的控制范围内，转移将被拒绝。
- 转移受到与常规转账相同的服务器端策略约束（支出限制、审批阈值等）。

## 输出格式

CLI命令将结果以JSON格式输出到stdout。成功响应会包含相关数据：

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
|-------|-------|------------|
| `401 Unauthorized` | API密钥无效或缺失 | 确认`key-id`是否正确；如有必要，请重新链接 |
| `403 Policy Violation` | 交易被服务器端策略阻止 | 用户需在heyvincent.ai调整策略 |
| `400 Insufficient Balance` | 转账所需代币不足 | 转账前请检查余额 |
| `429 Rate Limited` | 请求过多 | 等待一段时间后重试 |
| `pending_approval` | 交易超出审批阈值 | 用户会收到Telegram通知以进行批准或拒绝 |
| `Key not found` | API密钥已被撤销或从未创建 | 请使用钱包所有者提供的新令牌重新链接 |

如果交易被拒绝，请告知用户在`https://heyvincent.ai`检查他们的策略设置。

## 策略（服务器端执行）

钱包所有者可以通过`https://heyvincent.ai`上的声明URL来设置策略，从而控制代理的行为。所有策略都由Vincent API在服务器端执行——代理无法绕过或修改这些策略。如果交易违反策略，API会拒绝该交易。如果交易触发了审批阈值，API会暂停交易并通过Telegram通知钱包所有者进行人工审批。策略执行逻辑在[github.com/HeyVincent-ai/Vincent](https://github.com/HeyVincent-ai/Vincent)上公开可审计。

| 策略                        | 功能                                      |
| --------------------------- | ------------------------------------------------------------------- |
| **Address allowlist**       | 仅允许向特定地址转账/调用                         |
| **Token allowlist**         | 仅允许转移特定的ERC-20代币                         |
| **Function allowlist**      | 仅允许调用特定的合约函数（通过4字节选择器）                   |
| **Spending limit (per tx)** | 每笔交易的最大USD价值                           |
| **Spending limit (daily)**  | 每24小时内的最大USD价值                           |
| **Spending limit (weekly)** | 每7天内的最大USD价值                           |
| **Require approval**        | 每笔交易都需要通过Telegram进行人工审批                     |
| **Approval threshold**      | 超过指定金额的交易需要人工批准                         |

在声明所有权之前，代理可以无策略限制地操作。这是有意设计的：代理优先的接入方式允许代理立即开始积累和管理资金。一旦人类操作员通过声明URL声明了钱包所有权，他们可以添加任何策略来限制代理的行为。钱包所有者也可以随时完全撤销代理的API密钥。

## 重新链接（恢复API访问）

如果代理丢失了API密钥，钱包所有者可以从前端生成一个**重新链接令牌**。代理随后可以使用此令牌获取新的API密钥。

**操作流程：**

1. 用户从`https://heyvincent.ai`的钱包详情页面生成重新链接令牌。
2. 用户将令牌提供给代理（例如，通过聊天发送）。
3. 代理运行`relink`命令：

```bash
npx @vincentai/cli@latest secret relink --token <TOKEN_FROM_USER>
```

CLI会用该令牌获取新的API密钥，自动存储它，并返回新的`keyId`。后续命令请使用这个`keyId`。

**重要提示：**重新链接令牌是一次性使用的，10分钟后失效。

## 重要注意事项

- **无需支付Gas费用。**所有交易费用都由赞助商承担——钱包不需要ETH作为Gas费用。
- **切勿尝试访问原始的Secret值。**私钥始终保存在服务器端——这就是设计的目的。
- 创建钱包后，请务必将声明URL分享给用户。
- 如果交易被拒绝，可能是由于服务器端策略的限制。请告知用户在`https://heyvincent.ai`检查他们的策略设置。
- 如果交易需要审批，系统会返回`status: "pending_approval"`。钱包所有者会收到Telegram通知以进行批准或拒绝。

---

## 原始签名器（高级功能）

用于在智能账户无法使用时进行原始ECDSA/Ed25519签名：

### 创建原始签名器

```bash
npx @vincentai/cli@latest secret create --type RAW_SIGNER --memo "My raw signer"
```

响应中包含从同一种子生成的以太坊（secp256k1）和Solana（ed25519）地址。

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

返回一个十六进制编码的签名。对于以太坊，签名格式为`r || s || v`（65字节）。对于Solana，签名格式为64字节的ed25519签名。