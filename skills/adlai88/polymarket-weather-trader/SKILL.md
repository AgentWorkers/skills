---
name: polymarket-weather-trader
displayName: Polymarket Weather Trader
description: 通过 Simmer API 利用 NOAA 的天气预报数据在 Polymarket 平台上进行交易。这一策略的灵感来源于 gopfan2 的策略（该策略曾获得超过 200 万美元的收益）。适用于用户希望交易与温度相关的天气衍生品、自动化执行天气相关的交易决策、查看 NOAA 的天气预报数据，或采用 gopfan2 的交易方式的情况。
metadata: {"clawdbot":{"emoji":"🌡️","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false,"automaton":{"managed":true,"entrypoint":"weather_trader.py"},"tunables":[{"env":"SIMMER_WEATHER_ENTRY_THRESHOLD","type":"number","default":0.05,"range":[0.01,0.30],"step":0.01,"label":"Entry edge threshold"},{"env":"SIMMER_WEATHER_EXIT_THRESHOLD","type":"number","default":0.85,"range":[0.5,0.99],"step":0.01,"label":"Exit probability threshold"},{"env":"SIMMER_WEATHER_MAX_POSITION_USD","type":"number","default":50,"range":[1,200],"step":5,"label":"Max position size"},{"env":"SIMMER_WEATHER_SIZING_PCT","type":"number","default":0.10,"range":[0.01,1.0],"step":0.01,"label":"Position sizing percentage"},{"env":"SIMMER_WEATHER_MAX_TRADES_PER_RUN","type":"number","default":5,"range":[1,20],"step":1,"label":"Max trades per run"}]}}
authors:
  - Simmer (@simmer_markets)
attribution: "Strategy inspired by gopfan2"
version: "1.12.0"
difficulty: beginner
published: true
---
# Polymarket 天气交易策略

使用 NOAA 的天气预报数据，在 Polymarket 上进行温度市场的交易。

> **这是一个模板。** 默认的信号来源是 NOAA 的温度预报数据——您可以将其与其他天气 API、不同的预报模型或额外的市场类型（如降水量、风速等）结合使用。该策略负责处理所有的交易逻辑（包括市场发现、数据解析、交易执行以及风险控制）。您需要提供相应的代理（agent）来实现策略的自动化执行。

## 何时使用此策略

当用户希望执行以下操作时，可以使用此策略：
- 自动交易天气相关市场
- 设置类似 gopfan2 的温度交易规则
- 在天气预测较低时买入
- 查看自己的天气交易头寸
- 配置交易阈值或交易地点

## v1.11.0 的新功能

- **仅限二元交易模式**：新增了 `SIMMER_WEATHER_BINARY_ONLY` 配置选项，用于跳过温度范围（例如 “NYC 34-35°F”）相关的交易，仅交易二元类型的天气市场（即 “是/否” 类型）。

### v1.2.0
- **每次扫描周期的最大交易数量**：新增了 `SIMMER_WEATHER_MAX_TRADES` 配置选项，用于限制每次扫描周期内的最大交易数量（默认值为 5 笔）。

### v1.1.1
- **状态检查脚本**：新增了 `scripts/status.py` 脚本，用于快速查看账户余额和交易头寸。
- **API 参考**：增加了 “快速命令” 部分，其中包含相关的 API 端点信息。

### v1.1.0
- **交易标记**：所有交易都会被标记为 `sdk:weather`，以便于进行投资组合管理。
- **智能调整交易规模**：根据可用余额自动调整交易规模（通过 `--smart-sizing` 参数控制）。
- **风险控制机制**：检查市场价格波动、滑点以及价格衰减情况。
- **价格趋势检测**：检测最近的价格下跌趋势，以获取更强的买入信号。

## 设置流程

当用户请求安装或配置此策略时，请按照以下步骤操作：
1. **获取 Simmer API 密钥**：
   - 用户可以从 simmer.markets/dashboard 的 SDK 标签页获取 API 密钥，并将其存储在环境变量 `SIMMER_API_KEY` 中。
2. **提供钱包私钥**（用于实时交易）：
   - 这是用户的 Polymarket 钱包私钥（用于存储 USDC 的钱包）。请将其存储在环境变量 `WALLET_PRIVATE_KEY` 中。
   - SDK 会使用此私钥在客户端自动签署交易订单，无需手动操作。
3. **配置交易参数**（或确认默认值）：
   - **买入阈值**：价格低于该阈值时买入（默认值为 0.15 美分）。
   - **卖出阈值**：价格高于该阈值时卖出（默认值为 0.45 美分）。
   - **每次交易的最大金额**：每次交易的最大金额（默认值为 2.00 美元）。
   **交易地点**：指定进行交易的城市（默认为纽约市 NYC）。
4. **将配置保存到环境变量中**。
5. **设置定时任务**（默认情况下未启用定时执行，用户需要手动启用）。

## 配置选项

| 配置项 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| 买入阈值 | `SIMMER_WEATHER_ENTRY` | 0.15 | 价格低于此阈值时买入 |
| 卖出阈值 | `SIMMER_WEATHER_EXIT` | 0.45 | 价格高于此阈值时卖出 |
| 每次交易的最大金额 | `SIMMER_WEATHER_MAX_POSITION` | 2.00 | 每次交易的最大金额（美元） |
| 每次扫描周期的最大交易数量 | `SIMMER_WEATHER_MAX_TRADES` | 5 | 每次扫描周期内的最大交易数量 |
| 仅限二元交易 | `SIMMER_WEATHER_BINARY_ONLY` | false | 跳过温度范围相关的交易，仅交易二元类型的天气市场 |
| 交易地点 | `SIMMER_WEATHER_LOCATIONS` | NYC | 用逗号分隔的城市列表 |
| 智能调整比例 | `SIMMER_WEATHER_SIZING_PCT` | 0.05 | 每笔交易的交易金额占可用余额的百分比 |

**支持的交易地点**：纽约市（NYC）、芝加哥（Chicago）、西雅图（Seattle）、亚特兰大（Atlanta）、达拉斯（Dallas）、迈阿密（Miami）。

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
- 获取投资组合信息：`GET /api/sdk/portfolio`
- 查看交易头寸：`GET /api/sdk/positions`

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
1. 从 Simmer API 获取当前活跃的天气市场数据。
2. 按照天气事件对市场进行分类（每个温度数据对应一个事件）。
3. 解析事件信息以获取具体地点和日期。
4. 获取该地点/日期的 NOAA 天气预报数据。
5. 找到与预报数据匹配的温度区间。
6. **风险控制**：检查是否存在价格波动、滑点等风险因素。
7. **价格趋势检测**：检测最近的价格下跌趋势，以获取更强的买入信号。
8. **买入决策**：如果当前价格低于买入阈值且满足其他风险控制条件，则执行买入操作。
9. **卖出决策**：检查现有头寸情况，如果价格高于卖出阈值，则执行卖出操作。
10. **交易标记**：所有交易都会被标记为 `sdk:weather`，以便于后续跟踪。

## 智能调整交易规模

通过 `--smart-sizing` 参数，交易规模会根据可用余额的 0.05% 自动计算（可配置）。该比例上限为每次交易的最大金额（默认为 2.00 美元）。如果可用余额不足，系统会回退到固定的交易规模。

## 风险控制机制

在交易前，该策略会执行以下检查：
- **价格波动风险**：如果市场价格波动过于频繁，将避免交易。
- **滑点风险**：如果预计滑点超过 15%，将避免交易。
- **市场状态风险**：如果市场在 2 小时内即将结束，将避免交易。
- **市场状态确认**：如果市场已经结束，将避免交易。

可以通过 `--no-safeguards` 参数关闭这些风险控制机制（但不建议这样做）。

## 交易标记

所有交易都会被标记为 `source: "sdk:weather"”，以便于投资组合管理和分析。这意味着：
- 投资组合报告显示各策略的交易情况。
- 复制交易策略不会影响您的天气交易结果。
- 您可以单独查看天气交易的盈亏情况。

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

- **“风险控制提示：价格波动过于频繁”**：表示该市场的价格波动较大，建议等待一段时间后再进行交易。
- **“滑点过高”**：市场流动性较低，建议减小交易规模或暂时避免交易。
- **“市场即将结束（X 小时后）”**：市场即将结束，交易风险增加，请谨慎操作。
- **“未找到天气市场”**：可能是因为当前季节该市场不活跃。
- **“外部钱包需要预先签署的订单”**：确保环境变量 `WALLET_PRIVATE_KEY` 已设置。SDK 会自动使用该密钥签署交易订单，无需手动操作。
- **提示：“余额显示为 0 美元，但实际上我有 USDC”**：Polymarket 使用的是桥接后的 USDC（合约地址为 `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`），而非原生 USDC。如果您最近将 USDC 桥接到了 Polygon 平台，请先转换回原生 USDC 再进行交易。
- **“API 密钥无效”**：请从 simmer.markets/dashboard 的 SDK 标签页重新获取 API 密钥。