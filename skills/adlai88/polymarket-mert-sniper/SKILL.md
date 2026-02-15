---
name: polymarket-mert-sniper
displayName: Mert Sniper
description: 在 Polymarket 平台上，存在一种基于“临近到期判决”的交易策略。这种策略通常在市场机会极不平衡（即胜算极低或极高）时进行交易。建议通过主题对交易机会进行筛选，设定投注上限，并且只在截止日期临近时交易那些具有较高胜算的分裂（split）事件。
metadata: {"clawdbot":{"emoji":"🎯","requires":{"env":["SIMMER_API_KEY"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
attribution: "Strategy inspired by @mert — https://x.com/mert/status/2020216613279060433"
version: "1.0.3"
published: true
---

# Mert Sniper

这是一种用于在Polymarket上进行“临近到期交易”的策略。该策略专注于在赔率严重失衡时进行交易。

> 策略来源：[@mert](https://x.com/mert/status/2020216613279060433) — 可按主题筛选市场；设置投注上限；仅在市场临近到期时进行交易；并且只交易赔率较高的交易。

## 适用场景

> **仅适用于Polymarket**。所有交易均使用真实的USDC在Polymarket上执行。使用`--live`参数可进行实时交易，否则为模拟交易。

当用户希望执行以下操作时，可以使用此策略：
- 在市场临近到期时进行交易；
- 按主题筛选交易（例如，仅交易SOLANA或加密货币市场）；
- 设置投注上限（例如，每次交易不超过10美元）；
- 仅在市场赔率严重失衡时（例如，赔率达到60/40或更高）进行交易；
- 运行自动化的交易策略。

## 设置流程

1. **获取Simmer API密钥**
   - 从simmer.markets/dashboard的SDK标签页获取API密钥；
   - 将密钥保存为环境变量`SIMMER_API_KEY`。

2. **确认设置**（或使用默认值）：
   - 市场筛选：需要扫描的市场（默认：所有市场）；
   - 最大投注额：每次交易的最高金额（默认10美元）；
   - 到期时间窗口：市场在多长时间内到期（默认2分钟）；
   - 最小赔率差：最低的赔率差（默认60/40）。

3. **将设置保存到config.json文件或环境变量中**。

## 配置参数

| 参数 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| 市场筛选 | `SIMMER_MERT_FILTER` | （所有市场） | 根据标签或关键词筛选市场（例如：`solana`、`crypto`） |
| 最大投注额 | `SIMMER_MERT_MAX_BET` | 10.00 | 每次交易的最高金额（美元） |
| 到期时间窗口 | `SIMMER_MERT_EXPIRY_MINS` | 2 | 仅在市场在N分钟内到期时进行交易 |
| 最小赔率差 | `SIMMER_MERT_MIN_SPLIT` | 0.60 | 仅当赔率达到或超过此值时进行交易（例如，0.60表示赔率为60/40） |
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
- 持仓信息：`GET /api/sdk/positions`

## 运行策略

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
1. 从Simmer API获取活跃市场（可选地根据标签/关键词进行筛选）；
2. 筛选出在到期时间窗口内到期的市场；
3. 检查市场的赔率差——仅当某一方的赔率达到最小赔率差（默认60%）时进行交易；
4. 确定交易方向：选择赔率较高的一方进行投注；
5. **安全措施**：检查市场是否可能出现价格反转、滑点等问题；
6. **执行交易**：在赔率较高的一方进行投注，且投注金额不超过设定的上限；
7. 报告已扫描、筛选和实际交易的市场列表。

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

## 故障排除

- **“未找到市场”**：
  - 检查筛选条件；可以先尝试不使用筛选条件进行测试；
  - 可能是某些市场暂时不可用（请查看simmer.markets的相关信息）。

- **“没有在指定时间内到期的市场”**：
  - 增加到期时间窗口：使用`--expiry 10`（例如，设置为10分钟）；
  - 或者增加扫描频率（例如，使用cron任务每分钟扫描一次）。

- **“赔率差太小”**：
  - 降低最小赔率差：使用`--set min_split=0.55`；
  - 这会提高交易频率，但每次交易的赔率差可能较小。

- **“某些市场在17小时后到期”**：
  - Polymarket的`endDate`表示整个市场的日终时间，而非单个市场的具体收盘时间；
  - 对于15分钟周期的加密货币市场（例如“BTC上涨或下跌 - 2月8日晚11点（ET时间）”，实际收盘时间会在文本中说明，但API中不会显示；
  - 这是Polymarket的数据限制——可以通过增加到期时间窗口（`--expiry 1080`）来解决这个问题，或者使用赔率差筛选条件来寻找交易机会。

- **“API密钥无效”**：
  - 从simmer.markets/dashboard的SDK标签页重新获取API密钥。