---
name: Vincent - A wallet for agents
description: 使用此技能可以安全地创建一个钱包，该钱包可供代理用于转账、交换以及任何基于以太坊虚拟机（EVM）的链上交易。此外，该钱包还支持原始签名（raw signing）和Polymarket赌博（Polymarket betting）功能。
---

# Vincent – 为代理设计的钱包

使用此功能，您可以安全地为代理创建一个钱包，用于转账、交易以及任何基于EVM区块链的操作，而无需向代理暴露私钥。创建钱包后，您可以设置支出策略，代理便可以在您设定的范围内进行代币转账、交易和智能合约交互。

**代理永远看不到私钥。**所有交易都在服务器端通过智能账户执行。钱包所有者可以通过可配置的策略来控制代理的权限。

## 选择哪种钱包类型

| 类型                | 使用场景                                      | 区块链                | 执行费用（Gas）         |
| ------------------- | ----------------------------------------- | ----------------------- | ---------------- |
| `EVM_WALLET`        | 转账、交易、去中心化金融（DeFi）操作、调用智能合约           | 任意EVM区块链           | 免费（由OpenClaw赞助） |
| `RAW_SIGNER`        | 为特定协议生成原始签名                         | 以太坊（Ethereum）和Solana区块链 | 需用户自行支付      |
| `POLYMARKET_WALLET` | 在Polymarket预测市场中进行交易                   | 仅限Polygon区块链       | 免费（由OpenClaw赞助） |

**建议选择 `EVM_WALLET`（默认设置）**，适用于：**
- 转账ETH或代币
- 在去中心化交易所（DEX）中交易代币
- 与智能合约交互
- 执行任何标准的EVM区块链交易

**仅在以下情况下选择 `RAW_SIGNER`：**
- 需要为不支持智能账户的协议生成ECDSA/Ed25519签名
- 需要为自己要广播的交易哈希签名
- 需要在Solana区块链上进行签名

**仅在以下情况下选择 `POLYMARKET_WALLET`：**
- 在Polymarket预测市场中下注
- 需要在Polygon区块链上使用USDC.e作为交易资金

## 配置

所有API请求都需要一个Bearer令牌（创建钱包时返回的API密钥）。如果您是OpenClaw实例，请将其存储在`~/.openclaw/credentials/agentwallet/<API_KEY_ID>.json`文件中；否则，请将其存储在当前工作目录下的`agentwallet/<API_KEY_ID>.json`文件中。

```
Authorization: Bearer <API_KEY>
```

## 快速入门

### 1. 创建钱包

为您的代理创建一个新的智能账户钱包。该操作会在服务器端生成私钥（您永远看不到私钥），同时创建一个ZeroDev智能账户，并返回一个API密钥以及钱包所有者的声明URL。

**响应内容包括：**
- `apiKey`：请妥善保管此密钥，用作所有后续请求的Bearer令牌。
- `claimUrl`：请将此链接分享给用户，以便他们可以声明钱包所有权并设置策略。
- `address`：智能账户的地址。

创建完成后，告诉用户：
> “这是您的钱包声明URL：`<claimUrl>`。请使用此链接来声明所有权、设置支出策略，并监控代理的钱包活动。”

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

该操作会返回所有ERC-20代币的余额，包括代币的符号、小数位数、图标以及对应的USD价值。

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

### 5. 交易代币

使用DEX的流动性（由0x平台提供支持）来交易代币。

**参数说明：**
- `sellToken` / `buyToken`：代币合约的地址。使用`0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`表示ETH。
- `sellAmount`：要出售的代币数量（例如，`"0.1"`表示0.1 ETH）。
- `chainId`：进行交易的区块链（1 = 以太坊，137 = Polygon，42161 = Arbitrum，10 = Optimism，8453 = Base等）。
- `slippageBps`：可选的滑点容忍度（以基点为单位，100表示1%）。默认值为100。

预览端点会返回预期的购买金额、路由信息及费用，但不会实际执行交易。执行端点会通过智能账户完成交易，并自动处理ERC20合约的批准流程。

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

## 策略设置

钱包所有者可以通过声明URL来设置代理的权限。如果交易违反策略设置，API会拒绝该交易或要求用户通过Telegram进行人工批准。

| 策略                        | 功能说明                                      |
| --------------------------- | ------------------------------------------------------------------- |
| **Address allowlist**       | 仅允许向指定地址进行转账/调用                         |
| **Token allowlist**         | 仅允许转移特定的ERC-20代币                         |
| **Function allowlist**      | 仅允许调用特定的智能合约函数                         |
| **Spending limit (per tx)** | 每次交易的最高USD金额限制                         |
| **Spending limit (daily)**  | 每24小时内的最高USD金额限制                         |
| **Spending limit (weekly)** | 每7天内的最高USD金额限制                         |
| **Require approval**        | 所有交易都需要通过Telegram进行人工批准                         |
| **Approval threshold**      | 金额超过指定阈值的交易需要人工批准                         |

如果没有设置任何策略，代理将可以执行所有操作。所有者声明钱包并设置策略后，代理将严格遵循这些规则。

## 重新链接（恢复API访问权限）

如果代理丢失了API密钥，钱包所有者可以通过前端生成一个**重新链接令牌**。代理可以使用此令牌获取新的API密钥。

**操作步骤：**
1. 用户从前端的钱包详情页面生成重新链接令牌。
2. 用户将令牌提供给代理（例如，通过聊天发送）。
3. 代理调用重新链接端点，将令牌兑换成新的API密钥。

**响应内容包括：**
- `secret`：钱包的元数据（ID、类型、地址、chainId等）。
- `apiKey.key`：新的API密钥，用作所有后续请求的Bearer令牌。

**重要提示：**
- **无需支付执行费用。**所有交易费用均由OpenClaw自动承担。
- **切勿尝试访问私钥的原始值。**私钥始终存储在服务器端。
- 请务必保存创建钱包时生成的API密钥。如果是OpenClaw实例，请将其存储在`~/.openclaw/credentials/agentwallet/<API_KEY_ID>.json`文件中；否则，请将其存储在当前工作目录下的`agentwallet/<API_KEY_ID>.json`文件中。
- 在使用API之前，请务必在`credentials`文件夹中查找API密钥。
- 创建钱包后，请务必将声明URL分享给用户。
- 如果交易被拒绝，可能是由于策略设置导致的。请让用户通过`https://heyvincent.ai`查看他们的策略设置。
- 如果交易需要批准，系统会返回`status: "pending_approval"`的状态。钱包所有者将通过Telegram收到批准或拒绝的提示。

---

## 原始签名器（高级功能）

适用于智能账户无法使用时所需的原始ECDSA/Ed25519签名操作。

### 创建原始签名器

```bash
curl -X POST "https://heyvincent.ai/api/secrets" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "RAW_SIGNER",
    "memo": "My raw signer"
  }'
```

响应内容包含从同一种子生成的以太坊（secp256k1）和Solana（ed25519）地址。

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
- `curve`：`"ethereum"`表示secp256k1签名算法，`"solana"`表示ed25519签名算法。

返回一个十六进制编码的签名。对于以太坊，签名格式为`r || s || v`（共65字节）；对于Solana，签名格式为64字节。

---

## Polymarket预测市场

Polymarket钱包使用Gnosis Safe钱包，并通过Polymarket的Relayer实现无gas交易。

### 创建Polymarket钱包

```bash
curl -X POST "https://heyvincent.ai/api/secrets" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "POLYMARKET_WALLET",
    "memo": "My prediction market wallet"
  }'
```

响应内容包括：
- `apiKey`：用作所有Polymarket请求的Bearer令牌。
- `claimUrl`：请与用户分享此链接，以便他们可以声明钱包所有权并设置策略。
- `walletAddress`：Safe钱包的地址（首次使用时会自动部署）。

**重要提示：**创建钱包后，钱包内没有资金。用户需要在Polygon区块链上向Safe钱包地址发送**USDC.e**才能进行交易。

### 获取余额

```bash
curl -X GET "https://heyvincent.ai/api/skills/polymarket/balance" \
  -H "Authorization: Bearer <API_KEY>"
```

返回：
- `walletAddress`：Safe钱包的地址（首次调用时会自动部署）。
- `collateral.balance`：可用于交易的USDC.e余额。
- `collateral.allowance`：Polymarket合约允许使用的最大金额。

**注意：**首次调用`getBalance`接口会触发Safe钱包的部署和资金审批（无需支付gas）。这可能需要30-60秒。

### 为钱包充值

在下单之前，请用户向Safe钱包地址发送USDC.e：
1. 通过`/balance`接口获取钱包地址。
2. 向该地址发送USDC.e（使用合约`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`）。
- 每次下注至少需要1美元。

**注意：**请不要发送原始的USDC（`0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359`）。Polymarket仅接受桥接后的USDC.e。

### 浏览和搜索市场

**市场响应包含：**
- `question`：市场问题。
- `outcomes`：结果数组（例如`["Yes", "No"]`或`["Team A", "Team B"]`）。
- `outcomePrices`：每个结果对应的当前价格。
- `tokenIds`：每个结果对应的代币ID（用于下注）。
- `acceptingOrders`：市场是否开放交易。
- `closed`：市场是否已经结束。

**重要提示：**请始终使用市场响应中的`tokenIds`数组。对于“是/否”类型的市场：
- `tokenIds[0]`对应“是”结果的代币ID。
- `tokenIds[1]`对应“否”结果的代币ID。

### 获取订单簿

```bash
curl -X GET "https://heyvincent.ai/api/skills/polymarket/orderbook/<TOKEN_ID>" \
  -H "Authorization: Bearer <API_KEY>"
```

返回订单的买卖价格和数量。请根据这些信息确定当前的市场价格。

### 下注

**参数说明：**
- `tokenId`：结果对应的代币ID（来自市场数据或订单簿）。
- `side`：`BUY`或`SELL`。
- `amount`：BUY订单的金额（以USD计）；SELL订单表示要出售的股份数量。
- `price`：限价（0.01至0.99）。可选——对于市价订单可省略。

**BUY订单：**
- `amount`表示您希望购买的金额（例如，`5`表示5美元）。
- 您将获得`amount / price`数量的代币（例如，5美元对应10股）。
- 最小订单金额为1美元。

**SELL订单：**
- `amount`表示要出售的股份数量。
- 您将获得`amount * price`对应的USD金额。
- 需要先持有相应的代币（通过之前的BUY操作获得）。

**重要提示：**在完成BUY订单后，请等待几秒钟再出售股份，因为交易需要时间在链上完成确认。

### 查看持仓和订单

```bash
# Get open orders
curl -X GET "https://heyvincent.ai/api/skills/polymarket/positions" \
  -H "Authorization: Bearer <API_KEY>"

# Get trade history
curl -X GET "https://heyvincent.ai/api/skills/polymarket/trades" \
  -H "Authorization: Bearer <API_KEY>"
```

### 取消订单

```bash
# Cancel specific order
curl -X DELETE "https://heyvincent.ai/api/skills/polymarket/orders/<ORDER_ID>" \
  -H "Authorization: Bearer <API_KEY>"

# Cancel all open orders
curl -X DELETE "https://heyvincent.ai/api/skills/polymarket/orders" \
  -H "Authorization: Bearer <API_KEY>"
```

### Polymarket操作流程示例：

1. **创建钱包：**  
   ```bash
   POST /api/secrets {"type": "POLYMARKET_WALLET", "memo": "Betting wallet"}
   ```

2. **获取Safe钱包地址：**  
   ```bash
   GET /api/skills/polymarket/balance
   # Returns walletAddress -- give this to user to fund
   ```

3. **用户向Polygon上的Safe钱包地址发送USDC.e：**  
4. **搜索市场：**  
   ```bash
   # Search by keyword - returns only active, tradeable markets
   GET /api/skills/polymarket/markets?query=bitcoin&active=true
   ```

5. **查看所需结果的订单簿：**  
   ```bash
   # Use the tokenId from the market response
   GET /api/skills/polymarket/orderbook/123456...
   # Note the bid/ask prices
   ```

6. **使用正确的代币ID下注：**  
   ```bash
   # tokenId must be from the tokenIds array, NOT the conditionId
   POST /api/skills/polymarket/bet
   {"tokenId": "123456...", "side": "BUY", "amount": 5, "price": 0.55}
   ```

7. **等待交易确认：**  
   ```bash
   POST /api/skills/polymarket/bet
   {"tokenId": "123456...", "side": "SELL", "amount": 9.09, "price": 0.54}
   ```

**常见错误：**
- “No orderbook exists for the requested token id”：市场可能已关闭，或者您使用的代币ID错误。请确认：
  - 市场状态为`acceptingOrders: true`。
  - 使用的是`tokenIds`数组中的代币ID，而不是`conditionId`。
  - 市场尚未结束交易。