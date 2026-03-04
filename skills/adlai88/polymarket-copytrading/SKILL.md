---
name: polymarket-copytrading
description: 使用 Simmer API 获取 Polymarket 上顶级交易者的镜像交易位置信息，并对来自多个钱包的交易数据进行大小加权聚合处理。
metadata:
  author: Simmer (@simmer_markets)
  version: "1.5.0"
  displayName: Polymarket Copytrading
  difficulty: beginner
---# Polymarket复制交易（Copytrading）

使用Simmer SDK复制Polymarket上成功交易者的持仓。

> **这是一个模板。** 默认逻辑会按照资金规模进行加权分配来复制大型交易者的持仓——你可以根据自己的钱包选择标准、持仓筛选条件或再平衡规则来修改这个模板。该工具会处理所有底层逻辑（如获取钱包信息、检测冲突、执行交易等），而策略的制定则由用户自行完成。

## 何时使用此工具

当用户希望执行以下操作时，可以使用此工具：
- 复制Polymarket上大型交易者的持仓
- 使用模拟资金（$SIM）进行模拟交易以测试策略
- 查看某个钱包的持仓情况
- 关注特定的交易者
- 查看这些交易者的复制交易持仓

## 快速命令

```bash
# Check account balance and positions
python scripts/status.py

# Detailed position list
python scripts/status.py --positions
```

**API参考：**
- 基础URL：`https://api.simmer.markets`
- 认证：`Authorization: Bearer $SIMMER_API_KEY`
- 投资组合：`GET /api/sdk/portfolio`
- 持仓信息：`GET /api/sdk/positions`

## 查找大型交易者钱包

- **[predicting.top](https://predicting.top)** — Polymarket上表现最佳的交易者排行榜（包含钱包地址）
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

这是最简单的方法——无需任何设置，直接提供钱包地址即可。

## 持久化设置（可选）

为了实现自动化的定期扫描，可以将钱包信息保存到环境变量中：

| 设置 | 环境变量 | 默认值 |
|---------|---------------------|---------|
| 目标钱包 | `SIMMER_COPYTRADING_WALLETS` | （未设置） |
| 前N大持仓 | `SIMMER_COPYTRADING_TOP_N` | 自动计算 |
- 每个持仓的最大金额 | `SIMMER_COPYTRADING_MAX_USD` | 50美元 |
- 每次运行的最大交易数量 | `SIMMER_COPYTRADING_MAX_TRADES` | 10笔 |

**前N大持仓的自动计算规则（未指定时）：**
- 账户余额 < 50美元：前5个持仓
- 账户余额 50-200美元：前10个持仓
- 账户余额 200-500美元：前25个持仓
- 账户余额 500美元以上：前50个持仓

**Polymarket的限制：**
- 每笔订单至少需要5份代币
- SDK要求每个持仓的最低价值为1.00美元（以过滤小额交易）

> ⚠️ **谨慎起步：** 先从小额开始（使用`--max-usd 5-10`），并通过`--dry-run`模式运行脚本，了解工具的运行情况后再逐步增加交易金额。

## 工作原理

脚本每个周期会执行以下操作：
1. 通过Simmer API获取所有目标钱包的持仓信息
2. 使用资金规模加权的方式合并这些持仓数据（资金越多的钱包影响越大）
3. 检测持仓冲突（例如，一个钱包持有多头仓位，另一个钱包也持有多头仓位，则跳过该市场）
4. 应用前N大持仓的筛选规则，专注于最具投资信心的持仓
5. 自动从Polymarket导入缺失的市场数据
6. 计算所需的再平衡交易量
7. 通过Simmer SDK执行交易（同时遵守平台的交易限额）
8. 将结果反馈给用户

## 使用$SIM进行模拟交易

复制交易支持$SIM模式——使用Simmer的LMSR市场中的模拟资金来复制大型交易者的持仓。无需实际钱包或USDC。

```bash
# Paper trade with $SIM (explicit)
python copytrading_trader.py --venue simmer --wallets 0x123... --live

# Auto-detect: if your account has no linked wallet, $SIM is used automatically
python copytrading_trader.py --wallets 0x123... --live
```

在$SIM模式下：
- 交易在Simmer的LMSR市场中以Polymarket的实际价格执行
- 每个市场都会分配10,000美元的模拟资金
- 持仓情况会显示在用户的Simmer投资组合中（来源：`sdk:copytrading`）
- 复制交易的信号仍然来自Polymarket的实时数据

## 运行脚本

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

**全量再平衡模式（包括卖出操作）：**
```bash
python copytrading_trader.py --rebalance
```

**在大型交易者平仓时卖出相应持仓：**
```bash
python copytrading_trader.py --whale-exits
```

## 结果报告

每次运行完成后，会向用户报告以下信息：
- 当前配置（目标钱包、前N大持仓）
- 获取到的钱包数量及总持仓数量
- 因冲突被跳过的市场
- 执行的交易（及原因）
- 用户当前的投资组合持仓情况

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

**用户：**“复制交易地址为0x1234...abcd的交易者的持仓”**
→ 运行：`python copytrading_trader.py --wallets 0x1234...abcd`
→ 显示该钱包的持仓情况以及将要执行的交易

**用户：**“地址为0x5678...efgh的交易者持有哪些持仓？”**
→ 运行：`python copytrading_trader.py --wallets 0x5678...efgh --dry-run`
→ 显示该钱包的持仓情况（不执行交易）

**用户：**“关注这些钱包：0xaaa..., 0xbbb..., 0xccc...”**
→ 运行：`python copytrading_trader.py --wallets 0xaaa...,0xbbb...,0xccc...`
→ 合并所有钱包的持仓信息并显示结果

**用户：**“只复制前5大持仓”**
→ 运行：`python copytrading_trader.py --wallets 0x... --top-n 5`

**用户：**“我的持仓表现如何？”**
→ 运行：`python copytrading_trader.py --positions`
→ 显示用户在Polymarket上的当前持仓及盈亏情况

**用户：**“显示复制交易的相关配置”**
→ 运行：`python copytrading_trader.py --config`
→ 显示当前设置

**用户：**“卖出那些已被大型交易者平仓的持仓”**
→ 运行：`python copytrading_trader.py --whale-exits`
→ 将用户的持仓与大型交易者的持仓进行对比，并卖出相应的持仓

**如何寻找值得关注的交易者钱包**

常见的方法包括：
1. **排行榜追踪**：查看Polymarket的排行榜，选择表现稳定的交易者
2. **关注社交媒体上的盈利交易者**：跟踪在社交媒体上表现优异的交易者
3. **特定策略**：关注那些在特定市场（如天气、政治或加密货币领域）有交易习惯的交易者

**使用建议：**
- 最佳使用方式是同时关注2-5个钱包以实现投资多样化
- 选择持仓策略较为相似的交易者（避免将高风险和低风险的钱包混合）
- 确保所关注的交易者交易的都是Polymarket平台上可交易的市场

## 常见问题及解决方法**

- **“订单金额太少” / “低于最低要求（5美元）**：Polymarket要求每笔订单至少5份代币
- 增加`--max-usd`参数的值或减少`--top-n`参数，以集中关注少数几个持仓
- **未指定钱包地址**：在命令中提供钱包地址，例如：`copytrading_trader.py --wallets 0x1234...`
- 或为自动扫描设置`SIMMER_COPYTRADING_WALLETS`环境变量
- **代理账户中没有USDC余额**：确保你的Polymarket钱包中有USDC，或者使用`--venue simmer`进行$SIM模拟交易
- **检测到持仓冲突**：如果多个钱包在同一市场持有相反方向的持仓（例如，一个持有多头，另一个持有空头），则跳过该市场
- **余额不足**：USDC余额不足以完成所有交易
- 调整`SIMMER_COPYTRADING_TOP_N`或`SIMMER_COPYTRADING_MAX_USD`参数
- **无法导入某些市场数据**：部分市场可能无法导入（可能是私有的等），这些市场会自动被跳过
- **外部钱包需要预签名订单**：如果环境变量`WALLET_PRIVATE_KEY`未设置，SDK会自动签名订单——无需手动操作
- **余额显示为0美元，但实际上我有USDC**：Polymarket使用的是`USDC.e`（桥接后的USDC，合约地址为`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`），并非原生USDC。如果最近将USDC桥接到了Polygon平台，可能需要先将USDC转换为`USDC.e`后再尝试

**注意：**  
- 请勿尝试手动签名订单或修改脚本代码——SDK会自动处理这些操作。