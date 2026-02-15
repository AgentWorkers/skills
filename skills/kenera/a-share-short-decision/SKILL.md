---
name: A股短线交易决策 A-Share Short-Term Decision
slug: a-share-short-decision
description: A股短期交易决策技巧，适用于1-5天的时间范围。适用于需要实时市场情绪数据、行业轮动分析、强势股票筛选、资金流向确认、基于日期的短期交易信号评估、交易预测记录以及次日市场走势对比的场景，尤其适用于中国A股的动量交易策略。
---

# A-Share短期决策技能

按照以下顺序执行操作：

1. 对目标日期运行 `short_term_signal_engine(analysis_date)`。
2. 如有需要，使用 `run_prediction_for_date(analysis_date)` 保存预测结果。
3. 使用 `compare_prediction_with_market(prediction_date, actual_date)` 将预测结果与实际市场情况进行比较。
4. 使用 `generate_daily_report(analysis_date)` 生成报告。

## 工具接口

### `short_term_signal_engine(analysis_date=None)`

- `analysis_date`：格式为 `YYYY-MM-DD` 或 `YYYYMMDD`
- 返回加权的短期评分及推荐状态。
- 当不存在可交易的标的时，始终返回友好的提示信息 `no_recommendation_message`。

### `run_prediction_for_date(analysis_date)`

- 为指定日期运行信号引擎。
- 将决策结果写入 `data/decision_log.jsonl` 文件中。

### `compare_prediction_with_market(prediction_date, actual_date=None)`

- 从日志中加载预测结果（如果缺失则自动生成）。
- 将预测的标的与 `actual_date` 当天的实际市场收盘价进行比较。
- 返回每只股票的收益及统计摘要。

## 无推荐行为

- 确保输出结果不为空。
- 如果 `candidates` 为空或信号状态为 `NO_TRADE`，则明确提示：“当前暂无可执行的短线买入标的”。
- 需要说明原因并提供下一步操作建议。

## 运行时代码

```bash
python3 main.py short_term_signal_engine --date 2026-02-12
python3 main.py run_prediction_for_date --date 2026-02-12
python3 main.py compare_prediction_with_market --prediction-date 2026-02-12 --actual-date 2026-02-13
python3 main.py generate_daily_report --date 2026-02-12
```

## 子技能工作流程

对于“优化-推荐”的循环流程，执行以下操作：

```bash
python3 subskills/config-optimization/optimize_from_aggressive.py --analysis-period "2026-02-01 to 2026-02-12"
python3 subskills/daily-recommendation/generate_daily_recommendation.py --date 2026-02-14
```

所有生成的文件都存储在 `data/` 目录下。