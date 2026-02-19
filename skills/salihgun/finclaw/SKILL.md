---
name: finclaw
description: AI财务助手——提供实时报价、图表、技术分析、投资组合跟踪、价格警报、关注列表、每日简报、宏观经济数据以及针对美国股票、BIST市场、加密货币和外汇的情绪分析服务。
metadata:
  { "openclaw": { "emoji": "📈", "requires": { "bins": ["python3"] }, "install": [{ "id": "setup", "kind": "uv", "package": "yfinance", "bins": ["python3"], "label": "Python 3 required" }] } }
---
# FinClaw — 人工智能财务助手

您的个人财务助手，覆盖 **美国股票**、**BIST（土耳其市场）**、**加密货币** 和 **外汇**。提供投资组合跟踪、价格警报、图表、技术分析、每日简报等功能。

## 首次设置

安装完成后运行一次脚本，以创建 Python 虚拟环境（venv）和数据库：
```bash
python3 {baseDir}/scripts/setup.py
```

然后将该脚本添加到 `openclaw.json` 文件的 `skills.entries` 部分：
```json
"finclaw": {
  "env": {
    "FINNHUB_API_KEY": "",
    "FRED_API_KEY": "",
    "ALPHA_VANTAGE_API_KEY": "",
    "EXCHANGE_RATE_API_KEY": ""
  }
}
```
API 密钥是可选的——核心功能（价格、图表、技术分析、投资组合、警报）无需密钥即可使用。

## 运行脚本

所有脚本均使用该技能对应的 Python 虚拟环境：
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/<script>.py [args]
```

---

## 市场数据

### quote.py — 实时报价
自动根据股票代码识别资产类型。查询结果缓存时间为 60 秒。
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/quote.py AAPL              # US stock
{baseDir}/venv/bin/python3 {baseDir}/scripts/quote.py THYAO.IS          # BIST stock
{baseDir}/venv/bin/python3 {baseDir}/scripts/quote.py BTC               # Crypto
{baseDir}/venv/bin/python3 {baseDir}/scripts/quote.py USD/TRY           # Forex
{baseDir}/venv/bin/python3 {baseDir}/scripts/quote.py AAPL MSFT BTC     # Multiple
{baseDir}/venv/bin/python3 {baseDir}/scripts/quote.py AAPL --force      # Skip cache
{baseDir}/venv/bin/python3 {baseDir}/scripts/quote.py AAPL --json       # JSON output
```

**股票代码识别规则：**
`.IS` → BIST（土耳其市场股票）  
`BTC/ETH/SOL...` → 加密货币  
`USD/TRY` → 外汇  
其他 → 美国股票

### crypto.py — 加密货币市场数据
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/crypto.py price BTC        # Binance price
{baseDir}/venv/bin/python3 {baseDir}/scripts/crypto.py top --limit 10   # Top gainers
{baseDir}/venv/bin/python3 {baseDir}/scripts/crypto.py try BTC          # Price in TRY
```

### forex.py — 汇率数据
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/forex.py rate USD TRY
{baseDir}/venv/bin/python3 {baseDir}/scripts/forex.py convert USD TRY --amount 1000
{baseDir}/venv/bin/python3 {baseDir}/scripts/forex.py multi USD --targets TRY EUR GBP
```

### chart.py — 价格图表
生成 PNG 格式的图表，并将文件发送给用户。
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/chart.py AAPL                           # Candlestick
{baseDir}/venv/bin/python3 {baseDir}/scripts/chart.py BTC --type line --period 1y     # Line chart
{baseDir}/venv/bin/python3 {baseDir}/scripts/chart.py AAPL --sma 20 50 200           # With SMAs
```
可选时间周期：1天、5天、1个月、3个月、6个月、1年、2年、5年

### technical.py — 技术分析
提供简单移动平均线（SMA）、指数移动平均线（EMA）、相对强弱指数（RSI）、MACD 以及买入/卖出信号。
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/technical.py AAPL
{baseDir}/venv/bin/python3 {baseDir}/scripts/technical.py BTC --period 1y --json
```

### news.py — 金融新闻（需要 FINNHUB_API_KEY）
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/news.py company --symbol AAPL
{baseDir}/venv/bin/python3 {baseDir}/scripts/news.py market --category crypto
```

### screener.py — 股票筛选器
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/screener.py us                    # US gainers
{baseDir}/venv/bin/python3 {baseDir}/scripts/screener.py bist --direction bottom  # BIST losers
{baseDir}/venv/bin/python3 {baseDir}/scripts/screener.py crypto --limit 15       # Crypto gainers
```

---

## 投资组合与警报

### portfolio.py — 投资组合管理
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/portfolio.py add --symbol AAPL --shares 10 --price 150
{baseDir}/venv/bin/python3 {baseDir}/scripts/portfolio.py sell --symbol AAPL --shares 5 --price 175
{baseDir}/venv/bin/python3 {baseDir}/scripts/portfolio.py remove --symbol AAPL
{baseDir}/venv/bin/python3 {baseDir}/scripts/portfolio.py list
{baseDir}/venv/bin/python3 {baseDir}/scripts/portfolio.py summary
```
可选参数：
`--fees 1.50`（费用：1.50）
`--date 2024-01-15`（查询日期：2024-01-15）
`--name "Apple Inc"`（查询股票名称：Apple Inc）
`--notes "Long hold"`（查询条件：长期持有）

### alerts.py — 价格警报
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/alerts.py create --symbol AAPL --condition above --target 200
{baseDir}/venv/bin/python3 {baseDir}/scripts/alerts.py create --symbol BTC --condition below --target 60000 --note "Buy signal"
{baseDir}/venv/bin/python3 {baseDir}/scripts/alerts.py list
{baseDir}/venv/bin/python3 {baseDir}/scripts/alerts.py delete --id 3
{baseDir}/venv/bin/python3 {baseDir}/scripts/alerts.py snooze --id 3 --hours 48
```
警报条件：
`above`（价格高于……）
`below`（价格低于……）
`change_pct`（价格变化百分比）
`volume_above`（成交量高于……）

### check_alerts.py — 预警检查脚本（用于定时任务）
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/check_alerts.py
```

### pnl.py — 盈亏统计
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/pnl.py                    # All positions
{baseDir}/venv/bin/python3 {baseDir}/scripts/pnl.py --symbol AAPL      # Single symbol
```

### watchlist.py — 关注列表
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/watchlist.py create --name "Tech"
{baseDir}/venv/bin/python3 {baseDir}/scripts/watchlist.py add --name "Tech" --symbol AAPL
{baseDir}/venv/bin/python3 {baseDir}/scripts/watchlist.py show --name "Tech" --prices
{baseDir}/venv/bin/python3 {baseDir}/scripts/watchlist.py list
```

---

## 智能辅助功能

### briefing.py — 市场简报
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/briefing.py morning    # Full morning briefing
{baseDir}/venv/bin/python3 {baseDir}/scripts/briefing.py close      # End-of-day summary
{baseDir}/venv/bin/python3 {baseDir}/scripts/briefing.py weekend    # Weekend crypto + forex recap
```

### macro.py — 宏观经济分析（需要 FRED_API_KEY）
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/macro.py dashboard
{baseDir}/venv/bin/python3 {baseDir}/scripts/macro.py indicator --name fed_rate
{baseDir}/venv/bin/python3 {baseDir}/scripts/macro.py list
```

### earnings.py — 公司财报日历（需要 FINNHUB_API_KEY）
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/earnings.py calendar
{baseDir}/venv/bin/python3 {baseDir}/scripts/earnings.py symbol --symbol AAPL
```

### sentiment.py — 新闻情绪分析（需要 ALPHA_VANTAGE_API_KEY）
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/sentiment.py --symbol AAPL
{baseDir}/venv/bin/python3 {baseDir}/scripts/sentiment.py --topics technology
```

### research.py — 深度市场研究
```bash
{baseDir}/venv/bin/python3 {baseDir}/scripts/research.py AAPL
```

---

## 数据来源
- **美国股票**：主要数据来源为 Finnhub，备用数据源为 yfinance（无需 API 密钥）
- **BIST（土耳其市场）**：数据来源为 yfinance，股票代码后缀需加 `.IS`（无需 API 密钥）
- **加密货币**：数据来源为 Binance API（无需 API 密钥）
- **外汇**：数据来源为 ExchangeRate-API（无需 API 密钥）
- **图表/技术分析**：使用 matplotlib、mplfinance 和 pandas 进行数据处理（本地计算）
- **新闻**：数据来源为 Finnhub（需要 FINNHUB_API_KEY）
- **宏观经济数据**：数据来源为 FRED（需要 FRED_API_KEY）
- **新闻情绪分析**：数据来源为 Alpha Vantage（需要 ALPHA_VANTAGE_API_KEY）