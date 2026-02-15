---
name: simmer-copytrading
displayName: Polymarket Copytrading
description: 使用 Simmer API 获取 Polymarket 顶部交易者的持仓位置信息，并对多个钱包的持仓数据进行加权汇总。
metadata: {"clawdbot":{"emoji":"🐋","requires":{"env":["SIMMER_API_KEY"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
version: "1.3.0"
---

# Polymarket复制交易

使用Simmer SDK复制成功交易者的持仓。

## 何时使用此技能

当用户希望执行以下操作时，可以使用此技能：
- 复制Polymarket上大型交易者的持仓
- 查看某个钱包的持仓情况
- 关注特定的交易者
- 查看他们的复制交易持仓

## 快速命令

```bash
# Check account balance and positions
python scripts/status.py

# Detailed position list
python scripts/status.py --positions
```

**API参考：**
- 基本URL：`https://api.simmer.markets`
- 认证：`Authorization: Bearer $SIMMER_API_KEY`
- 投资组合：`GET /api/sdk/portfolio`
- 持仓情况：`GET /api/sdk/positions`

## 查找大型交易者钱包

- **[predicting.top](https://predicting.top)** — Polymarket顶级交易者的排行榜（包含钱包地址）
- **[alphawhale.trade](https://alphawhale.trade)** — 用于复制和跟踪表现优异的交易者的工具
- **Polymarket排行榜** — 官方排名（需要账户）

## 快速入门（临时使用）

**用户直接在聊天中提供钱包地址：**
```
User: "Copytrade this wallet: 0x1234...abcd"
User: "What positions does 0x5678...efgh have?"
User: "Follow these whales: 0xaaa..., 0xbbb..."
```

→ 使用`--wallets`参数运行脚本：
```bash
python copytrading_trader.py --wallets 0x1234...abcd
python copytrading_trader.py --wallets 0xaaa...,0xbbb... --dry-run
```

这是最简单的方法——无需任何设置，只需直接提供钱包地址即可。

## 持久化设置（可选）

为了实现自动化的定期扫描，可以将钱包地址保存在环境变量中：

| 设置 | 环境变量 | 默认值 |
|---------|---------------------|---------|
| 目标钱包 | `SIMMER_COPYTRADING_WALLETS` | （未指定） |
| 前N大持仓 | `SIMMER_COPYTRADING_TOP_N` | 自动计算 |
- 每个持仓的最大金额 | `SIMMER_COPYTRADING_MAX_USD` | 50美元 |
- 每次运行的最大交易数量 | `SIMMER_COPYTRADING_MAX_TRADES` | 10笔 |

**前N大持仓的自动计算规则（未指定时）：**
- 账户余额 < 50美元：前5大持仓
- 账户余额 50-200美元：前10大持仓
- 账户余额 200-500美元：前25大持仓
- 账户余额 500美元以上：前50大持仓

**Polymarket的限制：**
- 每笔订单至少需要5份代币
- SDK要求每个持仓的价值至少为1.00美元（以过滤微不足道的持仓）

> ⚠️ **谨慎开始：** 先从小额开始（使用`--max-usd 5-10`），并通过`--dry-run`模式运行脚本，了解其运行情况后再逐步增加交易金额。

## 工作原理

脚本每个周期会执行以下操作：
1. 通过Simmer API从所有目标钱包获取持仓信息
2. 使用按规模加权的算法合并这些数据（钱包规模越大，影响力越大）
3. 检测持仓冲突（例如，一个钱包持有多头头寸，另一个钱包没有），并跳过这些市场
4. 应用前N大持仓的筛选规则，专注于置信度最高的持仓
5. 自动从Polymarket导入缺失的市场数据
6. 计算重新平衡所需的交易量
7. 通过Simmer SDK执行交易（遵守交易限额）
8. 将结果报告给用户

## 运行脚本

**执行扫描（默认为模拟运行，不进行实际交易）：**
```bash
python copytrading_trader.py
```

**执行实际交易：**
```bash
python copytrading_trader.py --live
```

**仅查看持仓情况：**
```bash
python copytrading_trader.py --positions
```

**查看当前配置：**
```bash
python copytrading_trader.py --config
```

**为单次运行指定特定钱包：**
```bash
python copytrading_trader.py --wallets 0x123...,0x456...
```

**全量重新平衡模式（包括卖出操作）：**
```bash
python copytrading_trader.py --rebalance
```

**在大型交易者平仓时卖出：**
```bash
python copytrading_trader.py --whale-exits
```

## 结果报告

每次运行后，会向用户发送以下信息：
- 当前配置（目标钱包、前N大持仓、每个持仓的最大金额）
- 获取到的钱包数量及总持仓数量
- 因持仓冲突而跳过的市场
- 执行的交易（或未执行的交易及其原因）
- 用户当前的Polymarket持仓情况

**示例输出：**
```
🐋 Copytrading Scan Complete

Configuration:
• Following 2 wallets
• Top 10 positions, max $50 each
• Balance: $250.00 USDC

Fetched positions:
• 0x1234...abcd: 15 positions
• 0x5678...efgh: 22 positions
• Combined: 28 unique markets
• Conflicts skipped: 2

Top 10 by allocation:
1. "Will BTC hit $100k?" - 18.5% → BUY YES
2. "Trump pardons X?" - 12.3% → BUY NO
3. "Fed rate cut Jan?" - 9.8% → Already held
...

Trades executed: 4 buys ($180 total)
• Bought 45 YES shares on "Will BTC hit $100k?" @ $0.82
• Bought 120 NO shares on "Trump pardons X?" @ $0.15
...

Next scan in 4 hours.
```

## 示例对话

**用户：“复制交易者0x1234...abcd的持仓”**
→ 运行：`python copytrading_trader.py --wallets 0x1234...abcd`
→ 报告该钱包的持仓情况以及将执行的交易

**用户：“0x5678...efgh持有哪些持仓？”**
→ 运行：`python copytrading_trader.py --wallets 0x5678...efgh --dry-run`
→ 显示该钱包的持仓情况（不执行交易）

**用户：“关注这些钱包：0xaaa..., 0xbbb..., 0xccc...”**
→ 运行：`python copytrading_trader.py --wallets 0xaaa...,0xbbb...,0xccc...`
→ 合并所有钱包的持仓情况并报告结果

**用户：“复制交易者0x...的前5大持仓”**
→ 运行：`python copytrading_trader.py --wallets 0x... --top-n 5`

**用户：“我的持仓表现如何？”**
→ 运行：`python copytrading_trader.py --positions`
→ 显示用户在Polymarket上的当前持仓及盈亏情况

**用户：“显示复制交易配置”**
→ 运行：`python copytrading_trader.py --config`
→ 显示当前设置

**用户：“卖出大型交易者平仓的持仓”**
→ 运行：`python copytrading_trader.py --whale-exits`
→ 将用户的持仓与大型交易者的持仓进行比较，并卖出他们已平仓的持仓

**用户：“进行全量重新平衡以匹配大型交易者的持仓”**
→ 运行：`python copytrading_trader.py --rebalance`
→ 包括买入和卖出操作，以匹配大型交易者的持仓配置

## 如何找到值得关注的大型交易者钱包

常见的方法包括：
1. **排行榜跟踪**：查看Polymarket的排行榜，寻找表现稳定的交易者
2. **关注社交媒体上的盈利交易者**：关注在社交媒体上表现优异的交易者
3. **特定策略**：关注那些在特定市场（如天气、政治或加密货币领域）有交易习惯的交易者

**最佳使用场景：**
- 关注2-5个钱包以实现投资多样化
- 确保所关注的钱包具有相似的交易策略（避免将高风险和保守型交易者混在一起）
- 确保钱包交易的品种在Polymarket平台上可用

## 常见问题及解决方法**

**“订单金额太少” / “低于最低要求（5份代币）**
- Polymarket要求每笔订单至少5份代币
- 增加`--max-usd`参数的值或减少`--top-n`参数，以便专注于更少的持仓

**“未指定钱包地址”**
- 在命令中提供钱包地址，例如：`copytrading_trader.py --wallets 0x1234...`
- 或为自动扫描设置`SIMMER_COPYTRADING_WALLETS`环境变量

**“代理账户没有USDC余额”**
- 确保你的Polymarket钱包中有足够的USDC
- 检查钱包是否已关联到simmer.markets dashboard

**“检测到持仓冲突”**
- 两个钱包在同一市场持有相反方向的头寸（例如，一个持有多头，另一个持有空头）
- 持仓净比例低于10%的市场会被自动跳过

**“余额不足”**
- USDC余额不足以完成所有交易
- 减少`SIMMER_COPYTRADING_TOP_N`或`SIMMER_COPYTRADING_MAX_USD`的值

**“无法导入某些市场数据”**
- 有些市场可能无法导入数据（可能是私有的或其他原因）
- 这些市场会自动被跳过