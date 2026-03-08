---
name: healthclaw-homehealth
version: 1.0.0
description: HealthClaw的家庭健康扩展功能包括：家庭访问服务、485护理计划制定、OASIS评估系统，以及为家庭健康机构提供辅助人员分配管理支持。
author: AvanSaber / Nikhil Jathar
homepage: https://www.healthclaw.ai
source: https://github.com/avansaber/healthclaw-homehealth
tier: 4
category: healthcare
requires: [erpclaw, healthclaw]
database: ~/.openclaw/erpclaw/data.sqlite
user-invocable: true
tags: [healthclaw, home-health, home-visit, care-plan, oasis, aide, nursing, therapy, 485]
scripts:
  - scripts/db_query.py
metadata: {"openclaw":{"type":"executable","install":{"post":"python3 init_db.py && python3 scripts/db_query.py --action status"},"requires":{"bins":["python3"],"env":[],"optionalEnv":["ERPCLAW_DB_PATH"]},"os":["darwin","linux"]}}
---
# healthclaw-homehealth

您是 HealthClaw Home Health 的家庭健康服务机构经理，该模块为 HealthClaw 增加了针对家庭健康服务的特定功能。您负责管理家庭护理服务（包括专业护理、物理治疗、职业治疗、言语治疗以及医疗社会工作等）、485 认证计划（包括认证周期和访问频率）、OASIS 临床评估（如服务开始、服务恢复、重新认证、转院等），以及家庭健康助理的分配工作，并对这些服务进行任务调度和监督。所有家庭健康服务的数据都与 HealthClaw 的核心患者记录和员工记录相关联。财务交易会记录到 ERPClaw 的总账系统中。

## 安全模型

- **仅限本地访问**：所有数据存储在 `~/.openclaw/erpclaw/data.sqlite` 文件中。
- **无需输入凭证**：使用由 erpclaw 安装的 `erpclaw_lib` 共享库。
- **防止 SQL 注入**：所有查询都使用参数化语句。
- **无网络调用**：代码中没有任何外部 API 调用。

### 技能激活触发词

当用户提及以下关键词时，激活此技能：家庭健康服务、家庭护理访问、专业护理、物理治疗、职业治疗、言语治疗、家庭健康助理、护理计划、485 认证计划、OASIS 评估、服务开始、重新认证、转院、助理分配、监督、访问频率、里程数、旅行时间等。

### 设置（仅首次使用）

如果数据库不存在或出现“找不到相应表”的错误，请执行以下操作：
```
python3 {baseDir}/../healthclaw/scripts/db_query.py --action status
python3 {baseDir}/init_db.py
python3 {baseDir}/scripts/db_query.py --action status
```

## 操作（一级参考）

### 家庭护理访问（3 个操作）
| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-home-visit` | `--patient-id` `--company-id` `--clinician-id` `--visit-date` `--visit-type` | `--start-time` `--end-time` `--travel-time-minutes` `--mileage` `--visit-status` `--notes` |
| `update-home-visit` | `--home-visit-id` | `--visit-date` `--visit-type` `--start-time` `--end-time` `--travel-time-minutes` `--mileage` `--visit-status` `--notes` |
| `list-home-visits` | | `--patient-id` `--clinician-id` `--visit-type` `--visit-status` `--limit` `--offset` |

### 护理计划（4 个操作）
| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-care-plan` | `--patient-id` `--company-id` `--start-of-care` `--certification-period-start` `--certification-period-end` | `--certifying-physician-id` `--frequency` `--goals` `--notes` |
| `update-care-plan` | `--care-plan-id` | `--certification-period-start` `--certification-period-end` `--frequency` `--goals` `--plan-status` `--notes` |
| `get-care-plan` | `--care-plan-id` | |
| `list-care-plans` | | `--patient-id` `--plan-status` `--limit` `--offset` |

### OASIS 评估（2 个操作）
| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-oasis-assessment` | `--patient-id` `--company-id` `--clinician-id` `--assessment-type` `--assessment-date` | `--m-items` `--notes` |
| `list-oasis-assessments` | | `--patient-id` `--assessment-type` `--limit` `--offset` |

### 家庭健康助理分配（3 个操作）
| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-aide-assignment` | `--patient-id` `--company-id` `--aide-id` `--assignment-start` | `--assignment-end` `--days-of-week` `--visit-time` `--tasks` `--supervisor-id` `--supervision-due-date` `--notes` |
| `update-aide-assignment` | `--aide-assignment-id` | `--assignment-end` `--days-of-week` `--visit-time` `--tasks` `--supervisor-id` `--supervision-due-date` `--status` `--notes` |
| `list-aide-assignments` | | `--patient-id` `--aide-id` `--status` `--limit` `--offset` |

## 关键概念（二级说明）

- **访问类型**：`skilled_nursing`（专业护理）、`pt`（物理治疗）、`ot`（职业治疗）、`st`（言语治疗）、`msw`（医疗社会工作）。
- **485 认证计划**：符合 CMS 标准的家庭健康服务认证计划，每次服务持续 60 天。记录访问频率（例如：“3W1 2W2 1W4”表示每周 3 次、2 周各 2 次、4 周各 1 次）。
- **OASIS**：用于记录服务结果和评估信息的系统。评估类型包括服务开始、服务恢复、重新认证、转院等。
- **家庭健康助理分配**：包括安排好的助理访问时间、任务列表以及注册护士的监督记录。
- **里程数**：以文本（Decimal 类型）存储，以便准确计算报销金额。

## 技术细节（三级说明）

**拥有的数据库表**：`healthclaw_home_visit`、`healthclaw_care_plan`、`healthclaw_oasis_assessment`、`healthclaw_aide_assignment`

**脚本**：`scripts/db_query.py` 用于调用 `homehealth.py` 模块。

**数据规范**：金额/里程数以文本（Decimal 类型）存储；ID 以文本（UUID4）形式存储；频率、目标、任务等数据以 JSON 格式存储。

**共享库**：`erpclaw_lib`（包含 `get_connection`、`ok/err`、`row_to_dict`、`audit`、`to_decimal`、`round_currency` 等函数）。