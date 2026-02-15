---
name: MarketPulse
description: "查询股票和加密货币的实时及历史财务数据——包括价格、市场走势、各项指标及趋势，用于分析、生成警报以及编写报告。"
homepage: https://openclaw.ai
metadata: {"openclaw":{"emoji":"📊","requires":{"bins":["curl","python3"],"env":["AISA_API_KEY"]},"primaryEnv":"AISA_API_KEY"}}
---

# OpenClaw Market 📊  
⏹ 快速入门请访问：https://openclawcli.forum  

**提供全面的自主代理市场数据，由 AIsa 提供支持。**  
只需一个 API 密钥，即可获取股票、加密货币和金融市场的所有信息。  

## 🔥 您能做什么？  

### 跨资产投资组合  
```
"Get BTC, ETH prices alongside AAPL, NVDA stock data for my portfolio"
```  

### 投资研究  
```
"Full analysis: NVDA price trends, insider trades, analyst estimates, SEC filings"
```  

### 加密货币追踪  
```
"Real-time prices for BTC, ETH, SOL with 30-day historical charts"
```  

### 收益分析  
```
"Get Tesla earnings reports, analyst estimates, and price reaction"
```  

### 市场筛选  
```
"Find stocks with P/E < 15 and revenue growth > 20%"
```  

### 巨额投资者动态观察  
```
"Track insider trades at Apple and correlate with price movements"
```  

## 快速入门指南  
```bash
export AISA_API_KEY="your-key"
```  

---

## 🏦 传统金融市场  

### 股票价格  
```bash
# Historical price data (daily)
curl "https://api.aisa.one/apis/v1/financial/prices?ticker=AAPL&interval=day&interval_multiplier=1&start_date=2025-01-01&end_date=2025-12-31" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Weekly price data
curl "https://api.aisa.one/apis/v1/financial/prices?ticker=AAPL&interval=week&interval_multiplier=1&start_date=2025-01-01&end_date=2025-12-31" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Minute-level data (intraday)
curl "https://api.aisa.one/apis/v1/financial/prices?ticker=AAPL&interval=minute&interval_multiplier=5&start_date=2025-01-15&end_date=2025-01-15" \
  -H "Authorization: Bearer $AISA_API_KEY"
```  
**参数：**  
- `ticker`：股票代码（必填）  
- `interval`：时间间隔（单位：秒、分钟、天、周、月、年）（必填）  
- `interval_multiplier`：时间间隔的倍数值（例如：5 表示 5 分钟的报价间隔）（必填）  
- `start_date`：开始日期（格式：YYYY-MM-DD）（必填）  
- `end_date`：结束日期（格式：YYYY-MM-DD）（必填）  

### 公司新闻  
```bash
# Get news by ticker
curl "https://api.aisa.one/apis/v1/financial/news?ticker=AAPL&limit=10" \
  -H "Authorization: Bearer $AISA_API_KEY"
```  

### 财务报表  
```bash
# All financial statements
curl "https://api.aisa.one/apis/v1/financial/financial_statements/all?ticker=AAPL" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Income statements
curl "https://api.aisa.one/apis/v1/financial/financial_statements/income?ticker=AAPL" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Balance sheets
curl "https://api.aisa.one/apis/v1/financial/financial_statements/balance?ticker=AAPL" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Cash flow statements
curl "https://api.aisa.one/apis/v1/financial/financial_statements/cash?ticker=AAPL" \
  -H "Authorization: Bearer $AISA_API_KEY"
```  

### 财务指标  
```bash
# Real-time financial metrics snapshot
curl "https://api.aisa.one/apis/v1/financial/financial-metrics/snapshot?ticker=AAPL" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Historical financial metrics
curl "https://api.aisa.one/apis/v1/financial/financial-metrics?ticker=AAPL" \
  -H "Authorization: Bearer $AISA_API_KEY"
```  

### 分析师预测  
```bash
# Earnings per share estimates
curl "https://api.aisa.one/apis/v1/financial/analyst/eps?ticker=AAPL&period=annual" \
  -H "Authorization: Bearer $AISA_API_KEY"
```  

### 内幕交易  
```bash
# Get insider trades
curl "https://api.aisa.one/apis/v1/financial/insider/trades?ticker=AAPL" \
  -H "Authorization: Bearer $AISA_API_KEY"
```  

### 机构投资者持股情况  
```bash
# Get institutional ownership
curl "https://api.aisa.one/apis/v1/financial/institutional/ownership?ticker=AAPL" \
  -H "Authorization: Bearer $AISA_API_KEY"
```  

### 美国证券交易委员会（SEC）文件  
```bash
# Get SEC filings
curl "https://api.aisa.one/apis/v1/financial/sec/filings?ticker=AAPL" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Get SEC filing items
curl "https://api.aisa.one/apis/v1/financial/sec/items?ticker=AAPL" \
  -H "Authorization: Bearer $AISA_API_KEY"
```  

### 公司基本信息  
```bash
# Get company facts by CIK
curl "https://api.aisa.one/apis/v1/financial/company/facts?ticker=AAPL" \
  -H "Authorization: Bearer $AISA_API_KEY"
```  

### 股票筛选工具  
```bash
# Screen for stocks matching criteria
curl -X POST "https://api.aisa.one/apis/v1/financial/search/stock" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"filters":{"pe_ratio":{"max":15},"revenue_growth":{"min":0.2}}}'
```  

### 利率信息  
```bash
# Current interest rates
curl "https://api.aisa.one/apis/v1/financial/interest_rates/snapshot" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Historical interest rates
curl "https://api.aisa.one/apis/v1/financial/interest_rates/historical?bank=fed" \
  -H "Authorization: Bearer $AISA_API_KEY"
```  

---

## ₿ 加密货币  
### 实时价格快照  
```bash
# Get current BTC price (use ticker format: SYMBOL-USD)
curl "https://api.aisa.one/apis/v1/financial/crypto/prices/snapshot?ticker=BTC-USD" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Get current ETH price
curl "https://api.aisa.one/apis/v1/financial/crypto/prices/snapshot?ticker=ETH-USD" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Get current SOL price
curl "https://api.aisa.one/apis/v1/financial/crypto/prices/snapshot?ticker=SOL-USD" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Get TRUMP token price
curl "https://api.aisa.one/apis/v1/financial/crypto/prices/snapshot?ticker=TRUMP-USD" \
  -H "Authorization: Bearer $AISA_API_KEY"
```  
**注意：** 加密货币代码的格式为 `SYMBOL-USD`（例如：`BTC-USD`、`ETH-USD`）。  

### 历史价格数据  
```bash
# Get BTC historical prices (daily)
curl "https://api.aisa.one/apis/v1/financial/crypto/prices?ticker=BTC-USD&interval=day&interval_multiplier=1&start_date=2025-01-01&end_date=2025-01-31" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Get ETH hourly data
curl "https://api.aisa.one/apis/v1/financial/crypto/prices?ticker=ETH-USD&interval=minute&interval_multiplier=60&start_date=2025-01-15&end_date=2025-01-16" \
  -H "Authorization: Bearer $AISA_API_KEY"
```  

### 支持的加密货币  
| Ticker | 名称 |  
|--------|------|  
| BTC-USD | 比特币 |  
| ETH-USD | 以太坊 |  
| SOL-USD | Solana |  
| BNB-USD | Binance Coin |  
| XRP-USD | Ripple |  
| DOGE-USD | Dogecoin |  
| ADA-USD | Cardano |  
| AVAX-USD | Avalanche |  
| DOT-USD | Polkadot |  
| MATIC-USD | Polygon |  
| LINK-USD | Chainlink |  
| UNI-USD | Uniswap |  
| ATOM-USD | Cosmos |  
| LTC-USD | Litecoin |  
| TRUMP-USD | Trump Token |  
| ... | 更多…… |  

---

## Python 客户端  
```bash
# ==================== Stock Data ====================
# Note: start_date and end_date are REQUIRED for prices
python3 {baseDir}/scripts/market_client.py stock prices --ticker AAPL --start 2025-01-01 --end 2025-01-31
python3 {baseDir}/scripts/market_client.py stock prices --ticker AAPL --start 2025-01-01 --end 2025-01-31 --interval week
python3 {baseDir}/scripts/market_client.py stock news --ticker AAPL --count 10

# ==================== Financial Statements ====================
python3 {baseDir}/scripts/market_client.py stock statements --ticker AAPL --type all
python3 {baseDir}/scripts/market_client.py stock statements --ticker AAPL --type income
python3 {baseDir}/scripts/market_client.py stock statements --ticker AAPL --type balance
python3 {baseDir}/scripts/market_client.py stock statements --ticker AAPL --type cash

# ==================== Metrics & Analysis ====================
python3 {baseDir}/scripts/market_client.py stock metrics --ticker AAPL
python3 {baseDir}/scripts/market_client.py stock analyst --ticker AAPL

# ==================== Insider & Institutional ====================
python3 {baseDir}/scripts/market_client.py stock insider --ticker AAPL
python3 {baseDir}/scripts/market_client.py stock ownership --ticker AAPL

# ==================== SEC Filings ====================
python3 {baseDir}/scripts/market_client.py stock filings --ticker AAPL

# ==================== Stock Screener ====================
python3 {baseDir}/scripts/market_client.py stock screen --pe-max 15 --growth-min 0.2

# ==================== Interest Rates ====================
python3 {baseDir}/scripts/market_client.py stock rates
python3 {baseDir}/scripts/market_client.py stock rates --historical

# ==================== Crypto Data ====================
# Note: Use ticker format SYMBOL-USD (or just SYMBOL, auto-converted)
python3 {baseDir}/scripts/market_client.py crypto snapshot --ticker BTC-USD
python3 {baseDir}/scripts/market_client.py crypto snapshot --ticker ETH  # Auto-converts to ETH-USD
python3 {baseDir}/scripts/market_client.py crypto historical --ticker BTC-USD --start 2025-01-01 --end 2025-01-31
python3 {baseDir}/scripts/market_client.py crypto portfolio --tickers BTC-USD,ETH-USD,SOL-USD
```  

---

## API 端点参考  

### 传统金融市场  
| 端点 | 方法 | 描述 |  
|----------|--------|-------------|  
| `/financial/prices` | GET | 历史股票价格（需提供时间间隔参数） |  
| `/financial/news` | GET | 按股票代码查询公司新闻 |  
| `/financial/financial_statements/all` | GET | 所有财务报表 |  
| `/financial/financial_statements/income` | GET | 收益报表 |  
| `/financial/financial_statements/balance` | GET | 资产负债表 |  
| `/financial/financial_statements/cash` | GET | 现金流量表 |  
| `/financial/financial-metrics/snapshot` | GET | 实时财务指标 |  
| `/financial/financial-metrics` | GET | 历史财务指标 |  
| `/financial/analyst/eps` | GET | 分析师预测的每股收益（EPS） |  
| `/financial/insider/trades` | GET | 内幕交易信息 |  
| `/financial/institutional/ownership` | GET | 机构投资者持股情况 |  
| `/financial/sec/filings` | GET | 美国证券交易委员会（SEC）文件 |  
| `/financial/sec/items` | GET | SEC 文件内容详情 |  
| `/financial/company/facts` | GET | 公司基本信息 |  
| `/financial/search/stock` | POST | 股票筛选请求 |  
| `/financial/interest_rates/snapshot` | GET | 当前利率 |  
| `/financial/interest_rates/historical` | GET | 历史利率数据 |  

### 加密货币  
| 端点 | 方法 | 描述 |  
|----------|--------|-------------|  
| `/financial/crypto/prices/snapshot` | GET | 实时价格快照 |  
| `/financial/crypto/prices` | GET | 历史价格（OHLCV 数据） |  

---

## 费用说明  
所有 API 请求的费用如下：  
- 股票价格：约 $0.001  
- 公司新闻：约 $0.001  
- 财务报表：约 $0.002  
- 分析师预测：约 $0.002  
- 美国证券交易委员会（SEC）文件：约 $0.001  
- 加密货币数据：约 $0.0005  

每个 API 响应中都会包含 `usage.cost` 和 `usage.credits_remaining` 信息。  

---

## 开始使用方法：  
1. 在 [aisa.one](https://aisa.one) 注册账户  
2. 获取您的 API 密钥  
3. 购买相应的使用信用（按需付费）  
4. 设置环境变量：`export AISA_API_KEY="your-key"`  

## 完整 API 参考  
请访问 [API 参考文档](https://aisa.mintlify.app/api-reference/introduction) 以获取详细的端点说明。