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

这是一个用于Polymarket平台的自动化交易策略，专门针对BTC/ETH/SOL货币的5分钟和15分钟快速交易市场。该策略采用均值回归策略，并结合动量耗尽检测、订单簿不平衡确认以及基于波动率的头寸调整机制。

> **默认模式为模拟交易（Paper mode）**。如需进行真实交易，请使用`--live`参数。

## 策略原理

当最新的5分钟蜡烛图显示价格快速上涨（动量超过预设阈值）时，该脚本会买入反向头寸，以捕捉价格回调的机会。信号筛选条件包括：

- **动量（Momentum）**：使用Binance的1分钟蜡烛图数据，阈值可配置（默认为1.0%）。
- **订单簿不平衡（Order Book Imbalance）**（可选）：通过分析Binance L2订单簿的前20个层次来判断市场趋势。
- **NOFX机构净流量（NOFX Institutional Netflow）**：根据机构投资者的交易数据来筛选交易。
- **时间过滤（Time-of-Day Filter）**：默认会跳过流动性较低的时间段（02:00–06:00 UTC）。
- **费用平衡条件（Fee-Accurate EV）**：仅在执行交易时确保费用收益超过成本。
- **基于波动率的头寸调整（Volatility-Adjusted Sizing）**：在高波动率情况下自动减少头寸规模。
- **预缓存机制（Pre-Caching）**：每次运行时，该策略会扫描并缓存即将开放的市场信息（存储在`fast_markets_cache.json`文件中）。市场开盘后，系统会暂时使用缓存数据执行交易，以避免错过任何交易机会。

## 设置步骤

### 1. 获取Simmer API密钥
- 在[simmer.markets](https://simmer.markets)注册账户。
- 进入**控制面板（Dashboard）** -> **SDK**选项卡。
- 复制您的API密钥：`export SIMMER_API_KEY="your-key-here"`。

### 必需的环境变量

| 变量          | 是否必需 | 描述                                      | 默认值                                      |
|---------------|---------|-----------------------------------------|---------------------------------------|
| `SIMMER_API_KEY`    | 是       | 您的Simmer SDK密钥                             | 从[simmer.markets](https://simmer.markets)获取                |
| `TRADING_VENUE`    | 是       | 执行环境（Paper或polymarket）                          | `simmer`（模拟交易）或`polymarket`（真实交易）                 |
| `WALLET_PRIVATE_KEY` | 可选     | 您的Polymarket钱包私钥                             | 仅当`TRADING_VENUE="polymarket"`时需要                 |

- **`simmer`（默认）**：模拟交易模式，使用虚拟资金进行交易，无需实际使用USDC。
- **`polymarket`**：真实交易模式，需要连接到Polymarket平台，并确保钱包中持有USDC。

> [警告！]
> 请勿泄露您的`WALLET_PRIVATE_KEY`或`SIMMER_API_KEY`。SDK会在本地签署交易，您的私钥不会被传输。

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

**使用OpenClaw进行定时任务配置：**
```bash
openclaw cron add \
  --name "Simmer FastLoop" \
  --cron "*/5 * * * *" \
  --tz "UTC" \
  --session isolated \
  --message "Run: cd /path/to/skill && python polymarket-simmer-fastloop.py --live --quiet. Show output summary." \
  --announce
```

**在Linux系统中使用crontab进行定时任务配置：**
```
*/5 * * * * cd /path/to/skill && python polymarket-simmer-fastloop.py --live --quiet
```

## 全部配置参数

| 参数          | 默认值       | 描述                                      | 可调整范围                                      |
|---------------|-----------|-----------------------------------------|---------------------------------------|
| `entry_threshold` | 0.05       | 与50分钟周期内价格最小波动的差异阈值                | 可调整范围：0.01–0.1                          |
| `min_momentum_pct` | 1.0        | 触发交易的最低动量百分比                         | 可调整范围：0.5–2.0                          |
| `max_position` | 5.0        | 单次交易的最大金额（单位：美元）                         | 可调整范围：1–10                          |
| `signal_source` | binance     | 数据来源（Binance或coingecko）                     | 可选择                              |
| `lookback_minutes` | 5          | 蜡烛图回顾时间窗口（分钟）                         | 可调整范围：3–15                          |
| `min_time_remaining` | 60         | 如果剩余时间少于N秒，则跳过交易                         | 可调整范围：30–180                         |
| `target_time_min` | 90         | 优先选择剩余时间大于或等于N秒的市场                   | 可调整范围：60–180                         |
| `target_time_max` | 210        | 优先选择剩余时间小于或等于N秒的市场                   | 可调整范围：90–360                         |
| `asset`       | BTC         | 可交易的资产（BTC、ETH或SOL）                         | 可选择                              |
| `window`       | 5m         | 交易周期（5分钟或15分钟）                         | 可调整范围：3–30                         |
| `volume_confidence` | true        | 禁用低成交量信号                             | 可选择                             |
| `require_orderbook` | false       | 是否需要订单簿确认                         | 可选择                             |
| `time_filter`     | true        | 跳过02:00–06:00 UTC的时间段                         | 可选择                             |
| `vol_sizing`     | true        | 根据波动率调整头寸规模                         | 可选择                             |
| `fee_buffer`     | 0.05        | 费用收益的额外缓冲空间                         | 可调整范围：0.01–0.1                          |
| `daily_budget`    | 10.0        | 每天的最大交易预算                             | 可调整范围：5.0–50.0                         |
| `starting_balance` | 1000.0       | 模拟交易账户的初始余额                         | 可调整范围：1000.0–10000.0                         |

## 常见问题解决方法

- **“动量低于阈值”**：表示资产价格变动幅度太小。如有需要，可降低`min_momentum_pct`的值。
- **“订单簿不平衡：中性”**：表示市场处于平衡状态，当`require_orderbook`设置为`true`时，该策略会忽略此类信号。
- **“时间过滤：低流动性时段”**：当前时间为02:00–06:00 UTC。可通过设置`time_filter=false`来忽略该时段。