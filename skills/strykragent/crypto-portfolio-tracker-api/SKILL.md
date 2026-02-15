---
name: crypto-portfolio-tracker-api
description: 跟踪加密货币投资组合的实时价格、盈亏计算以及资产配置分析。支持查询比特币（Bitcoin）、以太坊（Ethereum）、Solana 以及超过 10,000 种代币的持有情况。
---
# 加密货币投资组合追踪器 API

该 API 可用于追踪加密货币投资组合的实时价格及盈亏情况。

## 安装

```bash
npm install crypto-portfolio-tracker-api
```

## 使用方法

```javascript
const { PortfolioTracker } = require('crypto-portfolio-tracker-api');

const tracker = new PortfolioTracker();

// Get current price
const btc = await tracker.getPrice('BTC');

// Get multiple prices
const prices = await tracker.getPrices(['BTC', 'ETH', 'SOL']);

// Track portfolio with P&L
const portfolio = await tracker.trackPortfolio([
  { symbol: 'BTC', amount: 0.5, costBasis: 30000 },
  { symbol: 'ETH', amount: 10, costBasis: 2000 }
]);

console.log(`Total: $${portfolio.totalValue}`);
console.log(`P&L: $${portfolio.totalPnL}`);
```

## 命令行接口 (CLI)

```bash
# Get price
npx crypto-portfolio-tracker-api price BTC

# Track portfolio from file
npx crypto-portfolio-tracker-api track portfolio.json
```

## API 方法

- `getPrice(symbol)` - 获取单个代币的价格
- `getPrices(symbols)` - 获取多个代币的价格
- `trackPortfolio(holdings)` - 计算投资组合的价值及盈亏

## 数据来源

本服务由 [PRISM API](https://prismapi.ai) 提供支持