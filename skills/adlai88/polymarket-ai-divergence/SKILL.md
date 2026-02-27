---
name: polymarket-ai-divergence
displayName: Polymarket AI Divergence
description: 寻找那些 Simmer 的 AI 估值与实际市场价格存在差异的市场，然后利用 Kelly 算法在价格被高估或低估的一侧进行交易。系统会扫描这些差异，检查相关费用和风险保障措施，并在费用为零的市场中执行交易（前提是具备足够的交易优势）。
metadata: {"clawdbot":{"emoji":"🔮","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false,"automaton":{"managed":true,"entrypoint":"ai_divergence.py"},"tunables":[{"env":"SIMMER_DIVERGENCE_MIN_EDGE","type":"number","default":0.05,"range":[0.01,0.30],"step":0.01,"label":"Minimum edge threshold"},{"env":"SIMMER_DIVERGENCE_MAX_BET_USD","type":"number","default":50,"range":[1,200],"step":5,"label":"Max bet per trade"},{"env":"SIMMER_DIVERGENCE_KELLY_CAP","type":"number","default":0.25,"range":[0.01,1.0],"step":0.01,"label":"Kelly fraction cap"},{"env":"SIMMER_DIVERGENCE_DAILY_BUDGET_USD","type":"number","default":100,"range":[10,500],"step":10,"label":"Daily budget"},{"env":"SIMMER_DIVERGENCE_MAX_TRADES_PER_RUN","type":"number","default":5,"range":[1,20],"step":1,"label":"Max trades per run"},{"env":"SIMMER_DIVERGENCE_DIRECTION_FILTER","type":"enum","default":"any","options":["any","yes_only","no_only"],"label":"Direction filter"}]}}
authors:
  - Simmer (@simmer_markets)
version: "2.0.2"
published: true
---
# Polymarket AI 分歧交易策略

该策略用于寻找 Simmer 的 AI 预测价格与实际市场价格出现分歧的市场，并利用这种价格差异进行交易。

> **这是一个模板。** 默认逻辑是在 AI 预测价格与实际价格的偏差超过 2% 时进行交易，且每次交易的投注金额上限为 25%（遵循 Kelly 算法）。您可以根据需要修改该策略，设置不同的交易阈值、投注策略或额外过滤条件（例如：仅交易在 7 天内能够完成交易的市场）。该策略负责处理所有的交易相关流程（包括价格差异的检测、费用检查、风险控制以及交易执行），而具体的交易决策由您的代理程序（agent）负责。

## 功能概述

1. **扫描** 所有活跃市场，检测 AI 预测价格与实际市场价格之间的差异。
2. **筛选** 出现超过预设阈值（默认为 2%）且交易费用为零的市场。
3. **检查** 相关风险控制机制（例如：检测市场趋势的突然反转、以及用户已持有的头寸情况）。
4. **确定投注金额**：使用 Kelly 算法进行计算，并设置保守的投注上限。
5. **执行交易**：在 AI 预测价格被低估的市场进行买入（当 AI 表示看涨时），或在 AI 预测价格被高估的市场进行卖出（当 AI 表示看跌时）。

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
| `min_divergence` | `SIMMER_DIVERGENCE_MIN` | 5.0 | 显示价格差异的最低百分比阈值 |
| `min_edge` | `SIMMER_DIVERGENCE_MIN_EDGE` | 0.02 | 可交易的最低价格差异阈值（2%） |
| `max_bet_usd` | `SIMMER_DIVERGENCE_MAX_BET` | 每次交易的最高投注金额（美元） |
| `max_trades_per_run` | `SIMMER_DIVERGENCE_MAX_TRADES` | 每次运行周期的最大交易次数 |
| `kelly_cap` | `SIMMER_DIVERGENCE_KELLY_CAP` | Kelly 算法中的投注比例上限（25%） |
| `daily_budget` | `SIMMER_DIVERGENCE_DAILY_BUDGET` | 每日的交易预算上限 |
| `default_direction` | `SIMMER_DIVERGENCE_direction` | 过滤条件："看涨" 或 "看跌" |

**通过 CLI 更新配置：** `python ai_divergence.py --set max_bet_usd=10`

## 工作原理

### 价格差异信号

每个市场的数据包含两个价格：
- **AI 预测价格**（`current_probability`）：基于多模型集成预测得出的价格。
- **实际市场价格**（`external_price_yes`）：Polymarket/Kalshi 平台上的实际市场价格。

**价格差异 = AI 预测价格 - 实际市场价格**

- 当价格差异大于 0 时：AI 认为市场被低估 → 执行买入操作。
- 当价格差异小于 0 时：AI 认为市场被高估 → 执行卖出操作。

### Kelly 算法用于确定投注金额

投注金额的计算遵循 Kelly 算法：
```
kelly_fraction = edge / (1 - price)
position_size = kelly_fraction * max_bet_usd
```
同时，投注金额的上限被设置为 `kelly_cap`（默认为 25%），以控制风险。

### 费用筛选

Polymarket 上 75% 的市场交易费用为零；剩余的 25% 的市场收取 10% 的交易费用（主要针对短期交易的加密货币和体育赛事相关市场）。该策略**仅交易费用为零的市场**，以避免费用对投资回报产生负面影响。

### 风险控制机制

- **费用检查**：跳过任何存在交易费用的市场。
- **趋势反转检测**：利用 SDK 的上下文 API 检测交易策略的矛盾之处。
- **头寸检查**：避免在用户已持有头寸的市场进行交易。
- **每日预算限制**：当达到每日交易预算上限时，停止交易。
- **保守的投注策略**：通过 Kelly 算法确保不会过度投注。

## 使用的 API 端点

- `GET /api/sdk/markets/opportunities`：获取按价格差异排序的市场列表。
- `GET /api/sdk/context/{market_id}`：获取特定市场的费用率和风险控制信息。
- `POST /api/sdk/trade`：通过 SDK 客户端执行交易。
- `GET /api/sdk/positions`：获取当前的投资组合持仓情况。

## 常见问题及解决方法

- **“没有符合交易条件的市场”**：所有市场的价格差异都低于 `min_edge` 阈值。可以通过 `--set min_edge=0.01` 来降低该阈值，或等待出现更大的价格差异。
- **“每日预算已用完”**：策略已达到每日交易预算上限。可以通过 `--set daily_budget=50` 来调整预算。
- **所有市场都被跳过（因为费用问题）**：仅交易费用为零的市场。如果所有可交易的市场都存在费用问题，策略将不会执行任何交易。这是该策略的设计初衷。
- **“上下文数据获取失败”**：可能是由于 SDK 的上下文 API 的请求频率限制（每分钟 18 次请求）。如果频繁执行该策略，可以减少 `max_trades_per_run` 的值。