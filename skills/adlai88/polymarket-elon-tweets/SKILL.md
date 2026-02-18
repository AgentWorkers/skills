---
name: polymarket-elon-tweets
displayName: Polymarket Elon Tweet Trader
description: '使用 XTracker 的推文计数数据来交易 Polymarket 上的 “Elon Musk #tweets” 相关市场。当组合成本低于 1 美元时，购买相邻的价格区间桶（range buckets），以获得结构上的优势。适用于希望交易与 Elon Musk 推文数量相关的市场、自动化进行与 Elon Musk 推文相关的投资策略、查看 XTracker 的统计数据，或执行类似 noovd 的交易策略的用户。'
metadata: {"clawdbot":{"emoji":"🐦","requires":{"env":["SIMMER_API_KEY","WALLET_PRIVATE_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
attribution: "Strategy inspired by @noovd"
version: "1.0.2"
published: true
---
# Polymarket：基于Elon Musk推文数量的交易策略

使用XTracker提供的推文数量数据，在Polymarket平台上进行交易。

## 适用场景

当用户希望执行以下操作时，可以使用此策略：
- 自动交易与Elon Musk推文数量相关的市场
- 设置类似@noovd风格的批量交易规则
- 查看XTracker提供的推文事件进度和统计数据
- 监控并退出现有的推文交易头寸
- 配置交易策略的参数（如买卖间隔或入场价格阈值）

## 策略原理

Polymarket每周会发布一次“Elon Musk将发布多少条推文？”的预测活动，预测结果分为多个区间（例如：200-219、220-239、240-259条）。如果预测结果落在某个区间内，该区间的交易价格为1美元。策略的具体步骤如下：
1. **获取XTracker的推文数量预测数据**：XTracker会实时跟踪Elon Musk的推文数量并预测最终总数。
2. **确定目标区间**：选择与XTracker预测结果相匹配的区间。
3. **买入相邻区间**：买入目标区间及其两侧的区间（买入间隔可配置）。
4. **判断成本是否合理**：只有当所有买入区间的价格总和低于1美元（即“正收益”阈值）时，才会执行买入操作。
5. **结算收益**：当预测结果确定后，系统会自动结算一个区间的收益，从而覆盖所有买入成本。

## 设置流程

当用户请求安装或配置此策略时，需要完成以下步骤：
1. **安装Simmer SDK**  
   ```bash
   pip install simmer-sdk
   ```

2. **获取Simmer API密钥**：  
   用户可以从simmer.markets/dashboard的SDK标签页获取API密钥，并将其存储在环境变量`SIMMER_API_KEY`中。
3. **提供钱包私钥**：  
   这是用于在Polymarket平台上进行交易的私钥（用于存储USDC代币的钱包）。请将私钥存储在环境变量`WALLET_PRIVATE_KEY`中。SDK会使用该密钥在客户端自动签署交易订单，无需用户手动操作。
4. **配置策略参数**：  
   - **最大买入金额**：所有买入区间的价格总和阈值（默认为0.90美元）  
   - **每次交易的最大金额**：每个买入区间的最大金额（默认为5.00美元）  
   - **买入间隔**：两侧买入的区间数量（默认为1个区间）  
   - **卖出阈值**：当某个区间价格超过此阈值时卖出  
   - **其他参数**：可根据需要调整其他配置项。
5. **将配置保存到config.json文件或环境变量中**  
6. **设置定时任务**：（默认未启用，用户需手动启用定时执行）

## 配置参数

| 参数          | 环境变量        | 配置键            | 默认值            | 说明                          |
|----------------|------------------|------------------|------------------|--------------------------------------------|
| 最大买入金额      | `SIMMER_ELON_MAX_BUCKET_SUM` | `max_bucket_sum`      | 0.90                          | 只有当所有买入区间价格总和低于此值时才买入            |
| 每次交易的最大金额    | `SIMMER_ELON_MAX_POSITION` | `max_position_usd`     | 5.00                          | 每个买入区间的最大金额                    |
| 买入间隔        | `SIMMER_ELON_BUCKET_SPREAD` | `bucket_spread`      | 1                              | 每侧买入的区间数量（默认为1个区间）                |
| 智能调整比例     | `SIMMER_ELON_SIZING_PCT` | `sizing pct`       | 0.05                          | 每笔交易占余额的百分比                  |
| 每次扫描的最大交易数量 | `SIMMER_ELON_MAX_TRADES` | `max_trades_per_run`    | 6                              | 每次扫描的最大交易数量                    |
| 卖出阈值      | `SIMMER_ELON_EXIT`     | `exit_threshold`     | 0.65                          | 当某个区间价格超过此值时卖出                    |
| 最大滑点        | `SIMMER_ELON_SLIPPAGE_MAX` | `slippage_max pct`     | 0.25                          | 如果滑点超过此值则放弃交易                    |
| 最小买入金额      | `SIMMER_ELON_MIN_POSITION` | `min_position_usd`     | 2.00                          | 智能调整的下限金额                    |
| 数据来源        | `SIMMER_ELON_DATA_SOURCE` | `data_source`      | `xtracker`                        | 数据来源                        |

配置优先级：环境变量 > config.json > 默认值。

## 快速命令

```bash
# Check account balance and positions
python scripts/status.py

# Detailed position list
python scripts/status.py --positions
```

**API参考**：
- 基本URL：`https://api.simmer.markets`
- 认证方式：`Authorization: Bearer $SIMMER_API_KEY`
- 获取投资组合信息：`GET /api/sdk/portfolio`
- 查看交易头寸：`GET /api/sdk/positions`

## 策略运行流程

脚本的运行流程如下：
1. 每次运行时，获取XTracker提供的Elon Musk推文数量预测数据。
2. 获取实时推文数量、预测总数及剩余预测天数。
3. 在Simmer平台上查找与预测结果匹配的交易市场（如果市场不存在，则自动导入数据）。
4. 找到与预测结果相匹配的买入区间。
5. 评估所有买入区间，如果所有区间价格总和低于配置的阈值，则买入这些区间。
6. 检查现有交易头寸，如果某个区间价格超过卖出阈值，则卖出。
7. 实施安全机制（如防止价格剧烈波动导致的错误交易）。
8. 所有交易都会被标记为`sdk:elon-tweets`，以便后续跟踪。

## 自动导入功能

如果Simmer平台上尚不存在与Elon Musk推文数量相关的交易市场，该策略会自动导入这些市场数据：
- 从XTracker的跟踪信息中提取Polymarket的交易URL。
- 使用SDK提供的导入接口（支持多结果事件）批量导入数据。
- 无论实际买入区间数量多少，每天仅计为一次导入。

## 智能调整交易金额

通过`--smart-sizing`参数，可以调整每次交易的金额：
- 交易金额默认为可用USDC余额的5%（可通过`sizing pct`参数调整）。
- 如果投资组合中无法找到符合条件的交易数据，系统会使用固定金额进行交易。

## 安全机制

在交易前，策略会进行以下检查：
- **价格波动预警**：如果价格波动幅度过大，会放弃交易。
- **滑点限制**：如果预计滑点超过15%，会放弃交易。
- **市场状态检查**：跳过已关闭或已完成交易的市场。
- **价格异常**：跳过价格极端（高于98%或低于2%）的区间。

可以通过`--no-safeguards`参数关闭这些安全机制（不推荐使用）。

## 数据标记

所有交易都会被标记为`source: "sdk:elon-tweets"`，以便：
- 在投资组合报告中区分不同策略的交易结果。
- 其他策略不会误售用户的推文交易相关资产。
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

- **“未找到XTracker的跟踪数据”**：可能是XTracker尚未更新Elon Musk的推文数据。新数据通常在每周三或周四发布。
- **“买入区间价格过高”**：可能是买入区间价格过高，导致利润空间较小。可以等待价格下降或调整买入间隔。
- **“未找到匹配的Simmer市场”**：可能是市场数据尚未导入。策略会在下一次运行时自动尝试导入。
- **“安全机制触发”**：可能是用户在该市场的交易行为过于频繁或剧烈。建议等待一段时间后再进行交易。
- **“外部钱包需要预签名订单”**：确保环境变量`WALLET_PRIVATE_KEY`已设置。SDK会自动使用私钥签署订单。
- **“余额显示为0美元，但实际上有USDC”**：Polymarket使用的是桥接后的USDC（合约地址`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`），而非原生USDC。如果最近将USDC桥接到Polygon平台，请先转换后再尝试交易。
- **“API密钥无效”**：请从simmer.markets/dashboard的SDK标签页重新获取API密钥。