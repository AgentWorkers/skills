---
name: polymarket-mert-sniper
displayName: Mert Sniper
description: 在 Polymarket 平台上，存在一种基于“临近到期”的交易策略（即针对即将到期的资产进行交易）。当市场机会极不平衡（即胜算极低或极高）时，这种策略可能会带来较高的风险。建议按主题筛选交易机会，设定投注上限，并且只在对到期日临近的、表现强劲的资产进行交易。
metadata: {"clawdbot":{"emoji":"🎯","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
attribution: "Strategy inspired by @mert — https://x.com/mert/status/2020216613279060433"
version: "1.0.4"
published: true
---
# Mert Sniper

这是一个用于在Polymarket上进行近乎到期的“定罪交易”（conviction trading）的脚本。该脚本会在市场赔率严重失衡时执行交易。

> 策略来源：[@mert](https://x.com/mert/status/2020216613279060433) — 可按主题筛选市场，限制投注金额，等待市场接近到期时间，仅交易赔率较高的交易。

> **这是一个模板。** 默认逻辑（考虑市场到期时间和赔率差异）可以帮助你开始使用该脚本；你可以根据自己的需求添加或修改筛选条件、交易时机规则或市场选择标准。该脚本会处理所有交易相关的细节（如市场发现、交易执行和风险控制），而策略的核心逻辑（即“定罪交易”逻辑）则由用户自行提供。

## 适用场景

> **仅适用于Polymarket。** 所有交易都在Polymarket上使用真实的USDC进行。使用`--live`参数可进行实时交易，否则为模拟交易。

适合以下情况：
- 交易那些即将到期的市场；
- 按主题筛选市场（例如，仅交易SOLANA或加密货币相关市场）；
- 限制单笔投注金额（例如，不超过10美元）；
- 仅在市场赔率严重失衡时（例如，赔率达到60/40或更高）时进行交易；
- 运行自动化的到期交易策略。

## 设置流程

1. **获取Simmer API密钥**
   - 从simmer.markets/dashboard的SDK选项卡中获取API密钥；
   - 将密钥存储在环境变量`SIMMER_API_KEY`中。

2. **配置参数**（或确认默认值）：
   - **市场筛选**：需要扫描的市场（默认：所有市场）；
   - **单笔最大投注额**：每次交易的最大金额（默认10美元）；
   - **到期时间窗口**：距离市场结算还有多少时间（默认2分钟）；
   - **最低赔率差异**：只有当赔率达到至少60/40时才进行交易。

3. **将配置保存到`config.json`文件或环境变量中**。

## 配置参数

| 参数 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| 市场筛选 | `SIMMER_MERT_FILTER` | (all) | 用于筛选市场的标签或关键词（例如：`solana`、`crypto`） |
| 单笔最大投注额 | `SIMMER_MERT_MAX_BET` | 10.00 | 每次交易的最大金额（美元） |
| 到期时间窗口 | `SIMMER_MERT_EXPIRY_MINS` | 2 | 仅交易在N分钟内到期的市场 |
| 最低赔率差异 | `SIMMER_MERT_MIN_SPLIT` | 0.60 | 只有当赔率达到或超过此比例时才进行交易（例如，0.60表示赔率为60/40） |
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
- 财产信息：`GET /api/sdk/portfolio`
- 持有头寸信息：`GET /api/sdk/positions`

## 运行脚本

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

脚本每个周期会执行以下操作：
1. 从Simmer API获取活跃市场列表（可选地根据标签或关键词进行筛选）；
2. 筛选出在到期时间窗口内到期的市场；
3. 检查市场的赔率差异——仅当某一方的赔率达到或超过最低要求（默认60%）时才进行交易；
4. 确定交易方向（选择赔率较高的方）；
5. **风险控制**：检查市场是否可能出现反转、滑点等问题；
6. **执行交易**：在赔率较高的方向上进行交易，且投注金额不超过设定的上限；
7. 报告已扫描、筛选和实际交易的市场信息。

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
  - 检查你的筛选条件；可以先尝试不使用筛选条件进行测试；
  - 可能是因为某些市场暂时不可用，请查看simmer.markets的官方信息。

- **“没有在指定时间内到期的市场”**：
  - 增加到期时间窗口：使用`--expiry 10`（表示10分钟后到期）；
  - 或者增加脚本的执行频率（例如，使用cron任务每分钟执行一次）。

- **“赔率差异太小”**：
  - 降低最低赔率差异阈值：使用`--set min_split=0.55`；
  - 这会提高交易频率，但每次交易的赔率优势会降低。

- **对于15分钟周期的市场，结果显示“在17小时后到期”**：
  - Polymarket的`endDate`指的是整个市场的日终时间，而非单个市场的具体收盘时间；
  - 对于15分钟周期的加密货币市场（例如“BTC上涨或下跌 - 2月8日晚11点（ET）”，实际收盘时间会在文本中显示，但API中不会提供；
  - 这是Polymarket的数据限制，可以尝试增加到期时间窗口（例如`--expiry 1080`），或者使用赔率筛选条件来寻找交易机会。

- **“API密钥无效”**：
  请从simmer.markets/dashboard的SDK选项卡中重新获取API密钥。