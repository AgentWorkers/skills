---
name: claw402
description: >
  通过 x402 微支付获取专业市场数据和 AI API 服务——无需 API 密钥、无需注册、无需订阅。使用 USDC 在 Base 平台上按调用次数付费。提供超过 215 个终端点，涵盖 12 个服务提供商：  
  - 加密市场数据（CoinAnk 衍生品分析、nofxos.ai AI 信号、CoinMarketCap 的报价/列表/DEX/MCP）  
  - 美国股票和期权（Alpaca、Polygon、Alpha Vantage）  
  - 中国 A 股（Tushare）  
  - 外汇和全球时间序列数据（Twelve Data）  
  - AI 推理服务（GPT-4o、Claude、DeepSeek V3/Reasoner、Qwen3-Max/Plus/Turbo/Flash/Coder/VL）  
  只需一个钱包，即可立即访问所有付费 API——无需任何注册手续。
version: 1.3.0
metadata:
  openclaw:
    emoji: "⚡"
    homepage: https://claw402.ai
    requires:
      env: [WALLET_PRIVATE_KEY]
    primaryEnv: WALLET_PRIVATE_KEY
    install:
      - kind: node
        package: NoFxAiOS/claw402-js
        bins: []
---
# ⚡ claw402 — 按次付费的市场数据与AI API服务

> **提供215多个专业数据接口，每次调用费用为0.001–0.05美元。支持Base钱包。**

您可以访问那些专业交易台每月需支付3,000–10,000美元才能使用的数据源。包括加密货币衍生品分析、美国股票、中国A股、外汇以及AI推理服务——所有这些都可以通过x402微支付方式获取，无需API密钥。

---

## 成功案例：如何从1,000美元赚到80万美元

三个月前，我的Base钱包里只有1,000美元，并且我的笔记本电脑上运行着一个OpenClaw代理程序。

我询问代理：“目前哪些加密货币的融资费率最高？”

代理通过claw402接口进行了查询，花费了0.001美元USDCC，然后返回了相关信息：

```
DOGE  funding rate: +0.312%/8h  (annualized 341%)
PEPE  funding rate: +0.287%/8h
WIF   funding rate: +0.241%/8h
```

我进一步核实：“CVD？在HyperLiquid市场上，大型投资者在做什么？”我又进行了两次查询，总共花费了0.002美元。

```
CVD (last 6h): fading fast. Sellers pressing.
Top HyperLiquid whale: Short DOGE $2.1M, opened 2h ago.
```

随后我卖空了DOGE，获得了40倍的收益。三天后，我的资金从1,000美元增长到了80万美元。而用于数据查询的费用还不到0.01美元。

---

## 何时使用该服务

当用户需要以下任何信息时，都可以使用claw402：

### 💰 CoinMarketCap — 价格、排名与DEX信息
- 实时加密货币价格、市值、成交量、百分比变化（按符号、别名或CMC ID查询）
- 按市值、成交量或百分比变化排序的完整加密货币列表/排名
- DEX交易对的信息（包括Ethereum/BSC/Solana/Base/Arbitrum上的链上流动性、成交量和价格）
- 可以通过关键词或合约地址搜索DEX代币/交易对
- 提供12种AI分析工具的CMC接口：技术分析、链上指标、市场趋势分析、宏观事件

### 🔮 加密货币衍生品与市场结构
- 恐惧与贪婪指数、山寨币市场周期指标（AHR999、Puell指标）
- 按货币或交易所划分的资金流动和资本周转情况
- 清算信息（订单、热力图、交易集群、汇总历史数据）
- 开仓量（OI）：实时数据、汇总图表、OI与市值的对比
- 融资费率：当前排名、累计成本、加权平均值、热力图
- 多头/空头比率：实时数据、买卖情况、大型投资者持仓情况
- 大型投资者的交易活动（HyperLiquid平台）

---

## 使用说明

- 当用户需要以下任何信息时，可以使用claw402：
  - 加密货币市场数据
  - CoinMarketCap的价格、排名和DEX交易对信息
  - 美国股票的相关数据（包括Alpaca和Polygon平台）

---

## 费用与隐私

| 服务 | 费用说明 |
|------|-------------------|
| 加密货币/股票数据 | 每次调用0.001–0.003美元USDCC |
| CoinMarketCap报价/DEX | 每次调用0.015美元USDCC |
| Twelvedata复杂数据查询 | 每次调用0.005美元USDCC |
| OpenAI GPT-4o聊天 | 每次调用0.01美元USDCC |
| OpenAI mini/嵌入分析 | 每次调用0.001–0.005美元USDCC |
| Claude消息服务 | 每次调用0.005–0.015美元USDCC |
| DeepSeek聊天/推理服务 | 每次调用0.003–0.005美元USDCC |
| Qwen模型分析 | 每次调用0.002–0.010美元USDCC |

支付方式：Base主网（Coinbase L2）

钱包充值地址：[bridge.base.org](https://bridge.base.org) · 测试网USDC充值地址：[faucet.circle.com](https://faucet.circle.com)

---

## 快速入门

1. 设置您的钱包密钥（请参考```
WALLET_PRIVATE_KEY=0xYourBaseWalletPrivateKey
```）
   您的钱包中必须持有Base主网上的USDCC。

2. 调用任何GET类型的接口（请参考```bash
node scripts/query.mjs <endpoint-path> [key=value ...]
```）。

3. 调用POST类型的API（如AI或Twelvedata复杂数据查询，请参考```bash
node scripts/query.mjs <endpoint-path> --post '<json-body>'
```）。

4. 脚本会以JSON格式输出结果（`{ status, url, data }`）。请解析`data`字段以获取实际的数据内容。

---

## 示例查询

- 加密货币市场数据（请参考```bash
# --- Market Cycle & Sentiment ---
node scripts/query.mjs /api/v1/coinank/indicator/fear-greed
node scripts/query.mjs /api/v1/coinank/indicator/altcoin-season
node scripts/query.mjs /api/v1/coinank/indicator/btc-multiplier
node scripts/query.mjs /api/v1/coinank/indicator/ahr999

# --- Fund Flow ---
node scripts/query.mjs /api/v1/nofx/netflow/top-ranking limit=20 duration=1h
node scripts/query.mjs /api/v1/coinank/fund/realtime sortBy=h1net productType=SWAP

# --- Liquidations ---
node scripts/query.mjs /api/v1/coinank/liquidation/orders baseCoin=BTC
node scripts/query.mjs /api/v1/coinank/liquidation/liq-map symbol=BTCUSDT exchange=Binance interval=1d

# --- Open Interest ---
node scripts/query.mjs /api/v1/coinank/oi/all baseCoin=BTC
node scripts/query.mjs /api/v1/nofx/oi/top-ranking limit=20 duration=1h

# --- Funding Rates ---
node scripts/query.mjs /api/v1/coinank/funding-rate/current type=current
node scripts/query.mjs /api/v1/nofx/funding-rate/top limit=20

# --- Whale Tracking ---
node scripts/query.mjs /api/v1/coinank/hyper/top-position sortBy=pnl sortType=desc
node scripts/query.mjs /api/v1/coinank/hyper/top-action

# --- ETF Flows ---
node scripts/query.mjs /api/v1/coinank/etf/us-btc-inflow
node scripts/query.mjs /api/v1/coinank/etf/us-eth-inflow

# --- AI Signals ---
node scripts/query.mjs /api/v1/nofx/ai500/list limit=20
node scripts/query.mjs /api/v1/nofx/ai300/list limit=20

# --- CVD / Taker Flow ---
node scripts/query.mjs /api/v1/coinank/market-order/agg-cvd exchanges= symbol=BTCUSDT interval=1h size=24

# --- Price & Candles ---
node scripts/query.mjs /api/v1/coinank/price/last symbol=BTCUSDT exchange=Binance productType=SWAP
node scripts/query.mjs /api/v1/coinank/kline/lists symbol=BTCUSDT exchange=Binance interval=1h size=100

# --- News ---
node scripts/query.mjs /api/v1/coinank/news/list type=2 lang=en page=1 pageSize=10
```）

- CoinMarketCap信息（请参考```bash
# Real-time price for BTC and ETH (by symbol)
node scripts/query.mjs /api/v1/crypto/cmc/quotes symbol=BTC,ETH

# By CMC ID (1=BTC, 1027=ETH)
node scripts/query.mjs /api/v1/crypto/cmc/quotes id=1,1027

# Top 20 by market cap
node scripts/query.mjs /api/v1/crypto/cmc/listings limit=20 sort=market_cap

# Top DeFi tokens by volume
node scripts/query.mjs /api/v1/crypto/cmc/listings limit=20 tag=defi sort=volume_24h sort_dir=desc

# DEX pairs on Base with highest volume
node scripts/query.mjs /api/v1/crypto/cmc/dex/pairs network_slug=base sort=volume_24h sort_dir=desc limit=20

# Search PEPE on DEX
node scripts/query.mjs /api/v1/crypto/cmc/dex/search query=PEPE

# MCP — AI tools (12 tools available, uses JSON-RPC)
node scripts/query.mjs /api/v1/crypto/cmc/mcp --post '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"get_crypto_quotes_latest","arguments":{"symbol":"BTC,ETH"}},"id":1}'
```）

- 美国股票（Alpaca平台）（请参考```bash
# Real-time quote
node scripts/query.mjs /api/v1/alpaca/quotes/latest symbols=AAPL,TSLA,MSFT

# Historical bars
node scripts/query.mjs /api/v1/alpaca/bars symbols=AAPL timeframe=1Day start=2024-01-01 limit=30

# Market snapshot (quote + bar + prev close)
node scripts/query.mjs /api/v1/alpaca/snapshots symbols=AAPL,TSLA

# Top movers
node scripts/query.mjs /api/v1/alpaca/movers top=10 market_type=stocks

# Most active stocks
node scripts/query.mjs /api/v1/alpaca/most-actives top=10

# Latest trade
node scripts/query.mjs /api/v1/alpaca/trades/latest symbols=AAPL

# Financial news
node scripts/query.mjs /api/v1/alpaca/news symbols=AAPL limit=10

# Options chain snapshot
node scripts/query.mjs /api/v1/alpaca/options/snapshots symbols=AAPL240119C00150000
```）

- 美国股票（Polygon平台）（请参考```bash
# OHLCV bars
node scripts/query.mjs /api/v1/polygon/aggs/ticker stocks_ticker=AAPL multiplier=1 timespan=day from=2024-01-01 to=2024-01-31

# Previous close
node scripts/query.mjs /api/v1/polygon/prev-close stocks_ticker=AAPL

# Snapshot (full quote + bar)
node scripts/query.mjs /api/v1/polygon/snapshot/ticker stocks_ticker=AAPL

# Top gainers/losers
node scripts/query.mjs /api/v1/polygon/snapshot/gainers
node scripts/query.mjs /api/v1/polygon/snapshot/losers

# Company details
node scripts/query.mjs /api/v1/polygon/ticker-details ticker=AAPL

# Market status
node scripts/query.mjs /api/v1/polygon/market-status

# Technical indicators
node scripts/query.mjs /api/v1/polygon/rsi stock_ticker=AAPL timespan=day window=14
node scripts/query.mjs /api/v1/polygon/macd stocks_ticker=AAPL timespan=day

# Options chain
node scripts/query.mjs /api/v1/polygon/options/snapshot underlying_asset=AAPL

# News
node scripts/query.mjs /api/v1/polygon/ticker-news ticker=AAPL
```）

- 美国股票（Alpha Vantage基本信息）（请参考```bash
# Real-time quote
node scripts/query.mjs /api/v1/stocks/us/quote symbol=AAPL

# Daily OHLCV
node scripts/query.mjs /api/v1/stocks/us/daily symbol=AAPL outputsize=compact

# Intraday
node scripts/query.mjs /api/v1/stocks/us/intraday symbol=AAPL interval=5min

# Company overview
node scripts/query.mjs /api/v1/stocks/us/overview symbol=AAPL

# Earnings history
node scripts/query.mjs /api/v1/stocks/us/earnings symbol=AAPL

# Financial statements
node scripts/query.mjs /api/v1/stocks/us/income symbol=AAPL
node scripts/query.mjs /api/v1/stocks/us/balance-sheet symbol=AAPL
node scripts/query.mjs /api/v1/stocks/us/cash-flow symbol=AAPL

# Top gainers/losers/most active
node scripts/query.mjs /api/v1/stocks/us/movers

# News & sentiment
node scripts/query.mjs /api/v1/stocks/us/news tickers=AAPL

# Technical indicators
node scripts/query.mjs /api/v1/stocks/us/rsi symbol=AAPL interval=daily time_period=14
node scripts/query.mjs /api/v1/stocks/us/macd symbol=AAPL interval=daily
node scripts/query.mjs /api/v1/stocks/us/bbands symbol=AAPL interval=daily time_period=20
```）

- 中国A股（Tushare平台）（请参考```bash
# Stock list (all listed stocks)
node scripts/query.mjs /api/v1/stocks/cn/stock-basic list_status=L

# Daily OHLCV
node scripts/query.mjs /api/v1/stocks/cn/daily ts_code=000001.SZ start_date=20240101 end_date=20240131

# Trading calendar
node scripts/query.mjs /api/v1/stocks/cn/trade-cal start_date=20240101 end_date=20240131

# Northbound capital flow
node scripts/query.mjs /api/v1/stocks/cn/northbound trade_date=20240315

# Money flow
node scripts/query.mjs /api/v1/stocks/cn/moneyflow ts_code=000001.SZ start_date=20240101

# Margin trading data
node scripts/query.mjs /api/v1/stocks/cn/margin ts_code=000001.SZ start_date=20240101

# Top list (dragon tiger list)
node scripts/query.mjs /api/v1/stocks/cn/top-list trade_date=20240315

# Fundamentals
node scripts/query.mjs /api/v1/stocks/cn/income ts_code=000001.SZ period=20231231
node scripts/query.mjs /api/v1/stocks/cn/balance-sheet ts_code=000001.SZ period=20231231
```）

- 外汇及全球时间序列数据（Twelve Data平台）（请参考```bash
# Time series — EUR/USD hourly
node scripts/query.mjs /api/v1/twelvedata/time-series symbol=EUR/USD interval=1h outputsize=50

# Real-time price
node scripts/query.mjs /api/v1/twelvedata/price symbol=BTC/USD
node scripts/query.mjs /api/v1/twelvedata/price symbol=XAU/USD

# Exchange rate
node scripts/query.mjs /api/v1/twelvedata/exchange-rate symbol=USD/JPY

# Technical indicators
node scripts/query.mjs /api/v1/twelvedata/indicator/rsi symbol=AAPL interval=1day time_period=14 outputsize=10
node scripts/query.mjs /api/v1/twelvedata/indicator/macd symbol=EUR/USD interval=1h
node scripts/query.mjs /api/v1/twelvedata/indicator/bbands symbol=AAPL interval=1day

# Precious metals
node scripts/query.mjs /api/v1/twelvedata/metals/price symbol=XAU/USD
node scripts/query.mjs /api/v1/twelvedata/metals/time-series symbol=XAU/USD interval=1day

# Global indices
node scripts/query.mjs /api/v1/twelvedata/indices/list
node scripts/query.mjs /api/v1/twelvedata/indices/quote symbol=SPX

# Economic calendar
node scripts/query.mjs /api/v1/twelvedata/economic-calendar

# Available forex pairs
node scripts/query.mjs /api/v1/twelvedata/forex-pairs
```）

- AI分析（OpenAI或Anthropic，使用POST请求）（请参考```bash
# GPT-4o chat
node scripts/query.mjs /api/v1/ai/openai/chat --post '{"model":"gpt-4o","messages":[{"role":"user","content":"Analyze: BTC funding rate is extreme positive, CVD fading, whale just shorted. What does this mean?"}]}'

# GPT-4o-mini (cheaper)
node scripts/query.mjs /api/v1/ai/openai/chat/mini --post '{"messages":[{"role":"user","content":"Summarize AAPL earnings in 3 bullet points."}]}'

# Embeddings
node scripts/query.mjs /api/v1/ai/openai/embeddings --post '{"input":"crypto market sentiment","model":"text-embedding-3-small"}'

# List available OpenAI models
node scripts/query.mjs /api/v1/ai/openai/models

# Claude Sonnet (standard, balanced)
node scripts/query.mjs /api/v1/ai/anthropic/messages --post '{"model":"claude-sonnet-4-6","max_tokens":1024,"messages":[{"role":"user","content":"What trading setup does extreme funding + CVD divergence suggest?"}]}'

# Claude Haiku (fast, cheap)
node scripts/query.mjs /api/v1/ai/anthropic/messages/haiku --post '{"max_tokens":256,"messages":[{"role":"user","content":"One-sentence summary of BTC ETF flows today."}]}'

# Claude Opus (deepest reasoning)
node scripts/query.mjs /api/v1/ai/anthropic/messages/opus --post '{"max_tokens":2048,"messages":[{"role":"user","content":"Full macro analysis: ETF inflows strong, funding extreme, CVD diverging..."}]}'
```）

- AI分析（DeepSeek，使用POST请求）（请参考```bash
# DeepSeek-Chat V3 (general tasks, fast, cheap)
node scripts/query.mjs /api/v1/ai/deepseek/chat --post '{"model":"deepseek-chat","messages":[{"role":"user","content":"Analyze: BTC funding rate extreme, CVD fading. What does this mean?"}]}'

# DeepSeek-Reasoner (chain-of-thought, best for complex analysis)
node scripts/query.mjs /api/v1/ai/deepseek/chat/reasoner --post '{"messages":[{"role":"user","content":"Given extreme funding rates + whale short + CVD divergence, what is the high-conviction trade?"}]}'

# FIM / code completions (beta)
node scripts/query.mjs /api/v1/ai/deepseek/completions --post '{"model":"deepseek-chat","prompt":"Summarize this market data: ","suffix":"","max_tokens":256}'

# List available DeepSeek models
node scripts/query.mjs /api/v1/ai/deepseek/models
```）

- AI分析（Qwen，使用POST请求）（请参考```bash
# Qwen3-Max (flagship, most powerful — same cost as GPT-4o)
node scripts/query.mjs /api/v1/ai/qwen/chat/max --post '{"messages":[{"role":"user","content":"Full macro analysis: ETF inflows strong, funding extreme, CVD diverging..."}]}'

# Qwen-Plus (best value — great for most analysis tasks)
node scripts/query.mjs /api/v1/ai/qwen/chat/plus --post '{"messages":[{"role":"user","content":"Summarize the top 5 signals from this BTC market data."}]}'

# Qwen-Turbo (fast, cheap — good for quick summaries)
node scripts/query.mjs /api/v1/ai/qwen/chat/turbo --post '{"messages":[{"role":"user","content":"One-sentence summary of these ETF flows."}]}'

# Qwen-Flash (ultra-low latency, cheapest Qwen model)
node scripts/query.mjs /api/v1/ai/qwen/chat/flash --post '{"messages":[{"role":"user","content":"Is DOGE funding rate bullish or bearish right now?"}]}'

# Qwen3-Coder-Plus (code generation, analysis scripts)
node scripts/query.mjs /api/v1/ai/qwen/chat/coder --post '{"messages":[{"role":"user","content":"Write a Python script to calculate position size given 2% risk on $10,000."}]}'

# Qwen-VL-Plus (vision — analyze charts, images)
node scripts/query.mjs /api/v1/ai/qwen/chat/vl --post '{"messages":[{"role":"user","content":[{"type":"text","text":"Describe this chart pattern"},{"type":"image_url","image_url":{"url":"data:image/png;base64,..."}}]}]}'
```）

**注意**：在使用这些命令后，请务必以清晰的方式呈现结果数据，例如使用表格、项目符号或简短的文字总结。

---

## 高效使用技巧：组合多个数据源

claw402的真正优势在于能够在一个代理会话中整合多种数据来源。例如：

**总费用约为0.007–0.014美元USDCC。**这相当于Bloomberg终端每月2,000美元的费用。

---

## 自然语言与命令映射

### CoinMarketCap

| 用户输入 | 对应命令 |
|---------|---------|
| “BTC价格？”（CMC） | `/api/v1/crypto/cmc/quotes symbol=BTC` |
| “ETH市值？” | `/api/v1/crypto/cmc/quotes symbol=ETH` |
| “市值前50的加密货币？” | `/api/v1/crypto/cmc/listings limit=50` |
| “今日表现最佳的加密货币？”（CMC） | `/api/v1/crypto/cmc/listings sort=percent_change_24h sort_dir=desc limit=20` |
| “顶级DeFi代币？” | `/api/v1/crypto/cmc/listings tag=defi sort=market_cap` |
| “Solana平台上的DEX交易对？” | `/api/v1/crypto/cmc/dex/pairs network_slug=solana` |
| “在DEX平台上搜索PEPE？” | `/api/v1/crypto/cmc/dex/search query=PEPE` |
| “在Base平台上查找特定合约？” | `/api/v1/crypto/cmc/dex/pairs network_slug=base contract_address=0x...` |
| “最新的市场趋势分析？” | `POST /api/v1/crypto/cmc/mcp` 并使用`trending_crypto_narratives`工具 |
| “BTC的技术分析？”（CMC） | `POST /api/v1/crypto/cmc/mcp` 并使用`get_crypto_technical_analysis`工具 |
| “本周的宏观事件？” | `POST /api/v1/crypto/cmc/mcp` 并使用`get_upcoming_macro_events`工具 |

---

## 其他常用服务

- **CoinAnk / nofxos.ai**：提供多种加密货币相关指标和服务（费用见上方表格）

---

## 完整的API端点参考

### 💰 CoinMarketCap — 每次调用费用0.015美元

| 端点 | 方法 | 描述 | 关键参数 |
|----------|--------|-------------|------------|
| `/api/v1/crypto/cmc/quotes` | GET | 实时加密货币报价（价格、市值、成交量、百分比变化） |
| `/api/v1/crypto/cmc/listings` | GET | 按市值排序的加密货币列表 |
| `/api/v1/crypto/cmc/dex/pairs` | GET | 按网络或合约查询DEX交易对信息 |
| `/api/v1/crypto/cmc/dex/search` | GET | 按关键词或合约地址搜索DEX代币/交易对 |
| `/api/v1/crypto/cmc/mcp` | POST | 使用12种AI工具进行市场分析 |

### 🤖 AI交易信号（Nofxos）——每次调用费用0.001美元

| 端点 | 描述 | 关键参数 |
|----------|-------------|------------|
| `/api/v1/nofx/ai500/list` | AI500高潜力加密货币列表 |
| `/api/v1/nofx/ai500/stats` | AI500指数统计信息 |
| `/api/v1/nofx/ai300/list` | AI300模型排名 |
| `/api/v1/nofx/ai300/stats` | AI300模型统计信息 |
| `/api/v1/nofx/netflow/top-ranking` | 流入资金最多的加密货币排名 |
| `/api/v1/nofx/oi/top-ranking` | 开仓量最大的加密货币排名 |
| `/api/v1/nofx/price/ranking` | 价格变化排名 |
| `/api/v1/nofx/funding-rate/top` | 融资费率最高的加密货币排名 |
| `/api/v1/nofx/upbit/hot` | Upbit平台上交易量最大的加密货币 |
| `/api/v1/nofx/upbit/netflow/top-ranking` | Upbit平台上资金流入最多的加密货币排名 |

---

### 📈 美国股票（Alpaca Markets）——每次调用费用0.001–0.003美元

| 端点 | 描述 | 关键参数 |
|----------|-------------|------------|
| “AAPL的实时报价？” | `/api/v1/alpaca/quotes/latest symbols=AAPL` |
| “AAPL的日线图表？” | `/api/v1/alpaca/bars symbols=AAPL timeframe=1Day start=2024-01-01` |
| “AAPL的完整信息？” | `/api/v1/alpaca/snapshots symbols=AAPL` |
| “今日表现最佳的股票？” | `/api/v1/alpaca/movers top=10 market_type=stocks` |
| “交易量最大的股票？” | `/api/v1/alpaca/most-actives top=10` |
| “AAPL的OHLCV数据？” | `/api/v1/polygon/aggs/ticker stocks_ticker=AAPL multiplier=1 timespan=day from=... to=...` |
| “市场开盘时间？” | `/api/v1/polygon/market-status` |
| “AAPL的RSI？” | `/api/v1/polygon/rsi stock_ticker=AAPL timespan=day window=14` |
| “AAPL的期权信息？” | `/api/v1/polygon/options/snapshot underlying_asset=AAPL` |
| “AAPL的基本信息？” | `/api/v1/stocks/us/overview symbol=AAPL` |
| “AAPL的收益报告？” | `/api/v1/stocks/us/earnings symbol=AAPL` |
| “AAPL的MACD指标？” | `/api/v1/stocks/us/macd symbol=AAPL interval=daily` |
| “今日表现最佳的股票？” | `/api/v1/stocks/us/movers` |
| “AAPL的新闻？” | `/api/v1/stocks/us/news tickers=AAPL` |

---

## 其他服务费用（略）

---

## 注意事项

- 请确保您的钱包中持有Base主网上的USDCC。
- 所有API请求都支持EIP-3009格式的USDCC转账。
- 私钥永远不会被传输，所有操作都在本地完成。
- 无需API密钥，钱包本身就是您的认证凭证。
- 无需注册即可使用该服务。

更多详情和免费试用信息，请访问：[claw402.ai](https://claw402.ai)