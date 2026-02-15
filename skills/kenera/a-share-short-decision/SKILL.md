---
name: a-share-short-decision
description: A股短期交易决策工具，适用于1-5天的投资周期。适用于需要了解市场情绪、行业轮动情况、筛选强势股票、确认资金流向、对短期交易信号进行加权评估、实施严格的风险控制以及生成每日交易报告的场景，尤其适合用于A股市场的趋势交易策略。
---

# A-Share短期决策技能

按照以下顺序执行短期决策：

1. 运行 `get_market_sentiment`。
2. 运行 `get_sector_rotation`。
3. 使用选定的行业板块运行 `scan_strong_stocks`。
4. 对顶级候选股票运行 `analyze_capital_flow`。
5. 运行 `short_term_signal_engine`。
6. 应用 `short_term_risk_control`。
7. 使用 `generate_daily_report` 输出每日摘要。

## 工具合约

### `get_market_sentiment()`

返回值：

```json
{
  "limit_up": 65,
  "limit_down": 4,
  "max_height": 4,
  "break_rate": 0.18,
  "market_sentiment_score": 72
}
```

### `get_sector_rotation(top_n=5)`

返回值：

```json
{
  "top_sectors": [
    {"name": "AI-Compute", "strength": 85.2}
  ]
}
```

### `scan_strong_stocks(sectors=None, top_n=10)`

筛选规则：
- 日涨幅 > 5%
- 成交量比率 > 1.5
- 3天上涨趋势
- 排除成交量大的看跌蜡烛图

### `analyze_capital_flow(symbol=None)`

返回值：

```json
{
  "main_flow": 180000000,
  "flow_trend": "3-day-inflow"
}
```

### `short_term_signal_engine()`

权重：
- 市场情绪 25%
- 行业板块强度 25%
- 股票成交量强度 20%
- 资本流入 20%
- 技术形态 10%

信号策略：
- 分数 >= 75：`SHORT_BUY`（买入）
- 60~75：`WATCHLIST`（观察名单）
- <60：`NO_TRADE`（不交易）

### `short_term_risk_control(market_sentiment_score)`

规则：
- 最大持仓比例 <= 15%
- 当市场情绪低于40%时，强制止损
- 当市场情绪低于40%时，禁止新仓入场

### `generate_daily_report()`

输出每日文本报告，内容包括：
- 市场情绪
- 行业板块表现最强的股票
- 短期关注股票
- 风险控制与交易建议

## 运行环境

请始终使用包含此 `SKILL.md` 文件的目录作为技能执行的根目录。

使用方法：

```bash
python main.py short_term_signal_engine
python main.py generate_daily_report
```