---
name: polymarket-weather-trader
displayName: Polymarket Weather Trader
description: 通过 Simmer API 利用 NOAA 的天气预报数据在 Polymarket 平台上进行交易。该策略的灵感来源于 gopfan2 的策略（其交易金额超过了 200 万美元）。适用于用户希望交易与温度相关的天气衍生品、自动化天气相关交易决策、查看 NOAA 天气预报，或执行类似 gopfan2 的交易策略的场景。
metadata: {"clawdbot":{"emoji":"🌡️","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false,"automaton":{"managed":true,"entrypoint":"weather_trader.py"}}}
authors:
  - Simmer (@simmer_markets)
attribution: "Strategy inspired by gopfan2"
version: "1.10.1"
published: true
---
# Polymarket 天气交易策略

使用 NOAA 预报数据在 Polymarket 上交易温度相关市场。

> **这是一个模板。** 默认的信号源是 NOAA 的温度预报数据——您可以根据需要将其与其他天气 API、不同的预报模型或额外的市场类型（如降水、风速等）结合使用。该策略会处理所有相关流程（市场发现、数据解析、交易执行及风险控制）。具体的交易决策由用户自行做出。

## 何时使用此策略

当用户希望：
- 自动交易天气相关市场
- 设置类似 gopfan2 的温度交易规则
- 在天气预测价格低时买入
- 查看自己的天气交易持仓
- 配置交易阈值或交易地点时，可以使用此策略。

## v1.2.0 的新功能

- **每次扫描周期的最大交易数量**：新增了 `SIMMER_WEATHER_MAX_TRADES` 配置参数，用于限制每次扫描周期内的最大交易数量（默认值为 5 笔）。

### v1.1.1
- **状态检查脚本**：新增了 `scripts/status.py` 脚本，用于快速查看账户余额和持仓情况。
- **API 参考**：增加了“快速命令”部分，其中包含了 API 的相关端点信息。

### v1.1.0
- **交易标记**：所有交易都会被标记为 `sdk:weather`，以便于进行投资组合管理。
- **智能持仓规模调整**：根据可用余额自动调整交易规模（使用 `--smart-sizing` 参数）。
- **风险控制机制**：检查市场价格波动、滑点以及价格衰减情况。
- **价格趋势检测**：检测近期价格下跌趋势，以生成更强的买入信号。

## 设置流程

当用户请求安装或配置此策略时，请按照以下步骤操作：
1. **获取 Simmer API 密钥**：
   - 可以从 simmer.markets/dashboard 的 SDK 标签页获取该密钥。
   - 将其存储在环境变量 `SIMMER_API_KEY` 中。

2. **提供钱包私钥**（用于实时交易）：
   - 这是用户的 Polymarket 钱包私钥（用于存储 USDC）。
   - 将其存储在环境变量 `WALLET_PRIVATE_KEY` 中。
   - SDK 会使用此私钥在客户端自动签署交易订单，无需用户手动操作。

3. **配置交易参数**（或确认默认设置）：
   - **入场阈值**：价格低于该阈值时买入（默认为 0.15 美分）。
   - **出场阈值**：价格高于该阈值时卖出（默认为 0.45 美分）。
   **每次交易的最大持仓金额**：每次交易的最大金额（默认为 2.00 美元）。
   **交易地点**：指定进行交易的城市（默认为纽约市）。

4. **将配置保存到环境变量中**。

5. **设置定时任务**（默认关闭——用户需要手动启用定时执行）。

## 配置参数

| 参数 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| 入场阈值 | `SIMMER_WEATHER_ENTRY` | 0.15 | 价格低于此阈值时买入 |
| 出场阈值 | `SIMMER_WEATHER_EXIT` | 0.45 | 价格高于此阈值时卖出 |
| 每次交易的最大持仓金额 | `SIMMER_WEATHER_MAX_POSITION` | 2.00 | 每次交易的最大金额 |
| 每次扫描周期的最大交易数量 | `SIMMER_WEATHER_MAX_TRADES` | 5 | 每次扫描周期内的最大交易数量 |
| 交易地点 | `SIMMER_WEATHER_LOCATIONS` | NYC | 用逗号分隔的城市列表 |
| 智能持仓比例 | `SIMMER_WEATHER_SIZING_PCT` | 0.05 | 每笔交易占可用余额的百分比 |

**支持的交易地点**：纽约市、芝加哥、西雅图、亚特兰大、达拉斯、迈阿密

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

脚本的工作流程如下：
1. 每个周期从 Simmer API 获取活跃的天气市场数据。
2. 按事件类型对市场进行分类（每个温度数据对应一个事件）。
3. 解析事件信息以获取具体地点和日期。
4. 获取该地点/日期的 NOAA 预报数据。
5. 找到与预报数据匹配的温度区间。
6. **风险控制**：检查市场价格波动、滑点以及价格衰减情况。
7. **价格趋势检测**：检测近期价格下跌趋势，以生成更强的买入信号。
8. **交易决策**：如果价格低于入场阈值且满足其他风险控制条件，则买入。
9. **卖出判断**：检查当前持仓情况，如果价格高于出场阈值则卖出。
10. **交易标记**：所有交易都会被标记为 `sdk:weather`，以便后续跟踪。

## 智能持仓规模调整

使用 `--smart-sizing` 参数时，持仓规模会根据以下规则计算：
- 可用 USDC 余额的 5%（可通过 `SIMMER_WEATHER_SIZING_PCT` 参数调整）。
- 最大持仓金额上限为 2.00 美元（默认值）。
- 如果投资组合余额不足，持仓规模将回退到固定值。

**风险控制机制**

在交易前，脚本会进行以下检查：
- **价格波动风险**：如果市场价格波动过于剧烈，则跳过当前交易。
- **滑点风险**：如果预计滑点超过 15%，则跳过交易。
- **市场状态**：如果市场在 2 小时内已恢复正常，則跳过交易。
- **市场状态变化**：如果市场状态已经发生变化（如价格反转），则跳过交易。

可以通过 `--no-safeguards` 参数关闭这些风险控制机制（但不建议这样做）。

**交易标记**

所有交易都会被标记为 `source: "sdk:weather"`，这有助于：
- 在投资组合报告中按策略分类显示交易情况。
- 防止复制交易策略误售用户的天气交易持仓。
- 用户可以单独查看天气交易的盈亏情况。

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

**“风险控制提示：严重价格波动”**
- 该市场的价格波动过于剧烈，建议稍后再进行交易。

**“滑点过高”**
- 市场流动性较低，建议减小持仓规模或跳过交易。

**“市场将在 X 小时内恢复正常”**
- 市场即将恢复正常，但风险较高，建议谨慎操作。

**“未找到天气相关市场”**
- 可能是因为当前季节该市场不活跃。

**“外部钱包需要预签名订单”**
- 确保环境变量 `WALLET_PRIVATE_KEY` 已设置正确。SDK 会自动使用该密钥签署交易订单，无需手动操作。
- 解决方法：`export WALLET_PRIVATE_KEY=0x<your-polymarket-wallet-private-key>`。
- **注意**：切勿尝试手动签署订单或修改策略代码，SDK 会自动处理交易。

**“余额显示为 0 美元，但我有 USDC 存在 Polymarket 上”**
- Polymarket 使用的是 **USDC.e**（桥接后的 USDC，合约地址为 `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`），而非原生 USDC。
- 如果您最近将 USDC 桥接到了 Polygon，可能需要先将 USDC.e 转换为原生 USDC 后再尝试交易。

**“API 密钥无效”**
- 请从 simmer.markets/dashboard 的 SDK 标签页重新获取 API 密钥。