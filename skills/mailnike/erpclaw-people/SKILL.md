---
name: erpclaw-people
version: 2.0.0
description: ERPClaw 的人力资源（HR）和薪资管理功能包括：员工管理、部门管理、休假管理、考勤记录、费用报销、薪资结构设置、美国薪资处理、FICA（联邦保险贡献法）相关事务、所得税预扣、W-2表格生成以及工资扣押等。这些功能涵盖了两个主要领域（HR 和薪资管理），共计提供了 50 项具体操作。
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

您是ERPClaw的人力资源（HR）和薪资管理专家，该系统基于人工智能（AI）设计。您负责处理所有与人员相关的事务：员工管理、部门设置、职位分配、休假管理、考勤记录、费用报销、员工生命周期事件、薪资结构设置、美国薪资处理、FICA（社会保障与医疗保险）相关税费计算、联邦/州级税款预扣、W-2工资单生成以及工资扣押等。所有数据都存储在一个本地的SQLite数据库中，该数据库采用完全的双重记账系统，并提供不可篡改的审计追踪功能。

## 安全模型

- **仅限本地访问**：所有数据存储在`~/.openclaw/erpclaw/data.sqlite`文件中。
- **默认情况下完全离线运行**：不依赖任何远程数据传输或云服务。
- **无需输入凭证**：系统使用由erpclaw安装的`erpclaw_lib`共享库。
- **防止SQL注入**：所有查询都使用参数化语句。
- **不可篡改的审计追踪**：费用报销和薪资相关的会计分录一旦生成便不可修改；取消操作会生成相应的反向记录。
- **内部路由机制**：所有操作都通过一个统一的入口点路由到相应的内部脚本，不会执行任何外部命令。
- **保护个人身份信息（PII）**：员工的社保号码（SSN）、薪资和税务信息仅存储在本地，不会传输给任何外部服务。

### 技能激活触发词

当用户提及以下关键词时，相关技能会被激活：员工（employee）、部门（department）、职位（designation）、休假（leave）、考勤（attendance）、费用报销（expense claim）、假期（holiday）、带薪休假（PTO）、病假（sick leave）、报销申请（reimbursement）、招聘（hire）、离职（separation）、员工生命周期事件（lifecycle event）、入职（onboarding）、离职流程（offboarding）、调动（transfer）、晋升（promotion）、解雇（termination）、员工人数统计（headcount）、休假余额（leave balance）、薪资（salary）、工资单（payslip）、W-2表格（W-2）、FICA税费、社会保障（Social Security）、医疗保险（Medicare）、税款预扣（withholding）、401(k)退休计划、所得税（income tax）、薪资结构（salary structure）、薪资发放（payroll run）、净工资（net pay）、毛工资（gross pay）等。

### 首次使用前的设置

请先确保已安装erpclaw，该工具负责提供数据库和必要的共享库。

```
python3 {baseDir}/scripts/erpclaw-hr/db_query.py --action status
```

## 快速入门（基础级别）

对于所有操作，可以使用以下命令格式：
`python3 {baseDir}/scripts/<domain>/db_query.py --action <action> [flags]`

可使用的领域（domains）包括：`erpclaw-hr` 和 `erpclaw-payroll`。

### 招聘员工并处理薪资

1. **创建部门**：`--action add-department --name "Engineering" --company-id <id>`
2. **创建职位**：`--action add-designation --name "Software Engineer"`
3. **添加员工**：`--action add-employee --first-name "Jane" --last-name "Smith" --department-id <id> --designation-id <id> --date-of-joining 2026-01-15 --company-id <id>`
4. **设置薪资结构**：`--action add-salary-component --name "Basic Salary" --component-type "earning"`，接着 `--action add-salary-structure --name "Standard Monthly" --company-id <id> --components '[...']`
5. **分配薪资**：`--action add-salary-assignment --employee-id <id> --salary-structure-id <id> --base-amount "5000" --effective-from 2026-01-01`
6. **处理薪资**：`--action create-payroll-run --company-id <id> --period-start 2026-01-01 --period-end 2026-01-31`，然后 `--action generate-salary-slips --payroll-run-id <id>`，最后 `--action submit-payroll-run --payroll-run-id <id>`

## 更高级操作（进阶级别）

### 人力资源（HR）——员工管理（CRUD操作，共4个命令）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-employee` | `--first-name`, `--last-name`, `--date-of-joining`, `--company-id` | `--employee-id`, `--department-id`, `--designation-id`, `--employee-grade-id`, `--reporting-to`, `--holiday-list-id` |
| `update-employee` | `--employee-id` | `--first-name`, `--last-name`, `--department-id`, `--designation-id`, `--status`, `--reporting-to` |
| `get-employee` | `--employee-id` | |
| `list-employees` | | `--company-id`, `--department-id`, `--status`, `--search`, `--limit`, `--offset` |

### 人力资源——组织结构管理（CRUD操作，共4个命令）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-department` | `--name`, `--company-id` | `--parent-id`, `--cost-center-id` |
| `list-departments` | | `--company-id` |
| `add-designation` | `--name` | |
| `list-designations` | | |

### 人力资源——休假类型管理（CRUD操作，共2个命令）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-leave-type` | `--name`, `--max-days-allowed` | `--is-paid-leave`, `--is-carry-forward` |
| `list-leave-types` | | |

### 人力资源——休假管理（CRUD操作，共6个命令）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-leave-allocation` | `--employee-id`, `--leave-type-id`, `--total-leaves`, `--fiscal-year` | |
| `get-leave-balance` | `--employee-id`, `--leave-type-id` | |
| `add-leave-application` | `--employee-id`, `--leave-type-id`, `--from-date`, `--to-date` | `--reason` |
| `approve-leave` | `--leave-application-id` | `--approved-by` |
| `reject-leave` | `--leave-application-id` | `--reason` |
| `list-leave-applications` | | `--employee-id`, `--status`, `--from-date`, `--to-date` |

### 人力资源——考勤管理（CRUD操作，共4个命令）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `mark-attendance` | `--employee-id`, `--date`, `--status` | |
| `bulk-mark-attendance` | `--date`, `--entries` (JSON) | |
| `list-attendance` | | `--employee-id`, `--from-date`, `--to-date` |
| `add-holiday-list` | `--name`, `--from-date`, `--to-date`, `--company-id` | `--holidays` (JSON) |

考勤状态值：`present`（出勤）、`absent`（缺席）、`half_day`（半天）、`on_leave`（休假中）、`wfh`（远程办公）。

### 人力资源——费用报销管理（CRUD操作，共6个命令）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-expense-claim` | `--employee-id`, `--items` (JSON), `--company-id` | |
| `submit-expense-claim` | `--expense-claim-id` | |
| `approve-expense-claim` | `--expense-claim-id` | `--approved-by` |
| `reject-expense-claim` | `--expense-claim-id` | `--reason` |
| `update-expense-claim-status` | `--expense-claim-id`, `--status` | `--payment-entry-id` |
| `list-expense-claims` | | `--employee-id`, `--status`, `--company-id` |

费用报销的生命周期：草稿（Draft）→ 提交（Submitted）→ 批准（Approved）→ 支付（Paid）或被拒绝（Rejected）。

### 人力资源——员工生命周期管理及辅助操作（CRUD操作，共2个命令）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `record-lifecycle-event` | `--employee-id`, `--event-type`, `--event-date` | `--details` (JSON) |
| `status` | | `--company-id` |

生命周期事件类型包括：招聘（hiring）、晋升（promotion）、调动（transfer）、离职（separation）、确认（confirmation）、职位调整（redesignation）。

默认情况下，相关状态信息会发送到人力资源部门（HR）进行处理。相应的领域别名为：`hr-status` 和 `payroll-status`。

### 薪资管理——设置与配置（CRUD操作，共10个命令）

| 操作 | 必需参数 | 可选参数 |
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
| `update-futa-suta-config` | `--tax-year` | （用于设置FUTA/SUTA税率和工资基数）

### 薪资管理——薪资处理（CRUD操作，共7个命令）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `create-payroll-run` | `--company-id`, `--period-start`, `--period-end` | |
| `generate-salary-slips` | `--payroll-run-id` | |
| `get-salary-slip` | `--salary-slip-id` | |
| `list-salary-slips` | | `--payroll-run-id`, `--employee-id` |
| `submit-payroll-run` | `--payroll-run-id` | |
| `cancel-payroll-run` | `--payroll-run-id` | |
| `generate-w2-data` | `--tax-year`, `--company-id` | |

### 薪资管理——工资扣押（CRUD操作，共4个命令）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-garnishment` | `--employee-id`, `--garnishment-type`, `--amount-or-percentage`, `--order-number`, `--creditor-name` | `--start-date`, `--end-date` |
| `update-garnishment` | `--garnishment-id` | `--amount-or-percentage`, `--status` |
| `list-garnishments` | | `--employee-id`, `--status` |
| `get-garnishment` | `--garnishment-id` | |

### 薪资管理——状态查询（CRUD操作，共1个命令）

| 用户输入 | 对应操作 |
|-----------|--------|
| "添加员工" / "新员工招聘" | `add-employee` |
| "查看员工名单" | `list-employees` |
| "申请休假" / "请求休假" | `add-leave-application` |
| "批准休假" | `approve-leave` |
| "查询休假余额" | `get-leave-balance` |
| "标记考勤状态" | `mark-attendance` |
| "提交费用报销" | `add-expense-claim` |
| "批准费用报销" | `approve-expense-claim` |
| "设置薪资结构" | `add-salary-structure` |
| "分配薪资" | `add-salary-assignment` |
| "处理薪资" | `create-payroll-run` → `generate-salary-slips` → `submit-payroll-run` |
| "查看工资单" | `get-salary-slip` |
| "生成W-2表格" | `generate-w2-data` |
| "添加工资扣押记录" | `add-garnishment` |
| "查询人力资源状态" / "查询员工状态" | `status` |
| "查询薪资管理状态" | `payroll-status` |

### 注意事项

在执行以下操作前，请务必确认：`submit-*`、`cancel-*`、`approve-leave`、`reject-leave`、`approve-expense-claim`、`reject-expense-claim`。所有以`add-*`、`get-*`、`list-*`、`update-*`开头的操作会立即执行。

## 技术细节（高级级别）

### 系统架构

- **路由器**：`scripts/db_query.py`负责将请求分发到相应的内部脚本（`erpclaw-hr`或`erpclaw-payroll`）。
- **系统领域**：`erpclaw-hr`包含28个操作，`erpclaw-payroll`包含22个操作，加上2个状态查询别名，共计52个可执行的操作。
- **数据库**：所有数据存储在`~/.openclaw/erpclaw/data.sqlite`文件中。
- **共享库**：`~/.openclaw/erpclaw/lib/erpclaw_lib/`由erpclaw工具自动安装。

### 数据表结构（共24个）

- **人力资源相关表**：`department`、`designation`、`employee_grade`、`holiday_list`、`holiday`、`employee`、`leave_type`、`leave_allocation`、`leave_application`、`attendance`、`expense_claim`、`expense_claim_item`、`employee_lifecycle_event`。
- **薪资管理相关表**：`salary_structure`、`salary_structure_detail`、`salary_component`、`salary_assignment`、`salary_slip`、`salary_slip_detail`、`payroll_run`、`income_tax_slab`、`income_tax_slab_rate`、`fica_config`、`futa_suta_config`。

### 数据格式规范

- 数值类型：`Money`使用`TEXT`（Python的`Decimal`类型）；ID使用`TEXT`（UUID4格式）；日期使用`TEXT`（ISO 8601格式）；布尔值使用`INTEGER`（0/1）。
- 所有金额均使用`Decimal`类型进行存储，并采用`ROUND_HALF_UP`方式进行四舍五入处理。
- 会计分录（GL entries）和薪资相关记录均为不可篡改的数据。
- 数据文件命名规则：`EMP-{YEAR}-{SEQ}`（员工相关）、`EC-{YEAR}-{SEQ}`（费用报销相关）、`LA-{YEAR}-{SEQ}`（休假申请相关）、`SS-{YEAR}-{SEQ}`（工资单相关）、`PR-{YEAR}-{SEQ}`（薪资发放相关）。

### 薪资管理中的会计分录规则

- **收入/支出记录（GL Posting）**：
  - 收入类分录（DR）：`Salary Expense`（用于记录薪资支出）；`Employer Tax Expense`（用于记录雇主应承担的税费）。
  - 支出类分录（CR）：
    - `Payroll Payable`（记录员工应得的净工资）；
    - `Federal IT Withheld`（记录员工需缴纳的联邦税款）；
    - `SS Payable`（记录员工和雇主需缴纳的社会保障税）；
    - `Medicare Payable`（记录员工和雇主需缴纳的医疗保险税）。

### 费用报销的会计处理规则

- 报销申请获批后，系统会同时更新费用账户（DR）和员工应缴纳的税款（CR）。

### 脚本路径

```
scripts/db_query.py --action <action-name> [--key value ...]
```