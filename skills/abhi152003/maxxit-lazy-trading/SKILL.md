---
emoji: 📈
name: maxxit-lazy-trading
version: 1.2.1
author: Maxxit
description: 通过 Maxxit 的 Lazy Trading API，在 Ostium 和 Aster 平台上执行永久性交易（即长期持有的交易策略）。该 API 提供了用于开仓/平仓、风险管理、获取市场数据、复制交易其他 OpenClaw 代理的交易程序化接口，同时还包含一个去中心化的 Alpha Marketplace，用于买卖经过 ZK（Zero-Knowledge）验证的交易信号（这些信号来自 Arbitrum Sepolia 平台）。
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

通过 Maxxit 的懒人交易 API，在 Ostium 和 Aster DEX 上执行永久性期货交易。此功能支持通过编程接口自动开仓/平仓和管理风险。

## 何时使用此功能

- 用户希望在 Ostium 上进行交易
- 用户希望在 Aster DEX 上进行交易
- 用户询问懒人交易账户详情
- 用户想查看他们的 USDC/ETH 余额
- 用户想查看他们的未平仓头寸或投资组合
- 用户想查看已平仓头寸的历史记录或盈亏情况
- 用户想了解可交易的符号
- 用户想获取市场数据或 LunarCrush 指标以供分析
- 用户想要整个市场的快照用于交易目的
- 用户想比较不同代币的排名（AltRank）
- 用户想发现高情绪价值的交易机会
- 用户想了解加密货币资产的社会媒体关注趋势
- 用户想开新的交易头寸（多头/空头）
- 用户想平仓现有头寸
- 用户想设置或修改止盈水平
- 用户想设置或修改止损水平
- 用户想获取当前的代币/市场价格
- 用户提到“懒人交易”、“永久性期货”或“期货交易”
- 用户想自动化他们的交易流程
- 用户想复制交易者的头寸
- 用户想寻找其他 OpenClaw 代理以学习
- 用户想查看表现最佳的交易者的交易记录
- 用户想找到高影响力因子的交易者进行复制
- 用户想出售他们的交易信号作为“阿尔法产品”
- 用户想浏览或购买来自 ZK 验证的交易者的无信任阿尔法产品
- 用户想生成他们的交易表现的 ZK 证明，或将头寸标记为“阿尔法交易”

---

## ⚠️ DEX 路由规则（必须遵守）

1. **如有疑问，请先询问交易所**：“您想在 Ostium 还是 Aster 上进行交易？”
2. **在回复中明确说明当前使用的交易所**（例如：“使用 Ostium...” 或 “使用 Aster...”）
3. **不要混合建议交易所**：
   - 如果用户在 **Ostium** 上交易，只建议使用 Ostium 的接口/操作。
   - 如果用户在 **Aster** 上交易，只建议使用 Aster 的接口/操作。
4. **不要询问网络类型**：
   - 在此设置中，**Ostium** 仅支持主网。
   - **Aster** 仅支持测试网。
   - 因此，不要询问“主网还是测试网？”
5. 如果用户在对话过程中更换交易所，请确认切换后继续使用相应的交易所流程。

## ⚠️ 重要：API 参数规则（在调用任何接口之前请阅读）

> **永远不要假设、猜测或凭空设置 API 请求参数的值**。每个必需的参数都必须来自之前的 API 响应或用户的明确输入。如果您没有所需的值，必须首先从相应的依赖接口获取它。

### 参数依赖关系图

以下显示了每个必需参数的来源。**在调用接口之前，请务必解决所有依赖关系**。

| 参数 | 来源 | 需要获取的接口 |
|-----------|--------|------------------------|
| `userAddress` / `address` | `/club-details` 响应 → `user_wallet` | `GET /club-details` |
| `agentAddress` | `/club-details` 响应 → `ostium_agent_address` | `GET /club-details` |
| `tradeIndex` | `/open-position` 响应 → `actualTradeIndex` **或** `/positions` 响应 → `tradeIndex` | `POST /open-position` 或 `POST /positions` |
| `pairIndex` | `/positions` 响应 → `pairIndex` **或** `/symbols` 响应 → `symbol id` | `POST /positions` 或 `GET /symbols` |
| `entryPrice` | `/open-position` 响应 → `entryPrice` **或** `/positions` 响应 → `entryPrice` | `POST /open-position` 或 `POST /positions` |
| `market` / `symbol` | 用户指定的代币 **或** `/symbols` 响应 → `symbol`（例如 `ETH/USD`） | 用户输入或 `GET /symbols` |
| `side` | 用户指定 “long” 或 “short” | 用户输入（必需） |
| `collateral` | 用户指定的 USDC 金额 | 用户输入（必需） |
| `leverage` | 用户指定的杠杆倍数 | 用户输入（必需） |
| `takeProfitPercent` | 用户指定的百分比（例如，0.30 = 30%） | 用户输入（必需） |
| `stopLossPercent` | 用户指定的百分比（例如，0.10 = 10%） | 用户输入（必需） |
| `address`（用于复制交易） | `/copy-traders` 响应 → `creatorWallet` 或 `walletAddress` | `GET /copy-traders` |
| `commitment`（阿尔法交易） | `/alpha/agents` 响应 → `commitment` | `GET /alpha/agents` |
| `listingId`（阿尔法交易） | `/alpha/listings` 响应 → `listingId` | `GET /alpha/listings` |
| `alpha`, `contentHash`（阿尔法交易） | `/alpha/purchase` 第二阶段响应 → `alpha`, `contentHash` | `GET /alpha/purchase` + `X-Payment` 标头 |
| `txHash`（阿尔法交易） | `/alpha/pay` 响应 → `txHash` | `POST /alpha/pay` |

### 必须遵循的工作流程规则

1. **始终首先调用 `/club-details` 以获取 `userWallet`（用作 `userAddress`/`address`）和 `ostium_agent_address`（用作 `agentAddress`）。将这些信息缓存起来，因为它们在会话期间不会改变。**
2. **永远不要硬编码或猜测钱包地址。**这些地址对每个用户都是唯一的，必须来自 `/club-details`。
3. **开仓时**：首先获取市场数据（通过 `/lunarcrush` 或 `/market-data`），向用户展示数据，获取明确的交易参数（抵押品、杠杆、方向、止盈、止损），然后执行交易。
   - **市场格式规则（Ostium）**：`/symbols` 返回的格式为 `ETH/USD`，但 `/open-position` 仅接受基础代币（例如 `ETH`）。在传递之前需要转换基础代币。
4. **开仓后设置止盈/止损时**：使用 `/open-position` 响应中的 `actualTradeIndex`。如果无法获取（例如，头寸是在之前开的），则调用 `/positions` 来获取 `tradeIndex`、`pairIndex` 和 `entryPrice`。
5. **平仓头寸时**：需要 `tradeIndex` — 必须首先调用 `/positions` 来查找用户指定市场的正确头寸。
6. **询问用户交易参数** — 永远不要假设抵押品金额、杠杆、止盈百分比或止损百分比。展示默认值，但允许用户确认或修改。
7. **在交易前通过调用 `/symbols` 验证市场是否存在**，以确保代币在 Ostium 上可用。
8. **对于阿尔法交易用户**：按照以下顺序操作：`/alpha/agents` → `/alpha/listings` → `/alpha/purchase` → `/alpha/pay` → `/alpha/verify` → `/club-details` → `/alpha/execute`。不要跳过任何步骤。对于 `/alpha/verify`，请传递从购买阶段收到的 `content` 对象 — 不要修改键或值。

### 在每次 API 调用之前的准备事项

---

## 认证

所有请求都需要一个以 `lt_` 为前缀的 API 密钥。可以通过以下方式传递：
- 标头：`X-API-KEY: lt_你的_API_key`
- 或：`Authorization: Bearer lt_你的_API_key`

## API 接口

## Ostium 程序化接口（`/api/lazy-trading/programmatic/*`）

> 除非前面有 `/aster/` 前缀，否则 `/api/lazy-trading/programmatic/*` 下的所有接口都是用于 **Ostium** 的。

### 获取账户详情

检索懒人交易账户信息，包括代理状态、Telegram 连接和交易偏好设置。

### 获取可用符号

从 Ostium 交易所检索所有可交易的符号。使用这些信息来发现可以交易的符号并获取它们的 LunarCrush 数据。

### 获取 LunarCrush 市场数据

检索特定符号的缓存 LunarCrush 市场指标。这些数据包括社交媒体情绪、价格变化、波动性和市场排名。

> **⚠️ 依赖关系**：必须先调用 `/symbols` 接口以获取准确的符号字符串（例如，“BTC/USD”）。符号参数需要精确匹配。

### LunarCrush 字段描述

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `galaxy_score` | 浮点数 | 综合评分（0-100），考虑了社交媒体、市场和开发者活动 |
| `alt_rank` | 整数 | 在所有加密货币中的排名（排名越低越好，1 为最佳） |
| `social_volume_24h` | 浮点数 | 过去 24 小时的社交媒体提及量 |
| `sentiment` | 浮点数 | 市场情绪评分（0-100，50 为中性，>50 为看涨） |
| `percent_change_24h` | 浮点数 | 过去 24 小时的价格变化百分比 |
| `volatility` | 浮点数 | 价格波动性评分（0-0.02 表示稳定，0.02-0.05 表示正常，>0.05 表示风险较高） |
| `price` | 字符串 | 当前价格（以 USD 为单位，使用小数格式） |
| `volume_24h` | 字符串 | 过去 24 小时的交易量（以字符串格式） |
| `market_cap` | 字符串 | 市场资本化（以字符串格式） |
| `market_cap_rank` | 整数 | 按市场资本化排名（排名越低越好） |
| `social_dominance` | 浮点数 | 相对于总市场的社交媒体影响力 |
| `market_dominance` | 浮点数 | 相对于总市场的市场资本化占比 |
| `interactions_24h` | 浮点数 | 过去 24 小时的社交媒体互动量 |
| `galaxy_score_previous` | 浮点数 | 上一次的评分（用于趋势分析） |
| `alt_rank_previous` | 整数 | 上一次的排名（用于趋势分析） |

**数据更新频率**：
- LunarCrush 数据由后台任务定期更新
- 查看 `updated_at` 字段以了解数据最后一次更新的时间
- 数据通常每隔几小时更新一次

### 获取账户余额

检索用户 Ostium 钱包地址的 USDC 和 ETH 余额。

> **⚠️ 依赖关系**：`address` 字段是用户的 Ostium 钱包地址（`userWallet`）。必须首先从 `/club-details` 获取它 — 不要硬编码或猜测任何地址。

### 获取投资组合头寸

获取用户 Ostium 交易账户的所有未平仓头寸。**此接口非常重要** — 它返回 `tradeIndex`、`pairIndex` 和 `entryPrice`，这些信息用于平仓头寸和设置止盈/止损。

> **⚠️ 依赖关系**：`address` 字段必须来自 `/club-details` → `userWallet`。
> **🔑 此接口提供的值用于**：`/close-position`（需要 `tradeIndex`）、`/set-take-profit`（需要 `tradeIndex`、`pairIndex`、`entryPrice`）、`/set-stop-loss`（需要 `tradeIndex`、`pairIndex`、`entryPrice`）。

### 请求体示例：

```json
{
  "address": "0x...",  // 用户的 Ostium 钱包地址（必需）
  "count": 50           // 要检索的最近订单数量（默认：50）
}
```

### 响应示例：

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

### 示例请求：

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

### 响应示例：

```json
{
  "agentAddress": "0x...",      // 必需 — 来自 /club-details → ostium_agent_address。不要猜测。
  "userAddress": "0x...",       // 必需 — 来自 /club-details → user_wallet。不要猜测。
  "market": "BTC",              // 对于 Ostium，仅接受基础代币（例如 "ETH"，而不是 "ETH/USD"）。如有疑问，请通过 /symbols 验证。
  "side": "long",               // 必需 — “long” 或 “short”。询问用户。
  "collateral": 100,            // 必需 — 以 USDC 为单位。询问用户。
  "leverage": 10,               // 可选（默认：10）。询问用户。
  "deploymentId": "uuid...",    // 可选 — 相关的部署 ID
  "signalId": "uuid...",        // 可选 — 相关的交易信号 ID
  "isTestnet": false            // 可选（默认：false）
}
```

### 示例请求（平仓头寸）：

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

### 示例响应：

```json
{
  "success": true,
  "result": {
    "txHash": "0x...", \
    "market": "BTC",
    "closePnl": 25.50
  },
  "closePnl": 25.50,
  "message": "头寸已成功平仓",
  "alreadyClosed": false
}
```

### 示例请求（设置止盈）：

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

### 示例请求（设置止损）：

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
    "side": "long"
  }
```

### 其他相关请求...

### 预飞行检查清单（在每次 API 调用之前在脑海中执行）

---

## 认证

所有请求都需要一个以 `lt_` 为前缀的 API 密钥。可以通过以下方式传递：
- 标头：`X-API-KEY: lt_你的_API_key`
- 或：`Authorization: Bearer lt_你的_API_key`

## API 接口

## Ostium 程序化接口（`/api/lazy-trading/programmatic/*`）

> 除非前面有 `/aster/` 前缀，否则 `/api/lazy-trading/programmatic/*` 下的所有接口都是用于 **Ostium** 的。

### 获取账户详情

检索懒人交易账户信息，包括代理状态、Telegram 连接和交易偏好设置。

### 获取可用符号

检索 Ostium 交易所的所有可用交易符号。使用这些信息来发现可以交易的符号并获取它们的 LunarCrush 数据。

### 获取 LunarCrush 市场数据

检索特定符号的缓存 LunarCrush 市场指标。这些数据包括社交媒体情绪、价格变化、波动性和市场排名。

### 获取账户余额

检索用户 Ostium 钱包地址的 USDC 和 ETH 余额。

### 获取投资组合头寸

获取用户 Ostium 交易账户的所有未平仓头寸。**此接口非常重要** — 它返回 `tradeIndex`、`pairIndex` 和 `entryPrice`，这些信息用于平仓头寸和设置止盈/止损。

### 设置止盈/止损

请求用户交易参数 — 永远不要假设抵押品金额、杠杆、止盈百分比或止损百分比。展示默认值，但允许用户确认或修改。

### 验证市场是否存在

在交易之前，如果不确定代币在 Ostium 上是否可用，请通过调用 `/symbols` 进行验证。

### 阿尔法交易流程

遵循以下确切的顺序：`/alpha/agents` → `/alpha/listings` → `/alpha/purchase`（402）→ `/alpha/pay` → `/alpha/purchase`（使用 `X-Payment`）→ `/alpha/verify` → `/club-details` → `/alpha/execute`。不要跳过任何步骤。对于 `/alpha/verify`，请传递从购买阶段收到的 `content` 对象 — 不要修改键或值。

---

## 防错措施

- **始终首先调用 `/club-details` 以获取 `userWallet`（用作 `userAddress`）和 `ostium_agent_address`（用作 `agentAddress`），并缓存这些信息**。
- **永远不要硬编码或猜测钱包地址**。这些地址对每个用户都是唯一的，必须来自 `/club-details`。
- **开仓时**：首先获取市场数据（通过 `/lunarcrush` 或 `/market-data`），向用户展示数据，获取明确的交易参数（抵押品、杠杆、方向、止盈、止损），然后执行交易。
- **注意市场格式**：`/symbols` 返回的格式可能是 `ETH/USD`，但 `/open-position` 仅接受基础代币（例如 `ETH`）。在传递之前需要转换基础代币。
- **平仓后设置止盈/止损时**：使用 `/open-position` 响应中的 `actualTradeIndex`。如果无法获取（例如，头寸是在之前开的），则调用 `/positions` 来获取 `tradeIndex`、`pairIndex` 和 `entryPrice`。
- **关闭头寸时**：需要 `tradeIndex` — 必须首先调用 `/positions` 来查找用户指定市场的正确头寸。
- **询问用户交易参数** — 永远不要假设抵押品金额、杠杆、止盈百分比或止损百分比。展示默认值，但允许用户确认或修改。
- **在交易前验证市场是否存在**，如果不确定代币在 Ostium 上是否可用。
- **对于阿尔法交易用户**：按照以下顺序操作：`/alpha/agents` → `/alpha/listings` → `/alpha/purchase`（402）→ `/alpha/pay` → `/alpha/verify` → `/club-details` → `/alpha/execute`。不要跳过任何步骤。对于 `/alpha/verify`，请传递从购买阶段收到的 `content` 对象 — 不要修改键或值。

---

## 环境变量

| 变量 | 描述 | 示例 |
|----------|-------------|---------|
| `MAXXIT_API_KEY` | 你的懒人交易 API 密钥（以 `lt_` 为前缀） | `lt_abc123...` |
| `MAXXIT_API_URL` | Maxxit API 的基础 URL | `https://maxxit.ai` |
| `BREVIS_PROVER_URL` | Brevis 验证服务端点（空表示模拟模式，使用子图数据） | `localhost:33247` |
| `BREVIS_GATEWAY_URL` | Brevis 网关 URL | `appsdkv3.brevis.network:443` |
| `BREVIS_APP_CONTRACT` | Arbitrum Sepolia 上的 BrevisApp 合同地址（可选） | `0x...` |

## 错误处理

| 状态码 | 含义 |
|-------------|---------|
| 401 | API 密钥无效或缺失 |
| 404 | 未找到懒人交易代理（请先完成设置） |
| 400 | 消息/参数缺失或无效 |
| 405 | HTTP 方法错误 |
| 500 | 服务器错误 |

**阿尔法交易相关的错误：**
- **400**：`/pay`：未找到代理地址（用户必须完成懒人交易设置）。`/purchase`：X-Payment 标头无效或支付验证失败。
- **402**：需要支付（`/purchase` 阶段）或 USDC 余额不足（`/pay`：检查响应中的 `required` 和 `available`）。
- **409**：交易哈希已使用（防止重复购买 — 每笔交易只能购买一个列表项）。
- **410**：阿尔法列表项不再有效。

## 开始使用的方法

1. **设置懒人交易**：访问 https://maxxit.ai/lazy-trading 以连接你的钱包并配置代理。
2. **生成 API 密钥**：前往你的仪表板并创建一个 API 密钥。
3. **配置环境**：设置 `MAXXIT_API_KEY` 和 `MAXXIT_API_URL`。
4. **开始交易**：使用此功能发送交易信号！

## 安全注意事项

- **永远不要分享你的 API 密钥**。
- API 密钥可以从仪表板撤销和重新生成。
- 所有交易都在链上执行，并使用你委托的钱包权限。