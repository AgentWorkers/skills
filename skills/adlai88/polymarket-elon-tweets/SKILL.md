---
name: polymarket-elon-tweets
displayName: Polymarket Elon Tweet Trader
description: '使用 XTracker 的帖子数量数据来交易 Polymarket 上的 “Elon Musk #tweets” 相关市场。当组合成本低于 1 美元时，购买相邻的价格区间桶（range buckets），以获得结构性优势。此策略适用于用户希望交易与 Elon Musk 推文数量相关的市场、自动化进行 Elon Musk 推文相关的投注、查看 XTracker 的统计数据，或执行类似 noovd 的交易策略的情况。'
metadata: {"clawdbot":{"emoji":"🐦","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false,"automaton":{"managed":true,"entrypoint":"elon_tweets.py"},"tunables":[{"env":"SIMMER_ELON_MAX_POSITION_USD","type":"number","default":50,"range":[1,200],"step":5,"label":"Max position size"},{"env":"SIMMER_ELON_BUCKET_SPREAD","type":"number","default":0.05,"range":[0.01,0.20],"step":0.01,"label":"Bucket spread"},{"env":"SIMMER_ELON_SIZING_PCT","type":"number","default":0.10,"range":[0.01,1.0],"step":0.01,"label":"Position sizing percentage"},{"env":"SIMMER_ELON_MAX_TRADES_PER_RUN","type":"number","default":5,"range":[1,20],"step":1,"label":"Max trades per run"},{"env":"SIMMER_ELON_EXIT_THRESHOLD","type":"number","default":0.85,"range":[0.5,0.99],"step":0.01,"label":"Exit probability threshold"},{"env":"SIMMER_ELON_SLIPPAGE_BPS","type":"number","default":100,"range":[10,500],"step":10,"label":"Slippage tolerance (basis points)"}]}}
authors:
  - Simmer (@simmer_markets)
attribution: "Strategy inspired by @noovd"
version: "1.0.4"
difficulty: advanced
published: true
---
# Polymarket：基于Elon Musk推文数量的交易策略

使用XTracker提供的推文数量数据，在Polymarket平台上进行交易。

## 适用场景

当用户希望执行以下操作时，可以使用此策略：
- 自动交易与Elon Musk推文数量相关的市场；
- 设置类似@noovd风格的批量交易规则；
- 查看XTracker提供的当前推文事件的相关数据和统计信息；
- 监控并平仓现有的推文交易头寸；
- 配置批量交易的买卖间隔或入场价格阈值。

## 策略原理

Polymarket每周会发布一次“Elon Musk会发布多少条推文？”的预测活动，预测结果分为多个区间（例如：200-219条、220-239条、240-259条）。其中只有一个区间预测结果为“YES”，对应的奖励为1美元。该策略的具体步骤如下：
1. **获取XTracker的推文预测数据**：XTracker会实时跟踪Elon Musk的推文数量并预测最终的总数；
2. **确定目标区间**：选择与XTracker预测结果相匹配的区间；
3. **买入相邻区间**：购买目标区间及其两侧的区间（买卖间隔可配置）；
4. **判断成本是否合理**：仅当所有相关区间的价格总和低于1美元（即“+EV”阈值）时才进行买入；
5. **收益结算**：当预测结果确定后，系统会自动结算其中一个区间的收益（1美元），以覆盖所有交易成本。

## 设置流程

当用户请求安装或配置此策略时，需要完成以下步骤：
1. **安装Simmer SDK**：  
   ```bash
   pip install simmer-sdk
   ```

2. **获取Simmer API密钥**：  
   用户可以从simmer.markets/dashboard的SDK标签页获取API密钥，并将其存储在环境变量`SIMMER_API_KEY`中。
3. **提供钱包私钥**：  
   这是用于Polymarket交易的私钥（用于存储USDC代币的钱包），需存储在环境变量`WALLET_PRIVATE_KEY`中。SDK会使用此密钥在客户端自动签署交易订单，无需用户手动操作。
4. **配置策略参数**：  
   - **最大交易成本**：所有相关区间的价格总和阈值（默认为0.90美元）；
   - **每次交易的最大金额**：每个区间的最大买入金额（默认为5.00美元）；
   - **买卖间隔**：每侧购买的相邻区间数量（默认为1个区间）；
   **平仓阈值**：当某个区间价格超过此阈值时卖出；
5. **保存配置**：将所有参数保存到`config.json`文件或环境变量中。
6. **设置定时任务**：（默认情况下定时任务是禁用的，用户需要手动启用。）

## 配置选项

| 配置项 | 环境变量 | 配置键 | 默认值 | 说明 |
|---------|-------------|------------|---------|-------------|
| 最大交易成本 | `SIMMER_ELON_MAX_BUCKET_SUM` | `max_bucket_sum` | 0.90 | 仅当所有相关区间的价格总和低于此值时才买入 |
| 每次交易的最大金额 | `SIMMER_ELON_MAX_POSITION` | `max_position_usd` | 5.00 | 每个区间的最大买入金额 |
| 买卖间隔 | `SIMMER_ELON_BUCKET_SPREAD` | `bucket_spread` | 1 | 每侧购买的相邻区间数量（默认为1个区间） |
| 智能调整比例 | `SIMMER_ELON_SIZING_PCT` | `sizing pct` | 每笔交易的资金占比（默认为0.05%） |
| 每次扫描的最大交易数量 | `SIMMER_ELON_MAX_TRADES` | `max_trades_per_run` | 每次扫描的最大交易次数（默认为6次） |
| 平仓阈值 | `SIMMER_ELON_EXIT` | `exit_threshold` | 0.65 | 当某个区间价格超过此阈值时卖出 |
| 最大滑点限制 | `SIMMER_ELON_SLIPPAGE_MAX` | `slippage_max pct` | 如果滑点超过此值则放弃交易 |
| 最小交易金额 | `SIMMER_ELON_MIN_POSITION` | `min_position_usd` | 智能调整的下限金额（默认为2.00美元） |
| 数据源 | `SIMMER_ELON_DATA_SOURCE` | `data_source` | xtracker | 数据来源（XTracker） |

配置文件的优先级：`config.json` > 环境变量 > 默认值。

## 快捷命令

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
1. 每次运行时，获取XTracker提供的Elon Musk推文事件的实时数据；
2. 计算当前推文数量、预测的推文总数以及剩余的预测天数；
3. 在Simmer平台上查找与推文数量预测相匹配的交易市场（如果市场数据不存在，则自动导入）；
4. 找到与XTracker预测结果相匹配的交易区间；
5. 评估所有相关区间的价格，并在价格总和低于配置的阈值时买入；
6. 检查现有头寸，如果某个区间的价格超过平仓阈值则卖出；
7. 实施安全机制，例如检查市场趋势反转情况或滑点风险；
8. 所有交易都会被标记为`sdk:elon-tweets`以便后续跟踪。

## 自动导入功能

如果Simmer平台上还没有与Elon Musk推文数量相关的交易市场，该策略会自动导入这些市场数据：
- 从XTracker的跟踪信息中提取Polymarket的交易链接；
- 使用SDK提供的导入接口（支持多结果事件）；
- 将所有相关区间的数据作为一个整体导入；
- 每天视为一次导入操作，无论实际区间的数量多少。

## 智能调整机制

通过`--smart-sizing`参数，可以启用智能调整机制：
- 交易金额会根据用户可用USDC余额的5%进行计算（可通过`sizing pct`参数调整）；
- 最大交易金额受`max_position`参数的限制（默认为5.00美元）；
- 如果无法获取到市场数据，则使用固定金额进行交易。

## 安全机制

在交易前，策略会执行以下检查：
- **市场趋势反转警告**：如果市场趋势发生剧烈反转，则放弃交易；
- **滑点限制**：如果预计滑点超过15%，则放弃交易；
- **市场状态检查**：跳过已关闭或结果已确定的市场；
- **价格异常**：跳过价格极端（高于98%或低于2%）的交易区间。

可以通过`--no-safeguards`参数关闭这些安全机制（但不建议这样做）。

## 数据标记

所有交易都会被标记为`source: "sdk:elon-tweets"”，这样：
- 用户可以在Polymarket的资产概览中看到该策略的交易情况；
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

- **“未找到XTracker的跟踪数据”**：可能是因为XTracker尚未更新Elon Musk的推文数据。新数据通常在每周三或周四更新。
- **“相关市场价格过高”**：可能是由于市场波动较大，导致交易机会较少。可以等待价格下降或调整`bucket_spread`参数。
- **“未找到匹配的Simmer市场”**：可能是市场数据尚未导入。策略会在下一次运行时自动尝试导入。
- **“安全机制触发”**：可能是因为市场趋势波动过于剧烈。建议等待市场稳定后再进行交易。
- **“外部钱包需要预签名订单”**：确保环境变量`WALLET_PRIVATE_KEY`已设置正确。SDK会自动使用该密钥签署交易订单，无需手动操作。
- **“账户余额显示为0美元，但实际上有USDC”**：Polymarket使用的是`USDC.e`（一种桥接后的USDC代币，合约地址为`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`）。如果最近将USDC桥接到Polygon平台，可能需要先将USDC转换为`USDC.e`后再进行交易。
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
````为占位符，实际代码需要根据具体的实现细节进行填充。