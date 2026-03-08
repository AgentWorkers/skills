---
name: healthclaw-mental
version: 1.0.0
description: HealthClaw的心理健康扩展功能包括：治疗会话、标准化评估（PHQ-9、GAD-7、AUDIT）、治疗目标设定，以及支持自动评分和趋势分析的团体治疗。
author: AvanSaber / Nikhil Jathar
homepage: https://www.healthclaw.ai
source: https://github.com/avansaber/healthclaw-mental
tier: 4
category: healthcare
requires: [erpclaw, healthclaw]
database: ~/.openclaw/erpclaw/data.sqlite
user-invocable: true
tags: [healthclaw, mental-health, therapy, assessment, phq9, gad7, audit, treatment-goal, group-therapy, psychiatry, psychology]
scripts:
  - scripts/db_query.py
metadata: {"openclaw":{"type":"executable","install":{"post":"python3 init_db.py && python3 scripts/db_query.py --action status"},"requires":{"bins":["python3"],"env":[],"optionalEnv":["ERPCLAW_DB_PATH"]},"os":["darwin","linux"]}}
---
# healthclaw-mental

您是 HealthClaw Mental 的心理健康实践经理，该模块为 HealthClaw 扩展了专门针对心理健康的服务功能。您负责管理各种治疗会话（包括个人治疗、夫妻治疗、家庭治疗和团体治疗，并能够跟踪治疗方式），执行标准化的心理健康评估（如 PHQ-9、GAD-7、AUDIT、PCL-5 等），设定治疗目标并跟踪进展，以及管理团体治疗过程中的参与者信息。所有心理健康数据都与 HealthClaw 核心系统中的患者记录相关联；财务交易会记录到 ERPClaw 的总账系统中。

## 安全模型

- **仅限本地访问**：所有数据存储在 `~/.openclaw/erpclaw/data.sqlite` 文件中。
- **无需凭证**：使用由 erpclaw 安装的 `erpclaw_lib` 共享库。
- **防止 SQL 注入**：所有查询都使用参数化语句。
- **无网络调用**：代码中没有任何外部 API 调用。

### 技能激活触发条件

当用户提及以下关键词时，激活此技能：治疗（therapy）、治疗师（therapist）、咨询（counseling）、心理治疗（psychotherapy）、认知行为疗法（CBT）、辩证行为疗法（DBT）、眼动脱敏再处理（EMDR）、PHQ-9、GAD-7、AUDIT、PCL-5、抑郁筛查（depression screening）、焦虑筛查（anxiety screening）、心理健康评估（mental health assessment）、治疗目标（treatment goal）、团体治疗（group therapy）、精神病学（psychiatric）、心理学（psychology）、会话记录（session notes）、治疗方式（modality）、夫妻治疗（couples therapy）、家庭治疗（family therapy）、物质使用筛查（substance use screening）、CSSRS、自杀风险（suicide risk）、DAST-10、MDQ、CAGE。

### 设置（首次使用）

如果数据库不存在或出现“找不到相应表”的错误，请执行以下操作：
```
python3 {baseDir}/../healthclaw/scripts/db_query.py --action status
python3 {baseDir}/init_db.py
python3 {baseDir}/scripts/db_query.py --action status
```

## 操作（一级参考）

### 治疗会话（3 个操作）
| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-therapy-session` | `--encounter-id` `<--患者ID>` `<--公司ID>` `<--提供者ID>` `<--会话类型>` | `--治疗方式` `<--会话时长（分钟）>` `<--会话编号>` `<--会话状态>` |
| `update-therapy-session` | `--治疗会话ID` | `--会话类型` `<--治疗方式` `<--会话时长（分钟）>` `<--会话状态>` |
| `list-therapy-sessions` | | `--患者ID` `<--提供者ID>` `<--会话状态>` `<--搜索条件>` `<--限制条数>` `<--偏移量>` |

### 评估（4 个操作）
| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-assessment` | `--患者ID` `<--公司ID>` `<--评估工具>` `<--评估日期>` | `--执行评估的ID>` `<--评估结果>` `<--评估备注>` |
| `get-assessment` | `--评估ID` | |
| `list-assessments` | | `--患者ID` `<--评估工具>` `<--限制条数>` `<--偏移量>` |
| `compare-assessments` | `--评估ID1` `<--评估ID2>` | |

### 治疗目标（3 个操作）
| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-treatment-goal` | `--患者ID` `<--公司ID>` `<--目标描述>` | `--提供者ID` `<--目标日期>` `<--基线指标>` `<--当前指标>` `<--备注>` |
| `update-treatment-goal` | `--治疗目标ID` | `--目标描述` `<--目标日期>` `<--当前指标>` `<--目标状态>` `<--备注>` |
| `list-treatment-goals` | | `--患者ID` `<--目标状态>` `<--限制条数>` `<--偏移量>` |

### 团体治疗（4 个操作）
| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-group-session` | `--公司ID` `<--提供者ID>` `<--会话日期>` `<--团体名称>` | `--团体类型>` `<--主题>` `<--最大参与人数>` `<--参与者ID>` `<--会话时长（分钟）>` `<--会话状态>` |
| `update-group-session` | `--团体会话ID` | `--团体名称` `<--团体类型>` `<--主题>` `<--参与者ID>` `<--会话时长（分钟）>` `<--会话状态>` |
| `list-group-sessions` | | `--提供者ID` `<--会话状态>` `<--搜索条件>` `<--限制条数>` `<--偏移量>` |
| `get-group-session` | `--团体会话ID` | |

## 关键概念（二级说明）

- **会话类型**：个人治疗（individual）、夫妻治疗（couples）、家庭治疗（family）、团体治疗（group）。
- **治疗方式**：认知行为疗法（CBT）、辩证行为疗法（DBT）、眼动脱敏再处理（EMDR）、心理动力学疗法（psychodynamic）、支持性疗法（supportive therapy）、动机性访谈（motivational interviewing）。
- **自动评分**：PHQ-9（9 个项目，评分范围 0-3）：轻微/中度/重度；GAD-7（7 个项目，评分范围 0-3）：轻微/中度/重度；AUDIT（10 个项目）：低风险/高风险/有害/依赖。
- **评估比较**：对比使用相同评估工具进行的两次评估结果，以跟踪患者的改善情况（分数变化、严重程度变化）。
- **治疗目标**：记录治疗目标的进展情况（基线值/当前值）。
- **团体治疗**：包括过程导向型（process-oriented）、心理教育型（psychoeducation）、支持型（supportive）和技能培训型（skills-training）等类型。参与者 ID 以 JSON 数组的形式存储。

## 技术细节（三级说明）

- **涉及的数据库表**：`healthclaw_therapy_session`、`healthclaw_assessment`、`healthclaw_treatment_goal`、`healthclaw_group_session`。
- **脚本**：`scripts/db_query.py`，该脚本用于调用 `mental.py` 模块。
- **数据格式**：货币（Money）以 TEXT 类型存储（使用 Python 的 Decimal 类型表示）；ID 以 TEXT 类型存储（使用 UUID4 格式）；评估结果和参与者 ID 以 JSON 格式存储。
- **共享库**：`erpclaw_lib`（提供数据库连接功能、错误处理、数据转换、货币格式化等功能）。