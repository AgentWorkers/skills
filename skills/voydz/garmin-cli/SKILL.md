---
name: garmin
description: 通过一个非交互式的命令行界面（CLI），从 Garmin Connect 读取健康、健身和活动数据。
metadata: {"clawdbot":{"emoji":"⌚","requires":{"bins":["gc"]}}}
---

# Garmin Connect CLI

该工具通过 `gc` CLI 提供对 Garmin Connect 中的健康和健身数据的读取访问功能。

## 设置

1. **通过 Homebrew 安装：**
    ```bash
    brew tap voydz/homebrew-tap
    brew install garmin-cli
    ```

2. **身份验证：**
    ```bash
    gc login --email user@example.com --password secret
    # With MFA:
    gc login --email user@example.com --password secret --mfa 123456
    ```

3. **验证连接：**
    ```bash
    gc status
    ```

## 日期快捷方式

大多数命令支持使用日期作为第一个参数：

- `today` — 当前日期
- `yesterday` — 上一天
- `week` — 过去 7 天（返回一个日期范围）
- `month` — 过去 30 天（返回一个日期范围）
- `YYYY-MM-DD` — 具体日期

也可以使用 `--date`、`--start`/`--end` 标志来指定日期范围。

## 输出格式

所有数据相关的命令都支持以下格式选项：

- `--format json` — 以机器可读的 JSON 格式输出（默认格式为表格）
- `--output FILE` — 将输出内容写入文件

在程序解析输出时，务必使用 `--format json` 标志。

## 使用方法

```bash
# Authentication
gc login --email EMAIL --password PASS [--mfa CODE | --wait-mfa]
gc logout
gc status
gc status --profile

# Daily Health
gc health today
gc steps today
gc steps week
gc steps --weekly --weeks N
gc steps --start DATE --end DATE
gc floors today
gc intensity today
gc intensity --weekly --weeks N
gc events today

# Heart Rate
gc heart today
gc heart resting today

# Sleep
gc sleep today

# Stress & Body Battery
gc stress today
gc stress --weekly --weeks N
gc stress all-day today
gc battery today
gc battery --start DATE --end DATE
gc battery --events today

# Vitals
gc respiration today
gc spo2 today
gc blood-pressure today [--end DATE]
gc lifestyle today

# Hydration
gc hydration today

# Activities
gc activities                                     # List recent (default 20)
gc activities --limit N --offset N --type TYPE
gc activities --start DATE --end DATE [--type TYPE]
gc activities today                               # Activities for a date
gc activities last                                # Most recent activity
gc activities get ID                              # Activity summary by ID
gc activities count                               # Total count
gc activities details ID
gc activities splits ID
gc activities typed-splits ID
gc activities split-summaries ID
gc activities weather ID
gc activities hr-zones ID
gc activities power-zones ID
gc activities exercise-sets ID
gc activities types                               # List all activity types
gc activities gear ID                             # Gear used for activity
gc activities progress --start DATE --end DATE --metric distance|duration|elevation
gc activities download ID --format fit|tcx|gpx|kml|csv [-o FILE]
gc activities upload FILE                         # .fit, .gpx, .tcx

# Body & Weight
gc body today [--end DATE]
gc body weighins today
gc body weighins --start DATE --end DATE

# Advanced Metrics
gc metrics vo2max today
gc metrics hrv today
gc metrics training-readiness today
gc metrics morning-readiness today
gc metrics training-status today
gc metrics fitness-age today
gc metrics race-predictions
gc metrics race-predictions --start DATE --end DATE --type daily|monthly
gc metrics endurance-score today [--end DATE]
gc metrics hill-score today [--end DATE]
gc metrics lactate-threshold                      # Latest
gc metrics lactate-threshold --no-latest --start DATE --end DATE --aggregation daily|weekly|monthly|yearly
gc metrics cycling-ftp

# Devices
gc devices                                        # List all devices
gc devices last-used
gc devices primary
gc devices settings DEVICE_ID
gc devices alarms
gc devices solar DEVICE_ID today [--end DATE]

# Goals, Records, Badges & Challenges
gc records
gc goals [--status active|future|past] [--limit N]
gc badges earned
gc badges available
gc badges in-progress
gc challenges adhoc [--start N --limit N]
gc challenges badge [--start N --limit N]
gc challenges available [--start N --limit N]
gc challenges non-completed [--start N --limit N]
gc challenges virtual [--start N --limit N]

# Gear
gc gear USER_PROFILE_NUMBER                       # List gear (profile number from gc status --profile)
gc gear defaults USER_PROFILE_NUMBER
gc gear stats GEAR_UUID
gc gear activities GEAR_UUID [--limit N]

# Workouts & Training Plans
gc workouts [--start N --limit N]
gc workouts get WORKOUT_ID
gc workouts download WORKOUT_ID [-o FILE]
gc workouts scheduled WORKOUT_ID
gc workouts create --file workout.json
gc workouts update WORKOUT_ID --file workout.json
gc workouts delete WORKOUT_ID
gc training-plans
gc training-plans get PLAN_ID
gc training-plans adaptive PLAN_ID

# Menstrual Cycle
gc menstrual today
gc menstrual calendar --start DATE --end DATE
gc menstrual pregnancy
```

## 示例

**以 JSON 格式获取今天的健康概要：**
```bash
gc health today --format json
```

**以 JSON 格式获取上周的步数以供分析：**
```bash
gc steps week --format json
```

**查找用户最近的一次跑步记录：**
```bash
gc activities --limit 5 --type running --format json
```

**获取特定活动的详细信息：**
```bash
gc activities get 12345678 --format json
```

**将某项活动下载为 GPX 格式：**
```bash
gc activities download 12345678 --format gpx -o run.gpx
```

**检查训练状态和心率变异性（HRV）：**
```bash
gc metrics training-readiness today --format json
gc metrics hrv today --format json
```

**获取昨天的睡眠数据和身体电量：**
```bash
gc sleep yesterday --format json
gc battery yesterday --format json
```

## 创建锻炼计划（简述）

- 建议使用带有 Garmin 标准格式 JSON 数据的 `--file` 参数；CLI 不会自动推断或转换数据字段。
- 可以通过导出现有的锻炼计划来获取有效的 JSON 数据：
  ```bash
  gc workouts get WORKOUT_ID --format json > workout.json
  ```
- 如果使用标志，请明确指定 `--sport-id`，并传递来自 API 的 `workoutSteps` JSON 数组。

Garmin 锻炼计划的 JSON 格式示例（最小化示例）：
```json
{
  "workoutName": "Zone 2 Ride",
  "sportType": {
    "sportTypeKey": "cycling",
    "sportTypeId": 17
  },
  "workoutSegments": [
    {
      "segmentOrder": 1,
      "sportType": {
        "sportTypeKey": "cycling",
        "sportTypeId": 17
      },
      "workoutSteps": [
        {
          "stepOrder": 1,
          "stepType": { "stepTypeKey": "warmup" },
          "endCondition": { "conditionTypeKey": "time" },
          "endConditionValue": 600
        },
        {
          "stepOrder": 2,
          "stepType": { "stepTypeKey": "interval" },
          "endCondition": { "conditionTypeKey": "time" },
          "endConditionValue": 3600
        }
      ]
    }
  ]
}
```

示例创建过程：
```bash
# Create from file (recommended)
gc workouts create --file workout.json

# Create with flags using exact Garmin steps JSON
gc workouts create \
  --name "Zone 2 Ride" \
  --sport cycling \
  --sport-id 17 \
  --steps '[{"stepOrder":1,"stepType":{"stepTypeKey":"warmup"},"endCondition":{"conditionTypeKey":"time"},"endConditionValue":600},{"stepOrder":2,"stepType":{"stepTypeKey":"interval"},"endCondition":{"conditionTypeKey":"time"},"endConditionValue":3600}]'
```

如何确定锻炼计划创建所需的格式和有效数据：

- 运动类型键/ID（用于 `sportType`）：
  - `gc activities types --format json`
- 锻炼计划的步数/目标值在 CLI 中不是硬编码的。
- 可以导出现有的锻炼计划并重复使用其中的数值：
    ```bash
    gc workouts get WORKOUT_ID --format json
    ```
- 请直接使用返回的 `stepType`、`endCondition` 和 `targetType` 字段。

**列出设备并获取太阳能数据：**
```bash
gc devices --format json
gc devices solar DEVICE_ID today --format json
```