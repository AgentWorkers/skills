---
name: polymarket-copytrading
displayName: Polymarket Copytrading
description: 使用 Simmer API 获取 Polymarket 上顶级交易者的持仓信息，并对多个钱包的持仓数据进行加权汇总。
metadata: {"clawdbot":{"emoji":"🐋","requires":{"env":["SIMMER_API_KEY","WALLET_PRIVATE_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false}}
authors:
  - Simmer (@simmer_markets)
version: "1.3.7"
published: true
---
# Polymarket 复制交易

使用 Simmer SDK 模拟成功交易者的持仓策略。

> **这是一个模板。** 默认逻辑会按照资产规模进行加权分配来复制大资金交易者的持仓——您可以根据自己的钱包选择标准、持仓筛选条件或再平衡规则对其进行调整。该工具负责处理所有底层逻辑（如钱包获取、冲突检测和交易执行），而您的代理程序则负责生成具体的交易策略。

## 适用场景

当用户希望执行以下操作时，可以使用此工具：
- 复制 Polymarket 上大资金交易者的持仓
- 查看某个钱包持有的持仓情况
- 关注特定的交易者
- 查看他们的复制交易持仓

## 快速命令

```bash
# Check account balance and positions
python scripts/status.py

# Detailed position list
python scripts/status.py --positions
```

**API 参考：**
- 基本 URL：`https://api.simmer.markets`
- 认证：`Authorization: Bearer $SIMMER_API_KEY`
- 投资组合：`GET /api/sdk/portfolio`
- 持仓情况：`GET /api/sdk/positions`

## 寻找大资金交易者

- **[predicting.top](https://predicting.top)** — Polymarket 上表现最佳的交易者排行榜（包含钱包地址）
- **[alphawhale.trade](https://alphawhale.trade)** — 用于复制和跟踪表现优异的交易者的工具
- **Polymarket Leaderboard** — 官方排名（需要账户）

## 快速入门（临时使用）

**用户直接在聊天中提供钱包地址：**
```
User: "Copytrade this wallet: 0x1234...abcd"
User: "What positions does 0x5678...efgh have?"
User: "Follow these whales: 0xaaa..., 0xbbb..."
```

→ 使用 `--wallets` 标志运行脚本：
```bash
python copytrading_trader.py --wallets 0x1234...abcd
python copytrading_trader.py --wallets 0xaaa...,0xbbb... --dry-run
```

这是最简单的方法——无需任何设置，只需直接提供钱包地址即可。

## 持久化设置（可选）

为了实现自动化的定期扫描，可以将钱包地址保存到环境变量中：

| 设置 | 环境变量 | 默认值 |
|---------|---------------------|---------|
| 目标钱包地址 | `SIMMER_COPYTRADING_WALLETS` | （未设置） |
| 前 N 个持仓 | `SIMMER_COPYTRADING_TOP_N` | 自动计算 |
- 每个持仓的最大金额 | `SIMMER_COPYTRADING_MAX_USD` | 50 美元 |
- 每次运行的最大交易数量 | `SIMMER_COPYTRADING_MAX_TRADES` | 10 笔 |

**前 N 个持仓的自动计算规则（未指定时）：**
- 账户余额 < 50 美元：显示前 5 个持仓
- 账户余额 50-200 美元：显示前 10 个持仓
- 账户余额 200-500 美元：显示前 25 个持仓
- 账户余额 > 500 美元：显示前 50 个持仓

**Polymarket 的限制：**
- 每笔订单至少需要持有 5 枚代币
- SDK 要求每个持仓的最低价值为 1.00 美元（以过滤小额交易）

> ⚠️ **谨慎起步：** 先从小额交易开始（使用 `--max-usd 5-10`），并通过 `--dry-run` 测试工具的运行情况，再逐步增加交易金额。

## 工作原理

脚本每个周期会执行以下操作：
1. 通过 Simmer API 从所有目标钱包中获取持仓信息
2. 使用加权算法合并这些持仓数据（资金越多的钱包影响越大）
3. 检测持仓冲突（例如，一个钱包持有多头头寸，另一个钱包没有），并跳过存在冲突的市场
4. 应用前 N 个持仓的筛选规则，专注于最具投资信心的持仓
5. 自动从 Polymarket 获取缺失的市场数据
6. 计算所需的再平衡交易量
7. 通过 Simmer SDK 执行交易（遵守平台的交易限额）
8. 将结果反馈给用户

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

**全量再平衡模式（包括卖出操作）：**
```bash
python copytrading_trader.py --rebalance
```

**在大资金交易者平仓时卖出相应持仓：**
```bash
python copytrading_trader.py --whale-exits
```

## 结果报告

每次运行后，会向用户发送以下信息：
- 当前配置（目标钱包地址、前 N 个持仓、每个持仓的最大金额）
- 获取到的钱包数量及总持仓数量
- 因冲突被跳过的市场
- 执行的交易（或未执行的交易及其原因）
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

## 示例对话**

**用户：“复制交易者 0x1234...abcd”的持仓情况”**
→ 运行：`python copytrading_trader.py --wallets 0x1234...abcd`
→ 显示该钱包的持仓情况以及即将执行的交易

**用户：“0x5678...efgh 持有哪些持仓？”**
→ 运行：`python copytrading_trader.py --wallets 0x5678...efgh --dry-run`
→ 显示该钱包的持仓情况（不执行交易）

**用户：“关注这些钱包：0xaaa..., 0xbbb..., 0xccc...”**
→ 运行：`python copytrading_trader.py --wallets 0xaaa...,0xbbb...,0xccc...`
→ 合并所有钱包的持仓信息并显示结果

**用户：“复制交易者 0x... 的前 5 个持仓”**
→ 运行：`python copytrading_trader.py --wallets 0x... --top-n 5`

**用户：“我的持仓表现如何？”**
→ 运行：`python copytrading_trader.py --positions`
→ 显示当前在 Polymarket 上的持仓情况及盈亏情况

**用户：“显示复制交易配置”**
→ 运行：`python copytrading_trader.py --config`
→ 显示当前的设置

**用户：“卖出大资金交易者已平仓的持仓”**
→ 运行：`python copytrading_trader.py --whale-exits`
→ 将用户的持仓与交易者的持仓进行对比，并卖出他们已平仓的代币

**用户：“进行全面再平衡以匹配大资金交易者的持仓”**
→ 运行：`python copytrading_trader.py --rebalance`
→ 包括买入和卖出操作，以匹配交易者的持仓策略

## 如何寻找值得关注的交易者

常见的方法包括：
1. **排行榜跟踪**：查看 Polymarket 的排行榜，寻找表现稳定的交易者
2. **关注社交媒体上的盈利交易者**：关注在社交媒体上活跃的盈利交易者
3. **特定策略**：关注那些在特定市场（如天气、政治或加密货币领域）有交易习惯的交易者

**最佳使用场景：**
- 关注 2-5 个钱包以实现投资多样化
- 选择持仓策略相似的交易者（避免同时关注高风险和保守型交易者）
- 确保所选钱包在 Polymarket 上有可交易的资产

## 常见问题及解决方法**

- **“订单金额太少” / “低于最低要求（5 枚代币）”**
  - Polymarket 要求每笔订单至少持有 5 枚代币
  - 增加 `--max-usd` 的值或减少 `--top-n` 的值，以集中关注更少的持仓

- **未指定钱包地址**
  - 在命令中提供钱包地址，例如：`copytrading_trader.py --wallets 0x1234...`
  - 或为自动扫描设置环境变量 `SIMMER_COPYTRADING_WALLETS`

- **代理程序没有 USDC 账户余额**
  - 确保您的 Polymarket 钱包中有 USDC
  - 检查钱包是否已在 simmer.markets/dashboard 中关联

- **检测到持仓冲突**
  - 两个钱包在同一市场持有相反的头寸（例如，一个持有多头，另一个持有空头）
  - 账户在该市场的净持仓比例低于 10% 的市场会被跳过

- **账户余额不足**
  - USDC 不足以完成所有交易
  - 减少 `SIMMER_COPYTRADING_TOP_N` 或 `SIMMER_COPYTRADING_MAX_USD` 的值

- **无法导入某些市场数据**
  - 有些市场可能无法导入数据（可能是私有的或受限制的）
  - 这些市场会被自动跳过

- **外部钱包需要预签名订单**
  - 环境变量 `WALLET_PRIVATE_KEY` 未设置
  - 当设置此变量后，SDK 会自动完成订单签名——无需手动操作
  - 解决方法：`export WALLET_PRIVATE_KEY=0x<your-polymarket-wallet-private-key>`
  - 请勿尝试手动签名订单或修改脚本代码

- **账户余额显示为 0 美元，但实际上我有 USDC”**
  - Polymarket 使用的是 **USDC.e**（桥接后的 USDC，合约地址为 `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`）——并非原生 USDC
  - 如果您最近将 USDC 桥接到了 Polygon，可能需要将桥接后的 USDC 转换为原生 USDC，然后再尝试