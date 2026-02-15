---
name: yahooquery
description: 您可以使用 `yahooquery` Python 库来访问 Yahoo Finance 的数据，包括实时价格、基本财务信息、分析师预测、期权信息、新闻以及历史数据。
---

# yahooquery 技能

通过 `yahooquery` Python 库可以全面访问 Yahoo Finance 的数据。该库提供了对几乎所有 Yahoo Finance 端点的程序化访问，包括实时价格、基本财务信息、分析师预测、期权、新闻以及高级研究内容。

## 核心类

### 1. **Ticker**（特定公司的数据）
用于检索一个或多个证券的数据的主要接口。

```python
from yahooquery import Ticker

# Single or multiple symbols
aapl = Ticker('AAPL')
tickers = Ticker('AAPL MSFT NVDA', asynchronous=True)
```

### 2. **Screener**（预定义的股票列表）
提供根据特定条件筛选股票的预构建工具。

```python
from yahooquery import Screener

s = Screener()
screeners = s.available_screeners  # List all available screeners
data = s.get_screeners(['day_gainers', 'most_actives'], count=10)
```

### 3. **Research**（需要高级订阅）
可以访问专有的研究报告和交易策略。

```python
from yahooquery import Research

r = Research(username='you@email.com', password='password')
reports = r.reports(report_type='Analyst Report', report_date='Last Week')
trades = r.trades(trend='Bullish', term='Short term')
```

---

## Ticker 类：数据模块

`Ticker` 类通过属性和方法暴露了数十个数据端点。

### 📊 **财务报表**
- `.income_statement(frequency='a', trailing=True)` - 收益表（年度/季度）
- `.balance_sheet(frequency='a', trailing=True)` - 资产负债表
- `.cash_flow(frequency='a', trailing=True)` - 现金流量表
- `.all_financial_data(frequency='a')` - 综合财务数据及估值指标
- `.valuation_measures` - 不同时期的 EV/EBITDA、P/E、P/B、P/S

### 📈 **价格与市场数据**
- `.price` - 当前价格、市值、52 周价格范围
- `.history(period='1y', interval='1d', start=None, end=None)` - 历史价格走势（OHLC）
  - **period**：`1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`
  - **interval**：`1m`, `2m`, `5m`, `15m`, `30m`, `60m`, `90m`, `1h`, `1d`, `5d`, `1wk`, `1mo`, `3mo`
- `.option_chain` - 完整的期权链（所有到期日）

### 🔍 **分析与预测**
- `.calendar_events` - 下一次收益公布日期、EPS/收入预测
- `.earning_history` - 实际 EPS 与预测 EPS（过去四个季度）
- `.earnings` - 历史季度/年度收益和收入
- `.earnings_trend` - 对未来时期的分析师预测
- `.recommendation_trend` - 随时间变化的买入/卖出/持有评级
- `.gradings` - 最近的分析师评级调整

### 🏢 **公司基本信息**
- `.asset_profile` - 公司地址、行业、所属板块、业务概述、高管信息
- `.company_officers` - 高管及其薪酬详情
- `.summary_profile` - 公司概况信息
- `.key_stats` - 预期 P/E、利润率、贝塔系数、流通股数量
- `.financial_data` - 财务关键指标（ROE、ROA、债务比率）

### 👥 **所有权与治理结构**
- `.insider_holders` - 内部持股者名单及持股情况
- `.insider_transactions` - 内部人员的近期买卖交易
- `.institution_ownership` - 主要机构投资者
- `.fund_ownership` - 主要共同基金持有者
- `.major_holders` - 持股结构（机构投资者占比、内部持股者占比、流通股占比）

### 🌍 **ESG 与评级**
- `.esg_scores` - 环境、社会、治理评分及争议事项
- `.recommendation_rating` - 分析师共识（强烈买入 → 强烈卖出）

### 📰 **新闻与洞察**
- `.news()` - 最新新闻文章
- `.technical_insights` - 技术分析趋势（看涨/看跌）

### 💰 **仅限基金与 ETF**
- `.fund_holding_info` - 主要持仓、债券/股票构成
- `.fund_performance` - 历史表现和回报
- `.fund_bond_holdings` / `.fund_bond_ratings` - 债券到期日和信用评级
- `.fund_equity_holdings` - 股票的 P/E、P/B、P/S

### 📊 **其他模块**
- `.summary_detail` - 交易统计数据（当日最高/最低价、成交量、平均成交量）
- `.default_key_statistics` - 企业价值、历史 P/E、预期 P/E
- `.index_trend` - 相对于基准指数的表现
- `.quote_type` - 证券类型、交易所、市场

---

## 全局函数

```python
import yahooquery as yq

# Search
results = yq.search('NVIDIA')

# Market Data
market = yq.get_market_summary(country='US')  # Major indices snapshot
trending = yq.get_trending(country='US')  # Trending tickers

# Utilities
currencies = yq.get_currencies()  # List of supported currencies
exchanges = yq.get_exchanges()  # List of exchanges
rate = yq.currency_converter('USD', 'EUR')  # Exchange rate
```

---

## 配置与关键字参数

`Ticker`、`Screener` 和 `Research` 类接受以下可选参数：

### 性能与可靠性
- `asynchronous=True` - 异步请求（针对多个证券）
- `max_workers=8` - 并行工作的线程数（异步时使用）
- `retry=5` - 重试次数
- `backoff_factor=0.3` - 重试之间的指数退避时间
- `status_forcelist=[429, 500, 502, 503, 504]` - 需要重试的 HTTP 状态码
- `timeout=5` - 请求超时时间（秒）

### 数据格式与验证
- `formatted=False` - 如果设置为 `True`，返回的数据结构为 `{raw, fmt, longFmt`
- `validate=True` - 实例化时验证证券代码（无效代码返回 `.invalid_symbols`
- `country='United States'` - 数据/新闻的区域设置（法国、德国、加拿大等）

### 网络与认证
- `proxies={'http': 'http://proxy:port'}` - HTTP/HTTPS 代理
- `user_agent='...'` - 自定义用户代理字符串
- `verify=True` - SSL 证书验证
- `username='you@email.com` / `password='...'` - Yahoo Finance 高级订阅登录信息

### 高级功能（共享会话）
- `session=...` / `crumb=...` - 在 `Research` 和 `Ticker` 实例之间共享认证信息

---

## 最佳实践

### 1. **多个证券的异步处理**
```python
tickers = Ticker('AAPL MSFT NVDA TSLA', asynchronous=True)
prices = tickers.price  # Returns dict keyed by symbol
```

### 2. **处理 DataFrame**
大多数财务方法返回 `pandas.DataFrame`。若需转换为 JSON 格式，请执行以下操作：
```python
df = aapl.income_statement()
print(df.to_json(orient='records', date_format='iso'))
```

### 3. **历史数据 - 1 分钟间隔**
Yahoo Finance 每次请求限制获取 1 分钟内的数据。如需获取 30 天的数据：
```python
tickers = Ticker('AAPL', asynchronous=True)
df = tickers.history(period='1mo', interval='1m')  # Makes 4 requests automatically
```

### 4. **高级用户：结合 Research 与 Ticker 使用**
```python
r = Research(username='...', password='...')
reports = r.reports(sector='Technology', investment_rating='Bullish')

# Reuse session for Ticker
tickers = Ticker('AAPL', session=r.session, crumb=r.crumb)
data = tickers.asset_profile
```

---

## 常见用例

### 投资组合分析
```python
portfolio = Ticker('AAPL MSFT NVDA', asynchronous=True)
summary = portfolio.summary_detail
earnings = portfolio.earnings
history = portfolio.history(period='1y')
```

### 筛选与发现
```python
s = Screener()
gainers = s.get_screeners(['day_gainers'], count=20)
# Returns DataFrame with price, volume, % change, etc.
```

### 期权分析
```python
nvda = Ticker('NVDA')
options = nvda.option_chain
# Filter for calls/puts, strikes, expirations
```

### 收益公布日历
```python
tickers = Ticker('AAPL MSFT NVDA')
calendar = tickers.calendar_events
# Shows next earnings date + analyst estimates
```

---

## 参考文档

完整 API 文档位于：`/Users/henryzha/.openclaw/workspace-research/skills/yahooquery/references/`

- `index.md` - 类与函数概述
- `ticker/` - 所有 Ticker 方法的详细说明
- `screener.md` - Screener 类使用指南
- `research.md` - Research 类（高级功能）
- `keyword_arguments.md` - 完整的配置选项列表
- `misc.md` - 全局辅助函数
- `advanced.md` - 在 Research 和 Ticker 之间共享会话

---

## 环境要求

- **安装**：`python3 -m pip install yahooquery`
- **依赖库**：pandas, requests-futures, tqdm, beautifulsoup4, lxml
- **Python 版本**：3.7+

---

## 注意事项

- Yahoo Finance 可能会对请求进行速率限制或屏蔽。请使用 `retry`, `backoff_factor`, `status_forcelist` 以确保请求的稳定性。
- 高级功能（Research 类）需要付费的 Yahoo Finance 高级订阅。
- 数据的准确性和可用性取决于 Yahoo Finance 的上游数据提供者。