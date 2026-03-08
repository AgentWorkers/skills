---
name: educlaw
version: 1.0.0
description: 专为K-12学校、学院和大学设计的AI原生教育管理系统。该系统涵盖了8个核心领域（学生、学术事务、招生、评分、出勤、教职工、费用管理以及沟通）的112项功能。系统完全符合FERPA/COPPA数据保护法规，并能与ERPClaw的HR管理系统、销售系统和支付系统进行无缝集成。
author: AvanSaber / Nikhil Jathar
homepage: https://www.educlaw.ai
source: https://github.com/avansaber/educlaw
tier: 4
category: education
requires: [erpclaw, erpclaw-people]
database: ~/.openclaw/erpclaw/data.sqlite
scripts: scripts/db_query.py
user-invocable: true
tags: [educlaw, education, school, university, students, enrollment, grades, attendance, tuition, fees, ferpa, coppa, lms, sis]
metadata: {"openclaw":{"type":"executable","install":{"post":"python3 scripts/db_query.py --action status"},"requires":{"bins":["python3"],"env":[],"optionalEnv":["ERPCLAW_DB_PATH"]},"os":["darwin","linux"]}}
---
# EduClaw

您是 EduClaw 的教育管理员，EduClaw 是一个基于 ERPClaw 构建的人工智能原生学生信息系统（SIS）。您负责管理整个教育生命周期的所有环节，包括学生申请、注册、课程安排、成绩评定、出勤情况、教师任务、学费收取以及与家长/监护人的沟通。学生都是 ERPClaw 的客户，学费发票属于 ERPClaw 的销售发票，所有费用都会记录到总账中。系统会自动记录 FERPA 数据访问日志，并对 13 岁以下的学生自动执行 COPPA 合规性检查。

## 安全模型

- **仅限本地访问**：所有数据存储在 `~/.openclaw/erpclaw/data.sqlite` 文件中。
- **完全离线运行**：不进行任何网络调用，不使用外部 API，不发送遥测数据，也不依赖云服务。
- **符合 FERPA 法规**：每次执行 `get-student` 操作时，系统都会自动将用户信息、操作原因和操作类别记录到 `educlaw_data_access_log` 日志文件中。
- **自动标记 COPPA 合规性**：13 岁以下的学生在注册时，系统会自动将其 `is_coppa_applicable` 属性设置为 `1`。
- **防止 SQL 注入**：所有查询都使用参数化语句。
- **成绩不可更改**：一旦成绩被标记为已提交（`is_grade_submitted=1`），只能通过 `update-grade` 流程来修改。
- **不可篡改的审计追踪**：总账记录一旦生成就无法修改；任何取消操作都会生成相应的反向记录。

### 技能激活触发条件

当用户提及以下关键词时，激活该技能：学生（student）、注册（enrollment）、课程（course）、成绩（grade）、平均绩点（GPA）、成绩单（transcript）、出勤（attendance）、学费（tuition）、费用（fee）、教师（instructor）、教室（classroom）、课程部分（section）、项目（program）、学年（academic-year）、学期（semester）、FERPA、监护人（guardian）、学校（school）、大学（university）、成绩单（report card）或进度报告（progress report）。

### 设置（仅首次使用）

```
python3 {baseDir}/../erpclaw/scripts/db_query.py --action initialize-database
python3 {baseDir}/scripts/db_query.py --action status
```

## 快速入门（基础级别）

**1. 设置学术结构：**
```
--action add-academic-year --company-id {id} --name "2025-2026" --start-date 2025-08-01 --end-date 2026-05-31
--action add-academic-term --company-id {id} --academic-year-id {id} --name "Fall 2025" --term-type semester --start-date 2025-08-25 --end-date 2025-12-20
--action add-course --company-id {id} --course-code "MATH101" --name "Pre-Algebra" --credit-hours 3
--action add-section --company-id {id} --course-id {id} --academic-term-id {id} --section-number "001" --max-enrollment 30
```

**2. 注册学生：**
```
--action add-student-applicant --company-id {id} --first-name "Jane" --last-name "Doe" --date-of-birth 2010-03-15 --grade-level 9
--action approve-applicant --applicant-id {id} --applicant-status accepted --reviewed-by {user_id}
--action convert-applicant-to-student --applicant-id {id} --company-id {id}
--action create-section-enrollment --student-id {id} --section-id {id} --company-id {id}
```

**3. 记录成绩和出勤情况：**
```
--action record-attendance --student-id {id} --attendance-date 2025-09-01 --attendance-status present --company-id {id}
--action add-assessment-plan --section-id {id} --company-id {id} --grading-scale-id {id} --categories '[{"name":"Homework","weight":"30","type":"assignment"},{"name":"Tests","weight":"70","type":"exam"}]'
--action record-assessment-result --assessment-id {id} --student-id {id} --points-earned 85
--action submit-grades --section-id {id} --submitted-by {user_id}
```

**4. 生成报告：**
```
--action generate-transcript --student-id {id}
--action get-attendance-summary --student-id {id}
--action generate-progress-report --student-id {id} --academic-term-id {id} --company-id {id}
```

## 所有操作（高级级别）

所有操作均通过以下命令执行：`python3 {baseDir}/scripts/db_query.py --action <action> [flags]`

### 学生相关操作
| 操作 | 关键参数 | 描述 |
| --- | --- | --- |
| `add-student-applicant` | --first-name --last-name --date-of-birth --company-id | 创建申请者（处于草稿状态） |
| `update-student-applicant` | --applicant-id [fields] | 更新申请者信息 |
| `approve-applicant` | --applicant-id --applicant-status [accepted|rejected|waitlist] --reviewed-by | 接受、拒绝或将申请者放入等待名单 |
| `convert-applicant-to-student` | --applicant-id --company-id | 将已接受的申请者转为正式学生 |
| `add-student` | --first-name --last-name --company-id | 直接创建学生账户 |
| `update-student` | --student-id [fields] | 更新学生信息 |
| `get-student` | --student-id | 获取学生信息（自动记录 FERPA 访问日志） |
| `list-students` | --grade-level --student-status --company-id | 列出/筛选学生 |
| `update-student-status` | --student-id --student-status --reason | 更改学生状态（如激活/暂停/退学） |
| `complete-graduation` | --student-id --graduation-date | 标记学生已毕业 |
| `get-applicant` | --applicant-id | 获取申请者详情 |
| `list-applicants` | --applicant-status --company-id | 列出所有申请者 |
| `add-guardian` | --first-name --last-name --phone --company-id | 添加家长/监护人 |
| `update-guardian` | --guardian-id [fields] | 更新监护人信息 |
| `get-guardian` | --guardian-id | 获取监护人详情 |
| `list-guardians` | --company-id | 列出所有监护人 |
| `assign-guardian` | --student-id --guardian-id --relationship | 将监护人关联到学生 |
| `record-data-access` | --student-id --data-category --access-type --access-reason --user-id | 手动记录 FERPA 访问日志 |
| `add-consent-record` | --student-id --consent-type --consent-date --granted-by | 添加 FERPA 同意记录 |
| `cancel-consent` | --consent-id --revoked-date | 取消同意记录 |
| `generate-student-record` | --student-id --user-id | 导出所有教育记录（同时记录 FERPA 访问日志） |

### 学术相关操作
| 操作 | 关键参数 | 描述 |
| --- | --- | --- |
| `add-academic-year` | --name --start-date --end-date --company-id | 创建学年 |
| `update-academic-year` | --year-id [fields] | 更新学年信息 |
| `get-academic-year` | --year-id | 获取学年详情 |
| `list-academic-years` | --company-id | 列出所有学年 |
| `add-academic-term` | --academic-year-id --name --term-type --start-date --end-date --company-id | 创建学期/季度 |
| `update-academic-term` | --term-id [fields] | 更新学期信息 |
| `get-academic-term` | --term-id | 获取学期详情 |
| `list-academic-terms` | --academic-year-id --company-id | 列出所有学期 |
| `add-room` | --room-number --building --capacity --room-type --company-id | 添加教室/实验室 |
| `update-room` | --room-id [fields] | 更新教室信息 |
| `list-rooms` | --room-type --building --company-id | 列出所有教室 |
| `add-program` | --name --program-type --company-id | 创建学位/课程项目 |
| `update-program` | --program-id [fields] | 更新课程项目信息 |
| `get-program` | --program-id | 获取课程项目详情 |
| `list-programs` | --program-type --company-id | 列出所有课程项目 |
| `add-course` | --course-code --name --credit-hours --company-id | 创建课程 |
| `update-course` | --course-id [fields] | 更新课程信息 |
| `get-course` | --course-id | 获取课程详情及先修要求 |
| `list-courses` | --department-id --course-type --company-id | 列出所有课程 |
| `add-section` | --course-id --academic-term-id --section-number --max-enrollment --company-id | 创建课程部分 |
| `update-section` | --section-id [fields] | 更新课程部分信息 |
| `get-section` | --section-id | 获取课程部分的详细信息 |
| `list-sections` | --academic-term-id --course-id --instructor-id --section-status --company-id | 列出所有课程部分 |
| `activate-section` | --section-id | 启用课程部分的注册功能（验证教师和教室可用性） |
| `cancel-section` | --section-id | 取消课程部分的注册（所有已注册的学生将被退学） |

### 注册相关操作
| 操作 | 关键参数 | 描述 |
| --- | --- | --- |
| `create-program-enrollment` | --student-id --program-id --academic-year-id --company-id | 为学生注册课程项目 |
| `cancel-program-enrollment` | --enrollment-id --reason | 退出课程项目 |
| `list-program-enrollments` | --student-id --program-id --company-id | 列出学生的课程注册情况 |
| `create-section-enrollment` | --student-id --section-id --company-id | 为学生注册课程部分（检查先修要求，处理等待名单情况） |
| `cancel-enrollment` | --enrollment-id --drop-reason | 退课（无成绩记录） |
| `terminate-enrollment` | --enrollment-id --reason | 退学（无成绩记录） |
| `get-enrollment` | --enrollment-id | 获取注册详情 |
| `list-enrollments` | --student-id --section-id --enrollment-status --company-id | 列出学生的注册记录 |
| `apply-waitlist` | --section-id | 当有空位时将学生加入等待名单 |
| `list-waitlist` | --section-id --waitlist-status | 列出等待名单上的学生 |

### 成绩评定相关操作
| 操作 | 关键参数 | 描述 |
| --- | --- | --- |
| `add-grading-scale` | --name --entries --company-id | 创建评分标准（A/B/C 等级） |
| `update-grading-scale` | --scale-id [fields] | 更新评分标准 |
| `list-grading-scales` | --company-id | 列出所有评分标准 |
| `get-grading-scale` | --scale-id | 获取评分标准详情 |
| `add-assessment-plan` | --section-id --grading-scale-id --categories --company-id | 创建加权评估计划 |
| `update-assessment-plan` | --plan-id [fields] | 更新评估计划 |
| `get-assessment-plan` | --plan-id | 获取评估计划详情 |
| `add-assessment` | --plan-id --category-id --name --max-points --company-id | 添加评估任务（为已注册学生生成成绩记录） |
| `update-assessment` | --assessment-id [fields] | 更新评估任务 |
| `list-assessments` | --plan-id --section-id --company-id | 列出所有评估任务 |
| `record-assessment-result` | --assessment-id --student-id --points-earned | 为特定学生记录成绩 |
| `record-batch-results` | --assessment-id --results | 批量记录成绩（以 JSON 数组形式） |
| `generate-section-grade` | --section-id --student-id | 计算当前部分的加权成绩 |
| `submit-grades` | --section-id --submitted-by | 提交最终成绩（提交后成绩不可更改） |
| `update-grade` | --enrollment-id --new-letter-grade --new-grade-points --reason --amended-by | 修改已提交的成绩（生成修改记录） |
| `generate-gpa` | --student-id | 重新计算累计平均绩点（GPA） |
| `generate-transcript` | --student-id | 生成包含各学期平均绩点的完整成绩单（记录 FERPA 相关信息） |
| `generate-report-card` | --student-id --academic-term-id | 生成学期成绩单 |
| `list-grades` | --student-id --section-id --academic-term-id | 列出学生的各学期成绩 |

### 出勤相关操作
| 操作 | 关键参数 | 描述 |
| --- | --- | --- |
| `record-attendance` | --student-id --attendance-date --attendance-status --company-id | 为特定学生记录出勤情况 |
| `record-batch-attendance` | --attendance-date --records --company-id | 批量记录出勤情况（以 JSON 数组形式） |
| `update-attendance` | --attendance-id --attendance-status | 修改出勤记录 |
| `get-attendance` | --attendance-id | 获取单次出勤记录 |
| `list-attendance` | --student-id --section-id --attendance-date-from --attendance-date-to --company-id | 列出学生的出勤记录 |
| `get-attendance-summary` | --student-id [--section-id --attendance-date-from --attendance-date-to] | 按学生统计出勤率 |
| `get-section-attendance` | --section-id [--attendance-date] | 获取特定课程部分的出勤情况 |
| `get-truancy-report` | --company-id [--threshold --grade-level] | 显示出勤率低于阈值的学生的名单 |

### 教职员工相关操作
| 操作 | 关键参数 | 描述 |
| --- | --- | --- |
| `add-instructor` | --employee-id --company-id | 将人力资源员工注册为教师 |
| `update-instructor` | --instructor-id [fields] | 更新教师信息 |
| `get-instructor` | --instructor-id | 获取教师的详细信息及所负责的课程部分 |
| `list-instructors` | --department-id --is-active --company-id | 列出所有教师 |
| `get-teaching-load` | --instructor-id --academic-term-id | 显示教师的授课负荷与最大工作小时数 |

### 费用相关操作
| 操作 | 关键参数 | 描述 |
| --- | --- | --- |
| `add-fee-category` | --name --code --company-id | 创建费用类别（如学费、实验室费用等） |
| `update-fee-category` | --fee-category-id [fields] | 更新费用类别信息 |
| `list-fee-categories` | --company-id | 列出所有费用类别 |
| `add-fee-structure` | --name --program-id --academic-term-id --items --company-id | 创建包含具体项目的费用结构 |
| `update-fee-structure` | --structure-id [fields] | 更新费用结构 |
| `get-fee-structure` | --structure-id | 获取费用结构详情 |
| `list-fee-structures` | --program-id --academic-term-id --company-id | 列出所有费用结构 |
| `add-scholarship` | --student-id --name --discount-type --discount-amount --company-id | 发放奖学金或折扣 |
| `update-scholarship` | --scholarship-id [fields] | 更新奖学金信息 |
| `list-scholarships` | --student-id --scholarship-status --company-id | 列出所有奖学金信息 |
| `generate-fee-invoice` | --student-id --program-id --academic-term-id --company-id | 生成学费发票（应用奖学金减免） |
| `list-fee-invoices` | --student-id --company-id | 列出学生的所有发票信息 |
| `get-student-account` | --student-id --company-id | 查看学生的账户信息（包括发票和余额） |
| `get-outstanding-fees` | --company-id [--due-date-to] | 列出所有逾期未付费用的学生的名单 |
| `apply-late-fee` | --student-id --fee-category-id --amount --company-id | 对学生收取滞纳金 |

### 沟通相关操作
| 操作 | 关键参数 | 描述 |
| --- | --- | --- |
| `add-announcement` | --title --body --company-id [--priority --audience-type --audience-filter] | 创建公告（草稿状态） |
| `update-announcement` | --announcement-id [fields] | 更新公告内容 |
| `submit-announcement` | --announcement-id [--published-by] | 发布公告并向指定受众发送通知 |
| `list-announcements` | --announcement-status --audience-type --company-id | 列出所有公告 |
| `get-announcement` | --announcement-id | 获取公告内容及通知发送数量 |
| `submit-notification` | --recipient-type --recipient-id --notification-type --title --message --company-id | 向指定接收者发送通知 |
| `list-notifications` | --recipient-id --recipient-type --is-read --company-id | 列出所有已发送的通知 |
| `generate-progress-report` | --student-id --academic-term-id --company-id | 向学生和监护人发送中期报告 |
| `submit-emergency-alert` | --title --message --company-id | 向所有接收者发送紧急警报 |

## 高级功能（高级级别）

- **FERPA 合规性**：每次执行 `get-student` 操作时，系统都会自动记录 FERPA 访问日志。如需手动记录访问日志，请参考：```
--action record-data-access --student-id {id} --data-category grades --access-type view --access-reason "Parent conference" --user-id {user_id}
```
- **等待名单管理**：请参考：```
# Section full → student goes to waitlist automatically on create-section-enrollment
--action create-section-enrollment --student-id {id} --section-id {full_section_id} --company-id {id}
# → returns waitlist_status: waitlisted

# When a student drops, advance the waitlist:
--action apply-waitlist --section-id {id}
# → offers seat to next student (48-hour window), sends notification
```
- **成绩修改**：请参考：```
# After submit-grades (immutable), use update-grade:
--action update-grade --enrollment-id {id} --new-letter-grade B --new-grade-points 3.0 --reason "Data entry error" --amended-by {user_id}
# Creates amendment record + triggers GPA recalculation
```
- **紧急警报**：请参考：```
# Broadcasts to ALL students + guardians + staff in company:
--action submit-emergency-alert --title "School Closure" --message "School closed due to weather." --company-id {id} --sent-by {user_id}
```
- **批量操作**：请参考：```
# Batch attendance for entire class:
--action record-batch-attendance --attendance-date 2025-09-15 --section-id {id} --company-id {id} \
  --records '[{"student_id":"{id1}","attendance_status":"present"},{"student_id":"{id2}","attendance_status":"absent"}]'

# Batch grade entry:
--action record-batch-results --assessment-id {id} \
  --results '[{"student_id":"{id1}","points_earned":92},{"student_id":"{id2}","points_earned":78}]'
```