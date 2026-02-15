---
name: fitbit-analytics
description: **Fitbit健康与健身数据集成**  
通过Fitbit Web API获取用户的步数、心率、睡眠质量、活动量、消耗的卡路里以及相关数据趋势。支持自动生成健康报告和提醒。  
所需参数：  
- FITBIT_CLIENT_ID  
- FITBIT_CLIENT_SECRET  
- FITBIT_ACCESS_TOKEN  
- FITBIT_REFRESH_TOKEN
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":["FITBIT_CLIENT_ID","FITBIT_CLIENT_SECRET","FITBIT_ACCESS_TOKEN","FITBIT_REFRESH_TOKEN"]},"homepage":"https://github.com/kesslerio/fitbit-analytics-openclaw-skill"}}
---

# Fitbit Analytics

## 快速入门

```bash
# Set Fitbit API credentials
export FITBIT_CLIENT_ID="your_client_id"
export FITBIT_CLIENT_SECRET="your_client_secret"
export FITBIT_ACCESS_TOKEN="your_access_token"
export FITBIT_REFRESH_TOKEN="your_refresh_token"

# Generate morning briefing with Active Zone Minutes
python scripts/fitbit_briefing.py

# Fetch daily steps
python scripts/fitbit_api.py steps --days 7

# Get heart rate data
python scripts/fitbit_api.py heartrate --days 7

# Sleep summary
python scripts/fitbit_api.py sleep --days 7

# Generate weekly health report
python scripts/fitbit_api.py report --type weekly

# Get activity summary
python scripts/fitbit_api.py summary --days 7
```

## 使用场景

适用于以下场景：
- 获取Fitbit的健康数据（步数、卡路里、心率、睡眠质量）
- 分析长期的活动趋势
- 设置不活动或心率异常的提醒
- 生成每日/每周的健康报告

## 核心工作流程

### 1. 每日简报
```bash
# Generate morning health briefing (includes Active Zone Minutes)
python scripts/fitbit_briefing.py                    # Today's briefing
python scripts/fitbit_briefing.py --date 2026-01-20  # Specific date
python scripts/fitbit_briefing.py --format brief     # 3-line summary
python scripts/fitbit_briefing.py --format json      # JSON output

# Example output includes:
# - Yesterday's activities (logged exercises)
# - Yesterday's Active Zone Minutes (total, Fat Burn, Cardio, Peak)
# - Today's activity summary (steps, calories, floors, distance)
# - Heart rate (resting, average, zones)
# - Sleep (duration, efficiency, awake episodes)
# - Trends vs 7-day average
```

**示例JSON输出：**
```json
{
  "date": "2026-01-21",
  "steps_today": 8543,
  "calories_today": 2340,
  "distance_today": 6.8,
  "floors_today": 12,
  "active_minutes": 47,
  "resting_hr": 58,
  "avg_hr": 72,
  "sleep_hours": 7.2,
  "sleep_efficiency": 89,
  "awake_minutes": 12,
  "yesterday_activities": [
    {"name": "Run", "duration": 35, "calories": 320}
  ],
  "yesterday_azm": {
    "activeZoneMinutes": 61,
    "fatBurnActiveZoneMinutes": 39,
    "cardioActiveZoneMinutes": 22
  }
}
```

**注意：** “Cardio Load”（心肺负荷）数据无法通过Fitbit API获取，仅适用于Fitbit Premium会员，并且仅在移动应用程序中可见。

### 2. 数据获取（命令行接口）
```bash
# Available commands:
python scripts/fitbit_api.py steps --days 7
python scripts/fitbit_api.py calories --days 7
python scripts/fitbit_api.py heartrate --days 7
python scripts/fitbit_api.py sleep --days 7
python scripts/fitbit_api.py summary --days 7
python scripts/fitbit_api.py report --type weekly
```

### 3. 数据获取（Python API）
```bash
export PYTHONPATH="{baseDir}/scripts"
python - <<'PY'
from fitbit_api import FitbitClient

client = FitbitClient()  # Uses env vars for credentials

# Fetch data (requires start_date and end_date)
steps_data = client.get_steps(start_date="2026-01-01", end_date="2026-01-16")
hr_data = client.get_heartrate(start_date="2026-01-01", end_date="2026-01-16")
sleep_data = client.get_sleep(start_date="2026-01-01", end_date="2026-01-16")
activity_summary = client.get_activity_summary(start_date="2026-01-01", end_date="2026-01-16")
PY
```

### 4. 数据分析
```bash
export PYTHONPATH="{baseDir}/scripts"
python - <<'PY'
from fitbit_api import FitbitAnalyzer

analyzer = FitbitAnalyzer(steps_data, hr_data)
summary = analyzer.summary()
print(summary)  # Returns: avg_steps, avg_resting_hr, step_trend
PY
```

### 5. 提醒设置
```bash
python {baseDir}/scripts/alerts.py --days 7 --steps 8000 --sleep 7
```

## 脚本

- `scripts/fitbit_api.py`：Fitbit Web API的封装层，支持命令行接口和数据分析功能
- `scripts/fitbit_briefing.py`：用于生成每日简报的脚本（支持文本或JSON格式的输出）
- `scripts/alerts.py`：基于设定阈值的提醒功能

## 可用的API方法

| 方法 | 描述 |
|--------|-------------|
| `get_steps(start, end)` | 获取指定时间范围内的步数 |
| `get_calories(start, end)` | 获取指定时间范围内的卡路里消耗量 |
| `get_distance(start, end)` | 获取指定时间范围内的行走距离 |
| `get_activity_summary(start, end)` | 获取活动概要 |
| `get_heartrate(start, end)` | 获取指定时间范围内的心率数据 |
| `get_sleep(start, end)` | 获取指定时间范围内的睡眠数据 |
| `get_sleep_stages(start, end)` | 获取详细的睡眠阶段信息 |
| `get_spo2(start, end)` | 获取指定时间范围内的血氧饱和度 |
| `get_weight(start, end)` | 获取体重数据 |
| `get_active_zone_minutes(start, end)` | 获取指定时间范围内的活跃区域分钟数 |

## 参考资料

- `references/api.md`：Fitbit Web API的官方文档
- `references/metrics.md`：各项健康指标的定义及解释

## 认证

使用Fitbit API需要OAuth 2.0进行身份验证：
1. 在 [https://dev.fitbit.com/apps](https://dev.fitbit.com/apps) 创建应用程序
2. 获取`client_id` 和 `client_secret`
3. 完成OAuth认证流程以获取`access_token` 和 `refresh_token`
4. 将这些认证信息设置到环境变量中或传递给相关脚本

## 环境变量

必须设置以下环境变量：
- `FITBIT_CLIENT_ID`
- `FITBIT_CLIENT_SECRET`
- `FITBIT_ACCESS_TOKEN`
- `FITBIT_REFRESH_TOKEN`

## 自动化（Cron作业）

Cron作业的配置在OpenClaw的网关中完成，不在本仓库中。请按照以下步骤配置：

### 每日早晨8:00的简报任务
```bash
openclaw cron add \
  --name "Morning Fitbit Health Report" \
  --cron "0 8 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --wake next-heartbeat \
  --deliver \
  --channel telegram \
  --target "<YOUR_TELEGRAM_CHAT_ID>" \
  --message "python3 /path/to/your/scripts/fitbit_briefing.py --format text"
```

**注意：** 请将 `/path/to/your/` 替换为实际的路径，将 `<YOUR_TELEGRAMCHAT_ID>` 替换为你的Telegram频道/群组ID。