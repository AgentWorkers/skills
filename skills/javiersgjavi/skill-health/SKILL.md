---
name: skill-health
description: "分析可穿戴设备生成的健康数据CSV文件（包括步数、心率、睡眠质量、消耗的卡路里、血氧饱和度（SpO2）、运动数据以及行走距离），并生成结构紧凑的JSON报告。这些报告可以按小时、每天、每周、每月以及过去30小时的睡眠数据来生成，同时支持跨时间段的统计分析。该功能适用于在运行Skill Health分析工具或整理分析结果时使用，也可用于解释输出数据的含义、数据质量以及需要注意的潜在问题。"
---
# 技能健康状况（Skill Health）

## 使用方法

运行 `scripts/` 目录下的分析脚本时，可以使用 `--data-path`（ZIP 文件或文件夹路径）或 `--data-dir`（包含健康数据文件的目录路径）参数。每个脚本会将分析结果以 JSON 格式输出到标准输出（stdout），也可以通过 `--output-dir` 参数将结果写入指定文件。

如果需要正确解析 CSV 格式的时间戳（在将其序列化为 UTC 之前），请使用 `--timezone` 参数（例如：`Europe/Madrid` 或 `America/New_York`）来指定时区。

**最小示例：**

```bash
python scripts/run_sleep.py --data-path data/health_data_latest.zip --output-dir outputs
python scripts/run_daily.py --data-path data/health_data_latest.zip --output-dir outputs
python scripts/run_cross_alerts.py --outputs-dir outputs --output-dir outputs
```

## 注意事项

- 睡眠指标的文件后缀为 `last_{window_hours}h`（默认为 `last_30h`）。
- 输出结果为压缩格式的 JSON 数据（`time_window` 使用 `s/e/r` 格式，`data_quality` 使用 `cov/rel` 格式）。
- 所需依赖库：Python 3.10 及以上版本和 `pandas`。

## 参考资料

- `references/overview.md`（数据结构、输出格式及关键决策）
- `references/operations.md`（执行窗口设置、质量评估规则）