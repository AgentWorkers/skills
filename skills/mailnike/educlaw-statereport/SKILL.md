---
name: educlaw-statereport
version: 1.0.0
description: >
  **EduClaw 州级报告功能**  
  EduClaw 提供了针对 K-12 学区（LEAs）的州级报告功能，包括与 Ed-Fi 的集成、数据验证以及提交流程的跟踪。该系统能够将 EduClaw 中收集到的运营数据转换为符合州/联邦要求的报告格式（如 Ed-Fi ODS/API、EDFacts、CRDC、IDEA 618 等）。
author: ERPForge
scripts:
  - scripts/db_query.py
parent: educlaw
requires: [erpclaw, educlaw]
database: ~/.openclaw/erpclaw/data.sqlite
user-invocable: true
table_prefix: sr_
domains:
  - demographics
  - discipline
  - ed_fi
  - state_reporting
  - data_validation
  - submission_tracking
total_actions: 98
metadata: {"openclaw":{"type":"executable","install":{"post":"python3 init_db.py && python3 scripts/db_query.py --action status"},"requires":{"bins":["python3"],"env":[],"optionalEnv":[]},"os":["darwin","linux"]}}
---
# EduClaw状态报告系统

该系统支持K-12地方教育机构（LEAs）的状态报告、Ed-Fi API集成、数据验证以及提交跟踪功能。

## 安全模型

- **仅限本地数据**：所有记录存储在`~/.openclaw/erpclaw/data.sqlite`文件中。
- **默认情况下完全离线**：在数据录入、验证、快照生成或提交跟踪过程中不进行任何网络操作。
- **核心操作无需凭证**：系统使用`erpclaw_lib`共享库（由`erpclaw`安装）。
- **防止SQL注入**：所有查询均使用参数化语句。
- **Ed-Fi同步为可选**：`submit-*-to-edfi`和`get-edfi-connection-test`操作仅在明确调用时才会向配置的ODS端点发起HTTPS请求，这是唯一的外部网络活动来源。
- **凭证保护**：OAuth客户端密钥在插入数据库前会被加密；解密后的凭证不会出现在操作输出、日志或错误信息中。

## 快速参考

### 第一层——日常操作

| 操作          | 描述                                      |
|-----------------|---------------------------------------------|
| `add-student-supplement` | 为学生创建状态报告补充信息（包括种族、SSID、特殊教育标志等）       |
| `assign-ssid`     | 记录分配给学生的SSID，并设置`ssid_status`为“assigned”       |
| `update-student-race`    | 设置学生的种族/族裔信息，并根据OMB规则自动计算联邦汇总数据   |
| `update-el-status`    | 更新学生的特殊教育相关标志（如`is_el`、`el_entry_date`、`home_language_code`） |
| `update-sped-status`    | 更新学生的特殊教育相关标志（如`is_sped`、`is_504`、`sped_entry_date`） |
| `add-discipline-incident` | 创建纪律事件（命名格式为INC-YYYY-NNNNN）             |
| `add-discipline-student` | 将学生关联到纪律事件，并自动填充IDEA/504相关标志       |
| `add-discipline-action` | 添加纪律处分记录，并为IDEA学生自动设置`mdr_required`字段   |
| `apply-validation`    | 对指定时间段内的所有数据执行验证规则                |
| `list-submission-errors` | 按错误类型、严重程度和类别列出未解决的错误         |
| `update-error-resolution` | 标记错误为已解决或延迟解决，并记录处理方法及备注     |

### 第二层——数据收集窗口管理

| 操作          | 描述                                      |
|-----------------|---------------------------------------------|
| `add-collection-window` | 定义一个新的状态报告数据收集窗口                 |
| `apply-window-status` | 将数据收集窗口的状态从“即将开始”更改为“开放中”等         |
| `create-snapshot`     | 冻结数据，生成快照及快照记录                   |
| `add-submission`     | 记录提交尝试（包括初次提交和修改）                    |
| `approve-submission` | 确认数据准确性，并原子性地更新提交记录、快照及窗口状态     |
| `create-amendment`     | 创建与原始记录关联的修改记录，并重新启动数据收集窗口       |
| `get-error-dashboard` | 按错误类型、严重程度和解决状态统计错误数量             |
| `assign-errors`     | 一次性将多个错误分配给相关工作人员                 |
| `generate-ada`     | 计算指定时间段内的ADA/ADM指标                 |
| `get-ada-dashboard` | 提供包含资金影响的ADA指标统计结果             |
| `list-chronic-absenteeism` | 标记缺勤天数超过10%的学生                 |

### 第三层——Ed-Fi集成与报告

| 操作          | 描述                                      |
|-----------------|---------------------------------------------|
| `add-edfi-config` | 创建Ed-Fi ODS连接配置文件，并加密OAuth密钥              |
| `get-edfi-connection-test` | 测试OAuth与ODS的连接状态，并记录最后一次测试时间         |
| `add-org-mapping` | 将地方教育机构/学校映射到NCES和Ed-Fi标识符          |
| `import-descriptor-mappings` | 上传多个代码到URI描述符的映射关系             |
| `submit-student-to-edfi` | 将学生信息及组织关联信息推送到Ed-Fi系统         |
| `submit-enrollment-to-edfi` | 将学生入学信息推送到Ed-Fi系统                 |
| `submit-attendance-to-edfi` | 将学生出勤信息推送到Ed-Fi系统                 |
| `submit-sped-to-edfi` | 将学生特殊教育计划信息推送到Ed-Fi系统                 |
| `submit-el-to-edfi` | 将学生语言教学计划信息推送到Ed-Fi系统                 |
| `submit-discipline-to-edfi` | 将纪律事件信息推送到Ed-Fi系统                 |
| `submit-staff-to-edfi` | 将员工信息及组织关联信息推送到Ed-Fi系统                 |
| `submit-failed-syncs` | 重新排队所有失败的同步请求                     |
| `import-validation-rules` | 加载57条内置的联邦验证规则                 |
| `generate-enrollment-report` | 按种族/年级/子群体统计入学人数                 |
| `generate-crdc-report` | 生成按种族/性别/残疾状况分类的CRDC格式报告         |
| `get-data-readiness-report` | 提供各类别的数据完整性评分（0-100分）                 |

## 所有操作索引

以下是6个领域内共98个操作的完整索引。所有操作名称均遵循ClawHub的命名规范。

| 操作          | 领域            | 描述                                      |
|-----------------|-----------------------------|
| `add-student-supplement` | 人口统计          | 为学生创建状态报告补充信息                         |
| `update-student-supplement` | 人口统计          | 更新补充信息字段，并重新计算联邦汇总数据                 |
| `get-student-supplement` | 人口统计          | 根据学生ID或补充信息ID获取相关数据                   |
| `list-student-supplements` | 人口统计          | 按条件筛选并列出所有补充信息                     |
| `assign-ssid`     | 人口统计          | 记录分配给学生的SSID                         |
| `update-student-race`    | 人口统计          | 设置学生的种族/族裔信息，并自动计算联邦汇总数据             |
| `update-el-status`    | 人口统计          | 更新学生的特殊教育相关标志                     |
| `update-sped-status`    | 人口统计          | 更新学生的特殊教育相关标志                     |
| `update-economic-status` | 人口统计          | 更新学生的经济劣势相关标志                     |
| `add-sped-placement` | 人口统计          | 为特殊教育学生添加安置记录                     |
| `update-sped-placement` | 人口统计          | 更新特殊教育学生的安置信息                     |
| `get-sped-placement` | 人口统计          | 根据学生ID和学年获取特殊教育学生的安置信息             |
| `list-sped-placements` | 人口统计          | 按条件筛选并列出特殊教育学生的安置情况                 |
| `add-sped-service` | 人口统计          | 为特殊教育学生的安置添加相关服务                     |
| `update-sped-service` | 人口统计          | 更新特殊教育服务的详细信息                     |
| `list-sped-services` | 人口统计          | 列出所有特殊教育服务                         |
| `delete-sped-service` | 人口统计          | 删除特殊教育服务的记录                     |
| `add-el-program` | 人口统计          | 记录学生的特殊教育项目参与情况                     |
| `update-el-program` | 人口统计          | 更新特殊教育项目的详细信息                     |
| `get-el-program` | 人口统计          | 根据学生ID获取特殊教育项目的详细信息                 |
| `list-el-programs` | 人口统计          | 按条件筛选并列出特殊教育项目                     |
| `add-discipline-incident` | 纪律管理          | 创建纪律事件记录                         |
| `update-discipline-incident` | 纪律管理          | 更新纪律事件的相关信息                     |
| `get-discipline-incident` | 纪律管理          | 获取包含学生信息的纪律事件记录                     |
| `list-discipline-incidents` | 纪律管理          | 按条件筛选并列出所有纪律事件                     |
| `delete-discipline-incident` | 纪律管理          | 仅删除未关联学生的纪律事件                     |
| `add-discipline-student` | 纪律管理          | 将学生关联到纪律事件                         |
| `update-discipline-student` | 纪律管理          | 更新学生的角色或IDEA/504相关标志                   |
| `delete-discipline-student` | 纪律管理          | 从纪律事件中移除学生                         |
| `list-discipline-students` | 纪律管理          | 列出与特定纪律事件相关的所有学生                     |
| `add-discipline-action` | 纪律管理          | 添加纪律处分记录                         |
| `update-discipline-action` | 纪律管理          | 更新纪律处分的详细信息，包括MDR结果                 |
| `record-mdr-outcome` | 纪律管理          | 记录纪律处分的结果                         |
| `get-discipline-action` | 纪律管理          | 获取特定的纪律处分记录                     |
| `list-discipline-actions` | 纪律管理          | 按条件筛选并列出所有纪律处分记录                     |
| `get-discipline-summary` | 纪律管理          | 提供CRDC格式的纪律管理总结报告                 |
| `add-edfi-config` | Ed-Fi集成          | 创建Ed-Fi ODS连接配置文件                     |
| `update-edfi-config` | Ed-Fi集成          | 更新ODS连接URL和OAuth凭证                     |
| `get-edfi-config` | Ed-Fi集成          | 获取Ed-Fi配置信息（不包含解密后的密钥）                 |
| `list-edfi-configs` | Ed-Fi集成          | 按条件筛选并列出所有配置文件                     |
| `get-edfi-connection-test` | Ed-Fi集成          | 测试OAuth令牌的获取情况，并记录最后一次测试时间             |
| `add-org-mapping` | Ed-Fi集成          | 将地方教育机构/学校映射到NCES和Ed-Fi标识符             |
| `update-org-mapping` | Ed-Fi集成          | 更新NCES/Ed-Fi标识符                         |
| `get-org-mapping` | Ed-Fi集成          | 获取组织映射关系                         |
| `list-org-mappings` | Ed-Fi集成          | 列出公司的所有组织映射关系                     |
| `add-descriptor-mapping` | Ed-Fi集成          | 添加代码到Ed-Fi描述符的映射关系                 |
| `update-descriptor-mapping` | Ed-Fi集成          | 更新描述符的URI映射关系                     |
| `import-descriptor-mappings` | Ed-Fi集成          | 从JSON数组上传多个描述符映射关系                 |
| `list-descriptor-mappings` | Ed-Fi集成          | 按条件筛选并列出所有描述符映射关系                     |
| `delete-descriptor-mapping` | Ed-Fi集成          | 删除特定的描述符映射关系                     |
| `submit-student-to-edfi` | Ed-Fi集成          | 将学生信息及组织关联信息推送到Ed-Fi系统                 |
| `submit-enrollment-to-edfi` | Ed-Fi集成          | 将学生入学信息推送到Ed-Fi系统                 |
| `submit-attendance-to-edfi` | Ed-Fi集成          | 将学生出勤信息推送到Ed-Fi系统                 |
| `submit-sped-to-edfi` | Ed-Fi集成          | 将学生特殊教育计划信息推送到Ed-Fi系统                 |
| `submit-el-to-edfi` | Ed-Fi集成          | 将学生语言教学计划信息推送到Ed-Fi系统                 |
| `submit-discipline-to-edfi` | Ed-Fi集成          | 将纪律事件信息推送到Ed-Fi系统                 |
| `submit-staff-to-edfi` | Ed-Fi集成          | 将员工信息及组织关联信息推送到Ed-Fi系统                 |
| `get-edfi-sync-log` | Ed-Fi集成          | 获取同步日志记录                         |
| `list-edfi-sync-errors` | Ed-Fi集成          | 列出所有失败的或待处理的同步请求                 |
| `submit-failed-syncs` | Ed-Fi集成          | 重新尝试所有失败的同步请求                     |
| `add-collection-window` | 状态报告          | 定义一个新的数据收集窗口                         |
| `update-collection-window` | 状态报告          | 更新窗口的日期和配置信息                     |
| `get-collection-window` | 状态报告          | 获取包含错误统计和快照摘要的窗口信息                 |
| `list-collection-windows` | 状态报告          | 按条件筛选并列出所有数据收集窗口                     |
| `apply-window-status` | 状态报告          | 将窗口状态从“即将开始”更改为“开放中”等                 |
| `create-snapshot` | 状态报告          | 冻结数据并生成快照                         |
| `get-snapshot` | 状态报告          | 获取快照的摘要信息                         |
| `list-snapshot-records` | 状态报告          | 获取学生级别的快照记录                     |
| `generate-ada` | 状态报告          | 计算ADA/ADM指标                         |
| `get-ada-dashboard` | 状态报告          | 提供包含趋势和资金影响的ADA指标统计结果                 |
| `list-chronic-absenteeism` | 状态报告          | 标记缺勤天数超过10%的学生                     |
| `get-data-readiness-report` | 状态报告          | 提供各类别的数据完整性评分（0-100分）                 |
| `generate-enrollment-report` | 状态报告          | 按种族/年级/子群体统计入学人数                 |
| `generate-crdc-report` | 状态报告          | 生成按种族/性别/残疾状况分类的CRDC格式报告                 |
| `add-validation-rule` | 数据验证          | 向系统中添加新的验证规则                     |
| `update-validation-rule` | 数据验证          | 更新规则的SQL语句、消息模板或元数据                 |
| `get-validation-rule` | 数据验证          | 根据ID或代码获取规则                     |
| `list-validation-rules` | 数据验证          | 按条件筛选并列出所有规则                     |
| `update-validation-rule-status` | 数据验证          | 激活或停用规则                         |
| `import-validation-rules` | 数据验证          | 加载57条内置的联邦验证规则                 |
| `apply-validation` | 数据验证          | 对指定时间段内的所有数据执行验证规则                 |
| `apply-student-validation` | 数据验证          | 对单个学生执行所有验证规则                     |
| `get-validation-results` | 数据验证          | 获取验证结果及详细统计信息                     |
| `assign-submission-error` | 数据验证          | 将错误分配给相关工作人员                     |
| `update-error-resolution` | 数据验证          | 标记错误为已解决或延迟解决                     |
| `list-submission-errors` | 数据验证          | 按错误类型、严重程度和类别列出所有错误                 |
| `get-error-dashboard` | 数据验证          | 按错误类型、严重程度和解决状态统计错误数量                 |
| `assign-errors` | 数据验证          | 一次性将多个错误分配给相关工作人员                 |
| `submit-error-escalation` | 数据验证          | 将错误情况上报给州级帮助台                     |
| `add-submission` | 提交跟踪          | 记录新的提交尝试                         |
| `update-submission-status` | 提交跟踪          | 更新提交记录的状态                     |
| `get-submission` | 提交跟踪          | 获取包含快照和错误统计的提交记录                 |
| `list-submissions` | 提交跟踪          | 按条件筛选并列出所有提交记录                     |
| `approve-submission` | 提交跟踪          | 确认数据准确性，并原子性地更新提交记录、快照                 |
| `create-amendment` | 提交跟踪          | 创建与原始记录关联的修改记录                     |
| `get-submission-history` | 提交跟踪          | 提供完整的提交历史记录                     |
| `generate-submission-package` | 提交跟踪          | 生成包含快照和记录的JSON文件，用于审计用途                 |
| `get-submission-audit-trail` | 提交跟踪          | 提供完整的审计跟踪记录                     |

## 不变量

- **人口统计领域**：每个`educlaw_student`对应唯一的`sr_student_supplement`记录。
- **人口统计领域**：`race_federal_rollup`是根据`is_hispanic_latino`和`race_codes`计算得出的。
- **人口统计领域**：每个学生每学年对应唯一的`sr_sped-placement`记录。
- **纪律管理领域**：IDEA学生且缺勤天数超过10天的情况下，`mdr_required`字段自动设置为1。
- **Ed-Fi领域**：`oauth_client_secret_encrypted`密钥永远不会以明文形式存储。
- **状态报告领域**：如果存在严重的未解决错误，则无法生成快照。
- **状态报告领域**：`sr_snapshot_record`记录仅支持插入操作（不允许更新或删除）。
- **提交跟踪领域**：`approve-submission`操作会原子性地更新提交记录、快照及窗口状态。
- **数据验证领域**：`rule_code`在整个系统中是唯一的。
- **所有领域**：`company_id`字段永远不会为NULL。