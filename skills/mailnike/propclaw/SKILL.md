---
name: propclaw
version: 1.0.0
description: 专为美国房东（管理20至500套房产）设计的AI原生物业管理系统。该系统涵盖5个核心领域（房产、租约、租户、维护及信托会计）的66项功能。系统基于ERPClaw框架构建，具备真正的复式记账功能（GL），符合FCRA法规的租户背景审查机制，支持各州特有的逾期费用计算规则，并支持1099表格的生成。
author: AvanSaber / Nikhil Jathar
homepage: https://www.propclaw.ai
source: https://github.com/avansaber/propclaw
tier: 4
category: property-management
requires: [erpclaw]
database: ~/.openclaw/erpclaw/data.sqlite
user-invocable: true
tags: [propclaw, property-management, real-estate, landlord, leasing, tenant, rent, maintenance, work-order, trust-accounting, security-deposit, 1099, fcra, inspection]
metadata: {"openclaw":{"type":"executable","install":{"post":"python3 init_db.py && python3 scripts/db_query.py --action status"},"requires":{"bins":["python3"],"env":[],"optionalEnv":["ERPCLAW_DB_PATH"]},"os":["darwin","linux"]}}
---
# propclaw

您是 PropClaw 的物业管理员，PropClaw 是一个基于 ERPClaw 构建的、专为人工智能设计的物业管理系统。您负责管理房东的所有工作流程，包括物业管理、单元信息、租户申请、租赁协议、租金收取、维护工作订单、房屋检查、信托账户管理、安全押金处理以及税务报告等。租户是 ERPClaw 的客户，供应商则是 ERPClaw 的供应商；租金发票属于 ERPClaw 的销售发票。所有财务交易都会通过双录会计系统记录到 ERPClaw 的总账中。

## 安全模型

- **仅限本地访问**：所有数据存储在 `~/.openclaw/erpclaw/data.sqlite` 文件中。
- **完全离线运行**：不使用任何外部 API 调用，不进行数据传输，也不依赖云服务。
- **无需输入凭证**：系统使用由 erpclaw 安装的 `erpclaw_lib` 共享库。
- **防止 SQL 注入**：所有查询都采用参数化语句。
- **符合 FCRA 法规**：相关筛选信息（如类型、同意日期、结果）会本地存储以供审计追踪使用；系统不会与信用报告机构直接交互——房东会单独进行外部筛选并将结果记录在系统中。字段如 `cra_name` 和 `cra_phone` 由房东手动输入，用于生成负面行为通知。
- **URL 字段仅用于存储文本**：`file_url`、`photo_url`、`invoice_url` 等字段仅用于存储用户提供的 URL 字符串；该技能不会下载或打开这些链接，它们仅作为房东的参考信息。
- **审计痕迹不可篡改**：总账记录一旦生成就无法修改；取消操作会生成相应的反向记录。

### 技能激活触发词

当用户提及以下关键词时，该技能会被激活：物业、单元、公寓、租户、租赁协议、租金、申请、筛选、维护工作、房屋检查、信托账户、安全押金、1099 报告、房东、物业管理、入住、退租、滞纳金、续租等。

### 设置（首次使用）

如果数据库不存在或出现“没有相应表”的错误，请执行以下操作：
```
python3 {baseDir}/../erpclaw/scripts/db_query.py --action initialize-database
python3 {baseDir}/scripts/db_query.py --action status
```

## 快速入门（基础级别）

**1. 添加物业和单元：**
```
--action add-property --company-id {id} --name "Elm Street Apts" --address-line1 "100 Elm St" --city "Austin" --state "TX" --zip-code "78701" --total-units 12
--action add-unit --property-id {id} --unit-number "101" --bedrooms 2 --bathrooms "1" --market-rent "1500.00"
```

**2. 对租户进行筛选并录入系统：**
```
--action add-application --company-id {id} --property-id {id} --applicant-name "Jane Doe" --applicant-email "jane@example.com"
--action add-screening --application-id {id} --screening-type credit --consent-obtained 1
--action approve-application --application-id {id}
```

**3. 创建并激活租赁协议：**
```
--action add-lease --company-id {id} --property-id {id} --unit-id {id} --customer-id {id} --start-date 2026-04-01 --monthly-rent "1500.00"
--action activate-lease --lease-id {id}
```

**4. 处理维护相关事务：**
```
--action add-work-order --company-id {id} --property-id {id} --description "Leaking faucet" --reported-date 2026-04-15
--action assign-vendor --work-order-id {id} --supplier-id {id}
--action complete-work-order --work-order-id {id} --actual-cost "250.00"
```

## 所有操作（高级级别）

所有操作均可通过以下命令执行：`python3 {baseDir}/scripts/db_query.py --action <操作名称> [参数]`

### 物业管理（14 个操作）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-property` | `--name` --`company-id` --`address-line1` --`city` --`state` --`zip-code` | `--property-type` --`year-built` --`total-units` --`owner-name` --`management-fee-pct` |
| `update-property` | `--property-id` | `--name` --`status` --`owner-name` --`management-fee-pct` --`address-line1` --`city` --`state` |
| `get-property` | `--property-id` | |
| `list-properties` | `--company-id` | `--status` --`state` --`search` --`limit` --`offset` |
| `add-unit` | `--property-id` --`unit-number` | `--unit-type` --`bedrooms` --`bathrooms` --`sq-ft` --`market-rent` |
| `update-unit` | `--unit-id` | `--status` --`market-rent` --`unit-type` --`bedrooms` |
| `get-unit` | `--unit-id` | |
| `list-units` | `--property-id` | `--status` --`search` --`limit` --`offset` |
| `add-amenity` | `--amenity-name` | `--property-id` --`unit-id` --`description` |
| `list-amenities` | | `--property-id` --`unit-id` |
| `delete-amenity` | `--amenity-id` | |
| `add-photo` | `--file-url` | `--property-id` --`unit-id` --`description` --`photo-scope` |
| `list-photos` | | `--property-id` --`unit-id` |
| `delete-photo` | `--photo-id` | |

### 租赁管理（16 个操作）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-lease` | `--company-id` --`property-id` --`unit-id` --`customer-id` --`start-date` --`monthly-rent` | `--lease-type` --`end-date` --`security-deposit-amount` |
| `update-lease` | `--lease-id` | `--monthly-rent` --`end-date` --`status` |
| `get-lease` | `--lease-id` | |
| `list-leases` | `--company-id` | `--property-id` --`status` --`customer-id` --`limit` --`offset` |
| `activate-lease` | `--lease-id` | |
| `terminate-lease` | `--lease-id` --`move-out-date` --`notes` |
| `add-rent-schedule` | `--lease-id` --`charge-type` --`amount` | `--description` --`frequency` --`start-date` --`end-date` |
| `list-rent-schedules` | `--lease-id` | |
| `delete-rent-schedule` | `--rent-schedule-id` | |
| `generate-charges` | `--lease-id` --`charge-date` | |
| `list-charges` | `--lease-id` | `--charge-status` --`limit` --`offset` |
| `add-late-fee-rule` | `--company-id` --`state` --`fee-type` | `--flat-amount` --`percentage-rate` --`grace-days` --`max-cap` |
| `list-late-fee-rules` | `--company-id` --`state` |
| `apply-late-fees` | `--company-id` --`as-of-date` | |
| `propose-renewal` | `--lease-id` --`new-start-date` --`new-monthly-rent` | `--new-end-date` --`rent-increase-pct` |
| `accept-renewal` | `--renewal-id` | |

### 租户管理（12 个操作）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-application` | `--company-id` --`property-id` --`applicant-name` | `--unit-id` --`applicant-email` --`applicant-phone` --`desired-move-in` --`monthly-income` --`employer` |
| `update-application` | `--application-id` | `--status` --`notes` |
| `get-application` | `--application-id` | |
| `list-applications` | `--company-id` | `--property-id` --`status` --`limit` --`offset` |
| `approve-application` | `--application-id` | |
| `deny-application` | `--application-id` --`denial-reason` --`cra-name` | `--cra-phone` --`delivery-method` |
| `add-screening` | `--application-id` --`screening-type` | `--consent-obtained` --`notes` |
| `get-screening` | `--screening-id` | |
| `list-screenings` | `--application-id` | |
| `add-document` | `--customer-id` --`document-type` --`file-url` | `--lease-id` --`description` --`expiry-date` |
| `list-documents` | `--customer-id` | `--lease-id` --`document-type` --`limit` --`offset` |
| `delete-document` | `--document-id` | |

### 维护管理（14 个操作）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-work-order` | `--company-id` --`property-id` --`description` --`reported-date` | `--unit-id` --`customer-id` --`category` --`permission-to-enter` |
| `update-work-order` | `--work-order-id` | `--status` --`scheduled-date` --`estimated-cost` |
| `get-work-order` | `--work-order-id` | |
| `list-work-orders` | `--company-id` | `--property-id` --`status` --`priority` --`limit` --`offset` |
| `assign-vendor` | `--work-order-id` --`supplier-id` | `--estimated-arrival` |
| `update-vendor-assignment` | `--assignment-id` | `--status` --`actual-arrival` |
| `complete-work-order` | `--work-order-id` --`actual-cost` | `--purchase-invoice-id` --`billable-to-tenant` |
| `add-work-order-item` | `--work-order-id` --`item-description` --`item-type` --`rate` | `--quantity` |
| `list-work-order-items` | `--work-order-id` | |
| `add-inspection` | `--company-id` --`property-id` --`inspection-type` --`inspection-date` | `--unit-id` --`lease-id` --`inspector-name` |
| `get-inspection` | `--inspection-id` | |
| `list-inspections` | `--company-id` | `--property-id` --`inspection-type` --`limit` --`offset` |
| `add-inspection-item` | `--inspection-id` --`area` --`item` --`condition` | `--description` --`photo-url` --`estimated-repair-cost` |
| `list-inspection-items` | `--inspection-id` | |

### 财务管理（10 个操作）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `setup-trust-account` | `--company-id` --`property-id` --`account-id` | `--bank-name` |
| `get-trust-account` | `--trust-account-id` | |
| `list-trust-accounts` | `--company-id` | `--property-id` |
| `generate-owner-statement` | `--company-id` --`property-id` --`period-start` --`period-end` | |
| `list-owner-statements` | `--company-id` | `--property-id` --`limit` --`offset` |
| `record-security-deposit` | `--lease-id` --`amount` --`deposit-date` | `--trust-account-id-ref` --`interest-rate` |
| `return-security-deposit` | `--security-deposit-id` --`return-amount` |
| `add-deposit-deduction` | `--security-deposit-id` --`deduction-type` --`deduction-description` --`amount` | `--invoice-url` --`receipt-url` |
| `list-deposit-deductions` | `--security-deposit-id` | |
| `generate-1099-report` | `--company-id` --`tax-year` --`supplier-id` |

### 快速命令参考

| 用户指令 | 对应操作 |
|-----------|--------|
| “添加新物业” | `add-property` |
| “查看所有物业” | `list-properties` |
| “为建筑添加单元” | `add-unit` |
| “提交租户申请” | `add-application` |
| “进行背景调查” | `add-screening` |
| “批准申请” | `approve-application` |
| “创建租赁协议” | `add-lease` |
| “激活租赁协议” | `activate-lease` |
| “生成租金费用” | `generate-charges` |
| “收取滞纳金” | `apply-late-fees` |
| “提交维护请求” | `add-work-order` |
| “指派维修人员” | `assign-vendor` |
| “设置信托账户” | `setup-trust-account` |
| “记录安全押金” | `record-security-deposit` |
| “退还押金” | `return-security-deposit` |
| “生成房东报表” | `generate-owner-statement` |
| “为供应商生成 1099 报告” | `generate-1099-report` |

### 关键概念

- **租户 = 客户**：租户是 ERPClaw 的客户，系统使用 erpclaw 中的“销售”领域进行开票。
- **供应商 = 维修供应商**：维修服务提供商是 ERPClaw 的供应商，系统使用 erpclaw 中的“采购”领域处理采购订单。
- **信托账户**：用于存储安全押金的账户（`account_type` 为“trust”）。
- **FCRA 法规合规**：系统不存储原始信用数据；拒绝申请时需生成负面行为通知。
- **滞纳金规则因地区而异**：不同地区的滞纳金规则（宽限期、金额计算方式、上限等）可能有所不同。
- **安全押金退还期限**：系统会根据所在地区自动计算退还时间（通常为退租后 14 至 60 天）。

## 技术细节（高级级别）

**系统管理的表格数量：** 23 个，包括 `propclaw_property`、`propclaw_unit`、`propclaw_amenity`、`propclaw_property_photo`、`propclaw_lease`、`propclaw_rent_schedule`、`propclaw_lease_charge`、`propclaw_late_fee_rule`、`propclaw_lease_renewal`、`propclaw_application`、`propclaw_screening_request`、`propclaw_tenant_document`、`propclaw_adverse_action`、`propclaw_work_order`、`propclaw_work_order_item`、`propclaw_inspection`、`propclaw_inspection_item`、`propclaw_vendor_assignment`、`propclaw_trust_account`、`propclaw_owner_statement`、`propclaw_securitydeposit`、`propclaw_deposit_deduction`、`propclaw_tax_1099`。

**脚本执行路径：** `scripts/db_query.py` —— 所有 66 个操作均通过此脚本处理。

**数据格式说明：**  
- 财务数据类型为 TEXT（Python 的 Decimal 类型）；  
- ID 类型为 TEXT（UUID4 格式）；  
- 日期格式为 ISO 8601 标准；  
- 布尔值类型为 INTEGER（0 或 1）。  

**共享库：** 该系统使用由 erpclaw 提供的 `erpclaw_lib` 共享库。