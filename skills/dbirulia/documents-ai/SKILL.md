---
name: veryfi-documents-ai
description: Veryfi 提供的实时 OCR（光学字符识别）和数据提取 API。该 API 可用于从收据、发票、银行对账单、W-9 表格、采购订单、提单等任何文档中提取结构化数据。适用于需要执行以下操作的场景：OCR 文档处理、字段提取、文档解析、欺诈检测，或简单地将文档转换为 Markdown 格式。
metadata:
  openclaw:
    requires:
      env:
        - VERYFI_CLIENT_ID
        - VERYFI_USERNAME
        - VERYFI_API_KEY
    primaryEnv: VERYFI_CLIENT_ID
---
# Veryfi 文档分析平台（Documents AI）

实时光学字符识别（OCR）和数据提取 API — 从收据、发票、银行对账单、W-9 表格、采购订单等文档中提取结构化数据，并提供文档分类、欺诈检测以及 Markdown 格式转换功能。

> **获取您的 API 密钥：** https://app.veryfi.com/api/settings/keys/

## 快速入门

### 收据和发票处理：
```bash
curl -X POST "https://api.veryfi.com/api/v8/partner/documents/" \
  -H "Content-Type: multipart/form-data" \
  -H "Client-Id: $VERYFI_CLIENT_ID" \
  -H "Authorization: apikey $VERYFI_USERNAME:$VERYFI_API_KEY" \
  -F "file=@invoice.pdf"
```

### 银行对账单处理：
```bash
curl -X POST "https://api.veryfi.com/api/v8/partner/bank-statements/" \
  -H "Content-Type: multipart/form-data" \
  -H "Client-Id: $VERYFI_CLIENT_ID" \
  -H "Authorization: apikey $VERYFI_USERNAME:$VERYFI_API_KEY" \
  -F "file=@bank-statement.pdf"
```

### 设置

### 1. 获取您的 API 密钥

```bash
# Visit API Auth Credentials page
https://app.veryfi.com/api/settings/keys/
```

**保存 API 密钥：**
```bash
export VERYFI_CLIENT_ID="your_client_id_here"
export VERYFI_USERNAME="your_username_here"
export VERYFI_API_KEY="your_api_key_here"
```

### 2. OpenClaw 配置（可选）

**推荐方式：使用环境变量**（最安全）：
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

**替代方式：存储在配置文件中**（请谨慎使用）：
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

**安全提示：** 如果将 API 密钥存储在 `~/.openclaw/openclaw.json` 文件中，请执行以下操作：**
- 设置文件权限：`chmod 600 ~/.openclaw/openclaw.json`
- **切勿将此文件提交到版本控制系统中**
- **尽可能使用环境变量或代理的密钥存储机制**
- **定期轮换 API 密钥，并在支持的情况下限制其权限**

## 常见任务

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

### 文档分类

无需完整提取文档内容即可识别文档类型。这有助于将文档路由到正确的处理端点、预过滤上传内容或进行批量排序。

```bash
curl -X POST "https://api.veryfi.com/api/v8/partner/classify/" \
  -H "Content-Type: multipart/form-data" \
  -H "Client-Id: $VERYFI_CLIENT_ID" \
  -H "Authorization: apikey $VERYFI_USERNAME:$VERYFI_API_KEY" \
  -F "file=@document.pdf"
```

> **注意：** 默认情况下，API 支持 15 种内置文档类型。您也可以通过传递 `document_types` 数组来指定自定义文档类型（参见下方示例）。

**响应示例：**
```json
{
  "id": 81023456,
  "document_type": {
    "score": 0.97,
    "value": "invoice"
  }
}
```

默认文档类型：`receipt`（收据）、`invoice`（发票）、`purchase_order`（采购订单）、`bank_statement`（银行对账单）、`check`（支票）、`w2`、`w8`、`w9`、`statement`（对账单）、`contract`（合同）、`credit_note`（信用票据）、`remittance_advice`（汇款通知）、`business_card`（商务卡）、`packing_slip`（包装单）、`other`（其他）。

若需使用自定义文档类型，请传递 `document_types` 数组：
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

### 可用于：
- 提取发票和收据数据
- 处理银行对账单
- 从支票中提取数据
- 文档分类和路由
- 从任何其他文档中提取数据

### 不适合用于：
- 视频/音频转录

## 最佳实践

| 文档类型 | API 端点 | 备注 |
|---------------|----------|------------|
| 收据和发票 | `/api/v8/partner/documents/` | 用于处理收据、发票和采购订单 |
| 银行对账单 | `/api/v8/partner/bank-statements/` | 用于处理银行对账单 |
| 支票 | `/api/v8/partner/checks/` | 用于处理加拿大地区的支票 |
| W-9 表格 | `/api/v8/partner/w9s/` | 处理 W-9 表格 |
| 任何文档 | `/api/v8/partner/any-documents/` | 用于从提供的文档列表中提取数据 |
| 文档分类 | `/api/v8/partner/classify/` | 无需完整提取内容即可识别文档类型 |

**可用文档类型列表：**
| 文档类型 | 描述 |
|---------------|----------|
| passport | 美国或国际护照 |
| incorporation_document | 公司注册证书 |
| us_driver_license | 美国驾驶执照 |
| uk_drivers_license | 英国驾驶执照 |
| us_health_insurance_card | 美国健康保险卡 |
| prescription_medication_label | 处方药品标签 |
| medicationinstructions | 药品使用说明 |
| vision_prescription | 视力处方 |
| auto_insurance_card | 汽车保险卡 |
| restaurant_menu | 餐厅菜单 |
| drinks_menu | 饮料菜单 |
| product_nutrition_facts | 产品营养成分标签 |
| goods_received_note | 收货通知 |
| vendor_statement | 供应商对账单 |
| flight_itinerary | 航班行程单 |
| bill_of_lading | 提单 |
| air_waybill | 空运提单 |
| freightinvoice | 货运发票 |
| shipping_label | 运输标签 |
| vehicle_registration | 车辆注册信息 |
| work_order | 工作订单 |
| settlement_letter | 结算函 |
| construction_estimate | 建筑工程估算书 |
| diploma | 毕业证书或学位证书 |
| price_sheet | 价格表 |
| mortgage_application_form | 抵押贷款申请表 |
| lab_test_request_form | 实验室检测申请表 |
| construction_snapshot | 建筑工程快照 |
| medical_prescription_list | 医疗处方列表 |
| v5c | 英国车辆注册证书（V5C） |
| bank_account_verification_letter | 银行账户验证函 |
| annual_mortgage_statement | 年度抵押贷款对账单 |
| investment_account_statement | 投资账户对账单 |
| certificate_of_good_standing | 信用状况证明书 |

**缺少所需文档类型？**
如果您需要提取数据的文档类型不存在，请在此创建：  
`https://app.veryfi.com/inboxes/anydocs?tab=blueprints`

**边界框与置信度：**
- 添加 `-F "bounding_boxes=true` 以获取元素坐标 |
- 添加 `-F "confidence_details=true` 以获取每个字段的置信度分数 |

**支持的输入格式：**
- `file` — 多部分文件上传 |
- `file_url` — 公开可访问的 URL |
- `file_data` — 基于 Base64 编码的文件内容 |

## 响应格式

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
- 查阅 Veryfi 的隐私政策和数据保留政策：https://www.veryfi.com/terms/
- 确认数据删除/保留的时间表
- 先使用非敏感样本文档进行测试
- 如有疑问，请联系 support@veryfi.com

**最佳实践：**
- 在确认服务的安全性和合规性之前，切勿上传高度敏感的个人信息（如 SSN、医疗记录、财务账户号码）
- 如有条件，使用权限和范围有限的 API 密钥
- 监控 API 使用日志以防止未经授权的访问
- **切勿将 API 密钥记录在代码示例或文档中**
- 在配置文件中设置适当的文件权限（JSON 配置文件权限设置为 600）
- 启用 API 密钥轮换功能并通过仪表板监控使用情况

## 故障排除

**错误代码 400（Bad Request）：**
- 请仅提供以下一种输入格式：`file`、`file_url` 或 `file_data`（用于 Base64 编码的文件内容）
- 确认用户名、API 密钥和客户端 ID 是否有效
- 查看 JSON 响应中的 `message` 字段以获取具体错误信息

**置信度分数缺失：**
- 在请求中添加 `confidence_details=true`，以便在响应中包含 `score` 和 `ocr_score` 字段
- 添加 `bounding_boxes=true` 以获取 `bounding_box` 和 `bounding_region` 坐标

## 提示：

- 将 `VERYFI_CLIENT_ID`、`VERYFI_USERNAME` 和 `VERYFI_API_KEY` 存储在环境变量中，而非硬编码
- 当需要每个字段的置信度分数或元素坐标时，使用 `confidence_details=true` 和 `bounding_boxes=true`
- 对于大量文档，先使用 `/classify/` 进行分类，再将其路由到相应的提取端点
- 保持文件大小在 20 MB 以内，并遵守页面限制（收据/发票最多 15 页，银行对账单最多 50 页）
- 在处理敏感数据之前，先用样本文档进行测试
- 如果需要的文档类型不存在，请在 `https://app.veryfi.com/inboxes/anydocs?tab=blueprints` 创建自定义文档类型

## 参考资料

- **API 文档：** https://docs.veryfi.com/
- **Veryfi SDK：** https://github.com/veryfi
- **获取 API 密钥：** https://app.veryfi.com/api/settings/keys/
- **隐私政策：** https://www.veryfi.com/terms/