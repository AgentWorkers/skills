---
name: simmer-calibration-report
displayName: "Simmer Calibration Report"
description: 在任何 Simmer 交易日志上运行校准报告。可以按策略、一天中的时间、价格区间和市场类型来分解胜率和预期收益（EV）。这样你就能清楚地知道自己的优势在哪里——以及劣势在哪里。
version: "1.0.4"
authors:
  - name: "DjDyll"
difficulty: "beginner"
---
# 📊 Simmer 校准报告

你可能认为自己很了解自己的交易能力，但这份报告能帮你验证这种认知是否正确。

> **注意：** 这只是一个模板。只需将其指向任何 Simmer JSONL 交易日志文件（无论是实时的、模拟的，还是从其他地方导出的），就能获得完整的校准结果。该工具不包含任何特定策略的逻辑处理；所有数据都来自你的交易日志。

## 设置

1. 安装所需依赖库：
   ```bash
   pip install simmer-sdk
   ```

2. 设置你的 API 密钥：
   ```bash
   export SIMMER_API_KEY=your_key_here
   ```

3. 运行脚本：
   ```bash
   python calibration_report.py --live
   ```

就这么简单。如果你的交易日志文件位于默认路径下，脚本就能自动执行校准操作。

## 配置参数

| 参数          | 环境变量          | 默认值        | 说明                          |
|----------------|------------------|-------------|--------------------------------------------|
| `journal_path`    | `CALIB_JOURNAL_PATH`    | `""`        | 交易日志文件的 JSONL 格式路径；空值表示自动检测路径。       |
| `min_trades`     | `CALIB_MIN_TRADES`     | `10`        | 显示交易记录的最小交易数量；低于此数量，则无法生成完整数据。       |
| `lookback_days`    | `CALIB_lookBACK_days`    | `30`        | 分析数据的时间范围（以天为单位）。                   |
| `include_unresolved` | `CALIB_INCLUDE_UNRESOLVED` | `false`        | 是否包含未完成的交易记录；包含未完成交易会导致评估值（EV）的准确性降低。 |

配置参数可以直接在脚本中设置：
```bash
python calibration_report.py --set lookback_days=60
python calibration_report.py --set min_trades=5
```

## 快速命令

```bash
# Sim journal (dry run data)
python calibration_report.py

# Live journal
python calibration_report.py --live

# Custom journal path
CALIB_JOURNAL_PATH=/path/to/journal.jsonl python calibration_report.py

# Show config
python calibration_report.py --config

# Summary only (good for cron)
python calibration_report.py --live --quiet
```

## 示例输出

```
📊 Calibration Report — Last 30 days
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 287 trades | 68.3% WR | +$0.038 EV/trade
Journal: data/live/trade_journal.jsonl

BY STRATEGY
  btc_momentum         n=142  WR=72.5%  EV=+0.047  ██████████████
  eth_midcandle        n=67   WR=61.2%  EV=+0.021  ██████
  btc_midcandle_scalp  n=49   WR=65.3%  EV=+0.031  ████████
  eth_btc_lag          n=29   WR=58.6%  EV=+0.015  ████

BY HOUR (UTC)
  00-06                n=44   WR=75.0%  EV=+0.055  ██████████████████
  06-12                n=89   WR=70.8%  EV=+0.044  ████████████████
  12-18                n=97   WR=65.0%  EV=+0.031  ██████████
  18-24                n=57   WR=64.9%  EV=+0.028  █████████

BY ENTRY PRICE
  0.20-0.35            n=38   WR=73.7%  EV=+0.052  ██████████████████
  0.35-0.50            n=71   WR=70.4%  EV=+0.041  █████████████
  0.50-0.65            n=89   WR=66.3%  EV=+0.033  ██████████
  0.65-0.80            n=61   WR=63.9%  EV=+0.024  ████████

🏆 Best segment: btc_momentum (EV=+0.047, WR=72.5%)
```

## 故障排除

| 故障现象        | 解决方法                                      |
|----------------|--------------------------------------------|
| “未找到交易日志”     | 明确设置 `CALIB_JOURNAL_PATH`，或确保 `data/live/trade_journal.jsonl` 文件存在于工作目录中。 |
| 未显示任何交易记录   | 交易尚未完成；将 `CALIB_INCLUDE_UNRESOLVED` 设置为 `true` 以查看未完成的交易（此时评估值可能不准确）。 |
| 无法生成完整数据    | 交易数量少于 `min_trades` 的阈值；调整该参数：`python calibration_report.py --set min_trades=5` |
| “未设置 SIMMER_API_KEY” | 使用 `export SIMMER_API_KEY=your_key_here` 命令设置 API 密钥。       |
| “未安装 simmer-sdk”   | 使用 `pip install simmer-sdk` 安装相关库。                   |