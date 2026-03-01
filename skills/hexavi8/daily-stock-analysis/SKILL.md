---
name: daily-stock-analysis
description: 一种用于全球股票的确定性每日股票分析工具。适用于用户需要每日分析、下一个交易日的收盘价预测、历史预测数据回顾、滚动准确性评估以及生成可靠的Markdown格式报告的场景。
---
# 每日股票分析

系统会进行基于市场数据的每日股票分析，包括预测、后续评估、滚动准确率跟踪以及一个结构化的自我优化机制，该机制会根据观察到的预测误差更新未来的分析假设。

## 基本规则

1. 仅在 `working_directory` 目录下读取和写入文件。
2. 新报告仅保存到：
   - `<working_directory>/daily-stock-analysis/reports/`
3. 文件命名规则为：
   - `YYYY-MM-DD-<TICKER>-analysis.md`
4. 如果存在相同股票代码/日期的文件，系统会询问用户：
      - 是否覆盖现有文件，或创建新版本（例如 `-v2`、`-v3` 等）；
   - 在无人值守的情况下，系统默认创建新版本。
5. 在进行新的预测之前，务必查看历史数据。
6. 为控制令牌使用量，限制历史数据的读取数量：
   - 脚本模式：最多读取 5 份历史报告
   - 兼容模式：最多读取 3 份历史报告

## 必需使用的脚本（优先使用）

1. 规划输出路径并收集历史数据：
   ```bash
python3 {baseDir}/scripts/report_manager.py plan \
  --workdir <working_directory> \
  --ticker <TICKER> \
  --run-date <YYYY-MM-DD> \
  --versioning auto \
  --history-limit 5
```

2. 从现有报告中计算滚动准确率：
   ```bash
python3 {baseDir}/scripts/calc_accuracy.py \
  --workdir <working_directory> \
  --ticker <TICKER> \
  --windows 1,3,7,30 \
  --history-limit 60
```

3. （可选）在用户明确确认后，迁移旧版本文件：
   ```bash
python3 {baseDir}/scripts/report_manager.py migrate \
  --workdir <working_directory> \
  --file <ABS_PATH_1> --file <ABS_PATH_2>
```

## 兼容模式（无 Python / 使用小型模型）

如果无法使用 Python 脚本或模型功能有限，可切换到最小化模式：
1. 为同一股票代码最多读取 3 份最新的报告。
2. 仅使用以下有限的资料来源：
   - 一个官方信息披露来源
   - 一个可靠的市场数据来源（Yahoo Finance 可接受）
3. 仅输出简洁的结果：
   - 投资建议
   - 预测收盘价 (`pred_close_t1`)
   - 之前的评估结果（`prev_pred_close_t1`、`prev_actual_close_t1`、`AE`、`APE`，如有的话）
   - 一项改进措施 (`improvement_action`)
4. 按照相同的文件命名规则将报告保存到指定的目录中。
详细信息请参阅 `references/minimal_mode.md`。

## 最小化运行流程

1. 确认股票代码、交易所和市场信息（如有疑问，请询问）。
2. 运行 `report_manager.py plan` 脚本。
3. 读取脚本返回的历史数据文件。
4. 如果存在旧版本文件，列出所有文件的绝对路径并询问用户是否需要迁移。
5. 根据 `references/sources.md` 和 `references/search_queries.md` 中的说明收集数据。
6. 运行 `calc_accuracy.py` 计算各项指标。
7. 使用 `references/report_template.md` 模板生成报告。
8. 将报告保存到 `report_manager.py` 返回的指定输出文件中。

## 必需的输出字段

必须包含以下内容：
- 投资建议 (`recommendation`)
- 预测收盘价 (`pred_close_t1`)
- 之前的预测收盘价 (`prev_pred_close_t1`)
- 之前的实际收盘价 (`prev_actual_close_t1`)
- 相对误差 (`AE`) 和平均绝对误差 (`APE`)
- 滚动准确率（严格/宽松标准）
- 改进措施 (`improvement_actions`）

## 自我优化（强制要求）

每次运行都必须根据之前的预测错误提出 1-3 项具体的改进措施，并在下次运行中应用这些措施。请勿跳过此步骤。

## 安排建议

建议用户将此任务设置为工作日的定期任务（例如当地时间 10:00），以确保预测和评估工作的连续性。

## 参考资料

默认参考资料：
- `references/workflow.md`
- `references/report_template.md`
- `references/metrics.md`
- `references/search_queries.md`
- `references/sources.md`
- `references/minimal_mode.md`
- `references/security.md`

如需深入分析（`full_report` 模式）：
- `references/fundamental-analysis.md`
- `references/technical-analysis.md`
- `references/financial-metrics.md`

## 合规性声明

请务必在报告末尾添加以下声明：
“本内容仅用于研究和信息提供目的，不构成投资建议或收益保证。市场存在风险，请谨慎投资。”