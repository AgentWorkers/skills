---
name: polymarket-mert-sniper
displayName: Mert Sniper
description: 在 Polymarket 平台上，存在一种接近到期的“定罪交易”策略（conviction trading）。这种策略通常在市场情况极度失衡（即赔率严重偏向某一方）时进行操作。你可以按主题筛选交易机会，限制自己的投注金额，并且只交易那些在截止日期临近时出现大幅价格波动（split）的资产。
metadata: {"clawdbot":{"emoji":"🎯","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
attribution: "Strategy inspired by @mert — https://x.com/mert/status/2020216613279060433"
version: "1.0.6"
published: true
---
# Mert Sniper

这是一个用于在Polymarket上进行交易策略的工具，专注于在合约即将到期时进行交易（尤其是当赔率严重倾斜时）。该策略由[@mert](https://x.com/mert/status/2020216613279060433)设计，可通过主题进行筛选，并限制每次交易的金额。用户可以自定义过滤条件、交易时机和市场选择标准。

**使用说明：**

- **仅支持Polymarket**：所有交易均在Polymarket上使用真实的USDC进行。
- **使用`--live`参数可进行实时交易，默认为模拟测试模式。

**适用场景：**
- 交易那些即将到期的合约；
- 按主题筛选交易（例如仅交易SOLANA或加密货币合约）；
- 限制每次交易的金额（例如不超过10美元）；
- 仅在市场赔率严重倾斜时（例如60/40或更高）进行交易；
- 运行自动化的交易策略。

**设置流程：**

1. **获取Simmer API密钥**：
   - 从simmer.markets/dashboard的SDK标签页获取API密钥，并将其存储为`SIMMER_API_KEY`环境变量。
2. **获取钱包私钥**（用于实时交易）：
   - 这是用户在Polymarket上的钱包私钥（用于存储USDC）。将其存储为`WALLET_PRIVATE_KEY`环境变量。
   - SDK会使用此密钥在客户端自动签署交易订单，无需手动操作。
3. **配置参数**：
   - **市场筛选**：指定需要扫描的市场（默认为所有市场）；
   - **最大交易金额**：每次交易的最大金额（默认为10美元）；
   - **到期时间窗口**：设定交易发生的最晚时间（默认为2分钟）；
   - **最小赔率阈值**：只有当赔率达到或超过此阈值（例如60/40）时才进行交易。

4. **将配置保存到config.json文件或环境变量中**。

**配置项说明：**

| 配置项 | 环境变量 | 默认值 | 说明 |
|---------|---------------------|---------|-------------|
| 市场筛选 | `SIMMER_MERT_FILTER` | (all) | 用于筛选市场的标签或关键词（例如`solana`、`crypto`） |
| 最大交易金额 | `SIMMER_MERT_MAX_BET` | 10.00 | 每次交易的最高金额（美元） |
| 到期时间窗口 | `SIMMER_MERT_EXPIRY_MINS` | 2 | 仅交易在N分钟内到期的市场 |
| 最小赔率阈值 | `SIMMER_MERT_MIN_SPLIT` | 0.60 | 只有当赔率达到或超过此阈值时才进行交易 |
| 每次扫描的最大交易次数 | `SIMMER_MERT_MAX_TRADES` | 5 | 每次扫描的最大交易次数 |
| 智能资金分配比例 | `SIMMER_MERT_SIZING_PCT` | 0.05 | 每笔交易的资金分配比例（百分比） |

**常用命令：**
（此处应列出与该技能相关的命令，但原文未提供具体命令，可根据实际需求补充。）

**API参考：**
- 基础URL：`https://api.simmer.markets`
- 认证方式：`Authorization: Bearer $SIMMER_API_KEY`
- 财产信息：`GET /api/sdk/portfolio`
- 持仓信息：`GET /api/sdk/positions`

**运行该技能的步骤：**
（此处应列出运行脚本的详细步骤，但原文未提供，可根据实际需求补充。）

**工作原理：**
- 脚本每个周期会：
  1. 从Simmer API获取活跃市场（可选地根据标签/关键词进行筛选）；
  2. 筛选出在到期时间窗口内到期的市场；
  3. 检查价格赔率，仅当某一方的赔率达到最小阈值时才进行交易；
  4. 确定交易方向（选择赔率较高的那一方）；
  5. 实施交易（金额上限为最大交易金额）；
  6. 报告扫描到的市场、筛选结果及实际交易情况。

**示例输出：**
（此处应展示示例输出结果，但原文未提供。）

**故障排除：**

- **“未找到市场”**：检查筛选条件；可以先尝试不使用筛选条件进行测试。
- **市场可能不可用**：请检查simmer.markets网站。
- **“没有在指定时间内到期的市场”**：增加到期时间窗口（例如`--expiry 10`）；或者增加扫描频率（例如使用cron任务每分钟扫描一次）。
- **赔率阈值设置过低**：降低最小赔率阈值（例如`--set min_split=0.55`）；这样交易频率会增加，但每次交易的确定性会降低。
- **对于15分钟周期的市场，实际结束时间可能与API显示不同**：Polymarket的`endDate`是指整个市场的结束时间，而非单个合约的结束时间。对于15分钟的加密货币市场（例如“BTC Up or Down - Feb 8, 11PM ET”），实际结束时间可能在文本中提及，但API中不会显示。解决方法是将到期时间窗口设置为更长的时间（例如`--expiry 1080`），或者使用赔率阈值来寻找交易机会。
- **“外部钱包需要预先签署的交易订单”**：确保`WALLET_PRIVATE_KEY`已正确设置。SDK会自动签署交易订单，无需手动操作。
- **余额显示为0美元，但实际上有USDC**：Polymarket使用的是`USDC.e`（一种桥接后的USDC形式，合约地址为`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`）。如果最近将USDC桥接到Polygon网络，可能需要将`USDC.e`转换为原生USDC后再尝试交易。
- **API密钥无效**：请从simmer.marketsdashboard的SDK标签页获取新的API密钥。