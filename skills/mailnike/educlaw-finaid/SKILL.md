---
name: educlaw-finaid
display_name: EduClaw Financial Aid
version: 1.0.0
description: 联邦、州及机构的财政援助管理，确保符合《Title IV》法规要求。包括ISIR处理、SAP评估、R2T4计算、奖学金发放、款项拨付、发票生成、勤工俭学项目以及贷款跟踪等流程。
author: ERPForge
parent: educlaw
requires: [erpclaw, erpclaw-people, educlaw]
database: ~/.openclaw/erpclaw/data.sqlite
user-invocable: true
scripts:
  - scripts/db_query.py
domains:
  - financial_aid
  - scholarships
  - work_study
  - loan_tracking
total_actions: 116
tables:
  - finaid_aid_year
  - finaid_pell_schedule
  - finaid_fund_allocation
  - finaid_cost_of_attendance
  - finaid_isir
  - finaid_isir_cflag
  - finaid_verification_request
  - finaid_verification_document
  - finaid_award_package
  - finaid_award
  - finaid_disbursement
  - finaid_sap_evaluation
  - finaid_sap_appeal
  - finaid_r2t4_calculation
  - finaid_professional_judgment
  - finaid_scholarship_program
  - finaid_scholarship_application
  - finaid_scholarship_renewal
  - finaid_work_study_job
  - finaid_work_study_assignment
  - finaid_work_study_timesheet
  - finaid_loan
metadata: {"openclaw":{"type":"executable","install":{"post":"python3 init_db.py && python3 scripts/db_query.py --action status"},"requires":{"bins":["python3"],"env":[],"optionalEnv":[]},"os":["darwin","linux"]}}
---
# EduClaw 财务援助系统

该系统负责管理联邦、州及院校层面的财务援助，涵盖了 Title IV 财务援助的整个生命周期，包括数据导入（ISIR）、资金分配、SAP 评估、R2T4 计算、专业判断、奖学金发放、勤工俭学项目以及贷款跟踪等流程。

## 安全模型

- **仅限本地存储**：所有数据均保存在 `~/.openclaw/erpclaw/data.sqlite` 文件中。
- **完全离线运行**：不依赖任何外部 API、遥测服务或云服务。
- **无需用户名和密码**：系统使用 `erpclaw_lib` 共享库（由 erpclaw 工具安装）。
- **防止 SQL 注入**：所有查询均采用参数化语句。
- **符合 FERPA 法规**：系统会记录学生对财务数据的访问记录。
- **遵守 Title IV 法规**：所有与财务援助相关的操作（如 ISIR、SAP、R2T4 和 COD 处理）均严格遵循联邦法规。相关记录会本地生成以便后续导出。

## 快速入门

```bash
# 1. Set up aid year
python3 db_query.py --action add-aid-year \
  --aid-year-code "2025-2026" --start-date 2025-07-01 --end-date 2026-06-30 \
  --pell-max-award 7395 --company-id <id>
python3 db_query.py --action import-pell-schedule --aid-year-id <id> --rows '<json>'

# 2. Import ISIR and create award package
python3 db_query.py --action import-isir --student-id <id> --aid-year-id <id> \
  --transaction-number 1 --receipt-date 2025-02-15 --sai -1500
python3 db_query.py --action create-award-package --student-id <id> \
  --aid-year-id <id> --isir-id <id> --cost-of-attendance-id <id>

# 3. Add awards and disburse
python3 db_query.py --action add-award --award-package-id <id> \
  --aid-type grant --aid-source federal --offered-amount 7395
python3 db_query.py --action submit-award-offer --id <id>
python3 db_query.py --action record-award-disbursement --award-id <id> --amount 3697.50
```

## 第一层 — 日常操作

### 财务援助年度与资金设置
| 操作 | 描述 |
|--------|-------------|
| `add-aid-year` | 创建一个新的财务援助年度，并设置佩尔奖学金（Pell Scholarship）的最高金额。 |
| `update-aid-year` | 更新财务援助年度的日期和参数设置。 |
| `activate-aid-year` | 激活该财务援助年度，准备进行后续处理。 |
| `get-aid-year` | 获取该财务援助年度的详细信息。 |
| `list-aid-years` | 列出所有已创建的财务援助年度。 |
| `import-pell-schedule` | 导入佩尔奖学金的发放计划。 |
| `list-pell-schedule` | 显示佩尔奖学金发放计划的详细信息。 |
| `add-fund-allocation` | 创建资金分配记录（包括佩尔奖学金、SEOG 等）。 |
| `update-fund-allocation` | 更新资金分配金额。 |
| `get-fund-allocation` | 获取资金分配的详细信息。 |
| `list-fund-allocations` | 查看该财务援助年度的所有资金分配记录。 |

### 出席费用（Cost of Attendance, COA）
| 操作 | 描述 |
|--------|-------------|
| `add-cost-of-attendance` | 根据学生的注册情况和生活状态定义出席费用。 |
| `update-cost-of-attendance` | 更新出席费用的构成。 |
| `delete-cost-of-attendance` | 删除出席费用记录。 |
| `get-cost-of-attendance` | 获取出席费用的详细信息。 |
| `list-cost-of-attendance` | 列出该财务援助年度的所有出席费用记录。 |

### ISIR 数据处理
| 操作 | 描述 |
|--------|-------------|
| `import-isir` | 导入包含学生信息（SAI）、依赖关系（dependency）和 C-flags 的 ISIR 数据。 |
| `complete-isir-review` | 标记 ISIR 数据已审核完毕。 |
| `update-isir` | 根据修改后的信息更新 ISIR 数据。 |
| `get-isir` | 获取 ISIR 数据的详细信息。 |
| `list-isirs` | 列出该学生在该财务援助年度的所有 ISIR 数据记录。 |
| `add-isir-cflag` | 为 ISIR 数据添加 C-flags（用于特殊说明）。 |
| `complete-isir-cflag` | 处理相关的 C-flags 问题。 |
| `list-isir-cflags` | 查看该 ISIR 数据的所有 C-flags。 |

## 第二层 — 奖学金发放与验证

### 验证流程
| 操作 | 描述 |
|--------|-------------|
| `create-verification-request` | 创建包含所需文件的验证请求。 |
| `add-verification-document` | 向验证请求中添加相关文件。 |
| `update-verification-document` | 更新文件的提交状态。 |
| `update-verification-request` | 更新整个验证请求的详细信息。 |
| `complete-verification` | 标记验证流程已完成。 |
| `get-verification-request` | 获取验证请求的详细信息。 |
| `list-verification-requests` | 列出所有待处理的验证请求。 |
| `list-verification-documents` | 查看每个验证请求所关联的所有文件。 |

### 奖学金发放与确认
| 操作 | 描述 |
|--------|-------------|
| `create-award-package` | 为学生创建奖学金发放包。 |
| `update-award-package` | 更新奖学金发放包的详细信息。 |
| `submit-award-offer` | 将奖学金发放包发送给学生。 |
| `cancel-award-package` | 取消奖学金发放包的发送。 |
| `get-award-package` | 获取包含所有奖学金信息的发放包。 |
| `list-award-packages` | 查看该学生在该财务援助年度的所有奖学金发放包。 |
| `add-award` | 向发放包中添加具体的奖学金项目。 |
| `update-award` | 更新奖学金的金额。 |
| `accept-award` | 学生接受奖学金。 |
| `deny-award` | 学生拒绝奖学金。 |
| `delete-award` | 删除未批准的奖学金记录。 |
| `get-award` | 获取奖学金的详细信息。 |
| `list-awards` | 列出该学生在该财务援助年度获得的所有奖学金。 |

### 资金发放
| 操作 | 描述 |
|--------|-------------|
| `record-award-disbursement` | 为奖学金发放相应的资金。 |
| `cancel-disbursement` | 取消已发放的资金。 |
| `record-credit-balance-return` | 记录退还给学生的剩余金额。 |
| `get-disbursement` | 获取资金发放的详细信息。 |
| `list-disbursements` | 查看该学生在该财务援助年度的所有资金发放记录。 |

## 第三层 — SAP、R2T4、COD 与专业判断

### SAP 评估（SAP Evaluation）
| 操作 | 描述 |
|--------|-------------|
| `generate-sap-evaluation` | 对学生的学术表现进行 SAP 评估。 |
| `generate-sap-batch` | 批量处理学生的 SAP 评估结果。 |
| `apply-sap-override` | 修改 SAP 评估结果。 |
| `get-sap-evaluation` | 获取 SAP 评估的详细信息。 |
| `list-sap-evaluations` | 查看所有学生的 SAP 评估结果。 |
| `submit-sap-appeal` | 提交针对 SAP 评估结果的申诉。 |
| `complete-sap-appeal` | 审批或拒绝申诉。 |
| `update-sap-appeal` | 更新申诉的详细信息。 |
| `get-sap-appeal` | 获取申诉的详细信息。 |
| `list-sap-appeals` | 查看所有学生的申诉记录。 |

### R2T4 计算（Return of Title IV）
| 操作 | 描述 |
|--------|-------------|
| `create-r2t4` | 为退学的学生生成 R2T4 计算结果。 |
| `generate-r2t4-calculation` | 执行 R2T4 计算。 |
| `approve-r2t4` | 审批 R2T4 计算结果。 |
| `record-r2t4-return` | 记录学生的退款情况。 |
| `record-r2t4-return-disbursement` | 记录退款的详细信息。 |
| `get-r2t4` | 获取 R2T4 计算的详细结果。 |
| `list-r2t4s` | 查看所有学生的 R2T4 计算结果。 |

### COD 处理（Common Origination & Disbursement）
| 操作 | 描述 |
|--------|-------------|
| `generate-cod-origination` | 生成 COD（Common Origination Document）记录。 |
| `update-cod-origination-status` | 更新 COD 的生成状态。 |
| `generate-cod-export` | 批量生成 COD 文件。 |
| `update-cod-status` | 更新 COD 的响应状态。 |

### 专业判断（Professional Judgment）
| 操作 | 描述 |
|--------|-------------|
| `add-professional-judgment` | 创建包含相关文件的专业判断请求。 |
| `approve-professional-judgment` | 经过主管审核后批准专业判断结果。 |
| `get-professional-judgment` | 获取专业判断的详细信息。 |
| `list-professional-judgments` | 查看所有专业判断请求的详细信息。 |

### 奖学金项目管理
| 操作 | 描述 |
|--------|-------------|
| `add-scholarship-program` | 创建新的奖学金项目。 |
| `update-scholarship-program` | 更新奖学金项目的申请条件。 |
| `terminate-scholarship-program` | 取消奖学金项目的运行。 |
| `get-scholarship-program` | 获取奖学金项目的详细信息。 |
| `list-scholarship-programs` | 查看所有奖学金项目的列表。 |
| `submit-scholarship-application` | 提交学生的奖学金申请。 |
| `complete-scholarship-review` | 审核申请。 |
| `approve-scholarship-application` | 向申请者发放奖学金。 |
| `deny-scholarship-application` | 拒绝申请。 |
| `update-scholarship-application` | 更新申请信息。 |
| `get-scholarship-application` | 获取申请的详细信息。 |
| `list-scholarship-applications` | 查看所有奖学金申请记录。 |
| `generate-scholarship-renewal` | 评估奖学金的续期资格。 |
| `list-scholarship-renewals` | 查看所有奖学金的续期申请情况。 |
| `generate-scholarship-matches` | 自动匹配符合条件的学生和奖学金项目。 |

### 勤工俭学管理
| 操作 | 描述 |
|--------|-------------|
| `add-work-study-job` | 创建勤工俭学职位。 |
| `update-work-study-job` | 更新职位的详细信息。 |
| `terminate-work-study-job` | 取消勤工俭学职位。 |
| `get-work-study-job` | 获取勤工俭学职位的详细信息。 |
| `list-work-study-jobs` | 查看所有勤工俭学职位的列表。 |
| `assign-student-to-job` | 为学生分配勤工俭学职位。 |
| `update-work-study-assignment` | 更新学生的勤工俭学任务信息。 |
| `terminate-work-study-assignment` | 结束学生的勤工俭学任务。 |
| `get-work-study-assignment` | 获取勤工俭学任务的详细信息。 |
| `list-work-study-assignments` | 查看所有学生的勤工俭学任务记录。 |
| `submit-work-study-timesheet` | 提交勤工俭学的工作时间表。 |
| `approve-work-study-timesheet` | 批准工作时间表。 |
| `deny-work-study-timesheet` | 拒绝工作时间表。 |
| `update-work-study-timesheet` | 更新工作时间表。 |
| `get-work-study-timesheet` | 获取工作时间表的详细信息。 |
| `list-work-study-timesheets` | 查看所有学生的工作时间表记录。 |
| `get-work-study-earnings-summary` | 获取学生的勤工俭学收入汇总。 |
| `generate-payroll-export` | 导出学生的工资单数据。 |

### 贷款跟踪
| 操作 | 描述 |
|--------|-------------|
| `add-loan` | 跟踪学生的贷款信息。 |
| `update-loan` | 更新贷款的详细信息。 |
| `get-loan` | 获取贷款的详细信息。 |
| `list-loans` | 查看学生的所有贷款记录。 |
| `get-loan-limits-status` | 检查学生的贷款总额限制。 |
| `update-mpn-status` | 更新学生的 MPN（MyPersonNumber）状态。 |
| `update-entrance-counseling` | 更新学生的入学咨询信息。 |
| `update-exit-counseling` | 更新学生的毕业咨询信息。 |
| `generate-cod-origination` | 生成贷款的 COD（Common Origination Document）。 |
| `update-cod-origination-status` | 更新贷款的生成状态。 |

## 合规性要求

- **Title IV**：所有操作严格遵循从 ISIR 数据导入到资金发放、SAP 评估、R2T4 计算直至最终发放的完整生命周期流程。
- **FAFSA**：基于 SAI 数据计算佩尔奖学金金额，并处理相关的 C-flags（特殊说明）。
- **SAP**：采用定量和定性的评估方法，并提供申诉流程。
- **R2T4**：遵守 34 CFR 668.22 规定，进行基于百分比的奖学金计算。
- **COD**：负责生成贷款的原始记录和发放相关文件。
- **FERPA**：系统会记录学生对财务数据的访问情况，确保符合 FERPA 法规要求。