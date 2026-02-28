---
name: stock-analyzer
description: Analyze Japanese and US stocks, track portfolios, and summarize financial news using Yahoo Finance data. Use when: (1) Fetching stock prices and indicators, (2) Analyzing portfolio performance, (3) Summarizing quarterly earnings reports, (4) Calculating technical analysis indicators.
---

# 股票分析工具

## 概述

这是一个全面的股票分析和投资组合跟踪工具，支持日本和美国市场。该工具与 Yahoo Finance 集成，用于实时数据采集、技术指标计算以及新闻摘要的生成。

## 快速入门

```bash
# Fetch stock data (Japan)
python3 scripts/fetch_yahoo.py --symbol 7203.T --market japan

# Fetch stock data (US)
python3 scripts/fetch_yahoo.py --symbol AAPL --market us

# Analyze portfolio
python3 scripts/analyze.py --portfolio data/portfolio.json

# Calculate technical indicators
python3 scripts/analyze.py --symbol 7203.T --indicators macd,rsi,bollinger
```

## 核心功能

### 1. 数据采集

**日本股票（Yahoo! Finance Japan）**
- 获取 TOPIX 指数成分股的实时价格（符号格式：XXXX.T）
- 提取历史数据（每日/每周/每月）
- 获取公司基本信息和财务报表

**美国股票（Yahoo Finance）**
- 获取 NYSE/NASDAQ 上挂牌的股票数据
- 获取盘前和盘后数据
- 获取 SEC 文件和分析师评级

**使用方法：**
```bash
# Real-time price
python3 scripts/fetch_yahoo.py --symbol 7203.T --realtime

# Historical data
python3 scripts/fetch_yahoo.py --symbol AAPL --period 1y --interval 1d

# Company fundamentals
python3 scripts/fetch_yahoo.py --symbol MSFT --fundamentals
```

### 2. 投资组合跟踪

跟踪多个持股的投资组合表现。

**功能：**
- 每日计算盈亏
- 行业配置分析
- 股息追踪
- 与基准指数进行绩效比较

**投资组合格式（JSON）：**
```json
{
  "holdings": [
    {
      "symbol": "7203.T",
      "shares": 100,
      "avg_cost": 2500,
      "currency": "JPY"
    },
    {
      "symbol": "AAPL",
      "shares": 50,
      "avg_cost": 150,
      "currency": "USD"
    }
  ]
}
```

**使用方法：**
```bash
# Analyze portfolio
python3 scripts/analyze.py --portfolio data/portfolio.json

# Export performance report
python3 scripts/analyze.py --portfolio data/portfolio.json --report performance.md
```

### 3. 新闻与收益摘要

自动汇总相关的财经新闻和收益报告。

**功能：**
- 日本：日经指数、彭博日本、公司新闻稿
- 美国：彭博、路透社、MarketWatch
- 收益电话会议记录分析
- 关键情绪提取

**使用方法：**
```bash
# Get recent news for a stock
python3 scripts/fetch_yahoo.py --symbol 7203.T --news

# Summarize earnings report
python3 scripts/fetch_yahoo.py --symbol AAPL --earnings --quarter 2024Q4

# Sentiment analysis
python3 scripts/analyze.py --symbol 7203.T --sentiment --days 7
```

### 4. 技术分析

计算常用的技术指标，以辅助交易决策。

**支持的指标：** 详见 [references/indicators.md](references/indicators.md)

**使用方法：**
```bash
# Single indicator
python3 scripts/analyze.py --symbol 7203.T --indicator macd

# Multiple indicators
python3 scripts/analyze.py --symbol AAPL --indicators macd,rsi,bollinger,ema

# Generate trading signals
python3 scripts/analyze.py --symbol 7203.T --signals --threshold 70
```

## 资源

### 脚本

**fetch_yahoo.py**
- 从 Yahoo Finance 获取股票数据
- 支持实时数据、历史数据和基本信息
- 参数：`--symbol`（股票代码）、`--market`（日本/美国）、`--period`（数据周期）、`--interval`（数据间隔）、`--news`（是否包含新闻）、`--earnings`（是否包含收益信息）

**analyze.py**
- 进行投资组合分析和技术指标计算
- 计算盈亏、资产配置和各项指标
- 参数：`--portfolio`（投资组合名称）、`--symbol`（股票代码）、`--indicators`（需要分析的指标）、`--sentiment`（情绪分析）、`--signals`（交易信号）

### 参考资料

**indicators.md** - 技术指标的定义和计算方法
- 移动平均线（MA）、指数移动平均线（EMA）、布林带（Bollinger Bands）
- 道氏平均指数（MACD）、相对强弱指数（RSI）、随机振荡器（Stochastic Oscillator）
- 交易信号的解释

**data_sources.md** - 可用的数据来源及其覆盖范围
- 日本：TOPIX、 Mothers、JASDAQ
- 美国：NYSE、NASDAQ、AMEX

## 注意事项

- 日本股票的符号后缀为 `.T`（例如：7203.T 表示丰田股票）
- 美国股票的符号直接使用股票代码（例如：AAPL）
- 货币转换使用 Yahoo Finance 提供的日元/美元汇率
- 美国股票的历史数据从 1970 年开始可用