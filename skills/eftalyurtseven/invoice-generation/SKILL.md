---
name: invoice-generation
description: 使用 each::sense AI 生成专业的发票、收据、报价单和财务文件。该工具能够创建带有品牌标识的商务文档，支持自动计算、多货币处理以及自定义布局功能。
metadata:
  author: eachlabs
  version: "1.0"
---
# 发票生成

使用 `each::sense` 功能生成专业的发票、收据、报价单和财务文件。该功能可创建视觉效果出色、内容准确的商务文档，适用于打印和数字传输。

## 主要特性

- **发票**：包含明细项目、税费和总金额的专业发票
- **收据**：已完成支付的交易收据
- **报价单/估算单**：带有有效期的售前报价
- **贷项通知单**：退款和调整文件
- **采购订单**：采购和订购相关文件
- **多货币支持**：支持多种货币和格式
- **税费计算**：自动处理增值税（VAT）、商品及服务税（GST）等税费
- **企业品牌定制**：支持自定义Logo、颜色和布局
- **重复开票模板**：适用于定期支付的标准化模板

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a professional invoice for web development services, $2,500 total, due in 30 days",
    "mode": "max"
  }'
```

## 文档类型及使用场景

| 文档类型 | 使用场景 | 关键要素 |
|---------------|----------|--------------|
| 发票 | 商品/服务账单 | 明细项目、税费、付款截止日期、付款条款 |
| 收据 | 支付确认 | 交易ID、支付方式、时间戳 |
| 报价单/估算单 | 售前定价 | 有效期、可选项目、条款 |
| 贷项通知单 | 退款/调整 | 原始发票引用、退款原因 |
| 采购订单 | 采购流程 | 供应商信息、运输详情、审批流程 |
| 预开发票 | 发货前使用 | 与普通发票类似，但标记为“预开发票” |

## 使用场景示例

### 1. 基本发票生成

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a simple invoice: Invoice #INV-2024-001, From: Acme Corp (123 Business St, NY 10001), To: Client Inc (456 Customer Ave, LA 90001), Service: Consulting Services - $1,500. Due date: March 15, 2024. Clean, professional design.",
    "mode": "max"
  }'
```

### 2. 带有明细项目的发票

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a detailed invoice with multiple line items: Invoice #INV-2024-042 From: Digital Solutions LLC To: TechStart Inc Line items: 1) Website Development - 40 hours @ $150/hr = $6,000 2) UI/UX Design - 20 hours @ $125/hr = $2,500 3) SEO Setup - flat rate $800 4) Hosting (Annual) - $480 Subtotal, 8% tax, and grand total. Payment terms: Net 30. Include bank transfer details section.",
    "mode": "max"
  }'
```

### 3. 带有企业品牌标识的发票

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a branded invoice for a creative agency. Company: Pixel Perfect Studios, use modern minimalist design with a navy blue and gold color scheme. Include space for logo at top left. Invoice #PP-2024-089 to MediaMax Corp. Services: Brand Identity Package $4,500, Social Media Templates $1,200, Brand Guidelines Document $800. Total $6,500. Due in 14 days. Include Pay Now button placeholder and QR code area for payment link.",
    "mode": "max",
    "image_urls": ["https://example.com/company-logo.png"]
  }'
```

### 4. 收据生成

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a payment receipt: Receipt #REC-78432 From: Cloud Services Pro To: Johnson Enterprises Payment received: $3,250.00 Payment method: Credit Card (Visa ending 4242) Transaction ID: TXN-2024-02-15-98765 Date: February 15, 2024 at 2:34 PM For: Invoice #INV-2024-038 (Annual SaaS Subscription) Status: PAID in full. Include a thank you message and support contact.",
    "mode": "max"
  }'
```

### 5. 报价单/估算单生成

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a project quote/estimate: Quote #QT-2024-015 From: BuildRight Construction To: Greenfield Properties Project: Office Renovation - 2nd Floor Line items: 1) Demolition and prep - $8,500 2) Electrical work - $12,000 3) Plumbing updates - $6,500 4) Flooring (800 sq ft) - $9,600 5) Painting and finishing - $4,200 6) Project management (10%) - $4,080 Total estimate: $44,880 Valid for 30 days. Include terms: 50% deposit required, final payment on completion. Add signature line for acceptance.",
    "mode": "max"
  }'
```

### 6. 多货币发票

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate an international invoice in Euros: Invoice #EU-2024-0023 From: TechGlobal GmbH (Berlin, Germany, VAT: DE123456789) To: Societe Digitale SARL (Paris, France, VAT: FR987654321) Services: Software License (Enterprise) - 12 months @ 850 EUR/month = 10,200 EUR Implementation Services - 3,500 EUR Training (Remote) - 1,800 EUR Subtotal: 15,500 EUR VAT (19%): 2,945 EUR Total: 18,445 EUR Payment: SEPA transfer, IBAN: DE89 3704 0044 0532 0130 00, BIC: COBADEFFXXX Due: 30 days. Reverse charge note for intra-EU B2B.",
    "mode": "max"
  }'
```

### 7. 带有税费计算的发票

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an invoice with complex tax breakdown: Invoice #TAX-2024-156 From: Retail Solutions Inc (GST: 12-3456789) To: Shop & Save Stores Line items with different tax rates: 1) POS Hardware (5 units @ $899) = $4,495 - Standard rate 10% GST 2) Software License = $2,400 - Standard rate 10% GST 3) Installation Services = $1,200 - Standard rate 10% GST 4) Training Materials (books) = $350 - Zero rated 5) Extended Warranty = $600 - Exempt Subtotal: $9,045 GST Summary: Standard rated (10%): $8,095 x 10% = $809.50 Zero rated: $350 x 0% = $0 Exempt: $600 Total GST: $809.50 Grand Total: $9,854.50 Include ABN and tax invoice statement.",
    "mode": "max"
  }'
```

### 8. 重复开票模板

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a recurring monthly invoice template: Invoice #[AUTO-NUMBER] From: CloudHost Pro Services To: [CLIENT NAME] Billing Period: [MONTH YEAR] Recurring Services: 1) Dedicated Server Hosting - $299/month 2) Managed Backup Service - $49/month 3) SSL Certificate - $9/month 4) Technical Support (Business) - $149/month Monthly Total: $506 Mark as RECURRING INVOICE. Show billing cycle: Monthly, auto-renews. Next billing date field. Include: Update payment method link, Cancel subscription link. Modern SaaS-style design with clean typography.",
    "mode": "max"
  }'
```

### 9. 贷项通知单/退款文件

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a credit note: Credit Note #CN-2024-008 From: Premium Supplies Co To: Office Depot Partners Original Invoice: #INV-2024-892 dated January 10, 2024 Reason for credit: Goods returned - defective items Credit items: 1) Ergonomic Chair Model X (2 units @ $450) = -$900 2) Return shipping covered = -$45 Total Credit: $945.00 Original invoice total: $2,340 Remaining balance due: $1,395 Note: Credit has been applied to your account. Future invoices will reflect this adjustment. Authorized by: [Signature line]. Use red accent color to indicate credit/refund.",
    "mode": "max"
  }'
```

### 10. 采购订单生成

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a purchase order: PO #PO-2024-0456 From (Buyer): MegaCorp Industries, 789 Corporate Blvd, Chicago IL 60601, Purchasing Dept Contact: Jane Smith, jane@megacorp.com To (Vendor): Industrial Supplies Ltd, 321 Warehouse Way, Detroit MI 48201 Ship To: MegaCorp Warehouse B, 456 Distribution Dr, Chicago IL 60602 Order Items: 1) Steel Brackets SKU-SB100 - 500 units @ $2.50 = $1,250 2) Mounting Hardware Kit SKU-MH200 - 200 units @ $8.00 = $1,600 3) Safety Cables SKU-SC300 - 1000 units @ $1.25 = $1,250 4) Industrial Adhesive SKU-IA400 - 50 gallons @ $45 = $2,250 Subtotal: $6,350 Shipping: $285 Total: $6,635 Required delivery date: March 1, 2024 Payment terms: Net 45 Special instructions: Deliver to loading dock B, call 30 min before arrival. Include approval signature lines for Requester, Manager, and Purchasing.",
    "mode": "max"
  }'
```

## 多次请求中的发票处理

使用 `session_id` 在多次请求中保持发票的一致性：

```bash
# Initial invoice creation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an invoice for marketing services, $5,000 total from Creative Agency to StartupXYZ",
    "session_id": "invoice-project-001"
  }'

# Add more line items
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Break that down into: Strategy $2,000, Content Creation $1,800, Ad Management $1,200. Add 7% sales tax.",
    "session_id": "invoice-project-001"
  }'

# Update styling
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Update the design to use a green and white color scheme, add payment instructions for Stripe.",
    "session_id": "invoice-project-001"
  }'
```

## 批量文档生成

一次性生成多份相关文档：

```bash
# Generate invoice
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create invoice #INV-001 for Project Alpha, $10,000 consulting fee to Acme Corp",
    "session_id": "project-alpha-docs",
    "mode": "eco"
  }'

# Generate matching receipt after payment
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a matching receipt for that invoice, payment received via wire transfer today",
    "session_id": "project-alpha-docs",
    "mode": "eco"
  }'
```

## 最佳实践

### 发票设计建议
- **清晰的层次结构**：企业信息放在顶部，明细项目位于中间，总金额醒目显示
- **易读的字体**：使用专业且清晰的排版
- **适当的间距**：避免布局过于拥挤
- **联系方式**：务必提供咨询联系方式

### 必需信息
- **唯一的发票编号**：采用连续编号或编码系统
- **发行日期和付款截止日期**：明确支付时间线
- **完整的业务信息**：公司名称、地址、税务识别码
- **明细费用**：项目描述、数量、单价、金额
- **付款说明**：银行账户信息、支持的支付方式

### 法律合规性要求
- 在规定要求的地方标注税务注册号码
- 使用正确的税率
- 正确标记文档类型（发票、报价单、预开发票等）
- 包含必要的法律免责声明

## 财务文档生成提示

生成发票和财务文件时，请注意以下内容：
- **文档类型**：发票、收据、报价单、贷项通知单、采购订单
- **双方信息**：发送方和接收方的完整信息
- **项目/服务信息**：项目描述、数量、单价
- **费用计算**：税率、折扣、总金额
- **付款条款**：付款截止日期、有效期
- **品牌元素**：颜色、样式、Logo
- **附加字段**：采购订单编号、项目参考编号、备注

### 示例提示结构

```
"Create a [document type] #[number]
From: [company name and details]
To: [client name and details]
Items: [list with quantities and prices]
Tax: [rate and type]
Terms: [payment terms]
Style: [design preferences]"
```

## 模式选择

在生成文档前询问用户：
**“您需要快速且低成本的文档，还是高质量的专业文档？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终面向客户的正式发票、品牌化文档 | 较慢 | 最高质量 |
| `eco` | 草稿发票、内部文件、批量生成 | 较快 | 适合一般需求 |

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 账户余额不足 | 请在 eachlabs.ai 补充余额 |
| 内容违规 | 包含禁止的内容 | 调整提示内容以符合政策要求 |
| 超时 | 文档生成过程复杂 | 将客户等待时间设置为至少 10 分钟 |

## 相关技能

- `each-sense`：核心 API 文档生成工具
- `document-generation`：通用文档生成功能
- `business-card-generation`：名片设计工具
- `letterhead-generation`：公司信头设计工具