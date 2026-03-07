---
name: polymarket-simmer-fastloop
displayName: Polymarket Simmer FastLoop Trader
description: 在 Polymarket 平台上，您可以进行 BTC/ETH/SOL 货币对的交易，使用 5/15 分钟的快速交易模式，并具备动量分析功能以及订单簿筛选功能。
version: "1.1.0"
author: "Xuano47"
tags: ["polymarket", "trading", "btc", "eth", "sol"]
env:
  - SIMMER_API_KEY
  - TRADING_VENUE
  - SIMMER_USER_ID
---
# Polymarket Simmer FastLoop Trader

这是一个用于 Polymarket 的自动化交易技能，适用于 BTC/ETH/SOL 股票的 5 分钟和 15 分钟快速交易市场。该策略采用均值回归方法，并结合动量衰竭检测、订单簿不平衡确认以及基于波动率的头寸调整机制。

> **默认模式为模拟交易（Paper mode）**。如需进行真实交易，请使用 `--live` 参数。

## 策略原理

当最新的 5 分钟蜡烛图显示价格快速上涨（动量超过阈值）时，脚本会买入反向头寸，以捕捉价格回调。信号筛选条件包括：

- **动量（Momentum）**：使用 Binance 的 1 分钟蜡烛图数据，可配置阈值（默认为 1.0%）。
- **订单簿不平衡（Order Book Imbalance）**（可选）：通过分析 Binance L2 订单簿的前 20 个层次来确定市场趋势。
- **NOFX 机构净流量（NOFX Institutional Netflow）**：根据机构投资者的交易数据来筛选交易。
- **时间过滤（Time-of-Day Filter）**：默认情况下会跳过流动性较低的时间段（02:00–06:00 UTC）。
- **费用平衡条件（Fee-Accurate EV）**：仅在执行价格与费用平衡点之间的交易时才进行交易。
- **基于波动率的头寸调整（Volatility-Adjusted Sizing）**：在高波动率情况下自动减少头寸大小。

## 设置步骤

### 1. 获取 Simmer API 密钥
- 在 [simmer.markets](https://simmer.markets) 注册账号。
- 进入 **控制面板（Dashboard）** -> **SDK** 标签页。
- 复制您的 API 密钥：`export SIMMER_API_KEY="your-key-here"`。

### 必需的环境变量

| 变量 | 是否必需 | 说明 | 值 |
|----------|----------|-------------|--------|
| `SIMMER_API_KEY` | 是 | 您的 Simmer SDK 密钥 | 从 [simmer.markets](https://simmer.markets) 获取 |
| `TRADING_VENUE` | 是 | 执行环境 | `simmer`（模拟交易）或 `polymarket`（真实交易） |
| `WALLET_PRIVATE_KEY` | 可选 | 您的 Polymarket 钱包私钥 | 仅当 `TRADING_VENUE="polymarket"` 时需要 |
| `SIMMER_USER_ID` | 是 | 您的 SkillPay 用户 ID（用于计费） | 通过 SkillPay 进行每次交易计费时需要 |

- **`simmer`**（默认）：模拟交易模式，使用虚拟资金进行交易，无需实际使用 USDC。
- **`polymarket`**：真实交易模式，需要连接到 Polymarket 并确保钱包中持有 USDC。

> [警告！]
> 请勿泄露您的 `WALLET_PRIVATE_KEY` 或 `SIMMER_API_KEY`。SDK 会在本地执行交易，您的私钥不会被传输。

### 3. 计费方式

每次交易通过 SkillPay 收费 0.001 USDT。如果您的账户余额不足，系统会在日志中提供支付链接。

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

**使用 OpenClaw：**
```bash
openclaw cron add \
  --name "Simmer FastLoop" \
  --cron "*/5 * * * *" \
  --tz "UTC" \
  --session isolated \
  --message "Run: cd /path/to/skill && python polymarket-simmer-fastloop.py --live --quiet. Show output summary." \
  --announce
```

**Linux crontab 设置：**
```
*/5 * * * * cd /path/to/skill && python polymarket-simmer-fastloop.py --live --quiet
```

## 全部配置参数

| 参数 | 默认值 | 说明 |
|---------|---------|-------------|
| `entry_threshold` | 0.05 | 价格偏离 50c 的最小幅度 |
| `min_momentum_pct` | 1.0 | 触发交易的最低资产价格变动百分比 |
| `max_position` | 5.0 | 每笔交易的最大金额 |
| `signal_source` | binance | 使用 Binance 或 Coingecko 数据源 |
| `lookback_minutes` | 5 | 蜡烛图回顾时间窗口（5 分钟） |
| `min_time_remaining` | 60 | 如果剩余时间少于 N 秒，则跳过当前交易 |
| `target_time_min` | 90 | 优先选择剩余时间大于或等于 N 秒的市场 |
| `target_time_max` | 210 | 优先选择剩余时间小于或等于 N 秒的市场 |
| `asset` | BTC | 可交易的资产（BTC、ETH 或 SOL） |
| `window` | 5m | 交易周期（5 分钟或 15 分钟） |
| `volume_confidence` | true | 如果成交量过低，则忽略交易信号 |
| `require_orderbook` | false | 是否需要订单簿确认 |
| `time_filter` | true | 跳过 02:00–06:00 UTC 的时间段 |
| `vol_sizing` | true | 根据波动率调整头寸大小 |
| `fee_buffer` | 0.05 | 在费用平衡点基础上增加额外的安全缓冲 |
| `daily_budget` | 10.0 | 每天的最大支出限额 |
| `starting_balance` | 1000.0 | 模拟交易账户的初始余额 |

## 常见问题解决方法

- **“动量低于阈值”**：表示资产价格变动幅度太小。如有需要，可以降低 `min_momentum_pct` 的值。
- **“订单簿不平衡：中性”**：表示市场处于平衡状态，当 `require_orderbook` 为 true 时，该信号会被忽略。
- **“时间过滤：流动性低”**：当前时间为 02:00–06:00 UTC。可以通过设置 `time_filter=false` 来忽略此限制。