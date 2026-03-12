---
name: polymarket-fast-loop
description: 使用 Simmer API，根据 CEX（中心化交易所）的价格动量信号，在 Polymarket 上进行 5 分钟和 15 分钟周期的快速交易。默认使用的信号数据来自 Binance 的 BTC/USDT 交易记录（klines）。适用于用户希望进行快速交易、自动化短期加密货币交易，或利用 CEX 的价格动量作为 Polymarket 的交易决策依据的情况。
metadata:
  author: Simmer (@simmer_markets)
  version: "1.3.5"
  displayName: Polymarket FastLoop Trader
  difficulty: advanced
---# Polymarket FastLoop Trader  
利用实时价格信号，在Polymarket上进行5分钟周期的加密货币快速交易。默认使用来自Binance的BTC价格趋势作为交易信号；同样适用于ETH和SOL资产。  

> **仅限Polymarket平台**：所有交易均在Polymarket上执行，且使用USDC作为交易货币。使用`--live`选项可进行实时交易，否则为模拟交易（dry-run模式）。  

> **此脚本为模板**：默认使用的Binance价格趋势信号可帮助您快速上手；您可以根据自己的需求替换为自定义信号或数据源。该脚本负责市场发现、数据导入及交易执行等所有底层逻辑。您只需提供交易策略即可。  

> ⚠️ 快速交易需支付Polymarket的10%手续费（`is_paid: true`），请在交易策略中考虑这一费用。  
> ⚠️ **风险监控不适用于周期小于15分钟的市场**：Simmer的止损和止盈机制每15分钟检查一次持仓情况，因此在5分钟或15分钟周期的市场中，这些机制可能不会触发。在Simmer控制台中配置的风险设置对这些市场无效。请根据实际情况调整交易规模，并避免依赖自动止损功能进行快速交易。  

## 市场查找方式  
- 直接通过Polymarket的Gamma API查询实时快速交易市场；  
- 每个周期自动发现新的交易市场；  
- 支持BTC、ETH和SOL资产（通过`--set asset=ETH`参数调整）；  
- 脚本每5分钟运行一次，以捕捉每个交易窗口的交易机会（或每1分钟运行一次，以捕捉窗口内的交易机会）。  

**无需等待Simmer自动显示市场**：FastLoop会实时在Polymarket上查找市场信息，然后通过Simmer执行交易。  

## 适用场景  
- 当用户希望在任何支持的资产上进行5分钟或15分钟的加密货币快速交易时；  
- 用于自动化短期加密货币交易策略；  
- 希望使用CEX的价格趋势作为Polymarket的交易信号时；  
- 需要监控快速交易市场中的持仓情况时。  

## 设置流程  
当用户请求安装或配置此脚本时，请按照以下步骤操作：  
1. **获取Simmer API密钥**：  
   - 从`simmer.markets/dashboard`的SDK选项卡中获取API密钥；  
   - 将其存储在环境变量`SIMMER_API_KEY`中。  

2. **提供钱包私钥**（用于实时交易）：  
   - 这是用户Polymarket钱包的私钥（用于存储USDC的钱包）；  
   - 将其存储在环境变量`WALLET_PRIVATE_KEY`中；  
   - SDK会使用该密钥在客户端自动签署交易订单（无需手动操作）。  

3. **配置参数**（或确认默认值）：  
   - 资产：BTC、ETH或SOL（默认为BTC）；  
   - 入场价格阈值：触发交易的最低价格波动幅度（默认为5美分）；  
   - 每笔交易的最大金额：$5.00；  
   - 交易周期：5分钟或15分钟（默认为5分钟）。  

4. **设置定时任务**：  
   - 由用户自行安排脚本的执行频率（参见“如何设置定时任务”部分）。  

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

## 如何设置定时任务  
脚本会按照预设的周期自动运行。您可以通过以下方式设置定时任务：  
- **Linux crontab**（适用于本地或VPS环境）：  
```
# Every 5 minutes (one per fast market window)
*/5 * * * * cd /path/to/skill && python fastloop_trader.py --live --quiet

# Every 1 minute (more aggressive, catches mid-window opportunities)
* * * * * cd /path/to/skill && python fastloop_trader.py --live --quiet
```  
- **OpenClaw原生cron任务**（适用于容器化或OpenClaw管理的环境）：  
```bash
openclaw cron add \
  --name "Fast Loop Trader" \
  --cron "*/5 * * * *" \
  --tz "UTC" \
  --session isolated \
  --message "Run fast loop trader: cd /path/to/skill && python fastloop_trader.py --live --quiet. Show the output summary." \
  --announce
```  
- **通过OpenClaw的Heartbeat功能**：  
   - 在`HEARTBEAT.md`文件中进行配置：  
```
Run: cd /path/to/fast market && python fastloop_trader.py --live --quiet
```  

## 配置选项  
配置参数可通过`config.json`文件、环境变量或`--set`命令进行调整：  
```bash
# Change entry threshold
python fastloop_trader.py --set entry_threshold=0.08

# Trade ETH instead of BTC
python fastloop_trader.py --set asset=ETH

# Multiple settings
python fastloop_trader.py --set min_momentum_pct=0.3 --set max_position=10
```  

### 配置参数说明  
| 参数 | 默认值 | 环境变量 | 说明 |  
|---------|---------|---------|-------------|  
| `entry_threshold` | 0.05 | `SIMMER_SPRINT_ENTRY` | 触发交易的最低价格波动幅度（50美分）；  
| `min_momentum_pct` | 0.5 | `SIMMER_SPRINT_MOMENTUM` | 触发交易的BTC价格最低涨幅百分比；  
| `max_position` | 5.0 | `SIMMER_SPRINT_MAX_POSITION` | 每笔交易的最高金额；  
| `signal_source` | binance | `SIMMER_SPRINT_SIGNAL` | 价格数据来源（Binance或Coingecko）；  
| `lookback_minutes` | 5 | `SIMMER_SPRINT_lookBACK` | 价格历史数据的查看时长（分钟）；  
| `min_time_remaining` | 60 | `SIMMER_SPRINT_MIN_TIME` | 忽略剩余时间不足60秒的快速市场；  
| `asset` | BTC | `SIMMER_SPRINT_ASSET` | 交易资产（BTC、ETH、SOL）；  
| `window` | 5m | `SIMMER_SPRINT_WINDOW` | 交易窗口时长（5分钟或15分钟）；  
| `volume_confidence` | true | `SIMMER_SPRINT_VOL_CONF` | 是否根据Binance的交易量加权信号；  

### 示例`config.json`文件  
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

## 命令行参数  
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
**默认使用Binance价格趋势作为交易信号**：  
1. 从Binance获取过去5分钟的每分钟价格数据（以BTCUSDT计）；  
2. 计算价格趋势：`(current_price - price_5min_ago) / price_5min_ago`；  
3. 比较当前价格趋势与Polymarket的市场价格；  
4. 当满足以下条件时执行交易：  
   - 价格趋势涨幅 ≥ `min_momentum_pct`（默认为0.5%）；  
   - 价格波动幅度 ≥ `entry_threshold`（默认为5美分）；  
   - 交易量大于平均交易量的1.5倍（排除价格波动较小的情况）。  

**示例**：  
- 如果过去5分钟内BTC价格上涨了0.8%，但快速交易市场中的价格仅为$0.52，且实际价格与预期价格（约$0.55）相差3美分，则执行买入操作。  

### 自定义信号  
**此脚本提供基础框架，您可以根据需要替换为自定义信号**：  
- **多交易所价格对比**：比较Binance、Kraken、Bitfinex等交易所的价格差异，以预测价格走势；  
- **市场情绪分析**：结合Twitter或社交媒体的信息，判断价格波动趋势；  
- **技术指标**：使用RSI、VWAP等技术指标进行分析；  
- **新闻影响**：利用新闻数据判断市场走势；  
- **链上数据**：分析大额交易者的行为、资金流动情况等。  

要自定义信号逻辑，请修改`fastloop_trader.py`文件中的`get_momentum()`函数或添加自定义函数。其余部分（市场发现、数据导入、交易规模调整等）保持不变。  

## 示例交易结果  
所有交易都会被标记为`source: "sdk:fastloop"`，便于进行统计和分析：  
- 投资组合会按交易策略进行分类显示；  
- 其他脚本不会干扰快速交易的盈利与亏损情况；  
- 可以单独追踪快速交易的盈亏情况。  

## 常见问题及解决方法：  
- **“未找到活跃的快速交易市场”**：可能是因为当前市场处于非交易时段或周末；  
  - 请直接在Polymarket上查看是否有活跃的BTC快速交易市场。  
- **“剩余时间不足60秒时未找到快速交易市场”**：当前交易窗口即将结束，下一个交易窗口尚未启动；  
  - 可适当减小`min_time_remaining`参数以适应更短的交易周期。  
- **“数据导入失败”**：可能是因为每日免费使用次数已用完（10次/天），或API请求次数达到限制；  
  - 可尝试使用`--set signal_source=coingecko`作为备用数据源。  
- **“交易失败：市场流动性不足”**：快速交易市场中的交易量较低，可尝试减小交易规模；  
- **“外部钱包需要预签名订单”**：确保环境变量`WALLET_PRIVATE_KEY`已设置；  
  - SDK会自动处理订单签署；  
- **“账户余额显示为0美元，但实际上有USDC”**：Polymarket使用的是桥接后的USDC（合约地址`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`），而非原生USDC；  
  - 如果您最近将USDC桥接到了Polygon平台，请先转换回原生USDC后再尝试交易。