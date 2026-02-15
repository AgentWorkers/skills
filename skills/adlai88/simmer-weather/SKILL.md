---
name: simmer-weather
displayName: Polymarket Weather Trader
description: 通过 Simmer API 利用 NOAA 的天气预报在 Polymarket 平台上进行交易。这一策略的灵感来源于 gopfan2 的盈利策略（盈利金额超过 200 万美元）。适用于用户想要交易与温度相关的市场、自动化进行天气相关的投注、查看 NOAA 的天气预报，或执行类似 gopfan2 的交易策略的情况。
metadata: {"clawdbot":{"emoji":"🌡️","requires":{"env":["SIMMER_API_KEY"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
attribution: "Strategy inspired by gopfan2"
version: "1.6.0"
---

# Polymarket 天气交易策略

使用 NOAA 预报数据在 Polymarket 上进行温度市场交易。

## 适用场景

当用户希望执行以下操作时，可以使用此策略：
- 自动进行天气市场交易
- 设置类似 gopfan2 的温度交易规则
- 在天气预测价格较低时买入
- 检查自己的天气交易头寸
- 配置交易阈值或交易地点

## v1.2.0 的新功能

- **单次扫描周期的最大交易数量**：新增了 `SIMMER_WEATHER_MAX_TRADES` 配置参数，用于限制每次扫描周期内的交易次数（默认值为 5 次）

### v1.1.1
- **状态检查脚本**：新增了 `scripts/status.py` 脚本，用于快速查看账户余额和交易头寸
- **API 参考**：增加了包含 API 端点的快速命令部分

### v1.1.0
- **交易标记**：所有交易都被标记为 `sdk:weather`，以便进行投资组合跟踪
- **智能资金分配**：根据可用余额自动调整交易头寸大小（使用 `--smart-sizing` 参数）
- **风险防护机制**：检查市场反转、滑点及价格波动等风险
- **价格趋势检测**：识别近期价格下跌情况，以获取更强的买入信号

## 设置流程

当用户请求安装或配置此策略时，请按照以下步骤操作：
1. **获取 Simmer API 密钥**：
   - 可在 simmer.markets/dashboard 的 SDK 标签页获取该密钥
   - 将密钥存储在环境变量 `SIMMER_API_KEY` 中
2. **确认设置**（或使用默认值）：
   - **买入阈值**：价格低于此值时买入（默认为 0.15 美分）
   - **卖出阈值**：价格高于此值时卖出（默认为 0.45 美分）
   - **单次交易最大金额**：每次交易的最大金额（默认为 2.00 美元）
   **交易地点**：指定进行交易的城市（默认为纽约市）
3. **将设置保存到环境变量中**
4. **配置定时任务**（默认关闭——用户需要手动启用）

## 配置参数

| 参数 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| 买入阈值 | `SIMMER_WEATHER_ENTRY` | 0.15 | 价格低于此值时买入 |
| 卖出阈值 | `SIMMER_WEATHER_EXIT` | 0.45 | 价格高于此值时卖出 |
| 单次交易最大金额 | `SIMMER_WEATHER_MAX_POSITION` | 2.00 | 每次交易的最大金额（美元） |
| 单次扫描周期的最大交易次数 | `SIMMER_WEATHER_MAX_TRADES` | 5 | 每次扫描周期内的最大交易次数 |
| 交易地点 | `SIMMER_WEATHER_LOCATIONS` | NYC | 用逗号分隔的城市列表 |
| 智能资金分配比例 | `SIMMER_WEATHER_SIZING_PCT` | 0.05 | 每笔交易的资金分配比例（占余额的百分比） |

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
- 交易头寸信息：`GET /api/sdk/positions`

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
```

## 工作原理

脚本的工作流程如下：
1. 每个周期从 Simmer API 获取活跃的天气市场数据
2. 按事件类型对市场进行分类（每个温度数据对应一个事件）
3. 解析事件名称以获取具体地点和日期
4. 获取该地点/日期的 NOAA 预报数据
5. 找到与预报数据匹配的温度区间
6. **风险防护机制**：检查市场反转、滑点及价格波动等风险
7. **价格趋势检测**：识别近期价格下跌情况，以获取更强的买入信号
8. **买入操作**：如果当前价格低于买入阈值且满足其他风险防护条件，则买入
9. **卖出操作**：检查现有头寸，如果价格高于卖出阈值则卖出
10. **交易标记**：所有交易都会被标记为 `sdk:weather`，以便后续跟踪

## 智能资金分配

使用 `--smart-sizing` 参数时，交易头寸大小会根据以下规则计算：
- 可用 USDC 余额的 5%（可通过 `SIMMER_WEATHER_SIZING_PCT` 参数调整）
- 最大交易金额不超过预设的最大值（默认为 2.00 美元）
- 如果投资组合中缺乏足够的资金，将使用固定头寸大小

**注意事项**：
- 此机制可防止过度交易，并根据账户规模动态调整头寸大小。

## 风险防护机制

在交易前，脚本会检查以下风险：
- **市场反转**：如果价格波动过于频繁，则跳过当前交易
- **滑点**：如果预计滑点超过 15%，则跳过交易
- **价格波动**：如果市场在 2 小时内即将恢复稳定，则跳过交易
- **市场状态**：如果市场已经趋于稳定，则跳过交易

**警告提示**：
- “严重市场反转警告”：表示价格波动过于剧烈，建议等待后再交易
- “滑点过高”：市场流动性较差，建议减小头寸或跳过交易
- “市场即将恢复稳定”：市场可能在短时间内恢复稳定，风险增加
- “未找到天气市场”：当前可能没有活跃的天气交易市场（受季节性影响）

**禁用风险防护机制**：可以使用 `--no-safeguard` 参数（不推荐）

**标记说明**：
- 所有交易都会被标记为 `source: "sdk:weather"`，便于投资组合管理和分析
- 这意味着投资组合会按策略进行分类显示
- 复制交易策略不会影响你的天气交易头寸
- 可以单独跟踪天气交易的盈亏情况

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

## 常见问题及解决方法**

- **“风险防护机制触发：严重市场反转警告”**：表示价格波动过于剧烈，建议等待后再交易
- **“滑点过高”**：市场流动性较差，建议减小头寸或跳过交易
- **“市场即将恢复稳定”**：市场可能在短时间内恢复稳定，风险增加
- **“未找到天气市场”**：当前可能没有活跃的天气交易市场（受季节性影响）
- **“API 密钥无效”**：请从 simmer.markets/dashboard 的 SDK 标签页重新获取 API 密钥