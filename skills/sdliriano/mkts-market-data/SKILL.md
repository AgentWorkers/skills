---
name: mkts-market-data
description: 从 mkts 查询股票、加密货币、ETF 和商品的实时市场数据
metadata: {"openclaw":{"requires":{"bins":["curl"]},"optionalEnv":["MKTS_API_KEY"],"emoji":"📊"}}
---
# mkts市场数据技能

您可以使用mkts API查询股票、加密货币、ETF和商品的实时及缓存市场数据。

**基础URL**：`https://mkts.io/api/v1`

**认证**：基本访问无需API密钥（每个IP每小时20次请求）。如需更高的请求限制，请注册免费API密钥，并通过请求头传递：`-H "X-API-Key: $MKTS_API_KEY"`

### 注册API密钥（可选）
通过编程方式获取免费API密钥，以增加请求限制（每小时100次请求）：
```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","name":"my-agent"}' \
  https://mkts.io/api/v1/register
```
返回：`{"success": true, "data": {"apiKey": "mk_live_...", ... }`。请保存该密钥——它仅显示一次。每个邮箱最多可注册3个密钥。

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

查询参数：`type`（crypto|stock|etf|commodity）、`sector`、`platform`、`marketType`、`search`、`limit`（1-500）、`offset`、`sort`（price|change24h|volume24h|marketCap）、`dir`（asc|desc）

### 单个资产
通过符号获取特定资产的详细信息：
```bash
curl -s -H "X-API-Key: $MKTS_API_KEY" https://mkts.io/api/v1/asset/AAPL
curl -s -H "X-API-Key: $MKTS_API_KEY" https://mkts.io/api/v1/asset/BTC
```

### 实时报价
直接从Yahoo Finance或CoinGecko获取最新报价（缓存时间为60秒，请求限制更严格）：
```bash
# Auto-detect source
curl -s -H "X-API-Key: $MKTS_API_KEY" https://mkts.io/api/v1/asset/AAPL/live

# Force crypto source
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/asset/bitcoin/live?type=crypto"
```

### 行情波动最大的资产
获取涨幅和跌幅最大的资产：
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
获取适合晨会或代理总结的精选信息：
```bash
curl -s -H "X-API-Key: $MKTS_API_KEY" https://mkts.io/api/v1/brief
```

返回内容：全球市场统计数据、涨幅/跌幅最大的前5个资产、行业总结以及自然语言格式的亮点。

### 新闻
从RSS源获取最新的财经新闻（免费，无需额外API费用）：
```bash
# All news
curl -s -H "X-API-Key: $MKTS_API_KEY" https://mkts.io/api/v1/news

# Filter by category
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/news?category=crypto&limit=10"
```

查询参数：`category`（crypto|markets|commodities）、`limit`（1-50，默认20）。

返回：`{ count, news, sources }`。每条新闻包含`title`、`link`、`pubDate`、`source`和`category`。来源包括CoinDesk、Cointelegraph、Decrypt、MarketWatch、CNBC、Investing.com、OilPrice和FXStreet。

### 历史价格（OHLCV）
获取任何资产的每日历史价格数据：
```bash
# Stock — full OHLCV from Yahoo Finance
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/asset/AAPL/history?range=3M"

# Crypto — close + volume from CoinGecko (max 365 days)
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/asset/BTC/history?range=1Y"
```

查询参数：`range`（1M|3M|6M|YTD|1Y，默认3M）。

返回：`{ symbol, range, candles, source }`。每个价格柱包含`date`、`close`，以及可选的`open`、`high`、`low`、`volume`。股票/ETF/商品包含完整的OHLCV数据；加密货币仅包含收盘价和成交量。

### 盈利公告日历
获取盈利公告日期、每股收益估计值及最近一个季度的业绩数据：
```bash
# Real-time lookup for specific symbols (max 20)
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/earnings?symbols=AAPL,TSLA,MSFT"

# Pre-cached weekly view (no real-time Yahoo calls)
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/earnings?week=current"
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/earnings?week=next"
```

查询参数：`symbols`（用逗号分隔，最多20个）或`week`（current|next）。仅支持股票和ETF——不支持加密货币/商品。

返回：`{ earnings }`数组。每条记录包含`symbol`、`name`、`earningsDate`、`earningsDates`、`epsEstimate`、`epsActual`、`revenueEstimate`、`surprisePercent`和`recentQuarters`（`{ date, actual, estimate }`数组）。

### 投资组合卡片图片
生成一张1200×630像素的PNG图片，展示投资组合概览：
```bash
curl -s -H "X-API-Key: $MKTS_API_KEY" "https://mkts.io/api/v1/portfolio/card?range=YTD" -o card.png
```

查询参数：`range`（1M|3M|6M|YTD|1Y，默认YTD）。需要API密钥。返回类型为`image/png`的图片。

卡片显示投资组合总价值、涨跌情况（用颜色编码表示）、折线图以及主要持仓的分布情况。

### 查看投资组合
获取已认证用户的投资组合持仓情况，包括当前价格、盈亏及持仓比例：
```bash
curl -s -H "X-API-Key: $MKTS_API_KEY" https://mkts.io/api/v1/portfolio
```

返回：`totalValue`、`totalCost`、`totalGainLoss`、`totalGainLossPercent`、`dayChange`、`dayChangePercent`以及`holdings`数组。每个持仓包含`symbol`、`name`、`type`、`quantity`、`avgCostBasis`、`currentPrice`、`currentValue`、`costBasis`、`gainLoss`、`gainLossPercent`、`dayChange`、`dayChangePercent`和`allocation`（占投资组合的百分比）。空的投资组合返回零值和空数组。

### 修改投资组合
添加、删除或清除持仓：
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

POST请求体参数：`symbol`（必填，大写）、`name`（必填）、`assetType`（crypto|stock|etf|commodity）、`quantity`（大于0）、`avgCostBasis`（大于等于0）。可选参数：`purchaseDate`（ISO格式字符串，最长20个字符）、`notes`（最长1000个字符）。
返回创建的持仓记录及其生成的`id`。

### 投资组合表现与基准对比
将您的投资组合历史表现与市场基准进行对比：
```bash
# YTD performance vs S&P 500
curl -s -H "X-API-Key: $MKTS_API_KEY" \
  "https://mkts.io/api/v1/portfolio/performance?range=YTD&benchmarks=SPY"

# 3-month performance vs S&P 500 and Bitcoin
curl -s -H "X-API-Key: $MKTS_API_KEY" \
  "https://mkts.io/api/v1/portfolio/performance?range=3M&benchmarks=SPY,BTC-USD"
```

查询参数：`range`（1M|3M|6M|YTD|1Y|ALL`、`benchmarks`（用逗号分隔，最多选择4个基准：SPY、QQQ、DIA、IWM、BTC-USD、GLD、AGG）。

返回：`portfolio.percentChange`、`portfolio.startValue`、每个基准的`percentChange`，以及包含每日百分比变化的`chartData`数组。空的投资组合返回零值。

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

POST请求体参数：`title`（必填，最长200个字符）、`content`（必填，最长10000个字符）。可选参数：`symbol`、`tags`（可选标签，例如：thesis、lesson、mistake、observation、buy、sell、watchlist）。
GET请求返回：`{ count, entries }`，按最新时间排序。

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
| 无API密钥 | 每个IP每小时20次请求 | 每个IP每小时20次请求 |
| 免费API密钥 | 每小时100次请求 | 每小时10次请求 |
| 高级账户 | 每小时1000次请求 | 每小时100次请求 |

当达到请求限制时，系统会返回429错误代码，并附带`Retry-After`头部信息（以秒为单位）。如需更高请求限制，请通过`POST /register`进行注册。

## 错误处理

- **401**：API密钥无效，或需要API密钥（如portfolio/journal端点）
- **404**：资产未找到
- **429**：请求限制超出——请等待`Retry-After`时间后重试
- **500/502/503**：服务器错误——请稍后重试

## 代理使用提示

- **开始使用无需API密钥**——市场数据端点无需认证即可使用（每小时20次请求）。如需更高请求限制，请通过`POST /register`注册
- **投资组合和日志端点需要API密钥**——使用前请先注册
- 使用`/v1/brief`获取晨会市场总结——该接口可一次性获取所有信息
- 使用`/v1/screen`构建观察列表或设置提醒条件
- 当用户请求比较特定股票时，使用`/v1/compare`
- 仅当用户需要实时报价时，使用`/v1/asset/{symbol}/live`——该接口的请求限制更严格
- 解析`meta_requestsRemaining`字段以管理您的请求限制使用情况
- `/v1/brief`中的`highlights`数组包含预格式化的自然语言摘要
- 当用户询问持仓、盈亏或投资组合表现时，使用`/v1/portfolio`
- 使用`POST /v1/portfolio`添加持仓——服务器会生成`id`，用于后续删除操作
- 使用`/v1/portfolio/performance?range=YTD&benchmarks=SPY`查询“我的表现与标普500指数相比如何？”
- 使用`/v1/journal`记录交易理由——附加`symbol`和`tags`以便更好地整理信息
- 投资组合和日志端点返回`Cache-Control: private, no-store`——这些数据不允许缓存
- 使用`/v1/news?category=crypto`在交易前获取相关新闻标题
- 使用`/v1/asset/{symbol}/history`进行技术分析——股票数据包含完整的OHLCV信息，加密货币数据仅包含收盘价和成交量
- 在盈利公告季前使用`/v1/earnings?symbols=AAPL`查看每股收益估计值和最近一个季度的业绩变化
- 使用`/v1/earnings?week=current`快速获取每周盈利公告日历（无需实时API请求）
- 使用`/v1/portfolio/card`生成可分享的投资组合图片——使用`-o card.png`命令将其保存到文件