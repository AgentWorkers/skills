---
name: stock-analysis
description: 使用 Yahoo Finance 的数据来分析股票和加密货币。支持投资组合管理、带有提醒的功能列表、股息分析、八维股票评分系统、热门趋势检测（Hot Scanner）以及谣言/早期信号检测。适用于股票分析、投资组合跟踪、收益反应监测、加密货币监控、追踪热门股票，或在谣言尚未被广泛传播之前就发现它们。
version: 6.2.0
homepage: https://finance.yahoo.com
commands:
  - /stock - Analyze a stock or crypto (e.g., /stock AAPL)
  - /stock_compare - Compare multiple tickers
  - /stock_dividend - Analyze dividend metrics
  - /stock_watch - Add/remove from watchlist
  - /stock_alerts - Check triggered alerts
  - /stock_hot - Find trending stocks & crypto (Hot Scanner)
  - /stock_rumors - Find early signals, M&A rumors, insider activity (Rumor Scanner)
  - /portfolio - Show portfolio summary
  - /portfolio_add - Add asset to portfolio
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["uv"],"env":[]},"install":[{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"}]}}
---

# 股票分析 v6.1

该工具支持对美国股票和加密货币进行8维分析，包括投资组合管理、关注列表、警报功能、股息分析以及**病毒式趋势检测**。

## v6.2的新功能

- 🔮 **谣言扫描器** — 在主流新闻之前捕捉早期信号：
  - 合并收购传闻
  - 内部人士的买卖行为
  - 分析师的评级调整
  - 通过Twitter/X检测到的“听说...”、“消息来源称...”等言论
- 🎯 **影响评分** — 根据谣言对市场潜在影响进行排名

## v6.1的功能

- 🔥 **热门股票/加密货币扫描器** — 从多个来源筛选热门股票和加密货币
- 🐦 **Twitter/X集成** — 通过bird CLI获取社交情绪数据
- 📰 **多源数据聚合** — 从CoinGecko、Google News、Yahoo Finance获取信息
- ⏰ **定时报告** — 每日趋势报告

## v6.0的功能

- 🆕 **关注列表 + 警报** — 设置价格目标、止损点及信号变化通知
- 🆕 **股息分析** — 提供股息收益率、派息率、增长情况等指标
- 🆕 **快速模式** — 使用`--fast`选项可跳过耗时的分析（如内部人士交易、新闻相关分析）
- 🆕 **性能提升** — 使用`--no-insider`选项可加快运行速度

## 快速命令

### 股票分析
```bash
# Basic analysis
uv run {baseDir}/scripts/analyze_stock.py AAPL

# Fast mode (skips insider trading & breaking news)
uv run {baseDir}/scripts/analyze_stock.py AAPL --fast

# Compare multiple
uv run {baseDir}/scripts/analyze_stock.py AAPL MSFT GOOGL

# Crypto
uv run {baseDir}/scripts/analyze_stock.py BTC-USD ETH-USD
```

### 股息分析（v6.0新增功能）
```bash
# Analyze dividends
uv run {baseDir}/scripts/dividends.py JNJ

# Compare dividend stocks
uv run {baseDir}/scripts/dividends.py JNJ PG KO MCD --output json
```

**股息指标：**
- 股息收益率及年度派息金额
- 派息率（低风险/中等风险/高风险/不可持续）
- 五年股息增长率（复合年增长率）
- 连续增长年份
- 安全评分（0-100分）
- 收入评级（优秀/良好/中等/较差）

### 关注列表 + 警报（v6.0新增功能）
```bash
# Add to watchlist
uv run {baseDir}/scripts/watchlist.py add AAPL

# With price target alert
uv run {baseDir}/scripts/watchlist.py add AAPL --target 200

# With stop loss alert
uv run {baseDir}/scripts/watchlist.py add AAPL --stop 150

# Alert on signal change (BUY→SELL)
uv run {baseDir}/scripts/watchlist.py add AAPL --alert-on signal

# View watchlist
uv run {baseDir}/scripts/watchlist.py list

# Check for triggered alerts
uv run {baseDir}/scripts/watchlist.py check
uv run {baseDir}/scripts/watchlist.py check --notify  # Telegram format

# Remove from watchlist
uv run {baseDir}/scripts/watchlist.py remove AAPL
```

**警报类型：**
- 🎯 **达到目标价格** — 价格达到设定目标
- 🛑 **触及止损点** — 价格低于止损点
- 📊 **信号变化** — 买入/持有/卖出信号发生变化

### 投资组合管理
```bash
# Create portfolio
uv run {baseDir}/scripts/portfolio.py create "Tech Portfolio"

# Add assets
uv run {baseDir}/scripts/portfolio.py add AAPL --quantity 100 --cost 150
uv run {baseDir}/scripts/portfolio.py add BTC-USD --quantity 0.5 --cost 40000

# View portfolio
uv run {baseDir}/scripts/portfolio.py show

# Analyze with period returns
uv run {baseDir}/scripts/analyze_stock.py --portfolio "Tech Portfolio" --period weekly
```

### 🔥 热门股票/加密货币扫描器（v6.1新增功能）
```bash
# Full scan - find what's trending NOW
python3 {baseDir}/scripts/hot_scanner.py

# Fast scan (skip social media)
python3 {baseDir}/scripts/hot_scanner.py --no-social

# JSON output for automation
python3 {baseDir}/scripts/hot_scanner.py --json
```

**数据来源：**
- 📊 CoinGecko热门加密货币排行榜 — 前15种热门加密货币
- 📈 CoinGecko涨幅最大的加密货币
- 📰 Google News — 金融与加密货币新闻
- 📉 Yahoo Finance — 表现最佳的加密货币
- 🐦 Twitter/X — 通过认证获取社交情绪数据

**输出结果：**
- 按提及次数排序的热门股票/加密货币
- 24小时内的加密货币价格变动情况
- 按类别划分的股价变动股票
- 带有股票代码的突发新闻

**Twitter设置（可选）：**
1. 安装bird：`npm install -g @steipete/bird`
2. 在Safari/Chrome浏览器中登录x.com
3. 创建`.env`文件，设置`AUTH_TOKEN`和`CT0`环境变量

### 🔮 谣言扫描器（v6.2新增功能）
```bash
# Find early signals, M&A rumors, insider activity
python3 {baseDir}/scripts/rumor_scanner.py
```

**扫描内容：**
- 🏢 **合并收购传闻** — 合并、收购、收购要约
- 👔 **内部人士交易** — 首席执行官/董事的买卖行为
- 📊 **分析师动作** — 评级调整、价格目标变更
- 🐦 **Twitter上的言论** — “听说...”、“消息来源称...”等
- ⚖️ **美国证券交易委员会（SEC）动态** — 相关调查和文件

**影响评分：**
- 根据谣言对市场潜在影响进行评分（1-10分）
- 合并收购/收购要约：+5分
- 内部人士交易：+4分
- 评级调整：+3分
- “听说...”/“消息来源称...”：+2分
- 高参与度：+2分

**最佳使用建议：** 在美国市场开盘前（07:00）运行该工具，以捕捉市场前期的信号。

## 分析维度（股票8个维度，加密货币3个维度）

### 股票
| 维度 | 权重 | 描述 |
|-----------|--------|-------------|
| 盈利惊喜 | 30% | 实际每股收益是否超出预期 |
| 基本面 | 20% | 市盈率、利润率、增长情况 |
| 分析师观点 | 20% | 分析师评级、价格目标 |
| 历史表现 | 10% | 过往的盈利反应 |
| 市场环境 | 10% | VIX指数、SPY指数/QQQ指数走势 |
| 行业 | 15% | 行业相对强弱 |
| 动量 | 15% | 相对强弱指数（RSI）、52周价格波动范围 |
| 情绪指标 | 10% | 市场恐慌/贪婪情绪、空头持仓情况 |

### 加密货币
- 市值及类别
- BTC相关性（30天）
- 动量（相对强弱指数、价格波动范围）

## 情绪指标

| 指标 | 来源 | 信号含义 |
|-----------|--------|--------|
| 恐慌/贪婪情绪 | CNN | 相反交易策略（恐慌时买入）
- 空头持仓 | Yahoo | 空头挤压潜力 |
| VIX指数结构 | 期货市场 | 市场压力检测 |
| 内部人士交易 | 美国证券交易委员会（SEC）EDGAR数据库 | 智能资金动向 |
| 看跌/看涨期权比例 | 期权市场 | 情绪极端情况

## 风险检测

- ⚠️ **财报发布前** — 如果距离财报发布时间少于14天，会发出警告
- ⚠️ **价格飙升后** — 如果价格在5天内上涨超过15%，会发出警报
- ⚠️ **超买** — 相对强弱指数（RSI）超过70且接近52周高点
- ⚠️ **风险警示** — GLD/TLT/UUP等资产价格同时上涨
- ⚠️ **地缘政治风险** — 关注台湾、中国、俄罗斯、中东等地区的政治动态
- ⚠️ **突发新闻** — 过去24小时内出现的危机相关新闻

## 性能选项

| 标志 | 效果 | 执行速度 |
|------|--------|-------|
| （默认） | 完整分析 | 5-10秒 |
| `--no-insider` | 跳过SEC EDGAR数据 | 3-5秒 |
| `--fast` | 跳过内部人士交易和新闻相关分析 | 2-3秒 |

## 支持的加密货币（前20种）

BTC, ETH, BNB, SOL, XRP, ADA, DOGE, AVAX, DOT, MATIC, LINK, ATOM, UNI, LTC, BCH, XLM, ALGO, VET, FIL, NEAR

（使用`-USD`后缀表示货币对，例如：`BTC-USD`）

## 数据存储

| 文件 | 存储位置 |
|------|----------|
| 投资组合数据 | `~/.clawdbot/skills/stock-analysis/portfolios.json` |
| 关注列表数据 | `~/.clawdbot/skills/stock-analysis/watchlist.json` |

## 限制事项

- Yahoo Finance的数据可能存在15-20分钟的延迟
- 空头持仓数据可能滞后约2周（根据FINRA规定）
- 内部人士交易数据可能滞后2-3天（根据SEC文件更新）
- 仅支持美国市场数据（非美国市场的信息可能不完整）
- 突发新闻数据采用1小时缓存机制，基于关键词筛选

## 免责声明

⚠️ 本工具仅用于提供信息参考，不构成金融建议。在做出投资决策前，请咨询持牌金融顾问。