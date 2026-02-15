---
name: polymarket
description: 查询 Polymarket 的预测市场信息。适用于有关预测市场、投注赔率、市场价格、事件概率的问题，或当用户需要 Polymarket 数据时使用。
---

# Polymarket

通过 Polymarket 的公共 API 查询预测市场数据（无需认证）。

## 快速入门

```bash
# Top markets by 24h volume
python3 scripts/polymarket.py --top

# Search markets
python3 scripts/polymarket.py --search "trump"

# Get specific market by slug
python3 scripts/polymarket.py --slug "will-trump-win-the-2024-election"

# List events (grouped markets)
python3 scripts/polymarket.py --events
```

## 脚本位置

`skills/polymarket/scripts/polymarket.py`

## API 端点

该脚本使用 `gamma-api.polymarket.com`：
- `/markets` - 显示各个市场的数据，包括价格和成交量
- `/events` - 包含相关市场的事件组

## 输出格式

市场数据包括：问题内容、答案的“是/否”概率（以百分比表示）、24 小时成交量以及总成交量。

## 解释价格数据

- `outcomePrices` 的取值范围为 0-1，代表概率：
  - 如果 `outcomePrices` 为 0.65，则表示市场认为“是”的概率为 65%
- 成交量越大，市场流动性越强，信号越可靠