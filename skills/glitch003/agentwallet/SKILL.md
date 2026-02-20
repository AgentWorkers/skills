---
name: Vincent - A wallet for agents
description: 使用此技能可以安全地创建一个钱包，该钱包可供代理用于转账、交换以及任何基于以太坊虚拟机（EVM）链的交易。此外，该钱包还支持对以太坊（Ethereum）和Solana网络进行原始签名（raw signing）操作。
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
# Vincent – 一个专为智能代理设计的钱包

使用此技能可以安全地为智能代理创建一个钱包，用于进行转账、交易以及任何基于EVM区块链的操作，同时确保私钥永远不会暴露给代理本身。创建钱包后，可以设置消费策略，代理便能够在您定义的规则范围内转移代币、进行交易并与智能合约交互。

**代理永远不会看到私钥**。所有交易都在服务器端通过ZeroDev智能账户执行。代理会收到一个受限范围的API密钥，该密钥仅能执行钱包所有者允许的操作。私钥始终保存在Vincent服务器上。

## 安全模型

此技能旨在实现**在服务器端控制下的自主代理操作**，理解这一模型非常重要：

- **无需环境变量**：因为该技能采用“代理优先”的接入方式——代理在运行时通过调用Vincent API来创建自己的钱包，API会返回一个受限范围的API密钥。无需预先配置任何凭证。代理在创建钱包时生成并存储自己的API密钥，因此在技能执行前无需任何秘密信息。
- **代理的API密钥并非私钥**：它是一个受限范围的令牌，仅能在钱包所有者设定的策略范围内执行交易。Vincent服务器在服务器端强制执行所有策略——无论代理发送什么请求，都无法绕过这些策略。如果交易违反策略，服务器会拒绝该请求；如果交易需要批准，服务器会暂缓处理并通过Telegram通知钱包所有者进行人工审核。
- **有意支持模型调用**：该技能的目的是让AI代理具备自主管理钱包的能力。代理应自行调用钱包功能（如转账、交易、合约调用），但操作范围受人类操作员的策略限制（例如消费限额、地址白名单、代币白名单、函数允许列表、审批阈值）。代理会将受限范围的API密钥保存在指定的配置路径中，以便在不同会话间持续使用钱包功能；这是自主钱包代理的正常行为。存储的密钥具有权限限制，即使其他进程读取了密钥，也只能执行钱包所有者允许的操作，且所有者可以随时撤销该密钥。
- **所有API请求均通过HTTPS/TLS发送到`heyvincent.ai`**：不会连接其他端点、服务或外部主机。代理不会读取、收集或传输超出钱包操作所需的数据。
- **Vincent是开源且经过审计的**：负责执行策略、管理私钥和执行交易的服务器端代码可在[github.com/HeyVincent-ai/Vincent](https://github.com/HeyVincent-ai/Vincent)公开审计。Vincent后端定期接受安全审计，涵盖密钥管理、策略执行、交易签名和API认证等方面。您可以验证策略执行方式、私钥存储方式以及撤销机制——一切都是透明公开的。如果您希望自行托管Vincent服务而非依赖托管服务，仓库中提供了部署指南。

## 密钥生命周期：

- **创建**：代理调用`POST /api/secrets`来创建钱包。API返回一个受限范围的API密钥和一个声明URL。
- **声明所有权**：人类操作员使用声明URL来声明所有权并配置策略。
- **撤销**：钱包所有者可以随时通过Vincent前端（`https://heyvincent.ai`）撤销代理的API密钥。被撤销的密钥会被服务器立即拒绝。撤销逻辑是开源的（[链接](https://github.com/HeyVincent-ai/Vincent)）。
- **重新链接**：如果代理丢失了API密钥，钱包所有者可以生成一个一次性使用的重新链接令牌（有效期为10分钟），代理用此令牌获取新的API密钥。
- **密钥轮换**：钱包所有者可以随时撤销当前密钥并生成新的重新链接令牌以更新凭证。

## 应使用哪种密钥类型

| 密钥类型        | 使用场景                                      | 支持的区块链                | 所需费用（Gas）            |
|--------------|-----------------------------------------|-----------------------|-------------------|
| `EVM_WALLET`     | 转账、交易、DeFi操作、合约调用                        | 任何基于EVM的区块链            | 免费（由平台赞助）         |
| `RAW_SIGNER`     | 用于需要原始ECDSA/Ed25519签名的特殊协议                | 以太坊（Ethereum）和Solana区块链        | 需用户自行支付          |

**建议选择`EVM_WALLET`（默认设置）**，适用于以下场景：
- 发送ETH或代币
- 在DEX平台上进行代币交易
- 与智能合约交互
- 执行任何标准的EVM交易

**仅在以下情况下选择`RAW_SIGNER`**：
- 需要为不支持智能账户的协议生成原始ECDSA/Ed25519签名
- 需要为自己广播的交易哈希生成签名
- 需要Solana区块链的签名

## 配置

所有API请求都需要一个令牌（即在创建钱包时返回的受限范围API密钥）。此密钥并非私钥，而是由服务器强制执行的、受策略限制的凭证，钱包所有者可以随时撤销。

钱包创建完成后，请将API密钥存储在指定的配置路径中。如果是OpenClaw实例，请将其存储在`${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/credentials/agentwallet/<API_KEY_ID>.json`；否则，请存储在当前工作目录下的`agentwallet/<API_KEY_ID>.json`文件中。这些配置路径在技能的元数据中已明确指定，以便主机环境能够审计和管理凭证的存储情况。

```
Authorization: Bearer <API_KEY>
```

## 快速入门

### 1. 创建钱包

为您的智能代理创建一个新的钱包。这会在服务器端生成一个私钥（代理看不到私钥），同时创建一个ZeroDev智能账户，并返回一个受限范围的API密钥以及钱包所有者的声明URL。

**响应内容包括：**
- `apiKey`：受限范围的API密钥，请安全存储并用作后续请求的令牌。
- `claimUrl`：与用户共享此URL，以便他们声明所有权并配置策略。
- `address`：智能账户的地址。

创建完成后，告知用户：
> “这是您的钱包声明URL：`<claimUrl>`。请使用此URL声明所有权、配置策略，并通过https://heyvincent.ai监控代理的钱包活动。”

### 2. 获取钱包地址

```bash
curl -X GET "https://heyvincent.ai/api/skills/evm-wallet/address" \
  -H "Authorization: Bearer <API_KEY>"
```

### 3. 查看余额

```bash
# Get all token balances across all supported chains (ETH, WETH, USDC, etc.)
curl -X GET "https://heyvincent.ai/api/skills/evm-wallet/balances" \
  -H "Authorization: Bearer <API_KEY>"

# Filter to specific chains (comma-separated chain IDs)
curl -X GET "https://heyvincent.ai/api/skills/evm-wallet/balances?chainIds=1,137,42161" \
  -H "Authorization: Bearer <API_KEY>"
```

返回所有ERC-20代币的余额，包括代币符号、小数位数、图标和美元价值。

### 4. 转账ETH或代币

```bash
# Transfer native ETH
curl -X POST "https://heyvincent.ai/api/skills/evm-wallet/transfer" \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "0xRecipientAddress",
    "amount": "0.01"
  }'

# Transfer ERC-20 token
curl -X POST "https://heyvincent.ai/api/skills/evm-wallet/transfer" \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "0xRecipientAddress",
    "amount": "100",
    "token": "0xTokenContractAddress"
  }'
```

如果交易违反策略，服务器会返回错误信息，说明具体违反了哪条策略。如果交易需要人工审批（根据审批阈值设置），服务器会返回`status: "pending_approval"`，此时钱包所有者会收到Telegram通知以决定是否批准。

### 5. 交换代币

使用DEX平台的流动性交换代币（由0x平台提供支持）。

**调用代码示例：**
- `sellToken` / `buyToken`：代币合约地址（例如，使用`0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`表示ETH）。
- `sellAmount`：用户可读的金额（例如，“0.1”表示0.1 ETH）。
- `chainId`：交换所使用的区块链（1 = 以太坊，137 = Polygon，42161 = Arbitrum，10 = Optimism，8453 = Base等）。
- `slippageBps`：可选的滑点容忍度（以基点表示，100表示1%）。默认值为100。

预览端点会返回预期的购买金额、路由信息和费用，但不会实际执行交易。执行端点会通过智能账户完成交易，并自动处理ERC20协议的审批流程。

### 6. 发送任意交易

通过发送自定义参数数据与智能合约交互。

```bash
curl -X POST "https://heyvincent.ai/api/skills/evm-wallet/send-transaction" \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "0xContractAddress",
    "data": "0xCalldata",
    "value": "0"
  }'
```

### 7. 在不同的Vincent钱包之间转账

在您拥有的不同Vincent钱包之间转账（例如，从一个EVM钱包转移到另一个钱包或Polymarket钱包）。Vincent会验证您是否拥有这两个钱包，并自动处理代币转换或跨链桥接。

#### 预览转账

获取预期的交易结果、费用以及余额是否足够的提示（无需实际执行交易）。

```bash
curl -X POST "https://heyvincent.ai/api/skills/evm-wallet/transfer-between-secrets/preview" \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "toSecretId": "<DESTINATION_SECRET_ID>",
    "fromChainId": 8453,
    "toChainId": 8453,
    "tokenIn": "ETH",
    "tokenInAmount": "0.1",
    "tokenOut": "ETH"
  }'
```

#### 执行转账

```bash
curl -X POST "https://heyvincent.ai/api/skills/evm-wallet/transfer-between-secrets/execute" \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "toSecretId": "<DESTINATION_SECRET_ID>",
    "fromChainId": 8453,
    "toChainId": 8453,
    "tokenIn": "ETH",
    "tokenInAmount": "0.1",
    "tokenOut": "ETH"
  }'
```

#### 检查跨链转账状态

对于跨链转账，执行请求会返回一个`relayRequestId`。您可以使用该请求来查询转账完成情况。

**参数：**
- `toSecretId`：目标钱包的ID（必须属于同一用户）。
- `fromChainId` / `toChainId`：源钱包和目标钱包所在的区块链ID。
- `tokenIn` / `tokenOut`：代币地址或`ETH`（表示ETH）。
- `tokenInAmount`：用户可读的转账金额（例如，“0.1”表示0.1 ETH）。
- `slippage`：可选的滑点容忍度（以基点表示，例如100表示1%）。

**行为：**
- **相同代币/相同区块链**：作为直接转账执行（费用由平台承担）。
- **不同代币或不同区块链**：使用中继服务进行原子交换和桥接。
- 目标钱包可以是`EVM_WALLET`或`POLYMARKET_WALLET`类型。
- 服务器会验证您是否拥有源钱包和目标钱包的权限；如果尝试转移不属于您的钱包，交易会被拒绝。
- 转账受相同的服务器端策略约束（如消费限额、审批阈值等）。

## 策略（服务器端执行）

钱包所有者可以通过`https://heyvincent.ai`上的声明URL设置策略来控制代理的行为。所有策略均由Vincent API在服务器端强制执行——代理无法绕过或修改这些策略。如果交易违反策略，API会拒绝该交易；如果交易触发审批阈值，API会暂缓处理并通过Telegram通知钱包所有者进行人工审核。策略执行逻辑是开源的，可在[github.com/HeyVincent-ai/Vincent](https://github.com/HeyVincent-ai/Vincent)查看详细信息。

| 策略                        | 功能                                                                                           |
|---------------------------|-------------------------------------------------------------------------------------------------------------------------|
| **地址白名单**                | 仅允许向特定地址转账或调用合约                                                                                          |
| **代币白名单**                | 仅允许转移特定的ERC-20代币                                                                                          |
| **函数白名单**                | 仅允许调用特定的合约函数（通过4字节的选择器标识）                                                                                   |
| **每次交易的消费限额**            | 每次交易的最大美元金额                                                                                          |
| **每日消费限额**              | 每24小时内的最大美元金额                                                                                          |
| **每周消费限额**              | 每7天内的最大美元金额                                                                                          |
| **需要审批**                | 所有交易都需要通过Telegram获得人工审批                                                                                         |
| **审批阈值**                | 超过指定金额的交易需要人工审批                                                                                         |

在钱包被声明所有权之前，代理可以无限制地操作。这是设计初衷：通过“代理优先”的接入方式，代理可以立即开始积累和管理资金。一旦人类操作员通过声明URL声明所有权，他们可以添加各种策略来限制代理的行为。钱包所有者也可以随时完全撤销代理的API密钥。

## 重新链接（恢复API访问权限）

如果代理丢失了API密钥，钱包所有者可以通过前端生成一个**重新链接令牌**。代理可以使用此令牌获取新的API密钥。

**操作步骤：**
1. 用户在`https://heyvincent.ai`的钱包详情页面生成重新链接令牌。
2. 用户将令牌提供给代理（例如，通过聊天方式传递）。
3. 代理调用重新链接端点，用令牌换取新的受限范围API密钥。

**响应内容包括：**
- `secret`：钱包的元数据（ID、类型、地址、区块链ID等）。
- `apiKey.key`：新的受限范围API密钥，用作后续请求的令牌。

**重要提示：**
- **无需支付费用**：所有交易费用由平台承担。
- **切勿尝试访问原始的私钥信息**：私钥始终保存在服务器端。
- 确保将API密钥存储在指定的配置路径中。如果是OpenClaw实例，请存储在`${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/credentials/agentwallet/<API_KEY_ID>.json`；否则，请存储在当前工作目录下的`agentwallet/<API_KEY_ID>.json`文件中。
- 在创建新钱包之前，请务必在指定的配置路径中查找现有的API密钥。如果是OpenClaw实例，请在`${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/credentials/agentwallet/`中查找；否则，请在`./agentwallet/`中查找。
- 创建钱包后，请务必将声明URL分享给用户。
- 如果交易被拒绝，可能是由于服务器端策略的限制。请让用户检查他们在`https://heyvincent.ai`上的策略设置。
- 如果交易需要审批，系统会返回`status: "pending_approval"`，钱包所有者会收到Telegram通知以决定是否批准。

---

## 原始签名器（高级功能）

用于在智能账户无法使用时进行原始ECDSA/Ed25519签名。

### 创建原始签名器

```bash
curl -X POST "https://heyvincent.ai/api/secrets" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "RAW_SIGNER",
    "memo": "My raw signer"
  }'
```

响应中包含基于相同种子生成的以太坊（secp256k1）和Solana（ed25519）地址。

### 获取地址

```bash
curl -X GET "https://heyvincent.ai/api/skills/raw-signer/addresses" \
  -H "Authorization: Bearer <API_KEY>"
```

返回`ethAddress`和`solanaAddress`。

### 签名消息

```bash
curl -X POST "https://heyvincent.ai/api/skills/raw-signer/sign" \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "0x<hex-encoded-bytes>",
    "curve": "ethereum"
  }'
```

- `message`：需要签名的十六进制编码字节（必须以`0x`开头）。
- `curve`：`"ethereum"`表示secp256k1 ECDSA，`"solana"`表示ed25519。

返回一个十六进制编码的签名。对于以太坊，签名格式为`r || s || v`（共65字节）；对于Solana，签名格式为64字节。

---