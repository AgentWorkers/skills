---
name: polymarket-fast-loop
displayName: Polymarket FastLoop Trader
description: 使用 Simmer API，根据 CEX（中心化交易所）的价格动量信号，在 Polymarket 上进行 5 分钟和 15 分钟周期的快速交易。默认使用的信号数据来自 Binance 的 BTC/USDT 交易记录（klines）。该功能适用于用户希望进行快速交易、自动化短期加密货币交易，或利用 CEX 的价格动量作为 Polymarket 的交易决策依据的情况。
metadata: {"clawdbot":{"emoji":"⚡","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false,"automaton":{"managed":true,"entrypoint":"fastloop_trader.py"},"tunables":[{"env":"SIMMER_FASTLOOP_ENTRY_THRESHOLD","type":"number","default":0.05,"range":[0.01,0.30],"step":0.01,"label":"Entry edge threshold"},{"env":"SIMMER_FASTLOOP_MOMENTUM_THRESHOLD","type":"number","default":0.03,"range":[0.01,0.20],"step":0.01,"label":"Momentum threshold"},{"env":"SIMMER_FASTLOOP_MAX_POSITION_USD","type":"number","default":50,"range":[1,200],"step":5,"label":"Max position size"},{"env":"SIMMER_FASTLOOP_LOOKBACK_MINUTES","type":"number","default":30,"range":[5,120],"step":5,"label":"Lookback window (minutes)"},{"env":"SIMMER_FASTLOOP_MIN_TIME_BETWEEN_TRADES_SEC","type":"number","default":60,"range":[10,600],"step":10,"label":"Min time between trades (seconds)"},{"env":"SIMMER_FASTLOOP_DAILY_BUDGET_USD","type":"number","default":100,"range":[10,500],"step":10,"label":"Daily budget"},{"env":"SIMMER_FASTLOOP_VOL_CONFIDENCE_MIN","type":"number","default":0.5,"range":[0.1,1.0],"step":0.05,"label":"Minimum volatility confidence"}]}}
authors:
  - Simmer (@simmer_markets)
version: "1.1.2"
published: true
---
# Polymarket FastLoop Trader

使用实时价格信号在 Polymarket 上进行 5 分钟周期的加密货币快速交易。默认使用来自 Binance 的 BTC 动量指标；也支持 ETH 和 SOL 资产。

> **仅适用于 Polymarket。** 所有交易都在 Polymarket 上使用真实的 USDC 执行。使用 `--live` 选项可进行实时交易，默认为模拟交易。

> **这是一个模板。** 默认的信号源（Binance 动量指标）可帮助您快速开始使用该技能——您可以根据自己的需求替换为自定义信号源或策略。该技能会处理所有市场发现、数据导入和交易执行等底层逻辑，您只需提供交易策略即可。

> ⚠️ 快速交易需支付 Polymarket 的 10% 手续费（`is_paid: true`），请在交易策略中考虑这一费用。

## 如何查找市场

- 直接通过 Polymarket 的 Gamma API 查询实时快速交易市场（不依赖 Simmer 的市场列表）
- 每个周期自动发现新的交易市场
- 支持 BTC、ETH 和 SOL 资产——只需更改 `--set asset` 参数即可；或者指定想要交易的资产
- 每 5 分钟运行一次，以捕捉每个交易窗口的机会（或每 1 分钟运行一次，以抓住窗口内的交易机会）

**无需等待 Simmer 自动显示市场信息。** FastLoop 会实时在 Polymarket 上查找市场，然后通过 Simmer 进行交易。

## 适用场景

当用户希望：
- 在任何支持的资产上进行 5 分钟或 15 分钟周期的加密货币快速交易
- 自动化进行短期加密货币预测交易
- 使用 CEX 的价格波动作为 Polymarket 的交易信号
- 监控快速交易中的持仓情况时，可以使用此技能。

## 设置流程

当用户请求安装或配置此技能时，请按照以下步骤操作：

1. **获取 Simmer API 密钥**
   - 从 simmer.markets/dashboard 的 SDK 标签页获取密钥
   - 将密钥存储在环境变量 `SIMMER_API_KEY` 中

2. **提供钱包私钥**（用于实时交易）
   - 这是用户用于 Polymarket 交易的钱包私钥（该钱包中存放 USDC）
   - 将私钥存储在环境变量 `WALLET_PRIVATE_KEY` 中
   - SDK 会使用此密钥在客户端自动签名交易订单，无需手动签名

3. **确认设置**（或使用默认值）
   - 资产：BTC、ETH 或 SOL（默认为 BTC）
   - 进场阈值：触发交易的最低价格波动幅度（默认为 5 分）
   - 每笔交易的最大持仓金额（默认为 5.00 美元）
   - 交易窗口周期：5 分钟或 15 分钟（默认为 5 分钟）

4. **设置定时任务或循环执行**（用户负责安排任务执行时间——详见“如何设置循环执行”）

## 快速入门

```bash
# Set your API key
export SIMMER_API_KEY="your-key-here"

# Dry run — see what would happen
python fastloop_trader.py

# Go live
python fastloop_trader.py --live

# Live + quiet (for cron/heartbeat loops)
python fastloop_trader.py --live --quiet

# Live + smart sizing (5% of balance per trade)
python fastloop_trader.py --live --smart-sizing --quiet
```

## 如何设置循环执行

脚本会执行一个完整的交易周期——用户需要设置定时任务或循环执行机制：

**Linux crontab**（本地或 VPS 环境）：
```
# Every 5 minutes (one per fast market window)
*/5 * * * * cd /path/to/skill && python fastloop_trader.py --live --quiet

# Every 1 minute (more aggressive, catches mid-window opportunities)
* * * * * cd /path/to/skill && python fastloop_trader.py --live --quiet
```

**OpenClaw 原生 cron 任务**（容器化或 OpenClaw 管理的环境）：
```bash
openclaw cron add \
  --name "Fast Loop Trader" \
  --cron "*/5 * * * *" \
  --tz "UTC" \
  --session isolated \
  --message "Run fast loop trader: cd /path/to/skill && python fastloop_trader.py --live --quiet. Show the output summary." \
  --announce
```

**通过 OpenClaw 的心跳机制执行**：请在 `HEARTBEAT.md` 文件中添加相应的配置：
```
Run: cd /path/to/fast market && python fastloop_trader.py --live --quiet
```

## 配置

可以通过 `config.json` 文件、环境变量或 `--set` 参数进行配置：

```bash
# Change entry threshold
python fastloop_trader.py --set entry_threshold=0.08

# Trade ETH instead of BTC
python fastloop_trader.py --set asset=ETH

# Multiple settings
python fastloop_trader.py --set min_momentum_pct=0.3 --set max_position=10
```

### 配置参数

| 参数 | 默认值 | 环境变量 | 说明 |
|---------|---------|---------|-------------|
| `entry_threshold` | 0.05 | `SIMMER_SPRINT_ENTRY` | 触发交易的最低价格波动幅度 |
| `min_momentum_pct` | 0.5 | `SIMMER_SPRINT_MOMENTUM` | 触发交易的 BTC 价格最低涨幅百分比 |
| `max_position` | 5.0 | `SIMMER_SPRINT_MAX_POSITION` | 每笔交易的最大持仓金额 |
| `signal_source` | binance | `SIMMER_SPRINT_SIGNAL` | 价格数据源（Binance 或 Coingecko） |
| `lookback_minutes` | 5 | `SIMMER_SPRINT_lookBACK` | 价格历史数据保留时间（分钟） |
| `min_time_remaining` | 60 | `SIMMER_SPRINT_MIN_TIME` | 跳过剩余时间不足 60 秒的快速交易市场 |
| `asset` | BTC | `SIMMER_SPRINT_ASSET` | 交易资产（BTC、ETH 或 SOL） |
| `window` | 5m | `SIMMER_SPRINT_WINDOW` | 交易窗口周期（5 分钟或 15 分钟） |
| `volume_confidence` | true | `SIMMER_SPRINT_VOL_CONF` | 根据 Binance 的交易量加权信号 |

### 示例 `config.json` 配置

```json
{
  "entry_threshold": 0.08,
  "min_momentum_pct": 0.3,
  "max_position": 10.0,
  "asset": "BTC",
  "window": "5m",
  "signal_source": "binance"
}
```

## 命令行选项

```bash
python fastloop_trader.py                    # Dry run
python fastloop_trader.py --live             # Real trades
python fastloop_trader.py --live --quiet     # Silent except trades/errors
python fastloop_trader.py --smart-sizing     # Portfolio-based sizing
python fastloop_trader.py --positions        # Show open fast market positions
python fastloop_trader.py --config           # Show current config
python fastloop_trader.py --set KEY=VALUE    # Update config
```

## 信号逻辑

**默认信号（Binance 动量指标）：**

1. 从 Binance 获取过去 5 分钟内的每分钟价格数据（以 BTCUSDT 为单位）
2. 计算价格涨幅：`(current_price - price_5min_ago) / price_5min_ago`
3. 比较价格涨幅与当前 Polymarket 的价格走势
4. 在满足以下条件时执行交易：
   - 价格涨幅 ≥ `min_momentum_pct`（默认为 0.5%）
   - 价格波动幅度 ≥ `entry_threshold`（默认为 5 分）
   - 交易量大于平均交易量的 1.5 倍（排除价格波动较小的情况）

**示例：** 如果过去 5 分钟内 BTC 价格上涨了 0.8%，但快速交易市场中的价格仅为 0.52 美元，且实际价格与预期价格（约 0.55 美元）相差 3 分，则执行买入操作。

### 自定义信号源：

**此技能只是一个模板。** 默认的 Binance 动量指标只是一个起点。您可以根据自己的需求替换为自定义信号源。技能会处理所有底层逻辑（市场发现、数据导入和订单执行）。自定义信号源的示例包括：
- **多交易所价格对比**：比较 Binance、Kraken、Bitfinex 等交易所的价格差异，以预测价格走势
- **市场情绪**：结合 Twitter 或社交媒体的信息，因为某些突发新闻可能会影响快速交易市场
- **技术指标**：使用 RSI、VWAP 或您喜欢的数据源提供的订单流分析结果
- **新闻事件**：利用您的智能代理解析新闻标题对价格的影响
- **链上数据**：分析鲸鱼交易者的行为、资金流动情况或清算比率

要自定义信号源，请修改 `fastloop_trader.py` 文件中的 `get_momentum()` 函数或添加自己的信号处理逻辑。其余部分（市场发现、数据导入、交易量评估等）保持不变。

## 示例交易结果

```
⚡ Simmer FastLoop Trading Skill
==================================================

  [DRY RUN] No trades will be executed. Use --live to enable trading.

⚙️  Configuration:
  Asset:            BTC
  Entry threshold:  0.05 (min divergence from 50¢)
  Min momentum:     0.5% (min price move)
  Max position:     $5.00
  Signal source:    binance
  Lookback:         5 minutes
  Min time left:    60s
  Volume weighting: ✓

🔍 Discovering BTC fast markets...
  Found 3 active fast markets

🎯 Selected: Bitcoin Up or Down - February 15, 5:30AM-5:35AM ET
  Expires in: 185s
  Current YES price: $0.480

📈 Fetching BTC price signal (binance)...
  Price: $97,234.50 (was $96,812.30)
  Momentum: +0.436%
  Direction: up
  Volume ratio: 1.45x avg

🧠 Analyzing...
  ⏸️  Momentum 0.436% < minimum 0.500% — skip

📊 Summary: No trade (momentum too weak: 0.436%)
```

## 数据标记

所有交易都会被标记为 `source: "sdk:fastloop"`。这意味着：
- 投资组合会按策略进行分类显示
- 其他技能不会影响快速交易的持仓情况
- 您可以单独跟踪快速交易的盈亏情况

## 常见问题及解决方法

- **“未找到活跃的快速交易市场”**：可能是因为当前时间不在交易时段或周末，建议直接在 Polymarket 上查看活跃的市场信息。
- **“剩余时间少于 60 秒时未找到快速交易市场”**：当前交易窗口即将结束，下一个交易窗口尚未开始。可以调整 `min_time_remaining` 参数以缩短等待时间。
- **“数据导入失败：超出请求限制”**：免费账户每天允许 10 次数据导入，专业账户每天允许 50 次。快速交易需要专业账户才能频繁使用此功能。
- **“无法获取价格数据”**：可能是 Binance API 出现故障或请求次数达到限制。可以尝试使用 `--set signal_source=coingecko` 作为备用数据源。
- **“交易失败：市场流动性不足”**：快速交易市场中的交易量较小，可以尝试减小交易金额。
- **“外部钱包需要预先签名订单”**：确保环境变量 `WALLET_PRIVATE_KEY` 已设置。SDK 会自动使用该密钥进行订单签名，无需手动操作。
- **“账户余额显示为 0 美元，但实际上我有 USDC”**：Polymarket 使用的是桥接后的 USDC（合约地址 `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`），而非原生 USDC。如果最近将 USDC 桥接到了 Polygon 平台，请先转换回原生 USDC，然后再尝试交易。