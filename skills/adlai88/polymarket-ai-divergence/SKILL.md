---
name: polymarket-ai-divergence
displayName: Polymarket AI Divergence
description: 寻找那些 Simmer 的 AI 估值与实际市场价格存在差异的市场，然后利用 Kelly 定量交易策略在价格被高估或低估的一侧进行交易。系统会扫描这些差异，检查相关费用及交易保障措施，并在费用为零的市场中执行具有足够优势的交易。
metadata: {"clawdbot":{"emoji":"🔮","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false,"automaton":{"managed":true,"entrypoint":"ai_divergence.py"},"tunables":[{"env":"SIMMER_DIVERGENCE_MIN_EDGE","type":"number","default":0.05,"range":[0.01,0.30],"step":0.01,"label":"Minimum edge threshold"},{"env":"SIMMER_DIVERGENCE_MAX_BET_USD","type":"number","default":50,"range":[1,200],"step":5,"label":"Max bet per trade"},{"env":"SIMMER_DIVERGENCE_KELLY_CAP","type":"number","default":0.25,"range":[0.01,1.0],"step":0.01,"label":"Kelly fraction cap"},{"env":"SIMMER_DIVERGENCE_DAILY_BUDGET_USD","type":"number","default":100,"range":[10,500],"step":10,"label":"Daily budget"},{"env":"SIMMER_DIVERGENCE_MAX_TRADES_PER_RUN","type":"number","default":5,"range":[1,20],"step":1,"label":"Max trades per run"},{"env":"SIMMER_DIVERGENCE_DIRECTION_FILTER","type":"enum","default":"any","options":["any","yes_only","no_only"],"label":"Direction filter"}]}}
authors:
  - Simmer (@simmer_markets)
version: "2.0.2"
difficulty: intermediate
published: true
---
# Polymarket AI 分歧交易策略

该策略用于寻找 Simmer 的 AI 预测价格与实际市场价格出现分歧的市场，并利用这种价格差异进行交易。

> **这是一个模板。** 默认逻辑是在 AI 预测价格与实际价格的差异超过 2% 时进行交易，且每次交易的资金占用量上限为 25%（根据 Kelly 公式计算）。您可以根据需要修改该策略，设置不同的交易阈值、资金分配策略或添加额外的过滤条件（例如：仅交易在 7 天内能够成交的市场）。该策略负责处理所有交易相关的细节工作（包括价格差异的检测、费用检查、风险控制以及交易执行），而具体的交易决策由您的代理系统（agent）负责。

## 功能概述

1. **扫描** 所有活跃市场，检测 AI 预测价格与实际市场价格之间的差异。
2. **筛选** 出现超过预设阈值（默认为 2%）且费用为零的市场。
3. **进行风险控制**：检查是否存在与先前交易方向相反的新交易（即“翻转交易”情况），以及用户是否已持有相关头寸。
4. **确定交易规模**：使用 Kelly 公式计算交易金额，并设置保守的资金上限。
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
|-------|---------|---------|-------------|
| `min_divergence` | `SIMMER_DIVERGENCE_MIN` | 5.0 | 显示结果时使用的最小价格差异百分比 |
| `min_edge` | `SIMMER_DIVERGENCE_MIN_EDGE` | 0.02 | 可进行交易的最小价格差异百分比（2%） |
| `max_bet_usd` | `SIMMER_DIVERGENCE_MAX_BET` | 每次交易的最大投注金额（美元） |
| `max_trades_per_run` | `SIMMER_DIVERGENCE_MAX_TRADES` | 每次运行时的最大交易次数 |
| `kelly_cap` | `SIMMER_DIVERGENCE_KELLY_CAP` | Kelly 公式计算的资金占用上限比例（默认为 25%） |
| `daily_budget` | `SIMMER_DIVERGENCE_DAILY_BUDGET` | 每日的交易预算上限 |
| `default_direction` | `SIMMER_DIVERGENCE_direction` | 过滤条件：" bullish"（看涨）或 "bearish"（看跌） |

**通过 CLI 更新配置：** `python ai_divergence.py --set max_bet_usd=10`

## 工作原理

### 价格差异信号

每个被扫描的市场都有两个价格：
- **AI 预测价格**（`current_probability`）：基于多模型集成预测得出的价格。
- **实际市场价格**（`external_price_yes`）：Polymarket/Kalshi 平台上的实际市场价格。

**价格差异计算公式：** `divergence = AI 预测价格 - 实际市场价格`

- 当 `divergence > 0` 时，AI 认为市场被低估，建议买入。
- 当 `divergence < 0` 时，AI 认为市场被高估，建议卖出。

### Kelly 公式用于确定交易规模

交易金额的计算使用 Kelly 公式：
```
kelly_fraction = edge / (1 - price)
position_size = kelly_fraction * max_bet_usd
```
同时，交易金额的上限被设置为 `kelly_cap`（默认为 25%），以控制风险。

### 费用筛选

Polymarket 上 75% 的市场免收交易费用，剩余 25% 的市场收取 10% 的费用（主要针对短期交易的加密货币和体育赛事相关市场）。该策略**仅交易免费市场**，以避免费用影响交易利润。

### 风险控制措施

- **费用检查**：跳过任何收取交易费用的市场。
- **翻转交易检测**：利用 SDK 的上下文 API 检测是否存在自相矛盾的交易行为。
- **头寸检查**：避免在用户已持有头寸的市场进行交易。
- **每日预算限制**：达到每日交易预算上限时停止交易。
- **保守的资金分配**：通过 Kelly 公式确保不会过度投注。

## 使用的 API 端点

- `GET /api/sdk/markets/opportunities`：获取按价格差异排序的市场列表。
- `GET /api/sdk/context/{market_id}`：获取特定市场的费用率和风险控制规则。
- `POST /api/sdk/trade`：通过 SDK 客户端执行交易。
- `GET /api/sdk/positions`：获取当前的投资组合持仓情况。

## 常见问题解决方法

- **“没有符合条件市场”**：所有市场的价格差异都低于 `min_edge` 设置。可以通过 `--set min_edge=0.01` 降低阈值，或等待出现更大的价格差异。
- **“每日预算已用完”**：策略达到了每日交易预算上限。可以通过 `--set daily_budget=50` 调整预算。
- **所有市场都被跳过（因费用问题）**：仅交易免费市场。如果所有可交易的市场都收取费用，则不会执行任何交易。这是该策略的设计初衷。
- **“上下文信息获取失败”**：可能是 SDK 的上下文 API 被限制了请求频率（每分钟 18 次请求）。如果频繁执行该策略，请减少 `max_trades_per_run` 的值。