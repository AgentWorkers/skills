---
name: polymarket-mert-sniper
description: 在 Polymarket 上，存在一种接近到期的“定罪交易”策略（conviction trading）。这种交易方式会在市场概率严重失衡时进行。你可以按主题筛选交易机会，设定投注上限，并且只在对冲那些在截止日期临近时出现大幅波动（split）的资产上进行交易。
metadata:
  author: Simmer (@simmer_markets)
  version: "1.0.7"
  displayName: Mert Sniper
  difficulty: advanced
  attribution: Strategy inspired by @mert — https://x.com/mert/status/2020216613279060433
---# Mert Sniper

这是一个用于在Polymarket上进行临近到期交易策略的工具。该策略专注于在赔率严重倾斜时进行交易。

> 策略来源：[@mert](https://x.com/mert/status/2020216613279060433) — 可按主题筛选市场，限制投注金额，并仅在临近到期时进行交易。

> **这是一个模板。** 默认逻辑（到期时间 + 赔率筛选）可以帮助你开始使用该工具 — 你可以根据自己的需求添加自定义筛选条件、交易时机规则或市场选择标准。该工具会处理所有的市场发现、交易执行和风险控制等细节。

## 适用场景

> **仅适用于Polymarket。** 所有交易均在Polymarket上使用真实的USDC进行。使用`--live`选项可进行实时交易，否则为模拟交易。

当你想要执行以下操作时，可以使用该工具：
- 交易那些即将到期的市场（最后时刻的投注）
- 按主题筛选市场（例如，仅交易SOLANA或加密货币市场）
- 限制投注金额（例如，每次不超过10美元）
- 仅在赔率严重倾斜时进行交易（例如，赔率至少为60/40）
- 运行自动化的临近到期交易策略

## 设置流程

1. **获取Simmer API密钥**
   - 从simmer.markets/dashboard的SDK标签页获取API密钥
   - 将其存储在环境变量`SIMMER_API_KEY`中

2. **获取钱包私钥**（用于实时交易）
   - 这是你的Polymarket钱包的私钥（用于存储USDC）
   - 将其存储在环境变量`WALLET_PRIVATE_KEY`中
   - SDK会使用该私钥在客户端自动签署交易订单，无需手动操作

3. **配置设置**（或确认默认值）
   - 市场筛选：要扫描的市场（默认：所有市场）
   - 每笔交易的最大投注金额（默认：10美元）
   - 到期时间窗口：距离市场结算的时间（默认：2分钟）
   - 最小赔率差：最低的赔率倾斜度（默认：60/40）

4. **将设置保存到config.json文件或环境变量中**

## 配置参数

| 参数 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| 市场筛选 | `SIMMER_MERT_FILTER` | （所有市场） | 根据标签或关键词筛选市场（例如：`solana`、`crypto`） |
| 每笔交易的最大投注金额 | `SIMMER_MERT_MAX_BET` | 10.00 | 每笔交易的最大金额（美元） |
| 到期时间窗口 | `SIMMER_MERT_EXPIRY_MINS` | 2 | 仅交易在N分钟内到期的市场 |
| 最小赔率差 | `SIMMER_MERT_MIN_SPLIT` | 0.60 | 仅当赔率差大于或等于此值时进行交易（例如：0.60表示赔率为60/40） |
| 每次扫描的最大交易次数 | `SIMMER_MERT_MAX_TRADES` | 5 | 每次扫描周期内的最大交易次数 |
| 智能投注比例 | `SIMMER_MERT_SIZING_PCT` | 0.05 | 每笔交易的投注金额占余额的百分比 |

## 快速命令

```bash
# Check account balance and positions
python scripts/status.py

# Detailed position list
python scripts/status.py --positions
```

**API参考：**
- 基础URL：`https://api.simmer.markets`
- 认证方式：`Authorization: Bearer $SIMMER_API_KEY`
- 财产概况：`GET /api/sdk/portfolio`
- 持仓情况：`GET /api/sdk/positions`

## 运行该工具

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
3. 检查市场的价格赔率差 — 仅在市场某一方的赔率达到最小要求（默认为60%）时进行交易
4. 确定交易方向：选择赔率较高的那一方进行投注
5. **风险控制**：检查市场可能出现的变化、滑点等情况
6. **执行交易**：在赔率较高的那一方进行投注，同时限制投注金额不超过最大限额
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
- 检查你的筛选条件 — 先尝试不使用任何筛选条件进行查询
- 可能是因为某些市场暂时不可用（请查看simmer.markets的官方信息）

**“没有在指定时间内到期的市场”**
- 增加到期时间窗口：`--expiry 10`（例如设置为10分钟）
- 或者增加扫描频率（例如使用cron任务，每分钟扫描一次）

**“赔率差太小”**
- 降低最小赔率差阈值：`--set min_split=0.55`
- 这会提高交易频率，但每次交易的投注金额可能会减少

**“某些市场的到期时间为17小时”**
- Polymarket的“endDate”是指整个平台的日终时间，而非单个市场的实际收盘时间
- 对于15分钟周期的市场（例如“BTC价格涨跌 - 2月8日晚11点（美国东部时间）”，实际收盘时间会在文本中说明，但API中不会显示
- 这是Polymarket的数据限制 — 可以通过增加到期时间窗口（`--expiry 1080`）来解决问题，或者使用赔率筛选条件来寻找交易机会

**“外部钱包需要预先签署的交易订单”**
- 确保环境变量`WALLET_PRIVATE_KEY`已设置
- SDK会在该变量存在的情况下自动签署交易订单，无需手动操作
- 解决方法：`export WALLET_PRIVATE_KEY=0x<你的Polymarket钱包私钥>`
- 请勿尝试手动签署订单或修改脚本代码 — SDK会自动处理这些操作

**“余额显示为0美元，但实际上我在Polygon上有USDC”**
- Polymarket使用的是`USDC.e`（一种桥接后的USDC形式，合约地址为`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`）——并非原生USDC
- 如果你最近将USDC桥接到了Polygon，可能需要先将USDC.e转换回原生USDC后再进行交易
- 将原生USDC转换回USDC.e后重新尝试

**“API密钥无效”**
- 从simmer.markets/dashboard的SDK标签页重新获取API密钥