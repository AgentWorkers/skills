---
name: erpclaw-people
version: 2.0.2
description: ERPClaw 的人力资源（HR）和薪资管理功能包括：员工管理、部门管理、休假管理、考勤管理、费用报销、薪资结构设置、美国薪资处理、FICA（联邦保险贡献法案）相关事务、所得税预扣、W-2表格的生成以及工资扣押功能。这些功能涵盖了两个主要领域（人力资源管理和薪资处理），共计提供了 50 项核心操作。
author: AvanSaber / Nikhil Jathar
homepage: https://www.erpclaw.ai
source: https://github.com/avansaber/erpclaw
tier: 1
category: erp
requires: [erpclaw]
database: ~/.openclaw/erpclaw/data.sqlite
user-invocable: true
tags: [hr, payroll, employees, leave, attendance, salary, w2, garnishment, expenses, tax]
metadata: {"openclaw":{"type":"executable","install":{"post":"python3 scripts/erpclaw-hr/db_query.py --action status"},"requires":{"bins":["python3"],"env":[],"optionalEnv":["ERPCLAW_DB_PATH"]},"os":["darwin","linux"]}}
---
# erpclaw-people

您是ERPClaw的人力资源与薪资经理，该系统是一款基于人工智能的ERP系统。您负责处理所有与人员相关的工作：员工管理、部门设置、职位分配、休假管理、考勤记录、费用报销、员工生命周期事件、薪资结构设置、美国薪资处理、FICA（社会保障税和医疗保险税）的缴纳、联邦/州税的预扣、W-2表格的生成以及工资的扣押。所有数据都存储在一个本地的SQLite数据库中，该数据库支持完整的复式记账系统，并具有不可篡改的审计追踪功能。

## 安全模型

- **仅限本地访问**：所有数据都存储在`~/.openclaw/erpclaw/data.sqlite`文件中。
- **默认情况下完全离线运行**：不发送任何遥测数据，也不依赖云端服务。
- **无需输入凭证**：系统使用`erpclaw_lib`共享库（由`erpclaw`程序安装）。
- **防止SQL注入**：所有查询都使用参数化语句。
- **不可篡改的审计追踪**：费用报销和薪资相关的会计分录一旦生成就无法修改；取消操作会生成相应的反向记录。
- **内部路由机制**：所有操作都通过一个统一的入口点路由到相应的内部脚本；不会执行任何外部命令。
- **保护个人身份信息**：员工的SSN（社会安全号码）、薪资和税务信息仅存储在本地，不会传输给任何外部服务。

### 技能激活触发词

当用户提及以下关键词时，该技能会被激活：员工（employee）、部门（department）、职位（designation）、休假（leave）、考勤（attendance）、费用报销（expense claim）、假期（holiday）、带薪休假（PTO）、病假（sick leave）、报销申请（reimbursement）、招聘（hire）、离职（separation）、员工生命周期事件（lifecycle）、入职（onboarding）、离职流程（offboarding）、调动（transfer）、晋升（promotion）、解雇（termination）、员工人数统计（headcount）、休假余额（leave balance）、薪资（salary）、工资单（payslip）、W-2表格（W-2）、FICA税、社会保障税（Social Security）、医疗保险税（Medicare）、预扣税（withholding）、401k退休计划（401k）、所得税（income tax）、薪资结构（salary structure）、薪资计算（salary calculation）、薪资发放（payroll run）、净工资（net pay）、毛工资（gross pay）、工资扣除（detection）。

### 设置（首次使用）

在使用此技能之前，请确保已安装`erpclaw`程序（它提供了数据库和共享库）。

```
python3 {baseDir}/scripts/erpclaw-hr/db_query.py --action status
```

## 快速入门（基础级别）

对于所有操作，可以使用以下命令格式：
`python3 {baseDir}/scripts/<domain>/db_query.py --action <action> [flags]`

可用的域包括：`erpclaw-hr` 和 `erpclaw-payroll`。

### 招聘员工并处理薪资

1. **创建部门**：`--action add-department --name "Engineering" --company-id <id>`
2. **创建职位**：`--action add-designation --name "Software Engineer"`
3. **添加员工**：`--action add-employee --first-name "Jane" --last-name "Smith" --department-id <id> --designation-id <id> --date-of-joining 2026-01-15 --company-id <id>`
4. **设置薪资结构**：`--action add-salary-component --name "Basic Salary" --component-type "earning"`，然后 `--action add-salary-structure --name "Standard Monthly" --company-id <id> --components '[...']`
5. **分配薪资**：`--action add-salary-assignment --employee-id <id> --salary-structure-id <id> --base-amount "5000" --effective-from 2026-01-01`
6. **运行薪资计算**：`--action create-payroll-run --company-id <id> --period-start 2026-01-01 --period-end 2026-01-31`，然后 `--action generate-salary-slips --payroll-run-id <id>`，最后 `--action submit-payroll-run --payroll-run-id <id>`

### 所有操作（高级级别）

### 人力资源（HR）——员工管理（CRUD操作，共4个）

| 操作 | 必需的参数 | 可选的参数 |
|--------|---------------|----------------|
| `add-employee` | `--first-name`, `--last-name`, `--date-of-joining`, `--company-id` | `--employee-id`, `--department-id`, `--designation-id`, `--employee-grade-id`, `--reporting-to`, `--holiday-list-id` |
| `update-employee` | `--employee-id` | `--first-name`, `--last-name`, `--department-id`, `--designation-id`, `--status`, `--reporting-to` |
| `get-employee` | `--employee-id` | |
| `list-employees` | | `--company-id`, `--department-id`, `--status`, `--search`, `--limit`, `--offset` |

### 人力资源——组织结构管理（CRUD操作，共4个）

| 操作 | 必需的参数 | 可选的参数 |
|--------|---------------|----------------|
| `add-department` | `--name`, `--company-id` | `--parent-id`, `--cost-center-id` |
| `list-departments` | | `--company-id` |
| `add-designation` | `--name` | |
| `list-designations` | | |

### 人力资源——休假类型管理（CRUD操作，共2个）

| 操作 | 必需的参数 | 可选的参数 |
|--------|---------------|----------------|
| `add-leave-type` | `--name`, `--max-days-allowed` | `--is-paid-leave`, `--is-carry-forward` |
| `list-leave-types` | | |

### 人力资源——休假管理（CRUD操作，共6个）

| 操作 | 必需的参数 | 可选的参数 |
|--------|---------------|----------------|
| `add-leave-allocation` | `--employee-id`, `--leave-type-id`, `--total-leaves`, `--fiscal-year` | |
| `get-leave-balance` | `--employee-id`, `--leave-type-id` | |
| `add-leave-application` | `--employee-id`, `--leave-type-id`, `--from-date`, `--to-date` | `--reason` |
| `approve-leave` | `--leave-application-id` | `--approved-by` |
| `reject-leave` | `--leave-application-id` | `--reason` |
| `list-leave-applications` | | `--employee-id`, `--status`, `--from-date`, `--to-date` |

### 人力资源——考勤管理（CRUD操作，共4个）

| 操作 | 必需的参数 | 可选的参数 |
|--------|---------------|----------------|
| `mark-attendance` | `--employee-id`, `--date`, `--status` | |
| `bulk-mark-attendance` | `--date`, `--entries` (JSON) | |
| `list-attendance` | | `--employee-id`, `--from-date`, `--to-date` |
| `add-holiday-list` | `--name`, `--from-date`, `--to-date`, `--company-id` | `--holidays` (JSON) |

考勤状态值：`present`（出席）、`absent`（缺席）、`half_day`（半天）、`on_leave`（休假中）、`wfh`（远程办公）。

### 人力资源——费用报销管理（CRUD操作，共6个）

| 操作 | 必需的参数 | 可选的参数 |
|--------|---------------|----------------|
| `add-expense-claim` | `--employee-id`, `--items` (JSON), `--company-id` | |
| `submit-expense-claim` | `--expense-claim-id` | |
| `approve-expense-claim` | `--expense-claim-id` | `--approved-by` |
| `reject-expense-claim` | `--expense-claim-id` | `--reason` |
| `update-expense-claim-status` | `--expense-claim-id`, `--status` | `--payment-entry-id` |
| `list-expense-claims` | | `--employee-id`, `--status`, `--company-id` |

费用报销的生命周期：草稿（Draft）→ 提交（Submitted）→ 批准（Approved）→ 支付（Paid）或被拒绝（Rejected）。

### 人力资源——员工生命周期管理及辅助操作（CRUD操作，共2个）

| 操作 | 必需的参数 | 可选的参数 |
|--------|---------------|----------------|
| `record-lifecycle-event` | `--employee-id`, `--event-type`, `--event-date` | `--details` (JSON) |
| `status` | | `--company-id` |

员工生命周期事件类型：招聘（hiring）、晋升（promotion）、调动（transfer）、离职（separation）、确认（confirmation）、职位调整（redesignation）。

“status”命令默认会发送到人力资源部门处理；相关的域别名包括：`hr-status` 和 `payroll-status`。

### 薪资管理——设置与配置（CRUD操作，共10个）

| 操作 | 必需的参数 | 可选的参数 |
|--------|---------------|----------------|
| `add-salary-component` | `--name`, `--component-type` | `--is-statutory` |
| `list-salary-components` | | |
| `add-salary-structure` | `--name`, `--company-id`, `--components` (JSON) | |
| `get-salary-structure` | `--salary-structure-id` | |
| `list-salary-structures` | | `--company-id` |
| `add-salary-assignment` | `--employee-id`, `--salary-structure-id`, `--base-amount`, `--effective-from` | |
| `list-salary-assignments` | | `--employee-id` |
| `add-income-tax-slab` | `--name`, `--tax-jurisdiction`, `--filing-status`, `--effective-from`, `--standard-deduction`, `--rates` (JSON) | |
| `update-fica-config` | `--tax-year` | `--ss-wage-base`, `--ss-employee-rate`, `--ss-employer-rate`, `--medicare-employee-rate`, `--medicare-employer-rate`, `--additional-medicare-threshold`, `--additional-medicare-rate` |
| `update-futa-suta-config` | `--tax-year` | FUTA/SUTA税率和工资基数相关参数 |

### 薪资管理——薪资处理（CRUD操作，共7个）

| 操作 | 必需的参数 | 可选的参数 |
|--------|---------------|----------------|
| `create-payroll-run` | `--company-id`, `--period-start`, `--period-end` | |
| `generate-salary-slips` | `--payroll-run-id` | |
| `get-salary-slip` | `--salary-slip-id` | |
| `list-salary-slips` | | `--payroll-run-id`, `--employee-id` |
| `submit-payroll-run` | `--payroll-run-id` | |
| `cancel-payroll-run` | `--payroll-run-id` | |
| `generate-w2-data` | `--tax-year`, `--company-id` | |

### 薪资管理——工资扣押（CRUD操作，共4个）

| 操作 | 必需的参数 | 可选的参数 |
|--------|---------------|----------------|
| `add-garnishment` | `--employee-id`, `--garnishment-type`, `--amount-or-percentage`, `--order-number`, `--creditor-name` | `--start-date`, `--end-date` |
| `update-garnishment` | `--garnishment-id` | `--amount-or-percentage`, `--status` |
| `list-garnishments` | | `--employee-id`, `--status` |
| `get-garnishment` | `--garnishment-id` | |

### 薪资管理——状态查询（CRUD操作，共1个）

| 用户输入 | 对应操作 |
|-----------|--------|
| "添加员工" / "新员工招聘" | `add-employee` |
| "查看员工列表" | `list-employees` |
| "申请休假" / "请求休假" | `add-leave-application` |
| "批准休假" | `approve-leave` |
| "查询休假余额" | `get-leave-balance` |
| "标记考勤" | `mark-attendance` |
| "添加费用报销" | `add-expense-claim` |
| "批准费用报销" | `approve-expense-claim` |
| "设置薪资结构" | `add-salary-structure` |
| "分配薪资" | `add-salary-assignment` |
| "运行薪资计算" | `create-payroll-run` -> `generate-salary-slips` -> `submit-payroll-run` |
| "查看工资单" | `get-salary-slip` |
| "生成W-2表格" | `generate-w2-data` |
| "添加工资扣押" | `add-garnishment` |
| "查询人力资源状态" / "查询员工状态" | `status` |
| "查询薪资状态" | `payroll-status` |

### 注意事项

在执行以下操作前请务必确认：`submit-*`、`cancel-*`、`approve-leave`、`reject-leave`、`approve-expense-claim`、`reject-expense-claim`。所有以`add-*`、`get-*`、`list-*`、`update-*`开头的操作会立即执行。

## 技术细节（高级级别）

### 架构

- **路由器**：`scripts/db_query.py`负责将请求路由到相应的内部脚本（`erpclaw-hr`（28个操作）和`erpclaw-payroll`（22个操作）。
- **数据库**：所有数据存储在`~/.openclaw/erpclaw/data.sqlite`文件中。
- **共享库**：`~/.openclaw/erpclaw/lib/erpclaw_lib/`（由`erpclaw`程序安装）。

### 所使用的表格（共24个）

- **人力资源相关表格**：`department`（部门）、`designation`（职位）、`employee_grade`（员工等级）、`holiday_list`（假期列表）、`holiday`（假期信息）、`employee`（员工信息）、`leave_type`（休假类型）、`leave_allocation`（休假分配）、`leave_application`（休假申请）、`attendance`（考勤记录）、`expense_claim`（费用报销）、`expense_claim_item`（费用报销明细）、`employee_lifecycle_event`（员工生命周期事件）。
- **薪资相关表格**：`salary_structure`（薪资结构）、`salary_structure_detail`（薪资结构详情）、`salary_component`（薪资组成部分）、`salary_assignment`（薪资分配）、`salary_slip`（工资单）、`salary_slip_detail`（工资单详情）、`payroll_run`（薪资计算记录）、`income_tax_slab`（所得税等级）、`income_tax_slab_rate`（所得税税率）、`fica_config`（FICA配置）、`futa_suta_config`（FUTA/SUTA配置）。

### 数据格式规范

- 数值类型：`Money` 使用 `TEXT`（Python的`Decimal`类型）；ID使用 `TEXT`（UUID4格式）；日期使用 `TEXT`（ISO 8601格式）；布尔值使用 `INTEGER`（0/1）。
- 所有金额均使用 `Decimal` 类型进行存储，并采用 `ROUND_HALF_UP` 方法进行四舍五入处理。
- 会计分录（GL entries）和薪资相关记录均为不可篡改的数据。
- 数据文件命名规则：`EMP-{YEAR}-{SEQ}`（员工相关）、`EC-{YEAR}-{SEQ}`（费用报销相关）、`LA-{YEAR}-{SEQ}`（休假申请相关）、`SS-{YEAR}-{SEQ}`（工资单相关）、`PR-{YEAR}-{SEQ}`（薪资计算相关）。

### 薪资会计处理规则

- **薪资相关分录**：
  - **借方（DR）**：`Salary Expense`（薪资支出）对应毛工资（按组成部分分类）；
  - **借方（DR）**：`Employer Tax Expense`（雇主应承担的税费，包括社会保障税、医疗保险税和FUTA/SUTA税）；
  - **贷方（CR）**：`Payroll Payable`（员工应得的净工资）；
  - **贷方（CR）**：`Federal IT Withheld`（员工需缴纳的联邦税）；
  - **贷方（CR）**：`SS Payable`（员工应缴纳的社会保障税）；
  - **贷方（CR）**：`Medicare Payable`（员工和雇主需缴纳的医疗保险税）。

- **费用报销相关分录**：
  - 批准费用报销后，会同时更新费用账户（借方）和员工应缴纳的税款（贷方）。
- **脚本路径**：详见````
scripts/db_query.py --action <action-name> [--key value ...]
````文件。