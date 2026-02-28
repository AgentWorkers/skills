---
name: fin-intel-hub
description: Comprehensive financial intelligence hub for SEC filings, crypto on-chain data, news sentiment, macro indicators, and global stock markets (US, China, Hong Kong, Taiwan, Japan, Korea). Use when users need to: (1) Retrieve SEC EDGAR filings (10-K, 10-Q, 8-K), (2) Monitor crypto on-chain metrics and whale alerts, (3) Analyze financial news sentiment, (4) Access macroeconomic indicators (Fed rates, CPI, unemployment), (5) Get global stock prices including Asian markets (HKEX, Tokyo, Taiwan, Korea, Shanghai, Shenzhen), or any financial data research and analysis tasks.
author: xuan622
source: https://github.com/xuan622/fin-intel-hub
license: MIT
environment_variables:
  - name: ALPHA_VANTAGE_API_KEY
    description: Optional - Alpha Vantage API key for US stock data
    required: false
  - name: NEWS_API_KEY
    description: Optional - NewsAPI key for news sentiment analysis
    required: false
  - name: FRED_API_KEY
    description: Optional - FRED API key for macroeconomic data
    required: false
  - name: GLASSNODE_API_KEY
    description: Optional - Glassnode API key for enhanced crypto exchange flow data
    required: false
  - name: ETHERSCAN_API_KEY
    description: Optional - Etherscan API key for Ethereum gas price data
    required: false
  - name: WHALE_ALERT_API_KEY
    description: Optional - Whale Alert API key for whale transaction monitoring
    required: false
requirements: |
  No pip packages required. Uses only Python standard library + requests.
---

# Fin Intel Hub

Fin Intel Hub 是一个专为 OpenClaw 设计的金融智能平台，支持包括美国、中国、香港、台湾、日本和韩国在内的全球市场。

## 主要功能

- **SEC 文件查询**：从 EDGAR 数据库中检索 10-K、10-Q 和 8-K 等 SEC 文件。
- **全球市场数据**：美国股票数据（Alpha Vantage）+ 亚洲市场数据（Yahoo Finance）。
- **亚洲市场**：香港、东京、台湾、韩国、上海、深圳的股票市场。
- **加密货币链上数据**：监控钱包资金流动以及交易所的出入金情况。
- **新闻情感分析**：汇总来自各类金融新闻来源的情感信息。
- **宏观经济仪表盘**：显示美联储利率、CPI 和失业率等宏观经济指标。

## API 密钥（可选）

所有 API 密钥均为可选。该工具在使用 Yahoo Finance 提供的股票数据时无需密钥即可正常运行。如需启用更多功能，请添加相应的 API 密钥：

| 服务 | 用途 | 免费使用量 | 是否必需？ |
|---------|---------|-----------|-----------|
| Yahoo Finance | 全球/亚洲股票、指数、期货、商品数据 | 无限制 | **不需要** |
| Alpha Vantage | 美国股票、财报数据 | 每天 25 次请求 | 可选 |
| NewsAPI | 金融新闻情感分析 | 每天 100 次请求 | 可选 |
| FRED API | 宏观经济数据 | 无限制 | 可选 |
| DeFiLlama | 加密货币链上数据 | 无限制 | **不需要** |

## 快速入门

### SEC 文件查询
```python
from scripts.sec_filings import get_recent_filings

# Get last 5 10-K filings for Apple
filings = get_recent_filings(ticker="AAPL", form="10-K", limit=5)
```

### 股票价格查询
```python
from scripts.market_data import get_price_history

# Get 30-day price history
prices = get_price_history(ticker="TSLA", days=30)
```

### 加密货币数据查询
```python
from scripts.crypto_onchain import get_exchange_flows

# Monitor exchange inflows/outflows
flows = get_exchange_flows(exchange="binance", days=7)
```

## 脚本参考

- `scripts/sec_filings.py`：用于与 SEC EDGAR 数据库进行交互的脚本。
- `scripts/market_data.py`：用于获取美国股票价格和财报数据的脚本。
- `scripts/yahoo_finance.py`：用于获取全球/亚洲股票价格的脚本。
- `scripts/crypto_onchain.py`：用于通过 DeFiLlama/CoinGecko 获取区块链数据的脚本。
- `scripts/sentiment_news.py`：用于分析新闻情感的脚本。
- `scripts/macro_data.py`：用于获取宏观经济指标的脚本。

### 亚洲市场示例
```python
from scripts.yahoo_finance import get_hong_kong_stock, get_tokyo_stock, get_taiwan_stock

# Hong Kong - Tencent
prices = get_hong_kong_stock("0700", period="1y")

# Tokyo - Toyota
prices = get_tokyo_stock("7203", period="1y")

# Taiwan - TSMC
prices = get_taiwan_stock("2330", period="1y")
```

### 指数与期货示例
```python
from scripts.yahoo_finance import get_sp500, get_nikkei225, get_vix
from scripts.yahoo_finance import get_crude_oil, get_gold, list_available_indices

# Global indices (15+ available)
sp500 = get_sp500(period="1y")
nasdaq = get_nasdaq(period="1y")
nikkei = get_nikkei225(period="1y")
hang_seng = get_hang_seng(period="1y")
vix = get_vix(period="1mo")  # Fear index

# Futures (15+ available)
oil_futures = get_crude_oil(period="6mo")
gold_futures = get_gold(period="6mo")
sp_futures = get_sp500_futures(period="1mo")
natural_gas = get_natural_gas(period="6mo")

# List all available
indices = list_available_indices()
futures = list_available_futures()
```

有关详细的 API 文档和数据结构，请参阅 `references/`。