---
name: mkts-market-data
description: 实时市场数据、投资组合跟踪、交易记录、筛选功能，以及针对股票、加密货币、ETF、商品和外汇的新闻服务——无需API密钥即可立即使用。
metadata: {"openclaw":{"requires":{"bins":["curl"]},"optionalEnv":["MKTS_API_KEY"],"emoji":"📊"}}
---
# mkts 市场数据技能

这是一个为 AI 代理提供的完整金融工具包。您可以获取市场概览、实时报价、历史价格（OHLCV 数据）、收益日历以及来自 8 个以上来源的新闻。您可以根据价格、成交量和市值筛选资产，同时并排比较多个股票代码。您可以跟踪投资组合的损益情况、资产配置以及与基准指数的表现，并在日志中记录交易理由。无需 API 密钥即可使用市场数据功能——如需更高的请求限制，请通过编程方式注册。

**基础 URL**: `https://mkts.io/api/v1`

**认证**: 基本访问无需 API 密钥（每个 IP 每小时 20 次请求）。如需更高的请求限制，请注册免费 API 密钥，并通过请求头传递该密钥：`-H "X-API-Key: $MKTS_API_KEY"`

### 注册 API 密钥（可选）
通过编程方式获取免费 API 密钥，以提升请求限制（每小时 100 次请求）：
```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","name":"my-agent"}' \
  https://mkts.io/api/v1/register
```
返回 `{ "success": true, "data": { "apiKey": "mk_live_...", ... } }`。请保存此密钥——它仅显示一次。每个电子邮件地址最多可注册 3 个密钥。

## 端点

### 市场概览
获取全球市场统计数据（总市值、比特币占比等）：
```bash
curl -s -H "X-API-Key: $MKTS_API_KEY" https://mkts.io/api/v1/market
```

### 列出资产
获取筛选后的、分页显示的资产列表：
```bash
# All assets (default: top 50 by market cap)
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/assets"

# Filter by type
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/assets?type=stock&limit=20"

# Filter by sector
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/assets?type=stock&sector=technology"

# Search by name or symbol
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/assets?search=apple"

# Pagination and sorting
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/assets?sort=change24h&dir=desc&limit=10&offset=0"
```

查询参数：`type`（crypto|stock|etf|commodity|forex）、`sector`、`platform`、`marketType`、`search`、`limit`（1-500）、`offset`、`sort`（price|change24h|volume24h|marketCap）、`dir`（asc|desc）

### 单个资产
通过符号获取特定资产的详细信息：
```bash
curl -s -H "X-API-Key: $MKTS_API_KEY" https://mkts.io/api/v1/asset/AAPL
curl -s -H "X-API-Key: $MKTS_API_KEY" https://mkts.io/api/v1/asset/BTC
```

### 实时报价
直接从 Yahoo Finance 或 CoinGecko 获取最新报价（缓存时间为 60 秒，请求限制更严格）：
```bash
# Auto-detect source
curl -s -H "X-API-Key: $MKTS_API_KEY" https://mkts.io/api/v1/asset/AAPL/live

# Force crypto source
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/asset/bitcoin/live?type=crypto"
```

对于股票/ETF，响应中会包含扩展时段的字段：`marketState`（PRE、REGULAR、POST、CLOSED）、`preMarketPrice`、`preMarketChange`、`preMarketChangePercent`、`preMarketTime`、`postMarketPrice`、`postMarketChange`、`postMarketChangePercent`、`postMarketTime`。时间以毫秒为单位的 Unix 时间戳表示。当市场不在该时段或资产类型为 24/7 交易时，这些字段值为 `null`。

### 行情波动最大的资产
获取涨幅最大的和跌幅最大的资产：
```bash
# Both gainers and losers
curl -s -H "X-API-Key: $MKTS_API_KEY" https://mkts.io/api/v1/movers

# Just gainers, limited to crypto
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/movers?direction=gainers&type=crypto&limit=5"
```

### 筛选器
根据范围条件筛选资产：
```bash
# Stocks down more than 3%, market cap > $10B
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/screen?type=stock&maxChange=-3&minMarketCap=10000000000"

# Crypto under $1 with high volume
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/screen?type=crypto&maxPrice=1&minVolume=1000000"
```

查询参数：`type`、`sector`、`minPrice`、`maxPrice`、`minChange`、`maxChange`、`minVolume`、`maxVolume`、`minMarketCap`、`maxMarketCap`、`limit`、`offset`、`sort`、`dir`

### 行业表现
获取各行业的综合表现：
```bash
curl -s -H "X-API-Key: $MKTS_API_KEY" https://mkts.io/api/v1/sectors
```

### 比较资产
并排比较多个资产：
```bash
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/compare?symbols=AAPL,MSFT,GOOGL"
```

### 市场简报
获取适合晨间简报或代理使用的精选摘要：
```bash
curl -s -H "X-API-Key: $MKTS_API_KEY" https://mkts.io/api/v1/brief
```

返回内容：全球市场统计数据、涨幅最大的/跌幅最大的前 5 个资产、行业总结以及自然语言形式的亮点。

### 宏观指标快照
一次调用即可获取关键宏观指标（比特币、以太坊、标准普尔 500 指数、纳斯达克、黄金、石油、美元指数、VIX、10 年期国债收益率）：
```bash
curl -s -H "X-API-Key: $MKTS_API_KEY" https://mkts.io/api/v1/macro
```

返回 `{ indicators, generatedAt }`。每个指标包含 `name`、`symbol`、`price` 和 `change24h`。比特币、以太坊、标准普尔 500 指数、纳斯达克、黄金和石油的指标会在数据更新时更新；美元指数和 VIX 的指标会实时获取，并缓存 60 秒。

### 新闻
从 RSS 源获取最新的财经新闻（免费，无需额外 API 费用）：
```bash
# All news
curl -s -H "X-API-Key: $MKTS_API_KEY" https://mkts.io/api/v1/news

# Filter by category
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/news?category=crypto&limit=10"

# News for a specific symbol (searches all feeds by symbol + company name)
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/news?symbol=HOOD"
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/news?symbol=AAPL&limit=5"
```

查询参数：`category`（crypto|markets|commodities|forex）、`symbol`（按资产符号筛选——优先于类别筛选）、`limit`（1-50，默认为 20）。

返回 `{ count, news, sources }`（如果按符号筛选，则还包括 `symbol`）。每条新闻包含 `title`、`link`、`pubDate`、`source` 和 `category`。来源包括 CoinDesk、Cointelegraph、Decrypt、MarketWatch、CNBC、Investing.com、OilPrice 和 FXStreet。

### 历史价格（OHLCV）
获取任何资产的每日历史价格数据：
```bash
# Stock — full OHLCV from Yahoo Finance
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/asset/AAPL/history?range=3M"

# Crypto — close + volume from CoinGecko (max 365 days)
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/asset/BTC/history?range=1Y"
```

查询参数：`range`（1M|3M|6M|YTD|1Y，默认为 3M）。

返回 `{ symbol, range, candles, source }`。每个价格柱状图包含 `date`、`close`，以及可选的 `open`、`high`、`low`、`volume`。股票/ETF/商品数据包含完整的 OHLCV；加密货币数据仅包含收盘价和成交量。

### 收益日历
获取收益日期、每股收益预估以及最近一个季度的业绩数据：
```bash
# Real-time lookup for specific symbols (max 20)
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/earnings?symbols=AAPL,TSLA,MSFT"

# Pre-cached weekly view (no real-time Yahoo calls)
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/earnings?week=current"
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/earnings?week=next"
```

查询参数：`symbols`（用逗号分隔，最多 20 个）或 `week`（当前或下一个季度）。仅支持股票和 ETF——不支持加密货币/商品。

返回 `{ earnings }` 数组。每条记录包含 `symbol`、`name`、`earningsDate`、`earningsDates`、`epsEstimate`、`epsActual`、`revenueEstimate`、`surprisePercent` 和 `recentQuarters`（`date, actual, estimate` 的数组）。

### 股票/ETF 详情（基本面）
获取公司的全面信息：概况、财务数据、收益情况、分析师共识、股东持股情况、SEC 文件以及 ETF 持有情况：
```bash
# Stock fundamentals
curl -s -H "X-API-Key: $MKTS_API_KEY" https://mkts.io/api/v1/asset/AAPL/details

# ETF details (includes top holdings and sector weightings)
curl -s -H "X-API-Key: $MKTS_API_KEY" https://mkts.io/api/v1/asset/SPY/details
```

仅支持股票和 ETF——不支持加密货币、商品和外汇。数据通过 Yahoo Finance 实时获取，缓存时间为 60 秒（计入实时请求限制）。

返回的详细信息包括：`symbol`、`name`、`description`、`website`、`industry`、`sector`、`employees`、`headquarters`、`executives`、`trailingPE`、`forwardPE`、`dividendYield`、`beta`、`fiftyTwoWeekHigh`、`fiftyTwoWeekLow`、`targetPrice`、`recommendationKey`、`numberOfAnalysts`、`totalRevenue`、`revenueGrowth`、`grossMargins`、`operatingMargins`、`profitMargins`、`ebitda`、`returnOnAssets`、`returnOnEquity`、`totalCash`、`totalDebt`、`debtToEquity`、`freeCashflow`、`operatingCashflow`、`currentRatio`、`earningsGrowth`、`revenuePerShare`、`earningsQuarterly`、`earningsYearly`、`forwardEstimates`、`insidersPercentHeld`、`institutionsPercentHeld`、`topInstitutionalHolders`、`insiderTransactions`、`netSharePurchaseActivity`、`recommendationTrend`、`calendarEvents`、`secFilings`。ETF 还包括 `fundFamily`、`category` 和 `topHoldings`（持有情况数组、行业权重）。

### 期权链
获取股票或 ETF 的期权链数据（看涨期权、看跌期权、未平仓合约数量、隐含波动率、到期时间）：
```bash
# Default (nearest expiration)
curl -s -H "X-API-Key: $MKTS_API_KEY" https://mkts.io/api/v1/asset/AAPL/options

# Specific expiration
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/asset/AAPL/options?expiration=2026-03-21"
```

仅支持股票和 ETF——不支持加密货币、商品和外汇。数据通过 Yahoo Finance 实时获取，缓存时间为 60 秒（计入实时请求限制）。

返回 `symbol`、`expirations`（可用日期的数组）、`selectedExpiration`、`lastPrice`、`calls`、`puts` 和 `summary`（`totalCallOI`、`totalPutOI`、`putCallRatio`、`totalCallVolume`、`totalPutVolume`）。每个合约包含 `strike`、`lastPrice`、`bid`、`ask`、`change`、`percentChange`、`volume`、`openInterest`、`impliedVolatility`、`inTheMoney`、`expiration`、`contractSymbol`。

### 投资组合卡片图片
生成一张 1200×630 像素的 PNG 图片，展示投资组合概览：
```bash
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/portfolio/card?range=YTD" -o card.png
```

查询参数：`range`（1M|3M|6M|YTD|1Y，默认为 YTD）。需要 API 密钥。返回类型为 `image/png`。

卡片显示投资组合的总价值、盈亏情况（用颜色编码表示）、折线图以及按配置比例排列的顶级持仓资产。

### 查看投资组合（读取）
获取已认证用户的投资组合持有情况，包括当前价格、损益情况以及资产配置：
```bash
curl -s -H "X-API-Key: $MKTS_API_KEY" https://mkts.io/api/v1/portfolio
```

返回 `totalValue`、`totalCost`、`totalGainLoss`、`totalGainLossPercent`、`dayChange`、`dayChangePercent` 以及 `holdings` 数组。每个持仓资产包含 `symbol`、`name`、`type`、`quantity`、`avgCostBasis`、`currentPrice`、`currentValue`、`costBasis`、`gainLoss`、`gainLossPercent`、`dayChange`、`dayChangePercent` 和 `allocation`（在投资组合中的占比）。空的投资组合返回零值和空的投资组合持有数组。

### 修改投资组合
添加、删除或清除持仓资产：
```bash
# Add a holding
curl -s -X POST -H "X-API-Key: $MKTS_API_KEY" -H "Content-Type: application/json" \
  -d '{"symbol":"AAPL","name":"Apple Inc.","assetType":"stock","quantity":10,"avgCostBasis":150.00}' \
  https://mkts.io/api/v1/portfolio

# Delete a single holding by ID
curl -s -X DELETE -H "X-API-Key: $MKTS_API_KEY" \
  https://mkts.io/api/v1/portfolio/HOLDING_ID

# Clear all holdings
curl -s -X DELETE -H "X-API-Key: $MKTS_API_KEY" \
  https://mkts.io/api/v1/portfolio
```

POST 请求体参数：`symbol`（必需，大写）、`name`（必需）、`assetType`（crypto|stock|etf|commodity|forex）、`quantity`（大于 0）、`avgCostBasis`（大于等于 0）。可选参数：`purchaseDate`（ISO 格式的字符串，最多 20 个字符）、`notes`（最多 1000 个字符）。
返回创建的持仓资产的唯一标识符（由服务器生成）。

### 投资组合表现与基准比较
将您的投资组合历史表现与市场基准进行比较：
```bash
# YTD performance vs S&P 500
curl -s -H "X-API-Key: $MKTS_API_KEY" \
  "https://mkts.io/api/v1/portfolio/performance?range=YTD&benchmarks=SPY"

# 3-month performance vs S&P 500 and Bitcoin
curl -s -H "X-API-Key: $MKTS_API_KEY" \
  "https://mkts.io/api/v1/portfolio/performance?range=3M&benchmarks=SPY,BTC-USD"
```

查询参数：`range`（1M|3M|6M|YTD|1Y|ALL`、`benchmarks`（用逗号分隔，最多 4 个基准指数：标准普尔 500 指数、纳斯达克 100 指数、道琼斯工业平均指数、黄金 ETF、GLD、AGG）。

返回 `portfolio.percentChange`、`portfolio.startValue`、`portfolio.endValue`、每个基准指数的 `percentChange`，以及包含每日百分比变化的 `chartData` 数组。空的投资组合返回零值。

### 日志
记录交易理由、备注和观察结果：
```bash
# List all journal entries
curl -s -H "X-API-Key: $MKTS_API_KEY" https://mkts.io/api/v1/journal

# Create a journal entry
curl -s -X POST -H "X-API-Key: $MKTS_API_KEY" -H "Content-Type: application/json" \
  -d '{"title":"AAPL thesis","content":"Strong services growth...","symbol":"AAPL","tags":["thesis","buy"]}' \
  https://mkts.io/api/v1/journal

# Delete a journal entry
curl -s -X DELETE -H "X-API-Key: $MKTS_API_KEY" \
  https://mkts.io/api/v1/journal/ENTRY_ID
```

POST 请求体参数：`title`（必需，最多 200 个字符）、`content`（必需，最多 10000 个字符）。可选参数：`symbol`、`tags`（数组，包括：thesis、lesson、mistake、observation、buy、sell、watchlist）。
GET 请求返回 `{ count, entries }`，按最新时间排序。

### 关注列表
创建和管理资产关注列表：
```bash
# List all watchlists
curl -s -H "X-API-Key: $MKTS_API_KEY" https://mkts.io/api/v1/watchlist

# Create a watchlist (optionally with symbols)
curl -s -X POST -H "X-API-Key: $MKTS_API_KEY" -H "Content-Type: application/json" \
  -d '{"name":"Tech","symbols":["AAPL","MSFT","GOOGL"]}' \
  https://mkts.io/api/v1/watchlist

# Get a single watchlist
curl -s -H "X-API-Key: $MKTS_API_KEY" https://mkts.io/api/v1/watchlist/WATCHLIST_ID

# Update a watchlist (rename, add/remove symbols)
curl -s -X PATCH -H "X-API-Key: $MKTS_API_KEY" -H "Content-Type: application/json" \
  -d '{"name":"Big Tech","addSymbols":["AMZN"],"removeSymbols":["GOOGL"]}' \
  https://mkts.io/api/v1/watchlist/WATCHLIST_ID

# Delete a single watchlist
curl -s -X DELETE -H "X-API-Key: $MKTS_API_KEY" \
  https://mkts.io/api/v1/watchlist/WATCHLIST_ID

# Delete all watchlists
curl -s -X DELETE -H "X-API-Key: $MKTS_API_KEY" \
  https://mkts.io/api/v1/watchlist
```

POST 请求体参数：`name`（必需，最多 100 个字符）。可选参数：`symbols`（大写符号的数组）。
PATCH 请求体参数（全部为可选）：`name`、`addSymbols`（数组）、`removeSymbols`（数组）。
GET 请求返回 `{ count, watchlists }`，按最新时间排序。每个关注列表包含 `id`、`userId`、`name`、`symbols`、`createdAt`、`updatedAt`。

## 响应格式

所有响应均遵循以下结构：
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "lastUpdated": 1708721400000,
    "requestsRemaining": 94,
    "resetTime": 1708725000000
  }
}
```

### 错误代码
```json
{
  "success": false,
  "error": "Rate limit exceeded",
  "meta": { "requestsRemaining": 0, "resetTime": 1708725000000 }
}
```

## 请求限制

| 等级 | 快照端点 | 实时端点 |
|------|-------------------|----------------|
| 无 API 密钥 | 每个 IP 每小时 20 次请求 | 每个 IP 每小时 20 次请求 |
| 免费 API 密钥 | 每小时 100 次请求 | 每小时 10 次请求 |
| 高级账户 | 每小时 1,000 次请求 | 每小时 100 次请求 |

当请求超出限制时，您会收到 429 错误代码，并附带 `Retry-After` 头部字段（以秒为单位）。如需更高的请求限制，请通过 `POST /register` 注册。

## 错误处理

- **401**：API 密钥无效，或需要 API 密钥（投资组合/日志/关注列表端点）
- **404**：未找到资产
- **429**：请求超出限制——请在 `Retry-After` 时间后重试
- **500/502/503**：服务器错误——请稍后重试

### 使用自然语言查询
使用自然语言查询市场数据。需要 API 密钥。此操作计入每日 AI 使用限制（免费账户每天 5 次请求，高级账户无限制）。
```bash
# Screen for assets
curl -s -X POST -H "X-API-Key: $MKTS_API_KEY" -H "Content-Type: application/json" \
  -d '{"q":"tech stocks down more than 5%"}' \
  https://mkts.io/api/v1/ask

# Look up a single asset
curl -s -X POST -H "X-API-Key: $MKTS_API_KEY" -H "Content-Type: application/json" \
  -d '{"q":"what is bitcoin at?"}' \
  https://mkts.io/api/v1/ask

# Top movers
curl -s -X POST -H "X-API-Key: $MKTS_API_KEY" -H "Content-Type: application/json" \
  -d '{"q":"top crypto gainers today"}' \
  https://mkts.io/api/v1/ask
```

POST 请求体：`{ "q": "your question" }`（最多 500 个字符）。返回 `{ query, action, summary, results, timestamp }`。支持的操作包括：`screen`、`lookup`、`compare`、`movers`、`macro`、`brief`。查询结果缓存时间为 5 分钟。

## 代理使用提示

- **开始使用时无需 API 密钥**——市场数据端点无需认证即可使用（每个 IP 每小时 20 次请求）。如需更高的请求限制，请通过 `POST /register` 注册。
- 投资组合、日志和关注列表端点 **需要 API 密钥**——如需使用这些功能，请先注册。
- 使用 `/v1/brief` 获取晨间市场摘要——它将所有信息整合在一个请求中。
- 使用 `/v1/screen` 构建关注列表或设置警报条件。
- 当用户请求比较特定股票代码时，使用 `/v1/compare`。
- 仅当用户需要实时报价时，使用 `/v1/asset/{symbol}/live`——该端点的请求限制更严格。
- 解析 `meta_requestsRemaining` 字段以管理您的请求限制预算。
- `/v1/brief` 中的 `highlights` 数组包含预先格式化的自然语言摘要。
- 当用户询问其持有情况、损益情况或投资组合表现时，使用 `/v1/portfolio`。
- 使用 `POST /v1/portfolio` 添加持仓资产——服务器会生成唯一的 `id`，用于后续删除操作。
- 使用 `/v1/portfolio/performance?range=YTD&benchmarks=SPY` 了解“我的表现与标准普尔 500 指数相比如何”。
- 使用 `/v1/journal` 记录交易理由——附上 `symbol` 和 `tags` 以便更好地组织信息。
- 投资组合、日志和关注列表端点的响应头设置为 `Cache-Control: private, no-store`——避免缓存这些数据。
- 使用 `/v1/watchlist` 管理资产关注列表——创建列表后，可以使用 `/v1/compare` 或 `/v1/screen` 处理这些资产。
- 使用 `/v1/watchlist/{id}` 和 `addSymbols`/`removeSymbols` 管理关注列表中的资产，而无需替换整个列表。
- 使用 `/v1/news?category=crypto` 在进行交易决策前获取相关新闻标题。
- 使用 `/v1/asset/{symbol}/history` 进行技术分析——股票数据包含完整的 OHLCV，加密货币数据仅包含收盘价和成交量。
- 在收益季前使用 `/v1/earnings?symbols=AAPL` 查看每股收益预估和最近一个季度的业绩变化。
- 使用 `/v1/earnings?week=current` 快速获取每周收益日历（不计入实时请求次数）。
- 使用 `/v1/portfolio/card` 生成可分享的投资组合图片——可以使用 `-o card.png` 将图片保存到文件。
- 使用 `/v1/news?symbol=AAPL` 获取特定资产的相关新闻——按资产符号和公司名称搜索新闻。
- 使用 `/v1/macro` 快速获取宏观指标概览——一次调用即可获取比特币、以太坊、标准普尔 500 指数、纳斯达克、黄金、石油、美元指数、VIX 和 10 年期国债的指标。
- 使用 `/v1/asset/{symbol}/details` 进行深入的基本面分析——一次调用即可获取收益情况、分析师目标、股东持股情况、SEC 文件和 ETF 持有情况。
- 使用 `/v1/asset/{symbol}/options` 进行衍生品分析——获取完整的期权链数据（看涨期权、看跌期权、未平仓合约数量、隐含波动率等）。结合 `/v1/asset/{symbol}/live` 可进行Delta中性策略分析。
- 使用 `POST /v1/ask` 进行复杂的自然语言查询——系统会解析请求意图并定向到相应的数据。需要 API 密钥，并计入每日 AI 使用限制。