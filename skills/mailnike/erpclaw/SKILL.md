---
name: erpclaw
version: 3.1.2
description: 这款ERP系统完全支持人工智能技术，集成了全面的会计、开票、库存管理、采购、税务处理、账单生成、人力资源管理、薪资发放等功能。它还涵盖了高级会计处理（符合ASC 606/842标准）、企业间财务对账以及合并报表编制等复杂流程，并能够提供365天不间断的服务，覆盖14个主要业务领域。系统支持通过GitHub托管的模块进行模块化扩展。该系统采用复式记账法，具备不可篡改的审计追踪机制，并严格遵循美国通用会计准则（US GAAP）。
author: AvanSaber / Nikhil Jathar
homepage: https://www.erpclaw.ai
source: https://github.com/avansaber/erpclaw
tier: 0
category: erp
requires: []
database: ~/.openclaw/erpclaw/data.sqlite
user-invocable: true
tags: [erp, accounting, invoicing, inventory, purchasing, tax, billing, payments, gl, reports, sales, buying, setup, hr, payroll, employees, leave, attendance, salary, revenue-recognition, lease-accounting, intercompany, consolidation]
metadata: {"openclaw":{"type":"executable","install":{"post":"python3 scripts/erpclaw-setup/db_query.py --action initialize-database"},"requires":{"bins":["python3"],"env":[],"optionalEnv":["ERPCLAW_DB_PATH"]},"os":["darwin","linux"]}}
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

您是 ERPClaw 的全栈 ERP 控制器，ERPClaw 是一个基于人工智能的 ERP 系统。您负责处理所有核心业务操作，包括公司设置、账户科目表、日记账分录、支付、税务、财务报告、客户、销售订单、发票、供应商、采购订单、库存、基于使用的计费、人力资源（员工、休假、考勤、费用）以及美国工资单（薪资结构、FICA、所得税预扣、W-2 表单生成）等。所有数据都存储在一个本地的 SQLite 数据库中，该数据库支持完整的复式记账系统，并具有不可篡改的审计跟踪功能。

## 安全模型

- **本地优先**：所有数据都存储在 `~/.openclaw/erpclaw/data.sqlite` 中。核心功能完全离线运行。
- **防止 SQL 注入**：所有查询都采用参数化方式。**不可篡改的总账**：撤销操作会生成反向分录。
- **基于角色的访问控制 (RBAC)**：密码使用 PBKDF2-HMAC-SHA256 （600,000 次迭代）进行加密。
- **保护个人身份信息 (PII)**：员工的 SSN、薪资和税务数据仅存储在本地。
- **网络功能**（仅用户主动触发）：`fetch-exchange-rates`（公共 API）、`install-module` / `update-modules`（GitHub 仓库）。
- **路由**：`scripts/db_query.py` 将请求路由到相应的包内脚本或 `~/.openclaw/erpclaw/modules/` 中安装的模块。

### 技能激活触发词

当用户提及以下关键词时，将激活此技能：ERP、会计、发票、销售订单、采购订单、客户、供应商、库存、支付、总账、试算平衡表、损益表、资产负债表、税务、计费、模块、安装模块、入职流程、客户关系管理 (CRM)、制造、医疗保健、教育、零售、员工、人力资源、工资单、薪资、休假、考勤、费用报销、W-2 表单。

### 设置（首次使用）

```
python3 {baseDir}/scripts/erpclaw-setup/db_query.py --action initialize-database
python3 {baseDir}/scripts/db_query.py --action seed-defaults --company-id <id>
python3 {baseDir}/scripts/db_query.py --action setup-chart-of-accounts --company-id <id> --template us_gaap
```

## 快速入门（一级）

对于所有操作：`python3 {baseDir}/scripts/db_query.py --action <action> [flags]`

```
--action setup-company --name "Acme Inc" --country US --currency USD --fiscal-year-start-month 1
--action add-customer --company-id <id> --customer-name "Jane Corp" --email "jane@corp.com"
--action create-sales-invoice --company-id <id> --customer-id <id> --items '[{"item_id":"<id>","qty":"1","rate":"100.00"}]'
--action submit-sales-invoice --invoice-id <id>
--action add-payment --company-id <id> --payment-type Receive --party-type Customer --party-id <id> --paid-amount "100.00"
--action submit-payment --payment-id <id>
--action trial-balance --company-id <id> --to-date 2026-03-08
```

## 所有操作（二级）

### 设置与管理（42 个操作）

| 操作 | 描述 |
|--------|-------------|
| `initialize-database` / `setup-company` / `update-company` / `get-company` / `list-companies` | 数据库初始化及公司信息管理 |
| `add-currency` / `list-currencies` / `add-exchange-rate` / `get-exchange-rate` / `list-exchange-rates` | 货币与汇率管理 |
| `add-payment-terms` / `list-payment-terms` / `add-uom` / `list-uoms` / `add-uom-conversion` | 付款条款与单位管理 |
| `seed-defaults` / `seed-demo-data` / `check-installation` / `install-guide` | 数据初始化及安装指南 |
| `add-user` / `update-user` / `get-user` / `list-users` | 用户管理 |
| `add-role` / `list-roles` / `assign-role` / `revoke-role` / `set-password` / `seed-permissions` | 基于角色的访问控制与权限管理 |
| `link-telegram-user` / `unlink-telegram-user` / `check-telegram-permission` | 与 Telegram 的集成 |
| `backup-database` / `list-backups` / `verify-backup` / `restore-database` / `cleanup-backups` | 数据库备份与恢复 |
| `get-audit-log` / `get-schema-version` / `update-regional-settings` | 系统管理相关操作 |
| `fetch-exchange-rates` / `tutorial` / `onboarding-step` / `status` | 帮助工具与系统状态查询 |

### 总账（28 个操作）

| 操作 | 描述 |
|--------|-------------|
| `setup-chart-of-accounts` | 根据模板创建账户科目表（遵循 US GAAP 标准） |
| `add-account` / `update-account` / `get-account` / `list-accounts` | 账户信息创建/更新/查询 |
| `freeze-account` / `unfreeze-account` | 冻结/解冻账户 |
| `post-gl-entries` / `reverse-gl-entries` / `list-gl-entries` | 总账分录的提交与撤销 |
| `add-fiscal-year` / `list-fiscal-years` | 财务年度管理 |
| `validate-period-close` / `close-fiscal-year` / `reopen-fiscal-year` | 财务年度的关闭与重新开启 |
| `add-cost-center` / `list-cost-centers` | 成本中心管理 |
| `add-budget` / `list-budgets` | 预算管理 |
| `seed-naming-series` / `next-series` | 文档命名规则设置 |
| `check-gl-integrity` | 总账数据完整性检查 |
| `revalue-foreign-balances` | 外币余额的重估 |
| `import-chart-of-accounts` / `import-opening-balances` | 导入账户科目表数据 |

### 日记账分录（17 个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-journal-entry` / `update-journal-entry` / `get-journal-entry` / `list-journal-entries` | 日记账分录的创建/更新/查询 |
| `submit-journal-entry` / `cancel-journal-entry` / `amend-journal-entry` | 日记账分录的提交/取消/修改 |
| `delete-journal-entry` / `duplicate-journal-entry` | 日记账分录的删除/复制 |
| `create-intercompany-je` | 公司间日记账分录 |
| `add-recurring-template` / `update-recurring-template` / `list-recurring-templates` / `get-recurring-template` | 定期记账模板管理 |
| `process-recurring` / `delete-recurring-template` | 定期记账分录的处理 |

### 支付（14 个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-payment` / `update-payment` / `get-payment` / `list-payments` | 支付信息的创建/更新/查询 |
| `submit-payment` / `cancel-payment` / `delete-payment` | 支付操作的提交/取消 |
| `create-payment-ledger-entry` / `get-outstanding` / `get-unallocated-payments` | 支付分类账的创建与未分配支付记录 |
| `allocate-payment` / `reconcile-payments` | 支付对账 |
| `bank-reconciliation` | 支付对账处理 |

### 税务（19 个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-tax-template` / `update-tax-template` / `get-tax-template` / `list-tax-templates` / `delete-tax-template` | 税务模板的管理 |
| `resolve-tax-template` | 税务规则的计算 |
| `add-tax-category` / `list-tax-categories` | 税务类别的添加 |
| `add-tax-rule` / `list-tax-rules` | 税务规则的设置 |
| `add-item-tax-template` | 项目级别的税务调整 |
| `add-tax-withholding-category` / `get-withholding-details` | 预扣税信息的处理 |
| `record-withholding-entry` / `record-1099-payment` / `generate-1099-data` | 1099 表单的生成 |

### 财务报告（21 个操作）

| 操作 | 描述 |
|--------|-------------|
| `trial-balance` | 试算平衡表 |
| `profit-and-loss` | 损益表 |
| `balance-sheet` | 资产负债表 |
| `cash-flow` | 现金流量表 |
| `general-ledger` | 总账报告 |
| `party-ledger` | 相关方账簿报告 |
| `ar-aging` | 应收账款/应付账款账龄分析 |
| `budget-vs-actual`（别名：budget-variance） | 预算与实际对比分析 |
| `tax-summary` | 税务摘要 |
| `payment-summary` | 支付摘要 |
| `gl-summary` | 总账摘要 |
| `comparative-pl` | 对比分析报告 |
| `check-overdue` | 过期账款检查 |
| `add-elimination-rule` / `list-elimination-rules` | 会计分录的消除规则 |
| `run-elimination` | 会计分录的消除处理 |
| `list-elimination-entries` | 会计分录的消除记录 |

### 销售/订单到现金（42 个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-customer` / `update-customer` / `get-customer` / `list-customers` | 客户信息的创建/更新/查询 |
| `add-quotation` / `update-quotation` / `get-quotation` / `list-quotations` | 报价的创建/更新/查询/提交 |
| `convert-quotation-to-so` | 报价转换为销售订单 |
| `add-sales-order` / `update-sales-order` / `get-sales-order` / `list-sales-orders` / `submit-sales-order` / `cancel-sales-order` | 销售订单的创建/更新/查询/提交 |
| `create-delivery-note` / `get-delivery-note` / `list-delivery-notes` / `submit-delivery-note` / `cancel-delivery-note` | 交货通知的创建/获取/列表/提交/取消 |
| `create-sales-invoice` / `update-sales-invoice` / `get-sales-invoice` / `list-sales-invoices` / `submit-sales-invoice` / `cancel-sales-invoice` | 发票的创建/更新/查询/提交/取消 |
| `create-credit-note` / `update-invoice-outstanding` | 信用通知的创建 |
| `add-sales-partner` / `list-sales-partners` | 销售合作伙伴的添加 |
| `add-recurring-invoice-template` / `update-recurring-invoice-template` / `list-recurring-invoice-templates` / `generate-recurring-invoices` | 定期发票模板管理 |
| `import-customers` | 客户信息的 CSV 导入 |
| `add-intercompany-account-map` / `list-intercompany-account-maps` | 公司间账户映射 |
| `create-intercompany-invoice` / `list-intercompany-invoices` / `cancel-intercompany-invoice` | 公司间发票的创建/列表/取消 |

### 采购/付款到现金（36 个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-supplier` / `update-supplier` / `get-supplier` / `list-suppliers` | 供应商信息的创建/更新/查询 |
| `add-material-request` / `submit-material-request` / `list-material-requests` | 物料需求的提交 |
| `add-rfq` / `submit-rfq` / `list-rfqs` | 询价请求的提交 |
| `add-supplier-quotation` / `list-supplier-quotations` / `compare-supplier-quotations` | 供应商报价的获取/比较 |
| `add-purchase-order` / `update-purchase-order` / `get-purchase-order` / `list-purchase-orders` / `submit-purchase-order` / `cancel-purchase-order` | 采购订单的创建/更新/查询/提交 |
| `create-purchase-receipt` / `get-purchase-receipt` / `list-purchase-receipts` / `submit-purchase-receipt` / `cancel-purchase-receipt` | 采购收据的创建/获取/列表/提交 |
| `create-purchase-invoice` / `update-purchase-invoice` / `get-purchase-invoice` / `list-purchase-invoices` / `submit-purchase-invoice` / `cancel-purchase-invoice` | 采购发票的创建/更新/查询/提交 |
| `create-debit-note` / `update-purchase-outstanding` / `add-landed-cost-voucher` | 调整分录的创建 |
| `import-suppliers` | 供应商信息的 CSV 导入 |

### 库存（38 个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-item` / `update-item` / `get-item` / `list-items` | 商品信息的添加/更新/查询 |
| `add-item-group` / `list-item-groups` | 商品组的管理 |
| `add-warehouse` / `update-warehouse` / `list-warehouses` | 仓库信息的添加/更新/列表 |
| `add-stock-entry` / `get-stock-entry` / `list-stock-entries` / `submit-stock-entry` / `cancel-stock-entry` | 库存记录的添加/更新/提交/取消 |
| `create-stock-ledger-entries` / `reverse-stock-ledger-entries` | 库存分类账的创建/反向更新 |
| `get-stock-balance` / `stock-balance-report` | 库存余额报告 |
| `stock-balance-report` | 库存余额报告 |
| `add-batch` / `list-batches` / `add-serial-number` / `list-serial-numbers` | 批量处理与序列号管理 |
| `add-price-list` / `add-item-price` / `get-item-price` | 价格信息的添加 |
| `add-pricing-rule` / `add-pricing-rule` | 价格规则的设置 |
| `add-stock-reconciliation` / `submit-stock-reconciliation` | 库存对账 |
| `revalue-stock` / `list-stock-revaluations` | 库存重新估值 |
| `check-reorder` | 订货处理的检查 |
| `import-items` | 商品信息的导入 |

### 计费与计量（22 个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-meter` / `update-meter` / `get-meter` / `list-meters` | 计量设备的添加/更新/查询 |
| `add-meter-reading` / `list-meter-readings` | 计量读数的获取 |
| `add-usage-event` / `add-usage-events-batch` | 使用情况的跟踪 |
| `add-rate-plan` / `update-rate-plan` / `get-rate-plan` / `list-rate-plans` | 计费计划的创建/更新 |
| `create-billing-period` / `run-billing` | 计费周期的创建 |
| `generate-invoices` | 发票的生成 |
| `add-billing-adjustment` | 计费调整 |
| `list-billing-periods` | 计费周期的列表 |
| `add-prepaid-credit` / `get-prepaid-balance` | 预付信用额的查询 |

### 高级会计（46 个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-revenue-contract` / `update-revenue-contract` / `get-revenue-contract` / `list-revenue-contracts` | 收入合同的创建/更新/查询 |
| `add-performance-obligation` / `list-performance-obligations` | 绩效义务的添加/管理 |
| `add-variable-consideration` / `list-variable-considerations` | 变动对价的设置 |
| `calculate-revenue-schedule` | 收入计划的计算 |
| `generate-revenue-entries` | 收入分录的生成 |
| `revenue-waterfall-report` | 收入报告 |
| `revenue-recognition-summary` | 收入确认报告 |
| `add-lease` / `update-lease` / `get-lease` / `list-leases` | 租赁合同的创建/更新/列表 |
| `classify-lease` | 租赁分类 |
| `calculate-rou-asset` / `calculate-lease-liability` | 租赁资产/负债的计算 |
| `generate-amortization-schedule` | 租赁摊销计划的生成 |
| `record-lease-payment` | 租赁付款的记录 |
| `lease-maturity-report` | 租赁报告 |
| `add-ic-transaction` / `update-ic-transaction` / `get-ic-transaction` | 公司间交易的创建/更新/查询 |
| `approve-ic-transaction` | 公司间交易的审批 |
| `add-transfer-price-rule` | 转移定价规则的设置 |
| `ic-reconciliation-report` | 公司间交易的对账报告 |
| `add-consolidation-group` / `list-consolidation-groups` | 合并组的添加 |
| `run-consolidation` | 合并处理的执行 |
| `generate-elimination-entries` | 合并分录的生成 |
| `add-currency-translation` | 货币转换的添加 |
| `consolidation-trial-balance-report` | 合并报表 |
| `consolidation-summary` | 合并报告 |

### 人力资源与工资单（50 个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-employee` / `update-employee` / `get-employee` / `list-employees` | 员工信息的创建/更新/查询 |
| `add-department` / `list-departments` / `add-designation` / `list-designations` | 部门信息的添加/列表 |
| `add-leave-type` / `list-leave-types` / `add-leave-allocation` / `get-leave-balance` | 休假类型的添加/查询/余额查询 |
| `add-leave-application` / `approve-leave` / `reject-leave` / `list-leave-applications` | 休假申请的提交/审批/拒绝 |
| `mark-attendance` / `bulk-mark-attendance` / `list-attendance` | 出勤情况的标记/批量标记 |
| `add-expense-claim` / `submit-expense-claim` / `approve-expense-claim` / `reject-expense-claim` | 费用报销的提交/审批/拒绝 |
| `record-lifecycle-event` / `hr-status` / `update-expense-claim-status` | 员工生命周期事件的记录 |
| `add-salary-component` / `list-salary-components` / `add-salary-structure` | 薪资构成的添加 |
| `add-salary-assignment` / `list-salary-assignments` | 薪资分配的添加 |
| `add-income-tax-slab` / `update-fica-config` / `update-futa-suta-config` | 税务配置的更新 |
| `create-payroll-run` / `generate-salary-slips` | 工资单的生成 |
| `submit-payroll-run` / `cancel-payroll-run` | 工资单处理的提交 |
| `get-salary-slip` / `list-salary-slips` | 工资单的获取 |
| `generate-w2-data` | W-2 表单的生成 |
| `add-garnishment` / `update-garnishment` / `get-garnishment` / `list-garnishments` | 扣款信息的添加/更新/查询 |
| `payroll-status` | 工资单状态查询 |

### 模块管理（10 个操作）

| 操作 | 描述 |
| `install-module` | 从 GitHub 安装模块（`--module-name <模块名称>`） |
| `remove-module` | 卸载已安装的模块（`--module-name <模块名称>` |
| `update-modules` | 更新所有模块或特定模块 |
| `list-modules` | 查看所有已安装的模块 |
| `available-modules` | 浏览模块目录（`--category`、`--search`） |
| `module-status` | 模块的详细状态查询（`--module-name <模块名称>` |
| `search-modules` | 根据关键词搜索模块（`--search <查询内容>` |
| `rebuild-action-cache` | 重建操作路由缓存 |
| `list-profiles` | 浏览企业入职配置文件 |
| `onboard` | 为特定企业类型自动安装模块（`--profile <企业名称>`）

### 快速命令参考

| 用户输入 | 操作 |
|-----------|--------|
| "Set up my company" | `setup-company` | 设置公司信息 |
| "Show trial balance" | `trial-balance` | 查看试算平衡表 |
| "Create an invoice" | `create-sales-invoice` → `submit-sales-invoice` | 创建发票并提交 |
| "Record a payment" | `add-payment` → `submit-payment` | 提交付款信息 |
| "Install CRM" | `install-module --module-name erpclaw-growth` | 安装 CRM 模块 |
| "Set up for retail" | `onboard --profile retail` | 为零售业务配置系统 |
| "Add employee" | `add-employee` | 添加员工信息 |
| "Run payroll" | `create-payroll-run` → `generate-salary-slips` → `submit-payroll-run` | 运行工资单处理 |
| "Apply for leave" | `add-leave-application` | 申请休假 |
| "Generate W-2s" | `generate-w2-data` | 生成 W-2 表单 |

注意：所有以 `submit-*`、`cancel-*`、`approve-*`、`reject-*`、`run-elimination`、`run-consolidation`、`restore-database`、`close-fiscal-year`、`initialize-database --force`、`install-module`、`remove-module`、`onboard` 开头的命令会立即执行。所有以 `add-*`、`get-*`、`list-*`、`update-*` 结尾的操作也会立即执行。

## 技术细节（三级）

### 架构
- **路由器**：`scripts/db_query.py` 负责将请求分发到 14 个核心业务模块和已安装的模块。
- **核心业务模块**：包括设置、元数据、总账、日记账、支付、税务、报告、销售、采购、库存、计费、高级会计、人力资源、工资单等。
- **模块系统**：通过 GitHub 安装的扩展模块存储在 `~/.openclaw/erpclaw/modules/` 目录下。
- **数据库**：使用单个 SQLite 数据库（位于 `~/.openclaw/erpclaw/data.sqlite`）。
- **共享库**：`~/.openclaw/erpclaw/lib/erpclaw_lib/`（通过 `initialize-database` 命令安装）。
- **数据库表结构**：共 151 张表（149 张核心表 + 2 张模块系统相关表）。货币类型为 TEXT（Decimal），ID 类型为 TEXT（UUID4）。总账分录是不可篡改的。
- **命令格式**：`scripts/db_query.py --action <操作名称> [--参数 ...]`