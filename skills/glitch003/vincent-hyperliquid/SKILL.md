---
name: Vincent - HyperLiquid for agents
description: 使用此技能为您的代理创建一个 HyperLiquid 永续合约（perpetuals）和现货交易钱包。您可以进行交易、管理现货余额、在子账户之间转移 USDC、获取价格、下达订单——所有这些操作都不需要暴露私钥。
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
# Vincent – 为代理设计的 HyperLiquid 工具

使用此工具可以为代理创建 HyperLiquid 永续合约和现货钱包。代理可以交易衍生品、查看现货余额，并在衍生品子账户和现货子账户之间转移 USDC。生成的执行权限（EOA）即代表 HyperLiquid 账户——可以直接通过 HL 桥接器进行资金注入，立即开始交易，无需经过安全部署或抵押品审批流程。

**代理永远不会看到私钥。**所有操作都在服务器端执行。代理会收到一个受限范围的 API 密钥，该密钥仅能执行钱包所有者允许的操作。

所有命令均使用 `@vincentai/cli` 包。API 密钥会自动存储和解析。

## 安全模型

**无需环境变量。**代理在运行时通过调用 Vincent API 来创建自己的 HyperLiquid 钱包，该 API 会返回一个受限范围的 API 密钥。无需预先配置任何凭证。

**生成的 EOA 是一个独立的 HyperLiquid 账户。**与 Polymarket 不同（Polymarket 会部署 Gnosis Safe），这里的 EOA 私钥本身就是 HyperLiquid 账户。存款会通过 HyperLiquid 桥接器从 Arbitrum 直接转入该账户，或者通过其他 HL 账户的 `usdSend` 操作转入。

**代理的 API 密钥并非私钥。**它是一个在服务器端强制执行的受限范围的令牌。Vincent 服务器会在执行任何交易前评估所有策略。如果交易违反策略，服务器会拒绝该交易；如果交易需要人工批准，服务器会暂存交易并通知钱包所有者。

**所有 API 调用均通过 HTTPS/TLS 发送到 `heyvincent.ai`。**该服务会代表代理在服务器端调用 `api.hyperliquid.xyz`。

**密钥生命周期：**
- **创建**：代理运行 `secret create` 命令——Vincent 生成 EOA，存储密钥，并返回 `keyId`、`walletAddress` 和 `claimUrl`。
- **认领**：操作员使用 `claimUrl` 在 `https://heyvincent.ai` 进行认领并配置策略。
- **撤销**：钱包所有者可以随时从前端撤销代理的 API 密钥。
- **重新链接**：代理通过 `secret relink` 命令，用所有者生成的一次性重新链接令牌换取新密钥。

## 快速入门

### 1. 检查是否存在现有密钥

在创建新钱包之前，先检查是否已经存在密钥：

```bash
npx @vincentai/cli@latest secret list --type HYPERLIQUID_WALLET
```

如果返回了密钥，请将其 `id` 作为后续命令的 `--key-id` 参数使用。如果没有，则创建一个新的密钥。

### 2. 创建 HyperLiquid 钱包

```bash
npx @vincentai/cli@latest secret create --type HYPERLIQUID_WALLET --memo "My HL perp wallet"
```

返回以下信息：
- `keyId` — 用于后续所有命令
- `walletAddress` — EOA 地址（即 HyperLiquid 账户地址）
- `claimUrl` — 与用户共享以完成认领操作

创建完成后，告知用户：
> “这是您的钱包认领 URL：`<claimUrl>`。请使用此 URL 进行认领、设置消费策略，并在 `https://heyvincent.ai` 监控代理的钱包活动。”

**重要提示：**钱包创建时是空的。用户必须先存款 USDC 才能进行交易。

### 3. 查看余额

```bash
npx @vincentai/cli@latest hyperliquid balance --key-id <KEY_ID>
```

返回以下信息：
- `walletAddress` — EOA 地址
- `accountValue` — 衍生品账户的总价值（以 USD 计算）
- `withdrawable` — 可从衍生品账户中提取的 USDC 数量
- `positions` — 打开的衍生品头寸数组
- `spotBalances` — 现货代币余额数组（每个条目包含 `coin`、`token`、`hold`、`total`）

### 4. 在衍生品子账户和现货子账户之间转移资金

HyperLiquid 有独立的衍生品子账户和现货子账户。交易前必须确保 USDC 存在正确的子账户中。使用 `internal-transfer` 命令在它们之间转移 USDC：

```bash
# Move 100 USDC from spot → perps (needed before perp trading)
npx @vincentai/cli@latest hyperliquid internal-transfer --key-id <KEY_ID> --amount 100 --to-perp true

# Move 50 USDC from perps → spot (needed before spot trading)
npx @vincentai/cli@latest hyperliquid internal-transfer --key-id <KEY_ID> --amount 50 --to-perp false
```

参数：
- `--amount`：要转移的 USDC 数量（字符串或数字）
- `--to-perp`：`true` 表示从现货子账户转移到衍生品子账户；`false` 表示从衍生品子账户转移到现货子账户

**响应代码：**
- `200` — `status: "executed"` — 转移完成
- `202` — `status: "pending_approval"` — 需要人工批准
- `403` — `status: "denied"` — 被策略拒绝

### 5. 向钱包注入资金

可以通过以下方式向 EOA 地址注入资金：
- **通过 Arbitrum 的 HyperLiquid 桥接器**：访问 `https://app.hyperliquid.xyz/portfolio` 并将 USDC 转入 EOA 地址
- **通过其他 HL 账户的 `usdSend` 操作** — 即时完成

进行 BTC 衍生品交易的最小资金要求：**2 美元**（在 20 倍默认杠杆率下，足以覆盖 10 美元的名义价值及手续费）。

### 6. 浏览市场

```bash
npx @vincentai/cli@latest hyperliquid markets --key-id <KEY_ID>
```

返回一个 JSON 对象，将货币名称映射到中间价格（例如 `{"BTC": "105234.5", "ETH": "3412.0", ...}`）。

### 7. 查看订单簿

```bash
npx @vincentai/cli@latest hyperliquid orderbook --key-id <KEY_ID> --coin BTC
```

返回一个包含买卖订单信息的数组 `levels`（每个元素为 `[price, size, numOrders]`）。`levels[1][0][0]` 表示最高卖价，`levels[0][0][0]` 表示最低买价。

### 8. 下单

```bash
# Market buy (IoC — fills immediately or cancels)
npx @vincentai/cli@latest hyperliquid trade --key-id <KEY_ID> \
  --coin BTC --is-buy true --sz 0.0001 \
  --limit-px 106000 --order-type market

# Market sell to close (reduceOnly)
npx @vincentai/cli@latest hyperliquid trade --key-id <KEY_ID> \
  --coin BTC --is-buy false --sz 0.0001 \
  --limit-px 104000 --order-type market --reduce-only

# GTC limit buy
npx @vincentai/cli@latest hyperliquid trade --key-id <KEY_ID> \
  --coin BTC --is-buy true --sz 0.0001 \
  --limit-px 100000 --order-type limit
```

参数：
- `--coin`：资产名称（例如 `BTC`、`ETH`、`SOL`）
- `--is-buy`：`true` 表示买入；`false` 表示卖出/平仓
- `--sz`：交易量（以基础货币计，例如 `0.0001` BTC）
- `--limit-px`：价格。对于市价单，应设置略高于买价（买入）或低于卖价（卖出）以确保成交。建议值：买入时为 `askPx * 1.005`，卖出时为 `bidPx * 0.995`。
- `--order-type`：`market`（即时成交）或 `limit`（限价单）
- `--reduce-only`：在平仓时使用此参数，以防止意外开立相反方向的新订单

**最低交易金额：**10 美元（例如，以 100,000 美元/比特币的价格计算，交易量为 0.0001 比特币）。默认杠杆率为 20 倍跨保证金。

**响应代码：**
- `200` — `status: "executed"`，并返回 `orderId`（数字）和 `fillDetails`
- `202` — `status: "pending_approval"` — 需要人工批准
- `403` — `status: "denied"` — 被策略拒绝

### 9. 查看未成交订单

```bash
# All open orders
npx @vincentai/cli@latest hyperliquid open-orders --key-id <KEY_ID>

# Filter by coin
npx @vincentai/cli@latest hyperliquid open-orders --key-id <KEY_ID> --coin BTC
```

### 10. 查看交易历史

```bash
# All fills
npx @vincentai/cli@latest hyperliquid trades --key-id <KEY_ID>

# Filter by coin
npx @vincentai/cli@latest hyperliquid trades --key-id <KEY_ID> --coin ETH
```

### 11. 取消订单

```bash
# Cancel a specific order (requires coin and numeric order ID)
npx @vincentai/cli@latest hyperliquid cancel-order --key-id <KEY_ID> --coin BTC --oid <ORDER_ID>

# Cancel all open orders
npx @vincentai/cli@latest hyperliquid cancel-all --key-id <KEY_ID>

# Cancel all orders for a specific coin
npx @vincentai/cli@latest hyperliquid cancel-all --key-id <KEY_ID> --coin ETH
```

## 交易引擎：止损、止盈和追踪止损

**交易引擎** 全面支持 HyperLiquid。您可以为任何 HyperLiquid 头寸设置自动止损、止盈和追踪止损规则。规则会在价格条件满足时自动执行——无需使用大型语言模型（LLM）。

对于 HyperLiquid 规则，请使用 `--venue hyperliquid`，并设置 `--market-id` 或 `--token-id` 为货币名称（例如 `BTC`、`ETH`、`SOL`）。`--trigger-price` 是绝对的 USD 价格（与 Polymarket 不同，Polymarket 使用 0–1 的范围）。

### 止损

```bash
npx @vincentai/cli@latest trading-engine create-rule --key-id <KEY_ID> \
  --venue hyperliquid --market-id BTC --token-id BTC \
  --rule-type STOP_LOSS --trigger-price 95000
```

当 BTC 价格跌至 95,000 美元时卖出头寸。

### 止盈

```bash
npx @vincentai/cli@latest trading-engine create-rule --key-id <KEY_ID> \
  --venue hyperliquid --market-id ETH --token-id ETH \
  --rule-type TAKE_PROFIT --trigger-price 4500
```

当 ETH 价格升至 4,500 美元时卖出头寸。

### 追踪止损

```bash
npx @vincentai/cli@latest trading-engine create-rule --key-id <KEY_ID> \
  --venue hyperliquid --market-id SOL --token-id SOL \
  --rule-type TRAILING_STOP --trigger-price 170 --trailing-percent 5
```

当 SOL 价格从其峰值下跌 5% 时卖出头寸。

### 管理规则

```bash
# List all rules
npx @vincentai/cli@latest trading-engine list-rules --key-id <KEY_ID>

# Update trigger price
npx @vincentai/cli@latest trading-engine update-rule --key-id <KEY_ID> --rule-id <RULE_ID> --trigger-price 98000

# Cancel a rule
npx @vincentai/cli@latest trading-engine delete-rule --key-id <KEY_ID> --rule-id <RULE_ID>

# View rule events
npx @vincentai/cli@latest trading-engine events --key-id <KEY_ID>
```

有关完整策略文档（包括基于大型语言模型的策略、信号管道和驱动程序），请参阅 **交易引擎** 部分。

## 策略（服务器端执行）

钱包所有者可以通过在 `https://heyvincent.ai` 设置策略来控制代理的操作权限。所有策略在交易执行前都会在服务器端得到执行。

| 策略                        | 功能                                                         |
| --------------------------- | ---------------------------------------------------------------- |
| **单次交易消费限额** | 每笔交易的最大名义金额（以 USD 计）                                      |
| **每日消费限额**     | 每 24 小时的最大名义金额                                      |
| **每周消费限额**     | 每 7 天的最大名义金额                                      |
| **需要批准**        | 所有交易都需要通过 Telegram 获得人工批准                               |
| **批准阈值**      | 金额超过指定阈值的交易需要人工批准                               |

如果交易被拒绝，API 会返回 `status: "denied` 及原因。如果需要批准，会返回 `status: "pending_approval`，同时钱包所有者会收到 Telegram 通知。

## 重新链接

如果代理丢失了 API 密钥：
1. 用户通过 `https://heyvincent.ai` 生成一个新的重新链接令牌。
2. 用户将令牌提供给代理。
3. 代理运行以下命令：

```bash
npx @vincentai/cli@latest secret relink --token <TOKEN_FROM_USER>
```

重新链接令牌是一次性使用的，10 分钟后失效。

## 工作流程示例

```bash
# 1. Create wallet
npx @vincentai/cli@latest secret create --type HYPERLIQUID_WALLET --memo "HL wallet"
# → returns keyId, walletAddress, claimUrl

# 2. Tell user: "Fund <walletAddress> on HyperLiquid with USDC, then I can trade."

# 3. Check balance after funding (returns both perps and spot balances)
npx @vincentai/cli@latest hyperliquid balance --key-id <KEY_ID>
# → accountValue shows perps balance, spotBalances shows spot holdings

# 4. Transfer USDC between sub-accounts if needed
# Move 100 USDC from spot → perps before perp trading:
npx @vincentai/cli@latest hyperliquid internal-transfer --key-id <KEY_ID> --amount 100 --to-perp true
# Move 50 USDC from perps → spot before spot trading:
npx @vincentai/cli@latest hyperliquid internal-transfer --key-id <KEY_ID> --amount 50 --to-perp false

# 5. Get BTC mid price
npx @vincentai/cli@latest hyperliquid markets --key-id <KEY_ID>

# 6. Get order book to find best ask
npx @vincentai/cli@latest hyperliquid orderbook --key-id <KEY_ID> --coin BTC
# → levels[1][0][0] is best ask, e.g. "105200.0"

# 7. Open long — 0.5% above ask to ensure IoC fill
npx @vincentai/cli@latest hyperliquid trade --key-id <KEY_ID> \
  --coin BTC --is-buy true --sz 0.0001 --limit-px 105726 --order-type market

# 8. Check fills
npx @vincentai/cli@latest hyperliquid trades --key-id <KEY_ID> --coin BTC

# 9. Close long — 0.5% below bid
npx @vincentai/cli@latest hyperliquid orderbook --key-id <KEY_ID> --coin BTC
npx @vincentai/cli@latest hyperliquid trade --key-id <KEY_ID> \
  --coin BTC --is-buy false --sz 0.0001 --limit-px 104674 --order-type market --reduce-only
```

## 输出格式

所有 CLI 命令都会将结果以 JSON 格式输出到标准输出（stdout）。

**balance:**
```json
{
  "walletAddress": "0x...",
  "accountValue": "105.23",
  "withdrawable": "95.00",
  "positions": [
    {
      "position": {
        "coin": "BTC",
        "szi": "0.0001",
        "entryPx": "105200.0",
        "positionValue": "10.52",
        "unrealizedPnl": "0.05",
        "liquidationPx": null,
        "leverage": { "type": "cross", "value": 20 }
      },
      "type": "oneWay"
    }
  ],
  "spotBalances": [
    {
      "coin": "USDC",
      "token": 0,
      "hold": "0.0",
      "total": "50.0"
    }
  ]
}
```

**markets:**
```json
{
  "BTC": "105234.5",
  "ETH": "3412.0",
  "SOL": "185.3"
}
```

**orderbook:**
```json
{
  "coin": "BTC",
  "levels": [
    [["105200.0", "0.5", 3], ["105100.0", "1.2", 5]],
    [["105300.0", "0.3", 2], ["105400.0", "0.8", 4]]
  ]
}
```
`levels[0]` 包含降序排列的买价，`levels[1]` 包含升序排列的卖价。每个条目为 `[price, size, numOrders]`。最高买价为 `levels[0][0][0]`，最高卖价为 `levels[1][0][0]`。

**已执行的交易：**
```json
{
  "orderId": 12345678,
  "status": "executed",
  "transactionLogId": "clx...",
  "walletAddress": "0x...",
  "fillDetails": {
    "totalSz": "0.0001",
    "avgPx": "105250.0"
  }
}
```

**待批准的交易：**
```json
{
  "status": "pending_approval",
  "transactionLogId": "clx...",
  "walletAddress": "0x...",
  "reason": "Exceeds approval threshold"
}
```

**被拒绝的交易：**
```json
{
  "status": "denied",
  "transactionLogId": "clx...",
  "walletAddress": "0x...",
  "reason": "Exceeds daily spending limit"
}
```

**已执行的内部转账：**
```json
{
  "status": "executed",
  "transactionLogId": "clx..."
}
```

**待批准的内部转账：**
```json
{
  "status": "pending_approval",
  "transactionLogId": "clx...",
  "reason": "Exceeds approval threshold"
}
```

**被拒绝的内部转账：**
```json
{
  "status": "denied",
  "transactionLogId": "clx...",
  "reason": "Exceeds daily spending limit"
}
```

**未成交订单：**
```json
{
  "walletAddress": "0x...",
  "openOrders": [
    {
      "coin": "BTC",
      "side": "B",
      "limitPx": "100000.0",
      "sz": "0.0001",
      "oid": 12345678,
      "timestamp": 1700000000000,
      "origSz": "0.0001"
    }
  ]
}
```
`side` 字段表示订单方向：`B` 表示买入/多头，`A` 表示卖出/空头。

**已成交的交易：**
```json
{
  "walletAddress": "0x...",
  "fills": [
    {
      "coin": "BTC",
      "px": "105200.0",
      "sz": "0.0001",
      "side": "B",
      "time": 1700000000000,
      "dir": "Open Long",
      "closedPnl": "0",
      "fee": "0.0105",
      "oid": 12345678
    }
  ]
}
```

**取消订单/全部取消：**
```json
{}
```
成功时返回空对象。任何非零的退出代码表示操作失败。

## 错误处理

| 错误代码 | 原因 | 解决方案 |
|-------|-------|------------|
| `401 Unauthorized` | API 密钥无效或缺失 | 确认密钥 ID 是否正确；如需重新链接，请重新生成令牌 |
| `status: "denied"` | 交易被服务器端策略拒绝 | 用户需在 heyvincent.ai 调整策略 |
| `status: "pending_approval"` | 交易金额超过批准阈值 | 不要重试——等待钱包所有者通过 Telegram 回复批准/拒绝 |
| `400 Bad Request` | 参数无效（例如非数字值或货币名称错误） | 修正参数值 |
| `429 Rate Limited` | 请求过多 | 等待一段时间后重试 |
| `500 TRADE_FAILED` | HyperLiquid 拒绝了交易（例如保证金不足或价格错误） | 检查账户余额和订单参数 |
| `Key not found` | API 密钥已被撤销或从未生成 | 请向钱包所有者请求新的重新链接令牌 |

## 重要说明：
- **无需支付 gas 费用。**HyperLiquid L1 是无 gas 费用的——所有衍生品交易均直接结算。
- **衍生品子账户和现货子账户**：生成的 EOA 同时拥有衍生品子账户（用于跨保证金交易）和现货子账户。使用 `internal-transfer` 命令在它们之间转移 USDC。默认情况下，存款会通过 HL 桥接器进入衍生品子账户。
- **切勿尝试访问原始的秘密值。**私钥始终保存在服务器端。
- 创建钱包后，务必将认领 URL 分享给用户。
- 对于市价单，始终将 `limitPx` 设置在最佳价格的一定范围内（买入时为 `* 1.005`，卖出时为 `* 0.995`），以确保按当前市场价格成交。
- 如果交易返回 `status: "pending_approval"`，请勿重试——等待钱包所有者的回复。