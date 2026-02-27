---
name: polymarket-copytrading
displayName: Polymarket Copytrading
description: 使用 Simmer API 获取 Polymarket 上顶级交易者的持仓位置信息，并对多个钱包的持仓数据进行加权汇总。
metadata: {"clawdbot":{"emoji":"🐋","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false,"automaton":{"managed":true,"entrypoint":"copytrading_trader.py"},"tunables":[{"env":"SIMMER_COPYTRADING_MAX_USD","type":"number","default":50,"range":[1,200],"step":5,"label":"Max bet per trade"},{"env":"SIMMER_COPYTRADING_TOP_N","type":"number","default":5,"range":[1,20],"step":1,"label":"Positions to track"},{"env":"SIMMER_COPYTRADING_MAX_TRADES","type":"number","default":5,"range":[1,20],"step":1,"label":"Max trades per run"}]}}
authors:
  - Simmer (@simmer_markets)
version: "1.4.0"
published: true
---
# Polymarket 复制交易

使用 Simmer SDK 复制 Polymarket 上表现优异的交易者的持仓。

> **这是一个模板。** 默认逻辑会按照资产规模进行加权分配来复制大型交易者的持仓——您可以根据自己的钱包选择标准、持仓筛选条件或再平衡规则对其进行调整。该工具会处理所有底层逻辑（如钱包获取、冲突检测和交易执行），而策略的制定则由用户自行完成。

## 何时使用此工具

当用户需要以下操作时，请使用此工具：
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
- 基本 URL：`https://api.simmer.markets`
- 认证：`Authorization: Bearer $SIMMER_API_KEY`
- 投资组合：`GET /api/sdk/portfolio`
- 持仓情况：`GET /api/sdk/positions`

## 寻找大型交易者钱包

- **[predicting.top](https://predicting.top)** — Polymarket 上表现最佳的交易者排行榜（包含钱包地址）
- **[alphawhale.trade](https://alphawhale.trade)** — 用于复制和跟踪表现优异的交易者的工具
- **Polymarket Leaderboard** — 官方排行榜（需要账户）

## 快速入门（临时使用）

**用户直接在聊天中提供钱包地址：**
```
User: "Copytrade this wallet: 0x1234...abcd"
User: "What positions does 0x5678...efgh have?"
User: "Follow these whales: 0xaaa..., 0xbbb..."
```

→ 使用 `--wallets` 标志运行：
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

> ⚠️ **谨慎开始：** 先从小额开始尝试（使用 `--max-usd 5-10`），并通过 `--dry-run` 模式了解工具的运行情况，再逐步增加交易金额。

## 工作原理

脚本每个周期会执行以下操作：
1. 通过 Simmer API 从所有目标钱包中获取持仓信息
2. 使用加权聚合方法合并这些持仓数据（资产规模较大的钱包影响更大）
3. 检测持仓冲突（例如，一个钱包持有多头仓位，另一个钱包持相反方向的头寸），并跳过这些市场
4. 应用前 N 个持仓的筛选规则，专注于最具投资信心的持仓
5. 从 Polymarket 自动导入缺失的市场数据
6. 计算所需的再平衡交易
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
- 持仓情况会显示在用户的 Simmer 投资组合中（数据来源：`sdk:copytrading`)
- 交易信号仍然来自 Polymarket 的实际数据

## 运行工具

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

**在大型交易者平仓时卖出：**
```bash
python copytrading_trader.py --whale-exits
```

## 结果报告

每次运行后，会向用户报告以下信息：
- 当前配置（目标钱包、前 N 个持仓、每个钱包的最大持仓数量）
- 获取到的钱包数量及总持仓数量
- 因冲突而被跳过的市场
- 执行的交易（或未执行的交易及其原因）
- 用户当前的持仓情况

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

**用户：“复制交易地址为 0x1234...abcd 的持仓”**
→ 运行：`python copytrading_trader.py --wallets 0x1234...abcd`
→ 显示该钱包的持仓情况以及即将执行的交易

**用户：“地址为 0x5678...efgh 的持仓是什么？”**
→ 运行：`python copytrading_trader.py --wallets 0x5678...efgh --dry-run`
→ 显示该钱包的持仓情况（不执行交易）

**用户：“关注这些钱包：0xaaa..., 0xbbb..., 0xccc...”**
→ 运行：`python copytrading_trader.py --wallets 0xaaa...,0xbbb...,0xccc...`
→ 合并所有钱包的持仓信息并显示结果

**用户：“复制交易地址为 0x... 的前 5 个持仓”**
→ 运行：`python copytrading_trader.py --wallets 0x... --top-n 5`

**用户：“我的持仓表现如何？”**
→ 运行：`python copytrading_trader.py --positions`
→ 显示用户在 Polymarket 上的当前持仓及盈亏情况

**用户：“显示复制交易配置”**
→ 运行：`python copytrading_trader.py --config`
→ 显示当前设置

**用户：“卖出大型交易者已平仓的持仓”**
→ 运行：`python copytrading_trader.py --whale-exits`
→ 将用户的持仓与大型交易者的持仓进行对比，并卖出他们已平仓的代币

**用户：“进行全量再平衡以匹配大型交易者的持仓”**
→ 运行：`python copytrading_trader.py --rebalance`
→ 包括买入和卖出操作，以匹配大型交易者的持仓配置

## 如何寻找值得关注的大型交易者钱包

常见方法：
1. **排行榜跟踪**：查看 Polymarket 的排行榜，寻找表现稳定的交易者
2. **关注社交媒体上的盈利交易者**：跟踪在社交媒体上活跃的盈利交易者
3. **特定策略**：关注那些在特定市场（如天气、政治或加密货币领域）有交易习惯的交易者

**最佳使用场景：**
- 关注 2-5 个钱包以实现投资多样化
- 所选钱包的投资策略较为一致（避免将高风险和低风险的钱包混合）
- 所选钱包在 Polymarket 上都有可交易的资产

## 故障排除

**“订单金额太少” / “低于最低要求（5 枚代币）**：
- Polymarket 要求每笔订单至少包含 5 枚代币
- 增加 `--max-usd` 的值或减少 `--top-n` 的值，以专注于更少的持仓

**“未指定钱包”**
- 在命令中提供钱包地址，例如：`copytrading_trader.py --wallets 0x1234...`
- 或为自动扫描设置环境变量 `SIMMER_COPYTRADING_WALLETS`

**“代理账户中没有 USDC”**
- 确保您的 Polymarket 账户中有 USDC，或使用 `--venue simmer` 选项进行 $SIM 模拟交易
- 检查钱包是否已关联到 simmer.markets/dashboard

**“检测到持仓冲突”**
- 两个钱包在同一市场持有相反方向的持仓
- 净持仓比例小于 10% 的市场会被自动跳过

**“余额不足”**
- USDC 不足以完成所有交易
- 减少 `SIMMER_COPYTRADING_TOP_N` 或 `SIMMER_COPYTRADING_MAX_USD` 的值

**“无法导入某些市场”**
- 有些市场可能无法导入（可能是私有的等原因）
- 这些市场会被自动跳过

**“外部钱包需要预签名订单”**
- 环境变量 `WALLET_PRIVATE_KEY` 未设置
- 当设置此变量后，SDK 会自动完成订单签名——无需手动操作
- 解决方法：`export WALLET_PRIVATE_KEY=0x<your-polymarket-wallet-private-key>`
- 请勿尝试手动签名订单或修改代码——SDK 会自动处理签名操作

**“余额显示为 0 美元，但我实际上在 Polygon 上有 USDC”**
- Polymarket 使用的是 **USDC.e**（桥接后的 USDC，合约地址为 `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`）——这不是原生 USDC
- 如果您最近将 USDC 桥接到了 Polygon，可能需要将桥接后的 USDC 转换为原生 USDC，然后再尝试

**注意：**