---
name: intervals-icu-api
description: **使用 intervals.icu API 访问和管理训练数据的完整指南**  
本指南适用于处理 Intervals.icu 中的运动员资料、活动记录、训练计划、健康数据等相关内容。涵盖以下方面：  
1. **身份验证**：如何使用 intervals.icu API 进行身份验证。  
2. **检索包含复合数据字段的活动记录**：如何获取包含多种数据字段的活动详情。  
3. **管理带有计划训练的日历事件**：如何创建或更新与训练计划相关的日历事件。  
4. **创建/更新训练数据**：如何添加或修改训练数据。  
**所有操作均提供 curl 命令示例**，方便读者快速实践。
---

# intervals.icu API 使用指南

本指南全面介绍了如何使用 intervals.icu API 来管理运动员的训练数据、活动、锻炼计划以及日历事件。

## 认证

### API 密钥方法

请从 [intervals.icu 设置页面](https://intervals.icu/settings) 获取您的运动员 ID 和 API 密钥。

```bash
# Using API Key header
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID
```

### 承载令牌方法 (OAuth)

```bash
# Using Bearer token
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID
```

**基础 URL:** `https://intervals.icu/api/v1`

**日期格式:** ISO-8601（例如：`2024-01-15` 或 `2024-01-15T10:30:00`）

---

## 核心概念

### 运动员 ID

在 intervals.icu 中的唯一标识符。所有 API 端点都会使用 `{id}` 作为路径参数。

### 活动与事件

- **活动**: 已完成的锻炼记录，包含实际数据（GPS 数据、功率数据、心率数据）。可通过 `/athlete/{id}/activities` 获取。
- **事件**: 日历上的计划锻炼。可通过 `/athlete/{id}/events` 获取。

### 数据字段

活动和事件可以返回不同的字段。使用 `fields` 查询参数来选择需要包含或排除的特定数据，以优化查询效率。

---

## 获取活动（已完成的锻炼）

### 获取指定日期范围内的活动列表

按完成时间从新到旧排序，获取两个日期之间的所有活动。

```bash
# Basic activity list
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/activities?oldest=2024-01-01&newest=2024-01-31"

# With limit
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/activities?oldest=2024-01-01&limit=10"

# Specific fields only (more efficient)
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/activities?oldest=2024-01-01&fields=id,name,start_date_local,type,distance,moving_time,icu_training_load"

# For specific activity type (Ride, Run, Swim, etc.)
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/activities?oldest=2024-01-01&newest=2024-01-31" | jq '.[] | select(.type == "Ride")'
```

### 将活动数据与外部数据结合

使用 `fields` 参数将活动数据与外部信息关联起来：

```bash
# Power, HR, and load data
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/activities?oldest=2024-01-01&fields=name,icu_weighted_avg_watts,average_heartrate,icu_training_load,icu_atl,icu_ctl"

# Include fatigue and fitness metrics
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/activities?oldest=2024-01-01&fields=id,name,type,icu_training_load,icu_atl,icu_ctl,perceived_exertion"

# Combine power zones and zone times
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/activities?oldest=2024-01-01&fields=id,name,distance,moving_time,icu_zone_times,icu_weighted_avg_watts"

# HR zones + intensity data
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/activities?oldest=2024-01-01&fields=id,name,type,average_heartrate,max_heartrate,icu_hr_zone_times,trimp"
```

### 获取单次活动的详细信息

```bash
# Get activity by ID with all data
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/activity/ACTIVITY_ID"

# Get activity with intervals
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/activity/ACTIVITY_ID?intervals=true"
```

### 导出活动数据（CSV 或 JSON 格式）

```bash
# Get activity streams as JSON
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/activity/ACTIVITY_ID/streams.json"

# Get activity streams as CSV (includes time, power, heart_rate, cadence, etc.)
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/activity/ACTIVITY_ID/streams.csv" \
  --output activity_streams.csv

# Get specific stream types
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/activity/ACTIVITY_ID/streams.json?types=watts,heart_rate,cadence"
```

---

## 日历与计划锻炼

### 获取日历事件（计划锻炼）

从日历中获取计划中的锻炼、备注和训练目标。

```bash
# Get all events in date range
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/events?oldest=2024-02-01&newest=2024-02-29"

# Get with specific fields
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/events?oldest=2024-02-01&newest=2024-02-29&fields=id,name,category,start_date_local,description"

# Filter by category (WORKOUT, NOTE, TARGET, FITNESS_DAYS, etc.)
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/events?oldest=2024-02-01&category=WORKOUT"

# Get workout targets for date range
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/events?oldest=2024-02-01&category=TARGET"
```

### 获取单次事件的详细信息

```bash
# Get specific planned workout
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/events/EVENT_ID"
```

### 下载计划锻炼文件

将计划中的锻炼数据导出为多种格式，以便在训练设备上使用。

```bash
# Download as .zwo (Zwift format)
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/events/EVENT_ID/download.zwo" \
  --output workout.zwo

# Download as .mrc (TrainerRoad format)
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/events/EVENT_ID/download.mrc" \
  --output workout.mrc

# Download as .erg (Wahoo format)
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/events/EVENT_ID/download.erg" \
  --output workout.erg

# Download as .fit (Garmin format)
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/events/EVENT_ID/download.fit" \
  --output workout.fit

# Download multiple workouts as zip
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/workouts.zip?oldest=2024-02-01&newest=2024-02-29&ext=zwo" \
  --output workouts.zip
```

---

## 创建和写入数据

### 创建手动记录的活动

向训练记录中添加手动记录的活动。

```bash
# Basic manual activity
curl -X POST \
  -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Morning Run",
    "type": "Run",
    "start_date_local": "2024-01-15T06:00:00",
    "distance": 10000,
    "moving_time": 3600,
    "description": "Easy morning run"
  }' \
  https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/activities/manual

# With power (cycling activity)
curl -X POST \
  -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Indoor Zwift",
    "type": "Ride",
    "start_date_local": "2024-01-15T18:00:00",
    "moving_time": 3600,
    "icu_joules": 900000,
    "icu_weighted_avg_watts": 250,
    "average_heartrate": 155,
    "trainer": true
  }' \
  https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/activities/manual

# With external ID (for syncing with external systems)
curl -X POST \
  -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Strava Activity",
    "type": "Run",
    "start_date_local": "2024-01-15T07:00:00",
    "distance": 5000,
    "moving_time": 1800,
    "external_id": "strava_12345"
  }' \
  https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/activities/manual
```

### 批量创建活动

```bash
# Bulk create activities
curl -X POST \
  -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "name": "Monday Easy Run",
      "type": "Run",
      "start_date_local": "2024-01-15T06:00:00",
      "distance": 10000,
      "moving_time": 3600
    },
    {
      "name": "Tuesday Interval Ride",
      "type": "Ride",
      "start_date_local": "2024-01-16T18:00:00",
      "moving_time": 5400,
      "icu_weighted_avg_watts": 280
    }
  ]' \
  https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/activities/manual/bulk
```

### 创建计划锻炼（日历事件）

在日历中添加未来的锻炼计划。

```bash
# Basic planned workout
curl -X POST \
  -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Vo2Max Intervals",
    "category": "WORKOUT",
    "start_date_local": "2024-02-15T18:00:00",
    "description": "6x 4min at 110% FTP with 3min recovery"
  }' \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/events?upsertOnUid=true"

# Planned workout with Intervals.icu format description
curl -X POST \
  -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sweet Spot Build",
    "category": "WORKOUT",
    "start_date_local": "2024-02-16T18:00:00",
    "description": "[Workout \"Sweet Spot\" \"\" Bike 300\n  [SteadyState 600 88 92 \"\"]\n  [SteadyState 600 88 92 \"\"]\n  [SteadyState 600 88 92 \"\"]\n]"
  }' \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/events?upsertOnUid=true"

# Create workout from .zwo file contents
curl -X POST \
  -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Zwift Structured Workout",
    "category": "WORKOUT",
    "start_date_local": "2024-02-17T19:00:00",
    "file_contents": "<Workout_Instruction version=\"1\">\n<author></author>\n<name>My Workout</name>\n<description></description>\n<sportType>Bike</sportType>\n<tags></tags>\n<workout>\n<Warmup Duration=\"600\" PowerLow=\"0.5\" PowerHigh=\"0.75\"/>\n<SteadyState Duration=\"1200\" Power=\"0.85\"/>\n</workout>\n</Workout_Instruction>"
  }' \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/events?upsertOnUid=true"
```

### 批量创建事件

```bash
# Bulk create planned workouts
curl -X POST \
  -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "name": "Easy Spin",
      "category": "WORKOUT",
      "start_date_local": "2024-02-15T18:00:00",
      "description": "60min at 60-65% FTP"
    },
    {
      "name": "Threshold Work",
      "category": "WORKOUT",
      "start_date_local": "2024-02-17T19:00:00",
      "description": "3x 10min at 95-105% FTP"
    },
    {
      "name": "Long Run",
      "category": "WORKOUT",
      "start_date_local": "2024-02-18T07:00:00",
      "description": "90min easy run at conversational pace"
    }
  ]' \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/events/bulk?upsertOnUid=true&updatePlanApplied=true"
```

### 设置训练目标

为特定日期设定训练目标。

```bash
# Create power target
curl -X POST \
  -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "FTP Test Target",
    "category": "TARGET",
    "start_date_local": "2024-02-20T18:00:00",
    "description": "Target power: 300W"
  }' \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/events?upsertOnUid=true"

# Create duration target
curl -X POST \
  -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Daily Volume Target",
    "category": "TARGET",
    "start_date_local": "2024-02-21T00:00:00",
    "description": "Target: 2 hours training"
  }' \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/events?upsertOnUid=true"
```

---

## 更新数据

### 更新活动

修改已完成的锻炼记录。

```bash
# Update activity notes and tags
curl -X PUT \
  -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Recovery Ride - Updated",
    "description": "Felt great, good recovery",
    "commute": false
  }' \
  https://intervals.icu/api/v1/activity/ACTIVITY_ID

# Update activity perceived exertion and feel
curl -X PUT \
  -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "perceived_exertion": 7,
    "feel": 8,
    "description": "Good session, felt strong"
  }' \
  https://intervals.icu/api/v1/activity/ACTIVITY_ID
```

### 更新计划锻炼（日历事件）

修改日历中的计划锻炼事件。

```bash
# Update workout details
curl -X PUT \
  -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Modified VO2Max Session",
    "description": "8x 3min at 130% FTP with 2min recovery - UPDATED"
  }' \
  https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/events/EVENT_ID

# Hide event from athlete view
curl -X PUT \
  -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "hide_from_athlete": true
  }' \
  https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/events/EVENT_ID

# Prevent athlete from editing event
curl -X PUT \
  -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "athlete_cannot_edit": true
  }' \
  https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/events/EVENT_ID
```

### 批量更新事件（指定日期范围）

```bash
# Hide all workouts for a week
curl -X PUT \
  -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "hide_from_athlete": true
  }' \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/events?oldest=2024-02-15&newest=2024-02-22"
```

---

## 健康与恢复数据

### 获取健康数据

跟踪睡眠质量、疲劳程度、静息心率等健康指标。

```bash
# Get wellness data for date range
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/wellness?oldest=2024-01-01&newest=2024-01-31"

# Get wellness data as CSV
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/wellness.csv?oldest=2024-01-01&newest=2024-01-31" \
  --output wellness.csv

# Get specific wellness fields
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/wellness?oldest=2024-01-01&fields=id,sleep_secs,soreness,fatigue,resting_hr,notes"
```

### 更新健康数据

为特定日期记录健康数据。

```bash
# Add sleep, HRV, and fatigue
curl -X PUT \
  -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "2024-01-15",
    "sleep_secs": 28800,
    "resting_hr": 52,
    "fatigue": 3,
    "soreness": 2
  }' \
  https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/wellness/2024-01-15

# Add notes
curl -X PUT \
  -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "2024-01-15",
    "notes": "Great sleep, feeling recovered"
  }' \
  https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/wellness/2024-01-15
```

### 批量更新健康数据

```bash
# Update multiple wellness days at once
curl -X PUT \
  -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "id": "2024-01-15",
      "sleep_secs": 28800,
      "resting_hr": 52
    },
    {
      "id": "2024-01-16",
      "sleep_secs": 30600,
      "resting_hr": 50
    },
    {
      "id": "2024-01-17",
      "sleep_secs": 27000,
      "resting_hr": 54
    }
  ]' \
  https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/wellness-bulk
```

---

## 运动设置与训练区间

### 获取运动设置

获取某项运动的功率区间、心率区间和 FTP 设置。

```bash
# Get Ride settings
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/sport-settings/Ride"

# Get Run settings
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/sport-settings/Run"

# List all sport settings
curl -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/sport-settings"
```

### 更新运动设置

修改功率区间、FTP 区间或心率区间。

```bash
# Update FTP and power zones
curl -X PUT \
  -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "ftp": 310,
    "power_zones": [0, 114, 152, 191, 229, 267, 310]
  }' \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/sport-settings/Ride?recalcHrZones=false"

# Update LTHR and HR zones
curl -X PUT \
  -H "Authorization: ApiKey API_KEY:YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "lthr": 165,
    "hr_zones": [0, 123, 142, 160, 178, 197, 220]
  }' \
  "https://intervals.icu/api/v1/athlete/YOUR_ATHLETE_ID/sport-settings/Ride?recalcHrZones=true"
```

---

## 常见使用场景

### 工作流程：将训练数据同步到外部系统

```bash
#!/bin/bash

ATHLETE_ID="YOUR_ATHLETE_ID"
API_KEY="YOUR_API_KEY"
DATE="2024-01-15"

# 1. Get completed activities
ACTIVITIES=$(curl -s -H "Authorization: ApiKey $ATHLETE_ID:$API_KEY" \
  "https://intervals.icu/api/v1/athlete/$ATHLETE_ID/activities?oldest=$DATE&newest=$DATE&fields=id,name,type,distance,icu_training_load")

# 2. Get planned workouts for today
EVENTS=$(curl -s -H "Authorization: ApiKey $ATHLETE_ID:$API_KEY" \
  "https://intervals.icu/api/v1/athlete/$ATHLETE_ID/events?oldest=$DATE&newest=$DATE&category=WORKOUT")

# 3. Get wellness data
WELLNESS=$(curl -s -H "Authorization: ApiKey $ATHLETE_ID:$API_KEY" \
  "https://intervals.icu/api/v1/athlete/$ATHLETE_ID/wellness/$DATE")

echo "Activities: $ACTIVITIES"
echo "Events: $EVENTS"
echo "Wellness: $WELLNESS"
```

### 工作流程：创建每周训练计划

```bash
#!/bin/bash

ATHLETE_ID="YOUR_ATHLETE_ID"
API_KEY="YOUR_API_KEY"

# Define workouts for the week
WORKOUTS='[
  {
    "name": "Monday - Easy Spin",
    "category": "WORKOUT",
    "start_date_local": "2024-02-19T18:00:00",
    "description": "60min at 60-65% FTP"
  },
  {
    "name": "Tuesday - VO2Max",
    "category": "WORKOUT",
    "start_date_local": "2024-02-20T18:00:00",
    "description": "6x 4min at 110% FTP with 3min recovery"
  },
  {
    "name": "Wednesday - Recovery",
    "category": "WORKOUT",
    "start_date_local": "2024-02-21T18:00:00",
    "description": "45min easy"
  },
  {
    "name": "Thursday - Threshold",
    "category": "WORKOUT",
    "start_date_local": "2024-02-22T19:00:00",
    "description": "2x 15min at 95-105% FTP"
  },
  {
    "name": "Friday - Rest Day",
    "category": "NOTE",
    "start_date_local": "2024-02-23T00:00:00",
    "description": "Rest and recovery"
  },
  {
    "name": "Saturday - Long Ride",
    "category": "WORKOUT",
    "start_date_local": "2024-02-24T09:00:00",
    "description": "150min at Zone 2"
  },
  {
    "name": "Sunday - Easy Recovery",
    "category": "WORKOUT",
    "start_date_local": "2024-02-25T10:00:00",
    "description": "60min easy spin"
  }
]'

# Create all workouts at once
curl -X POST \
  -H "Authorization: ApiKey $ATHLETE_ID:$API_KEY" \
  -H "Content-Type: application/json" \
  -d "$WORKOUTS" \
  "https://intervals.icu/api/v1/athlete/$ATHLETE_ID/events/bulk?upsertOnUid=true&updatePlanApplied=true"
```

### 工作流程：分析每周训练数据

```bash
#!/bin/bash

ATHLETE_ID="YOUR_ATHLETE_ID"
API_KEY="YOUR_API_KEY"

# Get activities with load and zone data for the week
curl -s -H "Authorization: ApiKey $ATHLETE_ID:$API_KEY" \
  "https://intervals.icu/api/v1/athlete/$ATHLETE_ID/activities?oldest=2024-01-08&newest=2024-01-14&fields=name,type,distance,icu_training_load,icu_zone_times,average_heartrate" | \
  jq '[.[] | {name: .name, load: .icu_training_load, zones: .icu_zone_times, hr: .average_heartrate}]'
```

---

## 重要说明

### 速率限制

请合理使用 API 请求，避免频繁发送大量请求。

### 数据字段选择

使用 `fields` 参数仅请求所需的数据，以提高性能并减少数据传输量。

### 日期格式

始终使用 ISO-8601 格式：`YYYY-MM-DD` 或 `YYYY-MM-DDTHH:MM:SS`。

### 更新操作（Upsert）

在创建事件时，使用 `upsertOnUid=true` 选项来更新具有相同 UID 的现有事件，避免重复创建。

### 外部 ID

在从其他系统同步数据时，请使用 `external_id` 以避免重复。

### 论坛讨论

如需更多关于 API 的详细信息，请参阅：[API 访问论坛帖子](https://forum.intervals.icu/t/api-access-to-intervals-icu/609)

---

## 响应状态码

- **200**: 成功
- **201**: 创建成功（活动或事件）
- **400**: 请求错误（参数无效）
- **401**: 未经授权（API 密钥或令牌无效）
- **404**: 未找到（ID 无效）
- **429**: 速率限制（请求过多）
- **500**: 服务器错误

请查看响应头中的错误详情和速率限制信息。