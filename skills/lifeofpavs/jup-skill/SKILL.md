---
name: jupiter-skill
description: 在 Solana 上执行 Jupiter API 操作——获取报价、签署交易、执行交易对换（swap）以及参与预测市场（prediction markets）。适用于实现代币对换（token swaps）、定期投资计划（DCA）、限价单（limit orders）、借贷（lending）等功能，或任何与 Jupiter 相关的集成场景。其中包含用于 Ultra 和 Metis 交易对换流程的脚本。
---
# Jupiter API 技能

通过 4 个实用脚本执行 Jupiter API 操作，用于在 Solana 上获取数据、签署交易和执行交易对换。

**基础 URL**: `https://api.jup.ag`

## 快速参考

| 任务 | 脚本 | 示例 |
|------|--------|---------|
| 获取任何 Jupiter API 数据 | `fetch-api.ts` | `pnpm fetch-api -e /ultra/v1/search -p '{"query":"SOL"}'` |
| 签署交易 | `wallet-sign.ts` | `pnpm wallet-sign -t "BASE64_TX" -w ~/.config/solana/id.json` |
| 执行 Ultra 订单 | `execute-ultra.ts` | `pnpm execute-ultra -r "REQUEST_ID" -t "SIGNED_TX"` |
| 将交易发送到 RPC | `send-transaction.ts` | `pnpm send-transaction -t "SIGNED_TX"` |

## 设置

在使用脚本之前，请安装依赖项：
```bash
cd /path/to/jup-skill
pnpm install
```

## API 密钥设置

**必需。** 所有 Jupiter API 端点都需要 `x-api-key` 标头。

1. 访问 [portal.jup.ag](https://portal.jup.ag)
2. 创建账户并生成 API 密钥
3. 通过环境变量设置（推荐）：
   ```bash
   export JUP_API_KEY=your_api_key_here
   ```
   或者在每个命令中通过 `--api-key` 标志传递。

## 脚本

### fetch-api.ts

从任何 Jupiter API 端点获取数据。

```bash
# Search for tokens
pnpm fetch-api -e /ultra/v1/search -p '{"query":"SOL"}'

# Get Ultra swap order (quote + unsigned transaction)
pnpm fetch-api -e /ultra/v1/order -p '{
  "inputMint": "So11111111111111111111111111111111111111112",
  "outputMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  "amount": "1000000",
  "taker": "YOUR_WALLET_ADDRESS"
}'

# Get Metis quote
pnpm fetch-api -e /swap/v1/quote -p '{
  "inputMint": "So11111111111111111111111111111111111111112",
  "outputMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  "amount": "1000000",
  "slippageBps": "50"
}'

# POST request (for Metis swap transaction)
pnpm fetch-api -e /swap/v1/swap -m POST -b '{
  "quoteResponse": {...},
  "userPublicKey": "YOUR_WALLET"
}'
```

**参数：**
- `-e, --endpoint`（必需）：API 路径，例如 `/ultra/v1/order`
- `-p, --params`：查询参数（GET）或请求体（POST）作为 JSON 字符串
- `-b, --body`：POST 请求的请求体
- `-m, --method`：HTTP 方法，`GET`（默认）或 `POST`
- `-k, --api-key`：API 密钥（或使用 `JUP_API_KEY` 环境变量）

### wallet-sign.ts

使用本地钱包文件签署交易。

> **安全提示**：必须使用 `--wallet` 标志。此脚本不接受命令行参数中的私钥，以防止在 shell 历史记录和进程列表中暴露私钥。

```bash
# Using Solana CLI wallet (JSON array format)
pnpm wallet-sign -t "BASE64_UNSIGNED_TX" --wallet ~/.config/solana/id.json

# Tilde expansion is supported
pnpm wallet-sign -t "BASE64_UNSIGNED_TX" --wallet ~/my-wallets/trading.json
```

**参数：**
- `-t, --unsigned-tx`（必需）：Base64 编码的未签名交易
- `-w, --wallet`（必需）：Solana CLI JSON 钱包文件的路径（支持使用 `~` 表示当前目录）

**输出：** 签署后的交易（base64 格式）输出到标准输出。

### execute-ultra.ts

签署交易后执行 Ultra 订单。

```bash
pnpm execute-ultra -r "REQUEST_ID_FROM_ORDER" -t "BASE64_SIGNED_TX"
```

**参数：**
- `-r, --request-id`（必需）：来自 `/ultra/v1/order` 响应的请求 ID
- `-t, --signed-tx`（必需）：Base64 编码的已签名交易
- `-k, --api-key`：API 密钥（或使用 `JUP_API_KEY` 环境变量）

**输出：** 包含签名和状态的执行结果 JSON。

### send-transaction.ts

将已签名的交易发送到 Solana RPC。**用于 Metis 交易对换**（Ultra 内部处理 RPC）。

> **警告**：默认的公共 Solana RPC（`api.mainnet-beta.solana.com`）有速率限制，不适合生产环境使用。请使用专用的 RPC 提供者（如 Helius、QuickNode、Triton 等）进行生产应用。

```bash
# Default RPC (mainnet-beta)
pnpm send-transaction -t "BASE64_SIGNED_TX"

# Custom RPC
pnpm send-transaction -t "BASE64_SIGNED_TX" -r "https://your-rpc.com"

# With environment variable
export SOLANA_RPC_URL="https://your-rpc.com"
pnpm send-transaction -t "BASE64_SIGNED_TX"
```

**参数：**
- `-t, --signed-tx`（必需）：Base64 编码的已签名交易
- `-r, --rpc-url`：RPC 端点（默认：`https://api.mainnet-beta.solana.com`）
- `--skip-preflight`：跳过预检（更快，但安全性较低）
- `--max-retries`：最大重试次数（默认：3）

**输出：** 交易签名输出到标准输出。

---

## 工作流程

### Ultra 交易对换（推荐）

Ultra 不需要 RPC，无需支付 gas，并具有自动滑点优化。

```
Ultra Swap Progress:
- [ ] Step 1: Get order from /ultra/v1/order
- [ ] Step 2: Sign the transaction
- [ ] Step 3: Execute via /ultra/v1/execute
- [ ] Step 4: Verify result
```

**步骤 1：获取订单**

```bash
ORDER=$(pnpm fetch-api -e /ultra/v1/order -p '{
  "inputMint": "So11111111111111111111111111111111111111112",
  "outputMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  "amount": "1000000",
  "taker": "YOUR_WALLET_ADDRESS"
}')
echo "$ORDER"
```

响应中包含 `requestId` 和未签名的交易（base64 格式）。

**步骤 2：签署交易**

从响应中提取交易并签署：

```bash
UNSIGNED_TX=$(echo "$ORDER" | jq -r '.transaction')
SIGNED_TX=$(pnpm wallet-sign -t "$UNSIGNED_TX" -w ~/.config/solana/id.json)
```

**步骤 3：执行订单**

```bash
REQUEST_ID=$(echo "$ORDER" | jq -r '.requestId')
pnpm execute-ultra -r "$REQUEST_ID" -t "$SIGNED_TX"
```

**步骤 4：验证**

在 [Solscan](https://solscan.io) 上检查签名。

---

### Metis 交易对换（高级）

当需要自定义交易组合或精细控制时，使用 Metis。

```
Metis Swap Progress:
- [ ] Step 1: Get quote from /swap/v1/quote
- [ ] Step 2: Build transaction via /swap/v1/swap
- [ ] Step 3: Sign the transaction
- [ ] Step 4: Send to RPC
- [ ] Step 5: Verify on-chain
```

**步骤 1：获取报价**

```bash
QUOTE=$(pnpm fetch-api -e /swap/v1/quote -p '{
  "inputMint": "So11111111111111111111111111111111111111112",
  "outputMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  "amount": "1000000",
  "slippageBps": "50"
}')
```

**步骤 2：构建交易**

```bash
SWAP_TX=$(pnpm fetch-api -e /swap/v1/swap -m POST -b "{
  \"quoteResponse\": $QUOTE,
  \"userPublicKey\": \"YOUR_WALLET_ADDRESS\",
  \"dynamicComputeUnitLimit\": true,
  \"prioritizationFeeLamports\": \"auto\"
}")
```

**步骤 3：签署**

```bash
UNSIGNED_TX=$(echo "$SWAP_TX" | jq -r '.swapTransaction')
SIGNED_TX=$(pnpm wallet-sign -t "$UNSIGNED_TX" --wallet ~/.config/solana/id.json)
```

**步骤 4：发送到 RPC**

```bash
pnpm send-transaction -t "$SIGNED_TX" -r "https://your-rpc.com"
```

**步骤 5：验证**

在 Solscan 上检查签名。

---

### 预测市场（测试版）

根据真实世界事件结果进行交易。合约交易金额为 $0-$1 USD，价格反映事件发生的概率。

```
Prediction Market Flow:
- [ ] Step 1: Browse events/markets
- [ ] Step 2: Create order (buy YES/NO contracts)
- [ ] Step 3: Sign and send transaction
- [ ] Step 4: Monitor position
- [ ] Step 5: Claim winnings (if correct)
```

**步骤 1：浏览事件**

```bash
# Search for events
pnpm fetch-api -e /prediction/v1/events/search -p '{"query":"election","limit":"10"}'

# List all events
pnpm fetch-api -e /prediction/v1/events -p '{"category":"politics","includeMarkets":"true"}'

# Get specific event with markets
pnpm fetch-api -e /prediction/v1/events/{eventId} -p '{"includeMarkets":"true"}'
```

**步骤 2：创建订单**

```bash
# Buy YES contracts on a market
ORDER=$(pnpm fetch-api -e /prediction/v1/orders -m POST -b '{
  "ownerPubkey": "YOUR_WALLET_ADDRESS",
  "marketId": "MARKET_ID",
  "isYes": true,
  "isBuy": true,
  "contracts": 10,
  "maxBuyPriceUsd": 0.65
}')
```

响应中包含未签名的交易（base64 格式）和订单详情。

**步骤 3：签署并发送**

```bash
UNSIGNED_TX=$(echo "$ORDER" | jq -r '.transaction')
SIGNED_TX=$(pnpm wallet-sign -t "$UNSIGNED_TX" -w ~/.config/solana/id.json)
pnpm send-transaction -t "$SIGNED_TX" -r "YOUR_RPC_URL"
```

**步骤 4：监控头寸**

```bash
# List your positions
pnpm fetch-api -e /prediction/v1/positions -p '{"ownerPubkey":"YOUR_WALLET_ADDRESS"}'

# Get specific position
pnpm fetch-api -e /prediction/v1/positions/{positionPubkey}

# View order history
pnpm fetch-api -e /prediction/v1/history -p '{"ownerPubkey":"YOUR_WALLET_ADDRESS"}'
```

**步骤 5：领取收益**

市场结算后，领取获胜头寸的收益：

```bash
CLAIM=$(pnpm fetch-api -e /prediction/v1/positions/{positionPubkey}/claim -m POST -b '{
  "ownerPubkey": "YOUR_WALLET_ADDRESS"
}')
UNSIGNED_TX=$(echo "$CLAIM" | jq -r '.transaction')
SIGNED_TX=$(pnpm wallet-sign -t "$UNSIGNED_TX" -w ~/.config/solana/id.json)
pnpm send-transaction -t "$SIGNED_TX" -r "YOUR_RPC_URL"
```

## 预测 API 端点

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| GET | `/prediction/v1/events` | 使用过滤器列出事件 |
| GET | `/prediction/v1/events/search` | 根据查询搜索事件 |
| GET | `/prediction/v1/events/{eventId}` | 获取事件详情 |
| GET | `/prediction/v1/markets/{marketId}` | 获取市场详情 |
| GET | `/prediction/v1/orderbook/{marketId}` | 获取订单簿 |
| POST | `/prediction/v1/orders` | 创建订单（返回未签名的交易） |
| DELETE | `/prediction/v1/orders` | 关闭/取消订单 |
| GET | `/prediction/v1/positions` | 列出用户头寸 |
| DELETE | `/prediction/v1/positions/{positionPubkey}` | 卖出头寸 |
| POST | `/prediction/v1/positions/{positionPubkey}/claim` | 领取收益 |
| GET | `/prediction/v1/leaderboards` | 查看排行榜 |
| GET | `/prediction/v1/profiles/{ownerPubkey}` | 用户资料统计 |

**关键概念**

- **合约**：以单位进行交易，每个单位的价值为 $0-$1，基于概率
- **YES/NO**：二元结果 - 如果你认为事件会发生则购买 YES，否则购买 NO
- **结算**：获胜的合约支付 $1，失败的合约支付 $0
- **无领取费用**：获胜者每份合约可获得全额 $1

---

### Jupiter 借贷

存入代币以赚取收益或抵押代币进行借贷。

**存入（赚取收益）**

```bash
# Get deposit transaction
DEPOSIT=$(pnpm fetch-api -e /lend/v1/earn/deposit -m POST -b '{
  "asset": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  "amount": "1000000",
  "signer": "YOUR_WALLET_ADDRESS"
}')

# Sign and send
UNSIGNED_TX=$(echo "$DEPOSIT" | jq -r '.transaction')
SIGNED_TX=$(pnpm wallet-sign -t "$UNSIGNED_TX" -w ~/.config/solana/id.json)
pnpm send-transaction -t "$SIGNED_TX" -r "YOUR_RPC_URL"
```

**提取**

```bash
WITHDRAW=$(pnpm fetch-api -e /lend/v1/earn/withdraw -m POST -b '{
  "asset": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  "amount": "1000000",
  "signer": "YOUR_WALLET_ADDRESS"
}')
# Sign and send as above
```

---

### 投资组合 API

跟踪 DeFi 头寸、平台信息和在 Solana 上质押的 JUP。

**获取头寸**

获取钱包地址在 Jupiter 产品中的所有头寸。

```bash
# Get all positions
pnpm fetch-api -e /portfolio/v1/positions/YOUR_WALLET_ADDRESS

# Filter by specific platforms
pnpm fetch-api -e /portfolio/v1/positions/YOUR_WALLET_ADDRESS -p '{"platforms":"jupiter-exchange,jupiter-governance"}'
```

响应包括：
- `elements`：头寸类型数组（Multiple, Liquidity, Leverage, BorrowLend, Trade）
- `tokenInfo`：按网络和地址索引的代币元数据
- `fetcherReports`：每个数据获取器的状态

**获取平台**

列出投资组合 API 跟踪的所有可用平台。

```bash
pnpm fetch-api -e /portfolio/v1/platforms
```

响应包括平台详情：
- `id`：平台标识符（例如 `jupiter-exchange`）
- `name`：显示名称
- `image`：Logo URL
- `description`：平台概述
- `defiLlamaId`：DefiLlama 参考链接
- `isDeprecated`：平台是否已弃用
- `tags`：分类标签
- `links`：社交/网站链接（网站、Discord、Twitter、GitHub、文档）

**获取质押的 JUP**

检查钱包的质押 JUP 金额和待解押金额。

```bash
pnpm fetch-api -e /portfolio/v1/staked-jup/YOUR_WALLET_ADDRESS
```

响应：
```json
{
  "stakedAmount": 15000.5,
  "unstaking": [
    {
      "amount": 500,
      "until": 1711000000000
    }
  ]
}
```

- `stakedAmount`：总质押的 JUP 金额
- `unstaking`：待解押的金额及完成时间戳（毫秒）

---

### 触发 API（限价单）

创建在价格条件满足时自动执行的订单。

**创建限价单**

```bash
ORDER=$(pnpm fetch-api -e /trigger/v1/createOrder -m POST -b '{
  "inputMint": "So11111111111111111111111111111111111111112",
  "outputMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  "maker": "YOUR_WALLET_ADDRESS",
  "payer": "YOUR_WALLET_ADDRESS",
  "params": {
    "makingAmount": "1000000000",
    "takingAmount": "150000000",
    "expiredAt": null
  }
}')

# Sign and send
UNSIGNED_TX=$(echo "$ORDER" | jq -r '.transaction')
SIGNED_TX=$(pnpm wallet-sign -t "$UNSIGNED_TX" -w ~/.config/solana/id.json)
pnpm send-transaction -t "$SIGNED_TX" -r "YOUR_RPC_URL"
```

参数：
- `makingAmount`：要出售的输入代币数量（最小单位）
- `takingAmount`：要接收的输出代币最小数量
- `expiredAt`：过期时间戳（null = 无过期）
- `slippageBps`：可选的滑点容忍度（0 = 仅精确价格）

**获取订单**

```bash
# Get active orders
pnpm fetch-api -e /trigger/v1/getTriggerOrders -p '{"user":"YOUR_WALLET","orderStatus":"active"}'

# Get order history
pnpm fetch-api -e /trigger/v1/getTriggerOrders -p '{"user":"YOUR_WALLET","orderStatus":"history","page":"1"}'
```

**取消订单**

```bash
# Cancel single order
CANCEL=$(pnpm fetch-api -e /trigger/v1/cancelOrder -m POST -b '{
  "maker": "YOUR_WALLET_ADDRESS",
  "order": "ORDER_ACCOUNT_ADDRESS",
  "computeUnitPrice": "auto"
}')
# Sign and send transaction

# Cancel all orders (batched in groups of 5)
CANCEL_ALL=$(pnpm fetch-api -e /trigger/v1/cancelOrders -m POST -b '{
  "maker": "YOUR_WALLET_ADDRESS",
  "computeUnitPrice": "auto"
}')
```

**触发 API 端点**

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| POST | `/trigger/v1/createOrder` | 创建限价单 |
| GET | `/trigger/v1/getTriggerOrders` | 根据钱包获取订单 |
| POST | `/trigger/v1/cancelOrder` | 取消单个订单 |
| POST | `/trigger/v1/cancelOrders` | 批量取消多个订单 |

**费用**：稳定对价为 0.03%，其他对价为 0.1%。

---

### 定期 API（DCA）

在指定时间间隔自动购买代币。

**创建定期订单**

```bash
ORDER=$(pnpm fetch-api -e /recurring/v1/createOrder -m POST -b '{
  "user": "YOUR_WALLET_ADDRESS",
  "inputMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  "outputMint": "So11111111111111111111111111111111111111112",
  "params": {
    "time": {
      "inAmount": "10000000",
      "numberOfOrders": 10,
      "interval": 86400,
      "minPrice": null,
      "maxPrice": null,
      "startAt": null
    }
  }
}')

# Sign and send
UNSIGNED_TX=$(echo "$ORDER" | jq -r '.transaction')
SIGNED_TX=$(pnpm wallet-sign -t "$UNSIGNED_TX" -w ~/.config/solana/id.json)
pnpm send-transaction -t "$SIGNED_TX" -r "YOUR_RPC_URL"
```

参数：
- `inAmount`：总花费金额（原始单位）
- `numberOfOrders`：要购买的订单数量
- `interval`：购买间隔（86400 = 每天）
- `minPrice`/`maxPrice`：可选的价格范围（null = 任意价格）
- `startAt`：开始时间戳（null = 立即）

**获取订单**

```bash
# Get active DCA orders
pnpm fetch-api -e /recurring/v1/getRecurringOrders -p '{"user":"YOUR_WALLET","orderStatus":"active","recurringType":"time"}'

# Get order history
pnpm fetch-api -e /recurring/v1/getRecurringOrders -p '{"user":"YOUR_WALLET","orderStatus":"history","recurringType":"time","page":"1"}'
```

**取消订单**

```bash
CANCEL=$(pnpm fetch-api -e /recurring/v1/cancelOrder -m POST -b '{
  "user": "YOUR_WALLET_ADDRESS",
  "order": "ORDER_ACCOUNT_ADDRESS",
  "recurringType": "time"
}')
# Sign and send transaction
```

**定期 API 端点**

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| POST | `/recurring/v1/createOrder` | 创建定期订单 |
| GET | `/recurring/v1/getRecurringOrders` | 根据钱包获取定期订单 |
| POST | `/recurring/v1/cancelOrder` | 取消订单 |

**费用**：每次执行费用为 0.1%。Token2022 代币不支持。

---

## API 端点参考

| 使用场景 | API | 端点 |
|----------|-----|----------|
| 代币交易对换（默认） | Ultra | `/ultra/v1/order`, `/ultra/v1/execute` |
| 带控制的交易对换 | Metis | `/swap/v1/quote`, `/swap/v1/swap` |
| 限价单 | Trigger | `/trigger/v1/createOrder`, `/trigger/v1/cancelOrder` |
| 获取限价单 | Trigger | `/trigger/v1/getTriggerOrders` |
| 定期订单 | Recurring | `/recurring/v1/createOrder`, `/recurring/v1/cancelOrder` |
| 获取定期订单 | Recurring | `/recurring/v1/getRecurringOrders` |
| 代币搜索 | Ultra | `/ultra/v1/search` |
| 代币持有情况 | Ultra | `/ultra/v1/holdings/{address}` |
| 代币警告 | Ultra | `/ultra/v1/shield` |
| 代币价格 | Price | `/price/v3?ids={mints}` |
| 代币元数据 | Tokens | `/tokens/v2/search?query={query}` |
| 投资组合头寸 | Portfolio | `/portfolio/v1/positions/{address}` |
| 投资组合平台 | Portfolio | `/portfolio/v1/platforms` |
| 抵押的 JUP | Portfolio | `/portfolio/v1/staked-jup/{address}` |
| 预测市场 | Prediction | `/prediction/v1/events`, `/prediction/v1/orders` |
| 借贷存入 | Lend | `/lend/v1/earn/deposit` |
| 借贷提取 | Lend | `/lend/v1/earn/withdraw` |

---

## 注意事项与限制

### API 密钥与速率限制

| 等级 | 速率限制 |
|------|------------|
| 免费 | 每分钟 60 次请求 |
| 专业版 | 每分钟最多 30,000 次请求 |
| Ultra | 根据执行的交易对换量动态调整 |

随着执行的交易对换量增加，Ultra 的速率限制也会增加。基础限制为每 10 秒 50 次请求。

### 费用

| API | 费用 |
|-----|-----|
| Ultra | 每笔交易对换 5-10 个基点 |
| Metis | 无 Jupiter 费用（用户需支付 gas） |

集成商可以添加自定义费用（50-255 个基点）。Jupiter 会收取集成商费用的 20%。

### 无 gas 要求

Ultra 提供“无 gas”交易对换服务，Jupiter 支付交易费用，但有以下重要限制：
- **用户仍需 SOL** 用于账户租金（创建代币账户）
- **用户必须签署** 交易（并非真正的“零接触”）
- **最低交易金额**：约 $10 等值
- 当接受方持有量小于 0.01 SOL 时自动执行
- JupiterZ RFQ：做市商支付交易费用

### 交易大小限制

Solana 交易的大小限制为 **1232 字节**。如果超过此限制：
- 减少报价请求中的 `maxAccounts` 参数
- 对于 Metis，使用 `dynamicComputeUnitLimit: true`

### 代币限制

- **Token2022**：不支持定期（DCA）订单
- 某些代币可能有转账费用或冻结权限

### Ultra 与 Metis 的比较

| 特性 | Ultra | Metis |
|---------|-------|-------|
| 是否需要 RPC | 不需要（Jupiter 处理） | 需要（用户需要使用 RPC） |
| 无 gas | 是（满足特定条件时） | 否 |
| 是否支持自定义指令 | 不支持 | 支持 |
| 交易组合 | 不支持 | 支持 |
| 滑点 | 自动优化 | 手动设置 |

**大多数交易对换使用 Ultra**。**仅在需要添加自定义指令或组合交易时使用 Metis**。

### 常见错误

| 错误 | 原因 | 解决方法 |
|-------|-------|-----|
| `TransactionExpiredBlockhashNotFound` | Blockhash 过期 | 重新请求订单/报价 |
| `SlippageToleranceExceeded` | 价格变动过大 | 增加滑点容忍度或重试 |
| `InsufficientFunds` | SOL/代币不足 | 检查余额 |
| `RateLimited (429)` | 请求过多 | 等待或升级等级 |
| `InvalidSignature` | 签名错误或交易损坏 | 验证钱包地址是否与接受方地址匹配 |

### Ultra 执行错误代码

| 代码 | 含义 |
|------|---------|
| 0 | 成功 |
| -1 至 -5 | 客户端/验证错误 |
| -1000 至 -1999 | 分集器路由错误 |
| -2000 至 -2999 | RFQ（做市商）错误 |

---

## 环境变量

| 变量 | 描述 | 默认值 |
|----------|-------------|---------|
| `JUP_API_KEY` | Jupiter API 密钥 | （必需） |
| `SOLANA_RPC_URL` | 发送交易的 RPC 端点 | `https://api.mainnet-beta.solana.com` |

---

## 常见代币发行地址

| 代币 | 发行地址 |
|-------|--------------|
| SOL（wrapped） | `So1111111111111111111111111111111111111112` |
| USDC | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |
| USDT | `Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB` |
| JUP | `JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN` |

---

## 资源

- [Jupiter 门户](https://portal.jup.ag) - API 密钥管理
- [Jupiter 文档](https://dev.jup.ag) - 完整文档
- [状态页面](https://status.jup.ag) - API 状态
- [Solscan](https://solscan.io) - 交易浏览器