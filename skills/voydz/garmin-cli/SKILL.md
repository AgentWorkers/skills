---
name: garmin
description: 通过一个非交互式的命令行界面（CLI）来访问Garmin Connect中的健康、健身和活动数据。
metadata: {"clawdbot":{"emoji":"⌚","requires":{"bins":["gc"]}}}
---
# Garmin Connect CLI

本技能通过 `gc` CLI 提供对 Garmin Connect 健康和健身数据的访问。

## 设置

1. **通过 Homebrew tap 安装：**
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

大多数命令接受日期作为第一个参数：

- `today` — 当前日期
- `yesterday` — 上一天
- `week` — 过去 7 天（返回一个日期范围）
- `month` — 过去 30 天（返回一个日期范围）
- `YYYY-MM-DD` — 特定日期

对于包含子命令的命令组（如活动、身体数据、压力、心率、月经数据），请在父命令前使用 `--date` 以避免参数冲突。也可以使用 `--date`、`--start`/`--end` 标志。

## 输出

所有数据命令都支持以下格式：

- `--format json` — 机器可读的输出格式（默认格式：`table`）
- `--output FILE` — 将输出写入文件

在程序化解析输出时，请始终使用 `--format json`。

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
gc heart --date today
gc heart resting --date today

# Sleep
gc sleep today

# Stress & Body Battery
gc stress --date today
gc stress --weekly --weeks N
gc stress all-day --date today
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
gc activities --date today                        # Activities for a date
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
gc body --date today [--end DATE]
gc body weighins --date today
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
gc gear --user-profile USER_PROFILE_NUMBER        # List gear (profile number from gc status --profile)
gc gear defaults USER_PROFILE_NUMBER
gc gear stats GEAR_UUID
gc gear activities GEAR_UUID [--limit N]

# Workouts & Training Plans
gc workouts [--start N --limit N]
gc workouts get WORKOUT_ID
gc workouts download WORKOUT_ID [-o FILE]
gc workouts scheduled WORKOUT_ID
gc workouts create --file workout.json
gc workouts create --name "Workout Name" --sport cycling --steps '[{"type":"warmup","duration":600},{"type":"interval","duration":1200,"target":"hr_zone:2"},{"type":"cooldown","duration":600}]'
gc workouts update WORKOUT_ID --file workout.json
gc workouts update WORKOUT_ID --name "Workout Name" --sport cycling --steps '[{"type":"warmup","duration":600},{"type":"interval","duration":1200},{"type":"cooldown","duration":600}]'
gc workouts delete WORKOUT_ID
gc training-plans
gc training-plans get PLAN_ID
gc training-plans adaptive PLAN_ID

## Workouts Steps JSON Schema (`--steps`)

`--steps` expects a JSON array of step objects. Each step can be shorthand or Garmin-shaped.

Shorthand step example:
```json
{"type":"interval","duration":1200,"target":"hr_zone:2"}
```

Supported shorthand fields:
- `type`: `warmup`, `interval`, `recovery`, `cooldown`, `rest`, `repeat`
- `duration`: seconds (implies `endCondition` = `time`)
- `target`: `hr_zone:2`, `power_zone:3`, `pace_zone:4`, `heart_rate:150`, `power:220`, `cadence:90`, `no_target`

Garmin-shaped fields (optional):
- `stepType`: `{"stepTypeKey":"warmup"}` (or any Garmin stepType object)
- `stepOrder`: integer
- `endCondition`: `{"conditionTypeKey":"time|distance|calories|heart_rate|cadence|power|iterations"}`
- `endConditionValue`: number
- `targetType`: `{"workoutTargetTypeKey":"no.target|heart.rate|power|speed|cadence|open|heart.rate.zone|power.zone|pace.zone"}`
- `targetValue`: number

For advanced Garmin payloads (repeat groups, nested steps, etc.), prefer `--file` with the full Garmin schema.

# Menstrual Cycle
gc menstrual --date today
gc menstrual calendar --start DATE --end DATE
gc menstrual pregnancy

# Raw API
gc api /biometric-service/biometric/latestFunctionalThresholdPower/CYCLING
gc api --method POST --body '{"foo":"bar"}' /some/endpoint
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

**调用原始的 Garmin Connect API 端点：**
```bash
gc api /biometric-service/biometric/latestFunctionalThresholdPower/CYCLING
gc api --method POST --body '{"foo":"bar"}' /some/endpoint
```

**获取关于特定活动的详细信息：**
```bash
gc activities get 12345678 --format json
```

**将活动数据下载为 GPX 格式：**
```bash
gc activities download 12345678 --format gpx -o run.gpx
```

**检查训练准备情况和心率变异性（HRV）：**
```bash
gc metrics training-readiness today --format json
gc metrics hrv today --format json
```

**获取昨天的睡眠和身体电池电量数据：**
```bash
gc sleep yesterday --format json
gc battery yesterday --format json
```

## 创建锻炼计划（简洁方式）

- 建议使用带有 Garmin 标准格式 JSON 数据的 `--file` 参数。
- 通过导出现有的锻炼计划来获取有效的数据：
  ```bash
  gc workouts get WORKOUT_ID --format json > workout.json
  ```
- 如果使用标志，`--steps` 可以是来自 API 的 `workoutSteps` JSON 数组，
  或者是一个包含 `type`、`duration`（秒）和可选 `target`（例如 `hr_zone:2`）的简写数组。
- 当提供了 `--sport` 时，`--sport-id` 是可选的；CLI 会从活动类型中自动解析对应的 ID。

Garmin 锻炼计划的示例格式（最小化示例）：
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

如何了解锻炼计划创建所需的格式和有效值：

- 运动类型键/ID（用于 `sportType`）：
  - `gc activities types --format json`
- 锻炼计划的步骤/目标枚举在 CLI 中不是硬编码的。
- 导出现有的锻炼计划并重复使用其中的值：
    ```bash
    gc workouts get WORKOUT_ID --format json
    ```
- 直接使用返回的 `stepType`、`endCondition` 和 `targetType` 字段。

**列出设备并获取太阳能数据：**
```bash
gc devices --format json
gc devices solar DEVICE_ID today --format json
```