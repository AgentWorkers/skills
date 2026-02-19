---
emoji: 📈
name: maxxit-lazy-trading
version: 1.2.0
author: Maxxit
description: 通过 Maxxit 的 Lazy Trading API，在 Ostium 上执行永久性交易（即长期持有的交易）。该 API 提供了用于开仓/平仓、管理风险、获取市场数据以及复制交易其他 OpenClaw 代理程序的编程接口。
homepage: https://maxxit.ai
repository: https://github.com/Maxxit-ai/maxxit-latest
disableModelInvocation: true
requires:
  env:
    - MAXXIT_API_KEY
    - MAXXIT_API_URL
metadata:
  openclaw:
    requiredEnv:
      - MAXXIT_API_KEY
      - MAXXIT_API_URL
    bins:
      - curl
    primaryCredential: MAXXIT_API_KEY
---
# Maxxit 懒人交易（Lazy Trading）

通过 Maxxit 的懒人交易 API，在 Ostium 协议上执行永久性期货交易。此功能允许通过编程接口自动开仓/平仓和管理风险。

## 何时使用此功能

- 用户希望在 Ostium 上执行交易
- 用户询问懒人交易账户详情
- 用户想查看他们的 USDC/ETH 余额
- 用户想查看他们的未平仓头寸或投资组合
- 用户想查看他们的平仓历史或损益
- 用户想了解可交易的符号
- 用户想获取市场数据或 LunarCrush 指标以供分析
- 用户想要整个市场的快照用于交易
- 用户想比较不同代币的排名（AltRank）
- 用户想发现高情绪价值的交易机会
- 用户想了解加密货币资产的社会媒体关注趋势
- 用户想开新的交易头寸（多头/空头）
- 用户想平仓现有的头寸
- 用户想设置或修改止盈水平
- 用户想设置或修改止损水平
- 用户想获取当前的代币/市场价格
- 用户提到“懒人交易”、“perps”、“perpetuals”或“期货交易”
- 用户想自动化他们的交易流程
- 用户想复制交易或镜像其他交易者的头寸
- 用户想发现可以学习的其他 OpenClaw 代理
- 用户想查看表现最好的交易者正在进行的交易
- 用户想找到高影响因子的交易者进行复制

---

## ⚠️ 重要提示：API 参数规则（在调用任何端点之前请阅读）

> **切勿假设、猜测或凭空想象 API 请求参数的值。** 每个必需的参数都必须来自之前的 API 响应或用户的明确输入。如果您没有所需的值，必须首先从相应的依赖端点获取它。

### 参数依赖关系图

以下显示了每个必需参数的来源。**在调用端点之前，请始终解决依赖关系。**

| 参数 | 来源 | 需要从中获取的端点 |
|-----------|--------|------------------------|
| `userAddress` / `address` | `/club-details` 响应 → `user_wallet` | `GET /club-details` |
| `agentAddress` | `/club-details` 响应 → `ostium_agent_address` | `GET /club-details` |
| `tradeIndex` | `/open-position` 响应 → `actualTradeIndex` **或** `/positions` 响应 → `tradeIndex` | `POST /open-position` 或 `POST /positions` |
| `pairIndex` | `/positions` 响应 → `pairIndex` **或** `/symbols` 响应 → `symbol id` | `POST /positions` 或 `GET /symbols` |
| `entryPrice` | `/open-position` 响应 → `entryPrice` **或** `/positions` 响应 → `entryPrice` | `POST /open-position` 或 `POST /positions` |
| `market` / `symbol` | 用户指定的代币 **或** `/symbols` 响应 → `symbol`（例如 `ETH/USD`） | 用户输入或 `GET /symbols` |
| `side` | 用户指定 „long“ 或 „short“ | 用户输入（必需） |
| `collateral` | 用户指定的 USDC 金额 | 用户输入（必需） |
| `leverage` | 用户指定的杠杆倍数 | 用户输入（必需） |
| `takeProfitPercent` | 用户指定的百分比（例如，0.30 = 30%） | 用户输入（必需） |
| `stopLossPercent` | 用户指定的百分比（例如，0.10 = 10%） | 用户输入（必需） |
| `address`（用于复制交易者交易） | `/copy-traders` 响应 → `creatorWallet` 或 `walletAddress` | `GET /copy-traders` |

### 强制性工作流程规则

1. **始终首先调用 `/club-details` 以获取 `userWallet`（用作 `userAddress`/`address`）和 `ostium_agent_address`（用作 `agentAddress`）。将这些值缓存起来，因为它们在会话期间不会改变。**
2. **切勿硬编码或猜测钱包地址。** 它们对每个用户都是唯一的，必须来自 `/club-details`。
3. **对于开仓：** 首先获取市场数据（通过 `/lunarcrush` 或 `/market-data`），展示给用户，获取明确的确认以及交易参数（抵押品、杠杆、方向、止盈、止损），然后执行交易。
   - **市场格式规则（Ostium）：** `/symbols` 返回的配对格式如 `ETH/USD`，但 `/open-position` 仅期望 `market` 作为基础代币（例如 `ETH`）。在 `/` 之前转换基础代币。
4. **在开仓后设置止盈/止损：** 使用 `/open-position` 响应中的 `actualTradeIndex`。如果您没有它（例如，头寸是之前开的），则调用 `/positions` 以获取 `tradeIndex`、`pairIndex` 和 `entryPrice`。
5. **对于平仓头寸：** 您需要 `tradeIndex` — 必须首先调用 `/positions` 以查找用户指定市场的正确索引。
6. **询问用户交易参数** — 切勿假设抵押品金额、杠杆、止盈百分比或止损百分比。展示默认值，但允许用户确认或覆盖。
7. **在交易之前，如果不确定代币是否在 Ostium 上可用，请通过调用 `/symbols` 来验证市场是否存在。**

### 在每次 API 调用之前的检查清单

---

## 认证

所有请求都需要一个以 `lt_` 为前缀的 API 密钥。通过以下方式传递它：
- 标头：`X-API-KEY: lt_你的 API 密钥`
- 或：`Authorization: Bearer lt_你的 API 密钥`

## API 端点

## Ostium 程序化端点（`/api/lazy-trading/programmatic/*`）

> 除非前缀为 `/aster/`，否则 `/api/lazy-trading/programmatic/*` 下的所有端点都是用于 **Ostium** 的。

### 获取账户详情

检索懒人交易账户信息，包括代理状态、Telegram 连接和交易偏好。

---

**响应：**
---

### 获取可用符号

从 Ostium 交易所检索所有可交易的符号。使用此信息来发现可以交易的符号并获取 LunarCrush 数据。

---

**响应：**
---

### 获取 LunarCrush 市场数据

检索特定符号的缓存 LunarCrush 市场指标。这些数据包括社会情绪、价格变化、波动性和市场排名。

> **⚠️ 依赖关系**：您必须首先调用 `/symbols` 端点以获取准确的符号字符串（例如，`BTC/USD`）。符号参数需要完全匹配。

---

**响应：**
---

**LunarCrush 字段描述：**

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `galaxy_score` | 浮点数 | 综合社会、市场和开发者活动的整体硬币质量评分（0-100） |
| `alt_rank` | 整数 | 在所有加密货币中的排名（排名越低越好，1 = 最好） |
| `social_volume_24h` | 浮点数 | 过去 24 小时的社交媒体提及量 |
| `sentiment` | 浮点数 | 市场情绪评分（0-100，50 为中性，>50 为看涨） |
| `percent_change_24h` | 浮点数 | 过去 24 小时的价格变化百分比 |
| `volatility` | 浮点数 | 价格波动性评分（0-0.02 表示稳定，0.02-0.05 表示正常，>0.05 表示风险） |
| `price` | 字符串 | 当前价格（以 USD 为单位，使用小数字符串） |
| `volume_24h` | 字符串 | 过去 24 小时的交易量（小数字符串） |
| `market_cap` | 字符串 | 市场资本化（小数字符串） |
| `market_cap_rank` | 整数 | 按市场资本化排名（排名越低越好） |
| `social_dominance` | 浮点数 | 相对于总市场的社交媒体量 |
| `market_dominance` | 浮点数 | 相对于总市场的市场资本化 |
| `interactions_24h` | 浮点数 | 过去 24 小时的社交媒体互动量 |
| `galaxy_score_previous` | 浮点数 | 上一次的银河评分（用于趋势分析） |
| `alt_rank_previous` | 整数 | 上一次的代币排名（用于趋势分析） |

**数据更新频率：**
- LunarCrush 数据由后台工作进程定期缓存和更新
- 查看 `updated_at` 字段以了解数据上次更新的时间
- 数据通常每隔几小时更新一次

### 获取账户余额

检索用户 Ostium 钱包地址的 USDC 和 ETH 余额。

> **⚠️ 依赖关系**：`address` 字段是用户的 Ostium 钱包地址（`user_wallet`）。您必须首先从 `/club-details` 获取它 — 切勿硬编码或猜测任何地址。

---

**响应：**
---

### 获取投资组合头寸

获取用户 Ostium 交易账户的所有未平仓头寸。**此端点至关重要** — 它返回 `tradeIndex`、`pairIndex` 和 `entryPrice`，这些是平仓头寸和设置止盈/止损所必需的。

> **⚠️ 依赖关系**：`address` 字段必须来自 `/club-details` → `user_wallet`。切勿猜测它。
>
> **🔑 此端点提供以下功能所需的值**：`/close-position`（需要 `tradeIndex`）、`/set-take-profit`（需要 `tradeIndex`、`pairIndex`、`entryPrice`）、`/set-stop-loss`（需要 `tradeIndex`、`pairIndex`、`entryPrice`）。

---

**请求体：**
---

**响应：**
---

> **从每个头寸中提取的关键字段：**
- `tradeIndex` — 用于 `/close-position`、`/set-take-profit`、`/set-stop-loss`
- `pairIndex` — 用于 `/set-take-profit`、`/set-stop-loss`
- `entryPrice` — 用于 `/set-take-profit`、`/set-stop-loss`
---

**示例代码：**
```bash
curl -L -X POST "${MAXXIT_API_URL}/api/lazy-trading/programmatic/history" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"address": "0x...", "count": 50}'
```

**响应示例：**
```json
{
  "address": "0x...",  // 用户的 Ostium 钱包地址（必需）
  "count": 50           // 要检索的最近订单数量（默认：50）
}
```

```bash
curl -L -X POST "${MAXXIT_API_URL}/api/lazy-trading/programmatic/open-position" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "agentAddress": "0x...", \
    "userAddress": "0x...", \
    "market": "BTC", \
    "side": "long", \
    "collateral": 100,
  }'
```

**响应示例：**
```json
{
  "agentAddress": "0x...",      // 必需 — 来自 /club-details → ostium_agent_address。切勿猜测。
  "userAddress": "0x...",       // 必需 — 来自 /club-details → user_wallet。切勿猜测。
  "market": "BTC",              // 必需 — 对于 Ostium 仅使用基础代币（例如 "ETH"，而不是 "ETH/USD"）。如果不确定，请通过 /symbols 验证。
  "side": "long",               // 必需 — “long” 或 “short”。询问用户。
  "collateral": 100,            // 必需 — 以 USDC 为单位的抵押品。询问用户。
  "leverage": 10,               // 可选（默认：10）。询问用户。
  "deploymentId": "uuid...",    // 可选 — 相关的部署 ID
  "signalId": "uuid...",        // 可选 — 相关的信号 ID
  "isTestnet": false            // 可选（默认：false）
}
```

**响应示例：**
```json
{
  "success": true,
  "orderId": "order_123",
  "tradeId": "trade_123",
  "transactionHash": "0x...", \
  "status": "OPEN",
  "message": "头寸已成功开仓",
  "actualTradeIndex": 2,       // ← 保存此值 — 用于 /set-take-profit 和 /set-stop-loss
  "entryPrice": 95000.0         // ← 保存此值 — 用于 /set-take-profit 和 /set-stop-loss
}
```

**示例代码：**
```bash
curl -L -X POST "${MAXXIT_API_URL}/api/lazy-trading/programmatic/close-position" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "agentAddress": "0x...", \
    "userAddress": "0x...", \
    "market": "BTC",
    "tradeId": "12345"
}
```

**响应示例：**
```json
{
  "agentAddress": "0x...",      // 必需 — 来自 /club-details → ostium_agent_address。切勿猜测。
  "userAddress": "0x...",       // 必需 — 来自 /club-details → user_wallet。切勿猜测。
  "market": "BTC",              // 必需 — 代币符号
  "tradeId": "12345",           // 可选 — 来自 /positions → tradeId
  "actualTradeIndex": 2,         // 强烈建议 — 来自 /positions → tradeIndex。切勿猜测。
  "isTestnet": false            // 可选（默认：false）
}
```

**示例代码：**
```bash
curl -L -X POST "${MAXXIT_API_URL}/api/lazy-trading/programmatic/set-take-profit" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "agentAddress": "0x...", \
    "userAddress": "0x...", \
    "market": "BTC",
    "tradeIndex": 2,
    "takeProfitPercent": 0.30,
    "entryPrice": 90000,
    "pairIndex": 0
}
```

**示例代码：**
```bash
curl -L -X POST "${MAXXIT_API_URL}/api/lazy-trading/programmatic/set-stop-loss" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "agentAddress": "0x...", \
    "userAddress": "0x...", \
    "market": "BTC",
    "tradeIndex": 2,
    "takeProfitPercent": 0.30,
    "entryPrice": 90000,
    "pairIndex": 0
}
```

**示例代码：**
```bash
curl -L -X POST "${MAXXIT_API_URL}/api/lazy-trading/programmatic/set-stop-loss" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "agentAddress": "0x...", \
    "userAddress": "0x...", \
    "market": "BTC",
    "tradeIndex": 2,
    "takeProfitPercent": 0.30,
    "entryPrice": 90000,
    "pairIndex": 0,
    "side": "long",
  }'
```

**示例代码：**
```bash
curl -L -X POST "${MAXXIT_API_URL}/api/lazy-trading/programmatic/market-data" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}"
```

**示例代码：**
```bash
curl -L -X GET "${MAXXIT_API_URL}/api/lazy-trading/programmatic/price?token=BTC&isTestnet=false" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}"
```

**示例代码：**
```bash
curl -L -X GET "${MAXXIT_API_URL}/api/lazy-trading/programmatic/programmatic/price?token=BTC&isTestnet=false" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}"
```

**示例代码：**
```bash
curl -L -X GET "${MAXXIT_API_URL}/api/lazy-trading/programmatic/programmatic/copy-traders" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}"
```

**示例代码：**
```bash
curl -L -X GET "${MAXXIT_API_URL}/api/lazy-trading/programmatic/copy-traders?source=openclaw" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}"
```

**示例代码：**
```bash
curl -L -X GET "${MAXXIT_API_URL}/api/lazy-trading/programmatic/copy-traders?source=leaderboard&minImpactFactor=50&minTrades=100" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}"
```

**示例代码：**
```json
{
  "success": true,
  "openclawTraders": [
    {
      "agentId": "3dbc322f-...", \
      "agentName": "OpenClaw Trader - 140226114735",
      "creatorWallet": "0x4e7f1e29d9e1f81c3e9249e3444843c2006f3325",
      "venue": "OSTIUM",
      "status": "PRIVATE",
      "isCopyTradeClub": false,
      "performance": {
        "apr30d": 0,
        "apr90d": 0,
        "aprSinceInception": 0,
        "sharpe30d": 0
      },
      "deployment": {
        "id": "dep-uuid",
        "status": "ACTIVE",
        "safeWallet": "0x...", \
        "isTestnet": false
      }
    },
  "topTraders": [
    {
      "walletAddress": "0xabc...", \
      "totalVolume": "1500000.000000",
      "totalClosedVolume": "1200000.000000",
      "totalPnl": "85000.000000",
      "totalProfitTrades": 120,
      "totalLossTrades": 30,
      "totalTrades": 150,
      "winRate": 0.80,
      "lastActiveAt": "2026-02-15T10:30:00.000Z",
      "scores": {
        "edgeScore": 0.82,
        "consistencyScore": 0.75,
        "stakeScore": 0.68,
        "freshnessScore": 0.92,
        "impactFactor": 72.5
      },
      "updatedAt": "2026-02-17T06:00:00.000Z"
    }
  ],
  "openclawCount": 5,
  "topTradersCount": 20
}
```

**示例代码：**
```bash
TRADER_ADDRESS=$(curl -s -L -X GET "${MAXXIT_API_URL}/api/lazy-trading/programmatic/copy-traders?source=openclaw" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}" | jq -r '.openclawTraders[0].creatorWallet')
```

**示例代码：**
```bash
curl -L -X GET "${MAXXIT_API_URL}/api/lazy-trading/programmatic/copy-trader-trades?address=${TRADER_ADDRESS}" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}"
```

**示例代码：**
```bash
curl -L -X GET "${MAXXIT_API_URL}/api/lazy-trading/programmatic/copy-trader-trades?address=${TRADER_ADDRESS}&hours=48&limit=50" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}"
```

---

## 认证

所有请求都需要一个以 `lt_` 为前缀的 API 密钥。通过以下方式传递它：
- 标头：`X-API-KEY: lt_你的 API 密钥`
- 或：`Authorization: Bearer lt_你的 API 密钥`

---

## 环境变量

| 变量 | 描述 | 示例 |
|----------|-------------|---------|
| `MAXXIT_API_KEY` | 您的懒人交易 API 密钥（以 `lt_` 开头） | `lt_abc123...` |
| `MAXXIT_API_URL` | Maxxit API 基础 URL | `https://maxxit.ai` |

## 错误处理

| 状态码 | 含义 |
|-------------|---------|
| 401 | API 密钥无效或缺失 |
| 404 | 未找到懒人交易代理（请先完成设置） |
| 400 | 缺少或无效的消息/参数 |
| 405 | HTTP 方法错误 |
| 500 | 服务器错误 |

## 开始使用

1. **设置懒人交易**：访问 https://maxxit.ai/lazy-trading 以连接您的钱包并配置您的代理
2. **生成 API 密钥**：前往您的仪表板并创建 API 密钥
3. **配置环境**：设置 `MAXXIT_API_KEY` 和 `MAXXIT_API_URL`
4. **开始交易**：使用此功能发送交易信号！

## 安全注意事项

- 切勿共享您的 API 密钥
- API 密钥可以从仪表板撤销和重新生成
- 所有交易都在链上执行，并使用您委托的钱包权限