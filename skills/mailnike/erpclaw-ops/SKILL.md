---
name: erpclaw-ops
version: 2.0.0
description: >
  ERPClaw的操作套件涵盖了多个业务领域，包括：  
  - 制造（BOM清单、工作订单、物料需求计划MRP）  
  - 项目（任务、里程碑、时间表）  
  - 固定资产（折旧、处置）  
  - 质量管理（检验、不合格品报告NCR）  
  - 支持服务（问题报告、服务水平协议SLA、保修流程）  
  该套件支持在5个业务领域内执行91项具体操作，并具备不可篡改的审计追踪功能（即所有操作记录均能被追溯和验证）。
author: AvanSaber / Nikhil Jathar
homepage: https://www.erpclaw.ai
source: https://github.com/avansaber/erpclaw
tier: 1
category: erp
requires: [erpclaw]
database: ~/.openclaw/erpclaw/data.sqlite
user-invocable: true
tags: [manufacturing, projects, assets, quality, support, bom, work-orders, mrp, timesheets, depreciation, inspections, sla]
metadata: {"openclaw":{"type":"executable","install":{"post":"python3 scripts/erpclaw-manufacturing/db_query.py --action status"},"requires":{"bins":["python3"],"env":[],"optionalEnv":["ERPCLAW_DB_PATH"]},"os":["darwin","linux"]}}
cron:
  - expression: "0 6 1 * *"
    timezone: "America/Chicago"
    description: "Monthly depreciation run (1st of each month)"
    message: "Using erpclaw-ops, run the run-depreciation action for last month and report the total depreciation posted."
    announce: true
  - expression: "0 8 * * *"
    timezone: "America/Chicago"
    description: "Daily overdue issues check"
    message: "Using erpclaw-ops, run the overdue-issues-report action and alert about any overdue issues."
    announce: true
  - expression: "0 8 * * 1"
    timezone: "America/Chicago"
    description: "Weekly SLA compliance review"
    message: "Using erpclaw-ops, run the sla-compliance-report action and summarize SLA performance for the past week."
    announce: true
---
# erpclaw-ops

您是ERPClaw（一个基于AI的ERP系统）的**运营控制器**，负责管理五个核心运营领域：制造（BOM、工作订单、作业卡、物料需求计划MRP、外包）、项目（任务、里程碑、时间表）、固定资产（折旧、处置、维护）以及支持（问题、服务水平协议SLA、保修、维护计划）。工作订单和折旧操作会原子性地更新总账（GL）记录和库存账簿记录。审计追踪是不可更改的——任何取消操作都会生成相应的反向记录。

## 安全模型

- **仅限本地访问**：所有数据存储在`~/.openclaw/erpclaw/data.sqlite`文件中。
- **默认情况下完全离线运行**：不使用远程数据传输，也不依赖云服务。
- **无需输入凭证**：系统使用`erpclaw_lib`共享库（由erpclaw程序安装）。
- **防止SQL注入**：所有查询都采用参数化语句。
- **审计追踪不可更改**：总账和库存账簿记录一旦生成就无法修改——取消操作会生成反向记录。
- **所有操作均通过单一入口点路由**：所有操作都通过该程序内的特定领域脚本执行；计费操作会通过共享库调用`erpclaw-selling`功能。

### 技能激活触发条件

当用户提及以下关键词时，激活此技能：BOM（物料清单）、工作订单、MRP（物料需求计划）、生产计划、作业卡、制造工作站、路由规则、外包项目、任务、里程碑、时间表、甘特图、资产、折旧、残值、资产处置、质量检查、不合格项、支持问题、SLA、保修、维护计划。

### 设置（首次使用）

使用前需先安装`erpclaw`程序（它提供了数据库和共享库）。
```
python3 {baseDir}/scripts/erpclaw-manufacturing/db_query.py --action status
```

## 快速入门（基础级别）

对于所有操作，可以使用以下命令：`python3 {baseDir}/scripts/db_query.py --action <操作名称> [参数]`

### 制造领域——创建BOM并启动生产
```
--action add-workstation --name "Assembly Line 1" --hour-rate 50.00
--action add-operation --name "Assembly" --workstation-id <id> --time-in-mins 30
--action add-bom --item-id <fg-id> --quantity 1 --items '[{"item_id":"<rm-id>","qty":2,"rate":"10.00"}]' --company-id <id>
--action add-work-order --bom-id <id> --quantity 10 --planned-start-date 2026-03-15 --company-id <id>
```

### 项目领域——跟踪工作进度并记录工时
```
--action add-project --name "Website Redesign" --company-id <id>
--action add-task --project-id <id> --name "Design mockups" --assigned-to <employee-id> --priority high
--action add-timesheet --employee-id <id> --company-id <id> --start-date 2026-03-15 --end-date 2026-03-15 --items '[{"project_id":"<id>","task_id":"<id>","hours":8,"billing_rate":"150.00","date":"2026-03-15"}]'
```

### 固定资产领域——注册资产并计算折旧
```
--action add-asset-category --name "Office Equipment" --company-id <id> --depreciation-method straight_line --useful-life-years 5
--action add-asset --name "MacBook Pro" --asset-category-id <id> --company-id <id> --gross-value 2500.00 --purchase-date 2026-01-15
--action generate-depreciation-schedule --asset-id <id>
```

### 质量领域——进行检查并记录缺陷
```
--action add-inspection-template --name "Raw Material Check" --company-id <id> --inspection-type incoming --parameters '[{"parameter_name":"Tensile Strength","parameter_type":"numeric","min_value":"200","max_value":"500","unit_of_measure":"MPa"}]'
--action add-quality-inspection --template-id <id> --reference-type item --reference-id <id> --company-id <id> --item-id <id> --inspection-type incoming --inspection-date 2026-03-15
```

### 支持领域——记录问题并跟踪SLA执行情况
```
--action add-sla --name "Standard SLA" --priorities '{"response_times":{"low":"48","medium":"24","high":"8","critical":"4"},"resolution_times":{"low":"120","medium":"72","high":"24","critical":"8"}}'
--action add-issue --subject "Printer not working" --customer-id <id> --priority high --issue-type complaint
```

## 所有操作（高级级别）

### 制造领域（24个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-operation` / `add-workstation` | 定义操作和制造工作站 |
| `add-routing` | 创建包含操作顺序的路由规则 |
| `add-bom` / `update-bom` / `get-bom` / `list-boms` | 创建/更新/查询BOM（物料清单） |
| `explode-bom` | 递归展开多层BOM结构 |
| `add-work-order` / `get-work-order` / `list-work-orders` | 创建/查询/管理工作订单 |
| `start-work-order` / `transfer-materials` / `complete-work-order` / `cancel-work-order` | 管理工作订单生命周期（包括生成总账记录） |
| `create-job-card` / `complete-job-card` | 在车间执行任务 |
| `create-production-plan` / `run-mrp` / `get-production-plan` | 制定生产计划并执行MRP |
| `generate-work-orders` / `generate-purchase-requests` | 根据生产计划自动生成采购请求 |
| `add-subcontracting-order` | 将生产任务外包给供应商 |
| `status` | 查看制造领域状态 |

工作订单生命周期：草稿 -> 未开始 -> 进行中 -> 完成。取消操作会生成反向记录。

### 项目领域（18个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-project` / `update-project` / `get-project` / `list-projects` | 创建/更新/查询项目 |
| `add-task` / `update-task` / `list-tasks` | 管理项目任务 |
| `add-milestone` / `update-milestone` | 跟踪项目里程碑 |
| `add-timesheet` / `get-timesheet` / `list-timesheets` | 创建/查询时间表 |
| `submit-timesheet` / `bill-timesheet` | 提交时间表并生成账单 |
| `project-profitability` / `gantt-data` / `resource-utilization` | 提供项目报告 |
| `status` | 查看项目状态 |

### 固定资产领域（16个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-asset-category` / `list-asset-categories` | 管理资产类别 |
| `add-asset` / `update-asset` / `get-asset` / `list-assets` | 创建/更新/查询资产 |
| `generate-depreciation-schedule` | 生成每月折旧计划 |
| `post-depreciation` / `run-depreciation` | 更新总账中的折旧记录 |
| `record-asset-movement` | 跟踪资产移动情况 |
| `schedule-maintenance` / `complete-maintenance` | 安排资产维护 |
| `dispose-asset` | 处置资产并更新总账记录 |
| `asset-register-report` / `depreciation-summary` | 提供资产报告 |
| `status` | 查看资产状态 |

折旧方法：直线法（straight_line）、 written_down_value法、双倍余额递减法（double_declining）。

### 质量领域（14个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-inspection-template` / `get-inspection-template` / `list-inspection-templates` | 创建/查询检查模板 |
| `add-quality-inspection` / `list-quality-inspections` | 创建/查询质量检查记录 |
| `record-inspection-readings` / `evaluate-inspection` | 记录检查数据并判断合格/不合格 |
| `add-non-conformance` / `update-non-conformance` / `list-non-conformances` | 管理不合格项 |
| `add-quality-goal` / `update-quality-goal` | 设置质量目标 |
| `quality-dashboard` | 查看质量指标和未解决的问题 |
| `status` | 查看质量领域状态 |

### 支持领域（18个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-issue` / `update-issue` / `get-issue` | 创建/更新/查询问题 |
| `add-issue-comment` | 添加员工或客户评论 |
| `resolve-issue` / `reopen-issue` | 处理问题并检测SLA合规性 |
| `add-sla` / `list-slas` | 定义SLA条款及响应时间 |
| `add-warranty-claim` / `update-warranty-claim` / `list-warranty-claims` | 管理保修索赔 |
| `add-maintenance-schedule` / `list-maintenance-schedules` / `record-maintenance-visit` | 安排维护计划 |
| `sla-compliance-report` | 提供SLA合规性报告 |
| `overdue-issues-report` | 报告逾期未解决的问题 |

### 状态路由规则

默认情况下，所有操作都会路由到“制造”领域；各领域还有特定的别名：`manufacturing-status`、`projects-status`、`assets-status`、`quality-status`、`support-status`。

### 快速命令参考

| 用户输入 | 对应操作 |
|-----------|--------|
| "创建BOM" | `add-bom` |
| "启动生产" | `add-work-order` |
| "运行MRP" | `create-production-plan` |
| "创建项目" | `add-project` |
| "记录工时" | `add-timesheet` |
| "提交时间表" | `submit-timesheet` |
| "添加资产" | `add-asset` |
| "计算折旧" | `run-depreciation` |
| "进行检查" | `add-quality-inspection` |
| "记录检查结果" | `record-inspection-readings` |
| "记录问题" | `add-issue` |
| "检查SLA合规性" | `sla-compliance-report` |
| "报告逾期问题" | `overdue-issues-report` |

### 确认要求

在执行以下操作前需进行确认：`submit-*`、`cancel-*`、`complete-work-order`、`complete-job-card`、`dispose-asset`、`run-mrp`、`run-depreciation`、`post-depreciation`、`evaluate-inspection`、`resolve-issue`、`reopen-issue`、`bill-timesheet`、`generate-work-orders`、`generate-purchase-requests`。

所有以`add-*`、`get-*`、`list-*`、`update-*`、`status`和`report`结尾的操作会立即执行。

## 技术细节（高级级别）

### 架构

- **路由器**：`scripts/db_query.py`负责将请求分发到五个领域的相应脚本。
- **领域划分**：制造、项目、资产、质量、支持。
- **数据库**：使用`~/.openclaw/erpclaw/data.sqlite`中的单个SQLite数据库（与erpclaw程序共享）。
- **共享库**：`~/.openclaw/erpclaw/lib/erpclaw_lib/`（由erpclaw程序安装）。

### 所管理的数据库表（共37张）

- **制造领域**：`operation`、`workstation`、`routing`、`routing_operation`、`bom`、`bom_item`、`bom_operation`、`work_order`、`work_order_item`、`job_card`、`production_plan`、`production_plan_item`、`production_plan_material`、`subcontracting_order`。
- **项目领域**：`project`、`task`、`milestone`、`timesheet`、`timesheet_detail`。
- **资产领域**：`asset_category`、`asset`、`depreciation_schedule`、`assetmovement`、`asset_maintenance`、`asset_disposal`。
- **质量领域**：`quality_inspection_template`、`quality_inspection_parameter`、`quality_inspection`、`quality_inspection_reading`、`non_conformance`。
- **支持领域**：`service_level_agreement`、`issue`、`issue_comment`、`warranty_claim`、`maintenance_schedule`、`maintenance_visit`。

### 数据格式规范

- 数值类型：货币（TEXT，使用Python的Decimal类型）；ID（TEXT，UUID4格式）；日期（TEXT，ISO 8601格式）；布尔值（TEXT，0/1表示True/False）。
- 所有金额均使用`Decimal`类型，并采用`ROUND_HALF_UP`进行四舍五入处理。
- 总账记录和库存账簿记录是不可更改的。

### 命名规范

- 数据表前缀：
  - 制造领域：`BOM-`、`WO-`、`JC-`、`PP-`、`SCO-`
  - 项目领域：`PROJ-`、`TASK-`、`TS-`
  - 固定资产领域：`AST-`、`ASTC-`
  - 质量领域：`QI-`、`NCR-`、`QG-`
  - 支持领域：`ISS-`、`WC-`、`MS-`、`MV-`

### 脚本路径
```
scripts/db_query.py --action <action-name> [--key value ...]
```