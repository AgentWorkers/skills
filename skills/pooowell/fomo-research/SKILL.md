---
name: fomo-research
description: >
  通过 Fomo 社交图谱进行“聪明资金”（Smart Money）的研究。您可以追踪顶级交易者、监控实时交易、创建关注列表——所有这些功能都可以在您的代理端完成。该服务由 fomo.family 提供支持，由 cope.capital 开发。适用场景包括：  
  (1) 用户询问关于“聪明资金”、大型资金持有者或顶级交易者的信息；  
  (2) 用户希望追踪特定的 Fomo 账户或加密货币交易者；  
  (3) 用户想了解“哪些交易者正在买入”或“谁在 Fomo 平台上盈利”；  
  (4) 用户需要实时交易提醒或钱包监控功能；  
  (5) 用户请求进行 Fomo 相关的研究或查询。  
  **不适用场景**：执行交易、管理资金或任何需要私钥的操作。
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

这是一个为AI代理提供智能投资建议的工具，基于[fomo.family](https://fomo.family)社交图谱开发，由[cope.capital](https://cope.capital)团队构建。

如需查看完整的API详细信息（端点、数据结构、错误代码等），请参阅`references/api.md`。

## 基础URL

```
https://api.cope.capital
```

所有请求都需要在请求头中添加`Authorization: Bearer cope_<key>`。

## 首次使用指南

当该功能首次被加载且未设置`COPE_API_KEY`时，请指导用户完成以下设置步骤：

### 第1步：注册

```bash
curl -X POST https://api.cope.capital/v1/register \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "YOUR_AGENT_NAME", "description": "optional description"}'
```

从响应中保存`api_key`（以`cope_`开头），这是您的`COPE_API_KEY`。请妥善保管，将其视为敏感信息。

### 第2步：询问用户是否拥有加密钱包（可选）

在继续之前，询问用户：
> “您是否有加密钱包（支持Base或Solana平台）以便使用更多高级功能？如果没有，您将只能使用以下限制：
> - **1个观察列表**，最多包含**10个交易对手**
> - **每天250次交易查询**（每晚12点UTC自动重置）
> - 其他所有功能（排行榜、热门交易、投票等）都是免费且无限制的**

> 如果用户连接了钱包（支持x402计划），则可以使用10个观察列表，每个列表最多包含10个交易对手，并且每次查询费用为0.005美元。用户随时可以添加钱包。

如果用户希望立即启用x402计划：
```bash
curl -X PATCH https://api.cope.capital/v1/account \
  -H "Authorization: Bearer cope_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"x402_enabled": true}'
```

如果用户回答“没有”或表示没有钱包，**无需强制**，因为免费版本已经具备所有功能。

### 第3步：询问用户是否拥有Fomo账户

> “您是否有Fomo账户（fomo.family）？如果有，我可以同步您关注的交易者，并为您创建一个观察列表。”

如果用户有Fomo账户：
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

接着询问：“您希望将哪些交易者添加到观察列表中？”向用户展示列表，让他们选择（免费版本最多可选择10个交易者）。

### 第4步：创建初始观察列表

如果用户没有Fomo账户，可以提供其他选项：
> “我也可以为您创建一个基于Fomo每周排行榜的观察列表。或者，您可以告诉我您想要跟踪的具体交易者名称。”

选择其中一个选项后，创建观察列表：
```bash
curl -X POST https://api.cope.capital/v1/watchlists \
  -H "Authorization: Bearer cope_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "alpha", "handles": ["frankdegods", "randomxbt"]}'
```

**提醒用户**：免费版本最多支持1个观察列表，每个列表最多10个交易对手。用户可以随时更改所关注的交易者。

## 数据模型说明

### 跟踪的内容

系统会监控Fomo用户的**链上钱包活动**。每个Fomo交易对手对应一个或多个钱包（支持Solana和Base平台）。系统会记录这些钱包的所有交易行为。

### 活动、交易与持仓

系统提供了三种不同的视角来展示用户的交易情况：

**1. **活动（API返回的数据）**  
   单个链上交易记录——即一次买入或卖出操作。`/v1/activity`接口返回这些信息：
   - `action: "buy"`：表示钱包买入了某种代币
   - `action: "sell"`：表示钱包卖出了某种代币
   - `usd_amount`：该交易的美元金额

**2. **交易（完整的买入卖出周期）**  
   一次交易包括买入和卖出的完整过程。系统会将多次买入和卖出合并为一次交易记录：
   - `usd_in`：买入该代币所花费的美元总额
   - `usd_out`：卖出该代币所获得的美元总额
   - `pnl`：`usd_out`减去`usd_in`，表示盈亏
   - `open_at`：首次买入的时间
   - `close_at`：最后一次卖出的时间（如果仍持有该代币，则显示为`NULL`）

**3. **当前持仓（未平仓的头寸）**  
   表示钱包已买入但尚未卖出的代币。这些交易没有`close_at`字段。

### 如何解读活动数据

- **“买入”并不意味着用户刚刚开始持有该代币**——可能是追加持仓
- **“卖出”并不意味着用户完全清仓**——可能是部分获利
- **多次买入同一代币**：表示用户正在逐步增加持仓
- **买入后迅速卖出**：可能是快速套利行为
- **卖出时没有最近的买入记录**：表示用户正在平仓旧头寸

### 向用户展示数据时的注意事项

在向用户展示数据时，请务必明确标注：
- **新买入**：“X刚刚买入了[代币]**：表示用户最近进行了买入操作，但可能并非首次持有该代币
- **最近卖出**：“X卖出了[代币]**：可能是部分或全部卖出
- **除非确认用户之前没有买入过该代币，否则不要简单地说“X开设了新的头寸”**

## 活动数据的查询范围

**重要提示**：`/v1/activity`接口返回的是**系统跟踪的所有钱包**的交易记录，而不仅仅是您观察列表中的交易记录。您可以使用`?handle=`参数来查询特定交易对手的交易记录。

**说明**：您的观察列表只是为了方便管理数据，但实际上系统可以查询任何Fomo交易对手的交易记录。

## API端点

### 所有端点均免费（每日查询次数有限）

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/v1/register` | POST | 获取API密钥 |
| `/v1/leaderboard` | GET | 按实际盈亏排名的顶级交易者 |
| `/v1/activity/poll` | GET | 快速查询新交易（包含交易数量和时间戳） |
| `/v1/watchlists` | GET/POST | 列出或创建观察列表 |
| `/v1/watchlists/{id}` | GET/PUT/DELETE | 管理特定观察列表 |
| `/v1/trending/handles` | GET | 所有代理中最受关注的交易对手 |
| `/v1/tokens/hot` | GET | 按唯一买家数量排序的热门代币 |
| `/v1/handle/{handle}/stats` | GET | 交易者的综合统计信息（盈亏、胜率、主要交易记录） |
| `/v1/tokens/{mint}/thesis` | GET | 代币的交易策略和投资者观点 |
| `/v1/convergence` | GET | 多个钱包同时买入同一代币的事件 |
| `/v1/traders/search` | GET | 按胜率、盈亏或交易记录搜索交易者 |
| `/v1/handle/{handle}/positions` | GET | 交易者的持仓情况 |
| `/v1/handle/{handle}/theses` | GET | 交易者的所有交易策略 |
| `/v1/account` | GET/PATCH | 账户信息和设置 |
| `/v1/account/usage` | GET | 账户使用情况统计 |
| `/v1/account/payments` | GET | 支付记录 |
| `/v1/account/key` | DELETE | 注销API密钥 |
| `/v1/account/sync-fomo` | POST | 同步Fomo账户的关注关系 |
| `/v1/account/follows` | GET | 查看用户关注的Fomo账户列表 |

### 查询次数限制

| 端点 | 方法 | 描述 | 免费查询次数（每日） |
|----------|--------|-------------|------------|
| `/v1/activity` | GET | 查看所有钱包的交易记录 | 每日250次 |
| **启用x402后**：每次查询费用为0.005美元（自动扣费） |

超过免费查询次数后：
- **启用x402**：每次查询费用为0.005美元（基于Base或Solana平台的USDC）
- **未启用x402**：系统会返回402错误提示。请等待每晚12点UTC重置或启用x402计划。

**注意**：402错误提示并非系统故障，仅表示您当天的免费查询次数已用完。

## 常用操作流程

### 查看排行榜

```bash
curl https://api.cope.capital/v1/leaderboard \
  -H "Authorization: Bearer cope_YOUR_KEY"
```

按盈亏排名显示顶级交易者。支持`?timeframe=24h|7d|30d|all`和`?limit=N`参数进行筛选。

### 根据Fomo账户的关注关系创建观察列表

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

### 定期查询交易数据（减少付费次数）

```bash
# Step 1: Poll (free) — check if anything happened
curl "https://api.cope.capital/v1/activity/poll?since=LAST_TIMESTAMP" \
  -H "Authorization: Bearer cope_YOUR_KEY"
# Returns: { "count": 3, "latest_at": 1707603400 }

# Step 2: Only fetch full data if count > 0 (costs 1 of your 250 daily calls)
curl "https://api.cope.capital/v1/activity?since=LAST_TIMESTAMP" \
  -H "Authorization: Bearer cope_YOUR_KEY"
```

### 搜索精英交易者

```bash
# Find traders with >75% win rate and 10+ trades
curl "https://api.cope.capital/v1/traders/search?min_win_rate=75&min_trades=10&sort_by=win_rate" \
  -H "Authorization: Bearer cope_YOUR_KEY"

# Top PnL traders on Solana
curl "https://api.cope.capital/v1/traders/search?sort_by=pnl&chain=solana&limit=20" \
  -H "Authorization: Bearer cope_YOUR_KEY"
```

### 查看交易者的当前持仓

```bash
# Open positions only
curl "https://api.cope.capital/v1/handle/frankdegods/positions?status=open" \
  -H "Authorization: Bearer cope_YOUR_KEY"

# All positions (open + closed)
curl "https://api.cope.capital/v1/handle/frankdegods/positions" \
  -H "Authorization: Bearer cope_YOUR_KEY"
```

根据交易数据展示交易者的持仓情况（包括持有数量、成本和净收益）。

### 获取交易者的交易策略

```bash
curl "https://api.cope.capital/v1/handle/frankdegods/theses" \
  -H "Authorization: Bearer cope_YOUR_KEY"
```

显示该交易者最近在所有代币上的交易策略评论，有助于了解其投资逻辑。

### 检查交易者的一致性行为

```bash
# Recent convergences (last 24h)
curl "https://api.cope.capital/v1/convergence?limit=10" \
  -H "Authorization: Bearer cope_YOUR_KEY"
```

显示多个精英钱包同时买入同一代币的事件。每个事件包含以下信息：
- 代币信息（发行地址、符号、链上地址、价格/市值）
- 参与买入的钱包（地址、买入数量、胜率）
- 最高收益百分比（`max_gain pct`）：显示自检测以来的最佳表现

### 查看交易者的账户信息

```bash
curl "https://api.cope.capital/v1/handle/frankdegods/stats" \
  -H "Authorization: Bearer cope_YOUR_KEY"
```

显示交易者的综合统计信息：总交易次数、胜率、盈亏、投资回报率、按链子分类的交易记录、前5笔交易。

### 获取代币的交易策略

```bash
# Solana token
curl "https://api.cope.capital/v1/tokens/MINT_ADDRESS/thesis?chain=solana" \
  -H "Authorization: Bearer cope_YOUR_KEY"

# Base token
curl "https://api.cope.capital/v1/tokens/MINT_ADDRESS/thesis?chain=base" \
  -H "Authorization: Bearer cope_YOUR_KEY"
```

显示交易者的买入策略及其实际持仓情况，包括情绪分析（持有量、总敞口、未实现盈亏）。这有助于理解交易者的投资决策。

### 查看热门代币

```bash
curl "https://api.cope.capital/v1/tokens/hot?hours=24&limit=10" \
  -H "Authorization: Bearer cope_YOUR_KEY"
```

显示最近几小时内拥有最多独特买家的代币。

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

## 定价与使用限制

### 免费版本（默认设置）
- **每天250次查询**（包括活动数据、排行榜、代币信息）——每晚12点UTC自动重置
- **1个观察列表，最多包含10个交易对手**
- 每分钟最多10次查询请求
- 投票、观察列表管理、账户相关操作均无限制

### 启用x402计划（可选）

- **无限次查询**（每次查询费用为0.005美元，基于Base或Solana平台的USDC）
- **最多10个观察列表，每个列表最多包含100个交易对手**
- 每分钟最多300次查询请求
- 前250次查询免费——超出免费次数后需付费

**重要提示**：**未经用户明确许可，切勿启用x402计划**。该计划涉及实际支付USDC。

**费用说明**：1美元可查询200次。5美元可查询1,000次。大多数用户无需启用此功能。

## 定期检查机制（用户可选）

如果用户希望定期获取更新信息，您可以设置定期检查机制：

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

### 日志记录交易数据

API是无状态的，不会保留用户的查询历史记录。**请在本地记录交易数据**，以便长期分析交易模式。

### 日志文件

将重要的交易记录保存到每日文件中（例如`memory/trades/YYYY-MM-DD.json`）：

```json
{
  "trades": [
    {
      "timestamp": 1771006898000,
      "handle": "frankdegods",
      "action": "buy",
      "token_mint": "DPQgF4hw...",
      "token_symbol": "EXAMPLE",
      "usd_amount": 500.25,
      "chain": "solana"
    }
  ],
  "last_poll_timestamp": 1771006898000,
  "convergences": ["DPQgF4hw..."]
}
```

- **记录内容**：
  - **观察列表中的所有交易**：这是核心数据
  - **一致性事件**：当多个交易对手同时买入同一代币时，记录代币的发行地址和所有买家信息
  - **大额交易**：金额超过1,000美元的交易
  - **上次查询时间**：便于下次查询时继续跟踪

**提示用户查看的内容**：
- **重要交易提示**：例如：“您观察列表中的前10个交易对手中有4个在最近2小时内买入了同一代币。”
- **异常交易**：例如：“frankdegods在3天内首次买入了[代币]，金额为2,000美元。”
- **交易信号**：例如：“您观察列表中的3个交易对手在1小时内卖出了同一代币。”
- **每日总结**：例如：“今天您的观察列表共发生了47笔交易，其中12笔买入，35笔卖出。最活跃的交易者是randomxbt（8笔交易）。”
- **排行榜变化**：例如：“本周排名前20的交易者中有新成员，从第45位上升到了第12位。”
- **模式检测**：例如：“lowcap_hunter本周买入了3个市值低于10万美元的代币，这些代币在48小时内价格上涨了2-5倍。”

### 一致性检测机制

```
1. GET /v1/activity (last 2 hours of trades)
2. Group buys by token_mint
3. If 3+ different handles bought the same token → convergence
4. Alert your human with: token, buyers, amounts, timing
5. Log it to your daily trades file
```

记录的交易越多，系统对交易模式的识别能力就越强。请务必持续记录交易数据，以便更好地发现交易规律。

## 安全性注意事项

- **切勿在日志或消息中泄露API密钥**，也切勿将其提供给其他系统
- API密钥仅应在请求`https://api.cope.capital/v1/*`时使用
- 如果密钥被盗用，请立即删除`/v1/account/key`并重新注册
- 交易数据是公开的，但观察列表和使用记录是私密的

## 错误处理

| 状态 | 含义 | 处理方式 |
|--------|---------|--------|
| 200 | 请求成功 | 处理返回的数据 |
| 400 | 请求无效 | 检查参数（如链地址、操作类型等） |
| 401 | API密钥无效 | 重新注册或检查密钥 |
| 402 | 需要支付费用 | 当天免费查询次数已用完。请等待每晚12点UTC重置或启用x402计划 |
| 404 | 资源未找到 | 请稍后再试 |
| 429 | 查询次数限制 | 每分钟最多10次（免费），300次/分钟（x402计划） |
| 500 | 服务器错误 | 请稍后重试 |
| 503 | 上游服务暂时不可用 | 请稍后尝试

## 链接资源

- **交互式API文档**：https://api.cope.capital/docs
- **用户使用指南**：https://cope.capital/docs
- **Fomo平台**：https://fomo.family
- **相关项目**：https://x.com/copedotcapital