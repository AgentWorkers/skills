---
name: google-finance
description: "**按计划从 Google Finance 获取股票价格和公司新闻**  
适用于用户需要监控股票行情、获取买卖建议、查看价格变动、关注公司新闻、设置股票提醒或跟踪投资组合中的股票的情况。  
可触发操作：`track stock`、`watch AAPL`、`stock alert`、`buy or sell`、`stock news`、`Google Finance`。  
默认关注列表：NVDA、AAPL、META、GOOGL。"
homepage: https://finance.google.com
user-invocable: true
metadata: {"clawdbot": {"emoji": "📈", "requires": {"bins": ["python3"]}, "os": ["darwin", "linux", "win32"], "files": ["scripts/parse-stock.py"]}}
---
# 股票跟踪器

监控股票价格，生成买入/卖出信号，并追踪您的投资组合。

## 快速入门

**查看所有关注的股票（自动获取数据）：**
```bash
python3 {baseDir}/scripts/parse-stock.py --check --summary
```

**查看单只股票：**
```bash
python3 {baseDir}/scripts/parse-stock.py --check --symbol AAPL
```

**添加/删除股票：**
```bash
python3 {baseDir}/scripts/parse-stock.py --add TSLA
python3 {baseDir}/scripts/parse-stock.py --remove TSLA
```

**显示关注列表：**
```bash
python3 {baseDir}/scripts/parse-stock.py --list
```

---

## 工作原理

`parse-stock.py` 脚本负责所有操作：

1. **从 Google Finance 获取数据**（无需 API 密钥！）
2. **根据股票 momentum、成交量和估值计算评分**
3. **生成买入/持有/卖出的信号**
4. **更新 `~/.openclaw/workspace/stock-tracker-state.json` 文件中的状态信息**

### 分析框架

使用 `{baseDir}/references/analysis-framework.md` 中提供的评分框架进行股票分析：

```
Symbol: AAPL
Price: $182.30  (+1.4% today)
Signal: BUY  [score: +6/10]
Confidence: MEDIUM

Key factors:
  ✅ Price above 50-day SMA (estimated)
  ✅ Volume 1.3× above average
  ✅ 2 positive news items in past 24h
  ⚠️  P/E 28.5 — elevated but within sector norm
  ❌ Within 3% of 52-week high (limited upside)

Recent headlines:
  • "Apple reportedly in talks with..." — Reuters (2h ago)
  • "iPhone sales beat estimates..." — Bloomberg (5h ago)

Recommendation: Consider buying on dips. Set stop-loss at 5% below current price.
```

### 4. 保存状态信息

将关注列表和最新价格保存在 `~/.openclaw/workspace/stock-tracker-state.json` 文件中。

**默认关注列表**（如果状态文件不存在，则在首次运行时自动加载）：
- `NVDA:NASDAQ` — NVIDIA
- `AAPL:NASDAQ` — Apple
- `META:NASDAQ` — Meta Platforms
- `GOOGL:NASDAQ` — Alphabet (Google)

文件格式：
```json
{
  "watchlist": ["NVDA:NASDAQ", "AAPL:NASDAQ", "META:NASDAQ", "GOOGL:NASDAQ"],
  "lastChecked": "2026-03-03T09:00:00Z",
  "snapshots": {
    "NVDA:NASDAQ": { "price": 875.40, "change_pct": 2.1, "ts": "2026-03-03T09:00:00Z" },
    "AAPL:NASDAQ": { "price": 182.30, "change_pct": 1.4, "ts": "2026-03-03T09:00:00Z" },
    "META:NASDAQ": { "price": 512.60, "change_pct": -0.8, "ts": "2026-03-03T09:00:00Z" },
    "GOOGL:NASDAQ": { "price": 175.20, "change_pct": 0.5, "ts": "2026-03-03T09:00:00Z" }
  }
}
```

在每次运行时加载状态信息，并将当前价格与上次记录的价格进行比较，以计算价格变化。

### 5. 发出重要价格变动警报

当出现以下任一情况时，会发出警报：
- 价格变化超过 ±3%
- 成交量超过 30 天平均成交量的 2 倍
- 任何新闻标题包含以下关键词：`earnings`（收益）、`merger`（合并）、`acquisition`（收购）、`SEC`（美国证券交易委员会）、`lawsuit`（诉讼）、`recall`（产品召回）、`CEO`（首席执行官）、`bankruptcy`（破产）

---

## 设置 Cron 计划

运行以下命令，设置一个定期任务，在每个工作日的市场开盘时间（美国东部时间 09:30）和收盘时间（16:00）检查股票价格：

```bash
# Market open — 09:30 ET (UTC-4 during EDT)
openclaw cron add \
  --name "Stock Open Check" \
  --cron "30 13 * * 1-5" \
  --tz "America/New_York" \
  --session isolated \
  --message "Run /stock-tracker check and output a full report with buy/sell signals for all watched stocks." \
  --announce \
  --channel slack \
  --to "channel:REPLACE_WITH_CHANNEL_ID"

# Market close — 16:00 ET
openclaw cron add \
  --name "Stock Close Check" \
  --cron "0 20 * * 1-5" \
  --tz "America/New_York" \
  --session isolated \
  --message "Run /stock-tracker check and output end-of-day summary with buy/sell signals for all watched stocks." \
  --announce
```

如需每 4 小时检查一次股票价格（包括盘后时间），请运行以下命令：
```bash
openclaw cron add \
  --name "Stock Tracker" \
  --every 14400000 \
  --session isolated \
  --message "Run /stock-tracker check for all watched symbols. Report price changes > 1%, news, and signals."
```

有关时区和交易所营业时间的详细信息，请参阅 `{baseDir}/references/data-sources.md`。

---

## 输出格式规则

- 始终显示：股票代码、价格、价格变化百分比、信号类型（买入、持有、卖出）
- 如果有多只股票，按信号类型分组显示（买入优先，然后是持有，最后是卖出）
- 使用表情符号表示信号类型：🟢 买入 / 🟡 持有 / 🔴 卖出
- 对于超过阈值的股票，后面加上 `⚠️ 警报`
- 每份报告结尾都会附有免责声明：*“本工具提供的信息不构成投资建议。数据来源于 Google Finance。”*

---

## 限制与注意事项

- Google Finance 不提供实时二级市场数据；某些交易所的股票价格可能会有 15 分钟的延迟。
- 该工具无法执行实际交易，仅提供参考建议。
- 对于非美国市场的股票，请使用相应的交易所后缀（例如 `0700.HK`、`7203.T`、`BABA.N`）。详细信息请参见 `data-sources.md`。
- 如果 Google Finance 取消了浏览器会话，系统会切换到 `data-sources.md` 中描述的 Yahoo Finance 数据源进行数据抓取。

---

## 外部接口

该工具仅向以下公共 URL 发送请求：

| URL | 用途 |
|-----|---------|
| `https://www.google.com/finance/quote/*` | 获取股票价格和统计信息 |

不会向任何外部接口发送用户数据、凭证或个人信息。

---

## 安全性与隐私

- **无需输入任何凭证。** 所有数据均来自公开的 Google Finance 页面。
- **数据仅存储在本地。** 关注列表和价格信息仅保存在您机器上的 `~/.openclaw/workspace/stock-tracker-state.json` 文件中，不会发送到远程服务器。
- **无需使用浏览器。** 数据通过 HTTP 请求获取，并从 HTML 页面中解析。
- `parse-stock.py` 脚本被限制在指定的工作目录内运行，仅读取/写入状态文件，不会访问环境变量或其他文件。
- **买入/卖出信号仅基于分析结果生成。** 任何财务数据或交易决策都不会被发送到外部。所有分析都在本地完成。