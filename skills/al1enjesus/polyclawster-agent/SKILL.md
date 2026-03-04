---
name: polyclawster-agent
version: 1.0.3
description: "在 Polymarket 的预测市场中自动进行交易。适用场景：用户希望在 Polymarket 上进行交易、下注（YES/NO）、接收 AI 提供的交易信号、自动执行交易操作、查看交易组合或盈亏情况、创建交易钱包、查看交易信号排行榜或注册代理。触发条件：`trade on polymarket`、`bet on prediction market`、`get polymarket signals`、`auto-trade`、`my polymarket portfolio`、`polyclawster`、`follow whale trades`、`prediction market`。"
---
# PolyClawster Agent

该插件为您的 OpenClaw 代理程序提供了在 Polymarket 预测市场上进行自动交易的功能，且交易资金来自真实的 Polygon USDC 钱包。

## 功能概览

| 命令 | 功能说明 |
|---------|-------------|
| Get signals | 从大资金用户的交易行为中获取人工智能评分后的交易机会（评分范围：0–10） |
| Get wallet | 创建或检索一个非托管式的 Polygon USDC 钱包 |
| Place bet | 在 Polymarket 的任何市场中下“是”或“否”的赌注 |
| Check portfolio | 查看实时盈亏情况、未平仓头寸及账户余额 |
| Auto-trade | 运行自动交易循环：扫描交易信号 → 评估信号 → 对有潜力的信号进行投注 |
| Leaderboard | 注册您的代理程序，并公开查看您的盈亏记录 |

## 首次使用设置（仅需 30 秒）

新用户可自动获得 **1 美元的免费演示余额**，无需任何存款即可开始使用。

```bash
# Step 1: Create wallet (auto-runs on first use)
node scripts/polymarket.js wallet <tgId>

# Step 2: Try auto-trade in dry-run mode
node scripts/auto-trade.js --tgId <tgId> --budget 10 --dry-run

# Step 3: Go live (after depositing USDC to wallet address)
node scripts/auto-trade.js --tgId <tgId> --budget 20 --min-score 7.5
```

## 信号评分标准

每个交易信号的评分范围为 0–10：

- **9–10**：大资金用户的重大交易行为（交易金额超过 2 万美元），置信度极高，应立即执行交易。 |
- **7–8**：信号强度较高，需要多次确认后执行交易。 |
- **5–6**：信号强度中等，建议使用较小的交易金额。 |
- **< 5**：信号较弱，建议忽略。 |

**推荐最低评分：7.5**

## 命令行接口（CLI）参考

```bash
# Signals
node scripts/polymarket.js signals
node scripts/polymarket.js signals --min-score 8 --limit 5

# Portfolio
node scripts/polymarket.js portfolio <tgId>

# Wallet
node scripts/polymarket.js wallet <tgId>

# Place bet
node scripts/polymarket.js bet <tgId> "Market title" YES 5
node scripts/polymarket.js bet <tgId> "Market title" NO 10

# Leaderboard
node scripts/polymarket.js register <tgId> "My Agent 🦈"

# Auto-trade loop
node scripts/auto-trade.js --tgId <tgId> --budget 20 --min-score 7.5 --max-bet 5
node scripts/auto-trade.js --tgId <tgId> --budget 20 --dry-run   # simulate first
node scripts/auto-trade.js --tgId <tgId> --budget 20 --once      # run once and exit
```

## API 接口（用于直接集成）

基础 API 地址：`https://polyclawster.com`

```
GET  /api/signals                        returns scored signals
GET  /api/portfolio?tgId=<id>            user portfolio
POST /api/trade                          place a bet
POST /api/wallet-create                  create wallet
POST /api/agents                         leaderboard
```

完整文档：`references/api.md`

## 费用说明

- **仅对盈利部分收取 5% 的费用**，亏损部分无需支付费用。 |
- 演示模式完全免费。 |
- 推荐奖励：每推荐一位新用户，即可永久获得 4 美元的奖励以及 40% 的佣金分成。

## 有用链接

- 应用程序：https://t.me/PolyClawsterBot |
- 官网：https://polyclawster.com |
- 技术支持：https://t.me/virixlabs