---
name: garmer
description: 从 Garmin Connect 中提取健康和健身数据，包括活动记录、睡眠情况、心率、压力水平、步数以及身体成分信息。当用户询问其 Garmin 设备的数据、健身指标、睡眠分析或健康状况时，可以使用这些信息进行解答。
license: MIT
compatibility: Requires Python 3.10+, pip/uv for installation. Requires Garmin Connect account credentials for authentication.
metadata:
  author: MoltBot Team
  version: "0.1.0"
  moltbot:
    emoji: "⌚"
    primaryEnv: "GARMER_TOKEN_DIR"
    requires:
      bins:
        - garmer
    install:
      - id: uv
        kind: uv
        package: garmer
        bins:
          - garmer
        label: Install garmer (uv)
      - id: pip
        kind: pip
        package: garmer
        bins:
          - garmer
        label: Install garmer (pip)
---

# Garmer – 从Garmin设备提取数据的工具

该工具能够从Garmin Connect服务中提取健康和健身数据，以便进行分析和获取洞察。

## 先决条件

1. 拥有一个包含健康数据的Garmin Connect账户。
2. 已安装`garmer`命令行工具（安装方法详见元数据中的说明）。

## 认证（一次性设置）

在使用`garmer`之前，请先进行认证：

```bash
garmer login
```

系统会提示您输入Garmin Connect的电子邮件地址和密码。认证生成的令牌会保存在`~/.garmer/garmin_tokens`文件中，以供后续使用。

要检查认证状态，请执行以下命令：

```bash
garmer status
```

## 可用的命令

### 每日总结

获取当天的健康数据摘要（步数、卡路里消耗、心率、压力水平）：

```bash
garmer summary
# For a specific date:
garmer summary --date 2025-01-15
# Include last night's sleep data:
garmer summary --with-sleep
garmer summary -s
# JSON output for programmatic use:
garmer summary --json
# Combine flags:
garmer summary --date 2025-01-15 --with-sleep --json
```

### 睡眠数据

获取睡眠分析结果（睡眠时长、睡眠阶段、睡眠质量评分、心率变异性HRV）：

```bash
garmer sleep
# For a specific date:
garmer sleep --date 2025-01-15
```

### 运动活动

列出最近进行的健身活动：

```bash
garmer activities
# Limit number of results:
garmer activities --limit 5
# Filter by specific date:
garmer activities --date 2025-01-15
# JSON output for programmatic use:
garmer activities --json
```

### 活动详情

获取某次具体运动的详细信息：

```bash
# Latest activity:
garmer activity
# Specific activity by ID:
garmer activity 12345678
# Include lap data:
garmer activity --laps
# Include heart rate zone data:
garmer activity --zones
# JSON output:
garmer activity --json
# Combine flags:
garmer activity 12345678 --laps --zones --json
```

### 健康状况概览

获取当天的综合健康数据：

```bash
garmer snapshot
# For a specific date:
garmer snapshot --date 2025-01-15
# As JSON for programmatic use:
garmer snapshot --json
```

### 数据导出

将多天的数据导出为JSON格式：

```bash
# Last 7 days (default)
garmer export

# Custom date range
garmer export --start-date 2025-01-01 --end-date 2025-01-31 --output my_data.json

# Last N days
garmer export --days 14
```

### 其他实用命令

```bash
# Update garmer to latest version (git pull):
garmer update

# Show version information:
garmer version
```

## Python API使用

如需进行更复杂的数据处理，可以使用Python API：

```python
from garmer import GarminClient
from datetime import date, timedelta

# Use saved tokens
client = GarminClient.from_saved_tokens()

# Or login with credentials
client = GarminClient.from_credentials(email="user@example.com", password="pass")
```

### 用户信息

```python
# Get user profile
profile = client.get_user_profile()
print(f"User: {profile.display_name}")

# Get registered devices
devices = client.get_user_devices()
```

### 每日总结

```python
# Get daily summary (defaults to today)
summary = client.get_daily_summary()
print(f"Steps: {summary.total_steps}")

# Get for specific date
summary = client.get_daily_summary(date(2025, 1, 15))

# Get weekly summary
weekly = client.get_weekly_summary()
```

### 睡眠数据

```python
# Get sleep data (defaults to today)
sleep = client.get_sleep()
print(f"Sleep: {sleep.total_sleep_hours:.1f} hours")

# Get last night's sleep
sleep = client.get_last_night_sleep()

# Get sleep for date range
sleep_data = client.get_sleep_range(
    start_date=date(2025, 1, 1),
    end_date=date(2025, 1, 7)
)
```

### 运动活动

```python
# Get recent activities
activities = client.get_recent_activities(limit=5)
for activity in activities:
    print(f"{activity.activity_name}: {activity.distance_km:.1f} km")

# Get activities with filters
activities = client.get_activities(
    start_date=date(2025, 1, 1),
    end_date=date(2025, 1, 31),
    activity_type="running",
    limit=20
)

# Get single activity by ID
activity = client.get_activity(12345678)
```

### 心率

```python
# Get heart rate data for a day
hr = client.get_heart_rate()
print(f"Resting HR: {hr.resting_heart_rate} bpm")

# Get just resting heart rate
resting_hr = client.get_resting_heart_rate(date(2025, 1, 15))
```

### 压力水平与身体状态

```python
# Get stress data
stress = client.get_stress()
print(f"Avg stress: {stress.avg_stress_level}")

# Get body battery data
battery = client.get_body_battery()
```

### 步数

```python
# Get detailed step data
steps = client.get_steps()
print(f"Total: {steps.total_steps}, Goal: {steps.step_goal}")

# Get just total steps
total = client.get_total_steps(date(2025, 1, 15))
```

### 身体成分

```python
# Get latest weight
weight = client.get_latest_weight()
print(f"Weight: {weight.weight_kg} kg")

# Get weight for specific date
weight = client.get_weight(date(2025, 1, 15))

# Get full body composition
body = client.get_body_composition()
```

### 水分摄入与呼吸数据

```python
# Get hydration data
hydration = client.get_hydration()
print(f"Intake: {hydration.total_intake_ml} ml")

# Get respiration data
resp = client.get_respiration()
print(f"Avg breathing: {resp.avg_waking_respiration} breaths/min")
```

### 综合报告

```python
# Get health snapshot (all metrics for a day)
snapshot = client.get_health_snapshot()
# Returns: daily_summary, sleep, heart_rate, stress, steps, hydration, respiration

# Get weekly health report with trends
report = client.get_weekly_health_report()
# Returns: activities summary, sleep stats, steps stats, HR trends, stress trends

# Export data for date range
data = client.export_data(
    start_date=date(2025, 1, 1),
    end_date=date(2025, 1, 31),
    include_activities=True,
    include_sleep=True,
    include_daily=True
)
```

## 常见工作流程

### 健康状况查询

当用户询问“我的睡眠情况如何？”或“我的健康数据摘要是什么？”时，可以使用此功能：

```bash
garmer snapshot --json
```

### 运动数据分析

当用户需要查看自己的运动记录或分析运动表现时，可以使用此功能：

```bash
garmer activities --limit 10
```

### 数据趋势分析

用于分析用户健康数据随时间的变化趋势：

```bash
garmer export --days 30 --output health_data.json
```

完成数据提取后，可以使用Python对JSON文件进行处理和分析。

## 可用的数据类型

- **运动类型**：跑步、骑行、游泳、力量训练等
- **睡眠数据**：睡眠时长、睡眠阶段（深度睡眠、浅睡眠、快速眼动睡眠）、睡眠质量评分、心率变异性HRV
- **心率数据**：静息心率、心率测量次数、心率区间
- **压力水平**：压力指数、身体状态指标
- **步数数据**：总步数、行走距离
- **身体成分数据**：体重、体脂百分比、肌肉质量
- **水分摄入数据**：每日水分摄入量
- **呼吸数据**：呼吸频率数据

## 错误处理

- 如果未完成认证，系统会提示用户重新认证：
  ```
Not logged in. Use 'garmer login' first.
```

- 如果会话已过期，系统会提示用户重新登录：
  ```bash
garmer login
```

## 环境变量

- `GARMER_TOKEN_DIR`：用于存储认证令牌的自定义目录
- `GARMER_LOG_LEVEL`：设置日志记录级别（DEBUG、INFO、WARNING、ERROR）
- `GARMER_CACHE_ENABLED`：启用/禁用数据缓存（true/false）

## 参考资料

有关API的详细文档及MoltBot集成示例，请参阅`references/REFERENCE.md`。