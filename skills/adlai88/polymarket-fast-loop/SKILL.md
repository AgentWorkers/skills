---
name: polymarket-fast-loop
description: 使用 Simmer API，根据 CEX（中心化交易所）的价格动量信号，在 Polymarket 上进行 5 分钟和 15 分钟周期的快速交易。默认使用的信号数据来自 Binance 的 BTC/USDT 价格历史数据（klines）。适用于用户希望进行快速交易、自动化短期加密货币交易，或利用 CEX 的价格动量作为 Polymarket 交易决策的依据。
metadata:
  author: Simmer (@simmer_markets)
  version: "1.3.4"
  displayName: Polymarket FastLoop Trader
  difficulty: advanced
---# Polymarket FastLoop Trader  
使用实时价格信号在 Polymarket 上进行 5 分钟周期的加密货币快速交易。默认使用来自 Binance 的 BTC 动量指标；同样适用于 ETH 和 SOL。  

> **仅适用于 Polymarket。** 所有交易均在 Polymarket 上执行，并使用真实的 USDC 作为交易货币。使用 `--live` 选项可进行实时交易，否则为模拟交易（默认设置）。  

> **此脚本为模板。** 默认的 Binance 动量指标可帮助您快速开始使用该技能——您可以根据自己的需求替换为其他信号源或策略。该脚本负责处理所有市场发现、数据导入和交易执行等繁琐工作，您只需提供交易策略即可。  

> ⚠️ 快速交易需支付 Polymarket 的 10% 手续费（`is_paid: true`），请在交易策略中考虑这一点。  
> ⚠️ **风险监控不适用于持续时间小于 15 分钟的市场。** Simmer 的止损和止盈机制每 15 分钟检查一次交易状态，因此在 5 分钟或 15 分钟周期的市场中，这些机制可能不会触发。在 Simmer 控制面板中配置的任何风险设置对这些市场无效。请根据实际情况调整交易规模，并不要依赖自动止损功能。  

## 市场查找方式  
- 直接通过 Polymarket 的 Gamma API 查询实时快速交易市场（不依赖于 Simmer 的市场列表）  
- 每个周期自动发现新的市场  
- 支持 BTC、ETH 和 SOL——只需更改 `--set asset` 参数即可；或让脚本自动查找您感兴趣的市场  
- 脚本每 5 分钟运行一次，以捕捉每个交易窗口的机会（或每 1 分钟运行一次以捕捉窗口内的交易机会）  

**无需等待 Simmer 自动显示市场信息。** FastLoop 会实时在 Polymarket 上查找市场，然后通过 Simmer 进行交易。  

## 适用场景  
- 当用户希望使用任何支持的资产进行 5 分钟或 15 分钟周期的加密货币快速交易时  
- 自动化短期加密货币预测交易  
- 使用 CEX 的价格走势作为 Polymarket 的交易信号  
- 监控快速交易中的持仓情况  

## 设置流程  
当用户请求安装或配置此技能时，请按照以下步骤操作：  
1. **获取 Simmer API 密钥**  
   - 从 `simmer.markets/dashboard` 的 SDK 标签页获取  
   - 将其存储在环境变量 `SIMMER_API_KEY` 中  

2. **提供钱包私钥**（实时交易必需）  
   - 这是用于 Polymarket 钱包的私钥（存储 USDC 的钱包）  
   - 将其存储在环境变量 `WALLET_PRIVATE_KEY` 中  
   - SDK 会使用此私钥在客户端自动签名交易订单，无需手动操作  

3. **配置参数**（或确认默认值）  
   - 交易资产：BTC、ETH 或 SOL（默认为 BTC）  
   - 进场阈值：触发交易的最低价格波动幅度（默认为 5 分钱）  
   - 每笔交易的最大金额：$5.00  
   - 交易周期：5 分钟或 15 分钟（默认为 5 分钟）  

4. **设置定时任务或循环执行**（用户负责安排执行频率——详见“如何循环执行”部分）  

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

## 如何循环执行脚本  
脚本会**自动运行一个周期**，具体执行方式由用户自行设置：  
- **Linux crontab**（本地或 VPS 环境）：  
  ```
# Every 5 minutes (one per fast market window)
*/5 * * * * cd /path/to/skill && python fastloop_trader.py --live --quiet

# Every 1 minute (more aggressive, catches mid-window opportunities)
* * * * * cd /path/to/skill && python fastloop_trader.py --live --quiet
```  
- **OpenClaw 原生 cron 任务**（容器化或 OpenClaw 管理的环境）：  
  ```bash
openclaw cron add \
  --name "Fast Loop Trader" \
  --cron "*/5 * * * *" \
  --tz "UTC" \
  --session isolated \
  --message "Run fast loop trader: cd /path/to/skill && python fastloop_trader.py --live --quiet. Show the output summary." \
  --announce
```  
- **通过 OpenClaw 的心跳机制执行**：  
  在 `HEARTBEAT.md` 文件中进行配置：  
  ```
Run: cd /path/to/fast market && python fastloop_trader.py --live --quiet
```  

## 配置方式  
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
| `entry_threshold` | 0.05 | `SIMMER_SPRINT_ENTRY` | 触发交易的最低价格波动幅度（分钱）  
| `min_momentum_pct` | 0.5 | `SIMMER_SPRINT_MOMENTUM` | 触发交易的 BTC 价格最低涨幅百分比（%）  
| `max_position` | 5.0 | `SIMMER_SPRINT_MAX_POSITION` | 每笔交易的最大金额（美元）  
| `signal_source` | binance | `SIMMER_SPRINT SIGNAL` | 价格数据源（Binance 或 Coingecko）  
| `lookback_minutes` | 5 | `SIMMER_SPRINT_lookBACK` | 价格历史数据保留的时间（分钟）  
| `min_time_remaining` | 60 | `SIMMER_SPRINT_MIN_TIME` | 跳过剩余时间不足 60 秒的快速市场  
| `asset` | BTC | `SIMMER_SPRINT_ASSET` | 交易资产（BTC、ETH、SOL）  
| `window` | 5m | `SIMMER_SPRINT_WINDOW` | 交易周期（5 分钟或 15 分钟）  
| `volume_confidence` | true | `SIMMER_SPRINT_VOL_CONF` | 是否根据 Binance 的交易量加权信号  

### 示例 `config.json` 文件  
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
1. 从 Binance 获取过去 5 分钟内的价格数据（`BTCUSDT`）  
2. 计算价格涨幅：`(current_price - price_5min_ago) / price_5min_ago`  
3. 比较价格涨幅与当前 Polymarket 的价格走势  
4. 当满足以下条件时执行交易：  
   - 价格涨幅 ≥ `min_momentum_pct`（默认 0.5%）  
   - 价格波动幅度 ≥ `entry_threshold`（默认 5 分钱）  
   - 交易量超过平均交易量的 1.5 倍（排除价格波动较小的情况）  

**示例：** 如果过去 5 分钟内 BTC 价格上涨了 0.8%，但快速市场的实际价格仅为 $0.52，且价格与预期价格 $0.55 的差距为 3 分钱，则执行买入操作。**  

### 自定义信号  
**此脚本为模板，Binance 动量指标仅作为起点。** 您可以根据需要替换为其他信号源：  
- **多交易所价格对比**：比较 Binance、Kraken、Bitfinex 等交易所的价格差异，以预测价格走势  
- **市场情绪**：结合 Twitter 或社交媒体的实时信息，因为市场情绪可能影响价格波动  
- **技术指标**：使用 RSI、VWAP 或其他技术指标  
- **新闻事件**：利用新闻信息分析市场趋势  
- **链上数据**：分析鲸鱼交易者行为、资金流动情况等  

要自定义信号逻辑，请编辑 `fastloop_trader.py` 文件中的 `get_momentum()` 函数或添加自己的信号处理函数。其余部分（市场发现、数据导入、交易规模调整等）保持不变。  

## 示例输出结果  
所有交易都会被标记为 `source: "sdk:fastloop"`，这意味着：  
- 投资组合会按策略进行分类显示  
- 其他技能不会影响快速交易的盈亏情况  
- 可以单独追踪快速交易的盈利和亏损  

## 常见问题及解决方法：  
- **“未找到活跃的快速市场”**：可能是因为市场处于非交易时间或周末  
  - 请直接在 Polymarket 上查看是否有活跃的 BTC 快速市场  
- **“剩余时间少于 60 秒的市场无法交易”**：当前交易窗口即将结束，下一个市场尚未开放  
  - 可以减小 `min_time_remaining` 值以在更接近交易结束的时间点进行交易  
- **“数据导入失败：达到每日导入次数限制”**：免费账户每天只能导入 10 次；专业账户每天可导入 50 次  
  - 快速交易需要专业账户才能更频繁地执行  
- **“无法获取价格数据”**：可能是 Binance API 出现故障或达到请求限制  
  - 可尝试使用 `--set signal_source=coingecko` 作为备用数据源  
- **“交易失败：市场流动性不足”**：快速市场的交易量较小，可尝试减小交易规模  
- **“外部钱包需要预签名订单”**：确保环境变量 `WALLET_PRIVATE_KEY` 已设置  
  - SDK 会自动签名订单，无需手动操作  
- **“账户余额显示为 $0，但实际上有 USDC”**：Polymarket 使用的是桥接后的 USDC（合约地址 `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`），而非原生 USDC  
  - 如果您最近将 USDC 桥接到了 Polygon，可能需要先将 USDC 转换为原生 USDC 后再尝试交易  

---