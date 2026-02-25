---
name: polymarket-elon-tweets
displayName: Polymarket Elon Tweet Trader
description: '使用 XTracker 的推文计数数据来交易 Polymarket 上的“埃隆·马斯克（Elon Musk）#推文”相关市场。当组合成本低于 1 美元时，买入相邻的价格区间，以获得结构性优势。适用于用户希望交易与推文数量相关的市场、自动化进行与埃隆·马斯克推文相关的投资策略、查看 XTracker 的统计数据，或执行类似 noovd 的交易策略的情况。'
metadata: {"clawdbot":{"emoji":"🐦","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false,"automaton":{"managed":true,"entrypoint":"elon_tweets.py"}}}
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
- 自动交易与Elon Musk推文数量相关的市场
- 设置类似@noovd风格的批量交易规则
- 查看XTracker提供的推文事件进度和统计数据
- 监控并平仓现有的推文交易头寸
- 配置交易策略中的价格区间（即“桶”范围）

## 策略原理

Polymarket每周会发布一次关于“Elon Musk将发布多少条推文？”的预测活动，这些活动会设置多个价格区间（例如：200-219、220-239、240-259）。当预测结果为“是”时，对应的区间价格为1美元。该策略的具体步骤如下：
1. **获取XTracker的推文数量预测数据**：XTracker会实时跟踪Elon Musk的推文数量并预测最终的总数。
2. **确定目标价格区间**：找到与XTracker预测结果相匹配的价格区间。
3. **买入相邻的价格区间**：买入目标区间及其两侧的价格区间（区间宽度可配置）。
4. **检查总成本**：只有当所有买入区间的价格总和低于1美元（即“正收益阈值”）时，才会执行买入操作。
5. **收益实现**：当预测结果最终确定时，其中一个买入区间会获得1美元的收益，从而覆盖所有交易成本。

## 设置流程

当用户请求安装或配置此策略时，需要完成以下步骤：
1. **安装Simmer SDK**  
   ```bash
   pip install simmer-sdk
   ```

2. **获取Simmer API密钥**：  
   用户可以从simmer.markets/dashboard的SDK标签页获取API密钥，并将其存储在环境变量`SIMMER_API_KEY`中。
3. **提供钱包私钥**（用于实时交易）：  
   这是用户在Polymarket平台上的钱包私钥（用于存储USDC代币）。请将其存储在环境变量`WALLET_PRIVATE_KEY`中。SDK会使用该密钥在客户端自动签署交易订单，无需用户手动操作。
4. **配置策略参数**：  
   - **最大买入总金额**：所有买入区间的价格总和阈值（默认值为0.90美元）。
   - **每次交易的最大金额**：每个买入区间的最大投资额（默认值为5.00美元）。
   - **价格区间宽度**：两侧需要买入的相邻区间数量（默认值为1，即目标区间两侧各买入1个区间）。
   - **平仓阈值**：当某个买入区间的价格超过此阈值时，执行平仓操作（默认值为0.65美元）。
5. **将配置保存到config.json文件或环境变量中**。

6. **设置定时任务**：  
   该策略默认不自动执行交易（需要用户手动启用定时任务）。

## 配置参数

| 参数                | 环境变量          | 配置键            | 默认值            | 说明                                      |
|------------------|------------------|------------------|------------------|-----------------------------------------|
| 最大买入总金额        | `SIMMER_ELON_MAX_BUCKET_SUM` | `max_bucket_sum`      | 0.90              | 只有当所有买入区间的价格总和低于此值时才执行买入操作          |
| 每次交易的最大金额       | `SIMMER_ELON_MAX_POSITION` | `max_position_usd`     | 5.00              | 每个买入区间的最大投资额                              |
| 价格区间宽度         | `SIMMER_ELON_BUCKET_SPREAD` | `bucket_spread`      | 1                | 每侧需要买入的相邻区间数量                              |
| 智能调整比例         | `SIMMER_ELON_SIZING_PCT` | `sizing pct`       | 0.05              | 每笔交易占账户余额的百分比                              |
| 每次扫描的最大交易数量     | `SIMMER_ELON_MAX_TRADES` | `max_trades_per_run`     | 6                | 每次扫描周期内的最大交易数量                              |
| 平仓阈值           | `SIMMER_ELON_EXIT`     | `exit_threshold`     | 0.65              | 当某个买入区间的价格超过此阈值时执行平仓操作                   |
| 最大滑点限制         | `SIMMER_ELON_SLIPPAGE_MAX` | `slippage_max pct`     | 0.05              | 如果滑点超过此值，则放弃交易                              |
| 最小投资额           | `SIMMER_ELON_MIN_POSITION` | `min_position_usd`     | 2.00              | 智能调整策略的最低投资额                              |
| 数据源             | `SIMMER_ELON_DATA_SOURCE` | `data_source`       | `xtracker`          | 数据来源（XTracker）                               |

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
   - 获取XTracker提供的Elon Musk推文事件的实时跟踪数据。
   - 获取当前的推文数量、预测的推文发布速度以及剩余的天数。
   - 在Simmer平台上查找与推文数量预测相匹配的交易市场（如果市场不存在，则自动导入相关数据）。
   - 找到与XTracker预测结果相匹配的价格区间。
   - 评估所有相邻的价格区间，并根据配置的策略执行买入或平仓操作。

## 自动导入机制

如果Simmer平台上还没有相关的推文数量交易市场，该策略会自动导入这些市场数据：
- 从XTracker的跟踪信息中提取Polymarket市场的URL。
- 使用SDK提供的导入接口（支持多结果事件）批量导入数据。
- 无论实际买入的区间数量多少，每天都算作一次导入操作。

## 智能调整投资额机制

通过`--smart-sizing`参数，每次交易的投资额会按照以下方式计算：
- 投资额 = 可用USDC余额的5%（可通过`sizing pct`参数进行配置）。
- 如果投资组合数据不可用，投资额将默认设置为`max_position`参数指定的金额（5.00美元）。

## 安全机制

在交易前，该策略会进行以下检查：
- **价格波动预警**：如果市场趋势发生剧烈反转，将放弃当前交易。
- **滑点限制**：如果预计的滑点超过15%，将放弃交易。
- **市场状态检查**：如果市场已经关闭或交易结果已经确定，将放弃交易。
- **价格异常检查**：如果某个买入区间的价格超过98%或低于2%，将放弃交易。

可以通过`--no-safeguards`参数关闭这些安全机制（但不推荐这样做）。

## 数据标记

所有交易都会被标记为`source: "sdk:elon-tweets"”，以便进行后续跟踪：
- 这有助于在投资组合报告中区分不同策略的交易结果。
- 其他策略将不会误售用户通过此策略进行的推文交易。
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

## 常见问题及解决方法

- **“未找到XTracker的跟踪数据”**：  
  可能是因为XTracker尚未开始更新Elon Musk的推文数据。新数据通常在每周三或周四发布。

- **“买入区间的总价格超过阈值”**：  
  可能是因为当前市场价格过高，导致投资机会较少。建议等待价格下降或调整价格区间宽度。

- **“未找到匹配的Simmer市场”**：  
  可能是因为市场数据尚未导入。策略会在下次运行时自动尝试导入。

- **“安全机制触发”**：  
  可能是因为市场趋势波动过于剧烈。建议等待市场稳定后再进行交易。

- **“外部钱包需要预签名订单”**：  
  确保环境变量`WALLET_PRIVATE_KEY`已设置正确。SDK会使用该密钥自动签署交易订单，无需用户手动操作。

- **“账户余额显示为0美元，但实际上我有USDC”**：  
  Polymarket使用的是`USDC.e`（一种桥接后的USDC代币，合约地址为`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`）。如果你最近将USDC桥接到了Polygon平台，可能需要先将USDC转换为`USDC.e`后再进行交易。

- **“API密钥无效”**：  
  请从simmer.markets dashboard的SDK标签页获取新的API密钥。