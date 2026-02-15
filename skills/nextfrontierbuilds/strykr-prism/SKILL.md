---
name: strykr-prism
description: 实时金融数据API，专为AI代理设计，支持股票、加密货币、外汇及ETF等金融产品的数据查询。提供超过120个数据端点（endpoints），可作为Alpha Vantage和CoinGecko的替代方案。兼容Claude和Cursor等AI平台。
version: 1.1.1
keywords: finance-api, market-data, stock-api, crypto-api, trading-bot, real-time-data, alpha-vantage-alternative, polygon-alternative, coingecko-alternative, ai-trading, fintech, defi, ai, ai-agent, ai-coding, llm, cursor, claude, claude-code, gpt, copilot, mcp, langchain, vibe-coding, agentic, openclaw
---

# 金融数据 API (Strykr PRISM)

**一个覆盖所有市场的 API**：为 AI 代理、交易机器人和金融科技应用提供实时金融数据。

由 Strykr PRISM 提供支持——统一管理加密货币、股票、ETF、外汇、商品和 DeFi 的数据。

## 配置

设置您的 PRISM API 密钥：
```bash
export PRISM_API_KEY="your-api-key"
```

**基础 URL：** `https://strykr-prism.up.railway.app`

## 快速参考

### 🔍 资产解析（核心功能）

将任何资产标识符解析为标准格式：

```bash
# Resolve symbol (handles BTC, BTCUSD, XBT, bitcoin, etc.)
curl "$PRISM_URL/resolve/BTC"
curl "$PRISM_URL/resolve/BTCUSDT"
curl "$PRISM_URL/resolve/bitcoin"

# Natural language resolution (for agents)
curl -X POST "$PRISM_URL/agent/resolve" \
  -H "Content-Type: application/json" \
  -d '{"query": "price of ethereum"}'

# Batch resolve
curl -X POST "$PRISM_URL/resolve/batch" \
  -H "Content-Type: application/json" \
  -d '{"symbols": ["BTC", "ETH", "AAPL", "GOLD"]}'

# Find trading venues for asset
curl "$PRISM_URL/resolve/venues/BTC"
```

### 💰 价格数据

```bash
# Crypto price
curl "$PRISM_URL/crypto/price/BTC"
curl "$PRISM_URL/crypto/price/ETH"

# Batch crypto prices
curl -X POST "$PRISM_URL/batch/crypto/prices" \
  -H "Content-Type: application/json" \
  -d '{"symbols": ["BTC", "ETH", "SOL"]}'

# Stock quote
curl "$PRISM_URL/stocks/AAPL/quote"

# Batch stock quotes
curl -X POST "$PRISM_URL/stocks/batch/quotes" \
  -H "Content-Type: application/json" \
  -d '{"symbols": ["AAPL", "MSFT", "GOOGL"]}'
```

### 📊 市场概览

```bash
# Full market overview (crypto + tradfi)
curl "$PRISM_URL/market/overview"

# Crypto global stats
curl "$PRISM_URL/crypto/global"

# Fear & Greed Index
curl "$PRISM_URL/market/fear-greed"

# Trending crypto
curl "$PRISM_URL/crypto/trending"

# Stock movers
curl "$PRISM_URL/stocks/gainers"
curl "$PRISM_URL/stocks/losers"
curl "$PRISM_URL/stocks/active"
```

### 🛡️ 代币安全分析

```bash
# Analyze token for risks
curl "$PRISM_URL/analyze/BTC"

# Copycat/scam detection
curl "$PRISM_URL/analyze/copycat/PEPE"

# Check for rebrands (MATIC → POL)
curl "$PRISM_URL/analyze/rebrand/MATIC"

# Fork detection
curl "$PRISM_URL/analyze/fork/ETH"

# Holder analytics (whale concentration)
curl "$PRISM_URL/analytics/holders/0x1234..."
```

### 🔥 趋势分析与发现

```bash
# Trending crypto overall
curl "$PRISM_URL/crypto/trending"

# Solana Pump.fun bonding tokens (UNIQUE!)
curl "$PRISM_URL/crypto/trending/solana/bonding"

# Graduated from bonding curve
curl "$PRISM_URL/crypto/trending/solana/graduated"

# Trending DEX pools
curl "$PRISM_URL/crypto/trending/pools"

# EVM trending
curl "$PRISM_URL/crypto/trending/evm"

# Multi-day stock movers
curl "$PRISM_URL/stocks/multi-day-movers"
```

### 📈 DeFi 与衍生品

```bash
# DEX pairs
curl "$PRISM_URL/dex/pairs"

# Hyperliquid perps
curl "$PRISM_URL/dex/hyperliquid/pairs"
curl "$PRISM_URL/dex/hyperliquid/BTC/funding"
curl "$PRISM_URL/dex/hyperliquid/BTC/oi"

# Cross-venue funding rates
curl "$PRISM_URL/dex/BTC/funding/all"

# Cross-venue open interest
curl "$PRISM_URL/dex/BTC/oi/all"
```

### 💼 钱包与链上信息

```bash
# Wallet balances (multi-chain)
curl "$PRISM_URL/wallets/0xYourAddress/balances"

# Native balance only
curl "$PRISM_URL/wallets/0xYourAddress/native"

# Supported chains
curl "$PRISM_URL/chains"

# On-chain price
curl "$PRISM_URL/analytics/price/onchain/0xContractAddress"
```

### 🌍 传统金融

```bash
# Forex rates
curl "$PRISM_URL/forex"
curl "$PRISM_URL/forex/USD/tradeable"

# Commodities
curl "$PRISM_URL/commodities"
curl "$PRISM_URL/commodities/GOLD/tradeable"

# ETFs
curl "$PRISM_URL/etfs/popular"

# Indexes
curl "$PRISM_URL/indexes"
curl "$PRISM_URL/indexes/sp500"
curl "$PRISM_URL/indexes/nasdaq100"

# Sectors
curl "$PRISM_URL/sectors"
```

### 🔧 系统与运行状况

```bash
# API health
curl "$PRISM_URL/health"

# Data source status
curl "$PRISM_URL/crypto/sources/status"

# Registry health
curl "$PRISM_URL/registry/health"
```

## 使用场景

### 自然语言价格查询

当用户询问“比特币的价格是多少”或“ETH 的价格是多少”时：

1. 使用 `/agent/resolve` 将自然语言查询转换为标准资产标识符；
2. 使用 `/crypto/price/{symbol}` 或 `/stocks/{symbol}/quote` 获取价格信息；
3. 返回格式化后的响应结果。

### 代币安全检查

当用户询问“这个代币安全吗”或“检查代币 0x1234...” 时：

1. 使用 `/analyze/{symbol}` 进行一般性安全分析；
2. 使用 `/analyze/copycat/{symbol}` 检测代币是否为山寨币；
3. 使用 `/analytics/holders/{contract}` 分析代币持有者的集中度；
4. 返回风险评估结果。

### 市场概览

当用户询问“市场现状如何”或“当前市场趋势是什么”时：

1. 使用 `/market/overview` 获取市场整体情况；
2. 使用 `/market/fear-greed` 分析市场情绪；
3. 使用 `/crypto/trending` 查看热门加密货币；
4. 使用 `/stocks/gainers` 和 `/losers` 查看股票涨跌情况。

### 跨市场相关性分析

当用户询问“什么与比特币相关”时：

1. 使用 `/market/overview` 查看跨市场数据；
2. 比较加密货币与股票、商品、外汇之间的关联性；
3. PRISM 提供超过 120 个终端点，支持真正的跨市场分析。

## 端点响应速度参考

| 端点            | 响应速度（毫秒） | 使用场景                          |
|------------------|------------------|--------------------------------------|
| `/resolve/{symbol}`     | 140-200ms      | 解析资产标识符                        |
| `/crypto/price/{symbol}`    | 1.9-2.1s      | 单个资产价格                        |
| `/market/fear-greed`    | 229ms      | 市场情绪分析                        |
| `/crypto/trending`     | 242ms      | 热门加密货币分析                    |
| `/analyze/copycat/{symbol}` | 160ms      | 代币欺诈检测                        |
| `/stocks/{symbol}/quote`    | 214ms      | 股票价格查询                        |
| `/agent/resolve`     | 3.4s      | 自然语言查询转换                      |

## 独特数据（其他平台没有）

- `/crypto/trending/solana/bonding` —— 监测 Solana 市场的虚假宣传行为；
- `/analyze/copycat` —— 检测代币是否为山寨币或模仿品；
- `/analyze/rebrand` —— 分析代币迁移（例如 MATIC 到 POL）；
- `/dex/{symbol}/funding/all` —— 查看跨平台的融资利率。

## 示例响应结果

### 价格查询
```
User: "price of bitcoin"
Response: "Bitcoin (BTC) is $43,250 (+2.1% 24h)"
```

### 安全检查
```
User: "is PEPE safe"
Response: "🛡️ PEPE Analysis
• Risk Score: 35/100 (Low)
• Liquidity: Locked ✅
• Top holders: 15% concentration
• Copycat risk: None detected
Overall: Lower risk, but DYOR"
```

### 市场概览
```
User: "how's the market"
Response: "📊 Market Overview
Crypto: BTC $43.2K (+2%), ETH $2,290 (+1.8%)
Fear & Greed: 72 (Greed)
Trending: SOL, ONDO, WIF
Stocks: S&P +0.3%, NASDAQ +0.5%"
```

---

由 [@NextXFrontier](https://x.com/NextXFrontier) 开发