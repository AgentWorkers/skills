---
name: crypto-trader
description: OpenClaw的自动化加密货币交易技能：支持8种交易策略（网格交易、定期定额投资（DCA）、趋势跟踪、套利、波段交易、复制交易、投资组合再平衡），支持多交易所连接（Binance、Bybit、Kraken、Coinbase），具备人工智能驱动的情绪分析功能，提供全面的风险管理工具、回测功能以及模拟交易体验，并通过Telegram/Discord/Email发送实时监控提醒。适用于用户咨询加密货币交易、投资组合管理、市场分析、交易策略的启动/停止、查看余额或运行回测等需求。
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: ["BINANCE_API_KEY", "BINANCE_API_SECRET"]
    primaryEnv: "BINANCE_API_KEY"
---
# 加密货币交易技能

该技能支持自动化加密货币交易，包含8种交易策略、多交易所支持、AI情绪分析以及全面的风险管理功能。

**重要提示**：默认情况下，所有操作都在**测试网**（模拟交易）上进行。只有在用户明确表示希望使用真实资金进行交易时，才需要将`CRYPTO_DEMO`设置为`false`。

## 先决条件

请从技能目录中安装所需的依赖项：

```bash
pip install -r {baseDir}/requirements.txt
```

**所需的环境变量**（在`.env`文件中设置或通过OpenClaw配置）：
- `BINANCE_API_KEY` 和 `BINANCE_API_SECRET`（用于Binance）
- `CRYPTO_DEMO=true`（默认：模拟交易模式）

**可选环境变量**：
- `BYBIT_API_KEY`, `BYBIT_API_SECRET`（用于Bybit）
- `KRAKEN_API_KEY`, `KRAKEN_API_SECRET`（用于Kraken）
- `COINBASE_API_KEY`, `COINBASE_API_SECRET`（用于Coinbase）
- `TELEGRAM_BOT_TOKEN`, `TELEGRAM_chat_ID`（用于Telegram警报）
- `DISCORD_WEBHOOK_URL`（用于Discord警报）
- `CRYPTOPANIC_API_KEY`（用于情绪分析）

## 可用功能

### 1. status -- 投资组合和策略概览

```bash
python3 {baseDir}/scripts/main.py --mode status
```

返回以下信息的JSON数据：
- 各交易所的投资组合价值
- 正在运行的策略及其状态
- 风险状况（每日盈亏、回撤率、紧急停止机制）
- 运行模式（模拟/真实交易）

当用户询问“我的投资组合情况如何？”、“当前有哪些策略在运行？”或“给我一个概览”时使用。

### 2. balance -- 检查交易所余额

```bash
python3 {baseDir}/scripts/main.py --mode balance
python3 {baseDir}/scripts/main.py --mode balance --exchange binance
```

返回指定交易所（或所有交易所）的余额信息，包括每种资产的总金额、可用金额和已使用金额。

当用户询问“我有多少比特币？”、“我的余额是多少？”或“显示我的资金情况”时使用。

### 3. start_strategy -- 启动交易策略

```bash
python3 {baseDir}/scripts/main.py --mode start_strategy --strategy grid --params '{"symbol":"BTC/USDT","price_range":[90000,110000],"num_grids":10,"order_amount_usdt":10}'
python3 {baseDir}/scripts/main.py --mode start_strategy --strategy dca --params '{"symbol":"ETH/USDT","interval":"daily","amount_per_buy_usdt":5}'
python3 {baseDir}/scripts/main.py --mode start_strategy --strategy trend --params '{"symbol":"BTC/USDT","timeframe":"4h"}'
```

支持的策略包括：
| 策略 | 名称 | 描述 |
|----------|------|-------------|
| Grid Trading | `grid_trading` | 在价格区间内等间距买入/卖出 |
| DCA | `dca` | 定期买入固定金额 |
| Trend Following | `trend_following` | 基于EMA交叉和RSI信号的交易策略 |
| Scalping | `scalping` | 利用价格波动进行快速小额交易 |
| Arbitrage | `arbitrage` | 利用不同交易所之间的价格差异进行套利 |
| Swing Trading | `swing_trading` | 基于Bollinger Bands和MACD的交易策略，持有时间2-14天 |
| Copy Trading | `copy_trading` | 复制跟踪钱包/交易者的交易 |
| Rebalancing | `rebalancing` | 重新平衡投资组合配置 |

每种策略都使用`config/strategies.yaml`文件中的默认参数，用户可以通过`--params`参数进行自定义。

**重要提示**：在启动任何策略之前，务必先与用户确认。清晰地展示参数并获取用户的批准。

当用户请求“开始比特币的网格交易”、“我想对以太坊进行DCA投资”或“跟随SOL的趋势进行交易”时使用。

### 4. stop_strategy -- 停止正在运行的策略

```bash
python3 {baseDir}/scripts/main.py --mode stop_strategy --strategy-id <id>
```

用于停止特定的交易策略。策略的ID会在启动时显示，并在列表中列出。

### 5. list_strategies -- 列出所有策略

```bash
python3 {baseDir}/scripts/main.py --mode list_strategies
```

返回所有可用且正在运行的策略，包括它们的状态、参数和性能指标。

### 6. backtest -- 在历史数据上测试策略

```bash
python3 {baseDir}/scripts/main.py --mode backtest --strategy grid_trading --params '{"symbol":"BTC/USDT","price_range":[40000,50000],"num_grids":10}' --start 2025-01-01 --end 2025-12-31
python3 {baseDir}/scripts/main.py --mode backtest --strategy dca --params '{"symbol":"BTC/USDT","interval":"daily","amount_per_buy_usdt":10}' --start 2025-06-01 --end 2025-12-31
python3 {baseDir}/scripts/main.py --mode backtest --strategy trend_following --params '{"symbol":"BTC/USDT","timeframe":"4h"}' --start 2025-01-01 --end 2025-12-31
```

返回以下性能指标：
- 相对于买入并持有的总回报百分比
- 胜率、交易数量
- 最大回撤率、夏普比率
- 费用影响
- 单个订单的历史记录

结果保存在`data/backtests/`文件夹中。

当用户询问“网格交易策略会有效吗？”、“对以太坊进行DCA测试”或“测试这个策略”时使用。

### 7. history -- 交易历史记录

```bash
python3 {baseDir}/scripts/main.py --mode history --days 7
python3 {baseDir}/scripts/main.py --mode history --days 30
```

返回过去N天内所有交易所的已完成交易记录。

### 8. sentiment -- 市场情绪分析

```bash
python3 {baseDir}/scripts/main.py --mode sentiment --symbol BTC
python3 {baseDir}/scripts/main.py --mode sentiment --symbol ETH
```

分析来自以下来源的情绪数据：
- 加密货币新闻RSS源（CoinTelegraph、CoinDesk）
- CryptoPanic（需要API密钥）
- Reddit（r/cryptocurrency、r/bitcoin）
- Twitter（需要bearer token）

返回一个综合情绪得分（范围：-1.0至1.0），标签包括：非常看跌、看跌、中性、看涨、非常看涨。

当用户询问“市场情绪如何？”、“比特币现在是否处于牛市？”或“有关以太坊的任何新闻吗？”时使用。

### 9. monitor -- 实时监控守护进程

```bash
python3 {baseDir}/scripts/main.py --mode monitor --action start
python3 {baseDir}/scripts/main.py --mode monitor --action status
python3 {baseDir}/scripts/main.py --mode monitor --action stop
```

该监控守护进程在后台运行，执行以下操作：
- 每10秒检查一次未成交订单
- 每60秒更新一次投资组合快照
- 每60秒检查一次风险限制
- 每5分钟评估一次策略信号
- 每30分钟进行一次情绪分析
- 通过Telegram/Discord/Email发送警报

### 10. emergency_stop -- 紧急停止机制

```bash
python3 {baseDir}/scripts/main.py --mode emergency_stop
```

立即执行以下操作：
1. 取消所有交易所的所有未成交订单
2. 停止所有正在运行的策略
3. 激活紧急停止机制（阻止所有未来的交易）

在用户发出“停止一切！”、“紧急情况！”或“取消所有交易”指令时使用。

## 配置文件

### config/exchanges.yaml
交易所连接设置、沙箱模式、速率限制。

### config/strategies.yaml
每种策略的默认参数。用户可以通过`--params`参数进行自定义。

### config/risk_limits.yaml
风险管理规则：
- `max_position_size_pct`：每个头寸的最大投资组合百分比（默认：25%）
- `max_daily_loss_eur`：每日亏损达到此金额时触发紧急停止（默认：50欧元）
- `max_drawdown pct`：达到历史最高价的回撤率时停止（默认：15%）
- `max_order_size_eur`：单笔交易的最大金额（默认：100欧元）
- `max_open_orders`：同时允许的最大订单数量（默认：50个）
- 止损（固定为5%，或跟踪3%）
- 盈利目标（10%，部分达到5%时平仓）

### config/notifications.yaml
根据事件类型和渠道设置警报发送规则。

## 安全规则

1. **绝对禁止**在真实交易模式下未经用户明确确认就执行交易。
2. 默认模式为**模拟交易**（`CRYPTO_DEMO=true`）。提醒用户当前使用的模式。
3. API密钥必须仅具有**交易**权限，**禁止**具有提款权限。
4. 自动执行风险限制。如果达到限制，请向用户说明情况。
5. 紧急停止机制始终可用，并优先于其他设置。
6. 在确认交易前，始终显示预估成本和风险。
7. 如果`CRYPTO_DEMO=false`，请明确警告用户这将使用**真实资金**。
8. 记录所有操作，用户可以随时查看历史记录。
9. 在启动策略时，展示完整的参数设置并获取用户的确认。
10. 即使用户要求，也绝不要绕过风险限制。解释设置这些限制的原因。

## 输出格式

所有功能都以结构化的JSON格式返回到标准输出（stdout）。解析这些数据并向用户提供易于理解的摘要，突出显示重要数值（盈亏、价格、风险指标）。适当使用表格进行清晰展示。

## 运行测试

```bash
cd {baseDir}
pip install pytest
python -m pytest tests/ -v
```

## 故障排除

### “交易所未初始化”
请检查目标交易所的环境变量中是否设置了正确的API密钥和密钥。

### “身份验证失败”
确认您的API密钥正确且未过期。对于测试网，请确保使用测试网密钥。

### “达到速率限制”
该技能会自动重试。如果问题持续存在，请降低策略评估的频率。

### “紧急停止机制已激活”
紧急停止机制已被触发。查看发生的情况，然后取消激活：
紧急停止的状态存储在`~/.openclaw/.crypto-trader-risk-state.json`文件中。将`"killed": false`设置为重置状态，或使用后续的CLI命令来取消激活。