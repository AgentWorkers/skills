---
name: polymarket-fast-loop
displayName: Polymarket FastLoop Trader
description: 通过 Simmer API，利用 CEX（中心化交易所）的价格动量信号，在 Polymarket 上进行 5 分钟和 15 分钟周期的快速交易。默认使用的信号数据来自 Binance 的 BTC/USDT 交易记录（klines）。适用于用户希望进行快速交易、自动化短期加密货币交易，或使用 CEX 的价格动量作为 Polymarket 的交易决策依据的场景。
metadata: {"clawdbot":{"emoji":"⚡","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
version: "1.0.10"
published: true
---
# Polymarket FastLoop Trader

该脚本用于利用实时价格信号在 Polymarket 的 5 分钟快速市场中进行交易。默认使用来自 Binance 的 BTC 动量指标；同样适用于 ETH 和 SOL 资产。

> **仅适用于 Polymarket。** 所有交易均在 Polymarket 上使用真实的 USDC 执行。使用 `--live` 选项可进行实时交易，否则为模拟交易。

> **这是一个模板。** 默认的 Binance 动量指标可作为起点，您可以根据自己的需求替换为其他信号或数据源。该脚本负责市场发现、数据导入和交易执行等所有底层逻辑，您只需提供交易策略即可。

> ⚠️ 快速市场需支付 Polymarket 的 10% 手续费（`is_paid: true`），请在交易策略中考虑这一费用。

## 市场查找方式

- 直接通过 Polymarket 的 Gamma API 查询实时快速市场信息（不依赖于 Simmer 的市场列表）
- 每个周期自动检测新的快速市场
- 支持 BTC、ETH 和 SOL 资产（通过 `--set asset=ETH` 修改资产类型，或指定所需市场）
- 每 5 分钟运行一次，以捕捉每个交易窗口的机会（或每 1 分钟运行一次，以捕捉交易窗口内的机会）

**无需等待 Simmer 中显示市场信息**。FastLoop 会实时在 Polymarket 中查找市场，然后通过 Simmer 进行交易。

## 适用场景

- 当用户希望在任何支持的资产上进行 5 分钟或 15 分钟的快速市场交易时
- 自动化短期加密货币预测交易
- 使用 CEX 的价格走势作为 Polymarket 的交易信号
- 监控快速市场中的持仓情况

## 设置流程

当用户请求安装或配置此脚本时，请按照以下步骤操作：

1. **获取 Simmer API 密钥**
   - 从 simmer.markets/dashboard 的 SDK 标签页获取 API 密钥
   - 将其存储在环境变量 `SIMMER_API_KEY` 中

2. **提供钱包私钥**（实时交易所需）
   - 这是用于 Polymarket 存储 USDC 的钱包私钥
   - 将其存储在环境变量 `WALLET_PRIVATE_KEY` 中
   - SDK 会使用该密钥在客户端自动签署订单，无需手动操作

3. **确认设置**（或保持默认值）
   - 资产：BTC、ETH 或 SOL（默认为 BTC）
   - 进场阈值：触发交易的最低价格波动幅度（默认为 5 分）
   - 每笔交易的最大持仓金额（默认为 5.00 美元）
   - 交易窗口时长：5 分钟或 15 分钟（默认为 5 分钟）

4. **设置定时任务或循环执行**（用户可自行安排执行频率）

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

## 循环执行方式

脚本会**自动运行一个周期**，具体执行频率由用户通过定时任务或循环脚本控制：

- **每 5 分钟运行一次（适用于每个快速市场窗口）：**
```
*/5 * * * * cd /path/to/skill && python fastloop_trader.py --live --quiet
```

- **每 1 分钟运行一次（更频繁，适用于捕捉交易窗口内的机会）：**
```
* * * * * cd /path/to/skill && python fastloop_trader.py --live --quiet
```

- **通过 OpenClaw 心跳机制触发：** 请在 `HEARTBEAT.md` 文件中进行配置：
```
Run: cd /path/to/fast market && python fastloop_trader.py --live --quiet
```

## 配置方式

配置方式包括通过 `config.json`、环境变量或 `--set` 参数进行设置：

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
| `entry_threshold` | 0.05 | `SIMMER_SPRINT_ENTRY` | 触发交易的最低价格波动幅度（单位：分） |
| `min_momentum_pct` | 0.5 | `SIMMER_SPRINT_MOMENTUM` | 触发交易的 BTC 价格最低涨幅百分比 |
| `max_position` | 5.0 | `SIMMER_SPRINT_MAX_POSITION` | 每笔交易的最大金额（美元） |
| `signal_source` | binance | `SIMMER_SPRINT SIGNAL` | 价格数据来源（Binance 或 Coingecko） |
| `lookback_minutes` | 5 | `SIMMER_SPRINT_lookBACK` | 价格历史数据时长（分钟） |
| `min_time_remaining` | 60 | `SIMMER_SPRINT_MIN_TIME` | 跳过剩余时间不足 60 秒的快速市场 |
| `asset` | BTC | `SIMMER_SPRINT_ASSET` | 交易资产（BTC、ETH、SOL） |
| `window` | 5m | `SIMMER_SPRINT_WINDOW` | 交易窗口时长（5 分钟或 15 分钟） |
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

1. 从 Binance 获取过去 5 分钟的每分钟价格数据（`BTCUSDT`）
2. 计算价格涨幅：`(current_price - price_5min_ago) / price_5min_ago`
3. 比较价格涨幅与当前 Polymarket 的价格走势
4. 在满足以下条件时执行交易：
   - 价格涨幅 ≥ `min_momentum_pct`（默认为 0.5%）
   - 价格波动幅度 ≥ `entry_threshold`（默认为 5 分）
   - 交易量大于平均交易量的 1.5 倍（排除价格波动较小的情况）

**示例：** 如果 BTC 在过去 5 分钟内价格上涨了 0.8%，但快速市场的实际价格仅为 0.52 美元，且价格与预期价格（约 0.55 美元）相差 3 分，则执行买入操作。

### 自定义信号

**该脚本提供模板，您可以根据自己的需求替换默认的 Binance 动量指标：**
- **多交易所价格对比**：比较 Binance、Kraken、Bitfinex 等交易所的价格差异，以预测价格走势
- **市场情绪**：结合 Twitter 或社交媒体上的信息，因为市场情绪可能影响快速市场
- **技术指标**：使用 RSI、VWAP 或您喜欢的数据源的订单流量分析
- **新闻事件**：利用新闻事件的影响进行交易决策
- **链上数据**：分析鲸鱼交易者行为、资金流动率、清算情况等

您可以通过修改 `fastloop_trader.py` 文件中的 `get_momentum()` 函数来实现自定义信号逻辑。其余部分（市场发现、数据导入、交易规模控制、费用计算）保持不变。

## 示例输出结果

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

所有交易都会被标记为 `source: "sdk:fastloop"`，这意味着：
- 投资组合会按策略分类显示
- 其他脚本不会影响快速市场的交易结果
- 您可以单独跟踪快速市场的盈亏情况

## 常见问题及解决方法

- **“未找到活跃的快速市场”**：可能是因为快速市场尚未启动（非交易时段或周末）
- 请直接在 Polymarket 上检查是否有活跃的 BTC 快速市场
- **“剩余时间少于 60 秒时未找到快速市场”**：当前交易窗口即将结束，下一个市场尚未开放
- 如果希望更频繁地交易，请减小 `min_time_remaining` 的值
- **“数据导入失败：达到每日导入次数上限”**：免费账户每天只能导入 10 次；专业账户每天可导入 50 次
- **“无法获取价格数据”**：可能是 Binance API 故障或受到速率限制
- 可尝试使用 `--set signal_source=coingecko` 作为备用数据源
- **“交易失败：市场流动性不足”**：快速市场的交易量较低，可尝试减小持仓规模
- **“外部钱包需要预签名订单”**：确保环境变量 `WALLET_PRIVATE_KEY` 已设置
- SDK 会自动签署订单，无需手动操作
- 如果问题仍然存在，请尝试将 `WALLET_PRIVATE_KEY` 设置为正确的私钥（例如 `export WALLET_PRIVATE_KEY=0x<your-polymarket-wallet-private-key>`），切勿手动签署订单或修改脚本代码
- **“账户余额显示为 0 美元，但实际有 USDC”**：Polymarket 使用的是桥接后的 USDC（合约地址 `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`），而非原生 USDC
- 如果您最近将 USDC 桥接到了 Polygon，可能需要先将桥接后的 USDC 转换为原生 USDC，然后再尝试交易