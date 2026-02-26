---
name: veryfi-documents-ai
description: >
  Veryfi提供的实时OCR（光学字符识别）和数据提取API（https://veryfi.com）：能够从收据、发票、银行对账单、W-9表格、采购订单、提单以及任何其他文档中提取结构化数据。当您需要执行以下操作时，可以使用该API：  
  - 对文档进行OCR处理；  
  - 提取文档中的关键字段；  
  - 解析收据/发票内容；  
  - 对文档进行分类；  
  - 检测欺诈行为；  
  - 从任何文档中获取原始的OCR文本。
metadata:
  openclaw:
    requires:
      env:
        - VERYFI_CLIENT_ID
        - VERYFI_USERNAME
        - VERYFI_API_KEY
    primaryEnv: VERYFI_CLIENT_ID
---
# Veryfi 文档 AI

实时光学字符识别（OCR）和数据提取 API — 从收据、发票、银行对账单、W-9 表格、采购订单等文档中提取结构化数据，同时提供文档分类、欺诈检测以及原始 OCR 文本输出。

> **获取您的 API 密钥：** https://app.veryfi.com/api/settings/keys/
> **了解更多信息：** https://veryfi.com

## 快速入门

### 收据和发票：
```bash
curl -X POST "https://api.veryfi.com/api/v8/partner/documents/" \
  -H "Content-Type: multipart/form-data" \
  -H "Client-Id: $VERYFI_CLIENT_ID" \
  -H "Authorization: apikey $VERYFI_USERNAME:$VERYFI_API_KEY" \
  -F "file=@invoice.pdf"
```

### 响应：
```json
{
  "id": 62047612,
  "created_date": "2026-02-19",
  "currency_code": "USD",
  "date": "2026-02-18 14:22:00",
  "document_type": "receipt",
  "category": "Meals & Entertainment",
  "is_duplicate": false,
  "vendor": {
    "name": "Starbucks",
    "address": "123 Main St, San Francisco, CA 94105"
  },
  "line_items": [
    {
      "id": 1,
      "order": 0,
      "description": "Caffe Latte Grande",
      "quantity": 1,
      "price": 5.95,
      "total": 5.95,
      "type": "food"
    }
  ],
  "subtotal": 5.95,
  "tax": 0.52,
  "total": 6.47,
  "payment": {
    "type": "visa",
    "card_number": "1234"
  },
  "ocr_text": "STARBUCKS\n123 Main St...",
  "img_url": "https://scdn.veryfi.com/documents/...",
  "pdf_url": "https://scdn.veryfi.com/documents/..."
}
```

### 银行对账单：
```bash
curl -X POST "https://api.veryfi.com/api/v8/partner/bank-statements/" \
  -H "Content-Type: multipart/form-data" \
  -H "Client-Id: $VERYFI_CLIENT_ID" \
  -H "Authorization: apikey $VERYFI_USERNAME:$VERYFI_API_KEY" \
  -F "file=@bank-statement.pdf"
```

### 响应：
```json
{
  "id": 4820193,
  "created_date": "2026-02-19T12:45:00.000000Z",
  "bank_name": "Chase",
  "bank_address": "270 Park Avenue, New York, NY 10017",
  "account_holder_name": "Jane Doe",
  "account_holder_address": "456 Oak Ave, San Francisco, CA 94110",
  "account_number": "****7890",
  "account_type": "Checking",
  "routing_number": "021000021",
  "currency_code": "USD",
  "statement_date": "2026-01-31",
  "period_start_date": "2026-01-01",
  "period_end_date": "2026-01-31",
  "beginning_balance": 12500.00,
  "ending_balance": 11835.47,
  "accounts": [
    {
      "number": "****7890",
      "beginning_balance": 12500.00,
      "ending_balance": 11835.47,
      "summaries": [
        { "name": "Total Deposits", "total": 3200.00 },
        { "name": "Total Withdrawals", "total": 3864.53 }
      ],
      "transactions": [
        {
          "order": 0,
          "date": "2026-01-05",
          "description": "Direct Deposit - ACME Corp Payroll",
          "credit_amount": 3200.00,
          "debit_amount": null,
          "balance": 15700.00,
          "category": "Income"
        },
        {
          "order": 1,
          "date": "2026-01-12",
          "description": "Rent Payment - 456 Oak Ave",
          "credit_amount": null,
          "debit_amount": 2800.00,
          "balance": 12900.00,
          "category": "Housing"
        },
        {
          "order": 2,
          "date": "2026-01-20",
          "description": "PG&E Utility Bill",
          "credit_amount": null,
          "debit_amount": 1064.53,
          "balance": 11835.47,
          "category": "Utilities"
        }
      ]
    }
  ],
  "pdf_url": "https://scdn.veryfi.com/bank-statements/...",
  "img_url": "https://scdn.veryfi.com/bank-statements/..."
}
```

## 设置

### 1. 获取您的 API 密钥

```bash
# Visit API Auth Credentials page
https://app.veryfi.com/api/settings/keys/
```

保存您的 API 密钥：
```bash
export VERYFI_CLIENT_ID="your_client_id_here"
export VERYFI_USERNAME="your_username_here"
export VERYFI_API_KEY="your_api_key_here"
```

### 2. OpenClaw 配置（可选）

**推荐：使用环境变量**（最安全的方式）：
```json5
{
  skills: {
    entries: {
      "veryfi-documents-ai": {
        enabled: true,
        // Keys loaded from environment variables:
        // VERYFI_CLIENT_ID, VERYFI_USERNAME, VERYFI_API_KEY
      },
    },
  },
}
```

**替代方案：存储在配置文件中**（请谨慎使用）：
```json5
{
  skills: {
    entries: {
      "veryfi-documents-ai": {
        enabled: true,
        env: {
          VERYFI_CLIENT_ID: "your_client_id_here",
          VERYFI_USERNAME: "your_username_here",
          VERYFI_API_KEY: "your_api_key_here",
        },
      },
    },
  },
}
```

**安全提示：** 如果将 API 密钥存储在 `~/.openclaw/openclaw.json` 文件中，请执行以下操作：
- 设置文件权限：`chmod 600 ~/.openclaw/openclaw.json`
- 绝不要将此文件提交到版本控制系统中
- 尽可能使用环境变量或代理的秘密存储机制
- 定期更换 API 密钥，并在支持的情况下限制 API 密钥的权限

## 常见任务

### 从收据或发票中提取数据（上传文件）
```bash
curl -X POST "https://api.veryfi.com/api/v8/partner/documents/" \
  -H "Content-Type: multipart/form-data" \
  -H "Client-Id: $VERYFI_CLIENT_ID" \
  -H "Authorization: apikey $VERYFI_USERNAME:$VERYFI_API_KEY" \
  -F "file=@invoice.pdf"
```

### 从收据或发票中提取数据（Base64 编码格式）

如果您的代理已经拥有文档的 Base64 编码内容（例如通过 API、电子邮件附件或工具输出），请使用 `file_data` 而不是上传文件：
```bash
# Encode the file first
BASE64_DATA=$(base64 -i invoice.pdf)

curl -X POST "https://api.veryfi.com/api/v8/partner/documents/" \
  -H "Content-Type: application/json" \
  -H "Client-Id: $VERYFI_CLIENT_ID" \
  -H "Authorization: apikey $VERYFI_USERNAME:$VERYFI_API_KEY" \
  -d "{
    \"file_name\": \"invoice.pdf\",
    \"file_data\": \"$BASE64_DATA\"
  }"
```

### 从 URL 中提取数据
```bash
curl -X POST "https://api.veryfi.com/api/v8/partner/documents/" \
  -H "Content-Type: application/json" \
  -H "Client-Id: $VERYFI_CLIENT_ID" \
  -H "Authorization: apikey $VERYFI_USERNAME:$VERYFI_API_KEY" \
  -d '{
    "file_url": "https://example.com/invoice.pdf"
  }'
```

### 从护照中提取数据
```bash
curl -X POST "https://api.veryfi.com/api/v8/partner/any-documents/" \
  -H "Content-Type: multipart/form-data" \
  -H "Client-Id: $VERYFI_CLIENT_ID" \
  -H "Authorization: apikey $VERYFI_USERNAME:$VERYFI_API_KEY" \
  -F "file=@passport.jpg" \
  -F "blueprint_name=passport"
```

### 从支票中提取数据
```bash
curl -X POST "https://api.veryfi.com/api/v8/partner/checks/" \
  -H "Content-Type: multipart/form-data" \
  -H "Client-Id: $VERYFI_CLIENT_ID" \
  -H "Authorization: apikey $VERYFI_USERNAME:$VERYFI_API_KEY" \
  -F "file=@check.jpg"
```

### 从 W-9 表格中提取数据
```bash
curl -X POST "https://api.veryfi.com/api/v8/partner/w9s/" \
  -H "Content-Type: multipart/form-data" \
  -H "Client-Id: $VERYFI_CLIENT_ID" \
  -H "Authorization: apikey $VERYFI_USERNAME:$VERYFI_API_KEY" \
  -F "file=@w9.pdf"
```

### 从 W-2 和 W-8 表格中提取数据

W-2 和 W-8 表格没有专用的 API 端点。请使用 `any-documents` 端点并指定相应的蓝图：
```bash
# W-2
curl -X POST "https://api.veryfi.com/api/v8/partner/any-documents/" \
  -H "Content-Type: multipart/form-data" \
  -H "Client-Id: $VERYFI_CLIENT_ID" \
  -H "Authorization: apikey $VERYFI_USERNAME:$VERYFI_API_KEY" \
  -F "file=@w2.pdf" \
  -F "blueprint_name=w2"

# W-8
curl -X POST "https://api.veryfi.com/api/v8/partner/any-documents/" \
  -H "Content-Type: multipart/form-data" \
  -H "Client-Id: $VERYFI_CLIENT_ID" \
  -H "Authorization: apikey $VERYFI_USERNAME:$VERYFI_API_KEY" \
  -F "file=@w8.pdf" \
  -F "blueprint_name=w8"
```

> **注意：** W-2 和 W-8 表格在分类时显示为特定类型（通过 `/classify/` 端点），但其数据提取实际上是通过 `any-documents` 端点处理的。**切勿** 向 `/api/v8/partner/w2s/` 或 `/api/v8/partner/w8s/` 发送请求，因为这些端点并不存在。

### 从文档中获取原始 OCR 文本

所有提取 API 端点都会在响应中返回一个 `ocr_text` 字段，其中包含文档的原始文本内容（以纯文本形式）。这有助于您自行处理文本或将其传递给大型语言模型（LLM）。

```bash
# Extract and pull ocr_text with jq
curl -X POST "https://api.veryfi.com/api/v8/partner/documents/" \
  -H "Content-Type: multipart/form-data" \
  -H "Client-Id: $VERYFI_CLIENT_ID" \
  -H "Authorization: apikey $VERYFI_USERNAME:$VERYFI_API_KEY" \
  -F "file=@document.pdf" \
  | jq '.ocr_text'
```

> **注意：** `ocr_text` 是纯文本，不是 Markdown 格式。如果需要 Markdown 格式的输出，请在提取后将其传递给 LLM 进行重新格式化。

### 对文档进行分类

在不进行完整数据提取的情况下识别文档类型。这有助于将文档路由到正确的处理端点、预过滤上传内容或批量排序。

```bash
curl -X POST "https://api.veryfi.com/api/v8/partner/classify/" \
  -H "Content-Type: multipart/form-data" \
  -H "Client-Id: $VERYFI_CLIENT_ID" \
  -H "Authorization: apikey $VERYFI_USERNAME:$VERYFI_API_KEY" \
  -F "file=@document.pdf"
```

> **注意：** 默认情况下，API 会根据 15 种内置类型进行分类。您也可以传递一个 `document_types` 数组来指定自定义类型（见下面的示例）。

### 响应：
```json
{
  "id": 81023456,
  "document_type": {
    "score": 0.97,
    "value": "invoice"
  }
}
```

默认文档类型：`receipt`（收据）、`invoice`（发票）、`purchase_order`（采购订单）、`bank_statement`（银行对账单）、`check`（支票）、`w2`（W-2 表格）、`w8`（W-8 表格）、`w9`（W-9 表格）、`statement`（对账单）、`contract`（合同）、`credit_note`（信用通知）、`remittance_advice`（汇款通知）、`business_card`（商务卡）、`packing_slip`（包装单）、`other`（其他）。

要使用自定义类型进行分类，请传递一个 `document_types` 数组：
```bash
curl -X POST "https://api.veryfi.com/api/v8/partner/classify/" \
  -H "Content-Type: multipart/form-data" \
  -H "Client-Id: $VERYFI_CLIENT_ID" \
  -H "Authorization: apikey $VERYFI_USERNAME:$VERYFI_API_KEY" \
  -F "file=@document.pdf" \
  -F 'document_types=["lease_agreement", "utility_bill", "pay_stub"]'
```

## 高级功能

### 收据、发票、支票和银行对账单的边界框信息
获取元素坐标以用于布局分析：
```bash
-F "bounding_boxes=true" 
-F "confidence_details=true"
```

## 使用场景

### 使用 Veryfi 文档 AI 进行以下操作：
- 提取发票和收据数据
- 处理银行对账单
- 从支票中提取数据
- 文档分类和路由
- 从任何其他文档中提取数据
- 从文档中获取原始 OCR 文本

### 不适用的场景：
- 视频或音频转录
- 网页搜索或实时数据查询
- 图像生成或编辑
- 非文档类型的二进制文件（如电子表格、代码、可执行文件）
- 未确认可用于第三方处理的文档（请参阅安全部分）

## 最佳实践

| 文档类型 | API 端点 | 备注 |
|---------------|----------|------------|
| 收据和发票 | `/api/v8/partner/documents/` | 用于处理收据、发票和采购订单 |
| 银行对账单 | `/api/v8/partner/bank-statements/` | 用于处理银行对账单 |
| 支票 | `/api/v8/partner/checks/` | 用于处理加拿大地区的支票 |
| W-9 表格 | `/api/v8/partner/w9s/` | 用于处理 W-9 表格 |
| W-2/W-8 表格 | `/api/v8/partner/any-documents/` | 使用 `blueprint_name=w2` 或 `blueprint_name=w8` |
| 任何文档 | `/api/v8/partner/any-documents/` | 用于从任何文档中提取数据；以下是可用的蓝图列表 |
| 分类 | `/api/v8/partner/classify/` | 在不进行完整数据提取的情况下识别文档类型 |

**可用蓝图列表：**
| blueprint_name | 文档类型 |
|---------------|----------|
| passport | 美国或国际护照 |
| incorporation_document | 公司注册证书 |
| us_driver_license | 美国驾驶执照 |
| uk_drivers_license | 英国驾驶执照 |
| us_health_insurance_card | 美国健康保险卡 |
| prescription_medication_label | 处方药标签 |
| medicationinstructions | 药物使用说明 |
| vision_prescription | 视力处方 |
| auto_insurance_card | 自动保险卡 |
| restaurant_menu | 餐厅菜单 |
| drinks_menu | 饮料菜单 |
| product_nutrition_facts | 产品营养标签 |
| goods_received_note | 收货通知 |
| vendor_statement | 供应商声明 |
| flight_itinerary | 航班行程单 |
| bill_of_lading | 提单 |
| air_waybill | 空运提单 |
| freightinvoice | 货运发票 |
| shipping_label | 运输标签 |
| vehicle_registration | 车辆注册信息 |
| work_order | 工作订单 |
| settlement_letter | 结算函 |
| construction_estimate | 建筑估算 |
| diploma | 文凭或学位证书 |
| price_sheet | 价格表 |
| mortgage_application_form | 抵押贷款申请表 |
| lab_test_request_form | 实验室检测申请表 |
| construction_snapshot | 建筑快照 |
| medical_prescription_list | 医疗处方列表 |
| v5c | 英国车辆注册证书（V5C） |
| bank_account_verification_letter | 银行账户验证函 |
| annual_mortgage_statement | 年度抵押贷款对账单 |
| investment_account_statement | 投资账户对账单 |
| certificate_of_good_standing | 信用良好证明 |
| w2 | 美国 W-2 工资和税务报表 |
| w8 | 美国 W-8 外籍身份证明 |

**缺少文档类型？**
如果您需要提取数据的文档类型（蓝图）不存在，请在此创建：  
`https://app.veryfi.com/inboxes/anydocs?tab=blueprints`

**边界框和置信度：**
- 添加 `-F "bounding_boxes=true` 以获取元素坐标
- 添加 `-F "confidence_details=true` 以获取每个字段的置信度分数

**支持的输入格式：**
- `file` — 多部分文件上传
- `file_url` — 公开可访问的 URL
- `file_data` — Base64 编码的内容（以 JSON 格式发送，包含 `file_name` 和 `file_data` 字段）

## 响应结构

### 收据/发票（`/api/v8/partner/documents/`）
```json
{
  "id": 62047612,
  "created_date": "2026-02-19T00:00:00.000000Z",
  "updated_date": "2026-02-19T00:00:05.000000Z",
  "currency_code": "USD",
  "date": "2026-02-18 14:22:00",
  "due_date": "2026-03-18",
  "document_type": "receipt",
  "category": "Meals & Entertainment",
  "is_duplicate": false,
  "is_document": true,
  "invoice_number": "INV-2026-001",
  "account_number": "ACCT-12345",
  "order_date": "2026-02-18",
  "delivery_date": null,
  "vendor": {
    "name": "Starbucks",
    "address": "123 Main St, San Francisco, CA 94105",
    "phone_number": "+1 415-555-0100",
    "email": null,
    "vat_number": null,
    "reg_number": null
  },
  "bill_to": {
    "name": "Jane Doe",
    "address": "456 Oak Ave, San Francisco, CA 94110"
  },
  "ship_to": {
    "name": null,
    "address": null
  },
  "line_items": [
    {
      "id": 1,
      "order": 0,
      "description": "Caffe Latte Grande",
      "quantity": 1,
      "price": 5.95,
      "total": 5.95,
      "tax": 0.52,
      "tax_rate": 8.75,
      "discount": null,
      "type": "food",
      "sku": null,
      "upc": null,
      "category": "Meals & Entertainment",
      "section": null,
      "date": null,
      "start_date": null,
      "end_date": null
    }
  ],
  "tax_lines": [
    {
      "order": 0,
      "name": "Sales Tax",
      "rate": 8.75,
      "total": 0.52,
      "base": 5.95
    }
  ],
  "subtotal": 5.95,
  "tax": 0.52,
  "tip": 0.00,
  "discount": 0.00,
  "total": 6.47,
  "payment": {
    "type": "visa",
    "card_number": "1234"
  },
  "reference_number": null,
  "notes": null,
  "img_url": "https://scdn.veryfi.com/documents/...",
  "pdf_url": "https://scdn.veryfi.com/documents/...",
  "ocr_text": "STARBUCKS\n123 Main St...",
  "meta": {
    "total_pages": 1,
    "processed_pages": 1,
    "fraud": {
      "score": 0.01,
      "color": "green",
      "decision": "Not Fraud",
      "types": []
    }
  }
}
```

### 支票（`/api/v8/partner/checks/`）
```json
{
  "id": 9301847,
  "created_date": "2026-02-19T00:00:00.000000Z",
  "updated_date": "2026-02-19T00:00:03.000000Z",
  "amount": 1500.00,
  "amount_text": "One Thousand Five Hundred and 00/100",
  "check_number": "4021",
  "date": "2026-02-15",
  "currency_code": "USD",
  "check_type": "personal_check",
  "payer_name": "John Smith",
  "payer_address": "789 Elm St, Austin, TX 78701",
  "receiver_name": "Acme Plumbing LLC",
  "receiver_address": null,
  "bank_name": "Wells Fargo",
  "bank_address": "420 Montgomery St, San Francisco, CA 94104",
  "memo": "Invoice #2026-038",
  "is_signed": true,
  "micr": {
    "routing_number": "121000248",
    "account_number": "****5678",
    "serial_number": "4021",
    "raw": "⑆121000248⑆ ****5678⑈ 4021",
    "branch": null,
    "institution": null
  },
  "fractional_routing_number": "12-1/1200",
  "routing_from_fractional": "121000248",
  "endorsement": {
    "is_endorsed": true,
    "is_signed": true,
    "mobile_or_remote_deposit": {
      "checkbox": false,
      "instructions": false
    }
  },
  "handwritten_fields": ["amount", "amount_text", "date", "receiver_name", "memo"],
  "fraud": {
    "score": 0.02,
    "color": "green",
    "types": [],
    "pages": [
      {
        "is_lcd": { "score": 0.98, "value": false },
        "ai_generated": { "score": 0.99, "value": false },
        "four_corners_detected": true
      }
    ]
  },
  "img_thumbnail_url": "https://scdn.veryfi.com/checks/...",
  "pdf_url": "https://scdn.veryfi.com/checks/..."
}
```

### 银行对账单（`/api/v8/partner/bank-statements/`）
```json
{
  "id": 4820193,
  "created_date": "2026-02-19T12:45:00.000000Z",
  "updated_date": "2026-02-19T12:45:10.000000Z",
  "bank_name": "Chase",
  "bank_address": "270 Park Avenue, New York, NY 10017",
  "account_holder_name": "Jane Doe",
  "account_holder_address": "456 Oak Ave, San Francisco, CA 94110",
  "account_number": "****7890",
  "account_type": "Checking",
  "routing_number": "021000021",
  "currency_code": "USD",
  "statement_date": "2026-01-31",
  "period_start_date": "2026-01-01",
  "period_end_date": "2026-01-31",
  "beginning_balance": 12500.00,
  "ending_balance": 11835.47,
  "minimum_due": null,
  "due_date": null,
  "accounts": [
    {
      "number": "****7890",
      "beginning_balance": 12500.00,
      "ending_balance": 11835.47,
      "summaries": [
        { "name": "Total Deposits", "total": 3200.00 },
        { "name": "Total Withdrawals", "total": 3864.53 }
      ],
      "transactions": [
        {
          "order": 0,
          "date": "2026-01-05",
          "posted_date": "2026-01-05",
          "description": "Direct Deposit - ACME Corp Payroll",
          "credit_amount": 3200.00,
          "debit_amount": null,
          "balance": 15700.00,
          "category": "Income",
          "vendor": "ACME Corp"
        },
        {
          "order": 1,
          "date": "2026-01-12",
          "posted_date": "2026-01-12",
          "description": "Rent Payment - 456 Oak Ave",
          "credit_amount": null,
          "debit_amount": 2800.00,
          "balance": 12900.00,
          "category": "Housing",
          "vendor": null
        }
      ]
    }
  ],
  "fraud": {
    "score": 0.01,
    "color": "green",
    "types": []
  },
  "pdf_url": "https://scdn.veryfi.com/bank-statements/...",
  "img_thumbnail_url": "https://scdn.veryfi.com/bank-statements/..."
}
```

## 安全与隐私

### 数据处理

**重要提示：** 上传到 Veryfi 的文档会被传输到 `https://api.veryfi.com` 并在 AWS 服务器上进行处理。

**在上传敏感文档之前：**
- 查看 Veryfi 的隐私政策和数据保留政策：https://www.veryfi.com/terms/
- 确认数据删除/保留的时间表
- 先使用非敏感样本文档进行测试
- 如有疑问，请联系 support@veryfi.com

**最佳实践：**
- 在确认服务的安全性和合规性之前，切勿上传高度敏感的个人信息（如 SSN、医疗记录、财务账户号码）
- 如果可能，请使用权限和范围有限的 API 密钥
- 监控 API 使用日志以防止未经授权的访问
- 绝不要将 API 密钥记录或提交到代码库或示例中

### 文件大小限制

- **每个文档的最大文件大小：** 20 MB
- **页面数量：** 收据/发票默认不超过 15 页，银行对账单不超过 50 页。如需增加限制，请联系支持团队。

### 操作安全措施

- 始终使用环境变量或安全的秘密存储机制来存储 API 密钥
- 绝不要在代码示例或文档中包含真实的 API 密钥
- 在示例中使用占位符值（如 `"your_api_key_here"`）
- 为配置文件设置适当的文件权限（JSON 配置文件权限为 600）
- 启用 API 密钥的定期更换，并通过仪表板监控使用情况

## 速率限制

Veryfi 对每个账户实施速率限制。具体限制取决于您的计划级别。

**一般指导原则：**
- **免费/入门计划：** 并发请求限制较低；避免同时发送大量请求
- **商业/企业计划：** 并发请求量较高；详情请联系支持团队
- 如果达到速率限制，API 会返回 **HTTP 429 Too Many Requests** 错误
- 实施指数级重试策略：等待 1 秒 → 2 秒 → 4 秒 → 8 秒后再尝试
- 对于高并发量的工作负载，请联系 support@veryfi.com 或访问 https://veryfi.com 以讨论企业级计划

## 故障排除

**400 Bad Request：**
- 请提供其中一个输入参数：`file`、`file_url` 或 `file_data`（对于 Base64 编码的内容）
- 使用 `file_data` 时，以 JSON 格式发送（不要使用多部分上传），并包含 `file_name` 和 `file_data` 字段
- 确认用户名、API 密钥和客户端 ID 是否有效
- 查看 JSON 响应中的 `message` 字段以获取具体的错误详情

**401 Unauthorized：**
- 您的 `Client-Id`、`VERYFI_USERNAME` 或 `VERYFI_API_KEY` 不正确或已过期
- 在 https://app.veryfi.com/api/settings/keys/ 确认凭据是否正确
- 确保 `Authorization` 标头格式为 `apikey USERNAME:API_KEY`（不要有额外的空格）
- 如果怀疑密钥被泄露，请更换密钥

**413 Payload Too Large：**
- 文件大小超过 20 MB 的限制
- 上传前压缩文件或降低图像分辨率
- 如果 PDF 文件的页数超过限制（发票 15 页，银行对账单 50 页），请分割文件

**429 Too Many Requests：**
- 您超过了计划的速率限制
- 实施指数级重试策略
- 对于持续的高并发量，请联系 support@veryfi.com 以升级计划

**500 / 5xx 服务器错误：**
- 服务器端暂时出现问题——稍后重试
- 如果错误持续，请查看 Veryfi 的状态页面或联系 support@veryfi.com

**缺少置信度分数：**
- 在请求中添加 `confidence_details=true` 以在响应中包含 `score` 和 `ocr_score` 字段
- 添加 `bounding_boxes=true` 以获取 `bounding_box` 和 `bounding_region` 坐标

**W-2/W-8 端点 404：**
- 不存在 `/w2s/` 或 `/w8s/` 端点——请使用 `/any-documents/` 并指定 `blueprint_name=w2` 或 `blueprint_name=w8`

## 提示

- 将 `VERYFI_CLIENT_ID`、`VERYFI_USERNAME` 和 `VERYFI_API_KEY` 存储在环境变量中，而不是硬编码
- 当需要每个字段的置信度分数或元素坐标时，使用 `confidence_details=true` 和 `bounding_boxes=true`
- 对于大量文档，先使用 `/classify/` 进行分类，然后路由到相应的提取端点
- 保持文件大小在 20 MB 以内，并遵守页面限制（发票 15 页，银行对账单 50 页）
- 在处理敏感数据之前，先用样本文档进行测试
- 如果需要的蓝图不存在，请在 `https://app.veryfi.com/inboxes/anydocs?tab=blueprints` 创建自定义蓝图
- 响应中的 `ocr_text` 包含原始提取的文本——如果需要 Markdown 格式或进一步处理，请将其传递给 LLM
- 对于 Base64 输入，务必包含 `file_name`，以便 Veryfi 正确识别文件类型

## 参考资料

- **API 文档：** https://docs.veryfi.com/
- **Veryfi：** https://veryfi.com
- **Veryfi SDK：** https://github.com/veryfi
- **获取 API 密钥：** https://app.veryfi.com/api/settings/keys/
- **隐私政策：** https://www.veryfi.com/terms/
- **支持：** support@veryfi.com