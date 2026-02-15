---
name: manifold
description: "在 Manifold Markets 预测市场中进行搜索、分析和交易。适用于用户需要查询预测市场的赔率、下注、查看投资组合或讨论 Manifold Markets 相关内容的情况。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires": { "bins": ["python3"], "env": ["MANIFOLD_API_KEY"] },
        "primaryEnv": "MANIFOLD_API_KEY",
      },
  }
---

# Manifold Markets

通过 Manifold API 在预测市场中进行交易。所有命令的输出格式为 JSON。

**脚本路径：** `{baseDir}/scripts/manifold.py`

运行方式：`python3 {baseDir}/scripts/manifold.py <command> [options]`

## 检查账户余额

```bash
python3 {baseDir}/scripts/manifold.py balance
```

## 搜索市场

```bash
# Search by keyword
python3 {baseDir}/scripts/manifold.py search "US election"

# Open binary markets, sorted by popularity
python3 {baseDir}/scripts/manifold.py search "AI" --filter open --sort most-popular --limit 5

# Closing soon
python3 {baseDir}/scripts/manifold.py search "" --filter closing-week --sort close-date
```

筛选条件：`all`, `open`, `closed`, `resolved`, `closing-day`, `closing-week`, `closing-month`

排序方式：`most-popular`, `newest`, `score`, `daily-score`, `24-hour-vol`, `liquidity`, `close-date`, `prob-descending`, `prob-ascending`

## 获取市场详情及概率

```bash
# By ID
python3 {baseDir}/scripts/manifold.py market <market-id>

# By slug (from URL)
python3 {baseDir}/scripts/manifold.py market some-market-slug

# Just the probability
python3 {baseDir}/scripts/manifold.py prob <market-id>
```

## 下注

```bash
# Market order: bet 100 mana on YES
python3 {baseDir}/scripts/manifold.py bet <contract-id> 100 YES

# Limit order at 40% probability
python3 {baseDir}/scripts/manifold.py bet <contract-id> 100 YES --limit-prob 0.40

# Dry run (simulate without executing)
python3 {baseDir}/scripts/manifold.py bet <contract-id> 100 YES --dry-run

# Bet on a specific answer in a multiple-choice market
python3 {baseDir}/scripts/manifold.py bet <contract-id> 50 YES --answer-id <answer-id>

# Limit order that expires in 1 hour
python3 {baseDir}/scripts/manifold.py bet <contract-id> 100 YES --limit-prob 0.35 --expires-ms 3600000
```

## 卖出股票

```bash
# Sell all shares in a market
python3 {baseDir}/scripts/manifold.py sell <contract-id>

# Sell specific outcome
python3 {baseDir}/scripts/manifold.py sell <contract-id> --outcome YES

# Sell partial shares
python3 {baseDir}/scripts/manifold.py sell <contract-id> --outcome NO --shares 50

# Sell in multiple-choice market
python3 {baseDir}/scripts/manifold.py sell <contract-id> --answer-id <answer-id>
```

## 取消限价单

```bash
python3 {baseDir}/scripts/manifold.py cancel <bet-id>
```

## 投资组合与持仓

```bash
# Your portfolio summary
python3 {baseDir}/scripts/manifold.py portfolio

# Your current positions with contract details
python3 {baseDir}/scripts/manifold.py my-positions --limit 10 --order profit

# Positions/leaderboard for a specific market
python3 {baseDir}/scripts/manifold.py positions <contract-id> --top 10

# Your position in a specific market
python3 {baseDir}/scripts/manifold.py positions <contract-id> --user-id <your-user-id>
```

## 下注历史记录

```bash
# Your recent bets
python3 {baseDir}/scripts/manifold.py bets --username <your-username>

# Bets on a specific market
python3 {baseDir}/scripts/manifold.py bets --contract-id <contract-id>

# Open limit orders only
python3 {baseDir}/scripts/manifold.py bets --username <your-username> --kinds open-limit
```

## 个人资料

```bash
python3 {baseDir}/scripts/manifold.py me
```

## 注意事项：

- 所有金额单位均为 **mana**（M$）。新账户的初始余额为 M$1,000。
- 限价单的赔率范围为 0.01 至 0.99（保留两位小数）。
- 当用户请求下注时，**务必先使用 `--dry-run` 选项**，以便他们在投入真实资金前确认预期结果。
- 搜索结果中包含 `id` 字段——请将这些 ID 用于下注或卖出操作。
- 对于多选市场，需先获取市场详情以查看可用的选项及其对应的 ID。
- API 的请求速率限制为：每分钟 500 次请求。