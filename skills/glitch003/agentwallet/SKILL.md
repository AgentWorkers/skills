---
name: Vincent - A wallet for agents
description: 使用此技能可以安全地创建一个钱包，该钱包可供代理用于转账、交换以及任何以太坊虚拟机（EVM）链上的交易。同时，该钱包还支持对以太坊和Solana网络进行原始签名操作（即直接生成用于验证交易的签名）。
homepage: https://heyvincent.ai
source: https://github.com/HeyVincent-ai/Vincent
metadata:
  clawdbot:
    homepage: https://heyvincent.ai
    requires:
      config:
        - ~/.openclaw/credentials/agentwallet
        - ./agentwallet
---
# Vincent – 一个专为代理设计的钱包

使用此技能可以安全地为代理创建一个钱包，代理可以使用该钱包进行转账、交换以及任何基于EVM链的交易，而无需暴露私钥。创建钱包后，设置相应的消费策略，代理便可以在您定义的规则范围内转移代币、进行交换以及与智能合约交互。

**代理永远不会看到私钥。**所有交易都通过ZeroDev智能账户在服务器端执行。代理会收到一个受限的API密钥，该密钥仅能执行钱包所有者允许的操作。私钥始终保存在Vincent服务器上。

## 安全模型

此技能旨在实现**在服务器端控制下的自主代理操作**，理解这一模型非常重要：

- **无需环境变量**，因为该技能采用“代理优先”的接入方式：代理在运行时通过调用Vincent API来创建自己的钱包，API会返回一个受限的API密钥。无需预先配置任何凭证。代理在创建钱包时生成并存储自己的API密钥——在技能运行之前无需任何秘密信息。
- **代理的API密钥并非私钥**，而是一个受限的承载令牌，仅能在钱包所有者设定的策略范围内执行交易。Vincent服务器在服务器端强制执行所有策略——无论代理发送什么请求，都无法绕过这些策略。如果交易违反策略，服务器会拒绝该请求。如果交易需要批准，服务器会暂停交易并通过Telegram通知钱包所有者进行人工审批。
- **有意支持模型调用**。该技能的目的是让AI代理具备自主管理钱包的能力。代理应在人工操作者设定的范围内自行执行钱包操作（如转账、交换、调用合约）。人工操作者通过策略（如消费限额、地址白名单、代币白名单、功能白名单、审批阈值）来控制代理的行为，而不是通过限制单个请求来实现控制。代理会将受限的API密钥保存在指定的配置路径中，以便在不同会话之间恢复钱包操作——这是自主钱包代理的预期行为。存储的密钥具有权限限制，即使其他进程读取了该密钥，也只能执行钱包所有者允许的操作，且所有者可以立即撤销该密钥。
- **所有API请求都通过HTTPS/TLS发送到`heyvincent.ai`**，不会连接其他端点、服务或外部主机。代理不会读取、收集或传输超出钱包操作所需的数据。
- **Vincent是开源的，并经过审计**。负责执行策略、管理私钥和执行交易的服务器端代码在[github.com/HeyVincent-ai/Vincent](https://github.com/HeyVincent-ai/Vincent)上公开可见。Vincent后端定期接受安全审计，涵盖密钥管理、策略执行、交易签名和API认证等方面。您可以验证策略执行的方式、私钥的存储方式、受限API密钥的验证方式以及撤销机制——没有任何隐藏的部分。如果您希望自行托管Vincent而不是依赖托管服务，仓库中提供了部署说明。

## 密钥生命周期：

- **创建**：代理调用`POST /api/secrets`来创建钱包。API会返回一个受限的API密钥和一个声明URL。
- **声明所有权**：人工操作者使用声明URL来获取钱包所有权并配置策略。
- **撤销**：钱包所有者可以在任何时候通过Vincent前端（`https://heyvincent.ai`）撤销代理的API密钥。被撤销的密钥会立即被服务器拒绝。撤销逻辑是开源的（[链接](https://github.com/HeyVincent-ai/Vincent)）。
- **重新链接**：如果代理丢失了API密钥，钱包所有者可以生成一个一次性使用的重新链接令牌（有效期为10分钟），代理用此令牌换取新的API密钥。
- **轮换**：钱包所有者可以随时撤销当前密钥并生成一个新的重新链接令牌以更新凭证。

## 应使用哪种密钥类型

| 密钥类型 | 使用场景                                      | 网络            | 所需Gas费用        |
| -------- | ----------------------------------------- | --------------------------- | ---------------- |
| `EVM_WALLET` | 转账、交换、DeFi操作、调用智能合约                      | 任何EVM链         | 免费（由Vincent赞助）   |
| `RAW_SIGNER` | 为特定协议生成原始签名                               | 任何区块链（Ethereum + Solana） | 需用户付费     |

**建议选择`EVM_WALLET`（默认）**，用于以下场景：
- 发送ETH或代币
- 在DEX上进行代币交换
- 与智能合约交互
- 执行任何标准的EVM交易

**仅在以下情况下选择`RAW_SIGNER`**：
- 需要为不支持智能账户的协议生成原始ECDSA/Ed25519签名
- 需要为自己广播的交易哈希生成签名
- 需要Solana签名

## 配置

所有API请求都需要一个承载令牌（即在创建钱包时返回的受限API密钥）。此密钥并非私钥，而是由服务器强制执行的、受策略限制的凭证，钱包所有者可以随时撤销。

钱包创建完成后，将API密钥存储在指定的配置路径中。如果是OpenClaw实例，请将其存储在`~/.openclaw/credentials/agentwallet/<API_KEY_ID>.json`中；否则，请将其存储在当前工作目录下的`agentwallet/<API_KEY_ID>.json`中。这些路径在技能的元数据中已明确说明，以便主机环境能够审计和管理凭证的存储情况。

```
Authorization: Bearer <API_KEY>
```

## 快速入门

### 1. 创建钱包

为代理创建一个新的智能账户钱包。这会在服务器端生成一个私钥（代理看不到私钥），同时创建一个ZeroDev智能账户，并返回一个受限的API密钥以及钱包所有者的声明URL。

**响应内容包括：**
- `apiKey`：一个受限的API密钥，需安全存储并用作未来所有请求的承载令牌
- `claimUrl`：与用户共享此URL，以便他们可以声明所有权并设置策略
- `address`：智能账户的地址

创建完成后，告知用户：
> “这是您的钱包声明URL：`<claimUrl>`。使用此URL来声明所有权、设置消费策略，并在https://heyvincent.ai上监控代理的钱包活动。”

### 2. 获取钱包地址

```bash
curl -X GET "https://heyvincent.ai/api/skills/evm-wallet/address" \
  -H "Authorization: Bearer <API_KEY>"
```

### 3. 检查余额

```bash
# Get all token balances across all supported chains (ETH, WETH, USDC, etc.)
curl -X GET "https://heyvincent.ai/api/skills/evm-wallet/balances" \
  -H "Authorization: Bearer <API_KEY>"

# Filter to specific chains (comma-separated chain IDs)
curl -X GET "https://heyvincent.ai/api/skills/evm-wallet/balances?chainIds=1,137,42161" \
  -H "Authorization: Bearer <API_KEY>"
```

返回所有ERC-20代币及其对应的符号、小数位数、图标和USD价值。

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

如果交易违反策略，服务器会返回错误信息，说明违反了哪条策略。如果交易需要人工批准（根据审批阈值策略），服务器会返回`status: "pending_approval"`，此时钱包所有者会收到Telegram通知以决定是否批准。

### 5. 交换代币

使用DEX的流动性交换一种代币为另一种代币（由0x提供支持）。

**调用代码示例：**
- `sellToken` / `buyToken`：代币合约地址。使用`0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeEeeE`表示ETH。
- `sellAmount`：用户可读的金额（例如`"0.1"`表示0.1 ETH）。
- `chainId`：交换所使用的区块链（1 = Ethereum，137 = Polygon，42161 = Arbitrum，10 = Optimism，8453 = Base等）。
- `slippageBps`：可选的滑点容忍度（以基点表示，100 = 1%）。默认值为100。

预览端点会返回预期的购买金额、路由信息和费用，但不会实际执行交易。执行端点会通过智能账户执行交换操作，并自动处理ERC20的审批流程。

### 6. 发送任意交易

通过发送自定义的calldata与任何智能合约进行交互。

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

### 7. 在不同的Vincent账户之间转账

在您拥有的不同Vincent账户之间转账资金（例如，从一个EVM钱包转移到另一个钱包或Polymarket钱包）。Vincent会验证您是否拥有这两个账户，并自动处理代币转换或跨链桥接。

#### 预览转账

获取预计的输出结果、费用以及余额是否足够的信息，而无需实际执行转账操作。

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

对于跨链转账，执行响应会包含一个`relayRequestId`。使用此请求来查询转账的完成情况。

**参数：**
- `toSecretId`：目标账户的ID（必须由同一用户拥有）。
- `fromChainId` / `toChainId`：源账户和目标账户所在的区块链ID。
- `tokenIn` / `tokenOut`：代币地址或`"ETH"`表示ETH。
- `tokenInAmount`：用户可读的转账金额（例如`"0.1"`）。
- `slippage`：可选的滑点容忍度（以基点表示，例如`100`表示1%）。

**行为：**
- **相同代币/相同区块链**：作为直接转账执行（费用由Vincent赞助）。
- **不同代币或不同区块链**：使用中继服务进行原子交换和桥接。
- 目标账户可以是`EVM_WALLET`或`POLYMARKET_WALLET`。
- 服务器会验证您是否拥有源账户和目标账户——如果尝试转移不属于您的账户，交易将被拒绝。
- 转账受相同的服务器端策略约束（如消费限额、审批阈值等）。

## 策略（服务器端执行）

钱包所有者可以通过`https://heyvincent.ai`上的声明URL设置策略来控制代理的行为。所有策略都由Vincent API在服务器端执行——代理无法绕过或修改这些策略。如果交易违反策略，API会拒绝该交易。如果交易触发审批阈值，API会暂停交易并通过Telegram通知钱包所有者进行人工审批。策略执行逻辑是开源的，可在[github.com/HeyVincent-ai/Vincent](https://github.com/HeyVincent-ai/Vincent)上查看。

| 策略                        | 功能                                                                                              |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **地址白名单**                | 仅允许向特定地址转账/调用                                                                                         |
| **代币白名单**                | 仅允许转移特定的ERC-20代币                                                                                         |
| **功能白名单**                | 仅允许调用特定的合约函数（通过4字节的选择器指定）                                                                                         |
| **每次交易的消费限额**            | 每次交易的最大USD金额                                                                                         |
| **每日消费限额**              | 每24小时内的最大USD金额                                                                                         |
| **每周消费限额**              | 每7天内的最大USD金额                                                                                         |
| **需要审批**                | 所有交易都需要通过Telegram获得人工审批                                                                                         |
| **审批阈值**                | 超过指定金额的交易需要人工审批                                                                                         |

在钱包被声明所有权之前，代理可以无限制地操作。这是设计初衷：通过“代理优先”的接入方式，代理可以立即开始积累和管理资金。一旦人工操作者通过声明URL声明了对钱包的所有权，他们就可以添加各种策略来限制代理的行为。钱包所有者也可以随时完全撤销代理的API密钥。

## 重新链接（恢复API访问权限）

如果代理丢失了API密钥，钱包所有者可以通过前端生成一个**重新链接令牌**。代理可以使用此令牌换取新的API密钥。

**操作步骤：**
1. 用户在`https://heyvincent.ai`的钱包详情页面生成一个重新链接令牌。
2. 用户将令牌提供给代理（例如通过聊天发送）。
3. 代理调用重新链接端点，用此令牌换取新的受限API密钥。

**响应内容包括：**
- `secret`：钱包的元数据（ID、类型、地址、chainId等）
- `apiKey.key`：新的受限API密钥，用作未来所有请求的承载令牌

**重要提示：**
- **无需支付Gas费用**。所有交易费用均由Vincent赞助。钱包无需使用ETH来支付Gas费用。
- **切勿尝试访问原始的秘密信息**。私钥始终保存在服务器端——这就是设计的目的。
- 确保将API密钥存储在指定的配置路径中。如果是OpenClaw实例，请将其存储在`~/.openclaw/credentials/agentwallet/<API_KEY_ID>.json`中；否则，请存储在当前工作目录下的`agentwallet/<API_KEY_ID>.json`中。
- 在创建新钱包之前，请务必在指定的配置路径中查找现有的API密钥。如果是OpenClaw实例，请在`~/.openclaw/credentials/agentwallet/`中查找；否则，请在`./agentwallet/`中查找。
- 创建钱包后，务必将声明URL分享给用户。
- 如果交易被拒绝，可能是由于服务器端的策略限制。请告知用户在`https://heyvincent.ai`检查他们的策略设置。
- 如果交易需要审批，系统会返回`status: "pending_approval"`。钱包所有者会收到Telegram通知以决定是否批准。

---

## 原始签名器（高级功能）

用于在智能账户无法使用时生成原始ECDSA/Ed25519签名。

### 创建原始签名器

```bash
curl -X POST "https://heyvincent.ai/api/secrets" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "RAW_SIGNER",
    "memo": "My raw signer"
  }'
```

响应中包含从同一种子生成的Ethereum（secp256k1）和Solana（ed25519）地址。

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

- `message`：需要签名的十六进制编码字节（必须以`0x`开头）
- `curve`：`"ethereum"`表示secp256k1 ECDSA，`"solana"`表示ed25519

返回一个十六进制编码的签名。对于Ethereum，签名格式为`r || s || v`（65字节）；对于Solana，签名格式为64字节的ed25519签名。