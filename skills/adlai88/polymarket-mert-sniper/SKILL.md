---
name: polymarket-mert-sniper
displayName: Mert Sniper
description: 在 Polymarket 上，存在一种接近到期的“定罪交易”策略（conviction trading）。这种策略通常在市场的概率分布严重失衡时进行操作（即市场走势极不清晰或难以预测）。建议通过主题进行筛选，控制投注金额，并且只在截止日期临近时、且市场走势明显强劲的情况下进行交易。
metadata: {"clawdbot":{"emoji":"🎯","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false,"automaton":{"managed":true,"entrypoint":"mert_sniper.py"}}}
authors:
  - Simmer (@simmer_markets)
attribution: "Strategy inspired by @mert — https://x.com/mert/status/2020216613279060433"
version: "1.0.7"
published: true
---
# Mert Sniper

这是一个用于在Polymarket上进行近乎到期的交易策略。该策略专注于在赔率严重失衡时进行交易。

> 策略来源：[@mert](https://x.com/mert/status/2020216613279060433) — 可通过主题进行筛选，限制投注金额，等待交易临近到期时再进行交易，且只交易赔率较高的市场。

> **这是一个模板。** 默认逻辑（到期时间 + 赔率筛选）可以帮助你开始使用该策略 — 你可以根据自己的需求添加自定义的筛选条件、交易时机规则或市场选择标准。该技能会处理所有的市场发现、交易执行和风险控制等细节。

## 适用场景

> **仅适用于Polymarket。** 所有交易都在Polymarket上使用真实的USDC进行。使用`--live`选项可进行实时交易，否则为模拟交易。

当用户希望执行以下操作时，可以使用此策略：
- 交易那些即将到期的市场（最后时刻的投注）
- 按主题筛选市场（例如，仅交易SOLANA或加密货币市场）
- 限制投注金额（例如，每次不超过10美元）
- 仅在赔率严重失衡时进行交易（例如，赔率至少为60/40）
- 运行自动化的到期交易策略

## 设置流程

1. **获取Simmer API密钥**
   - 从simmer.markets/dashboard的SDK标签页获取API密钥
   - 将其存储在环境变量`SIMMER_API_KEY`中

2. **获取钱包私钥**（实时交易所需）
   - 这是用于Polymarket钱包的私钥（该钱包中存储着USDC）
   - 将其存储在环境变量`WALLET_PRIVATE_KEY`中
   - SDK会使用此私钥在客户端自动签名交易订单，无需手动签名

3. **配置设置**（或确认默认值）
   - 市场筛选：要扫描的市场（默认：所有市场）
   - 最大投注金额：每次交易的最大金额（默认10美元）
   - 到期时间窗口：距离交易结算还有多少时间（默认2分钟）
   - 最小赔率差：最低的赔率差异（默认60/40）

4. **将设置保存到config.json文件或环境变量中**

## 配置选项

| 配置项 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| 市场筛选 | `SIMMER_MERT_FILTER` | (all) | 根据标签或关键词筛选市场（例如 `solana`、`crypto`） |
| 最大投注金额 | `SIMMER_MERT_MAX_BET` | 10.00 | 每次交易的最大金额（美元） |
| 到期时间窗口 | `SIMMER_MERT_EXPIRY_MINS` | 2 | 仅交易在N分钟内到期的市场 |
| 最小赔率差 | `SIMMER_MERT_MIN_SPLIT` | 0.60 | 仅当赔率差达到或超过此值时进行交易（例如0.60表示赔率为60/40） |
| 每次扫描的最大交易次数 | `SIMMER_MERT_MAX_TRADES` | 5 | 每次扫描周期内的最大交易次数 |
| 智能投注比例 | `SIMMER_MERT_SIZING_PCT` | 0.05 | 每次交易的投注金额占余额的百分比 |

## 快速命令

```bash
# Check account balance and positions
python scripts/status.py

# Detailed position list
python scripts/status.py --positions
```

**API参考：**
- 基础URL：`https://api.simmer.markets`
- 认证：`Authorization: Bearer $SIMMER_API_KEY`
- 投资组合：`GET /api/sdk/portfolio`
- 持仓情况：`GET /api/sdk/positions`

## 运行该策略

```bash
# Dry run (default -- shows opportunities, no trades)
python mert_sniper.py

# Execute real trades
python mert_sniper.py --live

# Filter to specific markets
python mert_sniper.py --filter solana

# Custom expiry window (5 minutes)
python mert_sniper.py --expiry 5

# With smart position sizing (uses portfolio balance)
python mert_sniper.py --live --smart-sizing

# Check positions only
python mert_sniper.py --positions

# View config
python mert_sniper.py --config

# Disable safeguards (not recommended)
python mert_sniper.py --no-safeguards
```

## 工作原理

该脚本每个周期会执行以下操作：
1. 从Simmer API获取活跃市场（可选地根据标签/关键词进行筛选）
2. 筛选出在到期时间窗口内到期的市场
3. 检查价格赔率差 — 仅当某一方的赔率达到或超过最小值（默认60%）时进行交易
4. 确定交易方向：选择赔率较高的一方进行投注
5. **风险控制**：检查市场是否存在突然反转的风险、滑点情况以及市场状态
6. **执行交易**：在赔率较高的一方进行投注，同时限制投注金额不超过最大值
7. 报告扫描到的市场、筛选后的市场以及实际进行交易的市场列表

## 示例输出

```
🎯 Mert Sniper - Near-Expiry Conviction Trading
==================================================

  [DRY RUN] No trades will be executed. Use --live to enable trading.

  Configuration:
  Filter:        solana
  Max bet:       $10.00
  Expiry window: 2 minutes
  Min split:     60/40
  Max trades:    5
  Smart sizing:  Disabled
  Safeguards:    Enabled

  Fetching markets (filter: solana)...
  Found 12 active markets

  Markets expiring within 2 minutes: 2

  SOL highest price on Feb 10?
     Resolves in: 1m 34s
     Split: YES 72% / NO 28%
     Side: YES (72% >= 60%)
     [DRY RUN] Would buy $10.00 on YES

  Summary:
  Markets scanned: 12
  Near expiry:     2
  Strong split:    1
  Trades executed: 0

  [DRY RUN MODE - no real trades executed]
```

## 常见问题及解决方法

**“未找到市场”**
- 检查你的筛选条件 — 先尝试不使用任何筛选条件进行搜索
- 可能是因为某些市场暂时不可用（请查看simmer.markets的相关信息）

**“没有在指定时间内到期的市场”**
- 增加到期时间窗口：`--expiry 10`（将时间窗口设置为10分钟）
- 或者增加扫描频率（例如，使用cron任务每分钟扫描一次）

**“赔率差太小”**
- 降低最小赔率差阈值：`--set min_split=0.55`
- 这会提高交易频率，但每次交易的赔率可能较低

**“某些15分钟周期的市场在17小时后到期”**
- Polymarket的`endDate`指的是整个平台的日终时间，而非单个市场的实际收盘时间
- 对于15分钟的加密货币市场（例如“BTC上涨或下跌 - 2月8日晚上11点（ET时间）”，实际收盘时间会在文本中说明，但API中不会显示
- 这是Polymarket的数据限制 — 可以通过增加到期时间窗口（`--expiry 1080`）来解决这个问题，或者使用赔率筛选条件来寻找交易机会

**“外部钱包需要预签名订单”**
- 确保环境变量`WALLET_PRIVATE_KEY`已设置
- SDK会在该变量存在的情况下自动签名交易订单，无需手动操作
- 解决方法：`export WALLET_PRIVATE_KEY=0x<your-polymarket-wallet-private-key>`
- 请勿尝试手动签名订单或修改脚本代码 — SDK会自动处理签名操作

**“余额显示为0美元，但实际上我在Polygon上有USDC”**
- Polymarket使用的是`USDC.e`（一种桥接后的USDC形式，合约地址为`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`）——并非原生USDC
- 如果你最近将USDC桥接到了Polygon，可能需要将`USDC.e`转换回原生USDC后再尝试交易
- 将原生USDC转换回`USDC.e`后重新尝试

**“API密钥无效”**
- 请从simmer.markets/dashboard的SDK标签页获取新的API密钥