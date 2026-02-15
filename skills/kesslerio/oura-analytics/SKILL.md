---
name: oura-analytics
description: Oura Ring的数据集成与分析功能：  
可通过Oura Cloud API获取用户的睡眠质量评分、身体状态（如“准备就绪”或“活跃”）、心率变异性（HRV）以及相关数据趋势。系统能够自动生成报告，分析这些数据与工作效率之间的关联，并在用户恢复状况不佳的日子触发警报。使用此功能需要OURA_API_TOKEN（可在cloud.ouraring.com获取）。
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":["OURA_API_TOKEN"]},"homepage":"https://github.com/kesslerio/oura-analytics-openclaw-skill"}}
---

# Oura Analytics

## 快速入门

```bash
# Set Oura API token
export OURA_API_TOKEN="your_personal_access_token"

# Fetch sleep data (last 7 days)
python {baseDir}/scripts/oura_api.py sleep --days 7

# Get readiness summary
python {baseDir}/scripts/oura_api.py readiness --days 7

# Generate weekly report
python {baseDir}/scripts/oura_api.py report --type weekly
```

## 使用场景

当需要执行以下操作时，请使用此技能：
- 获取 Oura Ring 的各项指标（睡眠质量、设备状态、活动量、心率变异性 HRV）
- 分析睡眠质量的长期变化趋势
- 研究睡眠质量与工作效率或事件之间的关联
- 设置设备状态低时的自动提醒
- 生成每日/每周/每月的健康报告

## 核心工作流程

### 1. 数据获取
```bash
export PYTHONPATH="{baseDir}/scripts"
python - <<'PY'
from oura_api import OuraClient

client = OuraClient(token="YOUR_TOKEN")
sleep_data = client.get_sleep(start_date="2026-01-01", end_date="2026-01-16")
readiness_data = client.get_readiness(start_date="2026-01-01", end_date="2026-01-16")
print(len(sleep_data), len(readiness_data))
PY
```

### 2. 趋势分析
```bash
export PYTHONPATH="{baseDir}/scripts"
python - <<'PY'
from oura_api import OuraClient, OuraAnalyzer

client = OuraClient(token="YOUR_TOKEN")
sleep_data = client.get_sleep(start_date="2026-01-01", end_date="2026-01-16")
readiness_data = client.get_readiness(start_date="2026-01-01", end_date="2026-01-16")

analyzer = OuraAnalyzer(sleep_data, readiness_data)
avg_sleep = analyzer.average_metric(sleep_data, "score")
avg_readiness = analyzer.average_metric(readiness_data, "score")
trend = analyzer.trend(sleep_data, "average_hrv")
print(avg_sleep, avg_readiness, trend)
PY
```

### 3. 提醒设置
```bash
python {baseDir}/scripts/alerts.py --days 7 --readiness 60 --efficiency 80
```

## 环境要求

必需的环境变量：
- `OURA_API_TOKEN`（用于访问 Oura Cloud API）

可选的环境变量（用于设置提醒、生成报告或指定时区/输出格式）：
- `KESSLER_TELEGRAM_BOT_TOKEN`（默认使用 `TELEGRAM_BOT_TOKEN`）
- `TELEGRAMCHAT_ID`（用于发送通知的 Telegram 聊天频道/群组 ID）
- `USER_TIMEZONE`（用户所在时区）
- `OURA_OUTPUT_DIR`（报告输出目录）

## 脚本

- `scripts/oura_api.py`：封装了 Oura Cloud API 的 Python 脚本，包含 `OuraAnalyzer` 和 `OuraReporter` 类
- `scripts/alerts.py`：基于阈值的提醒系统（命令行使用方式：`python {baseDir}/scripts/alerts.py --days 7 --readiness 60`）
- `scripts/weekly_report.py`：用于生成每周健康报告的脚本

## 参考资料

- `references/api.md`：Oura Cloud API 的官方文档
- `references/metrics.md`：各项指标的定义及解释

## 自动化配置（Cron 作业）

Cron 作业的配置应在 OpenClaw 的管理界面中进行，而非在此仓库中完成。请按照以下要求配置自动化任务：

### 每日晨间简报（上午 8:00）
```bash
openclaw cron add \
  --name "Daily Oura Health Report (Hybrid)" \
  --cron "0 8 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --wake next-heartbeat \
  --deliver \
  --channel telegram \
  --target "<YOUR_TELEGRAM_CHAT_ID>" \
  --message "Run the daily Oura health report with hybrid format: Execute bash /path/to/your/scripts/daily-oura-report-hybrid.sh"
```

### 每周睡眠报告（每周日上午 8:00）
```bash
openclaw cron add \
  --name "Weekly Oura Sleep Report" \
  --cron "0 8 * * 0" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --wake next-heartbeat \
  --deliver \
  --channel telegram \
  --target "<YOUR_TELEGRAM_CHAT_ID>" \
  --message "Run weekly Oura sleep report: bash /path/to/your/oura-weekly-sleep-alert.sh"
```

### 每日 Obsidian 记录（上午 8:15）
```bash
openclaw cron add \
  --name "Daily Obsidian Note" \
  --cron "15 8 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --wake next-heartbeat \
  --message "Create daily Obsidian note with Oura data. Run: source /path/to/venv/bin/activate && python /path/to/daily-note.py"
```

**注意：**请将 `/path/to/your/` 替换为实际的路径，将 `<YOUR_TELEGRAMCHAT_ID>` 替换为你的 Telegram 聊天频道/群组 ID。