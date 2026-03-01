---
name: healthsync
description: 查询存储在本地 SQLite 数据库中的 Apple Health 数据。利用此功能可以获取心率、步数、血氧饱和度（SpO2）、最大摄氧量（VO2 Max）、睡眠数据、锻炼记录、静息心率（HRV）、血压、活动能量/基础能量、身体指标、活动能力、跑步数据、正念练习记录以及手腕温度等信息。支持通过 `healthsync CLI` 或直接通过 SQLite 进行查询。仅支持读取数据，严禁对数据库进行写入操作。
metadata:
  author: sidv
  version: "1.1"
compatibility: Requires healthsync binary. Database at ~/.healthsync/healthsync.db must be populated via `healthsync parse`.
---
# healthsync — Apple Health 数据查询技能

## 安装 healthsync

```bash
# macOS and Linux (recommended)
curl -fsSL https://healthsync.sidv.dev/install | bash

# Or via Go
go install github.com/BRO3886/healthsync@latest
```

安装二进制文件后，解析您的 Apple Health 数据导出文件：

```bash
# Export from Health app → profile picture → Export All Health Data
healthsync parse ~/Downloads/export.zip
```

将此技能安装到您的代理中：

```bash
# Claude Code or Codex
healthsync skills install

# OpenClaw
healthsync skills install --agent openclaw
```

查询存储在本地 SQLite 数据库中的 Apple Health 数据。此技能为 **只读** 面向的——禁止执行任何 INSERT、UPDATE、DELETE 或 DROP 操作。

## 重要限制

- **只读** — 禁止对数据库进行任何写入操作（INSERT、UPDATE、DELETE、DROP、ALTER 等）。
- **两种查询方式**：命令行界面（CLI，使用 `healthsync query`）或直接通过 SQLite （`sqlite3 ~/.healthsync/healthsync.db`）。
- **建议使用 CLI** 进行简单查询；对于复杂的聚合、连接或自定义 SQL 语句，请使用直接 SQLite。

## 数据库位置

默认位置：`~/.healthsync/healthsync.db`

## 快速入门

```bash
# Recent heart rate readings
healthsync query heart-rate --limit 10

# Steps in a date range
healthsync query steps --from 2024-01-01 --to 2024-06-30 --limit 100

# Deduplicated daily step totals
healthsync query steps --total --from 2024-01-01

# Deduplicated daily active energy totals
healthsync query active-energy --total --from 2024-01-01

# Workouts as JSON
healthsync query workouts --format json --limit 20

# Sleep data as CSV
healthsync query sleep --format csv --limit 50

# Resting heart rate trend
healthsync query resting-heart-rate --limit 30

# HRV readings
healthsync query hrv --limit 30

# Blood pressure
healthsync query blood-pressure --limit 20

# Body weight trend
healthsync query body-mass --limit 30

# Direct SQLite for aggregations
sqlite3 ~/.healthsync/healthsync.db "SELECT date(start_date) as day, SUM(value) as total_steps FROM steps GROUP BY day ORDER BY day DESC LIMIT 7"

# Average resting heart rate per week
sqlite3 ~/.healthsync/healthsync.db "SELECT strftime('%Y-W%W', start_date) as week, ROUND(AVG(value),1) as avg_rhr FROM resting_heart_rate GROUP BY week ORDER BY week DESC LIMIT 12"
```

## CLI 参考

### `healthsync query <table>`

| 标志 | 描述 | 默认值 |
|------|-------------|---------|
| `--from` | 从指定日期开始过滤记录（包含该日期） | — |
| `--to` | 到指定日期结束过滤记录（包含该日期） | — |
| `--limit` | 返回的最大记录数 | 50 |
| `--format` | 输出格式：`table`、`json`、`csv` | `table` |
| `--total` | 去除重复后的每日总计（步数、活动能量、基础能量） | `false` |
| `--db` | 覆盖数据库路径 | `~/.healthsync/healthsync.db` |

### 可用的表格

**心脏健康**

| CLI 名称 | 数据库表格 | 备注 |
|----------|----------|-------|
| `heart-rate` | `heart_rate` | 每分钟心跳次数（BPM）；高频数据 |
| `resting-heart-rate` | `resting_heart_rate` | 日常静息心率 |
| `hrv` | `hrv` | 心率变异性（HRV SDNN，单位：毫秒）；夜间数据 |
| `heart-rate-recovery` | `heart_rate_recovery` | 运动后心率恢复时间 |
| `respiratory-rate` | `respiratory-rate` | 呼吸频率（每分钟） |
| `blood-pressure` | `blood_pressure` | 收缩压和舒张压（单位：毫米汞柱） |

**活动/能量**

| CLI 名称 | 数据库表格 | 备注 |
|----------|----------|-------|
| `steps` | `steps` | 步数 |
| `active-energy` | `active_energy` | 活动能量（单位：千卡） |
| `basal-energy` | `basal_energy` | 基础能量（单位：千卡） |
| `exercise-time` | `exercise_time` | 运动时间（单位：分钟） |
| `stand-time` | `stand_time` | 站立时间（单位：分钟） |
| `flights-climbed` | `flights_climbed` | 爬楼梯的次数 |
| `distance-walking-running` | `distance_walking_running` | 行走或跑步的距离（单位：公里/英里） |
| `distance-cycling` | `distance_cycling` | 骑自行车距离（单位：公里/英里） |

**身体状况**

| CLI 名称 | 数据库表格 | 备注 |
|----------|----------|-------|
| `body-mass` | `body_mass` | 体重（单位：千克/磅） |
| `bmi` | `body_mass_index` | 体质指数（BMI） |
| `height` | `height` | 身高（单位：米/英尺） |

**移动/步行**

| CLI 名称 | 数据库表格 | 备注 |
|----------|----------|-------|
| `walking-speed` | `walking_speed` | 步行速度（单位：米/秒） |
| `walking-step-length` | `walking_step_length` | 步幅（单位：米） |
| `walking-asymmetry` | `walking_asymmetry` | 步态不对称性（百分比） |
| `walking-double-support` | `walking_double_support` | 双脚支撑比例（百分比） |
| `walking-steadiness` | `walking_steadiness` | 步态稳定性（评分） |
| `stair-ascent-speed` | `stair_ascent-speed` | 上楼梯速度（单位：英尺/秒） |
| `stair-descent-speed` | `stair-descent-speed` | 下楼梯速度（单位：英尺/秒） |
| `six-minute-walk` | `six_minute-walk` | 六分钟步行距离（单位：米） |

**跑步**

| CLI 名称 | 数据库表格 | 备注 |
|----------|----------|-------|
| `running-speed` | `running_speed` | 跑步速度（单位：米/秒） |
| `running-power` | `running_power` | 跑步功率（单位：瓦特） |
| `running-stride-length` | `runningStride_length` | 步幅（单位：米） |
| `running-ground-contact-time` | `running_ground_contact_time` | 跑步时与地面的接触时间（单位：毫秒） |
| `running-vertical-oscillation` | `running_vertical_oscillation` | 跑步时的垂直振动幅度（单位：厘米） |

**其他**

| CLI 名称 | 数据库表格 | 备注 |
|----------|----------|-------|
| `spo2` | `spo2` | 血氧饱和度（0-1 的分数；0.98 表示 98%） |
| `vo2max` | `vo2_max` | 最大摄氧量（单位：毫升/分钟·千克） |
| `sleep` | `sleep` | 睡眠阶段（无单位） |
| `workouts` | `workouts` | 锻炼记录（包括时长、距离和消耗的能量） |
| `wrist-temperature` | `wrist_temperature` | 手腕温度（单位：摄氏度） |
| `time-in-daylight` | `time_in_daylight` | 日间活动时间（单位：分钟） |
| `dietary-water` | `dietary-water` | 每日饮水量（单位：毫升/升） |
| `physical-effort` | `physical_effort` | 体力活动强度（MET 评分） |
| `walking-heart-rate` | `walking_heart-rate` | 步行时的心率（单位：每分钟心跳次数） |
| `mindful-session` | `mindful_sessions` | 正念练习次数（无单位） |
| `stand-hours` | `stand-hours` | 站立时间（无单位） |

### `healthsync parse <file>`

将 Apple Health 数据导出文件解析到数据库中。（此命令仅供参考，除非用户明确要求，否则不要执行。）

| 标志 | 描述 | 默认值 |
|------|-------------|---------|
| `-v` | 详细日志记录，包含进度信息 | `false` |
| `--db` | 覆盖数据库路径 | `~/.healthsync/healthsync.db` |

### `healthsync server`

启动 HTTP 服务器以接收数据上传。（此命令仅供参考，除非用户请求，否则不要启动。）

**端点：**
- `POST /api/upload` — 上传 `.zip` 或 `.xml` 文件（multipart 形式，字段：`file`）。返回 202 状态码，解析过程为异步进行。
- `GET /api/upload/status` — 查询解析进度。
- `GET /api/health/{table}?from=&to=&limit=` — 以 JSON 格式查询数据。

## 数据库模式

### 标准数据表

模式：`id, source_name, start_date, end_date, value REAL, unit TEXT, created_at`

适用于所有表格，除了 `blood_pressure`、`sleep`、`mindful_sessions`、`stand_hours` 和 `workouts`。

```sql
CREATE TABLE resting_heart_rate (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT NOT NULL,
    start_date  TEXT NOT NULL,
    end_date    TEXT NOT NULL,
    value       REAL NOT NULL,
    unit        TEXT NOT NULL,
    created_at  TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_name, start_date, end_date, value)
);
```

### blood_pressure（特殊表格——包含收缩压和舒张压）

```sql
CREATE TABLE blood_pressure (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT NOT NULL,
    start_date  TEXT NOT NULL,
    end_date    TEXT NOT NULL,
    systolic    REAL NOT NULL,   -- mmHg
    diastolic   REAL NOT NULL,   -- mmHg
    unit        TEXT NOT NULL,   -- "mmHg"
    created_at  TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_name, start_date, end_date, systolic, diastolic)
);
```

### 分类表格（无单位列）

适用于：`sleep`、`mindful_sessions`、`stand_hours`

```sql
CREATE TABLE sleep (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT NOT NULL,
    start_date  TEXT NOT NULL,
    end_date    TEXT NOT NULL,
    value       TEXT NOT NULL,   -- e.g. HKCategoryValueSleepAnalysisAsleepCore
    created_at  TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_name, start_date, end_date, value)
);
```

### workouts（锻炼记录）

```sql
CREATE TABLE workouts (
    id                       INTEGER PRIMARY KEY AUTOINCREMENT,
    activity_type            TEXT NOT NULL,
    source_name              TEXT NOT NULL,
    start_date               TEXT NOT NULL,
    end_date                 TEXT NOT NULL,
    duration                 REAL,
    duration_unit            TEXT,
    total_distance           REAL,
    total_distance_unit      TEXT,
    total_energy_burned      REAL,
    total_energy_burned_unit TEXT,
    created_at               TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(activity_type, start_date, end_date, source_name)
);
```

### 日期格式

所有日期均以文本格式存储：`2024-01-15 08:30:00 +0530`。可以通过日期前缀进行过滤（例如：`2024-01-01`）。

### 睡眠阶段

| 值 | 含义 |
|-------|---------|
| `HKCategoryValueSleepAnalysisInBed` | 在床上 |
| `HKCategoryValueSleepAnalysisAsleepCore` | 核心睡眠阶段 |
| `HKCategoryValueSleepAnalysisAsleepDeep` | 深度睡眠 |
| `HKCategoryValueSleepAnalysisAsleepREM` | 快速眼动睡眠（REM） |
| `HKCategoryValueSleepAnalysisAwake` | 清醒状态 |
| `HKCategoryValueSleepAnalysisUnspecified` | 未指定的睡眠阶段 |

## 常见查询模式

### 每日步数总计（去重）

```bash
healthsync query steps --total --from 2024-01-01
```

### 每日活动能量总计（去重）

```bash
healthsync query active-energy --total --from 2024-01-01
```

### 每周平均静息心率

```sql
SELECT strftime('%Y-W%W', start_date) as week,
  ROUND(AVG(value), 1) as avg_rhr
FROM resting_heart_rate
GROUP BY week ORDER BY week DESC LIMIT 12;
```

### 心率变异性趋势

```sql
SELECT date(start_date) as day, ROUND(AVG(value), 1) as hrv_ms
FROM hrv
GROUP BY day ORDER BY day DESC LIMIT 30;
```

### 血压历史记录

```sql
SELECT date(start_date) as day,
  ROUND(AVG(systolic), 1) as avg_sys,
  ROUND(AVG(diastolic), 1) as avg_dia
FROM blood_pressure
GROUP BY day ORDER BY day DESC LIMIT 30;
```

### 体重变化趋势

```sql
SELECT date(start_date) as day, value as kg
FROM body_mass
ORDER BY day DESC LIMIT 30;
```

### 每晚睡眠时长

```sql
SELECT date(start_date) as night,
  ROUND(SUM((julianday(end_date) - julianday(start_date)) * 24), 1) as hours
FROM sleep
WHERE value LIKE '%Asleep%'
GROUP BY night ORDER BY night DESC LIMIT 14;
```

### 每日平均心率

```sql
SELECT date(start_date) as day,
  ROUND(AVG(value), 1) as avg_hr,
  MIN(value) as min_hr,
  MAX(value) as max_hr
FROM heart_rate
GROUP BY day ORDER BY day DESC LIMIT 30;
```

### 锻炼总结

```sql
SELECT activity_type, COUNT(*) as count,
  ROUND(AVG(duration), 1) as avg_min,
  ROUND(SUM(total_energy_burned)) as total_kcal
FROM workouts
GROUP BY activity_type ORDER BY count DESC;
```

### 每周最大摄氧量趋势

```sql
SELECT strftime('%Y-W%W', start_date) as week,
  ROUND(AVG(value), 2) as avg_vo2
FROM vo2_max
GROUP BY week ORDER BY week DESC LIMIT 12;
```

### 每周正念练习时间

```sql
SELECT strftime('%Y-W%W', start_date) as week,
  ROUND(SUM((julianday(end_date) - julianday(start_date)) * 1440), 0) as minutes
FROM mindful_sessions
GROUP BY week ORDER BY week DESC LIMIT 12;
```

## 限制

- **只读** — 此技能严禁对数据库进行写入操作。
- **无实时数据** — 数据仅更新至最近一次 `healthsync` 解析的时间点。
- **日期过滤基于字符串** — 日期字符串中包含时区信息。
- **SpO2 值为分数形式** — 0.98 表示 98% 的血氧饱和度。
- **血压数据为组合值** — 收缩压和舒张压在同一行中存储。
- **分类表格无单位列** — `sleep`、`mindful_sessions`、`stand_hours` 表格中的数据为文本格式，非数值类型。