---
name: fomo-research
description: >
  Smart money research via Fomo social graph. Track top traders, monitor live trades,
  build watchlists — all from your agent. Powered by fomo.family, built by cope.capital.
  Use when: (1) user asks about smart money, whale wallets, or top traders,
  (2) user wants to track specific Fomo handles or crypto traders,
  (3) user asks "what are the best traders buying", "who's profitable on fomo",
  (4) user wants real-time trade alerts or wallet monitoring,
  (5) user says "fomo research", "check fomo", "smart money", "wallet tracker".
  NOT for: executing trades, managing funds, or anything requiring private keys.
homepage: https://cope.capital
source: https://github.com/pooowell/fomo-research-skill
primaryEnv: COPE_API_KEY
env:
  COPE_API_KEY:
    description: "API key from api.cope.capital (starts with cope_). You get this by registering — see Setup step 1."
    required: true
    obtain: "POST https://api.cope.capital/v1/register with {agent_name, description}"
---

# Fomo Research

这是一个为AI代理提供的智能资金分析工具，基于[cope.capital](https://cope.capital)开发的[fomo.family](https://fomo.family)社交图谱技术。

如需查看完整的API详情（端点、数据结构、错误代码等），请参阅`references/api.md`。

## 基本URL

```
https://api.cope.capital
```

所有请求都需要在请求头中添加`Authorization: Bearer cope_<key>`。

## 首次使用指南

当此功能首次被加载且未设置`COPE_API_KEY`时，需指导用户完成以下设置步骤：

### 第1步：注册

```bash
curl -X POST https://api.cope.capital/v1/register \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "YOUR_AGENT_NAME", "description": "optional description"}'
```

从响应中保存`api_key`（以`cope_`开头），这将是您的`COPE_API_KEY`。请妥善保管，将其视为敏感信息。

### 第2步：询问是否拥有加密货币钱包（可选）

在继续之前，询问用户：
> “您是否有加密货币钱包（支持Base或Solana网络）以便使用更多高级功能？如果没有钱包，您将只能使用以下限制：
> - **1个观察列表**，最多包含**10个交易对手**
> - **每天250次交易查询**（数据在UTC时间午夜重置）
> - 其他所有功能（排行榜、热门交易、实时监控等）都是免费且无限制的**

> 如果用户连接了钱包（支持x402），则可以使用10个观察列表，每个列表最多包含10个交易对手，并且每次查询费用为0.005美元。用户随时可以添加钱包。

如果用户希望立即启用x402功能，请执行以下操作：
```bash
curl -X PATCH https://api.cope.capital/v1/account \
  -H "Authorization: Bearer cope_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"x402_enabled": true}'
```

如果用户表示没有钱包或不需要该功能，**无需强制**，免费版本已经可以满足所有需求。

### 第3步：询问用户是否拥有Fomo账户

> “您是否有Fomo账户（fomo.family）？如果有，我可以同步您关注的交易对手并为您生成观察列表。”

如果用户有Fomo账户，请继续下一步：
```bash
# Sync their profile
curl -X POST https://api.cope.capital/v1/account/sync-fomo \
  -H "Authorization: Bearer cope_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"fomo_handle": "THEIR_FOMO_USERNAME"}'

# Pull their follows
curl https://api.cope.capital/v1/account/follows \
  -H "Authorization: Bearer cope_YOUR_KEY"
```

然后询问：“您希望将哪些交易对手添加到观察列表中？”向用户展示列表，让他们进行选择（免费版本最多支持10个交易对手）。

### 第4步：创建初始观察列表

如果用户没有Fomo账户，可以提供其他选择：
> “我也可以为您生成一个基于Fomo每周排行榜的观察列表。或者您可以直接提供想要跟踪的交易对手的ID。”

根据用户的选择，创建相应的观察列表：
```bash
curl -X POST https://api.cope.capital/v1/watchlists \
  -H "Authorization: Bearer cope_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "alpha", "handles": ["frankdegods", "randomxbt"]}'
```

**提醒**：免费版本最多支持1个观察列表，每个列表最多10个交易对手。用户可以随时更换交易对手。

## 数据模型说明

### 跟踪的内容

系统会监控Fomo用户的**链上钱包活动**。每个Fomo交易对手对应一个或多个钱包（支持Solana和Base网络）。系统会记录这些钱包的所有交易行为。

### 交易、操作与持仓的区分

系统提供了三种不同的数据视图来展示用户的交易行为：

**1. **操作（API返回的数据）**  
   单个链上交易记录——即一次买入或卖出操作。`/v1/activity`接口返回的信息包括：
   - `action: "buy"`：表示钱包买入了某种代币
   - `action: "sell"`：表示钱包卖出了某种代币
   - `usd_amount`：该交易的美元金额

**2. **完整交易（买入-卖出循环）**  
   一次完整的交易包括买入和卖出两个操作。系统会将多次买入和卖出合并为一次交易记录：
   - `usd_in`：买入该代币所花费的美元总额
   - `usd_out`：卖出该代币所获得的美元总额
   - `pnl`：`usd_out`减去`usd_in`，表示盈亏
   - `open_at`：首次买入的时间
   - `close_at`：最后一次卖出的时间（如果仍持有该代币，则`close_at`为`NULL`）

**3. **当前持仓（未平仓的交易）**  
   表示钱包已买入但尚未完全卖出的代币。这类交易没有`close_at`字段。

### 如何解读交易数据

- **买入操作**并不一定意味着用户开始新的持仓；
- **卖出操作**也不一定意味着用户完全退出持仓；
- **多次买入同一代币**可能表示用户正在逐步增加持仓；
- **买入后迅速卖出**可能表示用户在进行快速套利；
- **卖出时没有之前的买入记录**可能表示用户正在平仓旧持仓。

### 向用户展示数据时的注意事项

在展示数据时，请务必明确标注：
- **新买入**：例如：“X刚刚买入了[代币]”——表示最近的一次买入操作，但不一定代表新持仓的开始；
- **最近卖出**：例如：“X卖出了[代币]”——可能是部分或全部卖出；
- **除非确认用户之前没有买入过该代币，否则不要简单地说“X建立了新的持仓”。

## 数据查询范围

**重要说明**：`/v1/activity`接口返回的是系统监控的所有钱包的最新交易记录，而不仅仅是您关注的交易对手的交易记录。您可以使用`?handle=`参数来查询特定交易对手的交易记录。

```bash
# Check what frankdegods is buying (uses 1 of your 250 daily calls)
curl "https://api.cope.capital/v1/activity?handle=frankdegods&action=buy" \
  -H "Authorization: Bearer cope_YOUR_KEY"
```

观察列表只是为了方便您整理数据——实际上，所有被监控的交易对手的交易记录都是可查询的。

## API端点

### 所有接口均为免费（每日查询次数无限制）

| 端点 | 方法 | 功能描述 |
|----------|--------|-------------|
| `/v1/register` | POST | 获取API密钥 |
| `/v1/leaderboard` | GET | 按真实盈亏排名的顶级交易者 |
| `/v1/activity/poll` | GET | 快速查询最新交易（包括交易数量和时间戳） |
| `/v1/watchlists` | GET/POST | 列出或创建观察列表 |
| `/v1/watchlists/{id}` | GET/PUT/DELETE | 管理特定观察列表 |
| `/v1/trending/handles` | GET | 所有代理中关注度最高的交易对手 |
| `/v1/account` | GET/PATCH | 账户信息和设置 |
| `/v1/account/usage` | GET | 账户使用情况统计 |
| `/v1/account/payments` | GET | 支付记录 |
| `/v1/account/key` | DELETE | 注销API密钥 |
| `/v1/account/sync-fomo` | POST | 同步Fomo账户的关注信息 |
| `/v1/account/follows` | GET | 查看用户关注的Fomo交易对手列表 |

### 查询次数限制

| 端点 | 方法 | 功能描述 | x402版本费用 |
|----------|--------|-------------|------------|
| `/v1/activity` | GET | 查看被监控钱包的完整交易记录 | 每次查询0.005美元 |

免费版本每天允许查询250次。超过这个次数后：
- **启用x402版本**：每次查询费用为0.005美元（自动扣费）；
- **未启用x402版本**：系统会返回402错误提示，需等待UTC时间午夜重置或手动启用x402版本。

注意：402错误提示并非系统故障，仅表示免费查询次数已用完。

## 常见操作流程

### 查看排行榜

```bash
curl https://api.cope.capital/v1/leaderboard \
  -H "Authorization: Bearer cope_YOUR_KEY"
```

根据盈亏排名显示顶级交易者。支持`?timeframe=24h|7d|30d|all`和`?limit=N`参数来调整查询时间范围。

### 根据Fomo账户关注的交易对手生成观察列表

```bash
# 1. Sync your Fomo profile
curl -X POST https://api.cope.capital/v1/account/sync-fomo \
  -H "Authorization: Bearer cope_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"fomo_handle": "your_handle"}'

# 2. See your follows
curl https://api.cope.capital/v1/account/follows \
  -H "Authorization: Bearer cope_YOUR_KEY"

# 3. Create a watchlist with selected handles
curl -X POST https://api.cope.capital/v1/watchlists \
  -H "Authorization: Bearer cope_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "alpha", "handles": ["frankdegods", "randomxbt"]}'
```

### 定时查询交易数据（减少付费次数）

```bash
# Step 1: Poll (free) — check if anything happened
curl "https://api.cope.capital/v1/activity/poll?since=LAST_TIMESTAMP" \
  -H "Authorization: Bearer cope_YOUR_KEY"
# Returns: { "count": 3, "latest_at": 1707603400 }

# Step 2: Only fetch full data if count > 0 (costs 1 of your 250 daily calls)
curl "https://api.cope.capital/v1/activity?since=LAST_TIMESTAMP" \
  -H "Authorization: Bearer cope_YOUR_KEY"
```

### 过滤交易数据

```bash
# By handle
curl "https://api.cope.capital/v1/activity?handle=frankdegods" \
  -H "Authorization: Bearer cope_YOUR_KEY"

# By chain
curl "https://api.cope.capital/v1/activity?chain=solana" \
  -H "Authorization: Bearer cope_YOUR_KEY"

# By action
curl "https://api.cope.capital/v1/activity?action=buy" \
  -H "Authorization: Bearer cope_YOUR_KEY"

# By minimum size
curl "https://api.cope.capital/v1/activity?min_usd=1000" \
  -H "Authorization: Bearer cope_YOUR_KEY"
```

## 价格与使用限制

### 免费版本（默认设置）
- **每天250次查询**（包括交易数据、排行榜信息等）——数据在UTC时间午夜重置
- **1个观察列表，最多包含10个交易对手**
- 每分钟最多10次查询请求
- 实时监控、观察列表管理、账户相关操作等均无限制

### 启用x402版本（可选）

- **无限次查询**（每次查询费用为0.005美元，支持Base或Solana网络）
- **最多10个观察列表，每个列表最多包含10个交易对手**
- 每分钟最多300次查询请求
- 前250次查询免费；超出免费次数后需付费

### 注意：**切勿在未经用户明确许可的情况下启用x402版本**。该版本需要用户使用真实的USDC进行支付。

```bash
curl -X PATCH https://api.cope.capital/v1/account \
  -H "Authorization: Bearer cope_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"x402_enabled": true}'
```

x402版本完全是可选的。只有在以下情况下才建议启用：
- 用户每天查询次数超过250次；
- 用户需要多个观察列表或更多交易对手；
- 用户明确表示希望升级功能。

**费用说明**：1美元可查询200次；5美元可查询1,000次。大多数用户无需使用此功能。

## 定期数据更新（用户可自定义）

如果用户希望系统定期更新数据，可以设置定时检查机制：
```
Every 5-15 minutes:
  1. GET /v1/activity/poll?since=LAST_TIMESTAMP  (free, doesn't count)
  2. If count > 0 → GET /v1/activity?since=LAST_TIMESTAMP  (1 daily call)
  3. Store latest_at for next poll

Every few hours:
  1. GET /v1/leaderboard  (1 daily call)
  2. Compare to previous — any new names in top 50?

Daily:
  1. GET /v1/account/usage  (free)
  2. Check remaining daily calls
```

### 交易数据的持久化存储

API是无状态的，不会保留用户的查询历史记录。建议用户将交易数据本地保存（例如保存到`memory/trades/YYYY-MM-DD.json`文件中），以便长期分析交易模式。

### 日志记录

- **记录所有观察列表中的交易**：这是核心数据来源；
- **当多个交易对手同时买入同一代币时**，记录该代币的发行信息和所有买入者；
- **金额较大的交易**（超过1,000美元的交易）也需要记录；
- **记录上次查询的时间戳**，以便下次查询时能从上次记录继续查询。

### 数据展示建议

在向用户展示数据时，请进行以下处理：
- **新买入**：例如：“X刚刚买入了[代币]”——仅说明最近的一次买入操作；
- **最近卖出**：例如：“X卖出了[代币]”——说明可能是部分或全部卖出；
- **避免直接说“用户建立了新的持仓”，除非能确认用户之前确实没有买入过该代币。

## 数据查询范围说明

**重要提示**：`/v1/activity`接口返回的是所有被监控钱包的交易记录，而不仅仅是您关注的交易对手的交易记录。您可以使用`?handle=`参数来查询特定交易对手的交易记录。

```bash
# Check what frankdegods is buying (uses 1 of your 250 daily calls)
curl "https://api.cope.capital/v1/activity?handle=frankdegods&action=buy" \
  -H "Authorization: Bearer cope_YOUR_KEY"
```

观察列表只是为了帮助您更方便地整理数据——实际上，所有被监控的交易对手的交易记录都是可查询的。

## 其他注意事项

- **免费版本每天允许250次查询**；
- 超过这个次数后，每次查询费用为0.005美元（x402版本）；
- 402错误提示表示免费查询次数已用完，需等待UTC时间午夜重置或手动启用x402版本。

### 常见操作流程

- **查看排行榜**：查看Fomo平台的顶级交易者（支持时间范围和查询数量限制）；
- **根据用户关注的交易对手生成观察列表**；
- **定期查询交易数据**（以减少付费次数）；
- **过滤交易数据**以优化查询效率。

## 安全注意事项

- **切勿在日志、消息或其他系统中泄露API密钥**；
- API密钥仅应在请求`https://api.cope.capital/v1/*`时使用；
- 如果密钥被盗用，请通过`DELETE /v1/account/key`删除密钥并重新注册；
- 交易数据是公开可见的，但观察列表和使用数据是私密的。

## 错误处理

| 状态码 | 含义 | 处理方式 |
|--------|---------|--------|
| 200 | 请求成功 | 处理返回的结果 |
| 400 | 请求无效 | 检查请求参数（如链路信息、操作类型等） |
| 401 | API密钥无效 | 重新注册或检查密钥 |
| 402 | 需要支付费用 | 免费查询次数已用完。等待UTC时间午夜重置或手动启用x402版本（正常情况） |
| 404 | 资源未找到 | 请求的资源不存在 |
| 429 | 查询次数受限 | 每分钟最多10次（免费版本）/300次（x402版本） |
| 500 | 服务器错误 | 请稍后重试 |
| 503 | 上游服务暂时不可用 | 请稍后尝试 |

## 相关链接

- **交互式API文档**：https://api.cope.capital/docs |
- **用户使用指南**：https://cope.capital/docs |
- **Fomo平台**：https://fomo.family |
- **其他相关服务**：https://x.com/copedotcapital