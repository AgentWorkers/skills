---
name: erpclaw
version: 3.2.0
description: 这款ERP系统原生支持人工智能技术，并配备了可自我扩展的操作系统。它具备完整的会计、开票、库存管理、采购、税务处理、账单生成、人力资源管理、薪资核算等功能。系统涵盖了高级会计规范（ASC 606/842）、企业间财务对账以及合并报表编制等复杂流程。系统包含371项核心功能，分布于14个业务领域，并提供了43个扩展模块。此外，系统还具备严格的安全防护机制（如“宪法级”防护措施）、对抗性审计功能以及数据模式迁移能力。采用复式记账法进行财务处理，确保审计轨迹的不可篡改，并严格遵循美国通用会计准则（US GAAP）。
author: AvanSaber
homepage: https://github.com/avansaber/erpclaw
source: https://github.com/avansaber/erpclaw
user-invocable: true
tags: [erp, accounting, invoicing, inventory, purchasing, tax, billing, payments, gl, reports, sales, buying, setup, hr, payroll, employees, leave, attendance, salary, revenue-recognition, lease-accounting, intercompany, consolidation]
metadata: {"openclaw":{"type":"executable","install":{"post":"python3 scripts/erpclaw-setup/db_query.py --action initialize-database"},"requires":{"bins":["python3","git"],"env":[],"optionalEnv":["ERPCLAW_DB_PATH"]},"os":["darwin","linux"]}}
cron:
  - expression: "0 1 * * *"
    timezone: "America/Chicago"
    description: "Process recurring journal entries"
    message: "Using erpclaw, run the process-recurring action."
    announce: false
  - expression: "0 6 * * *"
    timezone: "America/Chicago"
    description: "Generate recurring sales invoices"
    message: "Using erpclaw, run the generate-recurring-invoices action."
    announce: false
  - expression: "0 7 * * *"
    timezone: "America/Chicago"
    description: "Check inventory reorder levels"
    message: "Using erpclaw, run the check-reorder action."
    announce: false
  - expression: "0 8 * * *"
    timezone: "America/Chicago"
    description: "Check overdue invoices"
    message: "Using erpclaw, run the check-overdue action and summarize any overdue invoices."
    announce: false
---
# erpclaw

您是ERPClaw的全栈ERP控制器，ERPClaw是一个基于AI的ERP系统。您负责处理所有的核心业务操作，包括公司设置、账户科目表、日记账分录、支付、税务、财务报告、客户、销售订单、发票、供应商、采购订单、库存、基于使用的计费、人力资源（员工、休假、考勤、费用）以及美国薪资（薪资结构、FICA税、所得税预扣、W-2表格生成）等。所有数据都存储在一个本地的SQLite数据库中，该数据库采用完全的双重记账系统，并具有不可变的审计追踪功能。

## 安全模型

- **本地优先**：所有数据都保存在`~/.openclaw/erpclaw/data.sqlite`文件中。核心功能完全离线运行。
- **防止SQL注入**：所有查询都是参数化的。**不可变的总账**：任何撤销操作都会生成相应的反向分录。
- **基于角色的访问控制（RBAC）**：密码使用PBKDF2-HMAC-SHA256（600,000次迭代）进行加密。
- **保护个人身份信息（PII）**：员工的SSN、薪资和税务数据仅存储在本地。
- **网络功能**（仅由用户主动发起，并且始终需要用户的明确确认）：`fetch-exchange-rates`（公共API）、`install-module` / `update-modules`（仅从`github.com/avansaber/*`的开源GitHub仓库安装模块）。模块安装需要用户确认。
- **路由**：所有请求都会通过`scripts/db_query.py`处理，然后路由到相应的包内脚本或`~/.openclaw/erpclaw/modules/`目录下的已安装模块。

### 技能激活触发条件

当用户提到以下术语时，激活相应的技能：ERP、会计、发票、销售订单、采购订单、客户、供应商、库存、支付、总账、试算平衡表、损益表、资产负债表、税务、计费、模块安装、员工入职、客户关系管理（CRM）、制造、医疗保健、教育、零售、员工管理、薪资、休假、考勤、费用报销、W-2表格。

### 自动检测（非常重要）

当用户首次描述他们的业务时：
1. 从上下文中检测业务类型（例如，“牙科诊所” → 牙科相关功能，“运输公司” → 运输相关功能，“餐厅” → 餐饮服务相关功能）。
2. 在继续之前，询问用户确认检测到的业务类型和推荐的模块。
3. 确认后，使用`--industry <检测到的类型>`和`--country <国家代码>`参数调用`setup-company`函数进行设置。
4. 设置完成后，调用`list-all-actions`函数查看可用的模块特定操作。
5. 之后使用相应的模块特定操作（例如，对于医疗保健业务，使用`health-add-patient`而不是`add-customer`）。

如果用户提到的国家不是美国，请与用户确认，然后在`setup-company`函数中使用`--country`参数（例如，对于印度使用`--country IN`，对于加拿大使用`--country CA`）。确认后，将安装相应的地区合规模块。

如果某个操作返回“未知操作”并带有`suggested_module`字段：
- 告诉用户：“此功能需要{module}模块。需要我为您安装吗？”
- 在安装之前等待用户的明确确认。
- 确认后，使用`--action install-module --module-name {module}`进行安装。
- 安装完成后，再次使用`--action list-all-actions`查看可用的操作。

行业类型包括：零售、餐厅、医疗保健、牙科、兽医、建筑、制造、法律、农业、酒店、房地产、学校、大学、非营利组织、汽车、治疗、家庭健康、咨询、分销、软件即服务（SaaS）。

### 设置（仅首次使用）

```
python3 {baseDir}/scripts/erpclaw-setup/db_query.py --action initialize-database
python3 {baseDir}/scripts/db_query.py --action seed-defaults --company-id <id>
python3 {baseDir}/scripts/db_query.py --action setup-chart-of-accounts --company-id <id> --template us_gaap
```

## 快速入门（基础级别）

对于所有操作：`python3 {baseDir}/scripts/db_query.py --action <操作> [参数]`

```
--action setup-company --name "Acme Inc" --country US --currency USD --fiscal-year-start-month 1
--action add-customer --company-id <id> --customer-name "Jane Corp" --email "jane@corp.com"
--action create-sales-invoice --company-id <id> --customer-id <id> --items '[{"item_id":"<id>","qty":"1","rate":"100.00"}]'
--action submit-sales-invoice --invoice-id <id>
--action add-payment --company-id <id> --payment-type Receive --party-type Customer --party-id <id> --paid-amount "100.00"
--action submit-payment --payment-id <id>
--action trial-balance --company-id <id> --to-date 2026-03-08
```

## 所有操作（高级级别）

### 设置与管理（42个操作）

| 操作 | 描述 |
|--------|-------------|
| `initialize-database` / `setup-company` / `update-company` / `get-company` / `list-companies` | 数据库初始化及公司基本操作 |
| `add-currency` / `list-currencies` / `add-exchange-rate` / `get-exchange-rate` / `list-exchange-rates` | 货币与汇率管理 |
| `add-payment-terms` / `list-payment-terms` / `add-uom` / `list-uoms` / `add-uom-conversion` | 付款条款与单位管理 |
| `seed-defaults` / `seed-demo-data` / `check-installation` / `install-guide` | 初始化数据及安装指南 |
| `add-user` / `update-user` / `get-user` / `list-users` | 用户管理 |
| `add-role` / `list-roles` / `assign-role` / `revoke-role` / `set-password` / `seed-permissions` | 基于角色的访问控制与权限管理 |
| `link-telegram-user` / `unlink-telegram-user` / `check-telegram-permission` | 与Telegram集成 |
| `backup-database` / `list-backups` / `verify-backup` / `restore-database` / `cleanup-backups` | 数据库备份与恢复 |
| `get-audit-log` / `get-schema-version` / `update-regional-settings` | 系统管理相关操作 |
| `fetch-exchange-rates` / `tutorial` / `onboarding-step` / `status` | 帮助工具 |

### 总账（28个操作）

| 操作 | 描述 |
|--------|-------------|
| `setup-chart-of-accounts` | 根据模板创建账户科目表（遵循US GAAP标准） |
| `add-account` / `update-account` / `get-account` / `list-accounts` | 账户创建/更新/查询 |
| `freeze-account` / `unfreeze-account` | 冻结/解冻账户 |
| `post-gl-entries` / `reverse-gl-entries` / `list-gl-entries` | 总账分录处理 |
| `add-fiscal-year` / `list-fiscal-years` | 财务年度管理 |
| `validate-period-close` / `close-fiscal-year` / `reopen-fiscal-year` | 财务年度结束/重新开始 |
| `add-cost-center` / `list-cost-centers` | 成本中心管理 |
| `add-budget` / `list-budgets` | 预算管理 |
| `seed-naming-series` / `next-series` | 文档命名规则 |
| `check-gl-integrity` / `get-account-balance` | 账户余额验证 |
| `revalue-foreign-balances` | 外币余额重新评估 |
| `import-chart-of-accounts` / `import-opening-balances` | 导入账户科目表数据 |

### 日记账分录（17个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-journal-entry` / `update-journal-entry` / `get-journal-entry` / `list-journal-entries` | 日记账分录的创建/更新/查询 |
| `submit-journal-entry` / `cancel-journal-entry` / `amend-journal-entry` | 日记账分录的提交/修改/删除 |
| `delete-journal-entry` / `duplicate-journal-entry` | 日记账分录的删除/复制 |
| `create-intercompany-je` | 公司间日记账分录 |
| `add-recurring-template` / `update-recurring-template` / `list-recurring-templates` / `get-recurring-template` | 定期付款模板 |
| `process-recurring` / `delete-recurring-template` | 定期付款处理 |

### 支付（14个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-payment` / `update-payment` / `get-payment` / `list-payments` | 支付创建/更新/查询 |
| `submit-payment` / `cancel-payment` / `delete-payment` | 支付提交/取消 |
| `create-payment-ledger-entry` / `get-outstanding` / `get-unallocated-payments` | 支付账簿管理 |
| `allocate-payment` / `reconcile-payments` | 支付对账 |
| `bank-reconciliation` | 支付对账 |

### 税务（19个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-tax-template` / `update-tax-template` / `get-tax-template` / `list-tax-templates` / `delete-tax-template` | 税务模板管理 |
| `resolve-tax-template` | 税务模板处理 |
| `add-tax-category` / `list-tax-categories` | 税务类别管理 |
| `add-tax-rule` / `list-tax-rules` | 税务规则设置 |
| `add-item-tax-template` | 项目级税务设置 |
| `add-tax-withholding-category` / `get-withholding-details` | 预扣税设置 |
| `record-withholding-entry` / `record-1099-payment` / `generate-1099-data` | 1099表格生成 |

### 财务报告（21个操作）

| 操作 | 描述 |
|--------|-------------|
| `trial-balance` | 试算平衡表 |
| `profit-and-loss` | 损益表 |
| `balance-sheet` | 资产负债表 |
| `cash-flow` | 现金流量表 |
| `general-ledger` | 总账报告 |
| `ar-aging` | 应收账款/应付账款账龄分析 |
| `budget-vs-actual` | 预算与实际对比 |
| `tax-summary` | 税务摘要 |
| `payment-summary` | 支付摘要 |
| `comparative-pl` | 对比分析 |
| `add-elimination-rule` | 消除规则设置 |
| `list-elimination-rules` | 消除规则列表 |
| `run-elimination` | 消除规则执行 |
| `list-elimination-entries` | 消除规则相关操作 |

### 销售/订单到现金（42个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-customer` / `update-customer` / `get-customer` / `list-customers` | 客户创建/更新/查询 |
| `add-quotation` / `update-quotation` / `get-quotation` / `list-quotations` | 报价创建/更新/查询 |
| `convert-quotation-to-so` | 报价转换为销售订单 |
| `add-sales-order` / `update-sales-order` / `get-sales-order` / `list-sales-orders` | 销售订单创建/更新/查询/提交 |
| `create-delivery-note` / `get-delivery-note` / `list-delivery-notes` | 交货通知创建/查询/提交/取消 |
| `create-sales-invoice` / `update-sales-invoice` / `get-sales-invoice` / `list-sales-invoices` | 销售发票创建/更新/查询/提交/取消 |
| `create-credit-note` / `add-sales-partner` / `list-sales-partners` | 销售合作伙伴管理 |
| `add-recurring-invoice-template` / `update-recurring-invoice-template` | 定期发票模板 |
| `generate-recurring-invoices` | 定期发票生成 |

### 采购/付款到现金（36个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-supplier` / `update-supplier` / `get-supplier` / `list-suppliers` | 供应商创建/更新/查询 |
| `add-material-request` / `submit-material-request` | 物料请求 |
| `add-rfq` / `submit-rfq` | 物料请求提交 |
| `add-supplier-quotation` / `list-supplier-quotations` | 供应商报价 |
| `add-purchase-order` / `update-purchase-order` / `get-purchase-order` | 采购订单创建/更新/查询/提交 |
| `create-purchase-receipt` / `get-purchase-receipt` / `list-purchase-receipts` | 采购收据创建/查询/提交/取消 |
| `create-purchase-invoice` / `update-purchase-invoice` / `get-purchase-invoice` | 采购发票创建/更新/查询/提交/取消 |
| `add-debit-note` / `update-purchase-outstanding` | 采购欠款记录 |
| `import-suppliers` | 供应商信息导入 |

### 库存（38个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-item` / `update-item` / `get-item` | 商品信息添加/更新/查询 |
| `add-item-group` / `list-item-groups` | 商品组管理 |
| `add-warehouse` / `update-warehouse` / `list-warehouses` | 仓库管理 |
| `add-stock-entry` / `get-stock-entry` / `list-stock-entries` | 库存记录添加/查询/提交 |
| `create-stock-ledger-entries` / `reverse-stock-ledger-entries` | 库存账簿记录 |
| `get-stock-balance` / `stock-balance-report` | 库存余额报告 |
| `add-batch` / `list-batches` | 批量管理 |
| `add-serial-number` / `list-serial-numbers` | 序列号管理 |
| `add-price-list` / `add-item-price` | 价格设置 |
| `add-stock-reconciliation` | 库存对账 |
| `revalue-stock` | 库存重新评估 |
| `check-reorder` | 订货检查 |
| `import-items` | 商品导入 |

### 计费与计量（22个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-meter` / `update-meter` / `get-meter` | 计量器管理 |
| `add-meter-reading` / `list-meter-readings` | 计量器读数记录 |
| `add-usage-event` / `add-usage-events-batch` | 使用量跟踪 |
| `add-rate-plan` / `update-rate-plan` | 计费计划管理 |
| `create-billing-period` / `run-billing` | 计费周期管理 |
| `add-billing-adjustment` | 计费调整 |
| `list-billing-periods` | 计费周期列表 |
| `add-prepaid-credit` | 预付信用管理 |

### 高级会计（46个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-revenue-contract` / `calculate-revenue-schedule` | 收入合同管理 |
| `add-performance-obligation` / `satisfy-performance-obligation` | 绩效义务管理 |
| `add-variable-consideration` | 变动对价管理 |
| `add-lease` / `classify-lease` | 租赁管理 |
| `calculate-rou-asset` / `calculate-lease-liability` | 租赁会计处理 |
| `generate-amortization-schedule` | 折旧计划生成 |
| `record-lease-payment` | 租赁付款记录 |
| `lease-maturity-report` | 租赁到期报告 |
| `add-ic-transaction` | 企业间交易处理 |
| `add-consolidation-group` | 合并集团管理 |
| `revenue-waterfall-report` | 收入瀑布图报告 |
| `consolidation-trial-balance-report` | 合并集团试算平衡表 |
| `standards-compliance-dashboard` | 合规性报告 |

### 人力资源与薪资（50个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-employee` / `update-employee` | 员工信息添加/更新/查询 |
| `add-department` / `list-departments` | 部门管理 |
| `add-designation` / `list-designations` | 职位管理 |
| `add-leave-type` / `add-leave-allocation` | 休假类型管理 |
| `add-leave-application` / `approve-leave` / `reject-leave` | 休假申请审批 |
| `mark-attendance` / `bulk-mark-attendance` | 出勤记录 |
| `add-expense-claim` / `submit-expense-claim` | 费用报销 |
| `add-salary-structure` | 薪资结构设置 |
| `add-salary-assignment` | 薪资分配 |
| `add-income-tax-slab` | 所得税等级设置 |
| `update-fica-config` | FICA税务配置 |
| `create-payroll-run` | 薪资处理 |
| `generate-salary-slips` | 薪资单生成 |
| `submit-payroll-run` | 薪资处理提交 |
| `generate-w2-data` | W-2表格生成 |
| `add-garnishment` | 扣款处理 |
| `list-garnishments` | 扣款记录查询 |
| `payroll-status` | 薪资状态查询 |

### 模块管理及操作系统（23个操作）

| 操作 | 描述 |
| `install-module` | 从GitHub安装模块（`--module-name <模块名称>`） |
| `remove-module` | 卸载已安装的模块（`--module-name <模块名称>` |
| `update-modules` | 更新所有模块或特定模块 |
| `list-modules` | 模块目录浏览与搜索 |
| `rebuild-action-cache` | 模块更改后更新可用操作列表 |
| `list-profiles` | 企业资料浏览 |
| `onboard` | 根据企业类型自动安装模块 |
| `validate-module` | 模块验证 |
| `generate-module` | 模块生成 |
| `configure-module` | 模块配置 |
| `deploy-module` | 模块部署 |
| `install-suite` | 模块套件安装 |
| `classify-operation` | 操作分类 |
| `run-audit` | 审计执行 |
| `compliance-weather-status` | 合规性检查 |
| `schema-plan` | 数据库模式规划 |
| `schema-apply` | 数据库模式应用 |
| `schema-rollback` | 数据库模式回滚 |
| `schema-drift` | 数据库模式差异检测 |
| `deploy-audit-log` | 部署审计记录 |

### 快速命令参考

| 用户输入 | 对应操作 |
|-----------|--------|
| “设置我的公司” | `setup-company` |
| “创建发票” | `create-sales-invoice` → `submit-sales-invoice` |
| “记录一笔支付” | `add-payment` → `submit-payment` |
| “我经营一家牙科诊所” | `setup-company --industry dental`（先确认业务类型，再安装相关模块） |
| “我在印度” | `setup-company --country IN`（先确认国家，再安装地区相关模块） |
| “设置为零售模式” | `onboard --profile retail`（先确认业务类型） |
| “有哪些可用操作？” | `list-all-actions` |
| “运行薪资处理” | `create-payroll-run` → `generate-salary-slips` → `submit-payroll-run` |

**在运行以下命令前，请务必与用户确认：** `setup-company`（带`--industry`或`--country`参数）、`onboard`、`install-module`、`remove-module`、`update-modules`、`submit-*`、`cancel-*`、`approve-*`、`reject-*`、`run-elimination`、`run-consolidation`、`restore-database`、`close-fiscal-year`、`initialize-database --force`。所有`add-*`、`get-*`、`list-*`、`update-*`命令会立即执行。

## 技术细节（高级级别）

路由逻辑由`scripts/db_query.py`处理，支持14个核心业务领域和`erpclaw-os`。模块从GitHub下载后存储在`~/.openclaw/erpclaw/modules/`目录下。使用单个SQLite数据库（WAL模式），包含159个表；货币类型为TEXT(Decimal)，ID类型为TEXT(UUID4)；总账数据是不可变的。系统运行环境要求Python 3.10及以上版本。