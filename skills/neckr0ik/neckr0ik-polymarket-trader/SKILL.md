---
name: neckr0ik-polymarket-trader
version: 1.0.0
description: 在 Polymarket 上检测套利机会。监控价差套利、跨市场相关性以及由新闻引发的投资机会。可用于预测市场交易和发现无风险获利机会。
---
# Polymarket套利检测器

在Polymarket上检测无风险的套利机会。

## 快速入门

```bash
# Scan all markets for arbitrage opportunities
neckr0ik-polymarket-trader scan

# Monitor specific market for spreads
neckr0ik-polymarket-trader monitor --market "will-trump-declare-war"

# Find cross-platform arbitrage
neckr0ik-polymarket-trader cross-platform --markets bitcoin-100k

# Correlate news with markets
neckr0ik-polymarket-trader news --keywords "Israel,Iran,war"
```

## 该检测器能发现什么

### 1. 直接价差套利
当“YES”和“NO”的价格之和不等于1.00美元时。

```
Example:
YES: $0.48
NO: $0.50
Combined: $0.98
Profit: $0.02 (2.04% risk-free)
```

### 2. 跨市场相关性
价格不一致的相关市场。

```
Example:
"Trump wins 2026?" @ 55%
"Republican wins?" @ 48%
→ Logically impossible. Trump > Republican shouldn't happen.
```

### 3. 新闻驱动的套利机会
突发新闻与市场价格之间的差异。

```
Example:
News: "Israel strikes Tehran. Trump demands surrender."
Market: "Will Trump declare war on Iran?" @ 40%
Signal: Military action ≠ war declaration. May be overpriced.
```

### 4. 跨平台套利
Polymarket与Kalshi平台上的相同事件。

```
Example:
Polymarket: "BTC > $100k by EOY" YES @ 0.55
Kalshi: Same market YES @ 0.62
→ Buy Polymarket, sell Kalshi. 7% locked profit.
```

### 5. 靠近解决阶段的套利机会
那些结果几乎可以确定的套利机会。

```
Example:
Market resolves in 48 hours
Current price: $0.97
Buy and hold to $1.00
→ 3% profit in 2 days (548% annualized)
```

## 命令

### scan
扫描所有市场以寻找套利机会。

```bash
neckr0ik-polymarket-trader scan [options]

Options:
  --min-spread <pct>    Minimum spread percentage (default: 2)
  --max-results <n>     Max results to return (default: 20)
  --output <format>     Output format (table, json, csv)
```

### monitor
持续监控特定市场。

```bash
neckr0ik-polymarket-trader monitor --market <id> [options]

Options:
  --interval <sec>      Check interval (default: 5)
  --alert-spread <pct>  Alert when spread exceeds threshold
  --webhook <url>       Send alerts to webhook
```

### cross-platform
比较不同平台上的价格。

```bash
neckr0ik-polymarket-trader cross-platform [options]

Options:
  --platforms <list>    Platforms to compare (polymarket,kalshi)
  --min-spread <pct>    Minimum spread (default: 3)
```

### news
将突发新闻与市场行情进行关联分析。

```bash
neckr0ik-polymarket-trader news --keywords <terms> [options]

Options:
  --sources <list>      News sources (reuters,ap,cnbc,bbc)
  --market-keywords <list>  Polymarket search terms
  --alert               Send alerts on correlation
```

### endgame
寻找那些接近解决阶段的套利机会。

```bash
neckr0ik-polymarket-trader endgame [options]

Options:
  --min-prob <pct>      Minimum probability (default: 95)
  --max-days <n>        Max days to resolution (default: 7)
  --min-roi <pct>       Minimum annualized ROI (default: 100)
```

## 输出示例

### 价差套利检测结果

```
ARBITRAGE FOUND
Market: Will Bitcoin reach $100k by EOY 2026?
YES Price: $0.48
NO Price: $0.50
Spread: 2.0% ($0.02)
Volume: $1.2M
Profit/Trade: $20 per $1,000
Annualized: 548% (if held 2 days)
```

### 跨市场相关性结果

```
CORRELATION VIOLATION
Market 1: "Will Trump win 2026?" @ 55%
Market 2: "Will a Republican win?" @ 48%
Issue: Trump winning implies Republican wins
Logic: Market 1 should be <= Market 2
Action: Sell Market 1 YES, Buy Market 2 NO
```

### 新闻相关性结果

```
NEWS-MARKET CORRELATION
Breaking News: "Israel strikes Tehran. Trump demands surrender."
Related Markets:
  1. "Will Trump declare war on Iran?" @ 40% → May be OVERPRICED
  2. "Will Israel strike Lebanon?" @ 85% → Already occurred
  3. "Will oil hit $100?" @ 25% → May be UNDERPRICED
Signal: Military action ≠ formal war declaration
```

## 风险管理

- **价差阈值：** 仅交易价差超过2%（扣除费用后的价格）的套利机会。
- **持仓限制：** 每个市场的持仓比例不超过投资组合的10%。
- **市场选择标准：** 避免选择价格波动较大的市场。
- **执行速度：** 使用WebSocket进行实时通信，而非轮询方式。

## 技术细节

### 检测速度要求

| 方法 | 检测时间 | 执行速度 |
|--------|---------------|-----------|
| 手动检测 | 分钟 | 秒 |
| 半自动检测 | 秒 | 需人工干预 |
| 全自动机器人 | 毫秒 | 小于100毫秒 |

### 费用结构

| 平台 | 费用 |
|----------|-----|
| Polymarket US | 0.01% |
| Polymarket International | 赚利部分的2% |
| Polygon网络手续费 | 约0.007美元 |

## 参考资料

- `references/polymarket-strategies.md` — 完整的策略指南
- `scripts/arbitrage_detector.py` — 套利检测引擎
- `scripts/news_correlator.py` — 新闻与市场相关性分析工具