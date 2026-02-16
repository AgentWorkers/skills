---
name: Vincent - Polymarket for agents
description: 使用此技能为您的代理创建一个 Polymarket 钱包，并在预测市场中进行交易。您可以浏览市场、下注、管理持仓——所有这些操作都不需要暴露私钥。
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
# Vincent – 为代理设计的 Polymarket 工具

使用此工具为代理创建一个 Polymarket 钱包，并允许其在预测市场中进行交易。用户可以浏览市场、下注、跟踪持仓以及管理订单——所有这些操作都不会将私钥暴露给代理。该钱包使用 Polygon 上的 Gnosis Safe 技术，并通过 Polymarket 的中继器实现无 gas 支付的交易。

**代理永远不会看到私钥。**所有操作都在服务器端执行。代理会收到一个受限范围的 API 密钥，该密钥仅能执行钱包所有者允许的操作。私钥始终保存在 Vincent 服务器上。

## 安全模型

此工具专为**在服务器端控制下实现自主交易**而设计。理解以下安全模型非常重要：

- **无需环境变量**：因为该工具采用“代理优先”的接入方式：代理在运行时通过调用 Vincent API 来创建自己的 Polymarket 钱包，API 会返回一个受限范围的 API 密钥。无需预先配置任何凭证。代理在创建钱包时会生成并存储自己的 API 密钥——在工具运行之前无需任何秘密信息。
- **代理的 API 密钥并非私钥**：它是一个受限范围的承载令牌（Bearer token），仅能执行钱包所有者设定的策略允许的操作。Vincent 服务器会在服务器端强制执行所有策略——无论代理发送什么请求，都无法绕过这些策略。如果交易违反策略，服务器会拒绝该请求；如果交易需要批准，服务器会暂停交易并通知钱包所有者通过 Telegram 进行人工审批。
- **有意启用模型调用**：该工具的目的是让 AI 代理具备自主的 Polymarket 交易能力。代理应在人类操作员的设定范围内自行执行交易操作（如浏览市场、下注、管理持仓）。人类操作员通过策略（如消费限额、审批阈值）来控制代理的行为，而不是通过限制单个请求来实现控制。代理会将受限范围的 API 密钥保存在指定的配置路径中，以便在不同会话之间恢复交易——这是自主交易代理的预期行为。存储的密钥受到策略限制；即使其他进程读取了该密钥，也只能执行钱包所有者允许的操作，且所有者可以立即撤销该密钥。
- **所有 API 请求仅通过 HTTPS/TLS 发送到 `heyvincent.ai`**：不会连接其他端点、服务或外部主机。代理不会读取、收集或传输超出 Polymarket 钱包操作所需的数据。

## 密钥生命周期

- **创建**：代理调用 `POST /api/secrets` 来创建钱包。API 会返回一个受限范围的 API 密钥和一个声明 URL。
- **声明所有权**：人类操作员使用声明 URL 在 `https://heyvincent.ai` 上声明所有权并配置策略。
- **撤销**：钱包所有者可以随时通过 Vincent 前端撤销代理的 API 密钥。被撤销的密钥会被服务器立即拒绝。
- **重新链接**：如果代理丢失了 API 密钥，钱包所有者可以生成一个一次性使用的重新链接令牌（有效期为 10 分钟），代理用此令牌换取新的 API 密钥。
- **轮换**：钱包所有者可以随时撤销当前密钥并生成新的重新链接令牌以更换凭证。

## 配置

所有 API 请求都需要一个承载令牌（创建钱包时返回的受限范围 API 密钥）。此密钥并非私钥，而是由服务器强制执行的、受策略限制的凭证。钱包创建后，请将其存储在指定的配置路径中。如果是 OpenClaw 实例，请将其存储在 `~/.openclaw/credentials/agentwallet/<API_KEY_ID>.json` 中；否则，请将其存储在当前工作目录下的 `agentwallet/<API_KEY_ID>.json` 中。这些配置路径在工具的元数据中已明确指定。

```
Authorization: Bearer <API_KEY>
```

## 快速入门

### 1. 创建 Polymarket 钱包

为代理创建一个新的 Polymarket 钱包。此操作会在服务器端生成私钥（代理看不到私钥），在 Polygon 上部署 Gnosis Safe，并为代理返回一个受限范围的 API 密钥以及钱包所有者的声明 URL。

**响应内容包括：**
- `apiKey`：受限范围的 API 密钥；请安全存储此密钥，并将其用作所有后续请求的承载令牌。
- `claimUrl`：与用户共享此链接以声明所有权并设置策略。
- `walletAddress`：Safe 的地址（首次使用时才会部署）。

创建完成后，告知用户：
> “这是您的钱包声明 URL：`<claimUrl>`。请使用此链接声明所有权、设置消费策略，并在 `https://heyvincent.ai` 上监控代理的钱包活动。”

**重要提示：**创建完成后，钱包中没有任何资金。用户需要向 Safe 地址发送 **USDC.e（桥接的 USDC）** 才能进行下注。

### 2. 查看余额

返回以下信息：
- `walletAddress`：Safe 的地址（首次调用时如果需要才会部署）。
- `collateral.balance`：可用于交易的 USDC.e 余额。
- `collateral.allowance`：允许用于 Polymarket 合同的金额。

**注意：**首次查询余额时会触发 Safe 的部署和抵押品审批（通过中继器实现无 gas 支付）。这可能需要 30-60 秒。

### 3. 为钱包充值

在下注之前，用户需要向 Safe 地址发送 USDC.e：
1. 从 `/balance` 端点获取钱包地址。
2. 向该地址发送 USDC.e（桥接的 USDC，合约地址为 `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`）。
- 每笔交易至少需要 1 美元。

**请勿发送原生 USDC（`0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359`）。Polymarket 仅接受桥接的 USDC.e。**

### 4. 浏览和搜索市场

市场响应包含以下信息：
- `question`：市场问题。
- `outcomes`：结果数组（例如 `["Yes", "No"]` 或 `["Team A", "Team B"]`）。
- `outcomePrices`：每个结果的价格。
- `tokenIds`：每个结果对应的令牌 ID（用于下注）。
- `acceptingOrders`：市场是否开放交易。
- `closed`：市场是否已经结算。

**重要提示：**始终使用市场响应中的 `tokenIds` 数组。每个结果在数组中的索引位置对应相应的令牌 ID。对于“是/否”类型的市场：
  - `tokenIds[0]` 对应“是”结果的令牌 ID。
  - `tokenIds[1]` 对应“否”结果的令牌 ID。

### 5. 查看订单簿

返回买价和卖价以及相应的数量。这有助于在下注前了解当前市场价格。

### 6. 下注

参数：
- `tokenId`：结果对应的令牌 ID（来自市场数据或订单簿）。
- `side`：`BUY` 或 `SELL`。
- `amount`：买入订单的金额（以 USD 计）；卖出订单的数量。
- `price`：限价（0.01 到 0.99）。可选——市场订单可省略。

**买入订单：**
- `amount` 表示你愿意支付的金额（例如，5 表示 5 美元）。
- 你将收到 `amount / price` 数量的份额（例如，5 美元对应 10 份份额）。
- 最小订单金额为 1 美元。

**卖出订单：**
- `amount` 表示你要出售的份额数量。
- 你将收到 `amount * price` 的金额（以 USD 计）。
- 你必须先拥有这些份额（通过之前的买入操作获得）。

**重要提示：**买入订单成交后，请等待几秒钟再卖出。份额需要在链上完成结算。

如果交易违反策略，服务器会返回错误信息，说明违反了哪条策略。如果交易需要批准（基于审批阈值策略），服务器会返回 `status: "pending_approval"`，并通知钱包所有者进行人工审批。

### 7. 查看持仓和订单

### 8. 取消订单

## 策略（服务器端执行）

钱包所有者可以通过 `https://heyvincent.ai` 上的声明 URL 设置策略来控制代理的行为。所有策略都由 Vincent API 在服务器端强制执行——代理无法绕过或修改这些策略。如果交易违反策略，API 会拒绝该请求；如果交易触发审批阈值，API 会暂停交易并通知钱包所有者通过 Telegram 进行人工审批。

| 策略                          | 功能                                                                                              |
| --------------------------- | ----------------------------------------------------------------------------- |
| **消费限额（每次交易）**            | 每次交易的最大 USD 金额                                                                                   |
| **消费限额（每日）**            | 每 24 小时的最大 USD 金额                                                                                   |
| **消费限额（每周）**            | 每 7 天的最大 USD 金额                                                                                   |
| **需要审批**                | 每笔交易都需要通过 Telegram 进行人工审批                                                                             |
| **审批阈值**                | 金额超过指定阈值的交易需要人工审批                                                                             |

在钱包被声明所有权之前，代理可以无限制地操作。这是设计初衷：代理优先的接入方式允许代理立即开始交易。一旦人类操作员通过声明 URL 声明所有权，他们可以添加任何策略来限制代理的行为。钱包所有者也可以随时完全撤销代理的 API 密钥。

## 重新链接（恢复 API 访问权限）

如果代理丢失了 API 密钥，钱包所有者可以从前端生成一个**重新链接令牌**。代理可以使用此令牌换取新的受限范围 API 密钥。

**操作步骤：**
1. 用户在 `https://heyvincent.ai` 的钱包详情页面生成重新链接令牌。
2. 用户将令牌提供给代理（例如通过聊天发送）。
3. 代理调用重新链接端点，用令牌换取新的受限范围 API 密钥。

**响应内容包括：**
- `secret`：钱包的元数据（ID、类型、地址、chainId 等）。
- `apiKey.key`：新的受限范围 API 密钥，用作所有后续请求的承载令牌。

**重要提示：**重新链接令牌是一次性使用的，有效期为 10 分钟。此端点不需要身份验证——令牌本身即代表授权。

如果用户提供了重新链接令牌，请使用此端点恢复对钱包的访问权限。将返回的 API 密钥存储起来，并用于所有后续请求。

## 工作流程示例

1. **创建钱包：**
   ```bash
   POST /api/secrets {"type": "POLYMARKET_WALLET", "memo": "Betting wallet"}
   ```

2. **获取 Safe 地址（触发部署）：**
   ```bash
   GET /api/skills/polymarket/balance
   # Returns walletAddress -- give this to user to fund
   ```

3. **用户向 Polygon 上的 Safe 地址发送 USDC.e：**
   ```bash
   GET /api/skills/polymarket/balance
   # Returns walletAddress -- give this to user to fund
   ```

4. **搜索市场：**
   ```bash
   # Search by keyword - returns only active, tradeable markets
   GET /api/skills/polymarket/markets?query=bitcoin&active=true
   ```

5. **查看所需的订单簿信息：**
   ```bash
   # Use the tokenId from the market response
   GET /api/skills/polymarket/orderbook/123456...
   # Note the bid/ask prices
   ```

6. **使用正确的令牌 ID 下注：**
   ```bash
   # tokenId must be from the tokenIds array, NOT the conditionId
   POST /api/skills/polymarket/bet
   {"tokenId": "123456...", "side": "BUY", "amount": 5, "price": 0.55}
   ```

7. **等待结算（几秒钟）：**
   ```bash
   POST /api/skills/polymarket/bet
   {"tokenId": "123456...", "side": "SELL", "amount": 9.09, "price": 0.54}
   ```

8. **卖出持仓：**
   ```bash
   POST /api/skills/polymarket/bet
   {"tokenId": "123456...", "side": "SELL", "amount": 9.09, "price": 0.54}
   ```

## 重要提示：
- **任何下注或交易完成后**，请分享用户的 Polymarket 个人资料链接，以便他们可以验证和查看自己的持仓：`https://polymarket.com/profile/<polymarketWalletAddress>`（使用钱包的 Safe 地址）。
- **无需支付 gas。**所有 Polymarket 交易都通过 Polymarket 的中继器实现无 gas 支付。
- **切勿尝试访问原始的秘密信息。**私钥始终保存在服务器端——这是设计初衷。
- 请始终将 API 密钥存储在指定的配置路径中。如果是 OpenClaw 实例，请将其存储在 `~/.openclaw/credentials/agentwallet/<API_KEY_ID>.json` 中；否则，请存储在当前工作目录下的 `agentwallet/<API_KEY_ID>.json` 中。
- 在创建新钱包之前，请始终在指定的配置路径中查找现有的 API 密钥。如果是 OpenClaw 实例，请在 `~/.openclaw/credentials/agentwallet/` 中查找；否则，请在 `./agentwallet/` 中查找。
- 创建钱包后，请务必与用户分享声明 URL。
- 如果交易被拒绝，可能是由于服务器端的策略限制。请告知用户检查他们在 `https://heyvincent.ai` 上的策略设置。
- 如果交易需要审批，系统会返回 `status: "pending_approval"`。钱包所有者将收到 Telegram 通知以进行审批或拒绝。

**常见错误：**
- “请求的令牌 ID 不存在订单簿”：市场可能已关闭，或者你使用了错误的 ID。请确保：
  - 市场处于开放状态（`acceptingOrders: true`）。
  - 你使用的是 `tokenIds` 数组中的令牌 ID，而不是 `conditionId`。
  - 市场尚未结算。