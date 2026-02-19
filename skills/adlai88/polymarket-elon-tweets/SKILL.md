---
name: polymarket-elon-tweets
displayName: Polymarket Elon Tweet Trader
description: '使用 XTracker 的推文数量数据来交易 Polymarket 平台上的“Elon Musk #推文”相关市场。当组合成本低于 1 美元时，购买相邻的价格区间交易对，以获得结构上的优势。该策略适用于用户希望交易与 Elon Musk 推文数量相关的市场、自动化进行 Elon Musk 推文相关的投资决策、查看 XTracker 的统计数据，或执行类似 noovd 的交易策略的情况。'
metadata: {"clawdbot":{"emoji":"🐦","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
attribution: "Strategy inspired by @noovd"
version: "1.0.4"
published: true
---
# Polymarket：基于Elon Musk推文数量的交易策略

使用XTracker提供的推文数量数据，在Polymarket平台上进行交易。

## 适用场景

当用户希望执行以下操作时，可以使用此策略：
- 自动交易与Elon Musk推文数量相关的市场；
- 设置类似@noovd风格的批量交易规则；
- 查看XTracker提供的推文事件进度和统计数据；
- 监控并平仓现有的推文交易头寸；
- 配置交易策略中的价格区间（即“桶”范围）。

## 策略原理

Polymarket每周会发布一次关于“Elon Musk将发布多少条推文？”的预测活动，这些活动会设定多个价格区间（例如：200-219条、220-239条、240-259条）。当预测结果为“240-259条”时，对应的交易区间收益为1美元。该策略的具体步骤如下：
1. **获取XTracker的推文数量预测数据**：XTracker会实时跟踪Elon Musk的推文数量并预测最终总数。
2. **确定目标价格区间**：找到与XTracker预测结果相匹配的价格区间。
3. **买入相邻的价格区间**：买入目标区间及其两侧的价格区间（区间宽度可配置）。
4. **检查总成本**：只有当所有价格区间之和低于1美元（即“正收益阈值”）时，才会执行买入操作。
5. **收益结算**：当预测结果确定后，系统会自动结算其中一个价格区间的收益，以覆盖所有交易成本。

## 设置流程

当用户请求安装或配置此策略时，需要完成以下步骤：
1. **安装Simmer SDK**：  
   ```bash
   pip install simmer-sdk
   ```

2. **获取Simmer API密钥**：  
   用户可以从simmer.markets/dashboard的SDK标签页获取API密钥，并将其存储在环境变量`SIMMER_API_KEY`中。
3. **提供钱包私钥**：  
   这是用户用于Polymarket平台的钱包私钥（用于存放USDC代币），需存储在环境变量`WALLET_PRIVATE_KEY`中。SDK会使用该密钥在客户端自动签署交易订单，无需用户手动操作。
4. **配置策略参数**：  
   - **最大交易成本**：所有价格区间之和的阈值（默认为0.90美元）。
   - **每次交易的最大金额**：每个价格区间的最大投资额（默认为5.00美元）。
   - **价格区间宽度**：买入的相邻价格区间数量（默认为1个，即目标区间两侧各1个区间）。
   - **平仓阈值**：当价格区间价格超过此阈值时卖出。
5. **将配置保存到config.json文件或环境变量中**。
6. **设置定时任务**：  
   （默认情况下，该策略不会自动执行交易——用户需要手动启用定时任务。）

## 配置参数

| 参数          | 环境变量            | 配置键            | 默认值            | 说明                          |
|----------------|------------------|------------------|------------------|--------------------------------------------|
| 最大交易成本     | `SIMMER_ELON_MAX_BUCKET_SUM`    | `max_bucket_sum`      | 0.90            | 只有当所有价格区间之和低于此值时才买入                |
| 每次交易的最大金额   | `SIMMER_ELON_MAX_POSITION`    | `max_position_usd`     | 5.00            | 每个价格区间的最大投资额                    |
| 价格区间宽度     | `SIMMER_ELON_BUCKET_SPREAD`    | `bucket_spread`      | 1                | 每侧相邻价格区间的数量（默认为1个）                |
| 智能调整比例     | `SIMMER_ELON_SIZING_PCT`    | `sizing pct`       | 0.05            | 每笔交易的资金占比（百分比）                    |
| 每次扫描的最大交易次数 | `SIMMER_ELON_MAX_TRADES`    | `max_trades_per_run`    | 6               | 每次扫描的最大交易次数                    |
| 平仓阈值       | `SIMMER_ELON_EXIT`      | `exit_threshold`     | 0.65            | 当价格区间价格超过此值时卖出                    |
| 最大滑点        | `SIMMER_ELON_SLIPPAGE_MAX`    | `slippage_max pct`     | 0.05            | 如果滑点超过此值，则放弃交易                    |
| 最小交易金额     | `SIMMER_ELON_MIN_POSITION`    | `min_position_usd`     | 2.00            | 智能调整的下限金额（美元）                    |
| 数据来源       | `SIMMER_ELON_DATA_SOURCE`    | `data_source`      | `xtracker`        | 数据来源（XTracker）                    |

配置文件的优先级高于环境变量，高于默认设置。

## 快速操作命令

```bash
# Check account balance and positions
python scripts/status.py

# Detailed position list
python scripts/status.py --positions
```

**API参考**：
- 基础URL：`https://api.simmer.markets`
- 认证方式：`Authorization: Bearer $SIMMER_API_KEY`
- 财产信息查询：`GET /api/sdk/portfolio`
- 交易头寸查询：`GET /api/sdk/positions`

## 策略执行过程

脚本会按以下步骤运行：
1. 每次运行时，获取Elon Musk推文事件的实时跟踪数据。
2. 获取当前推文数量、预测的推文数量以及剩余的天数。
3. 在Simmer平台上搜索与推文数量预测相匹配的交易市场（如果市场不存在，则自动导入相关数据）。
4. 找到与XTracker预测结果相匹配的价格区间。
5. 评估相邻的价格区间，如果所有价格区间之和低于配置的最大交易成本，则买入这些区间。
6. 检查当前持有的头寸，如果某个价格区间价格超过平仓阈值，则卖出该区间。
7. 实施安全机制，例如检查市场趋势变化（防止频繁买卖）和滑点情况。
8. 所有交易都会被标记为`sdk:elon-tweets`，以便后续跟踪。

## 自动导入功能

如果Simmer平台上尚不存在与Elon Musk推文数量相关的交易市场，该策略会自动导入这些市场数据：
- 从XTracker的跟踪信息中提取Polymarket市场的URL。
- 使用SDK提供的导入接口（支持多结果事件）批量导入数据。
- 无论实际价格区间数量多少，每天仅计算为1次导入。

## 智能调整交易金额

通过`--smart-sizing`参数，系统会自动计算每次交易的最大金额：
- 计算为可用USDC余额的5%（可通过`sizing pct`参数调整）。
- 如果Polymarket平台不支持动态调整，系统会使用固定的最大交易金额（默认为5.00美元）。

## 安全机制

在交易前，系统会进行以下检查：
- **市场趋势变化**：如果市场趋势波动过于剧烈，系统会放弃交易。
- **滑点风险**：如果预计滑点超过15%，系统会放弃交易。
- **市场状态**：如果市场已经关闭或交易结果已确定，系统会放弃交易。
- **极端价格**：如果价格区间价格超过98%或低于2%，系统会放弃交易。

可以通过`--no-safeguards`参数关闭这些安全机制（但不推荐这样做）。

## 数据标记

所有交易都会被标记为`source: "sdk:elon-tweets"`，以便：
- 在Polymarket的资产报告中区分不同策略的交易情况。
- 其他策略无法识别这些交易。
- 用户可以单独查看与Elon Musk推文相关的交易盈亏情况。

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

- **“未找到XTracker的跟踪数据”**：  
  可能是因为XTracker尚未更新Elon Musk的推文数据。新数据通常在每周三或周四发布。
- **“价格区间总和超过阈值”**：可能是因为价格区间过于狭窄，导致盈利空间太小。可以等待价格下降或调整价格区间宽度。
- **“未找到匹配的Simmer市场”**：可能是市场数据尚未导入。系统会在下一次运行时自动尝试导入。
- **“安全机制触发：市场趋势变化警告”**：可能是因为该市场的价格波动过于剧烈。建议等待市场稳定后再进行交易。
- **“外部钱包需要预签名订单”**：确保环境变量`WALLET_PRIVATE_KEY`已设置。SDK会自动签署交易订单，无需手动操作。
- **“余额显示为0美元，但实际上我有USDC”**：Polymarket使用的是`USDC.e`（一种桥接后的USDC代币，合约地址为`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`）。如果最近将USDC桥接到Polygon平台，可能需要先转换回原生USDC后再进行交易。
- **“API密钥无效”**：请从simmer.markets/dashboard的SDK标签页重新获取API密钥。

---

请注意：上述代码块中的````bash
   pip install simmer-sdk
   ````、````bash
# Check account balance and positions
python scripts/status.py

# Detailed position list
python scripts/status.py --positions
````和````bash
# Dry run (default — shows opportunities, no trades)
python elon_tweets.py

# Execute real trades
python elon_tweets.py --live

# With smart position sizing (uses portfolio balance)
python elon_tweets.py --live --smart-sizing

# Show XTracker stats only
python elon_tweets.py --stats

# Check positions only
python elon_tweets.py --positions

# View config
python elon_tweets.py --config

# Update config
python elon_tweets.py --set max_position_usd=10.00

# Disable safeguards (not recommended)
python elon_tweets.py --no-safeguards

# Quiet mode — only output on trades/errors (ideal for cron)
python elon_tweets.py --live --quiet

# Combine: frequent scanning, minimal noise
python elon_tweets.py --live --smart-sizing --quiet
````为占位符，实际代码需要根据实际情况进行填充。