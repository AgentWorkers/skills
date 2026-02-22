---
name: Vincent - Polymarket for agents
description: 使用此技能为您的代理创建一个 Polymarket 钱包，并在预测市场中进行交易。您可以浏览市场、下注、管理持仓——所有这些操作都无需暴露私钥。
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

使用此工具为代理创建一个 Polymarket 钱包，并在预测市场中进行交易。您可以浏览市场、下注、跟踪持仓情况以及管理订单——所有这些操作都不会将私钥暴露给代理。该钱包基于 Polygon 上的 Gnosis Safe 技术，并通过 Polymarket 的中继器实现无 gas 交易。

**代理永远不会看到私钥**。所有操作都在服务器端执行。代理会收到一个受限的 API 密钥，该密钥仅能执行钱包所有者允许的操作。私钥始终保存在 Vincent 服务器上。

所有命令都使用 `@vincentai/cli` 包。API 密钥会自动存储和解析——您无需处理原始密钥或文件路径。

## 安全模型

此工具专为**在服务器端控制下由代理自主进行交易**而设计。理解以下安全模型非常重要：

- **无需环境变量**：因为此工具采用“代理优先”的注册方式：代理在运行时通过调用 Vincent API 自动创建其 Polymarket 钱包，API 会返回一个受限的 API 密钥。无需预先配置任何凭证。CLI 会在钱包创建过程中自动存储返回的 API 密钥。密钥的存储路径（`${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/credentials/agentwallet/` 或 `./agentwallet/`）在工具的元数据中进行了声明。

- **代理的 API 密钥并非私钥**：它是一个受限的承载令牌，仅能执行钱包所有者设定的策略允许的操作。Vincent 服务器会在服务器端强制执行所有策略——无论代理发送什么请求，都无法绕过这些策略。如果交易违反策略，服务器会拒绝该请求。如果交易需要批准，服务器会暂停交易并通过 Telegram 通知钱包所有者进行人工审批。

- **有意启用模型调用**：此工具的目的是让 AI 代理具备自主的 Polymarket 交易能力。代理应在人类操作员的定义范围内自行执行交易操作（如浏览市场、下注、管理持仓）。人类操作员通过策略（如消费限额、审批阈值）来控制代理的行为，而不是通过限制单个调用来实现控制。存储的密钥具有范围限制和策略约束——即使其他进程读取了密钥，也只能执行钱包所有者允许的操作，且所有者可以立即撤销该密钥。

- **所有 API 调用都通过 HTTPS/TLS 发送到 `heyvincent.ai`**。不会连接其他端点、服务或外部主机。代理不会读取、收集或传输超出 Polymarket 钱包操作所需的数据。

## 密钥生命周期：

- **创建**：代理运行 `secret create` 命令——CLI 会自动存储 API 密钥，并返回 `keyId` 和 `claimUrl`。
- **认领**：人类操作员使用 `claimUrl` 在 `https://heyvincent.ai` 上认领钱包所有权并配置策略。
- **撤销**：钱包所有者可以随时通过 Vincent 前端撤销代理的 API 密钥。被撤销的密钥会被服务器立即拒绝。
- **重新链接**：如果代理丢失了 API 密钥，钱包所有者可以生成一个一次性重新链接令牌，代理通过 `secret relink` 命令用它来获取新的密钥。
- **轮换**：钱包所有者可以随时撤销当前密钥并生成新的重新链接令牌以更换凭证。

## 快速入门

### 1. 检查是否存在现有密钥

在创建新钱包之前，先检查是否已有密钥：

```bash
npx @vincentai/cli@latest secret list --type POLYMARKET_WALLET
```

如果返回了密钥，请将其 `id` 作为后续命令的 `--key-id` 参数。如果没有密钥，则创建新钱包。

### 2. 创建 Polymarket 钱包

```bash
npx @vincentai/cli@latest secret create --type POLYMARKET_WALLET --memo "My prediction market wallet"
```

返回 `keyId`（用于后续所有命令）、`claimUrl`（与用户共享）和 `walletAddress`（EOA 地址；Safe 会在首次使用时懒加载部署）。

创建完成后，告知用户：

> “这是您的钱包认领链接：`<claimUrl>`。使用此链接来认领所有权、设置消费策略，并在 `https://heyvincent.ai` 上监控代理的钱包活动。”

**重要提示：** 创建完成后，钱包中没有任何资金。用户必须向 Safe 地址发送 **USDC.e（桥接的 USDC）** 才能进行下注。

### 3. 查看余额

```bash
npx @vincentai/cli@latest polymarket balance --key-id <KEY_ID>
```

返回：
- `walletAddress` — Safe 地址（首次调用时若需要会进行部署）
- `collateral.balance` — 可用于交易的 USDC.e 余额
- `collateral.allowance` — Polymarket 合同的允许交易金额

**注意：** 第一次查询余额时，系统会触发 Safe 的部署和抵押品审批（通过中继器实现无 gas 交易）。这可能需要 30-60 秒。

### 4. 为钱包充值

在下注之前，用户必须向 Safe 地址发送 USDC.e：

1. 从余额查询命令中获取钱包地址。
2. 向该地址发送 USDC.e（桥接的 USDC，合约地址为 `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`）。
3. 每次下注至少需要 1 美元（Polymarket 的最低要求）。

**请勿发送原生 USDC**（`0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359`）。Polymarket 仅接受桥接的 USDC.e）。

### 5. 从 Vincent EVM 钱包转账（备用充值方式）

如果您拥有 Vincent EVM 钱包且其中有钱，可以使用 `wallet transfer-between` 命令直接将资金转移到 Polymarket 钱包（请参阅钱包相关技能）。Vincent 会验证您是否拥有这两个钱包的私钥，并自动处理代币转换和跨链桥接，以便在 Polygon 上获取 USDC.e。

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
- 对于 Polymarket 目标地址，仅允许使用 `--to-chain 137`（Polygon）和 `--token-out 0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`（USDC.e）。
- 服务器会验证您是否拥有这两个钱包的私钥——向其他用户转账的请求会被拒绝。
- 对于跨链转账，请使用 `wallet transfer-between status --key-id <EVM_KEY_ID> --relay-id <RELAY_REQUEST_ID>` 命令查询状态。

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

市场响应包含以下信息：
- `question`：市场问题
- `outcomes`：结果数组（如 `["Yes", "No"]` 或 `["Team A", "Team B"]`
- `outcomePrices`：每个结果对应的当前价格
- `tokenIds`：每个结果对应的代币 ID（用于下注）
- `acceptingOrders`：市场是否开放交易
- `closed`：市场是否已结算

**重要提示：** 始终使用市场响应中的 `tokenIds` 数组。每个结果对应的代币 ID 在数组中的位置是固定的。对于“是/否”类型的市场：
  - `tokenIds[0]` 对应“是”结果
  - `tokenIds[1]` 对应“否”结果

### 7. 查看订单簿

```bash
npx @vincentai/cli@latest polymarket orderbook --key-id <KEY_ID> --token-id <TOKEN_ID>
```

返回买卖订单的价格和数量。这有助于在下注前了解当前市场价格。

### 8. 下注

```bash
npx @vincentai/cli@latest polymarket bet --key-id <KEY_ID> --token-id <TOKEN_ID> --side BUY --amount 5 --price 0.55
```

参数：
- `--token-id`：结果对应的代币 ID（来自市场数据或订单簿）
- `--side`：`BUY` 或 `SELL`
- `--amount`：BUY 订单的金额（以 USD 计）；SELL 订单表示要出售的股份数量。
- `--price`：可选的限价（0.01 到 0.99）。如果没有指定限价，则使用市场价。除非用户明确要求，否则必须使用市场价。

**BUY 订单：**
- `amount` 表示您愿意支付的金额（例如，5 表示 5 美元）。
- 您将获得 `amount / price` 数量的股份（例如，5 美元对应 10 股）。
- 最小订单金额为 1 美元。

**SELL 订单：**
- `amount` 表示要出售的股份数量。
- 您将收到 `amount * price` 的金额（以 USD 计）。
- 必须先持有相应的股份（通过之前的 BUY 操作获得）。

**重要提示：** 在完成 BUY 订单后，请等待几秒钟再出售股份。股份需要在链上完成结算。

如果交易违反策略，服务器会返回错误信息，说明违反了哪项策略。如果交易需要审批（基于审批阈值策略），服务器会返回 `status: "pending_approval"`，并通知钱包所有者进行人工审批。

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

**Holdings** 返回所有持仓情况，包括持有的股份、平均买入价、当前价格和未实现的盈亏。此端点可用于：
- 在下卖单前查看当前持仓
- 设置止损或止盈规则
- 计算投资组合的总价值和表现
- 向用户显示其活跃的投注记录

**Open Orders** 返回未成交的限价订单。

**Trades** 返回历史交易记录。

### 10. 取消订单

```bash
# Cancel specific order
npx @vincentai/cli@latest polymarket cancel-order --key-id <KEY_ID> --order-id <ORDER_ID>

# Cancel all open orders
npx @vincentai/cli@latest polymarket cancel-all --key-id <KEY_ID>
```

### 11. 回收已结算的持仓

市场结算后，您可以回收获胜的持仓，将条件性代币转换回 USDC.e。使用 `holdings` 命令查看哪些持仓具有 `redeemable: true` 属性，然后调用 `redeem` 命令进行回收。

```bash
# Redeem all redeemable positions
npx @vincentai/cli@latest polymarket redeem --key-id <KEY_ID>

# Redeem specific markets by condition ID
npx @vincentai/cli@latest polymarket redeem --key-id <KEY_ID> --condition-ids 0xabc123,0xdef456
```

如果没有可回收的持仓，`redeemed` 数组将为空，且不会执行任何操作。

**工作原理：** 回收操作是无 gas 的（通过 Polymarket 的中继器和 Safe 来完成）。对于标准市场，系统会调用 CTF 合同上的 `redeemPositions` 方法；对于高风险市场，系统会调用 NegRiskAdapter 上的 `redeemPositions` 方法。这两种情况都会自动处理。

**何时回收：** 定期检查持仓情况。市场结算后，可能需要一段时间才能使持仓可回收。请查看持仓响应中的 `redeemable: true` 属性。

### 12. 提取 USDC**

将 Polymarket Safe 中的 USDC.e 转移到 Polygon 上的任何以太坊地址。此操作也是无 gas 的，通过 Polymarket 的中继器完成。

```bash
npx @vincentai/cli@latest polymarket withdraw --key-id <KEY_ID> --to <RECIPIENT_ADDRESS> --amount <AMOUNT>
```

参数：
- `--to`：接收方以太坊地址（格式为 0x...，共 42 个字符）
- `--amount`：转账金额（以 USDC 表示，例如 “100” 表示 100 USDC）

**响应：**
- `status`：`executed`、`pending_approval` 或 `denied`
- `transactionHash`：Polygon 交易哈希（仅在执行成功时返回）
- `walletAddress`：发送资金的 Safe 地址

如果转账金额超过钱包的 USDC 余额，服务器会返回 `INSUFFICIENT_BALANCE` 错误。提款操作同样受到消费限额和审批阈值的限制。

## 策略（服务器端执行）

钱包所有者可以通过 `https://heyvincent.ai` 上的认领链接设置策略，从而控制代理的行为。所有策略都由 Vincent API 在服务器端强制执行——代理无法绕过或修改这些策略。如果交易违反策略，API 会拒绝该交易。如果交易触发审批阈值，API 会暂停交易并通过 Telegram 通知钱包所有者进行人工审批。

| 策略                          | 功能                                      |
| --------------------------- | ------------------------------------------------------ |
| **消费限额（每次交易）**            | 每次交易的最大 USD 金额                                      |
| **消费限额（每日）**                | 每 24 小时的最大 USD 金额                                      |
| **消费限额（每周）**                | 每 7 天的最大 USD 金额                                      |
| **需要审批**                    | 每笔交易都需要通过 Telegram 进行人工审批                         |
| **审批阈值**                    | 金额超过指定阈值的交易需要人工审批                         |

在钱包被认领之前，代理可以无限制地操作。这是设计初衷：代理优先的注册方式允许代理立即开始交易。一旦人类操作员通过认领链接认领了钱包，他们可以添加任何策略来限制代理的行为。钱包所有者也可以随时完全撤销代理的 API 密钥。

## 重新链接（恢复 API 访问权限）

如果代理丢失了 API 密钥，钱包所有者可以通过前端生成一个 **重新链接令牌**。代理可以使用该令牌获取新的受限 API 密钥。

**操作步骤：**
1. 用户在 `https://heyvincent.ai` 的钱包详情页面生成重新链接令牌。
2. 用户将令牌提供给代理（例如通过聊天发送）。
3. 代理运行 `relink` 命令：

```bash
npx @vincentai/cli@latest secret relink --token <TOKEN_FROM_USER>
```

CLI 会使用该令牌获取新的 API 密钥，并自动存储它，同时返回新的 `keyId`。后续命令均使用这个 `keyId`。

**重要提示：** 重新链接令牌是一次性使用的，10 分钟后失效。因此用户可以通过聊天安全地发送令牌给您，因为您会立即使用它。

## 工作流程示例

1. **创建钱包：**
   ```bash
   npx @vincentai/cli@latest secret create --type POLYMARKET_WALLET --memo "Betting wallet"
   ```

2. **获取 Safe 地址（触发部署）：**
   ```bash
   npx @vincentai/cli@latest polymarket balance --key-id <KEY_ID>
   # Returns walletAddress — give this to user to fund
   ```

3. **用户向 Polygon 上的 Safe 地址发送 USDC.e：**
   ```bash
   npx @vincentai/cli@latest polymarket balance --key-id <KEY_ID>
   # Returns walletAddress — give this to user to fund
   ```

4. **搜索市场：**
   ```bash
   # Search by keyword — returns only active, tradeable markets
   # Tip: use short keyword phrases; stop-words like "or" can cause empty results
   npx @vincentai/cli@latest polymarket markets --key-id <KEY_ID> --query "bitcoin up down" --active
   ```

5. **查看所需结果的订单簿：**
   ```bash
   npx @vincentai/cli@latest polymarket orderbook --key-id <KEY_ID> --token-id 123456...
   ```

6. **使用正确的代币 ID 下注：**
   ```bash
   # tokenId must be from the tokenIds array, NOT the conditionId
   npx @vincentai/cli@latest polymarket bet --key-id <KEY_ID> --token-id 123456... --side BUY --amount 5 --price 0.55
   ```

7. **等待结算（几秒钟）：**
   ```bash
   npx @vincentai/cli@latest polymarket bet --key-id <KEY_ID> --token-id 123456... --side SELL --amount 9.09 --price 0.54
   ```

8. **出售持仓：**
   ```bash
   npx @vincentai/cli@latest polymarket bet --key-id <KEY_ID> --token-id 123456... --side SELL --amount 9.09 --price 0.54
   ```

9. **市场结算后回收持仓：**
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

- **任何下注或交易完成后**，请分享用户的 Polymarket 个人资料链接（以便他们可以验证和查看持仓情况：`https://polymarket.com/profile/<polymarketWalletAddress>`（使用钱包的 Safe 地址）。
- **所有交易均为无 gas 的**：所有 Polymarket 交易都通过 Polymarket 的中继器实现无 gas 交易。
- **切勿尝试访问原始的私钥信息**。私钥始终保存在服务器端——这是安全要求。
- 创建钱包后，请务必与用户共享认领链接。
- 如果交易被拒绝，可能是由于服务器端的策略限制。请告知用户在 `https://heyvincent.ai` 查看他们的策略设置。
- 如果交易需要审批，系统会返回 `status: "pending_approval"`。钱包所有者将收到 Telegram 通知以进行审批。

**常见错误：**
- “No orderbook exists for the requested token id”：市场可能已关闭，或者您使用了错误的 ID。请确保：
  - 市场处于开放状态（`acceptingOrders: true`）
  - 您使用的是 `tokenIds` 数组中的代币 ID，而不是 `conditionId`
  - 市场尚未结算