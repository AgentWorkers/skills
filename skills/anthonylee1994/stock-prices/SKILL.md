---
name: stock-prices
description: 使用“Stock Prices API”查询实时股票价格和市场数据。该API适用于获取股票报价、分析市场数据，或处理如AAPL、NVDA、GOOGL等股票代码。
---

# 股票价格 API 技能

此技能可帮助您使用股票价格 API 获取实时市场数据和股票报价。

## API 端点

**基础 URL**: `https://stock-prices.on99.app`

**主要端点**: `/quotes?symbols={SYMBOLS}`

## 快速入门

获取一个或多个股票代码的报价：

```bash
curl "https://stock-prices.on99.app/quotes?symbols=NVDA"
curl "https://stock-prices.on99.app/quotes?symbols=AAPL,GOOGL,MSFT"
```

## 响应格式

API 返回的 JSON 数据结构如下：

```json
{
    "quotes": [
        {
            "symbol": "NVDA",
            "currentPrice": 188.54,
            "change": -1.5,
            "percentChange": -0.789308,
            "highPrice": 192.48,
            "lowPrice": 188.12,
            "openPrice": 191.405,
            "previousClosePrice": 190.04,
            "preMarketPrice": 191.8799,
            "preMarketChange": 3.3399048,
            "preMarketTime": "2026-02-11T13:49:16.000Z",
            "preMarketChangePercent": 1.771457
        }
    ]
}
```

## 可用的数据字段

| 字段                    | 类型              | 描述                           |
| ------------------------ | ----------------- | ------------------------------------- |
| `symbol`                 | 字符串            | 股票代码                           |
| `currentPrice`           | 数字            | 当前交易价格                         |
| `change`                 | 数字            | 相较前一收盘价的涨跌幅度                |
| `percentChange`          | 数字            | 相较前一收盘价的百分比涨跌                |
| `highPrice`              | 数字            | 当日最高价格                         |
| `lowPrice`               | 数字            | 当日最低价格                         |
| `openPrice`              | 数字            | 开盘价格                         |
| `previousClosePrice`     | 数字            | 前一交易日收盘价格                     |
| `preMarketPrice`         | 数字            | 预盘交易价格                         |
| `preMarketChange`        | 数字            | 预盘价格涨跌幅度                     |
| `preMarketTime`          | 字符串 (ISO 8601) | 预盘数据时间戳                     |
| `preMarketChangePercent` | 数字            | 预盘价格百分比涨跌                   |

## 使用指南

### 多个股票代码

通过用逗号分隔股票代码来查询多个股票（最多 50 个）：

```bash
curl "https://stock-prices.on99.app/quotes?symbols=AAPL,GOOGL,MSFT,TSLA,AMZN"
```

### 错误处理

始终检查响应是否有效：

```typescript
const response = await fetch("https://stock-prices.on99.app/quotes?symbols=NVDA");
const data = await response.json();

if (data.quotes && data.quotes.length > 0) {
    const quote = data.quotes[0];
    console.log(`${quote.symbol}: $${quote.currentPrice}`);
}
```

### 价格分析

计算常见指标：

```typescript
// Determine if stock is up or down
const isUp = quote.change > 0;
const direction = isUp ? "📈" : "📉";

// Calculate day's range percentage
const rangePct = ((quote.highPrice - quote.lowPrice) / quote.lowPrice) * 100;

// Compare current to open
const vsOpen = quote.currentPrice - quote.openPrice;
```

## 常见使用场景

### 1. 价格监控

```typescript
async function checkPrice(symbol: string) {
    const res = await fetch(`https://stock-prices.on99.app/quotes?symbols=${symbol}`);
    const data = await res.json();
    const quote = data.quotes[0];

    return {
        price: quote.currentPrice,
        change: quote.change,
        changePercent: quote.percentChange,
    };
}
```

### 2. 投资组合跟踪

```typescript
async function getPortfolio(symbols: string[]) {
    const symbolString = symbols.join(",");
    const res = await fetch(`https://stock-prices.on99.app/quotes?symbols=${symbolString}`);
    const data = await res.json();

    return data.quotes.map(q => ({
        symbol: q.symbol,
        value: q.currentPrice,
        dailyChange: q.percentChange,
    }));
}
```

### 3. 市场总结

```typescript
async function marketSummary(symbols: string[]) {
    const res = await fetch(`https://stock-prices.on99.app/quotes?symbols=${symbols.join(",")}`);
    const data = await res.json();

    const gainers = data.quotes.filter(q => q.change > 0);
    const losers = data.quotes.filter(q => q.change < 0);

    return {
        totalStocks: data.quotes.length,
        gainers: gainers.length,
        losers: losers.length,
        avgChange: data.quotes.reduce((sum, q) => sum + q.percentChange, 0) / data.quotes.length,
    };
}
```

## 热门股票代码

### 科技巨头（FAANG+）

- `AAPL` - 苹果
- `GOOGL` - 谷歌
- `META` - 脸书
- `AMZN` - 亚马逊
- `NFLX` - 纳斯达克
- `MSFT` - 微软

### 高关注度股票

- `NVDA` - 英伟达
- `TSLA` - 特斯拉
- `AMD` - 高通
- `INTC` - 英特尔
- `ORCL` | 甲骨文

### 指数

- `^GSPC` - 标普 500 指数
- `^DJI` - 道琼斯指数
- `^IXIC` - 纳斯达克指数

## 注意事项

- 所有价格均以美元计
- 市场交易时段内数据实时更新
- 提供预盘和盘后数据
- 时间戳采用 ISO 8601 格式（UTC）
- 每次请求最多支持 50 个股票代码