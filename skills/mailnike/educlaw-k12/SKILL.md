---
name: educlaw-k12
version: 1.0.0
description: EduClaw K-12扩展功能：学科管理、学生健康记录管理、特殊教育（IDEA/IEP/504相关流程）以及年级晋升工作流程。
author: ERPForge
parent: educlaw
requires: [erpclaw, erpclaw-people, educlaw]
database: ~/.openclaw/erpclaw/data.sqlite
user-invocable: true
scripts:
  - scripts/db_query.py
domains:
  - discipline
  - health_records
  - special_education
  - grade_promotion
total_actions: 76
tables: 23
metadata: {"openclaw":{"type":"executable","install":{"post":"python3 init_db.py && python3 scripts/db_query.py --action status"},"requires":{"bins":["python3"],"env":[],"optionalEnv":[]},"os":["darwin","linux"]}}
---
# EduClaw K-12扩展功能

EduClaw SIS的子模块，专为K-12教育阶段设计，新增了以下特定工作流程：  
- 行为事件跟踪（符合IDEA MDR规定）；  
- 学生健康记录管理（遵循FERPA数据访问规范）；  
- 完整的IDEA Part B流程管理（包括转介、个别化教育计划（IEP）制定、服务提供及进度跟踪）；  
- 第504条教育法规相关计划（Section 504 plans）；  
- 年终成绩晋升功能（支持批量处理）。

## 安全模型  

- **仅本地存储**：所有数据保存在`~/.openclaw/erpclaw/data.sqlite`文件中。  
- **完全离线运行**：不依赖外部API、遥测技术或云服务。  
- **无需用户名和密码**：使用`erpclaw_lib`共享库（由`erpclaw`工具安装）。  
- **防SQL注入**：所有查询均采用参数化语句。  
- **符合FERPA法规**：健康记录、纪律处分记录及特殊教育相关数据的访问操作均被详细记录。  
- **遵守IDEA规定**：IEP目标和服务内容不可更改；任何修改需重新制定IEP。  
- **数据不可篡改**：办公室访问记录、药物使用记录、免疫接种记录及晋升决定生成后均不可修改。

## 快速入门  

---  
## 第一层：常用操作  

### 纪律处分  

| 操作          | 描述                                      |  
|------------------|-----------------------------------------|  
| `add-discipline-incident` | 创建新的行为事件记录            |  
| `add-discipline-student` | 添加涉事学生（违规者/受害者/目击者/旁观者）           |  
| `add-discipline-action` | 添加处分措施；自动更新累计停学天数           |  
| `get-discipline-incident` | 获取包含所有学生及处分信息的事件记录（符合FERPA法规）   |  
| `complete-discipline-incident` | 关闭事件记录；设置审核人及时间戳            |  
| `add-discipline-notification` | 为涉事学生生成监护人通知                     |  

### 健康记录  

| 操作          | 描述                                      |  
|------------------|-----------------------------------------|  
| `add-health-profile` | 创建学生健康档案（每位学生一份）              |  
| `get-health-profile` | 获取学生健康档案（符合FERPA法规）                |  
| `get-emergency-health-info` | 快速查询紧急健康信息（过敏史、EpiPen信息、紧急联系人）    |  
| `add-office-visit` | 记录护士访问情况（数据不可篡改）                |  
| `record-medication-admin` | 记录药物使用情况；更新药物库存                |  
| `add-immunization` | 添加免疫接种记录（数据不可篡改）                |  
| `get-immunization-compliance` | 检查免疫接种是否符合年级要求                |  

### 特殊教育  

| 操作          | 描述                                      |  
|------------------|-----------------------------------------|  
| `create-sped-referral` | 启动IDEA转介流程（60天评估周期开始）           |  
| `add-iep` | 创建IEP草案                         |  
| `activate-iep` | 在家长同意下激活IEP；原有IEP将被替换           |  
| `add-iep-goal` | 添加可衡量的年度目标                        |  
| `add-iep-service` | 向IEP中添加强制性服务项目                |  
| `record-iep-service-session` | 记录服务提供情况；更新服务总时长             |  
| `get-active-iep` | 获取学生的当前IEP（包含目标、服务及执行团队）           |  
| `get-active-504-plan` | 获取学生的当前第504条教育法规相关计划（符合FERPA法规）     |  

### 年终成绩晋升  

| 操作          | 描述                                      |  
|------------------|-----------------------------------------|  
| `create-promotion-review` | 创建年终评估记录；自动统计纪律处分次数           |  
| `submit-promotion-decision` | 记录最终晋升/保留/条件性晋升的不可更改决定           |  
| `apply-grade-promotion` | 提升所有符合条件学生的成绩；12年级学生自动晋升       |  
| `list-at-risk-students` | 标记成绩/出勤未达标准的学生                   |  

---  
## 第二层：辅助操作  

### 纪律处分  

| 操作          | 关键参数                                      |  
|------------------|-----------------------------------------|  
| `update-discipline-incident` | `--incident-id`（事件ID）；可更新字段             |  
| `list-discipline-incidents` | `--academic-year-id`（学年ID）、`--severity`（严重程度）、`--incident-status`（事件状态）、`--student-id`（学生ID） |  
| `get-discipline-history` | `--student-id`（学生ID）；查询所有年份的历史记录       |  
| `get-cumulative-suspension-days` | `--student-id`（学生ID）、`--academic-year-id`（学年ID）；检查累计停学天数 |  
| `add-manifestation-review` | `--discipline-student-id`（学生ID）、`--iep-id`（IEP ID）、`--mdr-date`（MDR日期） |  
| `update-manifestation-review` | `--mdr-id`（MDR ID）、`--determination`（处理结果）、`--outcome-action`（处理方式） |  
| `add-pbis-recognition` | `--student-id`（学生ID）、`--incident-date`（事件日期）、`--description`（描述） |  

### 健康记录  

| 操作          | 关键参数                                      |  
|------------------|-----------------------------------------|  
| `update-health-profile` | `--student-id`（学生ID）；可更新字段             |  
| `submit-health-profile-verification` | `--student-id`（学生ID）、`--last-verified-by`（最后审核人）     |  
| `list-office-visits` | `--student-id`（学生ID）、`--date-from`（开始日期）、`--date-to`（结束日期）、`--disposition`（访问结果） |  
| `get-office-visit` | `--visit-id`（访问记录ID）                     |  
| `add-student-medication` | `--student-id`（学生ID）、`--medication-name`（药物名称）、`--route`（给药途径）、`--frequency`（使用频率） |  
| `update-student-medication` | `--medication-id`（药物ID）、`--medication-status`（药物状态）、`--supply-count`（剩余数量） |  
| `list-student-medications` | `--student-id`（学生ID）或`--student-medication-id`（药物ID）     |  
| `list-medication-logs` | `--student-id`（学生ID）或`--student-medication-id`（药物ID）     |  
| `add-immunization-waiver` | `--student-id`（学生ID）、`--vaccine-name`（疫苗名称）、`--waiver-type`（豁免类型） |  
| `update-immunization-waiver` | `--waiver-id`（豁免ID）、`--waiver-status`（豁免状态）     |  
| `get-immunization-record` | `--student-id`（学生ID）；查询所有接种记录及豁免情况     |  
| `list-health-alerts` | 全校范围内的健康警报信息（严重过敏、豁免情况、药物库存不足）     |  

### 特殊教育  

| 操作          | 关键参数                                      |  
|------------------|-----------------------------------------|  
| `update-sped-referral` | `--referral-id`（转介ID）、`--referral-status`（转介状态）、`--consent-received-date`（同意接收日期） |  
| `get-sped-referral` | `--referral-id`（转介ID）；包含评估结果           |  
| `list-sped-referrals` | `--referral-status`（转介状态）、`--approaching-deadline`（截止日期） |  
| `add-sped-evaluation` | `--referral-id`（转介ID）、`--evaluation-type`（评估类型）、`--evaluation-date`（评估日期） |  
| `list-sped-evaluations` | `--referral-id`（转介ID）；查询所有评估记录         |  
| `record-sped-eligibility` | `--referral-id`（转介ID）、`--is-eligible`（是否符合资格）、`--primary-disability`（主要残疾类型） |  
| `get-sped-eligibility` | `--student-id`（学生ID）或`--eligibility-id`（资格ID）     |  
| `update-iep` | `--iep-id`（IEP ID）；仅修改草案字段           |  
| `add-iep-amendment` | `--iep-id`（现有IEP ID）；创建修订内容           |  
| `get-iep` | `--iep-id`（IEP ID）；查询IEP详细信息           |  
| `list-iep-deadlines` | `--days-window`（默认30天）；查询修订截止日期         |  
| `list-reevaluation-due` | `--days-window`（默认90天）；查询重新评估截止日期         |  
| `list-iep-goals` | `--iep-id`（IEP ID）；查询所有目标             |  
| `list-iep-services` | `--iep-id`（IEP ID）；查询所有服务项目         |  
| `list-iep-service-logs` | `--iep-service-id`（服务记录ID）；查询服务执行日志         |  
| `add-iep-team-member` | `--iep-id`（IEP ID）、`--member-type`（团队成员类型）、`--member-name`（成员名称） |  
| `record-iep-progress` | `--iep-goal-id`（目标ID）、`--progress-rating`（进度评分）、`--reporting-period`（报告周期） |  
| `add-504-plan` | `--student-id`（学生ID）、`--meeting-date`（会议日期）、`--accommodations`（支持措施，JSON格式） |  
| `update-504-plan` | `--plan-504-id`（计划ID）、`--plan-status`（计划状态）、`--accommodations`（支持措施） |  

### 年终成绩晋升  

| 操作          | 关键参数                                      |  
|------------------|-----------------------------------------|  
| `update-promotion-review` | `--review-id`（评估记录ID）、`--teacher-recommendation`（教师建议）、`--counselor-recommendation`（辅导员建议） |  
| `list-promotion-reviews` | `--academic-year-id`（学年ID）、`--grade-level`（年级等级）、`--review-status`（评估状态） |  
| `get-promotion-decision` | `--decision-id`（决策ID）或`--student-id`（学生ID）+`--academic-year-id`（学年ID） |  
| `add-promotion-notification` | `--decision-id`（决策ID）；生成监护人通知           |  
| `create-intervention-plan` | `--student-id`（学生ID）、`--trigger`（触发条件）、`--intervention-types`（干预类型） |  
| `update-intervention-plan` | `--intervention-plan-id`（干预计划ID）、`--plan-status`（计划状态）、`--outcome-notes`（结果备注） |  
| `list-intervention-plans` | `--academic-year-id`（学年ID）、`--plan-status`（计划状态）、`--student-id`（学生ID） |  

---  
## 第三层：报告与高级工作流程  

| 操作          | 描述                                      |  
|------------------|-----------------------------------------|  
| `generate-discipline-report` | 提供全校范围内的纪律处分数据分析（按类型、严重程度、地点、PBIS比率分类） |  
| `generate-discipline-state-report` | 以州级格式报告纪律处分情况（按年级/残疾类型分类）；统计MDR次数   |  
| `generate-immunization-report` | 按年级统计免疫接种合规情况；生成年度免疫接种状态报告     |  
| `get-service-compliance-report` | 对比计划中的IEP服务提供时间与实际执行时间；检测差异       |  
| `generate-iep-progress-report` | 向家长展示学生目标完成情况及进度评分           |  
| `generate-promotion-report` | 按年级汇总晋升结果（包括晋升/保留/条件性晋升情况）       |  

## 关键工作流程  

### 1. 纪律处分事件 → MDR（IDEA适用学生）  

---  
### 2. 健康记录注册  

---  
### 3. 完整的IDEA流程管理  

---  
### 4. 年终成绩晋升  

---  
## FERPA/隐私政策说明  

- **健康记录相关操作**（`get-health-profile`、`list-office-visits`、`get-office-visit`、`get-immunization-record`、`get-emergency-health-info`）会被记录到`educlaw_data_access_log`文件中，数据类别为`health`。  
- **纪律处分相关操作**（`get-discipline-incident`、`get-discipline-history`）会被记录到`educlaw_data_access_log`文件中，数据类别为`discipline`。  
- **特殊教育相关操作**（`get-sped-referral`、`get-active-iep`、`get-iep`、`record-sped-eligibility`、`get-active-504-plan`、`generate-iep-progress-report`）会被记录到`educlaw_data_access_log`文件中，数据类别为`special_education`。  
- 紧急健康访问情况会在FERPA日志中标记为`is_emergency_access=1`。  

`special_education`数据类别用于记录与IEP和第504条教育法规相关的访问操作。  

## 业务规则  

- **数据不可篡改**：  
  - 已关闭的纪律处分事件无法重新开启。  
  - 每位学生的累计停学天数（`cumulative_suspension_days_ytd`）为该学年内的ISS（Institutional Suspension）和OSS（Office Suspension）累计值。  
  - 符合IDEA规定的学生在被开除前必须接受至少10天的MDR（Minority Disability Review）评估。  
  - 每位学生仅有一个健康档案（`UNIQUE(student_id)`。  
  - 访问记录、药物使用记录及免疫接种记录均为不可篡改数据。  
  - 药物使用相关的豁免记录需要指定`--issuing-physician`（开具医生信息）。  

- **特殊教育相关规则**：  
  - 每位学生同一时间最多只能有一个处于`iep_status='active'状态的IEP。  
  IEP的目标和服务内容不可更改；任何修改均需重新制定IEP。  
  - 第504条教育法规相关的评估截止日期为`consentreceived_date + 60天`。  
  - 对于16岁及以上的学生，IEP的过渡计划（transition_plan_required）为必填项。  
  - 每位学生每年仅进行一次晋升评估。  
  `submit-promotion-decision`操作会生成不可更改的晋升记录。  
  `apply-grade-promotion`操作具有幂等性（多次执行结果相同）。  

## 数据库  

所有数据存储在`~/.openclaw/erpclaw/data.sqlite`共享SQLite数据库中。  
运行`python3 init_db.py`命令可创建23个K-12教育阶段专用数据库表（需先确保`erpclaw`和`educlaw`相关父表已存在）。  

### 新增的23个数据库表：  

| 领域            | 表名                                      |  
|------------------|-----------------------------------------|  
| Discipline        | `educlaw_k12_discipline_incident`、`educlaw_k12_discipline_student`、`educlaw_k12_discipline_action`、`educlaw_k12_manifestation_review` |  
| Health Records     | `educlaw_k12_health_profile`、`educlaw_k12_health_visit`、`educlaw_k12_student_medication`、`educlaw_k12_medication_log`、`educlaw_k12_immunization`、`educlaw_k12_immunization_waiver` |  
| Special Education    | `educlaw_k12_sped_referral`、`educlaw_k12_sped_evaluation`、`educlaw_k12_sped_eligibility`、`educlaw_k12_iep`、`educlaw_k12_iep_goal`、`educlaw_k12_iep_service`、`educlaw_k12_iep_service_log`、`educlaw_k12_iep_team_member`、`educlaw_k12_iep_progress`、`educlaw_k12_504_plan` |  
| Grade Promotion    | `educlaw_k12_promotion_review`、`educlaw_k12_promotion_decision`、`educlaw_k12_intervention_plan` |