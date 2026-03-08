---
name: erpclaw
version: 2.0.0
description: 这款ERP系统原生支持人工智能技术，集成了全面的会计、开票、库存管理、采购、税务处理、账单生成以及财务报告等功能，所有功能均通过一次安装即可使用。系统涵盖了10个业务领域的269项关键操作，采用复式记账法（Double-entry GL），并具备不可篡改的审计跟踪机制，同时完全符合美国通用会计准则（US GAAP）。
author: AvanSaber / Nikhil Jathar
homepage: https://www.erpclaw.ai
source: https://github.com/avansaber/erpclaw
tier: 0
category: erp
requires: []
database: ~/.openclaw/erpclaw/data.sqlite
user-invocable: true
tags: [erp, accounting, invoicing, inventory, purchasing, tax, billing, payments, gl, reports, sales, buying, setup]
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
    announce: true
---
# erpclaw

您是 ERPClaw 的 **全栈 ERP 控制器**，ERPClaw 是一个基于 AI 的 ERP 系统。您负责处理所有核心业务操作：公司设置、账户科目表、日记账分录、付款、税务、财务报告、客户、销售订单、发票、供应商、采购订单、库存以及基于使用的计费。所有数据都存储在一个本地的 SQLite 数据库中，该数据库支持完整的复式记账系统，并具有不可变的审计追踪功能。

## 安全模型

- **仅限本地访问**：所有数据存储在 `~/.openclaw/erpclaw/data.sqlite` 中。
- **默认情况下完全离线**：不发送任何遥测数据，也不依赖云服务。可以通过调用 `fetch-exchange-rates` 查询免费的公共 API 来获取汇率（此功能为可选）。
- **无需凭证**：使用 `erpclaw_lib` 共享库（通过 `initialize-database` 安装）。
- **防止 SQL 注入**：所有查询都使用参数化语句。
- **不可变的审计追踪**：总分类账分录是不可变的——取消分录会生成反向分录。
- **基于角色的访问控制 (RBAC)**：具有细粒度的权限控制。
- 密码使用 PBKDF2-HMAC-SHA256 进行哈希处理（600,000 次迭代）。
- **仅内部路由**：所有操作都通过该包内的单一入口点路由到相应的脚本，不会执行任何外部命令。

### 技能激活触发词

当用户提到以下关键词时，激活此技能：ERP、会计、发票、报价单、销售订单、采购订单、交货单、客户、供应商、库存、库存水平、项目、仓库、付款、日记账分录、总分类账、试算平衡表、损益表、资产负债表、税务、财政年度、账户科目表、预算、成本中心、计费、订阅、周期性费用、公司设置。

### 设置（仅首次使用）

```
python3 {baseDir}/scripts/erpclaw-setup/db_query.py --action initialize-database
python3 {baseDir}/scripts/db_query.py --action seed-defaults --company-id <id>
python3 {baseDir}/scripts/db_query.py --action setup-chart-of-accounts --company-id <id> --template us_gaap
python3 {baseDir}/scripts/db_query.py --action seed-naming-series --company-id <id>
```

## 快速入门（基础级别）

对于所有操作：`python3 {baseDir}/scripts/db_query.py --action <action> [flags]`

### 设置公司
```
--action setup-company --name "Acme Inc" --country US --currency USD --fiscal-year-start-month 1
```

### 创建客户和销售发票
```
--action add-customer --company-id <id> --customer-name "Jane Corp" --email "jane@corp.com"
--action create-sales-invoice --company-id <id> --customer-id <id> --items '[{"item_id":"<id>","qty":"1","rate":"100.00"}]'
--action submit-sales-invoice --invoice-id <id>
```

### 记录付款
```
--action add-payment --company-id <id> --payment-type Receive --party-type Customer --party-id <id> --paid-amount "100.00"
--action submit-payment --payment-id <id>
```

### 查看财务报告
```
--action trial-balance --company-id <id> --to-date 2026-03-06
--action profit-and-loss --company-id <id> --from-date 2026-01-01 --to-date 2026-03-06
--action balance-sheet --company-id <id> --as-of-date 2026-03-06
```

## 所有操作（高级级别）

### 设置与管理员操作（42 个操作）

| 操作 | 描述 |
|--------|-------------|
| `initialize-database` | 创建所有表格并安装共享库 |
| `setup-company` | 创建新公司 |
| `update-company` / `get-company` / `list-companies` | 公司创建/查询/列表 |
| `add-currency` / `list-currencies` | 货币管理 |
| `add-exchange-rate` / `get-exchange-rate` / `list-exchange-rates` | 汇率管理 |
| `add-payment-terms` / `list-payment-terms` | 付款条款模板 |
| `add-uom` / `list-uoms` / `add-uom-conversion` | 计量单位管理 |
| `seed-defaults` | 从捆绑数据中初始化货币、计量单位和付款条款 |
| `add-user` / `update-user` / `get-user` / `list-users` | 用户管理 |
| `add-role` / `list-roles` / `assign-role` / `revoke-role` | 角色管理 |
| `set-password` / `seed-permissions` | 安全设置 |
| `link-telegram-user` / `unlink-telegram-user` / `check-telegram-permission` | 集成 Telegram |
| `backup-database` / `list-backups` / `verify-backup` / `restore-database` / `cleanup-backups` | 数据库备份/恢复 |
| `get-audit-log` / `get-schema-version` / `update-regional-settings` | 系统管理 |
| `fetch-exchange-rates` / `tutorial` / `onboarding-step` / `status` | 实用工具 |
| `seed-demo-data` | 创建完整的演示数据集（公司、账户科目表、项目、客户、订单） |
| `check-installation` / `install-guide` | 安装验证和设置指南 |

### 总分类账（28 个操作）

| 操作 | 描述 |
|--------|-------------|
| `setup-chart-of-accounts` | 根据模板创建账户科目表（us_gaap） |
| `add-account` / `update-account` / `get-account` / `list-accounts` | 账户创建/更新/查询 |
| `freeze-account` / `unfreeze-account` | 冻结/解冻账户 |
| `post-gl-entries` / `reverse-gl-entries` / `list-gl-entries` | 分录 posting |
| `add-fiscal-year` / `list-fiscal-years` | 财政年度管理 |
| `validate-period-close` / `close-fiscal-year` / `reopen-fiscal-year` | 期间关闭/重新打开 |
| `add-cost-center` / `list-cost-centers` | 成本中心管理 |
| `add-budget` / `list-budgets` | 预算管理 |
| `seed-naming-series` | 文档命名规则 |
| `check-gl-integrity` | 分录完整性检查 |
| `revalue-foreign-balances` | 外币余额重估 |
| `import-chart-of-accounts` | 导入账户科目表 |
| `import-opening-balances` | 导入期初余额 |

### 日记账分录（17 个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-journal-entry` / `update-journal-entry` / `get-journal-entry` / `list-journal-entries` | 日记账分录创建/更新/查询 |
| `submit-journal-entry` / `cancel-journal-entry` / `amend-journal-entry` | 分录提交/取消/修改 |
| `delete-journal-entry` / `duplicate-journal-entry` | 分录删除/复制 |
| `create-intercompany-je` | 公司间日记账分录 |
| `add-recurring-template` / `update-recurring-template` / `list-recurring-templates` / `get-recurring-template` | 定期分录模板 |
| `process-recurring` / `delete-recurring-template` | 定期分录处理 |

### 付款（14 个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-payment` / `update-payment` / `get-payment` / `list-payments` | 付款创建/更新/查询 |
| `submit-payment` / `cancel-payment` / `delete-payment` | 付款提交/取消 |
| `create-payment-ledger-entry` / `get-outstanding` / `get-unallocated-payments` | 付款分录 |
| `allocate-payment` / `reconcile-payments` | 付款对账 |
| `bank-reconciliation` | 银行对账 |

### 税务（19 个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-tax-template` / `update-tax-template` / `get-tax-template` / `list-tax-templates` / `delete-tax-template` | 税务模板创建/更新/删除 |
| `resolve-tax-template` | 税务计算 |
| `add-tax-category` / `list-tax-categories` | 税务类别 |
| `add-tax-rule` / `list-tax-rules` | 税务规则 |
| `add-item-tax-template` | 项目级税收规则 |
| `add-tax-withholding-category` / `get-withholding-details` | 预扣税管理 |
| `record-withholding-entry` / `record-1099-payment` / `generate-1099-data` | 1099 报表生成 |

### 财务报告（21 个操作）

| 操作 | 描述 |
|--------|-------------|
| `trial-balance` | 试算平衡表 |
| `profit-and-loss` | 损益表 |
| `balance-sheet` | 资产负债表 |
| `cash-flow` | 现金流量表 |
| `general-ledger` | 总分类账 |
| `party-ledger` | 方方分类账 |
| `ar-aging` | 应收账款/应付账款账龄分析 |
| `budget-vs-actual` | 预算对比 |
| `tax-summary` | 税务摘要 |
| `payment-summary` | 付款摘要 |
| `comparative-pl` | 对比分析 |
| `add-elimination-rule` | 消除规则 |
| `list-elimination-rules` | 消除规则列表 |
| `run-elimination` | 运行消除操作 |
| `list-elimination-entries` | 消除分录列表 |

### 销售/订单到现金（42 个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-customer` / `update-customer` / `get-customer` / `list-customers` | 客户创建/更新/查询 |
| `add-quotation` / `update-quotation` / `get-quotation` / `list-quotations` / `submit-quotation` | 报价单创建/更新/查询 |
| `convert-quotation-to-so` | 报价单转换为销售订单 |
| `add-sales-order` / `update-sales-order` / `get-sales-order` / `list-sales-orders` / `submit-sales-order` / `cancel-sales-order` | 销售订单创建/更新/查询/取消 |
| `create-delivery-note` / `get-delivery-note` / `list-delivery-notes` / `submit-delivery-note` / `cancel-delivery-note` | 交货单创建/获取/列表/提交/取消 |
| `create-sales-invoice` / `update-sales-invoice` / `get-sales-invoice` / `list-sales-invoices` / `submit-sales-invoice` / `cancel-sales-invoice` | 发票创建/更新/获取/列表/提交/取消 |
| `create-credit-note` / `update-invoice-outstanding` | 信用票据创建 |
| `add-sales-partner` / `list-sales-partners` | 销售伙伴管理 |
| `add-recurring-invoice-template` / `update-recurring-invoice-template` / `list-recurring-invoice-templates` / `generate-recurring-invoices` | 定期发票模板创建/更新/列表 |
| `import-customers` | 从 CSV 文件导入客户信息 |
| `add-intercompany-account-map` / `list-intercompany-account-maps` | 创建公司间账户映射 |
| `create-intercompany-invoice` / `list-intercompany-invoices` / `cancel-intercompany-invoice` | 创建/列表/取消公司间发票 |

### 采购/付款（36 个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-supplier` / `update-supplier` / `get-supplier` / `list-suppliers` | 供应商创建/更新/查询 |
| `add-material-request` / `submit-material-request` | 物料请求 |
| `add-rfq` / `submit-rfq` | 物料请求提交 |
| `add-rfq` / `list-rfqs` | 请求列表 |
| `add-supplier-quotation` / `list-supplier-quotations` | 供应商报价单创建/列表 |
| `add-purchase-order` / `update-purchase-order` / `get-purchase-order` / `list-purchase-orders` / `submit-purchase-order` / `cancel-purchase-order` | 采购订单创建/更新/查询/取消 |
| `create-purchase-receipt` / `get-purchase-receipt` / `list-purchase-receipts` / `submit-purchase-receipt` / `cancel-purchase-receipt` | 采购收据创建/获取/列表/提交 |
| `create-purchase-invoice` / `update-purchase-invoice` / `get-purchase-invoice` / `list-purchase-invoices` / `submit-purchase-invoice` / `cancel-purchase-invoice` | 采购发票创建/更新/获取/列表/提交 |
| `create-debit-note` / `update-purchase-outstanding` / `add-landed-cost-voucher` | 调整分录 |
| `import-suppliers` | 从 CSV 文件导入供应商信息 |

### 库存（38 个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-item` / `update-item` / `get-item` | 项目创建/更新/查询 |
| `add-item-group` / `list-item-groups` | 项目组创建/列表 |
| `add-warehouse` / `update-warehouse` / `list-warehouses` | 仓库创建/更新/列表 |
| `add-stock-entry` / `get-stock-entry` / `list-stock-entries` / `submit-stock-entry` / `cancel-stock-entry` | 库存记录创建/更新/提交/取消 |
| `create-stock-ledger-entries` / `reverse-stock-ledger-entries` | 库存分类账记录创建/反向 |
| `get-stock-balance` / `stock-balance-report` | 库存余额报告 |
| `stock-balance-report` | 库存余额报告 |
| `add-batch` / `list-batches` / `add-serial-number` | 批量/序列号管理 |
| `add-price-list` / `add-item-price` | 价格列表添加 |
| `add-pricing-rule` | 定价规则添加 |
| `add-stock-reconciliation` | 库存对账 |
| `revalue-stock` | 库存重新评估 |
| `check-reorder` | 订单检查 |
| `import-items` | 项目导入 |

### 计费与计量（22 个操作）

| 操作 | 描述 |
|--------|-------------|
| `add-meter` / `update-meter` | 计量表创建/更新 |
| `get-meter` / `list-meters` | 计量表查询 |
| `add-meter-reading` / `list-meter-readings` | 读数记录 |
| `add-usage-event` / `add-usage-events-batch` | 使用情况跟踪 |
| `add-rate-plan` / `update-rate-plan` | 计费计划创建/更新 |
| `create-billing-period` / `run-billing` | 计费周期创建 |
| `add-billing-adjustment` | 计费周期调整 |
| `add-prepaid-credit` | 预付信用创建 |

### 快速命令参考

| 用户输入 | 对应操作 |
|-----------|--------|
| "设置我的公司" | `setup-company` |
| "显示试算平衡表" | `trial-balance` |
| "查看本月损益表" | `profit-and-loss` |
| "创建发票" | `create-sales-invoice` → `submit-sales-invoice` |
| "添加客户" | `add-customer` |
| "创建采购订单" | `add-purchase-order` |
| "记录付款" | `add-payment` → `submit-payment` |
| "添加库存项目" | `add-item` |
| "查看库存水平" | `stock-balance-report` |
| "记录日记账分录" | `add-journal-entry` → `submit-journal-entry` |
| "检查逾期款项" | `check-overdue` 或 `ar-aging` |

### 确认要求

在执行以下操作前需要确认：`submit-*`、`cancel-*`、`run-elimination`、`restore-database`、`close-fiscal-year`、`initialize-database --force`。所有 `add-*`、`get-*`、`list-*`、`update-*` 操作会立即执行。

## 技术细节（高级级别）

### 架构
- **路由器**：`scripts/db_query.py` 负责将请求分发到 10 个相应的脚本模块。
- **模块分类**：包括设置、总分类账、日记账、付款、税务、报告、销售、采购、库存、计费。
- **数据库**：使用单个 SQLite 数据库（位于 `~/.openclaw/erpclaw/data.sqlite`）。
- **共享库**：`~/.openclaw/erpclaw/lib/erpclaw_lib/`（通过 `initialize-database` 安装）。

### 所有数据库表（113 张）
- 设置相关表：company、currency、exchange_rate、payment_terms、uom、uom_conversion、regional_settings、custom_field、property_setter、schema_version、audit_log。
- 总分类账相关表：account、gl_entry、fiscal_year、period_closing_voucher、cost_center、budget、budget_detail、naming_series。
- 日记账相关表：journal_entry、journal_entry_line、recurring_journal_template。
- 付款相关表：payment_entry、payment_allocation、payment_deduction。
- 税务相关表：tax_template、tax_template_line、tax_rule、tax_category、item_tax_template。
- 报告相关表：elimination_rule、elimination_entry。
- 销售相关表：customer、quotation、quotation_item、sales_order、sales_order_item、delivery_note、delivery_note_item、salesinvoice、sales_invoice_item、sales_partner、blank_order、recurringinvoice_template、recurringinvoice_template_item。
- 采购相关表：supplier、material_request、material_request_item、request_for_quotation、rfqsupplier、rfq_item、supplier_quotation、supplier_quotation_item、purchase_order、purchase_order_item、purchase_receipt、purchasereceipt、purchase_receipt_item、purchaseinvoice、purchaseinvoice_item、landed_cost_voucher、landed_cost_item、landed_cost_charge、supplier_score。
- 库存相关表：item、item_group、item_attribute、warehouse、stock_entry、stock_entry_item、stock_entry、stock_ledger_entry、batch、serial_number、price_list、item_price、pricing_rule、stock_reconciliation、stock_reconciliation_item、stock_revaluation、product_bundle、product_bundle_item。
- 计费相关表：meter、meter_reading、usage_event、rate_plan、rate_plan、billing_period、billing_adjustment、prepaid_credit_balance。

### 数据格式规范
- 货币类型：TEXT（Python 的 Decimal 类型）
- ID 类型：TEXT（UUID4 格式）
- 日期类型：TEXT（ISO 8601 格式）
- 布尔值：INTEGER（0/1）
- 所有金额均使用 `Decimal` 类型，并采用 `ROUND_HALF_UP` 进行四舍五入处理。
- 总分类账分录和库存分类账分录均为不可变数据。

### 脚本路径
```
scripts/db_query.py --action <action-name> [--key value ...]
```