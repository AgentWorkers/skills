---
name: open-market-data
description: 查询免费的金融数据API——股票、加密货币、宏观经济数据以及美国证券交易委员会（SEC）的文件
version: 0.1.0
tags: [finance, stocks, crypto, macro, sec, edgar, fred]
tools: [Bash]
metadata:
  openclaw:
    requires:
      bins: [node, omd]
    install:
      - kind: node
        package: open-market-data
        bins: [omd]
    homepage: https://github.com/anotb/open-market-data
    emoji: "\U0001F4C8"
---
# open-market-data (omd)

这是一个用于获取免费金融数据的统一命令行界面（CLI）。它通过单一接口查询来自8个数据源的信息，并具备自动路由和备用数据源的功能。

## 快速参考

```bash
# Stock quotes
omd quote AAPL
omd quote AAPL MSFT GOOGL

# Search
omd search "Apple Inc"

# Financial statements
omd financials AAPL
omd financials AAPL -p quarterly -l 8

# Price history
omd history AAPL --days 90

# Earnings
omd earnings AAPL

# Dividends
omd dividends AAPL

# Options chain
omd options AAPL
omd options AAPL -t call

# SEC filings
omd filing AAPL --type 10-K --latest
omd filing TSLA --type 8-K -l 5

# Insider transactions
omd insiders AAPL

# Crypto
omd crypto BTC
omd crypto top 20
omd crypto history ETH -d 30

# Macroeconomic data
omd macro GDP
omd macro GDP --limit 12
omd macro search "unemployment rate"

# Output formats
omd --json quote AAPL
omd --plain quote AAPL

# Force specific source
omd quote AAPL --source finnhub
omd financials AAPL --source sec-edgar
omd macro NY.GDP.MKTP.CD --source worldbank

# Bypass cache
omd --no-cache quote AAPL

# See all sources and their status
omd sources

# Configure API keys
omd config set fredApiKey <key>
omd config show
```

## 数据源

| 数据源 | 是否需要API密钥？ | 适用场景 |
|--------|------------------|-------------------|
| SEC EDGAR | 否 | 文件提交、XBRL财务数据、内幕交易信息 |
| Yahoo Finance | 否 | 实时报价、价格历史、期权信息、股息信息 |
| Binance | 否 | 加密货币价格（仅限非美国地区） |
| CoinGecko | 免费密钥 | 加密货币排名、更广泛的加密货币信息 |
| FRED | 免费密钥 | 国内生产总值（GDP）、失业率、利率等经济数据（超过80万个经济指标） |
| Finnhub | 免费密钥 | 实时股票报价、收益数据 |
| Alpha Vantage | 免费密钥 | 股票报价、财务数据（每日数据量限制为25条） |
| 世界银行 | 否 | 全球经济指标（GDP、失业率、通货膨胀率） |

## 如何使用（以`--json`格式输出数据）

当您需要以编程方式解析数据输出时，请使用`--json`选项。请确保将`--json`放在命令之前：

```bash
omd --json quote AAPL
omd --json financials AAPL -p quarterly
omd --json crypto top 10
omd --json macro GDP --limit 5
```

## 配置

API密钥可以通过环境变量或命令行参数进行配置：

```bash
export FRED_API_KEY=your_key
export COINGECKO_API_KEY=your_key
export FINNHUB_API_KEY=your_key
export ALPHA_VANTAGE_API_KEY=your_key
export EDGAR_USER_AGENT="YourCompany you@email.com"

# Or use CLI config
omd config set fredApiKey your_key
omd config set coingeckoApiKey your_key
omd config set finnhubApiKey your_key
omd config set alphaVantageApiKey your_key
omd config show
```

## 数据路由机制

系统会自动选择最合适的数据源来获取数据。如果首选数据源无法使用或达到其数据请求限制，系统会自动切换到下一个可用数据源。您可以使用`--source <数据源名称>`来指定使用特定的数据源。

| 数据类型 | 优先级顺序 |
|---------|-------------------|
| 股票报价 | Yahoo → Finnhub → Alpha Vantage |
| 财务数据 | SEC EDGAR → Yahoo → Alpha Vantage |
| 价格历史 | Yahoo → Alpha Vantage |
| 收益数据 | Yahoo → Finnhub |
| 股息信息 | Yahoo |
| 期权信息 | Yahoo |
| SEC文件提交 | SEC EDGAR |
| 内幕交易信息 | SEC EDGAR |
| 加密货币数据 | Binance → CoinGecko |
| 宏观/经济数据 | FRED → 世界银行 |
| 搜索结果 | SEC EDGAR → Yahoo → Finnhub → Alpha Vantage |