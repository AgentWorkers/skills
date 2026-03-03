---
name: Vincent - Polymarket for agents
description: >
  **Polymarket 预测市场交易功能**  
  该功能专为代理（agents）设计，适用于用户需要创建 Polymarket 钱包、浏览市场、下注、管理持仓或提取资金的情况。  
  相关触发词包括：`polymarket`、`prediction market`、`place bet`、`browse markets`、`trade prediction`、`polymarket wallet`、`betting`、`market odds`。
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
# Vincent – 为代理设计的 Polymarket 工具

使用此工具为您的代理创建一个 Polymarket 钱包，并在预测市场中进行交易。您可以浏览市场、下注、跟踪持仓情况以及管理订单——所有这些操作都不会将私钥暴露给代理。该钱包使用 Polygon 上的 Gnosis Safe，并通过 Polymarket 的中继器实现无 gas 的交易。

**代理永远不会看到私钥。**所有操作都在服务器端执行。代理会收到一个受限的 API 密钥，该密钥仅能执行钱包所有者允许的操作。私钥永远不会离开 Vincent 服务器。

所有命令都使用 `@vincentai/cli` 包。API 密钥会自动存储和解析——您无需处理原始密钥或文件路径。

## 安全模型

此工具旨在实现**在服务器端控制下的自主代理交易**，同时允许人类进行监督。理解这一安全模型非常重要：

- **无需环境变量**，因为此工具采用“代理优先”的接入方式：代理在运行时通过调用 Vincent API 来创建自己的 Polymarket 钱包，该 API 会返回一个受限的 API 密钥。无需预先配置任何凭证。CLI 会在钱包创建过程中自动存储返回的 API 密钥。密钥的存储路径（`${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/credentials/agentwallet/` 或 `./agentwallet/`）在工具的元数据中进行了声明。

- **代理的 API 密钥并非私钥**。它是一个受限的持有者令牌，只能执行钱包所有者设定的策略允许的操作。Vincent 服务器会在服务器端强制执行所有策略——无论代理发送什么请求，都无法绕过这些策略。如果交易违反策略，服务器会拒绝该请求。如果交易需要批准，服务器会暂停交易并通过 Telegram 通知钱包所有者进行人工审批。

- **有意启用模型调用**。此工具的目的是让 AI 代理具备自主的 Polymarket 交易能力。代理应在人类操作员定义的范围内自行执行交易操作（如浏览市场、下注、管理持仓）。人类通过策略来控制代理的行为（例如设置支出限制、审批阈值），而不是通过限制单个请求来实现控制。存储的密钥具有范围限制和策略约束——即使其他进程读取了密钥，也只能执行钱包所有者允许的操作，且所有者可以立即撤销该密钥。

- **所有 API 调用都通过 HTTPS/TLS 发送到 `heyvincent.ai`。**不会接触其他端点、服务或外部主机。代理不会读取、收集或传输超出 Polymarket 钱包操作所需的数据。

## 密钥生命周期：

- **创建**：代理运行 `secret create` 命令——CLI 会自动存储 API 密钥，并返回 `keyId` 和 `claimUrl`。
- **认领**：人类操作员使用 `claimUrl` 在 `https://heyvincent.ai` 上认领钱包所有权并配置策略。
- **撤销**：钱包所有者可以随时通过 Vincent 前端撤销代理的 API 密钥。被撤销的密钥会立即被服务器拒绝。
- **重新链接**：如果代理丢失了 API 密钥，钱包所有者可以生成一个一次性重新链接令牌，代理可以通过 `secret relink` 命令用它来获取新的密钥。
- **轮换**：钱包所有者可以随时撤销当前密钥并生成一个新的重新链接令牌以更新凭证。

## 快速入门

### 1. 检查是否存在现有密钥

在创建新钱包之前，先检查是否已经存在密钥：

```bash
npx @vincentai/cli@latest secret list --type POLYMARKET_WALLET
```

如果返回了密钥，请将其 `id` 作为后续命令的 `--key-id` 参数。如果不存在密钥，则创建新钱包。

### 2. 创建 Polymarket 钱包

```bash
npx @vincentai/cli@latest secret create --type POLYMARKET_WALLET --memo "My prediction market wallet"
```

返回 `keyId`（用于后续所有命令）、`claimUrl`（与用户共享）和 `walletAddress`（EOA 地址；Safe 会在首次使用时懒加载部署）。

创建完成后，告知用户：

> “这是您的钱包认领 URL：`<claimUrl>`。使用此 URL 来认领所有权、设置支出策略，并在 `https://heyvincent.ai` 上监控代理的钱包活动。”

**重要提示：**创建完成后，钱包中没有任何资金。用户必须向 Safe 地址发送 **USDC.e（桥接后的 USDC）** 才能进行下注。

### 3. 获取余额

```bash
npx @vincentai/cli@latest polymarket balance --key-id <KEY_ID>
```

返回：
- `walletAddress` — Safe 地址（首次调用时需要部署）
- `collateral.balance` — 可用于交易的 USDC.e 余额
- `collateral.allowance` — Polymarket 合同的允许金额

**注意：**首次调用余额接口时会触发 Safe 的部署和抵押品审批（通过中继器实现无 gas 交易）。这可能需要 30-60 秒的时间。

### 4. 为钱包充值

在下注之前，用户必须向 Safe 地址发送 USDC.e：

1. 从余额接口获取钱包地址。
2. 向该地址发送 USDC.e（桥接后的 USDC，合约地址为 `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`）。
3. 每次下注至少需要 1 美元（Polymarket 的最低要求）。

**请不要发送原始的 USDC**（`0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359`）。Polymarket 仅接受桥接后的 USDC.e）。

### 5. 从 Vincent EVM 钱包转账（备用充值方式）

如果您有 Vincent EVM 钱包并且里面有资金，可以使用 `wallet transfer-between` 命令直接将资金转移到 Polymarket 钱包（请参阅钱包相关工具）。Vincent 会验证您是否拥有这两个钱包的密钥，并自动处理代币转换和跨链桥接，以便在 Polygon 上获取 USDC.e。

```bash
# Preview the transfer first (use your EVM wallet key-id)
npx @vincentai/cli@latest wallet transfer-between preview --key-id <EVM_KEY_ID> \
  --to-secret-id <POLYMARKET_SECRET_ID> --from-chain 8453 --to-chain 137 \
  --token-in 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 --amount 10 \
  --token-out 0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174 --slippage 100

# Execute the transfer
npx @vincentai/cli@latest wallet transfer-between execute --key-id <EVM_KEY_ID> \
  --to-secret-id <POLYMARKET_SECRET_ID> --from-chain 8453 --to-chain 137 \
  --token-in 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 --amount 10 \
  --token-out 0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174 --slippage 100
```

**关键点：**
- 使用您的 **EVM 钱包的 key-id**（而非 Polymarket 的 key-id）进行这些操作。
- `--to-secret-id` 必须是您的 Polymarket 钱包的 secret ID。
- 对于 Polymarket 目的地，只能使用 `--to-chain 137`（Polygon）和 `--token-out 0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`（USDC.e）。
- 服务器会验证您是否拥有这两个钱包的密钥——尝试向其他用户转账的请求会被拒绝。
- 对于跨链转账，请使用 `wallet transfer-between status --key-id <EVM_KEY_ID> --relay-id <RELAY_REQUEST_ID>` 命令查看状态。

### 6. 浏览和搜索市场

```bash
# Search markets by keyword (recommended)
npx @vincentai/cli@latest polymarket markets --key-id <KEY_ID> --query bitcoin --limit 20

# Search by Polymarket URL or slug
npx @vincentai/cli@latest polymarket markets --key-id <KEY_ID> --slug btc-updown-5m-1771380900

# Or use a full Polymarket URL as the slug parameter
npx @vincentai/cli@latest polymarket markets --key-id <KEY_ID> --slug https://polymarket.com/event/btc-updown-5m-1771380900

# Get all active markets
npx @vincentai/cli@latest polymarket markets --key-id <KEY_ID> --active --limit 50

# Get specific market by condition ID
npx @vincentai/cli@latest polymarket market --key-id <KEY_ID> --condition-id <CONDITION_ID>
```

市场响应包含：
- `question`：市场问题
- `outcomes`：类似 `["Yes", "No"]` 或 `["Team A", "Team B"]` 的数组
- `outcomePrices`：每个结果的当前价格
- `tokenIds`：每个结果的代币 ID 数组——用于下注
- `acceptingOrders`：市场是否开放交易
- `closed`：市场是否已经结算

**重要提示：**始终使用市场响应中的 `tokenIds` 数组。每个结果对应的代币 ID 在数组中的位置是固定的。对于“是/否”类型的市场：
- `tokenIds[0]` 对应“是”结果的代币 ID
- `tokenIds[1]` 对应“否”结果的代币 ID

### 7. 获取订单簿

```bash
npx @vincentai/cli@latest polymarket orderbook --key-id <KEY_ID> --token-id <TOKEN_ID>
```

返回买卖订单的价格和数量。这有助于在下注前了解当前市场价格。

### 8. 下注

```bash
npx @vincentai/cli@latest polymarket bet --key-id <KEY_ID> --token-id <TOKEN_ID> --side BUY --amount 5 --price 0.55
```

参数：
- `--token-id`：结果的代币 ID（来自市场数据或订单簿）
- `--side`：`BUY` 或 `SELL`
- `--amount`：BUY 订单的金额（以 USD 计）。SELL 订单表示要出售的股份数量。
- `--price`：可选的限价（0.01 到 0.99）。如果没有指定限价，则使用市价订单。
- **BUY 订单**：
  - `amount` 表示您希望花费的 USD 金额（例如，`5` 表示 5 美元）。
  - 您将收到 `amount / price` 数量的股份（例如，$5 对应 0.50 的价格，即 10 股）。
- **SELL 订单**：
  - `amount` 表示要出售的股份数量。
  - 您必须先拥有这些股份（通过之前的 BUY 操作获得）。

**重要提示：**在 BUY 订单成交后，请等待几秒钟再出售股份。股份需要在链上完成结算。

如果交易违反策略，服务器会返回错误信息，说明违反了哪条策略。如果交易需要人工审批（基于审批阈值策略），服务器会返回 `status: "pending_approval"`，并通知钱包所有者进行审批或拒绝。

### 9. 查看持仓、未成交订单和交易记录

```bash
# Get current holdings with P&L (recommended for viewing positions)
npx @vincentai/cli@latest polymarket holdings --key-id <KEY_ID>

# Get open orders (unfilled limit orders in the order book)
npx @vincentai/cli@latest polymarket open-orders --key-id <KEY_ID>

# Filter open orders by market
npx @vincentai/cli@latest polymarket open-orders --key-id <KEY_ID> --market <CONDITION_ID>

# Get trade history
npx @vincentai/cli@latest polymarket trades --key-id <KEY_ID>
```

- **Holdings** 返回所有持有的股份、平均买入价格、当前价格和未实现的盈亏。此接口非常适合：
  - 在下卖单前查看当前持仓
  - 设置止损或止盈规则
  - 计算投资组合的总价值和表现
  - 向用户显示他们的活跃投注记录

- **Open Orders** 返回订单簿中未成交的限价订单。

- **Trades** 返回历史交易记录。

### 10. 取消订单

```bash
# Cancel specific order
npx @vincentai/cli@latest polymarket cancel-order --key-id <KEY_ID> --order-id <ORDER_ID>

# Cancel all open orders
npx @vincentai/cli@latest polymarket cancel-all --key-id <KEY_ID>
```

### 11. 回收已结算的持仓

市场结算后，可以回收获胜的持仓，将条件性代币转换回 USDC.e。使用 `holdings` 命令查看哪些持仓的 `redeemable: true`，然后调用 `redeem` 命令进行回收。

```bash
# Redeem all redeemable positions
npx @vincentai/cli@latest polymarket redeem --key-id <KEY_ID>

# Redeem specific markets by condition ID
npx @vincentai/cli@latest polymarket redeem --key-id <KEY_ID> --condition-ids 0xabc123,0xdef456
```

如果没有可回收的持仓，`redeemed` 将是一个空数组，表示没有交易发生。

**工作原理：**回收操作是无 gas 的（通过 Polymarket 的中继器和 Safe 来执行）。对于标准市场，它会调用 CTF 合同上的 `redeemPositions` 方法；对于高风险市场，它会调用 NegRiskAdapter 上的 `redeemPositions` 方法。这两种情况都会自动处理。

**何时回收：**定期检查持仓情况。市场结算后，可能需要一段时间才能使持仓变为可回收状态。请查看持仓响应中的 `redeemable: true` 字段。

### 12. 提取 USDC

将 Polymarket Safe 中的 USDC.e 转移到 Polygon 上的任何以太坊地址。此操作也是无 gas 的——通过 Polymarket 的中继器执行。

```bash
npx @vincentai/cli@latest polymarket withdraw --key-id <KEY_ID> --to <RECIPIENT_ADDRESS> --amount <AMOUNT>
```

参数：
- `--to`：接收方以太坊地址（格式为 0x...，共 42 个字符）
- `--amount`：USDC 金额（以人类可读的形式，例如 “100” 表示 100 USDC）

**响应：**
- `status`：`executed`、`pending_approval` 或 `denied`
- `transactionHash`：Polygon 交易哈希（仅在交易成功时返回）
- `walletAddress`：发送资金的 Safe 地址

如果金额超过钱包的 USDC 余额，服务器会返回 `INSUFFICIENT_BALANCE` 错误。提款时同样会应用策略检查（如支出限制和审批阈值）。

## 输出格式

CLI 命令将结果以 JSON 格式输出到标准输出（stdout）。

### 下注：

### 12. 对于需要人工审批的交易：

### 13. 错误处理

| 错误代码 | 原因 | 解决方案 |
|-------|-------|------------|
| `401 Unauthorized` | API 密钥无效或缺失 | 确认 key-id 是否正确；如有需要，请重新链接 |
| `403 Policy Violation` | 交易被服务器端策略阻止 | 用户需要在 heyvincent.ai 上调整策略 |
| `INSUFFICIENT_BALANCE` | 交易所需的 USDC.e 不足 | 请向钱包充值 USDC.e |
| `429 Rate Limited` | 请求过多 | 等待一段时间后重试 |
| `pending_approval` | 交易超出审批阈值 | 用户会收到 Telegram 通知以进行审批或拒绝 |
| `No orderbook exists` | 市场已关闭或代币 ID 错误 | 确认 `acceptingOrders: true` 并使用 `tokenIds[]`，而不是 `conditionId` |
| `Key not found` | API 密钥已被撤销或从未创建 | 请向钱包所有者请求新的令牌以重新链接 |

## 策略（服务器端执行）

钱包所有者可以通过 `https://heyvincent.ai` 上的认领 URL 设置策略来控制代理的行为。所有策略都由 Vincent API 在服务器端强制执行——代理无法绕过或修改这些策略。如果交易违反策略，API 会拒绝该交易。如果交易触发审批阈值，API 会暂停交易并通过 Telegram 通知钱包所有者进行人工审批。

| 策略                          | 功能                                                         |
| --------------------------- | ---------------------------------------------------------------- |
| **Spending limit (per tx)** | 每笔交易的最大 USD 金额                                      |
| **Spending limit (daily)**  | 每 24 小时的最大 USD 金额                               |
| **Spending limit (weekly)** | 每 7 天的最大 USD 金额                                 |
| **Require approval**        | 每笔交易都需要通过 Telegram 进行人工审批              |
| **Approval threshold**      | 金额超过指定阈值的交易需要人工审批           |

在钱包被认领之前，代理可以无策略限制地操作。这是有意设计的：代理优先的接入方式允许代理立即开始交易。一旦人类操作员通过认领 URL 认领了钱包，他们可以添加任何策略来限制代理的行为。钱包所有者也可以随时完全撤销代理的 API 密钥。

## 重新链接（恢复 API 访问权限）

如果代理丢失了 API 密钥，钱包所有者可以通过前端生成一个 **重新链接令牌**。代理随后可以使用该令牌获取新的受限 API 密钥。

**操作步骤：**
1. 用户在 `https://heyvincent.ai` 的钱包详情页面生成重新链接令牌。
2. 用户将令牌提供给代理（例如通过聊天发送）。
3. 代理运行 `relink` 命令：

```bash
npx @vincentai/cli@latest secret relink --token <TOKEN_FROM_USER>
```

CLI 会用该令牌获取新的 API 密钥，并自动存储它，同时返回新的 `keyId`。请使用这个 `keyId` 进行后续操作。

**重要提示：**重新链接令牌是一次性使用的，10 分钟后失效，因此用户可以通过聊天安全地发送令牌给您。

## 工作流程示例

1. **创建钱包**：
   ```bash
   npx @vincentai/cli@latest secret create --type POLYMARKET_WALLET --memo "Betting wallet"
   ```

2. **获取 Safe 地址（触发部署）：**
   ```bash
   npx @vincentai/cli@latest polymarket balance --key-id <KEY_ID>
   # Returns walletAddress — give this to user to fund
   ```

3. **用户向 Polygon 上的 Safe 地址发送 USDC.e**：

4. **搜索市场：**
   ```bash
   # Search by keyword — returns only active, tradeable markets
   # Tip: use short keyword phrases; stop-words like "or" can cause empty results
   npx @vincentai/cli@latest polymarket markets --key-id <KEY_ID> --query "bitcoin up down" --active
   ```

5. **查看所需的订单簿：**
   ```bash
   npx @vincentai/cli@latest polymarket orderbook --key-id <KEY_ID> --token-id 123456...
   ```

6. **使用正确的代币 ID 下注：**
   ```bash
   # tokenId must be from the tokenIds array, NOT the conditionId
   npx @vincentai/cli@latest polymarket bet --key-id <KEY_ID> --token-id 123456... --side BUY --amount 5 --price 0.55
   ```

7. **等待结算（几秒钟）**：

8. **出售持仓：**
   ```bash
   npx @vincentai/cli@latest polymarket bet --key-id <KEY_ID> --token-id 123456... --side SELL --amount 9.09 --price 0.54
   ```

9. **市场结算后回收持仓（如果持有股份）：**
   ```bash
   # Check holdings for redeemable positions
   npx @vincentai/cli@latest polymarket holdings --key-id <KEY_ID>
   # If redeemable: true, redeem to get USDC.e back
   npx @vincentai/cli@latest polymarket redeem --key-id <KEY_ID>
   ```

10. **将 USDC 提取到其他钱包：**
    ```bash
    npx @vincentai/cli@latest polymarket withdraw --key-id <KEY_ID> --to 0xRecipientAddress --amount 50
    ```

## 重要提示：

- **任何下注或交易后**，请分享用户的 Polymarket 个人资料链接，以便他们可以查看自己的持仓：`https://polymarket.com/profile/<polymarketWalletAddress>`（使用钱包的 Safe 地址）。
- **所有交易都是无 gas 的**。所有 Polymarket 交易都通过 Polymarket 的中继器实现无 gas 交易。
- **切勿尝试访问原始的密钥值**。私钥始终保留在服务器端——这就是设计的目的。
- 创建钱包后，请务必将认领 URL 分享给用户。
- 如果交易被拒绝，可能是由于服务器端策略的限制。请告知用户在 `https://heyvincent.ai` 上检查他们的策略设置。
- 如果交易需要审批，系统会返回 `status: "pending_approval"`。钱包所有者会收到 Telegram 通知以进行审批或拒绝。

有关常见错误及其解决方案的完整列表，请参阅上述的 **错误处理** 部分。