---
name: polymarket-elon-tweets
displayName: Polymarket Elon Tweet Trader
description: '使用 XTracker 的帖子计数数据来交易 Polymarket 上的 “Elon Musk #tweets” 相关市场。当组合成本低于 1 美元时，买入相邻的价格区间，以获得结构上的优势。适用于用户希望交易与 Elon Musk 推文数量相关的市场、自动化进行与 Elon Musk 推文相关的投注、查看 XTracker 的统计数据，或执行类似 noovd 的交易策略的情况。'
metadata: {"clawdbot":{"emoji":"🐦","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false,"automaton":{"managed":true,"entrypoint":"elon_tweets.py"},"tunables":[{"env":"SIMMER_ELON_MAX_POSITION_USD","type":"number","default":50,"range":[1,200],"step":5,"label":"Max position size"},{"env":"SIMMER_ELON_BUCKET_SPREAD","type":"number","default":0.05,"range":[0.01,0.20],"step":0.01,"label":"Bucket spread"},{"env":"SIMMER_ELON_SIZING_PCT","type":"number","default":0.10,"range":[0.01,1.0],"step":0.01,"label":"Position sizing percentage"},{"env":"SIMMER_ELON_MAX_TRADES_PER_RUN","type":"number","default":5,"range":[1,20],"step":1,"label":"Max trades per run"},{"env":"SIMMER_ELON_EXIT_THRESHOLD","type":"number","default":0.85,"range":[0.5,0.99],"step":0.01,"label":"Exit probability threshold"},{"env":"SIMMER_ELON_SLIPPAGE_BPS","type":"number","default":100,"range":[10,500],"step":10,"label":"Slippage tolerance (basis points)"}]}}
authors:
  - Simmer (@simmer_markets)
attribution: "Strategy inspired by @noovd"
version: "1.0.4"
published: true
---
# Polymarket：基于Elon Musk推文数量的交易策略

使用XTracker提供的推文数量数据，在Polymarket平台上进行交易。

## 适用场景

- 当用户希望自动交易与Elon Musk推文数量相关的市场时
- 设置类似@noovd风格的批量交易策略
- 查看XTracker提供的推文事件进度和统计数据
- 监控并平仓现有的推文市场头寸
- 配置交易策略的参数（如买卖间隔或入场价格）

## 策略原理

Polymarket每周会发布一次“Elon Musk将发布多少条推文？”的预测活动，预测结果分为多个区间（例如：200-219条、220-239条、240-259条）。当某个区间被预测为“会发布”时，该区间的交易价格为1美元。具体步骤如下：

1. **获取XTracker的推文数量预测**：XTracker实时跟踪Elon Musk的推文数量并预测最终总数。
2. **确定目标区间**：找到与XTracker预测结果相匹配的区间。
3. **买入相邻区间**：买入目标区间及其两侧的区间（买卖间隔可配置）。
4. **判断是否盈利**：仅当所有买入区间的价格总和低于1美元（即盈利阈值）时才执行买入操作。
5. **结算利润**：当预测事件结果确定后，其中一个买入区间会获得1美元的收益，从而覆盖交易成本。

## 设置流程

用户需要完成以下步骤来启用该策略：

1. **安装Simmer SDK**  
   ```bash
   pip install simmer-sdk
   ```

2. **获取Simmer API密钥**：  
   - 从simmer.markets dashboard的SDK标签页获取API密钥，并将其存储在环境变量`SIMMER_API_KEY`中。
3. **提供钱包私钥**（用于实时交易）：  
   - 这是用户Polymarket钱包的私钥（用于存放USDC代币）。  
   - 将私钥存储在环境变量`WALLET_PRIVATE_KEY`中。SDK会使用该密钥在客户端自动签署交易订单，无需手动操作。
4. **配置策略参数**：  
   - 最大买入区间价格总和：价格总和的阈值（默认为0.90美元）。  
   - 每个区间的最大买入金额：每个区间的最大买入金额（默认为5.00美元）。  
   - 买卖间隔：两侧的区间数量（默认为1个区间）。  
   - 平仓阈值：当区间价格超过此阈值时卖出。  
5. **将配置保存到config.json文件或环境变量中**。

6. **设置定时任务**（默认关闭，用户需手动启用）：  
   - 使用`cron`命令来定期执行该策略。

## 配置参数

| 参数 | 环境变量 | 配置键 | 默认值 | 说明 |
|---------|-------------|------------|---------|-------------|
| 最大买入区间价格总和 | `SIMMER_ELON_MAX_BUCKET_SUM` | `max_bucket_sum` | 0.90 | 仅当所有区间价格总和低于此值时买入 |
| 每个区间的最大买入金额 | `SIMMER_ELON_MAX_POSITION` | `max_position_usd` | 5.00 | 每个区间的最大买入金额 |
| 买卖间隔 | `SIMMER_ELON_BUCKET_SPREAD` | `bucket_spread` | 1 | 每侧购买的区间数量（默认为1个区间） |
| 智能调整比例 | `SIMMER_ELON_SIZING_PCT` | `sizing_pct` | 每笔交易的资金占比（默认为0.05%） |
| 每次扫描的最大交易次数 | `SIMMER_ELON_MAX_TRADES` | `max_trades_per_run` | 每次扫描的最大交易次数（默认为6次） |
| 平仓阈值 | `SIMMER_ELON_EXIT` | `exit_threshold` | 0.65 | 当区间价格超过此值时卖出 |
| 最大滑点限制 | `SIMMER_ELON_SLIPPAGE_MAX` | `slippage_max pct` | 如果滑点超过此值则放弃交易（默认为0.05%） |
| 最小买入金额 | `SIMMER_ELON_MIN_POSITION` | `min_position_usd` | 智能调整的下限（默认为2.00美元） |
| 数据来源 | `SIMMER_ELON_DATA_SOURCE` | `data_source` | `xtracker` | 数据来源（XTracker） |

配置优先级：config.json > 环境变量 > 默认值。

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
- 财产信息：`GET /api/sdk/portfolio`
- 交易头寸：`GET /api/sdk/positions`

## 运行策略

脚本的运行流程如下：

- 每次执行时，脚本会：
  - 获取XTracker提供的Elon Musk推文事件的实时数据。
  - 计算当前推文数量、预测的推文数量以及剩余的天数。
  - 在Simmer平台上搜索匹配的推文数量交易市场（如果不存在，则自动导入相关数据）。
  - 找到与XTracker预测结果相匹配的区间。
  - 评估相邻区间，并在价格总和低于配置阈值时买入这些区间。
  - 检查现有头寸，如果某个区间价格超过平仓阈值则卖出。
  - 实施安全机制（如防止价格剧烈波动导致的亏损）。
  - 所有交易都会被标记为`sdk:elon-tweets`以便后续跟踪。

## 自动导入功能

如果Simmer平台上尚未包含与Elon Musk推文数量相关的市场，该策略会自动导入这些市场数据：
- 从XTracker的跟踪信息中提取Polymarket事件的URL。
- 使用SDK提供的导入接口（支持多结果事件）批量导入数据。
- 无论实际买入的区间数量多少，每天仅计为一次导入。

## 智能调整机制

通过`--smart-sizing`参数，交易金额会根据可用USDC余额的5%进行计算（可通过`sizing_pct`参数调整）；如果Polymarket平台不支持动态调整，则使用固定金额（默认为5.00美元）。

## 安全机制

在交易前，该策略会进行以下检查：
- **价格剧烈波动警告**：如果市场走势频繁反转，则放弃交易。
- **滑点限制**：如果预计滑点超过15%，则放弃交易。
- **市场状态**：如果市场已关闭或预测结果已确定，则放弃交易。
- **极端价格**：如果某个区间的价格超过98%或低于2%，则放弃交易。

可以通过`--no-safeguard`参数关闭这些安全机制（不建议使用）。

## 数据标记

所有交易都会被标记为`source: "sdk:elon-tweets"`，这样：
- 财产报表会按策略进行分类显示。
- 其他策略不会误售用户的推文交易结果。
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

- **“未找到XTracker的跟踪数据”**：  
  - 可能是因为XTracker尚未更新Elon Musk的推文数据。新数据通常在每周三或周四发布。
- **“区间价格总和超过阈值”**：可能是因为该市场的价格波动较大，导致盈利空间过小。请等待价格下降或调整买卖间隔。
- **“未找到匹配的Simmer市场”**：可能是市场数据尚未导入。策略会在下一次运行时自动尝试导入。
- **“安全机制触发”**：可能是因为市场走势过于剧烈。请等待一段时间后再进行交易。
- **“外部钱包需要预签名订单”**：确保环境变量`WALLET_PRIVATE_KEY`已设置正确。SDK会自动签署交易订单。
- **“余额显示为0美元，但实际有USDC”**：Polymarket使用的是`USDC.e`（一种桥接后的USDC代币，合约地址为`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`）。如果用户最近将USDC桥接到了Polygon平台，可能需要先将USDC.e兑换为原生USDC后再进行交易。
- **“API密钥无效”**：请从simmer.markets dashboard的SDK标签页获取新的API密钥。