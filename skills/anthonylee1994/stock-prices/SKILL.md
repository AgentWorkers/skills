---
name: stock-prices
description: 使用 Stock Prices API 查询实时股票价格和市场数据。响应数据采用 TOON 格式，可以使用 @toon-format/toon 进行解码。适用于获取股票报价、分析市场数据，或处理如 AAPL、NVDA、GOOGL 等股票代码。
---
# 股票价格 API 技能

该技能可帮助您使用股票价格 API 获取实时市场数据和股票报价。

## API 端点

**基础 URL**：`https://stock-prices.on99.app`

**主要端点**：`/quotes?symbols={SYMBOLS}`

## 快速入门

查询一个或多个股票的价格（响应格式为 TOON）：

```bash
curl "https://stock-prices.on99.app/quotes?symbols=NVDA"
curl "https://stock-prices.on99.app/quotes?symbols=AAPL,GOOGL,MSFT"
```

请安装 `@toon-format/toon` 解码器以解析 TOON 格式的数据：`pnpm add @toon-format/toon`

## 响应格式

API 返回的数据采用 **TOON**（Token-Oriented Object Notation，面向令牌的对象表示法）格式——这种格式比 JSON 更紧凑、更易于阅读，使用的令牌数量仅约为 JSON 的 40%。因此，它非常适合用于大型语言模型（LLM）的提示和数据流处理。

### TOON 响应示例

```
quotes[1]{symbol,currentPrice,change,percentChange,highPrice,lowPrice,openPrice,previousClosePrice,preMarketPrice,preMarketChange,preMarketTime,preMarketChangePercent,...}:
  NVDA,188.54,-1.5,-0.789308,192.48,188.12,191.405,190.04,191.8799,3.3399048,2026-02-11T13:49:16.000Z,1.771457,...
```

### 解码 TOON 响应

使用 `@toon-format/toon` 将响应解析为 JavaScript/JSON 格式：

```typescript
import { decode } from "@toon-format/toon";

const response = await fetch("https://stock-prices.on99.app/quotes?symbols=NVDA");
const toonText = await response.text();
const data = decode(toonText);

// data.quotes is an array of quote objects
const quote = data.quotes[0];
console.log(`${quote.symbol}: $${quote.currentPrice}`);
```

解析后的数据结构与 JSON 相同，包括对象、数组和基本数据类型。

## 可用的数据字段

| 字段                    | 类型              | 描述                           |
| ------------------------ | ----------------- | ------------------------------------- |
| `symbol`                 | 字符串            | 股票代码                         |
| `currentPrice`           | 数字            | 当前交易价格                     |
| `change`                 | 数字            | 相较前一收盘价的涨跌幅度              |
| `percentChange`          | 数字            | 相较前一收盘价的百分比涨跌              |
| `highPrice`              | 数字            | 当日最高价格                     |
| `lowPrice`               | 数字            | 当日最低价格                     |
| `openPrice`              | 数字            | 开盘价格                       |
| `previousClosePrice`     | 数字            | 前一交易日收盘价格                 |
| `preMarketPrice`         | 数字            | 预交易价格                     |
| `preMarketChange`        | 数字            | 预交易价格涨跌幅度                 |
| `preMarketTime`          | 字符串 (ISO 8601)     | 预交易时间戳                     |
| `preMarketChangePercent` | 数字            | 预交易价格百分比涨跌                 |

## 使用指南

### 多个股票

通过逗号分隔股票代码来查询多个股票（最多支持 50 个股票）：

```bash
curl "https://stock-prices.on99.app/quotes?symbols=AAPL,GOOGL,MSFT,TSLA,AMZN"
```

### 错误处理

在访问数据之前，请务必检查响应是否有效，并使用 `@toon-format/toon` 解码 TOON 格式的数据：

```typescript
import { decode } from "@toon-format/toon";

const response = await fetch("https://stock-prices.on99.app/quotes?symbols=NVDA");
const data = decode(await response.text());

if (data.quotes && data.quotes.length > 0) {
    const quote = data.quotes[0];
    console.log(`${quote.symbol}: $${quote.currentPrice}`);
}
```

### 价格分析

可以计算一些常见的价格指标：

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
import { decode } from "@toon-format/toon";

async function checkPrice(symbol: string) {
    const res = await fetch(`https://stock-prices.on99.app/quotes?symbols=${symbol}`);
    const data = decode(await res.text());
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
import { decode } from "@toon-format/toon";

async function getPortfolio(symbols: string[]) {
    const symbolString = symbols.join(",");
    const res = await fetch(`https://stock-prices.on99.app/quotes?symbols=${symbolString}`);
    const data = decode(await res.text());

    return data.quotes.map(q => ({
        symbol: q.symbol,
        value: q.currentPrice,
        dailyChange: q.percentChange,
    }));
}
```

### 3. 市场总结

```typescript
import { decode } from "@toon-format/toon";

async function marketSummary(symbols: string[]) {
    const res = await fetch(`https://stock-prices.on99.app/quotes?symbols=${symbols.join(",")}`);
    const data = decode(await res.text());

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

## 流行的股票代码

### 科技巨头（FAANG+）

- `AAPL` - 苹果
- `GOOGL` - 谷歌
- `META` - 脸书
- `AMZN` - 亚马逊
- `NFLX` - 纳斯达克
- `MSFT` - 微软

### 热门股票

- `NVDA` - 英伟达
- `TSLA` - 特斯拉
- `AMD` - 高通
- `INTC` - 英特尔
- `ORCL` - 甲骨文

### 指数

- `^GSPC` - 标普 500 指数
- `^DJI` - 道琼斯指数
- `^IXIC` - 纳斯达克指数

## 注意事项

- **响应格式**：API 返回的数据格式为 TOON，而非 JSON。请使用 `@toon-format/toon` 的 `decode()` 函数进行解析。
- 所有价格均以美元计价。
- 市场交易时段内数据会实时更新。
- 提供预交易时间和盘后时间的数据。
- 时间戳采用 ISO 8601 格式（UTC）。
- 每次请求最多支持查询 50 个股票代码。