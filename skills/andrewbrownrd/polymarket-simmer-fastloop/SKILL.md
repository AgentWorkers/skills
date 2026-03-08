---
name: polymarket-simmer-fastloop
displayName: Polymarket Simmer FastLoop Trader
description: 在 Polymarket 平台上，您可以进行 BTC/ETH/SOL 货币对的交易，使用 5 分钟或 15 分钟的快速交易机制，并具备动量分析功能以及订单簿筛选功能。
version: "1.1.0"
author: "Xuano47"
tags: ["polymarket", "trading", "btc", "eth", "sol"]
env:
  - SIMMER_API_KEY
  - TRADING_VENUE
---
# Polymarket Simmer FastLoop Trader

这是一个用于Polymarket BTC/ETH/SOL市场的自动化交易策略，适用于5分钟和15分钟的快速交易时段。该策略采用均值回归策略，并结合动量衰竭检测、订单簿不平衡确认以及基于波动性的头寸调整机制。

> **默认模式为模拟交易（Paper mode）**。如需进行真实交易，请使用`--live`参数。

## 策略原理

当最新的5分钟蜡烛图显示价格快速上涨（动量超过阈值）时，脚本会买入反向头寸，以捕捉价格回调的机会。信号筛选条件包括：

- **动量（Momentum）**：使用Binance的1分钟蜡烛图数据，可配置阈值（默认为1.0%）。
- **订单簿不平衡（Order Book Imbalance）**（可选）：通过分析Binance L2订单簿的前20个层次来确定市场趋势。
- **NOFX机构净流量（NOFX Institutional Netflow）**：根据机构投资者的交易数据来筛选交易。
- **时间过滤（Time-of-Day Filter）**：默认会跳过交易量较低的时段（02:00–06:00 UTC）。
- **费用平衡条件（Fee-Accurate EV）**：仅在执行价格与费用平衡点之间的交易时才进行交易。
- **基于波动性的头寸调整（Volatility-Adjusted Sizing）**：在波动性较高时自动减少头寸规模。

## 设置步骤

### 1. 获取Simmer API密钥

- 在[simmer.markets](https://simmer.markets)注册账号。
- 进入**控制面板（Dashboard）** -> **SDK**选项卡。
- 复制您的API密钥：`export SIMMER_API_KEY="your-key-here"`。

### 必需的环境变量

| 变量 | 是否必需 | 说明 | 值 |
|----------|----------|-------------|--------|
| `SIMMER_API_KEY` | 是 | 您的Simmer SDK密钥 | 从[simmer.markets](https://simmer.markets)获取 |
| `TRADING_VENUE` | 是 | 执行环境 | `simmer`（模拟交易）或`polymarket`（真实交易） |
| `WALLET_PRIVATE_KEY` | 可选 | 您的Polymarket钱包密钥 | 仅在`TRADING_VENUE="polymarket"`时需要 |

- **`simmer`**（默认）：模拟交易模式，使用虚拟资金进行交易，无需实际使用USDC。
- **`polymarket`**：真实交易模式，需要连接到Polymarket市场，并确保钱包中持有USDC。

> [警告！]
> 请勿泄露您的`WALLET_PRIVATE_KEY`或`SIMMER_API_KEY`。SDK会在本地执行交易，您的私钥不会被传输。

## 快速入门

```bash
pip install simmer-sdk
export SIMMER_API_KEY="your-key-here"

# Paper mode (default)
python polymarket-simmer-fastloop.py

# Live trading
python polymarket-simmer-fastloop.py --live

# Check win rate and P&L stats
python polymarket-simmer-fastloop.py --stats

# Resolve expired trades against real outcomes
python polymarket-simmer-fastloop.py --resolve

# Quiet mode for cron
python polymarket-simmer-fastloop.py --live --quiet
```

## 定时任务设置

**使用OpenClaw：**
```bash
openclaw cron add \
  --name "Simmer FastLoop" \
  --cron "*/5 * * * *" \
  --tz "UTC" \
  --session isolated \
  --message "Run: cd /path/to/skill && python polymarket-simmer-fastloop.py --live --quiet. Show output summary." \
  --announce
```

**Linux crontab设置：**
```
*/5 * * * * cd /path/to/skill && python polymarket-simmer-fastloop.py --live --quiet
```

## 全部配置参数

| 参数 | 默认值 | 说明 |
|---------|---------|-------------|
| `entry_threshold` | 0.05 | 价格偏离50c的最小幅度 |
| `min_momentum_pct` | 1.0 | 触发交易的最低资产价格变动百分比 |
| `max_position` | 5.0 | 每笔交易的最大金额 |
| `signal_source` | binance | 数据来源（Binance或coingecko） |
| `lookback_minutes` | 5 | 蜡烛图回顾窗口时间（分钟） |
| `min_time_remaining` | 60 | 如果剩余时间少于N秒，则跳过交易 |
| `target_time_min` | 90 | 优先选择剩余时间大于或等于N秒的市场 |
| `target_time_max` | 210 | 优先选择剩余时间小于或等于N秒的市场 |
| `asset` | BTC | 交易资产（BTC、ETH或SOL） |
| `window` | 5m | 交易周期（5分钟或15分钟） |
| `volume_confidence` | true | 忽略交易量较低的交易信号 |
| `require_orderbook` | false | 是否需要订单簿确认 |
| `time_filter` | true | 跳过02:00–06:00 UTC的交易时段 |
| `vol_sizing` | true | 根据波动性调整头寸规模 |
| `fee_buffer` | 0.05 | 交易费用超出平衡点时的额外缓冲金额 |
| `daily_budget` | 10.0 | 每天的最大交易金额 |
| `starting_balance` | 1000.0 | 模拟交易账户的初始余额 |

## 故障排除

- **“动量低于阈值”**：资产价格变动幅度太小。如有需要，可以降低`min_momentum_pct`的值。
- **“订单簿不平衡：中性”**：市场处于平衡状态，当`require_orderbook`设置为`true`时，该信号将被忽略。
- **“时间过滤：低流动性时段”**：当前时间为02:00–06:00 UTC。可以通过设置`time_filter=false`来忽略该时段的交易。