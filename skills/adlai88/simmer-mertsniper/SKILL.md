---
name: simmer-mertsniper
displayName: Mert Sniper
description: 在 Polymarket 上，有一种接近到期的“定罪交易”策略。这种策略通常在市场概率严重失衡时进行操作（即交易机会极不均衡）。你可以按主题筛选交易机会，设置投注上限，并且只在截止日期临近时交易那些具有高收益潜力的交易（即那些价格波动较大的资产）。
metadata: {"clawdbot":{"emoji":"🎯","requires":{"env":["SIMMER_API_KEY"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
attribution: "Strategy inspired by @mert — https://x.com/mert/status/2020216613279060433"
version: "1.0.1"
---

# Mert Sniper

这是一种在Polymarket平台上使用的策略，主要用于在合约即将到期时进行交易。该策略专注于那些赔率严重失衡的市场进行交易。

> 策略来源：[@mert](https://x.com/mert/status/2020216613279060433) — 可通过主题进行筛选，限制投注金额，等待合约接近到期时间，仅交易赔率较高的市场。

## 适用场景

> **仅适用于Polymarket平台。** 所有交易均使用真实的USDC在Polymarket上执行。使用`--live`选项可进行实时交易，否则为模拟交易。

当用户希望执行以下操作时，可以使用此策略：
- 交易那些即将到期的合约（最后时刻的投注）
- 按主题筛选市场（例如，仅交易SOLANA或加密货币相关市场）
- 限制投注金额（例如，每次不超过10美元）
- 仅交易赔率严重失衡的市场（例如，赔率至少为60/40）
- 运行自动化的到期交易策略

## 设置流程

1. **获取Simmer API密钥**
   - 从simmer.markets/dashboard的SDK选项卡中获取API密钥
   - 将其存储在环境变量中，命名为`SIMMER_API_KEY`

2. **确认设置**（或使用默认值）
   - 市场筛选：要扫描的市场（默认：所有市场）
   - 最大投注金额：每次交易的最大金额（默认：10美元）
   - 到期时间窗口：距离合约到期还有多少时间（默认：2分钟）
   - 最小赔率差异：最低的赔率差异（默认：60/40）

3. **将设置保存到config.json文件或环境变量中**

## 配置参数

| 参数 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| 市场筛选 | `SIMMER_MERT_FILTER` | (all) | 标签或关键词筛选（例如：`solana`、`crypto`） |
| 最大投注金额 | `SIMMER_MERT_MAX_BET` | 10.00 | 每次交易的最大金额（美元） |
| 到期时间窗口 | `SIMMER_MERT_EXPIRY_MINS` | 2 | 仅交易在N分钟内到期的市场 |
| 最小赔率差异 | `SIMMER_MERT_MIN_SPLIT` | 0.60 | 仅当赔率达到或超过此值时进行交易（例如：0.60表示赔率为60/40） |
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
- 认证方式：`Authorization: Bearer $SIMMER_API_KEY`
- 财产组合信息：`GET /api/sdk/portfolio`
- 持有头寸信息：`GET /api/sdk/positions`

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
1. 从Simmer API获取活跃市场列表（可选地根据标签/关键词进行筛选）
2. 筛选出在到期时间窗口内到期的市场
3. 检查价格赔率差异——仅当某一方的赔率达到或超过最小阈值（默认为60%）时进行交易
4. 确定交易方向：选择赔率较高的那一方进行投注
5. **安全措施**：检查市场状态、价格波动情况以及可能出现的反转风险
6. **执行交易**：在赔率较高的那一方进行投注，同时遵守最大投注金额的限制
7. 报告已扫描、筛选和实际交易的市场列表

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

**“未找到符合条件市场”**
- 检查你的筛选条件——可以先尝试不使用任何筛选条件
- 可能是因为某些市场暂时不可用（请查看simmer.markets的相关信息）

**“没有在指定时间内到期的市场”**
- 增加到期时间窗口：`--expiry 10`（表示10分钟后到期）
- 或者增加扫描频率（例如，使用cron任务每分钟扫描一次）

**“赔率差异太小”**
- 降低最小赔率阈值：`--set min_split=0.55`
- 这会提高交易频率，但每次交易的赔率优势会降低

**“某些市场在17小时后到期”**
- Polymarket的`endDate`指的是整个平台的日终时间，并非单个市场的具体关闭时间
- 对于15分钟周期的加密货币市场（例如“BTC上涨或下跌 - 2月8日晚上11点（ET时间）”，实际的交易结束时间可能在文本中提及，但API中并未提供
- 这是Polymarket的数据限制——可以尝试增加到期时间窗口（`--expiry 1080`），或者使用赔率筛选条件来寻找交易机会

**“API密钥无效”**
- 请从simmer.markets/dashboard的SDK选项卡中重新获取API密钥