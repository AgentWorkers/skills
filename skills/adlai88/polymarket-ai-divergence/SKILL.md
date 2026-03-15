---
name: polymarket-ai-divergence
description: 寻找那些 Simmer 的 AI 生成的价格共识与实际市场价格存在差异的市场，然后利用 Kelly 定量交易策略在价格被高估或低估的一侧进行交易。系统会自动扫描价格差异，检查交易费用和相关安全措施，并仅在费用为零且具有足够交易优势的市场中执行交易。
metadata:
  author: Simmer (@simmer_markets)
  version: "2.2.0"
  displayName: Polymarket AI Divergence
  difficulty: intermediate
---# Polymarket AI 分歧交易策略

该策略旨在寻找 Simmer 的 AI 预测价格与实际市场价格出现分歧的市场，并利用这种价格差异进行交易。

> **这是一个模板。** 默认逻辑是当 AI 预测价格与实际价格的差异超过 2% 时，在零费用市场中进行交易，同时使用 Kelly 算法来确定交易金额，但交易金额上限为 25%。您可以根据需要修改该策略，设置不同的交易阈值、资金管理策略或额外的筛选条件（例如，仅交易在 7 天内能够解决的价格差异）。该策略负责处理所有交易相关的细节工作（包括价格差异的检测、费用检查、风险控制以及交易执行），而具体的交易决策由您的代理系统（agent）来完成。

## 功能概述

1. **扫描** 所有活跃市场，检测 AI 预测价格与实际市场价格之间的差异。
2. **筛选** 出现超过预设阈值（默认为 2%）且费用为零的市场。
3. **进行风险控制**：检查是否存在与先前交易相反的方向（例如，如果之前买入，则避免再次买入）。
4. **使用 Kelly 算法** 来确定交易金额，并设置保守的上限。
5. **执行交易**：在价格被低估的一侧进行买入（当 AI 预测价格上涨时）或卖出（当 AI 预测价格下跌时）。

## 快速命令

```bash
# Scan only (dry run, no trades)
python ai_divergence.py

# Scan + execute trades
python ai_divergence.py --live

# Only show bullish divergences
python ai_divergence.py --bullish

# Only >15% divergence
python ai_divergence.py --min 15

# JSON output
python ai_divergence.py --json

# Cron mode (quiet, trades only)
python ai_divergence.py --live --quiet

# Show config
python ai_divergence.py --config

# Update config
python ai_divergence.py --set max_bet_usd=10
```

## 配置参数

| 参数名          | 环境变量            | 默认值        | 说明                          |
|-----------------|------------------|-------------|--------------------------------------|
| `min_divergence`    | `SIMMER_DIVERGENCE_MIN`    | 5.0          | 显示价格差异的最低百分比阈值              |
| `min_edge`       | `SIMMER_DIVERGENCE_MIN_EDGE` | 0.02          | 可用于交易的最低价格差异百分比              |
| `max_bet_usd`     | `SIMMER_DIVERGENCE_MAX_BET`    | 5.0          | 每笔交易的最大投注金额                |
| `max_trades_per_run` | `SIMMER_DIVERGENCE_MAX_TRADES` | 3            | 每次运行中的最大交易次数                |
| `kelly_cap`     | `SIMMER_DIVERGENCE_KELLY_CAP`    | 0.25          | Kelly 算法中的资金使用上限                |
| `daily_budget`    | `SIMMER_DIVERGENCE_DAILY_BUDGET` | 25.0          | 每日的交易预算上限                  |
| `default_direction` | `SIMMER_DIVERGENCE_direction` | "(both)"       | 过滤条件："看涨" 或 "看跌"                |

**通过 CLI 更新配置：** `python ai_divergence.py --set max_bet_usd=10`

## 工作原理

### 价格差异信号

每个被扫描的市场都有两个价格：
- **AI 预测价格** (`current_probability`)：基于多模型集成预测得出的价格。
- **实际市场价格** (`external_price_yes`)：Polymarket/Kalshi 上的实际市场价格。

**价格差异 = AI 预测价格 - 实际市场价格**

- 当价格差异大于 0 时：AI 认为市场价格被低估 → 执行买入操作。
- 当价格差异小于 0 时：AI 认为市场价格被高估 → 执行卖出操作。

### Kelly 算法

交易金额的计算使用 Kelly 算法：
```
kelly_fraction = edge / (1 - price)
position_size = kelly_fraction * max_bet_usd
```
该算法的使用上限为 `kelly_cap`（默认为 25%），以控制交易风险。

### 费用筛选

Polymarket 上 75% 的市场收取 0% 的费用，其余 25% 的市场收取 10% 的费用（主要针对短期交易的加密货币和体育赛事相关市场）。本策略**仅交易零费用市场**，以避免费用影响交易利润。

### 风险控制措施

- **费用检查**：跳过任何收取交易费用的市场。
- **交易方向检测**：利用 SDK 的上下文 API 检测是否存在自相矛盾的交易行为。
- **持仓检查**：避免在已持有头寸的市场中再次进行交易。
- **每日预算限制**：达到每日交易预算上限时停止交易。
- **保守的资金管理**：使用 Kelly 算法进行交易金额的确定，以防止过度投注。

## 使用的 API 端点

- `GET /api/sdk/markets/opportunities` — 获取按价格差异排序的市场列表。
- `GET /api/sdk/context/{market_id}` — 获取特定市场的费用率和风险控制规则。
- `POST /api/sdk/trade` — 通过 SDK 客户端执行交易。
- `GET /api/sdk/positions` — 获取当前的投资组合持仓情况。

## 常见问题解决方法

- **“没有符合阈值的市场”**：所有市场的价格差异都低于 `min_edge` 设置。可以通过 `--set min_edge=0.01` 来降低阈值，或等待出现更大的价格差异。
- **“每日预算已用尽”**：策略已达到每日交易预算上限。可以通过 `--set daily_budget=50` 来调整预算。
- **所有市场都被跳过（因费用问题）**：仅交易零费用市场。如果所有可用的交易机会都涉及费用，策略将不会执行任何交易。这是设计初衷。
- **“上下文信息获取失败”**：SDK 的上下文 API 有速率限制（每分钟 18 次请求）。如果频繁调用该 API，可以减少 `max_trades_per_run` 的值。