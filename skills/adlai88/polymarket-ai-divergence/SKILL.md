---
name: polymarket-ai-divergence
displayName: Polymarket AI Divergence
description: 寻找那些 Simmer 的 AI 预测价格与实际市场价格存在差异的市场，然后利用 Kelly 定量策略在价格被高估或低估的一侧进行交易。系统会扫描市场中的价格差异，检查交易费用及相关保障措施，并仅在零费用且具有足够交易优势的市场中执行交易。
metadata: {"clawdbot":{"emoji":"🔮","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false,"automaton":{"managed":true,"entrypoint":"ai_divergence.py"}}}
authors:
  - Simmer (@simmer_markets)
version: "2.0.0"
published: true
---
# Polymarket AI 分歧交易策略

该策略用于寻找 Simmer 的 AI 估值与实际市场价格出现分歧的市场，并利用这种分歧进行交易。

> **这是一个模板。** 默认逻辑是在 AI 估值与市场价格的分歧超过 2% 时进行交易，且交易金额上限为 25%。你可以通过调整不同的阈值、策略或添加额外的过滤条件（例如：仅交易在 7 天内能够解决的价格分歧）来修改该策略。该策略负责处理所有交易相关的细节（如分歧检测、费用检查、风险控制以及交易执行），而具体的交易决策由用户代理（agent）负责。

## 功能概述

1. **扫描** 所有活跃市场，检测 AI 估值与市场价格之间的分歧情况。
2. **筛选** 出现超过预设阈值（默认为 2%）且费用为零的市场。
3. **进行风险控制**：检查是否存在交易反转的情况，以及用户是否已持有相关头寸。
4. **使用凯利公式（Kelly Criterion）** 来确定交易金额，并设置保守的交易上限。
5. **执行交易**：当 AI 认为市场被低估时买入，当市场被高估时卖出。

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

| 参数 | 环境变量 | 默认值 | 说明 |
|-----|---------|---------|-------------|
| `min_divergence` | `SIMMER_DIVERGENCE_MIN` | 5.0 | 用于显示的分歧百分比阈值 |
| `min_edge` | `SIMMER_DIVERGENCE_MIN_EDGE` | 0.02 | 可交易的最小分歧幅度（2%） |
| `max_bet_usd` | `SIMMER_DIVERGENCE_MAX_BET` | 单次交易的最大投注金额 |
| `max_trades_per_run` | `SIMMER_DIVERGENCE_MAX_TRADES` | 每次运行的最大交易次数 |
| `kelly_cap` | `SIMMER_DIVERGENCE_KELLY_CAP` | 凯利公式中的资金分配上限（25%） |
| `daily_budget` | `SIMMER_DIVERGENCE_DAILY_BUDGET` | 每日的交易预算上限 |
| `default_direction` | `SIMMER_DIVERGENCE_direction` | 过滤条件："牛市" 或 "熊市" |

**通过 CLI 更新配置：** `python ai_divergence.py --set max_bet_usd=10`

## 工作原理

### 分歧信号

每个市场的数据包含两个价格：
- **AI 估值**（`current_probability`）：由 Simmer 的多模型集成系统计算得出的价格（6 个大型语言模型 + 6 种交易策略 + SDK 代理的交易结果）。
- **实际市场价格**（`external_price_yes`）：Polymarket 或 Kalshi 平台上的实际市场价格。

**分歧计算公式：** `divergence = AI 估值 - 实际市场价格`

- 当 `divergence > 0` 时，AI 认为市场被低估，建议买入。
- 当 `divergence < 0` 时，AI 认为市场被高估，建议卖出。

### 凯利公式（Kelly Criterion）

交易金额的计算基于凯利公式，但会设置一个上限 `kelly_cap`（默认为 25%）以控制风险。

### 费用筛选

Polymarket 上 75% 的市场收取 0% 的交易费用，剩余的 25% 的市场收取 10% 的费用（主要针对短期交易的加密货币和体育赛事相关市场）。该策略**仅交易费用为零的市场**，以避免费用影响交易利润。

### 风险控制措施

- **费用检查**：跳过任何收取交易费用的市场。
- **交易反转检测**：利用 SDK 的上下文 API 检测是否存在自相矛盾的交易行为。
- **头寸检查**：避免在用户已持有头寸的市场进行交易。
- **每日预算限制**：当达到每日交易预算上限时停止交易。
- **保守的交易金额设定**：通过凯利公式确保不会过度投注。

## 使用的 API 端点

- `GET /api/sdk/markets/opportunities` — 获取按分歧程度排序的市场列表。
- `GET /api/sdk/context/{market_id}` — 获取特定市场的费用率和风险控制信息。
- `POST /api/sdk/trade` — 通过 SDK 客户端执行交易。
- `GET /api/sdk/positions` — 查看当前的投资组合头寸。

## 常见问题及解决方法

- **“没有符合条件市场的交易机会”**：可能是因为所有市场的分歧幅度都低于 `min_edge` 阈值。可以通过 `--set min_edge=0.01` 来降低阈值，或等待出现更大的价格分歧。
- **“每日预算已用尽”**：策略已达到每日交易预算上限。可以通过 `--set daily_budget=50` 来调整预算。
- **所有市场都被跳过（因费用问题）**：仅交易费用为零的市场。这是策略的设计初衷。
- **“上下文数据获取失败”**：可能是 SDK 的上下文 API 的请求频率限制（每分钟 18 次请求）。如果频繁执行该策略，可以减少 `max_trades_per_run` 的值。