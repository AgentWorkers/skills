---
name: finnhub
description: 您可以访问Finnhub的API来获取实时股票报价、公司新闻、市场数据、财务报表以及交易信号。当您需要当前的股票价格、公司新闻、收益数据或市场分析时，可以使用该API。
homepage: https://finnhub.io
metadata:
  {
    "openclaw": {
      "emoji": "📈",
      "requires": { "env": ["FINNHUB_API_KEY"] },
      "primaryEnv": "FINNHUB_API_KEY",
    },
  }
---

# Finnhub API

通过Finnhub API，您可以获取实时和历史股票市场数据、公司新闻、财务报表以及市场指标。

## 快速入门

从 [finnhub.io](https://finnhub.io) 获取您的API密钥（免费 tier 可用）。

在 OpenClaw 中进行配置：

```json5
{
  skills: {
    entries: {
      finnhub: {
        enabled: true,
        apiKey: "your-finnhub-api-key",
        env: {
          FINNHUB_API_KEY: "your-finnhub-api-key",
        },
      },
    },
  },
}
```

或者将其添加到 `~/.openclaw/.env` 文件中：

```
FINNHUB_API_KEY=your-api-key-here
```

## API 端点

基础 URL：`https://finnhub.io/api/v1`

所有请求都需要包含 `?token=${FINNHUB_API_KEY}` 参数。

### 股票报价（实时）

获取当前股票价格：

```bash
curl "https://finnhub.io/api/v1/quote?symbol=AAPL&token=${FINNHUB_API_KEY}"
```

返回值：`c`（当前价格），`h`（最高价），`l`（最低价），`o`（开盘价），`pc`（前收盘价），`t`（时间戳）

### 公司新闻

获取最新的公司新闻：

```bash
# News for a symbol
curl "https://finnhub.io/api/v1/company-news?symbol=AAPL&from=2025-01-01&to=2025-02-01&token=${FINNHUB_API_KEY}"

# General market news
curl "https://finnhub.io/api/v1/news?category=general&token=${FINNHUB_API_KEY}"
```

### 公司概况

获取公司信息：

```bash
curl "https://finnhub.io/api/v1/stock/profile2?symbol=AAPL&token=${FINNHUB_API_KEY}"
```

### 财务报表

获取公司的财务报表：

```bash
# Income statement
curl "https://finnhub.io/api/v1/stock/financials-reported?symbol=AAPL&token=${FINNHUB_API_KEY}"

# Balance sheet
curl "https://finnhub.io/api/v1/stock/financials-reported?symbol=AAPL&statement=bs&token=${FINNHUB_API_KEY}"

# Cash flow
curl "https://finnhub.io/api/v1/stock/financials-reported?symbol=AAPL&statement=cf&token=${FINNHUB_API_KEY}"

# Search in SEC filings (10-K, 10-Q, etc.)
# Note: This endpoint may require premium tier or have a different path
curl "https://finnhub.io/api/v1/stock/search-in-filing?symbol=AAPL&query=revenue&token=${FINNHUB_API_KEY}"
```

### 市场数据

获取市场指标：

```bash
# Stock candles (OHLCV)
curl "https://finnhub.io/api/v1/stock/candle?symbol=AAPL&resolution=D&from=1609459200&to=1640995200&token=${FINNHUB_API_KEY}"

# Stock symbols (search)
curl "https://finnhub.io/api/v1/search?q=apple&token=${FINNHUB_API_KEY}"

# Market status
curl "https://finnhub.io/api/v1/stock/market-status?exchange=US&token=${FINNHUB_API_KEY}"
```

### 交易信号

获取技术指标和交易信号：

```bash
# Technical indicators (may require premium tier)
curl "https://finnhub.io/api/v1/indicator?symbol=AAPL&indicator=rsi&resolution=D&token=${FINNHUB_API_KEY}"

# Support/Resistance (may require premium tier)
curl "https://finnhub.io/api/v1/scan/support-resistance?symbol=AAPL&resolution=D&token=${FINNHUB_API_KEY}"

# Pattern recognition (may require premium tier)
curl "https://finnhub.io/api/v1/scan/pattern?symbol=AAPL&resolution=D&token=${FINNHUB_API_KEY}"
```

**注意：**部分技术指标端点可能需要高级订阅才能使用。免费 tier 提供基本的市场数据和报价。

### 收益与日历

获取收益数据：

```bash
# Earnings calendar
curl "https://finnhub.io/api/v1/calendar/earnings?from=2025-02-01&to=2025-02-28&token=${FINNHUB_API_KEY}"

# Company earnings
curl "https://finnhub.io/api/v1/stock/earnings?symbol=AAPL&token=${FINNHUB_API_KEY}"
```

## 常见使用场景

### 寻找交易机会

1. 搜索股票：`GET /search?q=关键词`
2. 获取当前报价：`GET /quote?symbol=股票代码`
3. 查看最新新闻：`GET /company-news?symbol=股票代码&from=日期&to=日期`
4. 分析技术指标：`GET /indicator?symbol=股票代码&indicator=rsi`
5. 查看财务报表：`GET /stock/financials-reported?symbol=股票代码`
6. 搜索 SEC 文件：`GET /stock/search-in-filing?symbol=股票代码&query=关键词`

### 监控股票表现

1. 获取实时报价：`GET /quote?symbol=股票代码`
2. 获取历史K线图：`GET /stock/candle?symbol=股票代码&resolution=时间分辨率`
3. 查看公司概况：`GET /stock/profile2?symbol=股票代码`
4. 查看收益报告：`GET /stock/earnings?symbol=股票代码`

### 研究公司新闻

1. 公司特定新闻：`GET /company-news?symbol=股票代码`
2. 通用市场新闻：`GET /news?category=通用`
3. 行业新闻：`GET /news?category=科技`

### 搜索 SEC 文件

在公司的 SEC 文件（10-K、10-Q、8-K 等）中搜索：

```bash
# Search for specific terms in filings
# Note: This endpoint may require premium tier or have a different path
curl "https://finnhub.io/api/v1/stock/search-in-filing?symbol=AAPL&query=revenue&token=${FINNHUB_API_KEY}"

# Search for risk factors
curl "https://finnhub.io/api/v1/stock/search-in-filing?symbol=AAPL&query=risk&token=${FINNHUB_API_KEY}"

# Search for specific financial metrics
curl "https://finnhub.io/api/v1/stock/search-in-filing?symbol=AAPL&query=EBITDA&token=${FINNHUB_API_KEY}"
```

该端点可以在公司的 SEC 文件中搜索特定关键词或短语，有助于查找官方文件中关于特定主题、风险或财务指标的提及。

## 速率限制

免费 tier：
- 每分钟 60 次 API 调用
- 实时数据访问有限
- 历史数据可获取

付费 tier 提供更高的调用次数和更多功能。

## 注意事项

- 确保在查询参数中始终包含 `token=${FINNHUB_API_KEY}`
- 使用正确的日期格式：日期范围使用 `YYYY-MM-DD`
- 时间戳为 Unix 纪元秒
- 股票代码格式：如有需要，请加上交易所前缀（例如，`US:AAPL` 表示美国股票）
- 对于纸面交易，可将 Finnhub 数据与 Alpaca API 结合使用以执行交易指令