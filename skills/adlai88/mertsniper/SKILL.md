---
name: simmer-mertsniper
displayName: Mert Sniper
description: 在 Polymarket 上，存在一种接近到期的“定罪交易”策略。这种策略通常在市场概率严重失衡时进行操作（即市场走势极不明朗）。你可以按主题筛选交易机会，设置投注上限，并且只在对冲那些在截止日期临近时价格波动剧烈的资产时进行交易。
metadata: {"clawdbot":{"emoji":"🎯","requires":{"env":["SIMMER_API_KEY"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
attribution: "Strategy inspired by @mert — https://x.com/mert/status/2020216613279060433"
version: "1.0.0"
---

# Mert Sniper

这是一种用于在Polymarket上进行临近到期日期的“确信交易”（conviction trading）的策略。该策略会在市场赔率严重失衡时进行交易。

> 策略来源：[@mert](https://x.com/mert/status/2020216613279060433) — 可按主题筛选市场；设置投注上限；仅在市场临近到期时进行交易；并且只交易赔率较高的市场。

## 适用场景

> **仅适用于Polymarket**。所有交易均使用真实的USDC在Polymarket上执行。使用`--live`参数可进行真实交易，否则为模拟交易。

当用户希望执行以下操作时，可以使用此策略：
- 在市场临近到期时进行交易（即最后时刻的“确信投注”）
- 按主题筛选市场（例如，仅筛选SOLANA或加密货币市场）
- 设置投注上限（例如，每次投注不超过10美元）
- 仅在市场赔率严重失衡时（例如，赔率为60/40或更高）进行交易
- 运行自动化的到期交易策略

## 设置流程

1. **获取Simmer API密钥**
   - 从simmer.markets/dashboard的SDK标签页获取密钥
   - 将密钥存储在环境变量`SIMMER_API_KEY`中

2. **查看或确认设置**（默认值）
   - 市场筛选：需要扫描的市场（默认：所有市场）
   - 最大投注额：每次交易的最高金额（默认：10美元）
   - 到期时间窗口：距离市场结算的时间（默认：2分钟）
   - 最小赔率差异：最低的赔率差异要求（默认：60/40）

3. **将设置保存到config.json文件或环境变量中**

## 配置参数

| 参数 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| 市场筛选 | `SIMMER_MERT_FILTER` | （所有市场） | 用于筛选市场的标签或关键词（例如：`solana`、`crypto`） |
| 最大投注额 | `SIMMER_MERT_MAX_BET` | 10.00 | 每次交易的最高金额（美元） |
| 到期时间窗口 | `SIMMER_MERT_EXPIRY_MINS` | 2 | 仅交易在N分钟内结算的市场 |
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
- 账户信息：`GET /api/sdk/portfolio`
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
1. 从Simmer API获取活跃市场列表（可选地根据标签/关键词进行筛选）
2. 筛选出在到期时间窗口内结算的市场（默认为2分钟）
3. 检查市场价格的赔率差异——仅当某一方的赔率达到或超过`min_split`（默认为60%）时进行交易
4. 确定交易方向：选择赔率较高的一方进行投注
5. **安全措施**：检查市场是否可能出现价格反转、滑点等问题，并监控市场状态
6. **执行交易**：在赔率较高的一方进行投注，同时确保投注金额不超过设定的上限
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

- **“未找到符合条件的市场”**：
  - 检查你的筛选条件；可以先尝试不使用筛选条件进行测试
  - 可能是因为某些市场暂时不可用（请查看simmer.markets的官方信息）

- **“没有在指定时间内到期的市场”**：
  - 增加到期时间窗口：使用`--expiry 10`（表示10分钟）
  - 或者增加扫描频率（例如，使用cron任务每分钟扫描一次）

- **“赔率差异太小”**：
  - 降低`min_split`的值：使用`--set min_split=0.55`进行设置
  - 这会提高交易频率，但每次交易的“确信度”会降低

- **对于15分钟周期的市场，结果显示“市场将在17小时后结算”**：
  - Polymarket的`endDate`指的是整个平台的日终时间，而非单个市场的具体收盘时间
  - 对于15分钟的加密货币市场（例如“BTC价格涨跌 - 2月8日晚11点（ET时间）”，实际收盘时间会在相关文本中说明，但API中不会显示
  - 这是Polymarket的数据限制——可以尝试增加到期时间窗口（例如`--expiry 1080`），或者使用赔率筛选条件来寻找交易机会

- **“API密钥无效”**：
  - 从simmer.markets/dashboard的SDK标签页重新获取API密钥