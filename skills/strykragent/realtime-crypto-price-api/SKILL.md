---
name: realtime-crypto-price-api
description: 实时加密货币价格数据API，支持比特币（Bitcoin）、以太坊（Ethereum）、Solana以及超过10,000种其他代币。提供实时价格、历史数据、热门加密货币信息，并支持批量查询功能，适用于交易机器人和仪表板开发。
---

# 实时加密货币价格 API

该 API 可获取 10,000 多种加密货币的实时价格。

## 安装

```bash
npm install realtime-crypto-price-api
```

## 使用方法

```javascript
const { CryptoPrice } = require('realtime-crypto-price-api');

const client = new CryptoPrice();

// Get Bitcoin price
const btc = await client.getPrice('BTC');
console.log(`Bitcoin: $${btc.price}`);

// Get multiple prices
const prices = await client.getPrices(['BTC', 'ETH', 'SOL']);

// Top coins by market cap
const top10 = await client.getTopCoins(10);

// Trending gainers/losers
const gainers = await client.getTrending('gainers');

// Historical OHLCV data
const history = await client.getHistory('ETH', '1d', 30);

// Search tokens
const results = await client.search('pepe');
```

## 命令行接口 (CLI)

```bash
# Single price
npx realtime-crypto-price-api BTC

# Multiple prices
npx realtime-crypto-price-api batch BTC,ETH,SOL

# Top coins
npx realtime-crypto-price-api top 20

# Trending
npx realtime-crypto-price-api trending gainers
```

## API 方法

- `getPrice(symbol)` - 获取指定加密货币的 24 小时价格变化情况
- `getPrices(symbols)` - 批量查询多种加密货币的价格
- `getTopCoins(limit)` - 按市值排名前 `limit` 位的加密货币
- `getTrending(direction)` - 获取价格上涨或下跌的加密货币列表
- `getHistory(symbol, interval)` - 获取指定加密货币的历史价格数据（OHLCV 图表）
- `search(query)` - 根据查询条件查找加密货币

## 数据来源

该 API 由 [PRISM API](https://prismapi.ai) 提供支持，数据来源于 50 多家交易所的汇总信息。