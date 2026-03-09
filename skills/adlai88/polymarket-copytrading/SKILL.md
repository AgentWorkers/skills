---
name: polymarket-copytrading
description: 使用 Simmer API 获取 Polymarket 顶级交易者的镜像交易位置（即他们所持有的资产位置）。对来自多个钱包的交易数据进行按规模加权的汇总处理。
metadata:
  author: Simmer (@simmer_markets)
  version: "1.5.4"
  displayName: Polymarket Copytrading
  difficulty: beginner
---# Polymarket复制交易

使用Simmer SDK复制成功交易者的Polymarket持仓。

> **这是一个模板。** 默认逻辑会根据持仓规模进行加权分配来复制大型交易者的持仓——您可以根据自己的钱包选择标准、持仓筛选条件或再平衡规则对其进行修改。该工具会处理所有底层逻辑（如钱包获取、冲突检测和交易执行），而策略的制定则由用户自行完成。

## 何时使用此工具

当用户需要以下操作时，请使用此工具：
- 在Polymarket上复制大型交易者的持仓
- 使用$SIM进行模拟交易（无需真实资金）以测试策略
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

## 寻找大型交易者钱包

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

→ 使用`--wallets`参数运行：
```bash
python copytrading_trader.py --wallets 0x1234...abcd
python copytrading_trader.py --wallets 0xaaa...,0xbbb... --dry-run
```

这是最简单的方法——无需任何设置，只需直接提供钱包地址即可。

## 持久化设置（可选）

为了实现自动化的定期扫描，可以将钱包地址保存在环境变量中：

| 设置 | 环境变量 | 默认值 |
|---------|---------------------|---------|
| 目标钱包 | `SIMMER_COPYTRADING_WALLETS` | （未设置） |
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
- SDK要求每个持仓的最低价值为1.00美元（以避免处理小额交易）

> ⚠️ **谨慎开始：** 先从小额开始（使用`--max-usd 5-10`），并通过`--dry-run`模式运行，了解工具的运行情况后再逐步增加交易金额。

## 工作原理

> **默认情况下，仅执行买入操作。** 如果需要同时卖出大型交易者已平仓的持仓，可以使用`--rebalance`参数；如果仅在他们平仓时卖出持仓，则使用`--whale-exits`参数。

脚本的每个运行周期会：
1. 通过Simmer API从所有目标钱包获取持仓信息
2. 使用加权算法合并这些持仓（持仓规模越大，影响力越大）
3. 检测是否存在持仓冲突（例如，一个钱包持有多头持仓，另一个钱包持有空头持仓），并跳过这些市场
4. 应用前N大持仓的筛选规则，专注于最具投资信心的持仓
5. 从Polymarket自动导入缺失的市场数据
6. 计算再平衡交易以匹配目标持仓比例
7. 通过Simmer SDK执行交易（遵守交易限额）
8. 将结果反馈给用户

## $SIM模拟交易

复制交易支持$SIM模式——使用Simmer的LMSR市场中的模拟资金来复制大型交易者的持仓。无需实际钱包或USDC。

```bash
# Paper trade with $SIM (explicit)
python copytrading_trader.py --venue sim --wallets 0x123... --live

# Auto-detect: if your account has no linked wallet, $SIM is used automatically
python copytrading_trader.py --wallets 0x123... --live
```

在$SIM模式下：
- 交易在Simmer的LMSR市场中以Polymarket的实际价格执行
- 每个市场都有独立的10,000美元$SIM模拟资金
- 持仓情况会在您的Simmer投资组合中显示（来源：`sdk:copytrading`）
- 大型交易者的交易信号仍然来自Polymarket的实时数据

## 运行工具

**执行扫描（默认为模拟运行，不执行交易）：**
```bash
python copytrading_trader.py
```

**执行真实交易：**
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

**全套再平衡模式（包括卖出操作）：**
```bash
python copytrading_trader.py --rebalance
```

**在大型交易者平仓时卖出持仓：**
```bash
python copytrading_trader.py --whale-exits
```

## 报告结果

每次运行后，会向用户提供以下信息：
- 当前配置（目标钱包、前N大持仓、每个钱包的最大持仓数量）
- 获取到的钱包数量及总持仓数量
- 因冲突而跳过的市场
- 执行的交易（及其原因）
- 当前的投资组合持仓情况

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

**用户：“复制交易地址为0x1234...abcd的交易者的持仓”**
→ 运行：`python copytrading_trader.py --wallets 0x1234...abcd`
→ 显示该钱包的持仓情况以及将要执行的交易

**用户：“地址为0x5678...efgh的交易者持有哪些持仓？”**
→ 运行：`python copytrading_trader.py --wallets 0x5678...efgh --dry-run`
→ 显示该钱包的持仓情况（不执行交易）

**用户：“关注这些钱包：0xaaa..., 0xbbb..., 0xccc...”**
→ 运行：`python copytrading_trader.py --wallets 0xaaa...,0xbbb...,0xccc...`
→ 合并所有钱包的持仓情况并显示结果

**用户：“复制交易地址为0x...的交易者的前5大持仓”**
→ 运行：`python copytrading_trader.py --wallets 0x... --top-n 5`

**用户：“我的持仓情况如何？”**
→ 运行：`python copytrading_trader.py --positions`
→ 显示当前的Polymarket持仓情况及盈亏情况

**用户：“显示复制交易配置”**
→ 运行：`python copytrading_trader.py --config`
→ 显示当前设置

**用户：“卖出大型交易者已平仓的持仓”**
→ 运行：`python copytrading_trader.py --whale-exits`
→ 将您的持仓与大型交易者的持仓进行对比，并卖出他们已平仓的持仓

**如何寻找值得跟随的交易者**

常见的方法包括：
1. **排行榜追踪**：查看Polymarket的排行榜，寻找表现稳定的交易者
2. **关注社交媒体上的盈利交易者**：关注在社交媒体上活跃的盈利交易者
3. **特定策略**：关注那些在特定市场（如天气、政治或加密货币领域）有交易记录的交易者

该工具在以下情况下效果最佳：
- 关注2-5个交易者以实现投资分散
- 这些交易者的持仓策略较为一致（避免将高风险交易者与保守型交易者混合）
- 这些交易者交易的品种在Polymarket上都有交易机会

## 故障排除**

**“订单金额太小” / “低于最低要求（5份代币）**
- Polymarket要求每笔订单至少5份代币
- 增加`--max-usd`参数的值或减少`--top-n`参数的值，以专注于更少的持仓

**“未指定钱包地址”**
- 在命令中提供钱包地址，例如：“copytrade 0x1234...”
- 或为自动扫描设置`SIMMER_COPYTRADING_WALLETS`环境变量

**“代理账户中没有USDC余额”**
- 确保您的Polymarket钱包中有USDC，或者使用`--venue sim`参数进行$SIM模拟交易
- 检查钱包是否已关联到simmer.markets dashboard

**“检测到持仓冲突”**
- 两个钱包在同一市场持有相反方向的持仓（例如，一个持有多头，另一个持有空头）
- 持仓比例低于10%的市场会被跳过

**“余额不足”**
- USDC余额不足以完成所有交易
- 减少`SIMMER_COPYTRADING_TOP_N`或`SIMMER_COPYTRADING_MAX_USD`的值

**“无法导入某些市场”**
- 有些市场可能无法导入数据（可能是私有的等原因）
- 这些市场会被自动跳过

**“外部钱包需要预签名订单”**
- 环境变量`WALLET_PRIVATE_KEY`未设置
- 当设置此变量时，SDK会自动完成订单签名——无需手动签名
- 解决方法：`export WALLET_PRIVATE_KEY=0x<your-polymarket-wallet-private-key>`
- 请勿尝试手动签名订单或修改工具代码——SDK会自动处理签名操作

**“余额显示为0美元，但我实际上在Polygon上有USDC”**
- Polymarket使用的是**USDC.e**（桥接后的USDC，合约地址为`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`）——这不是原始的USDC
- 如果您最近将USDC桥接到了Polygon，可能需要将USDC.e转换回原始格式后再尝试

**注意：**