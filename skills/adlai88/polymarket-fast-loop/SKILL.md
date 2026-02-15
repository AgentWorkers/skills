---
name: polymarket-fast-loop
displayName: Polymarket FastLoop Trader
description: 使用 Simmer API，根据 CEX（中心化交易所）的价格动量信号，在 Polymarket 上进行 5 分钟和 15 分钟周期的快速交易（即“sprint”交易）。默认使用的信号数据来自 Binance 的 BTC/USDT 交易记录（klines）。该功能适用于用户希望进行快速交易、自动化短期加密货币交易，或利用 CEX 的价格动量作为 Polymarket 的交易依据的情况。
metadata: {"clawdbot":{"emoji":"⚡","requires":{"env":["SIMMER_API_KEY"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
version: "1.0.5"
published: true
---

# Polymarket FastLoop Trader

使用来自Binance的实时价格动量，在Polymarket的5分钟BTC快速市场中进行交易。

> **仅适用于Polymarket。** 所有交易都在Polymarket上使用真实的USDC执行。使用`--live`选项进行实时交易，默认为模拟交易（dry-run）。

**工作原理：** 脚本会定期查找当前的BTC快速市场，检查Binance上的BTC价格动量，并在动量与市场预期出现偏差时执行交易。

**这是一个模板。** 默认的信号（Binance动量）可以让你开始使用该脚本。你可以通过添加情绪分析、多交易所价格差异、新闻源或自定义信号来提升交易策略的准确性。

> ⚠️ 快速市场需要支付Polymarket的10%费用（`is_paid: true`）。请在交易策略中考虑这一费用。

## 适用场景

当用户希望执行以下操作时，可以使用此脚本：
- 交易BTC快速市场（5分钟或15分钟周期）
- 自动化短期加密货币预测交易
- 使用CEX的价格动量作为Polymarket的交易信号
- 监控快速市场中的持仓情况

## 设置流程

当用户请求安装或配置此脚本时，请按照以下步骤操作：
1. **获取Simmer API密钥**
   - 从simmer.markets/dashboard的SDK标签页获取API密钥
   - 将密钥存储在环境变量`SIMMER_API_KEY`中
2. **确认设置**（或保持默认值）
   - 资产：BTC、ETH或SOL（默认为BTC）
   - 入场阈值：触发交易的最低价格偏差（默认为5美分）
   - 最大持仓量：单次交易的最大金额（默认为5.00美元）
   - 时间窗口：5分钟或15分钟（默认为5分钟）
3. **设置定时任务或循环执行**（用户负责安排执行频率——详见“如何设置循环执行”）

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

脚本会**循环运行**一次。你可以设置定时任务或心跳机制来自动执行脚本：
- **每5分钟执行一次（适用于5分钟周期的快速市场）：**
```
*/5 * * * * cd /path/to/skill && python fastloop_trader.py --live --quiet
```

- **每1分钟执行一次（更频繁的执行方式，适用于捕捉市场中的即时机会）：**
```
* * * * * cd /path/to/skill && python fastloop_trader.py --live --quiet
```

- **通过OpenClaw心跳机制执行：** 将相关配置添加到`HEARTBEAT.md`文件中：
```
Run: cd /path/to/fast market && python fastloop_trader.py --live --quiet
```

## 配置

可以通过`config.json`文件、环境变量或`--set`命令来配置脚本参数：

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
| `entry_threshold` | 0.05 | `SIMMER_SPRINT_ENTRY` | 触发交易的最低价格偏差（单位：美分） |
| `min_momentum_pct` | 0.5 | `SIMMER_SPRINT_MOMENTUM` | 触发交易的最低价格变动百分比（单位：%） |
| `max_position` | 5.0 | `SIMMER_SPRINT_MAX_POSITION` | 单次交易的最大金额（单位：美元） |
| `signal_source` | binance | `SIMMER_SPRINT SIGNAL` | 价格数据来源（Binance或coingecko） |
| `lookback_minutes` | 5 | `SIMMER_SPRINT_lookBACK` | 价格历史数据的查看时长（单位：分钟） |
| `min_time_remaining` | 60 | `SIMMER_SPRINT_MIN_TIME` | 跳过剩余时间不足60秒的快速市场 |
| `asset` | BTC | `SIMMER_SPRINT_ASSET` | 交易资产（BTC、ETH、SOL） |
| `window` | 5m | `SIMMER_SPRINT_WINDOW` | 市场周期时长（5分钟或15分钟） |
| `volume_confidence` | true | `SIMMER_SPRINT_VOL_CONF` | 是否根据Binance的交易量来加权信号 |

### 示例`config.json`配置

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

**默认信号（Binance动量）：**
1. 从Binance获取过去5分钟的1分钟价格数据（`BTCUSDT`）
2. 计算价格动量：`(current_price - price_5min_ago) / price_5min_ago`
3. 比较动量方向与当前Polymarket的市场预期：
4. 在满足以下条件时执行交易：
   - 动量 ≥ `min_momentum_pct`（默认为0.5%）
   - 价格与预期价格（50美分）的偏差 ≥ `entry_threshold`（默认为5美分）
   - 交易量超过平均交易量的50%（`volume_ratio` > 0.5）（排除价格波动较小的情况）

**示例：** 如果过去5分钟内BTC价格上涨了0.8%，但快速市场的实际价格仅为0.52美元，且实际价格与预期价格（约0.55美元）的偏差为3美分，则执行买入操作。

### 自定义信号

默认的动量信号只是一个起点。你可以通过以下方式进一步优化交易策略：
- **多交易所比较：** 对比Binance、Kraken、Bitfinex等交易所的价格数据，交易所间的价格差异有助于预测市场走势
- **情绪分析：** 结合Twitter或社交媒体上的实时信息，因为热门话题可能影响快速市场
- **技术指标：** 使用RSI、VWAP等技术指标进行分析
- **新闻因素：** 考虑新闻事件对价格的影响，并根据你的判断来调整交易策略

脚本负责处理所有的数据获取和交易执行工作，而你负责提供具体的交易策略和逻辑。

## 示例输出

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

## 来源标记

所有交易都会被标记为`source: "sdk:fastloop"`。这意味着：
- 投资组合会按策略进行分类显示
- 其他脚本不会影响你的快速市场交易结果
- 你可以单独查看快速市场的盈亏情况

## 常见问题及解决方法

- **“未找到活跃的快速市场”**：可能是因为当前市场处于非交易时间或周末，建议直接在Polymarket上查看活跃的BTC快速市场。
- **“剩余时间不足60秒时未找到快速市场”**：当前市场周期即将结束，下一个市场尚未开始交易。可以调整`min_time_remaining`参数以允许在更接近市场结束的时间进行交易。
- **“导入数据失败：超出请求限制”**：免费账户每天只能导入10次数据，专业账户每天可导入50次。快速市场交易通常需要更高的请求频率，因此建议使用专业账户。
- **“无法获取价格数据”**：可能是Binance的API暂时不可用或请求次数达到上限。可以尝试使用`--set signal_source=coingecko`作为备用数据源。
- **“交易失败：市场流动性不足”**：快速市场的交易量较小，可以尝试减小单次交易的金额。