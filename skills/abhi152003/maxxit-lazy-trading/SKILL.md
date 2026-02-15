---
emoji: 📈
name: maxxit-lazy-trading
version: 1.1.0
author: Maxxit
description: 通过 Maxxit 的懒惰交易（Lazy Trading）API，在 Ostium 平台上执行永久性交易（即长期持有的交易）。该 API 提供了用于开仓/平仓、管理风险以及获取市场数据的程序化接口。
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

通过 Maxxit 的懒人交易 API，在 Ostium 协议上执行永久性期货交易。此功能支持通过编程接口自动化执行开仓/平仓操作以及风险管理。

## 适用场景

- 用户希望在 Ostium 上进行交易
- 用户查询懒人交易账户详情
- 用户查看 USDC/ETH 余额
- 用户查看未平仓头寸或投资组合
- 用户查看平仓历史或盈亏情况
- 用户查询可交易的符号
- 用户获取市场数据或 LunarCrush 指标以用于分析
- 用户需要整个市场的快照用于交易决策
- 用户希望比较不同代币的排名（AltRank）
- 用户希望识别高情绪值的交易机会
- 用户希望了解加密货币的社交媒体关注趋势
- 用户希望开新的交易头寸（多头/空头）
- 用户希望平仓现有头寸
- 用户希望设置或修改止盈水平
- 用户希望设置或修改止损水平
- 用户希望获取当前代币/市场价格
- 用户提及“懒人交易”、“永久性合约”或“期货交易”
- 用户希望自动化交易流程

---

## ⚠️ 重要提示：API 参数规则（在调用任何接口之前请务必阅读）

> **切勿假设、猜测或凭空设定 API 请求参数的值。** 所有必需的参数必须来自之前的 API 响应或用户的明确输入。如果缺少某个必需参数，必须首先从相应的依赖接口获取该参数。

### 参数依赖关系图

以下显示了每个必需参数的来源。**在调用接口之前，请务必解决所有依赖关系。**

| 参数 | 来源 | 需要获取的接口 |
|---------|--------|------------------------|
| `userAddress` / `address` | `/club-details` 响应 → `user_wallet` | `GET /club-details` |
| `agentAddress` | `/club-details` 响应 → `ostium_agent_address` | `GET /club-details` |
| `tradeIndex` | `/open-position` 响应 → `actualTradeIndex` **或** `/positions` 响应 → `tradeIndex` | `POST /open-position` 或 `POST /positions` |
| `pairIndex` | `/positions` 响应 → `pairIndex` **或** `/symbols` 响应 → 符号 `id` | `POST /positions` 或 `GET /symbols` |
| `entryPrice` | `/open-position` 响应 → `entryPrice` **或** `/positions` 响应 → `entryPrice` | `POST /open-position` 或 `POST /positions` |
| `market` / `symbol` | 用户指定的代币 **或** `/symbols` 响应 → `symbol` | 用户输入或 `GET /symbols` |
| `side` | 用户指定“long”或“short” | 用户输入（必需） |
| `collateral` | 用户指定的 USDC 金额 | 用户输入（必需） |
| `leverage` | 用户指定的杠杆倍数 | 用户输入（必需） |
| `takeProfitPercent` | 用户指定的百分比（例如：0.30 = 30%） | 用户输入（必需） |
| `stopLossPercent` | 用户指定的百分比（例如：0.10 = 10%） | 用户输入（必需） |

### 强制性工作流程规则

1. **始终首先调用 `/club-details` 以获取 `userWallet`（用作 `userAddress`/`address`）和 `ostium_agent_address`（用作 `agentAddress`）。将这些信息缓存起来，因为它们在会话期间不会改变。**
2. **切勿硬编码或猜测钱包地址。** 这些地址对每个用户都是唯一的，必须从 `/club-details` 中获取。**
3. **开仓时：** 首先获取市场数据（通过 `/lunarcrush` 或 `/market-data`），向用户展示数据，获取明确的交易参数（抵押品、杠杆、方向、止盈、止损），然后执行交易。**
4. **开仓后设置止盈/止损时：** 使用 `/open-position` 响应中的 `actualTradeIndex`。如果之前没有该信息（例如，头寸是在之前开的），则调用 `/positions` 来获取 `tradeIndex`、`pairIndex` 和 `entryPrice`。
5. **平仓时：** 需要 `tradeIndex` —— 必须首先调用 `/positions` 来查找用户指定市场/头寸对应的正确索引。
6. **向用户询问交易参数** —— 切勿假设抵押品金额、杠杆、止盈百分比或止损百分比。提供默认值，但允许用户确认或修改。
7. **在交易前，如果不确定某个代币是否在 Ostium 上可用，通过调用 `/symbols` 来验证市场是否存在。**

### 在每次 API 调用前的准备工作（请在心中默记）

---

## 认证

所有请求都需要一个以 `lt_` 为前缀的 API 密钥。可以通过以下方式传递：
- 请求头：`X-API-KEY: lt_你的_API_key`
- 或者：`Authorization: Bearer lt_你的_API_key`

## API 接口

### 获取账户详情

检索懒人交易账户信息，包括代理状态、Telegram 连接和交易偏好设置。

### 获取可用符号

检索 Ostium 交易所中所有可交易的符号。使用这些信息来了解可以交易的符号以及获取它们的 LunarCrush 数据。

### 获取 LunarCrush 市场数据

检索特定符号的缓存 LunarCrush 市场指标。这些数据包括社交情绪、价格变化、波动性和市场排名。

> **⚠️ 依赖关系**：必须先调用 `/symbols` 接口以获取准确的符号字符串（例如：“BTC/USD”）。符号参数必须完全匹配。

### LunarCrush 字段说明

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `galaxy_score` | 浮点数 | 综合社交、市场和开发者活动的整体代币质量评分（0-100） |
| `alt_rank` | 整数 | 在所有加密货币中的排名（排名越低越好，1 为最佳） |
| `social_volume_24h` | 浮点数 | 过去 24 小时的社交媒体提及量 |
| `sentiment` | 浮点数 | 市场情绪评分（0-100，50 表示中性，>50 表示看涨） |
| `percent_change_24h` | 浮点数 | 过去 24 小时的价格变化百分比 |
| `volatility` | 浮点数 | 价格波动性评分（0-0.02 表示稳定，0.02-0.05 表示正常，>0.05 表示风险较高） |
| `price` | 字符串 | 当前价格（以 USD 为单位，使用小数格式） |
| `volume_24h` | 字符串 | 过去 24 小时的交易量（使用小数格式） |
| `market_cap` | 字符串 | 市场资本化（使用小数格式） |
| `market_cap_rank` | 整数 | 按市场资本化排名的顺序（排名越低越好） |
| `social_dominance` | 浮点数 | 相对于总市场的社交媒体关注度 |
| `market_dominance` | 浮点数 | 相对于总市场的市场资本化占比 |
| `interactions_24h` | 浮点数 | 过去 24 小时的社交媒体互动量 |
| `galaxy_score_previous` | 浮点数 | 上一次的银河评分（用于趋势分析） |
| `alt_rank_previous` | 整数 | 上一次的代币排名（用于趋势分析） |

**数据更新频率：**
- LunarCrush 数据由后台任务定期更新和缓存
- 通过检查 `updated_at` 字段可以了解数据最后一次更新的时间
- 数据通常每隔几小时更新一次

### 获取账户余额

检索用户 Ostium 钱包地址的 USDC 和 ETH 余额。

> **⚠️ 依赖关系**：`address` 字段是用户的 Ostium 钱包地址（`user_wallet`）。必须首先从 `/club-details` 中获取该地址 —— 切勿硬编码或猜测。

### 获取投资组合头寸

获取用户 Ostium 交易账户的所有未平仓头寸。**此接口非常重要** —— 它返回 `tradeIndex`、`pairIndex` 和 `entryPrice`，这些信息是平仓和设置止盈/止损所必需的。

> **⚠️ 依赖关系**：`address` 字段必须来自 `/club-details` → `user_wallet`。切勿猜测。

**🔑 此接口提供的值被以下接口使用：**
- `/close-position`（需要 `tradeIndex`）
- `/set-take-profit`（需要 `tradeIndex`、`pairIndex`、`entryPrice`）
- `/set-stop-loss`（需要 `tradeIndex`、`pairIndex`、`entryPrice`）

### 请求体示例：

```bash
curl -L -X POST "${MAXXIT_API_URL}/api/lazy-trading/programmatic/history" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"address": "0x...", "count": 50}'
```

### 响应示例：

```json
{
  "address": "0x...",  // 用户的 Ostium 钱包地址（必需）
  "count": 50           // 要检索的最近订单数量（默认：50）
}
```

```json
{
  "success": true,
  "history": [
    {
      "market": "ETH",
      "side": "long",
      "collateral": 50.0,
      "leverage": 5,
      "price": 3200.0,
      "pnlUsdc": 15.50,
      "profitPercent": 31.0,
      "totalProfitPercent": 31.0,
      "rolloverFee": 0.05,
      "fundingFee": 0.10,
      "executedAt": "2025-02-10T15:30:00Z",
      "tradeId": "trade_123"
    }
  ],
  "count": 25
}
```

```bash
curl -L -X POST "${MAXXIT_API_URL}/api/lazy-trading/programmatic/open-position" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "agentAddress": "0x...", \
    "userAddress": "0x...", \
    "market": "BTC",
    "side": "long",
    "collateral": 100,
    "leverage": 10
  }
```

```json
{
  "agentAddress": "0x...",      // 必需 —— 来自 /club-details → ostium_agent_address。切勿猜测。
  "userAddress": "0x...",       // 必需 —— 来自 /club-details → user_wallet。切勿猜测。
  "market": "BTC",              // 必需 —— 代币符号。如果不确定，请通过 /symbols 验证。
  "side": "long",               // 必需 —— “long” 或 “short”。请询问用户。
  "collateral": 100,            // 必需 —— 抵押品（以 USDC 计）。请询问用户。
  "leverage": 10,               // 可选（默认：10）。请询问用户。
  "deploymentId": "uuid...",    // 可选 —— 相关的部署 ID
  "signalId": "uuid...",        // 可选 —— 相关的信号 ID
  "isTestnet": false            // 可选（默认：false）
}
```

```json
{
  "success": true,
  "orderId": "order_123",
  "tradeId": "trade_abc",
  "transactionHash": "0x...", \
  "txHash": "0x...", \
  "status": "OPEN",
  "message": "头寸已成功开仓",
  "actualTradeIndex": 2,       // 请保存此值 —— 用于 /set-take-profit 和 /set-stop-loss
  "entryPrice": 95000.0         // 请保存此值 —— 用于 /set-take-profit 和 /set-stop-loss
}
```

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

```json
{
  "agentAddress": "0x...",      // 必需 —— 来自 /club-details → ostium_agent_address。切勿猜测。
  "userAddress": "0x...",       // 必需 —— 来自 /club-details → user_wallet。切勿猜测。
  "market": "BTC",              // 必需 —— 代币符号
  "tradeId": "12345",           // 可选 —— 来自 /positions → tradeId
  "actualTradeIndex": 2,         // 强烈建议 —— 来自 /positions → tradeIndex。切勿猜测。
  "isTestnet": false            // 可选（默认：false）
}
```

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

```bash
curl -L -X POST "${MAXXIT_API_URL}/api/lazy-trading/programmatic/set-stop-loss" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "agentAddress": "0x...", \
    "userAddress": "0x...", \
    "market": "BTC",
    "tradeIndex": 2,
    "stopLossPercent": 0.10,
    "entryPrice": 90000,
    "pairIndex": 0,
    "side": "long"
  }
```

```bash
curl -L -X GET "${MAXXIT_API_URL}/api/lazy-trading/programmatic/market-data" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}"
```

```json
{
  "success": true,
  "data": [
    {
      "id": 0,
      "symbol": "BTC/USD",
      "group": "crypto",
      "maxLeverage": 150,
      "metrics": {
        "galaxy_score": 72.5,
        "alt_rank": 1,
        "social_volume_24h": 15234,
        "sentiment": 68.3,
        "percent_change_24h": 2.45,
        "volatility": 0.032,
        "price": "95000.12345678",
        "volume_24h": "45000000000.00000000",
        "market_cap": "185000000000.00000000",
        "market_cap_rank": 1,
        "social_dominance": 45.2,
        "market_dominance": 52.1,
        "interactions_24h": 890000,
        "galaxy_score_previous": 70.1,
        "alt_rank_previous": 1
      },
      "updated_at": "2026-02-14T08:30:00.000Z"
    },
    ...
  ],
  "count": 45
}
```

```bash
curl -X GET "${MAXXIT_API_URL}/api/lazy-trading/programmatic/price?token=BTC&isTestnet=false" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}"
```

## 准备工作流程：

1. **步骤 1：** 从 `/club-details` 获取地址（`userWallet` 和 `ostium_agent_address`）。
2. **步骤 2：** 从 `/symbols` 验证用户请求的代币是否在 Ostium 上可用，并获取准确的符号字符串和最大杠杆倍数。
3. **步骤 3：** 调用 `/lunarcrush?symbol=TOKEN/USD`（或 `/market-data` 获取所有代币的数据）。
4. **步骤 4：** 向用户展示数据，并询问交易参数。
5. **步骤 5：** 根据步骤 1 和 4 的信息，执行开仓操作。
6. **步骤 6（如果用户需要设置止盈/止损）：** 调用 `/set-take-profit` 和/或 `/set-stop-loss`。

---

## 环境变量

| 变量 | 描述 | 示例 |
|----------|-------------|---------|
| `MAXXIT_API_KEY` | 懒人交易 API 密钥（以 `lt_` 开头） | `lt_abc123...` |
| `MAXXIT_API_URL` | Maxxit API 基本 URL | `https://maxxit.ai` |

## 错误处理

| 状态码 | 含义 |
|-------------|---------|
| 401 | API 密钥无效或缺失 |
| 404 | 未找到懒人交易代理（请先完成设置） |
| 400 | 消息/参数缺失或无效 |
| 405 | HTTP 方法错误 |
| 500 | 服务器错误 |

## 开始使用

1. **设置懒人交易**：访问 https://maxxit.ai/lazy-trading 连接钱包并配置代理。
2. **生成 API 密钥**：前往控制面板生成 API 密钥。
3. **配置环境**：设置 `MAXXIT_API_KEY` 和 `MAXXIT_API_URL`。
4. **开始交易**：使用此功能发送交易指令！

## 安全注意事项

- **切勿共享您的 API 密钥**。
- API 密钥可以在控制面板中重新生成。
- 所有交易都在链上执行，并使用您委托的钱包权限。