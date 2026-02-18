---
name: polymarket-weather-trader
displayName: Polymarket Weather Trader
description: 通过 Simmer API 利用 NOAA 的天气预报数据在 Polymarket 平台上进行交易。该策略的灵感来源于 gopfan2 的策略（该策略已实现超过 200 万美元的收益）。适用于用户希望交易与温度相关的金融产品、自动执行天气相关的交易决策、查看 NOAA 的天气预报数据，或采用 gopfan2 的交易风格进行操作的情况。
metadata: {"clawdbot":{"emoji":"🌡️","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
attribution: "Strategy inspired by gopfan2"
version: "1.7.6"
published: true
---
# Polymarket 天气交易技能

使用 NOAA 预报数据在 Polymarket 上交易温度相关市场。

> **这是一个模板。** 默认的信号源是 NOAA 的温度预报数据——您可以将其与其他天气 API、不同的预报模型或额外的市场类型（如降水、风速等）结合使用。该技能负责处理所有相关流程（市场发现、数据解析、交易执行及风险控制）。您需要提供交易策略的具体实现（即 “alpha” 部分）。

## 何时使用此技能

当用户希望执行以下操作时，可以使用此技能：
- 自动交易与天气相关的市场
- 设置类似 gopfan2 的温度交易策略
- 在天气预测价格较低时买入
- 查看自己的天气交易头寸
- 配置交易阈值或交易地点

## v1.2.0 的新功能

- **每次扫描的最大交易数量**：新增配置参数 `SIMMER_WEATHER_MAX_TRADES` 以限制每次扫描周期内的交易次数（默认值为 5 笔）

### v1.1.1
- **状态检查脚本**：新增 `scripts/status.py` 脚本，用于快速检查账户余额和交易头寸
- **API 参考**：添加了包含 API 端点的快速命令部分

### v1.1.0
- **交易标记**：所有交易均被标记为 `sdk:weather`，以便进行投资组合跟踪
- **智能资金分配**：根据可用余额自动调整交易头寸大小（通过参数 `--smart-sizing` 控制）
- **风险控制机制**：检查市场反转、滑点及价格波动等风险
- **价格趋势检测**：检测近期价格下跌情况，以生成更强的买入信号

## 设置流程

当用户请求安装或配置此技能时，需要完成以下步骤：
1. **获取 Simmer API 密钥**：
   - 可从 simmer.markets/dashboard 的 SDK 标签页获取该密钥
   - 将其存储在环境变量 `SIMMER_API_KEY` 中

2. **提供钱包私钥**（用于实时交易）：
   - 这是用户的 Polymarket 钱包私钥（用于存储 USDC）
   - 将其存储在环境变量 `WALLET_PRIVATE_KEY` 中
   - SDK 会使用此密钥在客户端自动签名交易订单，无需手动操作

3. **配置交易参数**（或确认默认值）：
   - **入场阈值**：价格低于该阈值时买入（默认为 0.15 美分）
   - **出场阈值**：价格高于该阈值时卖出（默认为 0.45 美分）
   **每次交易的最大金额**：每次交易的最大金额（默认为 2.00 美元）
   **交易地点**：指定进行交易的城市（默认为纽约市）

4. **将配置保存到环境变量中**

5. **设置定时任务**（默认关闭——用户需要自行启用）

## 配置选项

| 配置项 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| 入场阈值 | `SIMMER_WEATHER_ENTRY` | 0.15 | 价格低于此阈值时买入 |
| 出场阈值 | `SIMMER_WEATHER_EXIT` | 0.45 | 价格高于此阈值时卖出 |
| 每次交易的最大金额 | `SIMMER_WEATHER_MAX_POSITION` | 2.00 | 每次交易的最大金额 |
| 每次扫描的最大交易次数 | `SIMMER_WEATHER_MAX_TRADES` | 5 | 每次扫描周期内的最大交易次数 |
| 交易地点 | `SIMMER_WEATHER_LOCATIONS` | NYC | 以逗号分隔的城市列表 |
| 智能资金分配比例 | `SIMMER_WEATHER_SIZING_PCT` | 0.05 | 每笔交易占可用余额的百分比 |

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

## 运行此技能

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

脚本的运行流程如下：
1. 从 Simmer API 获取当前活跃的天气市场数据
2. 按事件类型对市场进行分类（每个温度数据对应一个事件）
3. 解析事件信息以获取具体地点和日期
4. 获取该地点/日期的 NOAA 预报数据
5. 找到与预报数据匹配的温度区间
6. **风险控制**：检查市场是否存在反转、滑点等风险
7. **价格趋势检测**：检测近期价格走势，以生成更强的买入信号
8. **买入操作**：如果价格低于入场阈值且满足其他风险控制条件，则执行买入
9. **卖出操作**：检查当前持仓情况，如果价格高于出场阈值则卖出
10. **交易标记**：所有交易都会被标记为 `sdk:weather`，以便后续跟踪

## 智能资金分配

通过参数 `--smart-sizing`，交易头寸大小会按以下方式计算：
- 可用 USDC 余额的 5%（可通过 `SIMMER_WEATHER_SIZING_PCT` 配置）
- 最大交易金额上限为 2.00 美元
- 如果投资组合余额不足，将使用固定金额进行交易

**注意事项**：
- 此机制可防止过度交易，并根据账户规模动态调整交易规模。

## 风险控制措施

在交易前，脚本会检查以下风险：
- **市场反转**：如果价格波动过于剧烈，则跳过当前交易
- **滑点**：如果预计滑点超过 15%，则跳过交易
- **市场快速波动**：如果市场在 2 小时内恢复稳定，则跳过交易
- **市场已结束**：如果市场已结束交易，则跳过当前操作

**禁用风险控制**：可以使用参数 `--no-safeguards` 来禁用这些风险控制机制（不推荐）。

## 交易标记

所有交易都会被标记为 `source: "sdk:weather"`，以便进行以下操作：
- 投资组合报告显示按策略分类的交易情况
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

- **“风险控制提示：严重市场反转”**：表示该市场的价格波动过于剧烈，建议等待后再进行交易
- **“滑点过高”**：市场流动性较低，建议减小交易头寸或跳过交易
- **“市场将在 X 小时后恢复稳定”**：市场即将恢复稳定，但风险增加，请谨慎操作
- **“未找到天气交易市场”**：可能是因为当前季节该市场不活跃
- **“外部钱包需要预签名订单”**：确保环境变量 `WALLET_PRIVATE_KEY` 已设置正确
  - SDK 会自动使用该密钥签名交易订单，无需手动操作
  - 解决方法：`export WALLET_PRIVATE_KEY=0x<your-polymarket-wallet-private-key>`
  - 请勿尝试手动签名订单或修改脚本代码
- **“余额显示为 0 美元，但实际上我有 USDC”**：Polymarket 使用的是桥接后的 USDC（合约地址 `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`），而非原生 USDC
  - 如果您最近将 USDC 桥接到了 Polygon，可能需要将桥接后的 USDC 转换为原生 USDC 后再尝试交易
- **“API 密钥无效”**：请从 simmer.markets/dashboard 的 SDK 标签页重新获取 API 密钥