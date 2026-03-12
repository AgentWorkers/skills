---
name: polymarket-ai-divergence
description: 寻找那些 Simmer 的 AI 估值与实际市场价格存在差异的市场，然后利用 Kelly 定量投资策略在价格被高估或低估的一侧进行交易。系统会扫描市场中的价格差异，检查交易费用和相关风险保障措施，并仅在费用为零且具有足够交易优势的市场中执行交易。
metadata:
  author: Simmer (@simmer_markets)
  version: "2.1.1"
  displayName: Polymarket AI Divergence
  difficulty: intermediate
---# Polymarket AI 分歧交易策略

该策略旨在寻找 Simmer 的 AI 预测价格与实际市场价格出现分歧的市场，并利用这种价格差异进行交易。

> **这是一个模板。** 默认逻辑是在 AI 预测价格与实际价格之间的分歧超过 2% 时进行交易，且每次交易的投注金额上限为 25%（根据 Kelly 公式计算）。您可以根据需要修改该策略，设置不同的交易阈值、投注策略或添加额外的过滤条件（例如：仅交易在 7 天内能够得到结果的市场）。该策略负责处理所有交易相关的细节（如价格差异检测、费用验证、风险控制以及交易执行），而具体的交易决策由您的代理系统（agent）来完成。

## 功能概述

1. **扫描** 所有活跃市场，检测 AI 预测价格与实际市场价格之间的差异。
2. **筛选** 出现超过预设阈值（默认为 2%）且费用为零的市场。
3. **进行风险控制**：检查是否存在与先前交易方向相反的新交易（即“翻转交易”），以及用户是否已经持有相关头寸。
4. **使用 Kelly 公式** 来确定每次交易的投注金额，并设置保守的上限。
5. **执行交易**：当 AI 预测价格偏高时买入，当价格偏低时卖出。

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

| 参数名 | 环境变量 | 默认值 | 说明 |
|---------|-----------|---------|-------------------|
| `min_divergence` | `SIMMER_DIVERGENCE_MIN` | 5.0 | 显示结果时使用的最小价格差异百分比 |
| `min_edge` | `SIMMER_DIVERGENCE_MIN_EDGE` | 0.02 | 可进行交易的最小价格差异百分比（2%） |
| `max_bet_usd` | `SIMMER_DIVERGENCE_MAX_BET` | 每次交易的最大投注金额（美元） |
| `max_trades_per_run` | `SIMMER_DIVERGENCE_MAX_TRADES` | 每次运行时最多进行的交易次数 |
| `kelly_cap` | `SIMMER_DIVERGENCE_KELLY_CAP` | Kelly 公式计算中的投注比例上限（25%） |
| `daily_budget` | `SIMMER_DIVERGENCE_DAILY_BUDGET` | 每日的交易预算上限 |
| `default_direction` | `SIMMER_DIVERGENCE_direction` | 可选值：`both`（同时考虑买入和卖出信号）或 `bullish`（仅买入信号） |

**通过 CLI 更新配置：** `python ai_divergence.py --set max_bet_usd=10`

## 工作原理

### 价格差异信号

每个被扫描的市场都有两个价格：
- **AI 预测价格**（`current_probability`）：基于多模型集成预测得出的价格。
- **实际市场价格**（`external_price_yes`）：Polymarket/Kalshi 平台上的实际市场价格。

**价格差异 = AI 预测价格 - 实际市场价格**

- 当价格差异大于 0 时：AI 认为市场被低估 → 发出买入信号（执行买入操作）。
- 当价格差异小于 0 时：AI 认为市场被高估 → 发出卖出信号（执行卖出操作）。

### Kelly 公式用于确定投注金额

每次交易的投注金额根据 Kelly 公式计算，并受到 `kelly_cap`（默认值为 25%）的上限限制，以控制风险。

### 费用筛选

Polymarket 上 75% 的市场收取 0% 的交易费用，剩余的 25% 的市场收取 10% 的费用（主要针对短期交易的加密货币和体育赛事相关市场）。该策略**仅交易费用为零的市场**，以避免费用影响交易利润。

### 风险控制措施

- **费用检查**：跳过任何收取交易费用的市场。
- **翻转交易检测**：利用 SDK 的上下文 API 检测是否存在自相矛盾的交易行为。
- **头寸检查**：避免在用户已经持有相关头寸的市场中进行交易。
- **每日预算限制**：当达到每日交易预算上限时停止交易。
- **保守的投注策略**：通过 Kelly 公式确保不会过度投注。

## 使用的 API 端点

- `GET /api/sdk/markets/opportunities`：获取按价格差异排序的市场列表。
- `GET /api/sdk/context/{market_id}`：获取特定市场的费用信息和风险控制设置。
- `POST /api/sdk/trade`：通过 SDK 客户端执行交易。
- `GET /api/sdk/positions`：获取当前的投资组合持仓情况。

## 常见问题及解决方法

- **“没有符合条件市场的交易机会”**：可能是因为所有市场的价格差异都低于 `min_edge` 的设置。可以通过 `--set min_edge=0.01` 来降低阈值，或等待价格差异更大的市场出现。
- **“每日预算已用尽”**：表示策略已达到每日交易预算上限。可以通过 `--set daily_budget=50` 来调整预算。
- **所有市场都被跳过（因为费用问题）**：仅交易费用为零的市场。如果所有可交易的市场都收取费用，策略将不会执行任何交易。这是设计上的初衷。
- **“上下文信息获取失败”**：可能是由于 SDK 的上下文 API 的请求频率限制（每分钟 18 次请求）。如果频繁执行该策略，请考虑减少 `max_trades_per_run` 的值。