---
name: polymarket-fast-loop
description: 通过 Simmer API，利用 CEX（中心化交易所）的价格动量信号，在 Polymarket 上进行 5 分钟和 15 分钟周期的快速交易。默认使用的信号数据来自 Binance 的 BTC/USDT 价格历史数据（klines）。该功能适用于用户希望进行快速交易、自动化短期加密货币交易，或以 CEX 的价格动量作为 Polymarket 交易决策依据的场景。
metadata:
  author: Simmer (@simmer_markets)
  version: "1.3.3"
  displayName: Polymarket FastLoop Trader
  difficulty: advanced
---# Polymarket FastLoop Trader

使用实时价格信号，在Polymarket的5分钟快速交易市场中进行交易。默认使用来自Binance的BTC价格波动信号；同样适用于ETH和SOL。

> **仅适用于Polymarket。** 所有交易都在Polymarket上使用真实的USDC进行。使用`--live`选项可进行实时交易，否则为模拟交易。

> **这是一个模板。** 默认的Binance价格波动信号可帮助您开始使用该技能——您可以根据自己的信号、数据源或策略进行修改。该技能负责处理所有市场发现、数据导入和交易执行等繁琐工作，您只需提供交易策略即可。

> ⚠️ 快速交易市场需支付Polymarket的10%费用（`is_paid: true`），请在交易策略中考虑这一因素。

## 如何查找市场

- 直接通过Polymarket的Gamma API查询实时快速交易市场——不依赖于Simmer的市场列表
- 每个周期都会自动发现新的交易市场
- 支持BTC、ETH或SOL——只需更改`--set asset=ETH`参数，或指定您想要交易的市场
- 每5分钟运行一次，以捕捉每个交易窗口的机会（或每1分钟运行一次，以抓住窗口内的交易机会）

**您无需等待Simmer显示市场信息**。FastLoop会实时在Polymarket上查找市场，然后通过Simmer进行交易。

## 何时使用此技能

当用户希望：
- 在任何支持的资产上进行5分钟或15分钟的快速交易
- 自动化短期加密货币预测交易
- 使用CEX的价格波动信号作为Polymarket的交易信号
- 监控快速交易市场中的持仓情况

## 设置流程

当用户请求安装或配置此技能时，请按照以下步骤操作：

1. **获取Simmer API密钥**
   - 从simmer.markets/dashboard的SDK标签页获取
   - 将其存储在环境变量`SIMMER_API_KEY`中

2. **获取钱包私钥**（实时交易必需）
   - 这是用户Polymarket钱包的私钥（用于存储USDC）
   - 将其存储在环境变量`WALLET_PRIVATE_KEY`中
   - SDK会使用此密钥在客户端自动签署交易订单，无需手动签名

3. **确认设置**（或保持默认值）
   - 资产：BTC、ETH或SOL（默认为BTC）
   - 进场阈值：触发交易的最低价格波动幅度（默认为5美分）
   - 最大持仓量：每次交易的金额（默认为5.00美元）
   - 交易窗口：5分钟或15分钟（默认为5分钟）

4. **设置定时任务或循环执行**（用户负责安排执行时间——详见“如何循环执行”）

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

## 如何循环执行

脚本会**执行一个周期**，之后由用户自行设置定时任务或循环执行：

**Linux crontab**（本地或VPS环境）：
```
# Every 5 minutes (one per fast market window)
*/5 * * * * cd /path/to/skill && python fastloop_trader.py --live --quiet

# Every 1 minute (more aggressive, catches mid-window opportunities)
* * * * * cd /path/to/skill && python fastloop_trader.py --live --quiet
```

**OpenClaw原生cron**（容器化或OpenClaw管理的环境）：
```bash
openclaw cron add \
  --name "Fast Loop Trader" \
  --cron "*/5 * * * *" \
  --tz "UTC" \
  --session isolated \
  --message "Run fast loop trader: cd /path/to/skill && python fastloop_trader.py --live --quiet. Show the output summary." \
  --announce
```

**通过OpenClaw的心跳机制执行**：将相关配置添加到您的HEARTBEAT.md文件中：
```
Run: cd /path/to/fast market && python fastloop_trader.py --live --quiet
```

## 配置

可以通过`config.json`文件、环境变量或`--set`参数进行配置：

```bash
# Change entry threshold
python fastloop_trader.py --set entry_threshold=0.08

# Trade ETH instead of BTC
python fastloop_trader.py --set asset=ETH

# Multiple settings
python fastloop_trader.py --set min_momentum_pct=0.3 --set max_position=10
```

### 设置参数

| 参数 | 默认值 | 环境变量 | 说明 |
|---------|---------|---------|-------------|
| `entry_threshold` | 0.05 | `SIMMER_SPRINT_ENTRY` | 触发交易的最低价格波动幅度（50美分） |
| `min_momentum_pct` | 0.5 | `SIMMER_SPRINT_MOMENTUM` | 触发交易的最低BTC价格波动百分比 |
| `max_position` | 5.0 | `SIMMER_SPRINT_MAX_POSITION` | 每次交易的最大金额 |
| `signal_source` | binance | `SIMMER_SPRINT SIGNAL` | 价格数据源（Binance或coingecko） |
| `lookback_minutes` | 5 | `SIMMER_SPRINT_lookBACK` | 价格历史数据的时间长度（分钟） |
| `min_time_remaining` | 60 | `SIMMER_SPRINT_MIN_TIME` | 跳过剩余时间不足60秒的快速交易市场 |
| `asset` | BTC | `SIMMER_SPRINT_ASSET` | 交易资产（BTC、ETH、SOL） |
| `window` | 5m | `SIMMER_SPRINT_WINDOW` | 交易窗口时长（5分钟或15分钟） |
| `volume_confidence` | true | `SIMMER_SPRINT_VOL_CONF` | 根据Binance的交易量加权信号 |

### 示例config.json配置

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

**默认信号（Binance价格波动信号）：**

1. 从Binance获取过去5分钟的每分钟价格数据（`BTCUSDT`）
2. 计算价格波动幅度：`(current_price - price_5min_ago) / price_5min_ago`
3. 比较价格波动方向与当前Polymarket的市场行情
4. 在满足以下条件时执行交易：
   - 价格波动幅度 ≥ `min_momentum_pct`（默认为0.5%）
   - 价格波动幅度 ≥ `entry_threshold`（默认为5美分）
   - 交易量超过平均交易量的50%（排除价格波动较小的情况）

**示例：** 如果过去5分钟内BTC价格上涨了0.8%，但快速交易市场中的价格仅为0.52美元，且实际价格与预期价格（约0.55美元）相差3美分，则执行买入操作。

### 自定义信号

**此技能是一个模板**。默认的Binance价格波动信号只是一个起点。该技能负责处理所有繁琐的工作（市场发现、数据导入和订单执行），您只需提供自己的交易策略即可。

**自定义信号的示例：**
- **多交易所价格对比**：比较Binance、Kraken、Bitfinex等交易所的价格波动，以预测价格走势
- **市场情绪**：结合Twitter或社交媒体的实时信息——某些热门推文可能影响快速交易市场
- **技术指标**：使用RSI、VWAP等技术指标进行分析
- **新闻事件**：利用您的分析能力解读新闻标题对市场的影响
- **链上数据**：关注鲸鱼交易者的行为、资金流动情况、清算率等

要自定义信号，可以修改`fastloop_trader.py`文件中的`get_momentum()`函数或添加自己的信号处理逻辑。其余部分（市场发现、数据导入、交易量判断等）保持不变。

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
- 其他技能不会影响您的快速交易市场持仓
- 您可以单独跟踪快速交易市场的盈亏情况

## 故障排除

**“未找到活跃的快速交易市场”**
- 可能是因为快速交易市场处于非交易时间或周末
- 请直接在Polymarket上查看是否有活跃的BTC快速交易市场

**“剩余时间少于60秒时未找到快速交易市场”**
- 当前交易窗口即将结束，下一个交易窗口尚未开启
- 如果希望更接近交易结束时间进行交易，可以减小`min_time_remaining`的值

**“数据导入失败：超出请求限制”**
- 免费账户每天最多可导入10次数据；专业账户每天最多可导入50次
- 快速交易市场需要专业账户才能更频繁地进行交易

**“无法获取价格数据”**
- 可能是因为Binance的API暂时不可用或请求次数达到限制
- 可以尝试使用`--set signal_source=coingecko`作为备用数据源

**“交易失败：市场流动性不足”**
- 快速交易市场中的交易量较小，可以尝试减小交易金额

**“外部钱包需要预先签署的订单”**
- 确保环境变量`WALLET_PRIVATE_KEY`已设置
- SDK会在该变量存在的情况下自动签署订单，无需手动操作
- 解决方法：`export WALLET_PRIVATE_KEY=0x<your-polymarket-wallet-private-key>`
- 请勿尝试手动签署订单或修改技能代码，SDK会自动处理

**“账户余额显示为0美元，但实际上我有USDC”**
- Polymarket使用的是**USDC.e**（桥接后的USDC，合约地址为`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`），而非原生USDC
- 如果您最近将USDC桥接到了Polygon网络，可能需要将USDC.e兑换为原生USDC后再尝试交易
- 将原生USDC兑换为USDC.e后重新尝试交易