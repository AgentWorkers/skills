---
emoji: 📈
name: maxxit-lazy-trading
version: 1.2.6
author: Maxxit
description: 通过 Maxxit 的 Lazy Trading API，在 Ostium 和 Aster 上执行永久性交易（即持续进行的交易）。该 API 提供了用于开仓/平仓、风险管理、获取市场数据、复制交易其他 OpenClaw 代理的程序化接口，以及一个无需信任的 Alpha Marketplace，用于买卖经过 ZK（Zcash-Kernel）验证的交易信号（这些信号来自 Arbitrum Sepolia）。
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
## Maxxit 懒人交易（Maxxit Lazy Trading）

通过 Maxxit 的懒人交易 API，在 Ostium 和 Aster DEX 上执行永久性期货交易。此技能支持通过编程接口自动化交易，用于开仓/平仓和管理风险。

### 适用场景

- 用户希望在 Ostium 上进行交易
- 用户希望在 Aster DEX 上进行交易
- 用户询问懒人交易账户的详细信息
- 用户想查看他们的 USDC/ETH 余额
- 用户想查看他们的未平仓头寸或投资组合
- 用户想查看他们的平仓历史或利润/亏损（PnL）
- 用户想了解可交易的符号
- 用户想获取市场数据或 LunarCrush 指标以供分析
- 用户想要整个市场的快照用于交易目的
- 用户想比较不同代币的排名（AltRank）
- 用户想发现高情绪价值的交易机会
- 用户想了解加密货币资产的社会媒体流量趋势
- 用户想开新的交易头寸（多头/空头）
- 用户想平仓现有的头寸
- 用户想设置或修改止盈水平
- 用户想设置或修改止损水平
- 用户想获取当前的代币/市场价格
- 用户提到“懒人交易”、“永久性合约”或“期货交易”
- 用户想自动化他们的交易流程
- 用户想复制交易或跟随其他交易者的头寸
- 用户想寻找其他 OpenClaw 代理以学习
- 用户想查看表现最佳的交易者的交易
- 用户想找到高影响力因子的交易者进行复制
- 用户想出售他们的交易信号作为“alpha”
- 用户想浏览或购买来自 ZK 验证的交易者的无信任交易

### ⚠️ DEX 路由规则（必读）

1. **如果不确定，请先询问交易所**：“您想在 Ostium 还是 Aster 上进行交易？”
2. **在回答中明确说明当前使用的交易所**（例如：“使用 Ostium...” 或 “使用 Aster...”）
3. **不要混合交易所建议**：
   - 如果用户在 **Ostium** 上交易，仅建议使用 Ostium 的接口/操作。
   - 如果用户在 **Aster** 上交易，仅建议使用 Aster 的接口/操作。
4. **不要询问网络设置**：
   - 在此设置中，**Ostium** 仅支持主网。
   - **Aster** 仅支持测试网。
   - 因此，对于任一交易所都不要询问“主网或测试网？”
5. 如果用户在对话过程中更换交易所，请确认更换后继续使用相应的交易所流程。

### ⚠️ 重要提示：API 参数规则（在调用任何接口之前请阅读）

> **切勿假设、猜测或凭空想象 API 请求参数的值。** 所有必需的参数必须来自之前的 API 响应或用户的明确输入。如果您没有所需的值，必须首先从相应的依赖接口获取它。

### 参数依赖关系图

以下显示了每个必需参数的来源。**在调用接口之前，请务必解决依赖关系。**

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
| `address`（用于复制交易者交易） | `/copy-traders` 响应 → `creatorWallet` 或 `walletAddress` | `GET /copy-traders` |
| `commitment`（Alpha） | `/alpha/agents` 响应 → `commitment` | `GET /alpha/agents` |
| `listingId`（Alpha） | `/alpha/listings` 响应 → `listingId` | `GET /alpha/listings` |
| `alpha`, `contentHash`（Alpha） | `/alpha/purchase` 第二阶段响应 → `alpha`, `contentHash` | `GET /alpha/purchase` + `X-Payment` 标头 |
| `txHash`（Alpha） | `/alpha/pay` 响应 → `txHash` | `POST /alpha/pay` |

### 必须遵循的工作流程规则

1. **始终首先调用 `/club-details` 以获取 `userWallet`（用作 `userAddress`/`address`）和 `ostium_agent_address`（用作 `agentAddress`）。将这些信息缓存起来，因为它们在会话期间不会改变。**
2. **切勿硬编码或猜测钱包地址。** 它们对每个用户都是唯一的，必须来自 `/club-details`。
3. **开仓时**：首先获取市场数据（通过 `/lunarcrush` 或 `/market-data`），向用户展示数据，获取明确的交易参数（抵押品、杠杆、方向、止盈、止损），然后执行交易。
   - **市场格式规则（Ostium）**：`/symbols` 返回的配对格式如 `ETH/USD`，但 `/open-position` 仅期望以基础代币表示（例如 `ETH`）。在调用之前将基础代币转换过来。
4. **开仓后设置止盈/止损时**：使用 `/open-position` 响应中的 `actualTradeIndex`。如果不存在（例如，头寸是在之前开的），请调用 `/positions` 来获取 `tradeIndex`、`pairIndex` 和 `entryPrice`。
5. **平仓头寸时**：您需要 `tradeIndex` —— 必须首先调用 `/positions` 来查找用户指定市场的正确头寸。
6. **询问用户交易参数** —— 切勿假设抵押品金额、杠杆、止盈百分比或止损百分比。展示默认值，但允许用户确认或覆盖它们。
7. **在交易之前，如果不确定某个代币是否在 Ostium 上可用，请通过调用 `/symbols` 来验证市场是否存在。**
8. **对于 Alpha 消费者流程**：严格按照以下顺序操作：`/alpha/agents` → `/alpha/listings` → `/alpha/purchase` → `/alpha/pay` → `/alpha/purchase` → `/alpha/verify` → `/club-details` → `/alpha/execute`。切勿跳过任何步骤。对于 `/alpha/verify`，请传递从购买中收到的 `content` 对象 —— 不要修改键或值。

### 在每次 API 调用之前请在心中默记以下步骤

---

## 认证

所有请求都需要一个以 `lt_` 为前缀的 API 密钥。通过以下方式传递它：
- 标头：`X-API-KEY: lt_你的_API_key`
- 或者：`Authorization: Bearer lt_你的_API_key`

## API 接口

### Ostium 程序化接口（`/api/lazy-trading/programmatic/*`）

> 除非前面有 `/aster/` 前缀，否则 `/api/lazy-trading/programmatic/*` 下的所有接口都是用于 **Ostium** 的。

### 获取账户详细信息

检索懒人交易账户信息，包括代理状态、Telegram 连接和交易偏好。

### 获取可用符号

从 Ostium 交易所检索所有可交易的符号。使用这些信息来发现可以交易的符号并获取 LunarCrush 数据。

### 获取 LunarCrush 市场数据

检索特定符号的缓存 LunarCrush 市场指标。这些数据包括社会情绪、价格变化、波动性和市场排名。

### LunarCrush 字段描述

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `galaxy_score` | 浮点数 | 综合社会、市场和开发者活动的代币质量得分（0-100） |
| `alt_rank` | 整数 | 在所有加密货币中的排名（排名越低越好，1 为最佳） |
| `social_volume_24h` | 浮点数 | 过去 24 小时的社交媒体提及量 |
| `sentiment` | 浮点数 | 市场情绪得分（0-100，50 为中性，>50 为看涨） |
| `percent_change_24h` | 浮点数 | 过去 24 小时的价格变化百分比 |
| `volatility` | 浮点数 | 价格波动性得分（0-0.02 表示稳定，0.02-0.05 表示正常，>0.05 表示风险） |
| `price` | 字符串 | 当前价格（以美元表示，使用小数格式） |
| `volume_24h` | 字符串 | 过去 24 小时的交易量（以字符串表示） |
| `market_cap` | 字符串 | 市场资本化（以字符串表示） |
| `market_cap_rank` | 整数 | 按市场资本化排名的顺序（排名越低越好） |
| `social_dominance` | 浮点数 | 相对于总市场的社交媒体流量 |
| `market_dominance` | 浮点数 | 相对于总市场的市场资本化 |
| `interactions_24h` | 浮点数 | 过去 24 小时的社交媒体互动量 |
| `galaxy_score_previous` | 浮点数 | 上一次的银河得分（用于趋势分析） |
| `alt_rank_previous` | 整数 | 上一次的代币排名（用于趋势分析） |

**数据更新频率：**
- LunarCrush 数据由后台工作进程定期缓存和更新
- 查看 `updated_at` 字段以了解数据上次更新的时间
- 数据通常每隔几小时更新一次

### 获取账户余额

检索用户 Ostium 钱包地址的 USDC 和 ETH 余额。

### 获取投资组合头寸

获取用户 Ostium 交易账户的所有未平仓头寸。**此接口非常重要** —— 它返回 `tradeIndex`、`pairIndex` 和 `entryPrice`，这些信息是平仓头寸和设置止盈/止损所必需的。

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

```bash
curl -L -X POST "${MAXXIT_API_URL}/api/lazy-trading/programmatic/open-position" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "agentAddress": "0x...", \
    "userAddress": "0x...", \
    "market": "BTC", \
    "side": "long", \
    "collateral": 100, \
    "leverage": 10
}
```

### 响应示例：

```json
{
  "agentAddress": "0x...",      // 必需 —— 来自 /club-details → ostium_agent_address。切勿猜测。
  "userAddress": "0x...",       // 必需 —— 来自 /club-details → user_wallet。切勿猜测。
  "market": "BTC",              // 对于 Ostium，仅允许使用基础代币（例如 "ETH"，而不是 "ETH/USD"。如果不确定，请通过 /symbols 验证）。
  "side": "long",               // 必需 —— “long” 或 “short”。询问用户。
  "collateral": 100,            // 必需 —— 以 USDC 为单位表示的抵押品。询问用户。
  "leverage": 10,               // 可选（默认：10）。询问用户。
  "deploymentId": "uuid...",    // 可选 —— 相关的部署 ID
  "signalId": "uuid...",        // 可选 —— 相关的信号 ID
  "isTestnet": false            // 可选（默认：false）
}
```

### 其他相关操作

---