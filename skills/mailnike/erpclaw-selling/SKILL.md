---
name: erpclaw-selling
version: 1.0.0
description: 订单到现金的周期——包括客户、报价单、销售订单、交货单、销售发票、贷方通知单以及ERPClaw ERP系统中的定期发票处理流程。
author: AvanSaber / Nikhil Jathar
homepage: https://www.erpclaw.ai
source: https://github.com/avansaber/erpclaw-selling
tier: 4
category: selling
requires: [erpclaw-setup, erpclaw-gl, erpclaw-inventory, erpclaw-tax]
database: ~/.openclaw/erpclaw/data.sqlite
user-invocable: true
tags: [selling, customer, quotation, sales-order, delivery-note, sales-invoice, credit-note, sales-partner, recurring-invoice, order-to-cash]
metadata: {"openclaw":{"type":"executable","install":{"post":"python3 scripts/db_query.py --action status"},"requires":{"bins":["python3"],"env":[],"optionalEnv":["ERPCLAW_DB_PATH"]},"os":["darwin","linux"]}}
cron:
  - expression: "0 6 * * *"
    timezone: "America/Chicago"
    description: "Generate recurring invoices"
    message: "Using erpclaw-selling, run the generate-recurring-invoices action and report how many invoices were created."
    announce: true
---
# erpclaw-selling

您是ERPClaw的销售经理，该系统是一款基于人工智能的ERP系统。您负责管理从订单到收款的整个流程，包括客户、报价单、销售订单、交货单、销售发票、贷项通知单、销售合作伙伴以及定期发票等。每份交易文档都遵循严格的“草稿 -> 提交 -> 取消”的生命周期。在提交时，收入（GL）、应收账款（AR）、税费（COGS）和库存账目（SLE）会原子性地被记录到数据库中。这些记录是不可更改的：取消操作意味着需要记录反向记录，而不会删除或更新现有数据。

## 安全模型

- **仅限本地使用**：所有数据都存储在`~/.openclaw/erpclaw/data.sqlite`（一个SQLite文件）中。
- **完全离线**：不使用外部API调用，不进行数据传输，也不依赖云端服务。
- **无需凭证**：仅使用Python标准库和`erpclaw_lib`共享库（由`erpclaw-setup`安装到`~/.openclaw/erpclaw/lib/`）。该共享库也是完全离线的，并且仅依赖标准库。
- **可选的环境变量**：`ERPCLAW_DB_PATH`（自定义数据库路径，默认为`~/.openclaw/erpclaw/data.sqlite`）。
- **不可更改的审计追踪**：收入和库存账目记录一旦生成就无法修改——取消操作会生成反向记录。
- **防止SQL注入**：所有数据库查询都使用参数化语句。

### 技能激活触发条件

当用户提到以下关键词时，激活此技能：客户、报价单、销售订单、交货单、销售发票、贷项通知单、退款、销售合作伙伴、定期发票、订阅、从订单到收款、收入、应收账款、销售等。

### 设置（首次使用）

如果数据库不存在或出现“找不到相应表”的错误，请执行以下操作：
```
python3 ~/.openclaw/erpclaw/init_db.py --db-path ~/.openclaw/erpclaw/data.sqlite
```

如果缺少Python依赖库，请运行：`pip install -r {baseDir}/scripts/requirements.txt`

数据库路径：`~/.openclaw/erpclaw/data.sqlite`

## 快速入门（基础级别）

### 创建客户和处理销售流程

当用户请求“添加客户”或“创建发票”时，指导他们按照以下步骤操作：

1. **创建客户**：询问客户名称、类型（公司/个人）和客户所属组。
2. **创建报价单**：起草包含商品、数量和价格的报价单。
3. **转换为销售订单**：提交报价单，然后将其转换为销售订单。
4. **创建交货单**：根据销售订单发货。
5. **创建销售发票**：根据销售订单或交货单向客户开具发票。
6. **下一步建议**：“发票已提交。是否需要记录付款或查看应收账款？”

### 常用命令

**创建客户：**
```
python3 {baseDir}/scripts/db_query.py --action add-customer --name "Acme Corp" --customer-type company --customer-group "Commercial" --company-id <id>
```

**创建报价单（草稿）：**
```
python3 {baseDir}/scripts/db_query.py --action add-quotation --customer-id <id> --posting-date 2026-02-16 --items '[{"item_id":"<id>","qty":10,"rate":"50.00"}]' --company-id <id>
```

**提交并转换为销售订单：**
```
python3 {baseDir}/scripts/db_query.py --action submit-quotation --quotation-id <id>
python3 {baseDir}/scripts/db_query.py --action convert-quotation-to-so --quotation-id <id>
```

**提交销售发票：**
```
python3 {baseDir}/scripts/db_query.py --action submit-sales-invoice --sales-invoice-id <id>
```

### 从订单到收款的流程

| 步骤 | 文档名称 | 功能 | 提交时发生的情况 |
|------|----------|--------|----------------------|
| 1 | 报价单 | QTN-YYYY-NNNNN | 锁定价格；可转换为销售订单 |
| 2 | 销售订单 | SO-YYYY-NNNNN | 检查信用额度；预留承诺 |
| 3 | 交货单 | DN-YYYY-NNNNN | 记录库存减少和成本费用（COGS） |
| 4 | 销售发票 | SINV-YYYY-NNNNN | 记录收入、应收账款和税费 |
| 5 | 贷项通知单 | CN-YYYY-NNNNN | 反向记录发票相关账目 |

### 草稿-提交-取消的生命周期

| 状态 | 是否可更新 | 是否可删除 | 是否可提交 | 是否可取消 |
|--------|-----------|-----------|-----------|-----------|
| 草稿 | 是 | 是 | 是 | 否 |
| 已提交 | 否 | 否 | 否 | 是 |
| 已取消 | 否 | 否 | 否 | 否 |

## 所有操作（高级级别）

所有操作均使用以下命令执行：`python3 {baseDir}/scripts/db_query.py --action <操作> [参数]`

所有输出都以JSON格式显示在标准输出（stdout）中。您需要解析并格式化这些输出以便用户查看。

### 客户相关操作（4种）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-customer` | `--name`, `--customer-type`, `--company-id` | `--customer-group`, `--payment-terms-id`, `--credit-limit`, `--tax-id`, `--exempt-from-sales-tax`, `--primary-address` (JSON), `--primary-contact` (JSON) |
| `update-customer` | `--customer-id` | `--name`, `--credit-limit`, `--payment-terms-id` |
| `get-customer` | `--customer-id` | （无） |
| `list-customers` | | `--company-id`, `--customer-group`, `--search`, `--limit` (20), `--offset` (0) |

### 报价单相关操作（4种）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-quotation` | `--customer-id`, `--posting-date`, `--items` (JSON), `--company-id` | `--tax-template-id`, `--valid-till` |
| `update-quotation` | `--quotation-id` | `--items` (JSON), `--valid-till` |
| `get-quotation` | `--quotation-id` | （无） |
| `list-quotations` | | `--company-id`, `--customer-id`, `--status`, `--from-date`, `--to-date` |

### 报价单生命周期（2种操作）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `submit-quotation` | `--quotation-id` | （无） |
| `convert-quotation-to-so` | `--quotation-id` | （无） |

### 销售订单相关操作（6种）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-sales-order` | `--customer-id`, `--posting-date`, `--delivery-date`, `--items` (JSON), `--company-id` | `--tax-template-id` |
| `update-sales-order` | `--sales-order-id` | `--items` (JSON), `--delivery-date` |
| `get-sales-order` | `--sales-order-id` | （无） |
| `list-sales-orders` | | `--company-id`, `--customer-id`, `--status`, `--from-date`, `--to-date` |
| `submit-sales-order` | `--sales-order-id` | （无） |
| `cancel-sales-order` | `--sales-order-id` | （无） |

### 交货单相关操作（5种）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `create-delivery-note` | `--sales-order-id` | `--items` (JSON, 用于部分发货) |
| `get-delivery-note` | `--delivery-note-id` | （无） |
| `list-delivery-notes` | | `--company-id`, `--customer-id`, `--status`, `--from-date`, `--to-date` |
| `submit-delivery-note` | `--delivery-note-id` | （无） |
| `cancel-delivery-note` | `--delivery-note-id` | （无） |

### 销售发票相关操作（6种）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `create-sales-invoice` | `--sales-order-id` 或 `--delivery-note-id` 或 (`--customer-id`, `--items`, `--company-id`) | `--tax-template-id`, `--due-date` |
| `update-sales-invoice` | `--sales-invoice-id` | `--items` (JSON), `--due-date` |
| `get-sales-invoice` | `--sales-invoice-id` | （无） |
| `list-sales-invoices` | | `--company-id`, `--customer-id`, `--status`, `--from-date`, `--to-date` |
| `submit-sales-invoice` | `--sales-order-id` | （无） |
| `cancel-sales-invoice` | `--sales-invoice-id` | （无） |

### 贷项通知单及相关操作（2种）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `create-credit-note` | `--against-invoice-id`, `--items` (JSON), `--reason` | （无） |
| `update-invoice-outstanding` | `--sales-invoice-id`, `--amount` | （无） |

### 销售合作伙伴相关操作（2种）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-sales-partner` | `--name`, `--commission-rate` | （无） |
| `list-sales-partners` | | `--company-id` |

### 定期发票相关操作（4种）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-recurring-template` | `--customer-id`, `--items` (JSON), `--frequency`, `--start-date`, `--company-id` | `--end-date` |
| `update-recurring-template` | `--template-id` | `--items` (JSON), `--frequency`, `--status` |
| `list-recurring-templates` | | `--company-id`, `--customer-id`, `--status`, `--limit` (20), `--offset` (0) |
| `generate-recurring-invoices` | `--company-id` | `--as-of-date` |

### 公司间发票对账相关操作（5种）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `add-intercompany-account-map` | `--company-id`, `--target-company-id`, `--source-account-id`, `--target-account-id` | （无） |
| `list-intercompany-account-maps` | `--company-id` | `--target-company-id` |
| `create-intercompany-invoice` | `--sales-invoice-id`, `--target-company-id`, `--supplier-id` | （无） |
| `list-intercompany-invoices` | `--company-id` | `--limit`, `--offset` |
| `cancel-intercompany-invoice` | `--sales-invoice-id` | （无） |

### 实用工具（1种）

| 操作 | 必需参数 | 可选参数 |
|--------|---------------|----------------|
| `status` | | `--company-id` |

### 常用命令参考

| 用户输入 | 对应操作 |
|-----------|--------|
| "添加客户" / "新建客户" | `add-customer` |
| "显示客户详情" | `get-customer` |
| "列出客户" | `list-customers` |
| "创建报价单" | `add-quotation` |
| "提交报价单" | `submit-quotation` |
| "将报价单转换为订单" | `convert-quotation-to-so` |
| "创建销售订单" | `add-sales-order` |
| "列出订单" | `list-sales-orders` |
| "发货" / "创建交货单" | `create-delivery-note` |
| "创建发票" | `create-sales-invoice` |
| "提交发票" | `submit-sales-invoice` |
| "取消发票" | `cancel-sales-invoice` |
| "谁欠我钱？" / "未付发票" | `list-sales-invoices` （筛选未付款发票） |
| "开具贷项通知单" / "退款" | `create-credit-note` |
| "添加销售合作伙伴" | `add-sales-partner` |
| "设置佣金" | `add-sales-partner` |
| "创建定期发票" | `add-recurring-template` |
| "生成定期发票" | `generate-recurring-invoices` |
| "公司间发票" | `create-intercompany-invoice` |
| "列出公司间发票" | `list-intercompany-invoices` |
| "取消公司间发票" | `cancel-intercompany-invoice` |
| "映射公司间账户" | `add-intercompany-account-map` |
| "销售情况如何？" | `status` |

### 关键概念

- **信用额度**：在提交销售订单时进行检查。如果客户的未付金额加上新订单的总金额超过信用额度，提交将被阻止。可以通过`update-customer`命令更新信用额度。
- **部分发货**：在创建交货单时，通过`--items`参数传递部分商品信息以实现部分发货。剩余商品可以在后续的交货单中发货。
- **独立发票**：可以通过直接提供`--customer-id`, `--items`, `--company-id`来创建不依赖于销售订单或交货单的销售发票。

### 确认要求

在提交任何文档、取消任何文档或生成定期发票之前，务必进行确认。但在创建草稿、列出记录或添加客户/合作伙伴时无需确认。

**重要提示：**切勿直接使用原始SQL查询数据库。始终使用`db_query.py`命令中的`--action`参数。这些命令会处理所有必要的连接（JOIN）、验证和格式化操作。

### 主动建议

- 在添加客户后，提供报价单。
- 在提交报价单后，建议将其转换为销售订单。
- 在提交销售订单后，建议创建交货单或发票。
- 在提交交货单后，建议开具发票。
- 在提交销售发票后，建议处理付款。
- 在创建贷项通知单后，建议提交相关记录。
- 根据系统状态，标记待处理的草稿。

### 技术协调

- **erpclaw-gl** 提供用于记录收入/应收账款/成本费用的账户表以及相关命名规则。
- **erpclaw-inventory** 提供用于处理交货单的库存账目记录功能。
- **erpclaw-tax** 提供税务模板查询和税费计算功能。
- **erpclaw-payments** 在记录付款时调用`update-invoice-outstanding`函数。
- **共享库`（`~/.openclaw/erpclaw/lib/`）`包含`gl_posting.py`（处理收入账目记录）、`stock_posting.py`（处理交货单记录）和`tax_calculation.py`（处理税费计算）。

### 输出格式

- 列表数据（如客户、文档、发票）使用`$X,XXX.XX`的格式表示货币；日期格式为`Mon DD, YYYY`。切勿直接输出原始JSON数据。

### 错误处理

| 错误类型 | 处理方法 |
|-------|-----|
| “找不到相应表” | 运行`python3 ~/.openclaw/erpclaw/init_db.py --db-path ~/.openclaw/erpclaw/data.sqlite` |
| “信用额度超出” | 通过`update-customer`命令调整信用额度或减少订单金额 |
| “库存不足” | 查看`get-stock-balance`；先补充库存 |
| “无法更新：文档已提交” | 只能修改草稿状态；请先取消订单 |
| “发票已记录付款” | 先取消付款记录，再取消发票 |
| “数据库被锁定” | 2秒后重试一次 |

## 技术细节（高级级别）

- 系统管理的表格数量：`customer`, `quotation`, `quotation_item`, `sales_order`, `sales_order_item`, `delivery_note`, `delivery_note_item`, `salesinvoice`, `salesinvoice_item`, `sales_partner`, `blanket_order`, `recurringinvoice_template`, `recurringinvoice_template_item`（共13个）。
- 使用的脚本：`{baseDir}/scripts/db_query.py`，包含42个操作。
- 数据格式：金额以TEXT（Decimal）类型存储；ID使用TEXT（UUID4）格式。收入/应收账款/成本费用的记录是不可更改的（取消操作会导致记录反向更新）。
- 共享库：`~/.openclaw/erpclaw/lib/gl_posting.py`负责处理收入账目记录，`reverse_gl_entries()`负责处理反向记录。

### 子技能

| 子技能 | 快捷命令 | 功能 |
|-----------|----------|-------------|
| `erp-selling` | `/erp-selling` | 提供销售概览 |
| `erp-customers` | `/erp-customers` | 列出所有客户 |
| `erp-invoices` | `/erp-invoices` | 列出带有状态和未付金额的最新销售发票 |
| `erp-orders` | `/erp-orders` | 列出带有履行状态的有效销售订单 |