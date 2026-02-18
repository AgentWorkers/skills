---
name: polymarket-weather-trader
displayName: Polymarket Weather Trader
description: 通过 Simmer API 利用 NOAA 的天气预报数据在 Polymarket 平台上进行交易。该策略的灵感来源于 gopfan2 的策略（该策略已获得超过 200 万美元的收益）。适用于用户希望交易与温度相关的金融产品、自动执行基于天气数据的交易决策、查看 NOAA 的天气预报数据，或采用 gopfan2 的交易策略进行操作的情况。
metadata: {"clawdbot":{"emoji":"🌡️","requires":{"env":["SIMMER_API_KEY"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
attribution: "Strategy inspired by gopfan2"
version: "1.7.2"
published: true
---

# Polymarket 天气交易策略

使用 NOAA 预报数据在 Polymarket 上交易温度相关市场。

## 适用场景

当用户希望执行以下操作时，可以使用此策略：
- 自动交易天气相关市场
- 设置类似 gopfan2 的温度交易规则
- 在天气预测价格较低时买入
- 查看当前的天气交易持仓
- 配置交易阈值或交易地点

## v1.2.0 的新功能

- **单次扫描的最大交易次数**：新增了 `SIMMER_WEATHER_MAX_TRADES` 配置参数，用于限制每次扫描周期内的交易次数（默认值为 5 次）

### v1.1.1
- **状态检查脚本**：新增了 `scripts/status.py` 脚本，用于快速检查账户余额和持仓情况
- **API 参考**：增加了快速命令部分，提供了 API 端点信息

### v1.1.0
- **交易标记**：所有交易都被标记为 `sdk:weather`，以便于跟踪投资组合
- **智能持仓调整**：根据可用余额自动调整持仓规模（使用 `--smart-sizing` 参数）
- **风险防护机制**：检查市场价格波动、滑点以及价格走势变化
- **价格趋势检测**：识别近期价格下跌情况，以获取更强的买入信号

## 设置流程

当用户请求安装或配置此策略时，请按照以下步骤操作：
1. **获取 Simmer API 密钥**：
   - 可以从 simmer.markets/dashboard 的 SDK 标签页获取该密钥
   - 将密钥保存为环境变量 `SIMMER_API_KEY`
2. **确认设置**（或使用默认值）：
   - **买入阈值**：价格低于该阈值时买入（默认为 0.15 美分）
   - **卖出阈值**：价格高于该阈值时卖出（默认为 0.45 美分）
   - **单次最大交易金额**：每次交易的最大金额（默认为 2.00 美元）
   **交易地点**：指定进行交易的城市（默认为纽约市 NYC）
3. **将设置保存到环境变量中**
4. **配置定时任务**（默认关闭——用户需要手动启用）

## 配置参数

| 参数 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| 买入阈值 | `SIMMER_WEATHER_ENTRY` | 0.15 | 价格低于此值时买入 |
| 卖出阈值 | `SIMMER_WEATHER_EXIT` | 0.45 | 价格高于此值时卖出 |
| 单次最大交易金额 | `SIMMER_WEATHER_MAX_POSITION` | 2.00 | 每次交易的最大金额（美元） |
| 每次扫描的最大交易次数 | `SIMMER_WEATHER_MAX_TRADES` | 5 | 每次扫描周期内的最大交易次数 |
| 交易地点 | `SIMMER_WEATHER_LOCATIONS` | NYC | 用逗号分隔的城市列表 |
| 智能持仓调整比例 | `SIMMER_WEATHER_SIZING_PCT` | 0.05 | 每笔交易的持仓金额占可用余额的百分比 |

**支持的交易地点**：纽约市（NYC）、芝加哥（Chicago）、西雅图（Seattle）、亚特兰大（Atlanta）、达拉斯（Dallas）、迈阿密（Miami）

## 快速命令

```bash
# Check account balance and positions
python scripts/status.py

# Detailed position list
python scripts/status.py --positions
```

**API 参考**：
- 基础 URL：`https://api.simmer.markets`
- 认证方式：`Authorization: Bearer $SIMMER_API_KEY`
- 投资组合信息：`GET /api/sdk/portfolio`
- 持仓信息：`GET /api/sdk/positions`

## 运行策略

```bash
# Dry run (default — shows opportunities, no trades)
python weather_trader.py

# Execute real trades
python weather_trader.py --live

# With smart position sizing (uses portfolio balance)
python weather_trader.py --live --smart-sizing

# Check positions only
python weather_trader.py --positions

# View config
python weather_trader.py --config

# Disable safeguards (not recommended)
python weather_trader.py --no-safeguards

# Disable trend detection
python weather_trader.py --no-trends

# Quiet mode — only output on trades/errors (ideal for high-frequency runs)
python weather_trader.py --live --quiet

# Combine: frequent scanning, minimal noise
python weather_trader.py --live --smart-sizing --quiet
```

## 工作原理

该策略每个周期会执行以下操作：
1. 从 Simmer API 获取当前活跃的天气市场数据
2. 按事件类型对市场进行分类（每个温度数据对应一个事件）
3. 解析事件名称以获取具体地点和日期
4. 获取该地点/日期的 NOAA 预报数据
5. 找到与预报数据匹配的温度区间
6. **风险防护机制**：
   - 检查市场价格是否出现剧烈波动（“翻转警告”）
   - 检查交易是否因滑点导致损失
   - 检查市场是否在 2 小时内完成价格变动
7. **价格趋势检测**：识别近期价格下跌情况，以获取更强的买入信号
8. **买入操作**：如果价格低于买入阈值且满足其他风险防护条件，则执行买入
9. **卖出操作**：检查当前持仓情况，如果价格高于卖出阈值，则卖出
10. **交易标记**：所有交易都会被标记为 `sdk:weather`，以便于后续跟踪

## 智能持仓调整

使用 `--smart-sizing` 参数时，持仓规模会按照以下方式计算：
- 占可用 USDC 余额的 5%（可通过 `SIMMER_WEATHER_SIZING_PCT` 参数进行配置）
- 最大持仓金额不超过 `SIMMER_WEATHER_MAX_POSITION` 的限制（默认为 2.00 美元）
- 如果投资组合中的资金不足，持仓规模会恢复为固定值

**注意事项**：
- 此机制可防止过度交易，并根据账户规模自动调整持仓规模。

## 风险防护机制

在交易前，该策略会进行以下检查：
- **价格波动警告**：如果市场价格波动过于剧烈，则跳过当前交易
- **滑点风险**：如果预计滑点超过 15%，则跳过交易
- **市场状态**：如果市场在 2 小时内完成价格变动，则跳过交易
- **市场状态**：如果市场已经完成价格变动，则跳过交易

可以通过 `--no-safeguards` 参数关闭这些风险防护机制（不推荐使用）。

## 交易标记

所有交易都会被标记为 `source: "sdk:weather"`，这意味着：
- 投资组合报表会按策略类型显示交易明细
- 复制交易策略不会影响用户的天气交易结果
- 用户可以单独查看天气交易的盈亏情况

## 示例输出

```
🌤️ Simmer Weather Trading Skill
==================================================

⚙️ Configuration:
  Entry threshold: 15% (buy below this)
  Exit threshold:  45% (sell above this)
  Max position:    $2.00
  Locations:       NYC
  Smart sizing:    ✓ Enabled
  Safeguards:      ✓ Enabled
  Trend detection: ✓ Enabled

💰 Portfolio:
  Balance: $150.00
  Exposure: $45.00
  Positions: 8

📍 NYC 2026-01-28 (high temp)
  NOAA forecast: 34°F
  Matching bucket: 34-35°F @ $0.12
  💡 Smart sizing: $2.00 (capped at max position)
  ✅ Below threshold ($0.15) - BUY opportunity! 📉 (dropped 15% in 24h)
  Executing trade...
  ✅ Bought 62.5 shares @ $0.12

📊 Summary:
  Events scanned: 12
  Entry opportunities: 1
  Trades executed: 1
```

## 常见问题及解决方法

- **“风险防护机制触发：严重价格波动警告”**：表示该市场价格波动过于剧烈，建议等待后再进行交易
- **“滑点过高”**：市场流动性较低，建议减小持仓规模或跳过交易
- **“市场在 X 小时内完成价格变动”**：市场即将完成价格变动，风险增加，建议谨慎操作
- **“未找到天气市场”**：可能是因为当前季节该市场不活跃
- **“API 密钥无效”**：请从 simmer.markets/dashboard 的 SDK 标签页重新获取 API 密钥