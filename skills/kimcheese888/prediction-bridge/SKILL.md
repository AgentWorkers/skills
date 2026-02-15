---
name: prediction-bridge
description: 从 Prediction Bridge API 查询实时预测市场数据。当用户询问关于预测市场、赛事赔率、市场价格、大额交易（whale trades）、交易者分析或与预测市场相关的新闻时，可以使用该功能。该服务支持在 9 个以上平台上进行语义搜索（Polymarket、Kalshi、Limitless、Probable、PredictFun、SxBet、Myriad、PancakeSwap），并提供链上大额交易监控、智能盈亏（Smart PnL）分析以及交易者排行榜等功能。请运行捆绑的 Python 脚本来获取实时数据。
---

# Prediction Bridge

通过 Prediction Bridge API，您可以查询来自 9 个以上平台的实时预测市场数据。

## 使用方法

在 `scripts/prediction_bridge.py` 脚本中运行相应的命令。该脚本仅使用 Python 标准库，无需安装任何第三方库（如 pip）。

```bash
python scripts/prediction_bridge.py <command> [args] [options]
```

## 命令

### 按事件含义搜索

```bash
python scripts/prediction_bridge.py search "trump tariff" --limit 5
python scripts/prediction_bridge.py search "will bitcoin hit 100k"
python scripts/prediction_bridge.py search "2028 election" --include-inactive
```

### 浏览事件

```bash
python scripts/prediction_bridge.py events --limit 10
python scripts/prediction_bridge.py events --source polymarket --limit 5
python scripts/prediction_bridge.py events --status active --category "Crypto"
python scripts/prediction_bridge.py event 1839                          # detail by ID
```

### 与事件相关的新闻

```bash
python scripts/prediction_bridge.py news --limit 10
```

### 平台统计信息

```bash
python scripts/prediction_bridge.py stats
```

### 大额交易（链上交易）

```bash
python scripts/prediction_bridge.py whale-trades --limit 10
python scripts/prediction_bridge.py whale-trades --address 0x1234...    # by wallet
python scripts/prediction_bridge.py whale-trades --min-value 50000      # min USD
python scripts/prediction_bridge.py whale-trades --only-alerts          # above alert threshold
python scripts/prediction_bridge.py whale-trades --event-slug "us-election"
```

### 市场价格数据

```bash
python scripts/prediction_bridge.py market-history polymarket 18454
python scripts/prediction_bridge.py market-candles polymarket 18454 --interval 1h
```

### 分析工具

```bash
python scripts/prediction_bridge.py smart-pnl 18454                    # market Smart PnL
python scripts/prediction_bridge.py top-holders 18454                   # top holders breakdown
python scripts/prediction_bridge.py leaderboard --limit 20              # top traders
python scripts/prediction_bridge.py user-summary 0x1234...              # wallet portfolio
python scripts/prediction_bridge.py user-pnl 0x1234...                  # realized PnL
```

### 其他功能

```bash
python scripts/prediction_bridge.py languages                           # supported languages
python scripts/prediction_bridge.py --help                              # full help
```

## 常见使用场景

**“当前最热门的预测市场有哪些？”**
→ `events --limit 10`（按交易量排序）

**“查找关于 AI 监管的新闻”**
→ `search "AI regulation"`（语义搜索）

**“显示 Polymarket 上的最新大额交易”**
→ `whale-trades --limit 10`

**“哪些是顶级交易者？他们正在投注什么？”**
→ 先使用 `leaderboard --limit 10` 查看排行榜，然后使用 `user-summary <address>` 查看详细信息

**“某个市场的智能盈亏（Smart PnL）信号是什么？”**
→ 先从 `event <id>` 获取市场 ID，然后使用 `smart-pnl <market_id>`

**“今天有哪些影响预测市场的新闻？”**
→ `news --limit 10`

## 环境配置

您可以通过设置 `PREDICTION_BRIDGE_URL` 来覆盖默认的 API 基本地址：

```bash
export PREDICTION_BRIDGE_URL=https://prediction-bridge.onrender.com
```