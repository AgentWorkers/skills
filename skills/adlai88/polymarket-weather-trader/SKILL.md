---
name: polymarket-weather-trader
description: 通过 Simmer API 利用 NOAA 的天气预报数据在 Polymarket 平台上进行交易。这一策略的灵感来源于 gopfan2 的盈利策略（盈利金额超过 200 万美元）。适用于用户希望交易与温度相关的金融产品、自动化进行天气相关的投资决策、查看 NOAA 的天气预报数据，或执行类似 gopfan2 的交易策略的情况。
metadata:
  author: Simmer (@simmer_markets)
  version: "1.13.0"
  displayName: Polymarket Weather Trader
  difficulty: beginner
  attribution: Strategy inspired by gopfan2
---# Polymarket 天气交易策略

使用 NOAA 的天气预报数据，在 Polymarket 上进行温度市场的交易。

> **这是一个模板。** 默认的信号源是 NOAA 的温度预报数据——您可以根据需要将其与其他天气 API、不同的预报模型或额外的市场类型（如降水量、风速等）结合使用。该策略负责处理所有交易相关的细节（包括市场发现、数据解析、交易执行和风险控制）。用户需要提供自己的交易策略（即 “alpha” 参数）。

## 适用场景

当用户希望：
- 自动进行天气市场交易
- 设置类似 gopfan2 的温度交易规则
- 在天气预测较低时买入
- 查看自己的天气交易持仓
- 配置交易阈值或交易地点时，可以使用此策略。

## v1.11.0 的新功能

- **仅限二元交易模式**：新增了 `SIMMER_WEATHER_BINARY_ONLY` 配置选项，用于跳过温度范围（例如 “NYC 34-35°F”）（仅交易二元类型的 “是/否” 市场）。

### v1.2.0
- **每次扫描周期的最大交易数量**：新增了 `SIMMER_WEATHER_MAX_TRADES` 配置选项，用于限制每次扫描周期内的最大交易数量（默认值为 5 笔）。

### v1.1.1
- **状态检查脚本**：新增了 `scripts/status.py` 脚本，用于快速查看账户余额和持仓情况。
- **API 参考**：增加了快速命令部分，其中包含 API 的相关端点信息。

### v1.1.0
- **交易标记**：所有交易都会被标记为 `sdk:weather`，以便进行投资组合跟踪。
- **智能持仓调整**：根据可用余额自动调整持仓规模（通过 `--smart-sizing` 选项设置）。
- **风险控制机制**：检查市场价格波动、滑点以及价格趋势变化。
- **价格趋势检测**：检测最近的价格下跌情况，以生成更强的买入信号。

## 设置流程

当用户请求安装或配置此策略时，请按照以下步骤操作：

1. **获取 Simmer API 密钥**：
   - 用户可以从 simmer.markets/dashboard 的 SDK 标签页获取 API 密钥，并将其存储在环境变量 `SIMMER_API_KEY` 中。

2. **提供钱包私钥**（用于实时交易）：
   - 这是用户 Polymarket 钱包的私钥（用于存储 USDC）。请将其存储在环境变量 `WALLET_PRIVATE_KEY` 中。
   - SDK 会使用此私钥在客户端自动签署交易订单，无需手动操作。

3. **配置交易参数**（或确认默认值）：
   - **买入阈值**：价格低于该阈值时买入（默认为 0.15 美分）。
   - **卖出阈值**：价格高于该阈值时卖出（默认为 0.45 美分）。
   **每次交易的最大持仓金额**：每次交易的最大金额（默认为 2.00 美元）。
   **交易地点**：指定要进行交易的城市（默认为纽约市 NYC）。

4. **将配置参数保存到环境变量中**。

5. **设置定时任务**（默认情况下未启用定时执行，用户需要手动启用）。

## 配置选项

| 配置项 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| 买入阈值 | `SIMMER_WEATHER_ENTRY` | 0.15 | 价格低于此阈值时买入 |
| 卖出阈值 | `SIMMER_WEATHER_EXIT` | 0.45 | 价格高于此阈值时卖出 |
| 每次交易的最大持仓金额 | `SIMMER_WEATHER_MAX_POSITION` | 2.00 | 每次交易的最大金额（美元） |
| 每次扫描周期的最大交易数量 | `SIMMER_WEATHER_MAX_TRADES` | 5 | 每次扫描周期内的最大交易数量 |
| 仅限二元交易 | `SIMMER_WEATHER_BINARY_ONLY` | false | 跳过温度范围类型的交易（例如 “34-35°F”），仅交易二元类型的 “是/否” 市场 |
| 交易地点 | `SIMMER_WEATHER_LOCATIONS` | NYC | 用逗号分隔的城市列表 |
| 智能持仓调整比例 | `SIMMER_WEATHER_SIZING_PCT` | 0.05 | 每笔交易的持仓金额占可用余额的百分比 |

**支持的地点**：纽约市（NYC）、芝加哥（Chicago）、西雅图（Seattle）、亚特兰大（Atlanta）、达拉斯（Dallas）、迈阿密（Miami）。

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
- 查看投资组合：`GET /api/sdk/portfolio`
- 查看持仓情况：`GET /api/sdk/positions`

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
1. 每个周期从 Simmer API 获取当前活跃的天气市场数据。
2. 按照事件类型对市场进行分组（每个温度数据对应一个事件）。
3. 解析事件信息以获取具体地点和日期。
4. 获取该地点/日期的 NOAA 天气预报数据。
5. 找到与预报数据匹配的温度区间。
6. **风险控制**：检查是否存在价格波动、滑点等问题。
7. **价格趋势检测**：检测最近的价格下跌情况，以生成更强的买入信号。
8. **买入**：如果当前价格低于买入阈值且满足其他风险控制条件，则执行买入操作。
9. **卖出**：检查现有持仓情况，如果价格高于卖出阈值，则执行卖出操作。
10. **交易标记**：所有交易都会被标记为 `sdk:weather`，以便后续跟踪。

## 智能持仓调整

通过 `--smart-sizing` 选项，持仓金额会根据以下规则计算：
- 可用 USDC 余额的 5%（可通过 `SIMMER_WEATHER_SIZING_PCT` 配置调整）。
- 最大持仓金额上限为 2.00 美元。
- 如果投资组合余额不足，持仓金额会恢复到固定值。

这种机制有助于防止过度交易，并根据账户规模动态调整持仓规模。

## 风险控制措施

在交易前，策略会执行以下检查：
- **价格波动预警**：如果价格波动过于剧烈，将跳过当前交易机会。
- **滑点控制**：如果预计滑点超过 15%，将跳过交易。
- **市场状态检查**：如果市场在 2 小时内即将结束，将跳过交易。
- **市场状态确认**：如果市场已经结束，将跳过交易。

可以通过 `--no-safeguards` 选项关闭这些风险控制机制（但不推荐这样做）。

## 交易标记

所有交易都会被标记为 `source: "sdk:weather"`，以便进行以下操作：
- 投资组合报表会按策略类型显示交易明细。
- 复制交易策略不会影响用户的天气交易结果。
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

## 故障排除

- **“风险控制提示：价格波动过于剧烈”**：表示该市场的价格波动过于频繁，建议等待一段时间后再进行交易。
- **“滑点过高”**：市场流动性较低，建议减少持仓金额或跳过当前交易。
- **“市场将在 X 小时后结束”**：市场即将结束，交易风险增加，请谨慎操作。
- **“未找到天气市场”**：可能是因为当前季节该市场不活跃。
- **“外部钱包需要预签名订单”**：确保环境变量 `WALLET_PRIVATE_KEY` 已设置。SDK 会在该变量存在的情况下自动签署交易订单，无需手动操作。
- **提示：“余额显示为 0 美元，但实际上我有 USDC”**：Polymarket 使用的是桥接后的 USDC（合约地址为 `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`），而非原生 USDC。如果最近将 USDC 桥接到了 Polygon 平台，请先将其转换为原生 USDC 后再尝试交易。
- **“API 密钥无效”**：请从 simmer.markets/dashboard 的 SDK 标签页重新获取 API 密钥。