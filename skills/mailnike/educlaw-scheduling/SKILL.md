---
name: educlaw-scheduling
display_name: EduClaw Advanced Scheduling
version: 1.0.0
description: 负责为K-12（小学至高中）及高等教育机构制定教学计划、安排课程表、解决时间冲突以及分配教室资源。该功能属于EduClaw学生信息管理系统（SIS）的子模块。
author: ERPForge
parent: educlaw
requires: [erpclaw, educlaw]
database: ~/.openclaw/erpclaw/data.sqlite
user-invocable: true
scripts:
  - scripts/db_query.py
domains:
  - schedule_patterns
  - master_schedule
  - conflict_resolution
  - room_assignment
total_actions: 56
tables:
  - educlaw_schedule_pattern
  - educlaw_day_type
  - educlaw_bell_period
  - educlaw_master_schedule
  - educlaw_section_meeting
  - educlaw_course_request
  - educlaw_schedule_conflict
  - educlaw_room_booking
  - educlaw_instructor_constraint
metadata: {"openclaw":{"type":"executable","install":{"post":"python3 init_db.py && python3 scripts/db_query.py --action status"},"requires":{"bins":["python3"],"env":[],"optionalEnv":[]},"os":["darwin","linux"]}}
---
# EduClaw 高级调度系统

该系统专为 K-12 及高等教育机构提供高级调度功能，支持命名调度模式、主调度周期管理、课程需求分析、11 种冲突类型处理、智能教室分配以及教师约束管理。

## 快速入门

```bash
# 1. Define a schedule pattern
python3 db_query.py --action add-schedule-pattern \
  --name "Traditional 7-Period" --pattern-type traditional --cycle-days 1 --company-id <id>
python3 db_query.py --action add-day-type \
  --schedule-pattern-id <id> --code "MON-FRI" --name "Regular Day"
python3 db_query.py --action add-bell-period \
  --schedule-pattern-id <id> --period-number 1 --period-name "Period 1" \
  --start-time "08:00" --end-time "08:50" --duration-minutes 50
python3 db_query.py --action activate-schedule-pattern --pattern-id <id>

# 2. Build and publish master schedule
python3 db_query.py --action create-master-schedule \
  --academic-term-id <id> --schedule-pattern-id <id> --name "Fall 2026" --company-id <id>
python3 db_query.py --action add-section-meeting \
  --master-schedule-id <id> --section-id <id> --day-type-id <id> --bell-period-id <id>
python3 db_query.py --action generate-conflict-check --master-schedule-id <id>
python3 db_query.py --action submit-master-schedule --master-schedule-id <id>
```

---

## 第一级 — 核心调度工作流程

### `add-schedule-pattern`  
创建一个可重用的调度模式。

| 参数 | 必需 | 描述 |
|-----------|----------|-------------|
| `--name` | ✓ | 模式名称（例如：“传统七节课制”） |
| `--pattern-type` | ✓ | `traditional`、`block_4x4`、`block_ab`、`trimester`、`rotating_drop`、`semester`、`custom` |
| `--cycle-days` | ✓ | 一个周期内的唯一天数 |
| `--company-id` | ✓ | 公司 ID |
| `--description` | | 人类可读的描述 |
| `--notes` | | 内部备注 |
| `--total-periods-per-cycle` | | 预计算出的总课时数（仅供参考） |

### `add-day-type`  
为调度模式添加一个命名的日类型（例如：“Day A”、“Day B”）。

| 参数 | 必需 | 描述 |
|-----------|----------|-------------|
| `--schedule-pattern-id` | ✓ | 父级模式 ID |
| `--code` | ✓ | 简短代码（例如：“A”、“B”、“MON”） |
| `--name` | ✓ | 显示名称 |
| `--sort-order` | | 显示顺序（默认：0） |

### `add-bell-period`  
为调度模式添加一个命名的时间段。

| 参数 | 必需 | 描述 |
|-----------|----------|-------------|
| `--schedule-pattern-id` | ✓ | 父级模式 ID |
| `--period-number` | ✓ | 课时编号（例如：“1”、“Block A”） |
| `--period-name` | ✓ | 显示名称 |
| `--start-time` | ✓ | 开始时间（HH:MM） |
| `--end-time` | ✓ | 结束时间（HH:MM） |
| `--duration-minutes` | ✓ | 持续时间（分钟，大于 0） |
| `--period-type` | | `class`（默认）、`break`、`lunch`、`homeroom`、`advisory`、`flex`、`passing` |
| `--sort-order` | | 显示顺序 |
| `--applies-to-day-types` | | 日类型 ID 的 JSON 数组；空表示所有日类型 |

### `activate-schedule-pattern`  
在定义了日类型和时间段后，激活该调度模式。**必需参数：`--pattern-id`**

### `create-master-schedule`  
为某个学学期创建一个主调度容器。

| 参数 | 必需 | 描述 |
|-----------|----------|-------------|
| `--academic-term-id` | ✓ | 学期 ID（每个学期唯一） |
| `--schedule-pattern-id` | ✓ | 定义日和课时的模式 |
| `--name` | ✓ | 调度名称 |
| `--company-id` | ✓ | 公司 ID |
| `--build-notes` | | 内部建筑备注 |

### `add-section-meeting`  
将某个课程安排到特定的日类型和时间段中。

| 参数 | 必需 | 描述 |
|-----------|----------|-------------|
| `--master-schedule-id` | ✓ | 父级主调度模式 |
| `--section-id` | ✓ | 来自 `educlaw_section` 的课程编号 |
| `--day-type-id` | ✓ | 对应的日类型 |
| `--bell-period-id` | ✓ | 对应的时间段 |
| `--room-id` | | 教室分配 |
| `--instructor-id` | | 可覆盖默认设置 |
| `--meeting-type` | | `regular`（默认）、`lab`、`exam`、`field_trip`、`make_up` |
| `--meeting-mode` | | `in_person`（默认）、`hybrid`、`online` |

### `generate-conflict-check`  
对主调度模式进行 11 种冲突类型的检查。**必需参数：`--master-schedule-id`**  
冲突类型包括：`instructor_double_booking`（严重）、`room_double_booking`（严重）、`student_conflict`（高）、`instructor_overload`（高）、`instructor_contract_violation`（高）、`capacity_exceeded`（高）、`singleton_overlap`（高）、`room_shortage`（高）、`room_type_mismatch`（中）、`credential_mismatch`（中）、`contact_hours_deficit`（中）。

### `submit-master-schedule`  
发布主调度计划（如果存在未解决的严重冲突，则会阻塞发布）。**必需参数：`--master-schedule-id`**。可选参数：`--published-by`**

---

## 第二级 — 调度模式与主调度计划

- `update-schedule-pattern` **必需参数：`--pattern-id`**。可选参数：`--name`、`--description`、`--notes`
- `get-schedule-pattern` **必需参数：`--pattern-id`
- `list-schedule-patterns` **可选参数：`--company-id`、`--pattern-type`、`--is-active`、`--search`、`--limit`
- `get-day-type-calendar` **必需参数：`--pattern-id`、`--date-range-start`、`--date-range-end`
- `get-pattern-calendar` **必需参数：`--pattern-id`
- `get-contact-hours` **必需参数：`--pattern-id`。可选参数：`--section-id`、`--master-schedule-id`
- `update-master-schedule` **必需参数：`--master-schedule-id`。可选参数：`--name`、`--build-notes`、`--schedule-status`
- `get-master-schedule` **可选参数：`--master-schedule-id`、`--naming-series`
- `list-master-schedules` **可选参数：`--company-id`、`--schedule-status`、`--academic-term-id`
- `add-section-to-schedule` **必需参数：`--master-schedule-id`、`--section-id`
- `delete-section-meeting` **必需参数：`--section-meeting-id`
- `list-section-meetings` **必需参数：`--master-schedule-id`。可选参数：`--section-id`、`--day-type-id`、`--instructor-id`、`--room-id`
- `get-schedule-matrix` **必需参数：`--master-schedule-id`
- `update-schedule-lock` **必需参数：`--master-schedule-id`。可选参数：`--locked-by`
- `create-schedule-clone` **必需参数：`--master-schedule-id`、`--target-academic-term-id`。可选参数：`--name`、`--company-id`

## 第二级 — 课程请求

- `activate-course-requests` **必需参数：`--academic-term-id`
- `submit-course-request` **必需参数：`--student-id`、`--academic-term-id`、`--course-id`。可选参数：`--request-priority`、`--is-alternate`、`--alternate-for-course-id`、`--has-iep-flag`、`--prerequisite-override`、`--prerequisite-override-by`、`--prerequisite-override-note`、`--submitted-by`、`--company-id`
- `approve-course-requests` **必需参数：`--academic-term-id`、`--approved-by`。可选参数：`--course-id`
- `get-demand-report` **必需参数：`--academic-term-id`
- `get-singleton-analysis` **必需参数：`--academic-term-id`。可选参数：`--min-requests`
- `get-course-demand-analysis` **必需参数：`--academic-term-id`
- `get-fulfillment-report` **可选参数：`--master-schedule-id`、`--academic-term-id`
- `get-load-balance-report` **必需参数：`--master-schedule-id`
- `update-course-request` **必需参数：`--course-request-id`。可选参数：`--request-priority`、`--is-alternate`、`--has-iep-flag`
- `get-course-request` **必需参数：`--course-request-id`
- `list-course-requests` **可选参数：`--student-id`、`--academic-term-id`、`--course-id`、`--request-status`
- `complete-course-requests` **必需参数：`--academic-term-id`

## 第二级 — 冲突解决

- `list-conflicts` **必需参数：`--master-schedule-id`。可选参数：`--conflict-type`、`--severity`、`--conflict-status`
- `get-conflict` **必需参数：`--conflict-id`
- `complete-conflict` **必需参数：`--conflict-id`、`--resolution-notes`。可选参数：`--resolved-by`
- `accept-conflict` **必需参数：`--conflict-id`（非紧急情况）。可选参数：`--resolution-notes`、`--resolved-by`
- `get-conflict-summary` **必需参数：`--master-schedule-id`
- `get-singleton-conflict-map` **必需参数：`--master-schedule-id`
- `get-student-conflict-report` **必需参数：`--master-schedule-id`

## 第二级 — 教室分配

- `assign-room` **必需参数：`--section-meeting-id`、`--room-id`。可选参数：`--booking-type`、`--accessibility_required`、`--booked-by`
- `propose-room` **必需参数：`--section-meeting-id`。可选参数：`--room-type`、`--accessibility_required`
- `assign-rooms` **必需参数：`--master-schedule-id`。可选参数：`--room-type`
- `delete-room-assignment` **必需参数：`--section-meeting-id`、`--booking-id`
- `add-room-block` **必需参数：`--room-id`、`--day-type-id`、`--bell-period-id`、`--booking-title`。可选参数：`--booked-by`、`--booking-type`
- `update-room-swap` **必需参数：`--section-meeting-id`（A）、`--section-meeting-id-b`（B）`
- `get-room-availability` **必需参数：`--room-id`、`--master-schedule-id`
- `get-room-utilization-report` **必需参数：`--master-schedule-id`
- `list-rooms-by-features` **可选参数：`--company-id`、`--room-type`、`--capacity`、`--building`、`--features`（JSON）
- `assign-room-emergency` **必需参数：`--room-id`、`--target-room-id`、`--master-schedule-id`

## 第三级 — 教师约束

- `add-instructor-constraint` **必需参数：`--instructor-id`、`--academic-term-id`、`--constraint-type`（`unavailable`、`preferred`、`max_periods_per_day`、`max_consecutive_periods`、`requires_prep_period`、`preferred_building`）。可选参数：`--day-type-id`、`--bell-period-id`、`--constraint-value`、`--constraint-notes`、`--priority`（`hard`、`soft`、`preference`）
- `update-instructor-constraint` **必需参数：`--constraint-id`。可选参数：`--constraint-value`、`--constraint-notes`、`--priority`、`--is-active`
- `list-instructor-constraints` **必需参数：`--instructor-id`、`--academic-term-id`、`--constraint-type`、`--is-active`
- `delete-instructor-constraint` **必需参数：`--constraint-id`

---

## 生命周期规则

- **主调度计划**：`draft → building → review → published → locked → archived`。如果存在未解决的严重冲突，则无法发布。所有课程安排在发布时都会设置为 `scheduled`，学期状态设置为 `enrollment_open`。
- **课程请求**：`draft → submitted → approved → scheduled / alternate_used / unfulfilled`。任何请求都可以被 `withdrawn`。
- **冲突**：`open → resolving → resolved / accepted / superseded`。

## 工作流程

1. **模式创建**：`add-schedule-pattern → add-day-type (×N) → add-bell-period (×N) → activate-schedule-pattern`
2. **需求处理**：`activate-course-requests → submit-course-request (×N) → approve-course-requests → get-demand-report → complete-course-requests`
3. **调度构建**：`create-master-schedule → add-section-to-schedule (×N) → add-section-meeting (×N) → assign-room OR assign-rooms → update-master-schedule (status=review)`
4. **发布**：`generate-conflict-check → get-conflict-summary → [complete-conflict|accept-conflict] (×N) → submit-master-schedule → update-schedule-lock`
5. **紧急情况**：`get-room-availability → assign-room-emergency → generate-conflict-check`