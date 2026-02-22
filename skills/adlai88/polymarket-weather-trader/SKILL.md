---
name: polymarket-weather-trader
displayName: Polymarket Weather Trader
description: 使用 Simmer API 通过 NOAA 预报在 Polymarket 的天气市场中进行交易。这一策略的灵感来源于 gopfan2 的盈利策略（盈利金额超过 200 万美元）。适用于用户希望交易温度相关市场、自动化天气相关交易、查看 NOAA 预报或执行类似 gopfan2 的交易策略的情况。
metadata: {"clawdbot":{"emoji":"🌡️","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false,"automaton":{"managed":true,"entrypoint":"weather_trader.py"}}}
authors:
  - Simmer (@simmer_markets)
attribution: "Strategy inspired by gopfan2"
version: "1.10.0"
published: true
---
# Polymarket 天气交易策略

使用 NOAA 的天气预报数据，在 Polymarket 上交易温度相关市场。

> **这是一个模板。** 默认的交易信号基于 NOAA 的温度预报数据——您可以根据需要将其与其他天气 API、不同的预报模型或额外的市场类型（如降水量、风速等）结合使用。该策略负责处理所有交易相关的细节（包括市场发现、数据解析、交易执行及风险控制）。您需要提供相应的交易参数（如交易阈值等）。

## 何时使用此策略

当用户希望执行以下操作时，可以使用此策略：
- 自动交易与天气相关的市场
- 设置类似 gopfan2 的温度交易策略
- 在天气预测价格较低时买入
- 查看自己的天气交易持仓
- 配置交易阈值或交易地点

## v1.2.0 的新功能

- **每次扫描周期的最大交易次数**：新增了 `SIMMER_WEATHER_MAX_TRADES` 配置参数，用于限制每次扫描周期内的交易次数（默认值为 5 次）

### v1.1.1
- **状态检查脚本**：新增了 `scripts/status.py` 脚本，用于快速查看账户余额和持仓情况
- **API 参考**：增加了“快速命令”部分，其中包含 API 的相关端点信息

### v1.1.0
- **交易标记**：所有交易都会被标记为 `sdk:weather`，以便于跟踪交易记录
- **智能持仓调整**：根据可用余额自动调整持仓规模（通过 `--smart-sizing` 参数设置）
- **风险控制机制**：检查市场反转情况、滑点以及价格波动趋势
- **价格趋势检测**：检测最近的价格下跌情况，以生成更强的买入信号

## 设置流程

当用户请求安装或配置此策略时，请按照以下步骤操作：
1. **获取 Simmer API 密钥**：
   - 可以从 simmer.markets/dashboard 的 SDK 标签页获取该密钥
   - 将其存储在环境变量 `SIMMER_API_KEY` 中

2. **提供钱包私钥**（用于实时交易）：
   - 这是用户的 Polymarket 钱包私钥（用于存储 USDC）
   - 将其存储在环境变量 `WALLET_PRIVATE_KEY` 中
   - SDK 会使用此私钥在客户端自动签署交易订单，无需手动操作

3. **确认设置参数**（或使用默认值）：
   - **买入阈值**：价格低于该阈值时买入（默认为 0.15 美分）
   - **卖出阈值**：价格高于该阈值时卖出（默认为 0.45 美分）
   **每次交易的最大持仓金额**：每次交易的最大金额（默认为 2.00 美元）
   **交易地点**：指定进行交易的城市（默认为纽约市）

4. **将设置保存到环境变量中**

5. **配置定时任务**（默认情况下定时任务是禁用的——用户需要自行启用）

## 配置参数

| 参数 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| 买入阈值 | `SIMMER_WEATHER_ENTRY` | 0.15 | 价格低于此阈值时买入 |
| 卖出阈值 | `SIMMER_WEATHER_EXIT` | 0.45 | 价格高于此阈值时卖出 |
| 每次交易的最大持仓金额 | `SIMMER_WEATHER_MAX_POSITION` | 2.00 | 每次交易的最大金额（美元） |
| 每次扫描周期的最大交易次数 | `SIMMER_WEATHER_MAX_TRADES` | 5 | 每次扫描周期内的最大交易次数 |
| 交易地点 | `SIMMER_WEATHER_LOCATIONS` | NYC | 用逗号分隔的城市列表 |
| 智能持仓调整比例 | `SIMMER_WEATHER_SIZING_PCT` | 0.05 | 每次交易的持仓金额占可用余额的百分比 |

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
- 账户信息：`GET /api/sdk/portfolio`
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
3. 解析事件信息以获取具体地点和日期
4. 获取该地点/日期的 NOAA 天气预报数据
5. 找到与预报数据匹配的温度区间
6. **风险控制**：检查市场是否存在反转风险、滑点以及价格波动趋势
7. **价格趋势检测**：检测最近的价格下跌情况，以生成更强的买入信号
8. **买入操作**：如果价格低于买入阈值且满足其他风险控制条件，则执行买入操作
9. **卖出操作**：检查当前持仓情况，如果价格高于卖出阈值，则卖出
10. **交易标记**：所有交易都会被标记为 `sdk:weather`，以便后续跟踪

## 智能持仓调整

通过 `--smart-sizing` 参数，持仓规模会根据以下规则计算：
- 可用 USDC 余额的 5%（可通过 `SIMMER_WEATHER_SIZING_PCT` 参数调整）
- 最大持仓金额上限为 2.00 美元（默认值）
- 如果账户余额不足，持仓规模会回退到固定值

这种方式可以防止过度交易，并根据账户规模动态调整持仓规模。

## 风险控制机制

在交易前，该策略会检查以下风险因素：
- **市场反转风险**：如果价格波动过于频繁，将跳过当前交易
- **滑点风险**：如果预计滑点超过 15%，将跳过当前交易
- **市场快速波动风险**：如果市场在 2 小时内价格波动较大，将跳过交易
- **市场状态风险**：如果市场已经恢复正常，将跳过交易

可以通过 `--no-safeguards` 参数禁用这些风险控制机制（但不建议这样做）。

## 交易标记

所有交易都会被标记为 `source: "sdk:weather"`，以便于：
- 在账户报告中按策略分类显示交易情况
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

## 故障排除

- **“风险控制提示：严重市场反转风险”**：表示该市场的价格波动过于频繁，请等待一段时间后再进行交易
- **“滑点过高”**：市场流动性较低，建议减少持仓规模或跳过交易
- **“市场在 X 小时内将恢复正常”**：市场即将恢复正常，但风险较高，请谨慎操作
- **“未找到天气交易市场”**：可能是因为当前季节该市场不活跃
- **“外部钱包需要预先签署的交易订单”**：环境变量 `WALLET_PRIVATE_KEY` 未设置
  - SDK 会在该变量存在时自动签署交易订单，无需手动操作
  - 解决方法：设置 `export WALLET_PRIVATE_KEY=0x<your-polymarket-wallet-private-key>`
  - 请勿尝试手动签署订单或修改策略代码，SDK 会自动处理
- **“账户余额显示为 0 美元，但实际上我有 USDC”**：Polymarket 使用的是 **USDC.e**（桥接后的 USDC，合约地址为 `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`），而非原生 USDC
  - 如果您最近将 USDC 桥接到了 Polygon，可能需要先将 USDC.e 转换为原生 USDC 后再尝试交易
- **“API 密钥无效”**：请从 simmer.markets/dashboard 的 SDK 标签页获取新的 API 密钥