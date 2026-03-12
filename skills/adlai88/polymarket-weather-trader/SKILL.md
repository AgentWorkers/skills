---
name: polymarket-weather-trader
description: 通过 Simmer API 利用 NOAA 的天气预报数据在 Polymarket 平台上进行交易。这一策略的灵感来源于 gopfan2 的策略（该策略已为投资者赚取了超过 200 万美元的收益）。适用于用户希望交易与温度相关的天气衍生品、自动化进行天气相关的投资决策、查看 NOAA 的天气预报数据，或执行类似 gopfan2 的交易策略的情况。
metadata:
  author: Simmer (@simmer_markets)
  version: "1.14.0"
  displayName: Polymarket Weather Trader
  difficulty: beginner
  attribution: Strategy inspired by gopfan2
---# Polymarket 天气交易策略

使用 NOAA 预报数据在 Polymarket 上交易温度相关市场。

> **这是一个模板。** 默认的信号源是 NOAA 的温度预报数据——您可以根据需要将其与其他天气 API、不同的预报模型或额外的市场类型（如降水量、风速等）结合使用。该策略负责处理所有交易相关的细节（包括市场筛选、数据解析、交易执行和风险控制）。

## 何时使用此策略

当用户希望执行以下操作时，可以使用此策略：
- 自动交易天气相关市场
- 设置类似 gopfan2 的温度交易规则
- 在天气预报价格较低时买入
- 查看自己的天气交易持仓
- 配置交易阈值或交易地点

## v1.14.0 的新功能

- **修复了环境变量名称**，以匹配自动调优系统的命名规范（旧名称仍可作为别名使用）：
  - `SIMMER_WEATHER_ENTRY` → `SIMMER_WEATHER_ENTRY_THRESHOLD`
  - `SIMMER_WEATHER_EXIT` → `SIMMER_WEATHER_EXIT_THRESHOLD`
  - `SIMMER_WEATHER_MAX_POSITION` → `SIMMER_WEATHER_MAX_POSITION_USD`
  - `SIMMER_WEATHER_MAX_TRADES` → `SIMMER_WEATHER_MAX_TRADES_PER_RUN`
- **新增可调参数：`SIMMER_WEATHER_SLIPPAGE_MAX`** — 可调整的交易滑点保护值（默认为 15%）；在流动性较低的市场中可设置更高值。
- **新增可调参数：`SIMMER_WEATHER_MIN_LIQUIDITY`** — 如果市场流动性低于此阈值，则跳过该市场（默认值为 0，表示禁用）。在执行交易前会先过滤掉流动性不足的市场。
- `SIMMER_WEATHER_LOCATIONS` 和 `SIMMER_WEATHER_binary_ONLY` 现在也被列为自动调优的可调参数。

### v1.13.0
- **仅限二元交易模式**：新增 `SIMMER_WEATHER_binary_ONLY` 配置选项，用于跳过区间型市场（例如 “NYC 34-35°F”），仅交易二元类型的天气市场（即 “是/否” 类型）。

### v1.2.0
- **每次扫描周期的最大交易数量**：新增 `SIMMER_WEATHER_MAX_TRADES` 配置选项，用于限制每次扫描周期内的最大交易数量（默认值为 5 笔）。

### v1.1.1
- **状态脚本**：新增 `scripts/status.py` 脚本，用于快速查看账户余额和持仓情况。
- **API 参考**：添加了包含 API 端点的快速命令部分。

### v1.1.0
- **交易标记**：所有交易都会被标记为 `sdk:weather`，以便于进行投资组合跟踪。
- **智能持仓规模调整**：根据可用余额自动调整持仓规模（通过 `--smart-sizing` 选项设置）。
- **风险控制机制**：检查市场价格波动情况、交易滑点以及价格趋势变化。
- **价格趋势检测**：检测近期价格下跌情况，以生成更强的交易信号。

## 设置流程

当用户请求安装或配置此策略时，请按照以下步骤操作：
1. **获取 Simmer API 密钥**：
   - 可从 simmer.markets/dashboard 的 SDK 标签页获取密钥。
   - 将密钥存储在环境变量 `SIMMER_API_KEY` 中。
2. **提供钱包私钥**（用于实时交易）：
   - 这是用户的 Polymarket 钱包私钥（用于存放 USDC 的钱包）。
   - 将私钥存储在环境变量 `WALLET_PRIVATE_KEY` 中。
   - SDK 会使用该密钥在客户端自动签署交易订单，无需手动操作。
3. **配置相关参数**（或确认默认值）：
   - **买入阈值**：价格低于此值时买入（默认值为 0.15 美分）。
   - **卖出阈值**：价格高于此值时卖出（默认值为 0.45 美分）。
   **最大持仓金额**：每次交易的最大金额（默认值为 2.00 美元）。
   **交易地点**：指定要进行交易的城市（默认值为 NYC）。
4. **将配置信息保存到环境变量中**。
5. **设置定时任务**（默认情况下禁用定时任务——用户需要自行启用）。

## 配置参数

| 参数 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| 买入阈值 | `SIMMER_WEATHER_ENTRY_THRESHOLD` | 0.15 | 价格低于此值时买入 |
| 卖出阈值 | `SIMMER_WEATHER_EXIT_THRESHOLD` | 0.45 | 价格高于此值时卖出 |
| 每次交易的最大金额 | `SIMMER_WEATHER_MAX_POSITION_USD` | 2.00 | 每次交易的最大金额（美元） |
| 每次扫描周期的最大交易数量 | `SIMMER_WEATHER_MAX_TRADES_PER_RUN` | 5 | 每次扫描周期内的最大交易数量 |
| 交易地点 | `SIMMER_WEATHER_LOCATIONS` | NYC | 用逗号分隔的城市列表（例如：NYC, Chicago, Seattle, Atlanta, Dallas, Miami） |
| 仅限二元交易 | `SIMMER_WEATHER_binary_ONLY` | false | 跳过区间型市场，仅交易二元类型的天气市场 |
| 智能持仓比例 | `SIMMER_WEATHER_SIZING_PCT` | 0.05 | 每笔交易的持仓金额占可用余额的百分比 |
| 最大滑点 | `SIMMER_WEATHER_SLIPPAGE_MAX` | 0.15 | 如果滑点超过此值，则跳过该交易（0.15 表示 15%） |
| 最低流动性阈值 | `SIMMER_WEATHER_MIN_LIQUIDITY` | 0 | 如果市场流动性低于此金额，则跳过该市场（0 表示禁用） |

**旧的环境变量别名**（仍可兼容旧版本）：`SIMMER_WEATHER_ENTRY`, `SIMMER_WEATHER_EXIT`, `SIMMER_WEATHER_MAX_POSITION`, `SIMMER_WEATHER_MAX_TRADES`

**支持的交易地点**：NYC, Chicago, Seattle, Atlanta, Dallas, Miami

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
1. 从 Simmer API 获取当前活跃的天气市场数据。
2. 按照事件类型对市场进行分类（每个温度数据对应一个事件）。
3. 解析事件名称以获取具体地点和日期。
4. 获取该地点/日期的 NOAA 预报数据。
5. 找到与预报数据匹配的温度区间。
6. **风险控制**：检查市场价格波动情况、滑点以及价格变化趋势。
7. **趋势检测**：检测近期价格下跌情况，以生成更强的买入信号。
8. **买入操作**：如果当前价格低于买入阈值且满足其他风险控制条件，则执行买入操作。
9. **卖出操作**：检查现有持仓情况，如果价格高于卖出阈值，则卖出。
10. **交易标记**：所有交易都会被标记为 `sdk:weather`，以便后续跟踪。

## 智能持仓调整

通过 `--smart-sizing` 选项，持仓规模会根据以下规则计算：
- 可用 USDC 余额的 5%（可通过 `SIMMER_WEATHER_SIZING_PCT` 配置）。
- 最大持仓金额上限为 2.00 美元。
- 如果账户余额不足，持仓规模会恢复到固定值。

这种机制可防止过度交易，并根据账户规模动态调整持仓规模。

## 风险控制措施

在交易前，策略会执行以下检查：
- **价格波动风险**：如果市场价格波动过于剧烈，则跳过当前交易。
- **滑点风险**：如果预计滑点超过 15%，则跳过交易。
- **市场状态**：如果市场在 2 小时内即将结束交易，则跳过当前交易。
- **市场状态**：如果市场已经结束交易，则跳过当前交易。

可以通过 `--no-safeguards` 选项禁用这些风险控制措施（但不建议这样做）。

## 交易标记

所有交易都会被标记为 `source: "sdk:weather"`，以便于进行投资组合管理和跟踪：
- 投资组合报告显示各策略的交易情况。
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

## 常见问题及解决方法

- **“风险控制提示：价格波动过于剧烈”**：表示该市场的价格波动较大，建议等待后再进行交易。
- **“滑点过高”**：市场流动性较低，建议减少持仓规模或跳过交易。
- **“市场将在 X 小时后结束交易”**：市场即将结束交易，风险增加，请谨慎操作。
- **“未找到天气相关市场”**：可能是由于季节性原因导致天气市场暂时不活跃。
- **“外部钱包需要预先签署的交易订单”**：确保环境变量 `WALLET_PRIVATE_KEY` 已设置正确。SDK 会在该变量存在时自动签署交易订单，无需手动操作。
- **“账户余额显示为 0 美元，但实际上我有 USDC”**：Polymarket 使用的是 **USDC.e**（一种桥接形式的 USDC，合约地址为 `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`），而非原生 USDC。如果最近将 USDC 桥接到了 Polygon 平台，请先将其转换为原生 USDC 后再尝试交易。
- **“API 密钥无效”**：请从 simmer.markets/dashboard 的 SDK 标签页获取新的 API 密钥。