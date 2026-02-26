---
name: polymarket-copytrading
displayName: Polymarket Copytrading
description: 通过 Simmer API 获取 Polymarket 顶级交易者的镜像交易位置（mirror positions）。对来自多个钱包的交易数据进行按规模加权的聚合（size-weighted aggregation）。
metadata: {"clawdbot":{"emoji":"🐋","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false,"automaton":{"managed":true,"entrypoint":"copytrading_trader.py"}}}
authors:
  - Simmer (@simmer_markets)
version: "1.4.0"
published: true
---
# Polymarket 复制交易

使用 Simmer SDK 复制 Polymarket 上表现优异的交易者的持仓。

> **这是一个模板。** 默认逻辑会根据持仓金额的权重来复制大型交易者的持仓——您可以根据自己的钱包选择标准、持仓筛选条件或再平衡规则对其进行修改。该工具会处理所有底层逻辑（如钱包获取、冲突检测和交易执行），而策略的制定则由用户自行完成。

## 何时使用此工具

当用户需要执行以下操作时，请使用此工具：
- 复制 Polymarket 上大型交易者的持仓
- 使用模拟资金（$SIM）进行模拟交易以测试策略
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

**API 参考：**
- 基础 URL：`https://api.simmer.markets`
- 认证：`Authorization: Bearer $SIMMER_API_KEY`
- 投资组合：`GET /api/sdk/portfolio`
- 持仓情况：`GET /api/sdk/positions`

## 寻找大型交易者钱包

- **[predicting.top](https://predicting.top)** — Polymarket 上表现最好的交易者的排行榜（包含钱包地址）
- **[alphawhale.trade](https://alphawhale.trade)** — 用于复制和跟踪表现优异的交易者的工具
- **Polymarket Leaderboard** — 官方排行榜（需要账户）

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

为了实现自动化的定期扫描，可以将钱包地址保存在环境变量中：

| 设置 | 环境变量 | 默认值 |
|---------|---------------------|---------|
| 目标钱包 | `SIMMER_COPYTRADING_WALLETS` | （未设置） |
| 前 N 个持仓 | `SIMMER_COPYTRADING_TOP_N` | 自动计算 |
- 每个持仓的最大金额 | `SIMMER_COPYTRADING_MAX_USD` | 50 美元 |
- 每次运行的最大交易数量 | `SIMMER_COPYTRADING_MAX_TRADES` | 10 笔 |

**前 N 个持仓的自动计算规则（未指定时）：**
- 账户余额 < 50 美元：前 5 个持仓
- 账户余额 50-200 美元：前 10 个持仓
- 账户余额 200-500 美元：前 25 个持仓
- 账户余额 500 美元以上：前 50 个持仓

**Polymarket 的限制：**
- 每笔订单至少需要 5 枚代币
- SDK 要求每个持仓的最低价值为 1.00 美元（以过滤小额持仓）

> ⚠️ **谨慎开始：** 先从小额开始尝试（使用 `--max-usd 5-10`），并通过 `--dry-run` 选项了解工具的运行情况，再逐步增加交易金额。

## 工作原理

脚本每个周期会执行以下操作：
1. 通过 Simmer API 从所有目标钱包中获取持仓信息
2. 使用权重聚合方法合并这些持仓数据（持仓金额越大，影响力越大）
3. 检测持仓冲突（例如，一个钱包持有多头头寸，另一个钱包没有），并跳过存在冲突的市场
4. 应用前 N 个持仓的筛选规则，专注于最具投资价值的持仓
5. 自动从 Polymarket 获取缺失的市场数据
6. 计算再平衡交易以匹配目标持仓配置
7. 通过 Simmer SDK 执行交易（遵守平台的交易限额）
8. 将结果反馈给用户

## $SIM 模拟交易

复制交易支持 $SIM 模式——使用模拟资金在 Simmer 的 LMSR 市场上复制交易者的持仓。无需实际钱包或 USDC。

```bash
# Paper trade with $SIM (explicit)
python copytrading_trader.py --venue simmer --wallets 0x123... --live

# Auto-detect: if your account has no linked wallet, $SIM is used automatically
python copytrading_trader.py --wallets 0x123... --live
```

在 $SIM 模式下：
- 交易在 Simmer 的 LMSR 市场上以 Polymarket 的实际价格执行
- 每个市场都会分配 10,000 美元的模拟资金
- 持仓情况会在用户的 Simmer 投资组合中显示（来源：`sdk:copytrading`）
- 交易信号仍然来自 Polymarket 的实际数据

## 运行工具

**执行扫描（默认为模拟运行，不执行交易）：**
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

**在大型交易者平仓时卖出：**
```bash
python copytrading_trader.py --whale-exits
```

## 结果报告

每次运行后，会向用户报告以下信息：
- 当前配置（目标钱包、前 N 个持仓、每个钱包的最大持仓数量）
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

## 示例对话

**用户：“复制交易地址为 0x1234...abcd”的钱包的持仓情况”**
→ 运行：`python copytrading_trader.py --wallets 0x1234...abcd`
→ 显示该钱包的持仓情况以及即将执行的交易

**用户：“地址为 0x5678...efgh 的钱包持有哪些持仓？”**
→ 运行：`python copytrading_trader.py --wallets 0x5678...efgh --dry-run`
→ 显示该钱包的持仓情况（不执行交易）

**用户：“关注这些钱包：0xaaa..., 0xbbb..., 0xccc...”**
→ 运行：`python copytrading_trader.py --wallets 0xaaa...,0xbbb...,0xccc...`
→ 合并所有钱包的持仓信息并显示结果

**用户：“复制交易地址为 0x... 的前 5 个持仓”**
→ 运行：`python copytrading_trader.py --wallets 0x... --top-n 5`

**用户：“我的持仓表现如何？”**
→ 运行：`python copytrading_trader.py --positions`
→ 显示当前在 Polymarket 上的持仓情况及其盈亏情况

**用户：“显示复制交易配置”**
→ 运行：`python copytrading_trader.py --config`
→ 显示当前的设置

**用户：“卖出大型交易者已平仓的持仓”**
→ 运行：`python copytrading_trader.py --whale-exits`
→ 将用户的持仓与大型交易者的持仓进行对比，并卖出他们已平仓的代币

**用户：“进行全面再平衡以匹配大型交易者的持仓”**
→ 运行：`python copytrading_trader.py --rebalance`
→ 包括买入和卖出操作，以匹配大型交易者的持仓配置

## 如何寻找值得关注的大型交易者钱包

常见的方法包括：
1. **排行榜跟踪**：查看 Polymarket 的排行榜，寻找表现稳定的交易者
2. **关注社交媒体上的盈利交易者**：关注在社交媒体上活跃的盈利交易者
3. **特定策略**：关注那些在特定市场（如天气、政治或加密货币领域）有交易记录的交易者

该工具在以下情况下效果最佳：
- 关注 2-5 个钱包以实现投资多样化
- 这些钱包的交易策略较为一致（避免将高风险和低风险的钱包混合）
- 这些钱包交易的市場都在 Polymarket 上有提供

## 故障排除

**“订单金额太少” / “低于最低要求（5 枚代币）”**
- Polymarket 要求每笔订单至少需要 5 枚代币
- 增加 `--max-usd` 的值或减少 `--top-n` 的值，以便专注于更少的持仓

**“未指定钱包地址”**
- 在命令中提供钱包地址，例如：`copytrading_trader.py --wallets 0x1234...`
- 或为自动扫描设置环境变量 `SIMMER_COPYTRADING_WALLETS`

**“代理账户中没有 USDC”**
- 确保您的 Polymarket 账户中有 USDC，或者使用 `--venue simmer` 选项进行 $SIM 模拟交易
- 检查钱包是否已连接到 simmer.markets/dashboard

**“检测到持仓冲突”**
- 两个钱包在同一市场持有相反的方向（一个持有多头，另一个持有空头）
- 净持仓比例小于 10% 的市场会被跳过

**“余额不足”**
- USDC 不足以完成所有交易
- 减少 `SIMMER_COPYTRADING_TOP_N` 或 `SIMMER_COPYTRADING_MAX_USD` 的值

**“无法导入某些市场数据”**
- 有些市场可能无法导入数据（可能是私有的等原因）
- 这些市场会被自动跳过

**“外部钱包需要预签名订单”**
- 环境变量 `WALLET_PRIVATE_KEY` 未设置
- 当设置此变量后，SDK 会自动完成订单签名——无需手动签名
- 解决方法：`export WALLET_PRIVATE_KEY=0x<your-polymarket-wallet-private-key>`
- **注意**：不要尝试手动签名订单或修改脚本代码——SDK 会自动处理签名操作

**“余额显示为 0 美元，但我实际上在 Polygon 上有 USDC”**
- Polymarket 使用的是 **USDC.e**（桥接后的 USDC，合约地址为 `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`）——这不是原生 USDC
- 如果您最近将 USDC 桥接到了 Polygon，可能需要先将 USDC 转换为原生 USDC，然后再尝试

**其他注意事项：**
- 如果遇到问题，请参考上述提示进行排查和解决。