---
name: polymarket-elon-tweets
description: '使用 XTracker 的帖子计数数据来交易 Polymarket 上的 “Elon Musk #tweets” 相关市场。当组合成本低于 1 美元时，购买相邻的价格区间桶（range buckets），以获得结构性优势。适用于希望交易与 Elon Musk 推文数量相关的市场、自动化进行 Elon Musk 推文相关的交易策略、查看 XTracker 的统计数据，或执行类似 noovd 的交易策略的用户。'
metadata:
  author: Simmer (@simmer_markets)
  version: "1.0.4"
  displayName: Polymarket Elon Tweet Trader
  difficulty: advanced
  attribution: Strategy inspired by @noovd
---# Polymarket：基于Elon Musk推文数量的交易策略

使用XTracker提供的推文数量数据，在Polymarket平台上进行交易。

## 适用场景

当用户希望执行以下操作时，可以使用此策略：
- 自动交易与Elon Musk推文数量相关的市场；
- 设置类似@noovd风格的批量交易规则；
- 查看XTracker提供的推文事件相关的数据和统计信息；
- 监控并退出现有的推文交易头寸；
- 配置交易策略中的价格区间和入场阈值。

## 策略原理

Polymarket每周会发布一次“Elon Musk将会发布多少条推文？”的预测活动，预测结果分为多个价格区间（例如：200-219条、220-239条、240-259条）。其中只有一个区间的预测结果为“YES”，对应的奖励为1美元。该策略的具体步骤如下：
1. **获取XTracker的推文预测数据**：XTracker会实时跟踪Elon Musk的推文数量，并预测最终的总推文数；
2. **确定目标价格区间**：找到与XTracker预测结果相匹配的价格区间；
3. **买入相邻的价格区间**：买入目标价格区间及其两侧的价格区间（区间数量可配置）；
4. **判断买入条件**：只有当所有价格区间之和低于1美元（即盈利阈值）时，才进行买入；
5. **收益结算**：当预测结果确定后，系统会自动结算其中一个价格区间的收益，从而覆盖所有买入成本。

## 设置流程

当用户请求安装或配置此策略时，需要完成以下步骤：
1. **安装Simmer SDK**：  
   ```bash
   pip install simmer-sdk
   ```

2. **获取Simmer API密钥**：  
   用户可以从simmer.markets/dashboard的SDK标签页获取API密钥，并将其存储在环境变量`SIMMER_API_KEY`中。
3. **提供钱包私钥**：  
   这是用于在Polymarket平台上进行交易的私钥（用于存储USDC代币的钱包）。请将私钥存储在环境变量`WALLET_PRIVATE_KEY`中。SDK会使用该密钥在客户端自动签署交易订单，无需用户手动操作。
4. **配置策略参数**：  
   - **最大交易金额**：所有价格区间价格之和的阈值（默认为0.90美元）；
   - **每次交易的最大金额**：每个价格区间的最大买入金额（默认为5.00美元）；
   - **价格区间范围**：买入的相邻价格区间数量（默认为1个，即目标价格区间及其两侧的2个价格区间）；
   - **退出条件**：当某个价格区间价格超过此阈值时，系统会卖出该区间；
5. **保存配置信息**：将所有配置参数保存到`config.json`文件或环境变量中。
6. **设置定时任务**：（默认情况下，此策略不会自动执行交易——用户需要手动启用定时任务。）

## 配置选项

| 配置项          | 环境变量            | 配置键            | 默认值            | 说明                          |
|-----------------|------------------|------------------|------------------|--------------------------------------------|
| 最大交易金额        | `SIMMER_ELON_MAX_BUCKET_SUM`    | `max_bucket_sum`       | 0.90            | 只有当所有价格区间价格之和低于此值时才买入                |
| 每次交易的最大金额    | `SIMMER_ELON_MAX_POSITION`    | `max_position_usd`     | 5.00            | 每个价格区间的最大买入金额                    |
| 价格区间范围      | `SIMMER_ELON_BUCKET_SPREAD`    | `bucket_spread`       | 1               | 买入的相邻价格区间数量（默认为2个）                |
| 智能调整比例      | `SIMMER_ELON_SIZING_PCT`    | `sizing pct`        | 0.05            | 每笔交易的资金占比（百分比）                   |
| 每次扫描的最大交易次数   | `SIMMER_ELON_MAX_TRADES`    | `max_trades_per_run`     | 6               | 每次扫描的最大交易次数                     |
| 退出条件        | `SIMMER_ELON_EXIT`        | `exit_threshold`     | 0.65            | 当价格区间价格超过此阈值时卖出                   |
| 最大滑点          | `SIMMER_ELON_SLIPPAGE_MAX`    | `slippage_max pct`     | 0.05            | 如果滑点超过此值，则放弃交易                   |
| 最小交易金额      | `SIMMER_ELON_MIN_POSITION`    | `min_position_usd`     | 2.00            | 智能调整的下限金额（美元）                    |
| 数据来源        | `SIMMER_ELON_DATA_SOURCE`    | `data_source`       | `xtracker`        | 数据来源（XTracker）                     |

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

## 策略执行流程

脚本的执行流程如下：
1. 每次运行时，从XTracker获取Elon Musk推文事件的实时数据；
2. 获取当前的推文数量、预测的推文数量以及剩余的预测天数；
3. 在Simmer平台上查找与推文数量相关的交易市场（如果市场数据不存在，系统会自动导入）；
4. 找到与XTracker预测结果相匹配的价格区间；
5. 评估所有相邻的价格区间，并根据配置的策略进行买入或卖出操作；
6. 在交易完成后，系统会检查当前的头寸情况，并在必要时卖出；
7. 系统会进行一些安全检查，例如判断是否存在价格波动风险或滑点风险；
8. 所有交易都会被标记为`sdk:elon-tweets`，以便后续跟踪。

## 自动导入功能

如果Simmer平台上尚不存在与Elon Musk推文数量相关的交易市场，该策略会自动导入这些市场数据：
- 从XTracker的跟踪信息中提取Polymarket市场的URL；
- 使用SDK提供的导入接口（支持多结果事件）；
- 将所有相关价格区间作为一个整体导入到Simmer平台；
- 无论实际价格区间数量多少，每天仅计算为1次导入。

## 智能调整机制

通过`--smart-sizing`参数，系统会自动计算每次交易的最大金额：
- 计算方法为可用USDC余额的5%（可通过`sizing pct`参数进行调整）；
- 如果投资组合中的USDC余额不足，系统会使用默认的最大交易金额（5.00美元）。

## 安全保护机制

在交易前，系统会进行以下检查：
- **价格波动风险**：如果市场趋势波动过于剧烈，系统会放弃交易；
- **滑点风险**：如果预计的滑点超过15%，系统会放弃交易；
- **市场状态**：如果市场已经关闭或预测结果已经确定，系统会放弃交易；
- **极端价格**：如果某个价格区间的价格超过98%或低于2%，系统会放弃交易。

可以通过`--no-safeguards`参数关闭这些安全保护机制（但不推荐这样做）。

## 数据标记

所有交易都会被标记为`source: "sdk:elon-tweets"`，这样：
- 投资组合界面会按策略类型显示交易结果；
- 其他策略不会误售用户的推文交易头寸；
- 用户可以单独查看推文交易的盈亏情况。

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

## 常见问题及解决方法

**“未找到XTracker的跟踪数据”**：
- 可能是因为XTracker尚未更新Elon Musk的推文数据；
- 新的推文数据通常在每周三或周四更新。

**“价格区间总和超过阈值”**：
- 可能是因为价格区间过于狭窄，导致盈利空间太小；
- 可以等待价格下降或调整`bucket_spread`参数。

**“未找到匹配的Simmer市场”**：
- 可能是因为市场数据尚未导入到Simmer平台；
- 系统会在下一次运行时自动尝试导入数据；
- 请确认您的API密钥是否具有足够的导入权限（免费用户每天可导入10次，高级用户每天可导入50次）。

**“安全保护机制触发”**：
- 可能是因为该市场的价格波动过于剧烈；
- 在再次交易前，请等待价格稳定。

**“外部钱包需要预先签署的交易订单”**：
- 确保环境变量`WALLET_PRIVATE_KEY`已设置正确；
- SDK会在检测到该变量时自动签署交易订单，无需用户手动操作；
- 如果需要修改设置，请执行`export WALLET_PRIVATE_KEY=0x<your-polymarket-wallet-private-key>`；
- 请勿尝试手动签署订单或修改策略代码，因为SDK会自动处理交易。

**“余额显示为0美元，但我有USDC在Polygon上”**：
- Polymarket使用的是`USDC.e`（一种桥接后的USDC代币，合约地址为`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`）；
- 如果您最近将USDC桥接到了Polygon平台，可能需要先将USDC转换为`USDC.e`后再进行交易；
- 如果问题仍然存在，请尝试将`USDC.e`转换回原生USDC后再尝试交易。

**“API密钥无效”**：
- 请从simmer.markets/dashboard的SDK标签页获取新的API密钥。