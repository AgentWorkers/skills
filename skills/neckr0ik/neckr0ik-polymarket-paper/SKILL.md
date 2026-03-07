---
name: neckr0ik-polymarket-paper
version: 1.0.0
description: Polymarket的模拟交易平台。使用虚拟资金练习预测市场交易，学习交易策略，跟踪交易表现，并在排行榜上参与竞争。在投入真实资金之前，可先通过该平台进行训练。
---
# Polymarket 纸上交易

使用虚拟资金练习 Polymarket 交易，学习交易策略，并在排行榜上与其他交易者竞争。

## 快速入门

```bash
# Create account with $10,000 virtual
neckr0ik-polymarket-paper create-account --name "MyPortfolio"

# View available markets
neckr0ik-polymarket-paper markets --limit 20

# Place a trade
neckr0ik-polymarket-paper trade --market "will-bitcoin-reach-100k" --side YES --amount 500

# Check portfolio
neckr0ik-polymarket-paper portfolio

# View leaderboard
neckr0ik-polymarket-paper leaderboard --weekly
```

## 功能介绍

- **虚拟交易**：提供 10,000 美元的练习账户
- **真实市场数据**：使用 Polymarket 的实时价格数据
- **模拟执行**：订单以市场价格成交
- **绩效追踪**：记录胜率、投资回报率（ROI）和夏普比率（Sharpe Ratio）
- **排行榜**：与其他纸上交易者竞争
- **策略指南**：在投入真实资金前学习交易技巧

## 账户类型

| 账户等级 | 虚拟资金 | 每日可交易的市场数量 | 分析功能 |
|------|---------------|--------------|-----------|
| 免费 | 10,000 美元 | 5 个市场 | 基础功能 |
| 专业版（9 美元/月） | 100,000 美元 | 无限市场 | 高级功能 |
| 团队版（29 美元/月） | 多个账户 | 无限市场 | 全部功能 |

## 命令

### create-account

创建一个纸上交易账户。

```bash
neckr0ik-polymarket-paper create-account [options]

Options:
  --name <name>        Account name
  --tier <tier>        Account tier (free, pro, team)
  --initial <amount>   Starting cash (default: 10000)
```

### markets

查看可交易的 Polymarket 市场。

```bash
neckr0ik-polymarket-paper markets [options]

Options:
  --limit <n>         Max results (default: 20)
  --category <name>   Filter by category (crypto, politics, sports)
  --search <query>     Search by keyword
```

### trade

下达一笔纸上交易订单。

```bash
neckr0ik-polymarket-paper trade [options]

Options:
  --market <id>        Market ID or slug
  --side <side>        YES or NO
  --amount <dollars>   Amount to trade
  --limit <price>      Limit price (optional)
```

### portfolio

查看您的投资组合。

```bash
neckr0ik-polymarket-paper portfolio [options]

Options:
  --history            Show transaction history
  --performance        Show performance metrics
```

### resolve

手动完成交易（用于练习）。

```bash
neckr0ik-polymarket-paper resolve --market <id> --outcome <YES|NO>
```

### leaderboard

查看排名靠前的纸上交易者。

```bash
neckr0ik-polymarket-paper leaderboard [options]

Options:
  --period <period>    weekly, monthly, all-time
  --strategy <type>    Filter by strategy
```

### analytics

查看详细的交易分析报告。

```bash
neckr0ik-polymarket-paper analytics [options]

Options:
  --period <days>      Analysis period (default: 30)
  --strategy           Breakdown by strategy
```

### export

导出您的交易历史记录。

```bash
neckr0ik-polymarket-paper export [options]

Options:
  --format <format>    csv, json
  --output <file>      Output file
```

## 交易策略

### 1. 价差套利（练习）

当 YES 和 NO 选项的结合价格低于 1.00 美元时，同时买入这两个选项。

```
Example:
Market: "Will Bitcoin hit $100k?"
YES: $0.48
NO: $0.50
Combined: $0.98

Trade: Buy $490 YES + $500 NO = $990 total
Guaranteed payout: $1,000
Profit: $10 (1.01%)
```

### 2. 最终阶段交易

在交易临近结束时买入那些几乎可以确定会盈利的选项。

```
Example:
Market: "Will X happen by March 31?"
Current: March 28
YES price: $0.97
Days remaining: 3

Trade: Buy YES at $0.97
Hold until resolution at $1.00
Profit: 3.1% in 3 days (376% annualized)
```

### 3. 新闻相关性交易

在市场调整前根据新闻进行交易。

```
Example:
News: "Israel strikes Tehran. Trump demands surrender."
Market: "Will Trump declare war on Iran?" @ 40%

Analysis: Military action ≠ formal war declaration
Market likely overpriced
Trade: Sell YES (or buy NO)
```

## 绩效指标

| 指标 | 描述 |
|--------|-------------|
| 总盈亏（Total PnL） | 总利润/亏损 |
| 胜率（Win Rate） | 盈利交易的百分比 |
| 平均回报（Average Return） | 每笔交易的平均回报 |
| 夏普比率（Sharpe Ratio） | 经风险调整后的回报 |
| 最大回撤（Max Drawdown） | 最大收益与最大亏损之间的差额 |
| 卡尔玛比率（Calmar Ratio） | 回报率与最大回撤的比值 |

## 排行榜分类

| 分类 | 排名依据 |
|----------|-----------|
| 总体表现（Overall） | 总盈亏 |
| 投资回报率（ROI） | 投资回报 |
| 胜率（Win Rate） | 盈利交易的百分比 |
| 夏普比率（Sharpe Ratio） | 经风险调整后的回报 |
| 连胜记录（Streak） | 最长的连胜 streak |

## 教育资源

### 策略指南

1. **价差套利基础** — 无风险的盈利技巧
2. **最终阶段交易** — 高概率盈利的交易策略
3. **新闻相关性交易** — 基于新闻的事件驱动型交易
4. **风险管理** — 仓位控制与止损策略
5. **高级策略** — 跨市场、跨平台的交易技巧

### 练习场景

1. **场景：加密货币牛市**
   - 初始资金：50,000 美元
   - 问题：“到年底 BTC 价格会达到 150,000 美元吗？”
   - 学习内容：仓位控制与交易时机选择

2. **场景：选举之夜**
   - 初始资金：25,000 美元
   - 市场情况：多种选举结果可能
   - 学习内容：对冲策略与相关性分析

3. **场景：市场暴跌**
   - 初始资金：100,000 美元
   - 问题：“标普 500 指数会跌破 4000 点吗？”
   - 学习内容：风险管理与止损策略

## 示例交易记录

```bash
$ neckr0ik-polymarket-paper create-account --name "Learning"
✓ Created account: Learning
  Virtual cash: $10,000

$ neckr0ik-polymarket-paper markets --search "bitcoin"
Found 5 markets:
  1. "Will Bitcoin hit $100k by EOY 2026?" YES: 0.45
  2. "Will Bitcoin drop below $50k?" NO: 0.65
  3. "Will Bitcoin be banned?" NO: 0.92
  ...

$ neckr0ik-polymarket-paper trade --market "bitcoin-100k" --side YES --amount 1000
✓ Trade executed
  Market: "Will Bitcoin hit $100k by EOY 2026?"
  Side: YES
  Amount: $1,000
  Price: $0.45
  Shares: 2,222.22
  Fee: $0.01

$ neckr0ik-polymarket-paper portfolio
Portfolio: Learning
Cash: $8,999.99
Positions:
  - "bitcoin-100k" YES: 2,222.22 shares @ $0.45 = $999.99
Total Value: $10,000.00 (0.00% return)

$ neckr0ik-polymarket-paper leaderboard --weekly
Weekly Leaderboard:
  1. @trader1: +15.2% ($1,520 profit)
  2. @trader2: +12.8% ($1,280 profit)
  3. @trader3: +10.5% ($1,050 profit)
  ...
  127. @Learning: 0.0% ($0 profit)
```

## 相关资源

- `references/strategies.md` — 详细的策略指南
- `scripts/paper_trading.py` — 主要实现代码
- `projects/polymarket-paper-trading/` — 完整的平台设计文档