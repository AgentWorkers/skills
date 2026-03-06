---
name: polymarket-elon-tweets
description: '使用 XTracker 的帖子数量数据来交易 Polymarket 上的 “Elon Musk #tweets” 相关市场。当组合成本低于 1 美元时，购买相邻的价格区间桶（range buckets），以获得结构性优势。适用于用户希望交易与 Elon Musk 推文数量相关的市场、自动化进行与 Elon Musk 推文相关的投注、查看 XTracker 的统计数据，或执行类似 noovd 的交易策略的情况。'
metadata:
  author: Simmer (@simmer_markets)
  version: "1.1.0"
  displayName: Polymarket Elon Tweet Trader
  difficulty: advanced
  attribution: Strategy inspired by @noovd
---# Polymarket：基于Elon Musk推文数量的交易策略

使用XTracker提供的推文数量数据，在Polymarket平台上进行交易。

## 适用场景

当用户希望执行以下操作时，可以使用此策略：
- 自动交易与Elon Musk推文数量相关的市场；
- 设置类似@noovd风格的批量交易规则；
- 查看XTracker提供的当前推文事件的相关数据和统计信息；
- 监控并平仓现有的推文交易头寸；
- 配置批量交易的买卖价差或入场阈值。

## 策略原理

Polymarket每周会发布一次关于“Elon Musk将发布多少条推文？”的预测活动，预测结果分为多个区间（例如：200-219条、220-239条、240-259条）。其中只有某个区间被预测为“正确”，对应的奖励为1美元。该策略的具体步骤如下：
1. **获取XTracker的推文数量预测数据**：XTracker会实时跟踪Elon Musk的推文数量并预测最终的总数；
2. **确定目标区间**：找到与XTracker预测结果相匹配的区间；
3. **买入相邻区间**：买入目标区间以及其两侧的区间（买卖价差可配置）；
4. **检查总成本**：只有当所有相关区间的价格总和低于1美元（即“正收益”阈值）时，才会执行买入操作；
5. **奖励发放**：当预测结果被确认为正确时，系统会自动从用户的账户中扣除1美元，以覆盖交易成本。

## 设置流程

当用户请求安装或配置此策略时，需要完成以下步骤：
1. **安装Simmer SDK**：  
   ```bash
   pip install simmer-sdk
   ```

2. **获取Simmer API密钥**：  
   用户可以从simmer.markets/dashboard的SDK标签页获取API密钥，并将其存储在环境变量`SIMMER_API_KEY`中。
3. **提供钱包私钥**：  
   这是用于在Polymarket平台上进行交易的私钥（用于存储USDC代币的钱包）。请将私钥存储在环境变量`WALLET_PRIVATE_KEY`中。SDK会使用该密钥在客户端自动完成订单签名，无需用户手动操作。
4. **配置交易参数**：  
   - **最大交易成本**：所有相关区间的价格总和阈值（默认为0.90美元）；
   - **每次交易的最大金额**：每个区间的最大买入金额（默认为5.00美元）；
   - **买卖价差**：买入的相邻区间数量（默认为1个，即目标区间两侧各1个区间）；
   - **平仓阈值**：当某个区间的价格超过此阈值时卖出；
5. **保存配置**：将所有参数保存到`config.json`文件或环境变量中。
6. **设置定时任务**：（默认情况下，此策略不会自动执行交易——用户需要手动启用定时任务。）

## 配置选项

| 配置项 | 环境变量 | 配置键 | 默认值 | 说明 |
|---------|-------------|------------|---------|-------------|
| 最大交易成本 | `SIMMER_ELON_MAX_BUCKET_SUM` | `max_bucket_sum` | 0.90 | 只有当所有相关区间的价格总和低于此值时才进行交易 |
| 每次交易的最大金额 | `SIMMER_ELON_MAX_POSITION` | `max_position_usd` | 5.00 | 每个区间的最大买入金额 |
| 买卖价差 | `SIMMER_ELON_BUCKET_SPREAD` | `bucket_spread` | 1 | 每侧买入的区间数量（默认为1个，即目标区间两侧各1个区间） |
| 智能调整比例 | `SIMMER_ELON_SIZING_PCT` | `sizing pct` | 每笔交易的资金占比（默认为0.05%） |
| 每次扫描的最大交易次数 | `SIMMER_ELON_MAX_TRADES` | `max_trades_per_run` | 每次扫描周期内的最大交易次数（默认为6次） |
| 平仓阈值 | `SIMMER_ELON_EXIT` | `exit_threshold` | 0.65 | 当某个区间的价格超过此阈值时卖出 |
| 最大滑点限制 | `SIMMER_ELON_SLIPPAGE_MAX` | `slippage_max pct` | 如果滑点超过此值，则放弃交易 |
| 最小交易金额 | `SIMMER_ELON_MIN_POSITION` | `min_position_usd` | 智能调整的下限（默认为2.00美元） |
| 数据来源 | `SIMMER_ELON_DATA_SOURCE` | `data_source` | `xtracker` | 数据来源（XTracker） |

配置文件的优先级：`config.json` > 环境变量 > 默认值。

## 快速命令

```bash
# Check account balance and positions
python scripts/status.py

# Detailed position list
python scripts/status.py --positions
```

**API参考**：
- 基础URL：`https://api.simmer.markets`
- 认证方式：`Authorization: Bearer $SIMMER_API_KEY`
- 获取投资组合信息：`GET /api/sdk/portfolio`
- 查看交易头寸：`GET /api/sdk/positions`

## 运行策略

脚本的运行流程如下：
1. 每次运行时，脚本会：
   - 获取XTracker提供的Elon Musk推文事件的实时数据；
   - 获取当前的推文数量、预测的推文数量以及剩余的天数；
   - 在Simmer平台上查找与推文数量预测相匹配的交易市场（如果市场数据不存在，会自动导入）；
   - 找到与XTracker预测结果相匹配的交易区间；
   - 评估相邻区间的价格情况，并根据配置的买卖价差进行买入或卖出操作；
   - 在交易完成后，会检查当前的头寸情况，并在某个区间的价格超过平仓阈值时卖出；
   - 实施必要的安全检查（例如：避免频繁的买卖操作、控制滑点等）；
   - 所有交易都会被标记为`sdk:elon-tweets`，以便后续跟踪。

## 自动导入功能

如果Simmer平台上还没有与Elon Musk推文数量相关的交易市场，该策略会自动导入这些市场数据：
- 从XTracker的跟踪信息中提取Polymarket市场的URL；
- 使用SDK提供的导入接口（支持多结果事件）；
- 将所有相关区间的数据作为一个整体导入到Simmer平台；
- 无论实际区间数量多少，每天都视为一次导入操作。

## 智能调整交易金额

通过`--smart-sizing`参数，可以设置每次交易的金额：
- 交易金额默认为可用USDC余额的5%（可通过`sizing pct`参数进行配置）；
- 如果投资组合中的USDC余额不足，交易金额将自动调整为最大允许的金额（5.00美元）。

## 安全机制

在交易前，该策略会进行以下检查：
- **避免频繁的买卖操作**：如果用户在该市场的买卖方向频繁变动，系统会放弃交易；
- **控制滑点**：如果预计的滑点超过15%，系统会放弃交易；
- **市场状态检查**：如果市场已经关闭或交易结果已经确定，系统会避免交易；
- **价格异常检查**：如果某个区间的价格超过98%或低于2%，系统会避免交易。

可以通过`--no-safeguards`参数关闭这些安全机制（但不推荐这样做）。

**标记说明**

所有交易都会被标记为`source: "sdk:elon-tweets"`，这意味着：
- 投资组合报表会按策略进行分类显示；
- 其他策略不会误售用户在该市场中的交易头寸；
- 用户可以单独查看与Elon Musk推文交易相关的盈亏情况。

## 示例输出

```
🐦 Simmer Elon Tweet Trader
==================================================

⚙️ Configuration:
  Max bucket sum:  $0.90
  Max position:    $5.00
  Bucket spread:   1 (center ± 1 = 3 buckets)
  Exit threshold:  65%
  Data source:     xtracker

📊 XTracker Stats:
  Tracking: Elon Musk # tweets Feb 13 - Feb 20
  Current count: 187 posts
  Pace: 243 projected
  Days remaining: 2.3

🎯 Target cluster: 240-259 (center) + 220-239, 260-279
  240-259: $0.35
  220-239: $0.22
  260-279: $0.18
  Cluster sum: $0.75 (< $0.90 threshold) ✅

  Executing trades...
  ✅ Bought 14.3 shares of 240-259 @ $0.35
  ✅ Bought 22.7 shares of 220-239 @ $0.22
  ✅ Bought 27.8 shares of 260-279 @ $0.18

📊 Summary:
  Events scanned: 2
  Clusters evaluated: 2
  Trades executed: 3
  Exits: 0
```

## 常见问题及解决方法**

- **“未找到XTracker的跟踪数据”**：  
  可能是因为XTracker尚未更新Elon Musk的推文数据。新数据通常在每周三或周四发布。
- **“相关市场的总价格超过阈值”**：可能是因为某个区间的价格过高，导致利润空间过小。建议等待价格下降或调整买卖价差。
- **“未找到匹配的Simmer市场”**：可能是由于市场数据尚未导入。系统会在下一次运行时自动尝试导入。
- **“安全机制触发”**：可能是因为用户在该市场的买卖方向变化过于频繁。建议等待一段时间后再进行交易。
- **“外部钱包需要预先签名订单”**：确保环境变量`WALLET_PRIVATE_KEY`已设置正确。SDK会自动完成订单签名，无需用户手动操作。
- **“账户余额显示为0美元，但实际上有USDC”**：Polymarket使用的是`USDC.e`（一种桥接后的USDC代币，合约地址为`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`）。如果用户最近将USDC桥接到了Polygon平台，可能需要先将USDC转换为`USDC.e`后再进行交易。
- **“API密钥无效”**：请从simmer.markets/dashboard的SDK标签页获取新的API密钥。