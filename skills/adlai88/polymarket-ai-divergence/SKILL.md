---
name: polymarket-ai-divergence
displayName: Polymarket AI Divergence
description: 寻找那些 Simmer 的 AI 估值与实际市场价格出现分歧的市场，然后利用 Kelly 算法在价格被高估或低估的一侧进行交易。系统会扫描市场中的价格分歧情况，检查相关费用和风险保障措施，并在费用为零的市场中执行交易（前提是这些市场具有足够的交易优势）。
metadata: {"clawdbot":{"emoji":"🔮","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false,"automaton":{"managed":true,"entrypoint":"ai_divergence.py"}}}
authors:
  - Simmer (@simmer_markets)
version: "2.0.1"
published: true
---
# Polymarket AI 分歧交易策略

该策略用于寻找 Simmer 的 AI 预测结果与实际市场价格存在分歧的市场，并利用这种分歧进行交易。

> **这是一个模板。** 默认逻辑是在 AI 预测与市场价格的分歧超过 2% 时进行交易，且每次交易的资金使用比例上限为 25%（遵循 Kelly 定理）。你可以通过调整不同的阈值、资金使用策略或额外过滤器（例如：仅交易在 7 天内能够解决的价格分歧的市场）来修改该策略。该策略负责处理所有的交易相关细节（包括分歧检测、费用检查、风险控制以及交易执行），而具体的交易决策由你的代理程序（agent）来完成。

## 功能概述

1. **扫描** 所有活跃市场，检测 AI 预测价格与实际市场价格之间的分歧情况。
2. **筛选** 出现超过预设阈值（默认为 2%）且交易费用为零的市场。
3. **进行风险控制**：检查是否存在与先前交易方向相反的新交易（即“翻转交易”），以及用户是否已持有该市场的头寸。
4. **确定交易规模**：使用 Kelly 定理来计算交易金额，并设置保守的资金上限。
5. **执行交易**：当 AI 预测市场价格上涨时买入，预测市场价格下跌时卖出。

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
| `min_divergence` | `SIMMER_DIVERGENCE_MIN` | 5.0 | 分歧百分比的最低阈值（用于显示） |
| `min_edge` | `SIMMER_DIVERGENCE_MIN_EDGE` | 0.02 | 可交易的最低分歧幅度（2%） |
| `max_bet_usd` | `SIMMER_DIVERGENCE_MAX_BET` | 每笔交易的最大投注金额（美元） |
| `max_trades_per_run` | `SIMMER_DIVERGENCE_MAX_TRADES` | 每次运行时的最大交易次数 |
| `kelly_cap` | `SIMMER_DIVERGENCE_KELLY_CAP` | Kelly 定理资金使用比例的上限（25%） |
| `daily_budget` | `SIMMER_DIVERGENCE_DAILY_BUDGET` | 每日的交易预算上限 |
| `default_direction` | `SIMMER_DIVERGENCE_direction` | 过滤条件：“上涨”或“下跌” |

通过 CLI 更新配置：`python ai_divergence.py --set max_bet_usd=10`

## 工作原理

### 分歧信号

每个被扫描的市场都有两个价格：
- **AI 预测价格**（`current_probability`）：基于多模型集成预测得出的 Simmer AI 的预测价格。
- **实际市场价格**（`external_price_yes`）：Polymarket 或 Kalshi 平台上的实际市场价格。

**分歧计算公式：** `divergence = AI 预测价格 - 实际市场价格`

- 当 `divergence > 0` 时，AI 认为市场价格被低估 → 选择买入。
- 当 `divergence < 0` 时，AI 认为市场价格被高估 → 选择卖出。

### Kelly 定理资金使用

交易规模根据 Kelly 定理来计算：
```
kelly_fraction = edge / (1 - price)
position_size = kelly_fraction * max_bet_usd
```
同时，交易金额上限被设置为 `kelly_cap`（默认为 25%），以控制风险。

### 费用筛选

Polymarket 上 75% 的市场交易费用为零；剩余 25% 的市场收取 10% 的费用（主要针对短期交易的加密货币和体育赛事相关市场）。该策略**仅交易费用为零的市场**，以避免费用对交易利润造成负面影响。

### 风险控制措施

- **费用检查**：跳过任何存在交易费用的市场。
- **翻转交易检测**：利用 SDK 的上下文 API 检测是否存在自相矛盾的交易行为。
- **头寸检查**：避免在用户已持有该市场头寸的情况下进行交易。
- **每日预算限制**：当达到每日交易预算上限时停止交易。
- **保守的资金使用策略**：通过 Kelly 定理确保不会过度投注。

## 使用的 API 端点

- `GET /api/sdk/markets/opportunities`：获取按分歧程度排序的市场列表。
- `GET /api/sdk/context/{market_id}`：获取特定市场的费用率和风险控制规则。
- `POST /api/sdk/trade`：通过 SDK 客户端执行交易。
- `GET /api/sdk/positions`：获取当前的投资组合持仓情况。

## 常见问题解决方法

- **“没有符合条件市场的交易机会”**：可能是所有市场的分歧幅度都低于 `min_edge` 阈值。可以通过 `--set min_edge=0.01` 来降低阈值，或等待出现更大的价格分歧。
- **“每日预算已用完”**：策略已达到每日交易预算上限。可以通过 `--set daily_budget=50` 来调整预算。
- **所有市场均因费用问题被跳过**：仅交易费用为零的市场。如果所有可交易的市场都收取费用，则不会执行任何交易。这是该策略的设计初衷。
- **“上下文信息获取失败”**：可能是 SDK 的上下文 API 被限制了请求频率（每分钟 18 次请求）。如果频繁执行该策略，可以减少 `max_trades_per_run` 的值。