---
name: didit-proof-of-address
description: >
  Integrate Didit Proof of Address standalone API to verify address documents.
  Use when the user wants to verify a proof of address, validate utility bills,
  bank statements, government documents, extract address from documents, verify
  residential address, implement address verification, or perform PoA checks
  using Didit. Supports OCR extraction, geocoding, name matching, and multi-page documents.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - DIDIT_API_KEY
    primaryEnv: DIDIT_API_KEY
    emoji: "🏠"
    homepage: https://docs.didit.me
---

# Didit地址证明API

## 概述

该API通过上传图片或PDF文件来验证地址证明文件。它能够提取地址信息、进行真实性检查、姓名匹配、地理编码，并返回结构化数据。

**主要限制条件：**
- 支持的文件格式：JPG、JPEG、PNG、TIFF、PDF
- 文件最大大小：15MB
- 文件必须是在签发日期后的90天内生成的
- 文件应为全彩图像，所有角落都清晰可见，且未经任何数字编辑
- 该文件不能与用于身份验证的身份证件相同

**功能：**
- OCR文字识别
- 智能文件分类
- 与身份证明文件的姓名匹配
- 签发日期验证
- 基于经纬度坐标进行地理编码
- 语言检测
- 支持多页文件

**接受的文件类型：**

| 类型 | 示例 |
|---|---|
| 公用事业账单 | 电费、水费、燃气费、互联网费用、电话费、综合公用事业账单 |
| 银行对账单 | 账户对账单、信用卡对账单、抵押贷款对账单、贷款对账单 |
| 政府颁发的文件 | 税务评估文件、居住证明、选民登记文件 |
| 其他地址证明文件 | 租赁协议、保险单、雇主函件 |

**API参考文档：** https://docs.didit.me/reference/proof-of-address-standalone-api

---

## 认证

所有请求都必须包含`x-api-key`头部信息。您可以从[Didit商业控制台](https://business.didit.me) → API & Webhooks获取API密钥。

---

## 端点

```
POST https://verification.didit.me/v3/poa/
```

### 头部信息

| 头部信息 | 值 | 是否必填 |
|---|---|---|
| `x-api-key` | 您的API密钥 | 是 |
| `Content-Type` | `multipart/form-data` | 是 |

### 请求参数（multipart/form-data）

| 参数 | 类型 | 是否必填 | 默认值 | 说明 |
|---|---|---|---|---|
| `document` | 文件 | 是 | — | 地址证明文件（JPG/PNG/TIFF/PDF格式，最大15MB） |
| `save_api_request` | 布尔值 | 否 | `true` | 是否将结果保存到商业控制台 |
| `vendor_data` | 字符串 | 否 | — | 用于会话跟踪的标识符 |

### 示例请求

```python
import requests

response = requests.post(
    "https://verification.didit.me/v3/poa/",
    headers={"x-api-key": "YOUR_API_KEY"},
    files={"document": ("utility_bill.pdf", open("bill.pdf", "rb"), "application/pdf")},
    data={"vendor_data": "user-123"},
)
print(response.json())
```

```typescript
const formData = new FormData();
formData.append("document", documentFile);

const response = await fetch("https://verification.didit.me/v3/poa/", {
  method: "POST",
  headers: { "x-api-key": "YOUR_API_KEY" },
  body: formData,
});
```

### 响应（200 OK）

```json
{
  "request_id": "a1b2c3d4-...",
  "poa": {
    "status": "Approved",
    "issuing_state": "ESP",
    "document_type": "UTILITY_BILL",
    "issuer": "Endesa",
    "issue_date": "2025-01-15",
    "document_language": "es",
    "name_on_document": "Elena Martínez Sánchez",
    "poa_address": "Calle Mayor 10, 28013 Madrid",
    "poa_formatted_address": "Calle Mayor 10, 28013 Madrid, Spain",
    "poa_parsed_address": {
      "street_1": "Calle Mayor 10",
      "city": "Madrid",
      "region": "Comunidad de Madrid",
      "postal_code": "28013",
      "raw_results": {
        "geometry": {"location": {"lat": 40.4168, "lng": -3.7038}}
      }
    },
    "document_file": "https://example.com/document.pdf",
    "warnings": []
  },
  "created_at": "2025-05-01T13:11:07.977806Z"
}
```

### 状态码及其含义及处理方式

| 状态码 | 含义 | 处理方式 |
|---|---|---|
| `"Approved"` | 地址已验证，文件有效 | 可以继续您的流程 |
| `"Declined"` | 文件无效或已过期 | 查看`warnings`字段以获取具体原因 |
| `"In Review"` | 需要人工审核 | 检查是否存在姓名不匹配或文件质量问题 |
| `"Not Finished"` | 处理未完成 | 等待或重试 |

### 错误响应

| 错误代码 | 含义 | 处理方式 |
|---|---|---|
| `400` | 请求无效 | 检查文件格式、大小或参数是否正确 |
| `401` | API密钥无效 | 请确认`x-api-key`头部信息是否正确 |
| `403` | 信用额度不足 | 请在business.didit.me上充值 |

---

## 响应字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `status` | 字符串 | `"Approved"`, `"Declined"`, `"In Review"`, `"Not Finished"` |
| `issuing_state` | 字符串 | ISO 3166-1 alpha-3国家代码 |
| `document_type` | 字符串 | `"UTILITY_BILL"`, `"BANK_STATEMENT"`, `"GOVERNMENT_ISSUED_DOCUMENT"`, `"OTHER_POA DOCUMENT"` |
| `issuer` | 字符串 | 文件签发机构名称 |
| `issue_date` | 字符串 | 文件签发日期（格式为YYYY-MM-DD） |
| `document_language` | 字符串 | 检测到的文件语言代码 |
| `name_on_document` | 字符串 | 提取出的姓名 |
| `poa_address` | 字符串 | 提取的原始地址 |
| `poaFormatted_address` | 字符串 | 格式化后的地址 |
| `poaparsed_address` | 对象 | `{street_1, street_2, city, region, postal_code}`（街道、城市、地区、邮政编码） |
| `poaparsed_address.raw_results.geometry.location` | 对象 | `{lat, lng}`（地理编码后的经纬度坐标） |
| `document_file` | 字符串 | 临时URL（有效期为60分钟） |
| `warnings` | 数组 | `{risk, log_type, short_description, long_description}`（错误信息） |

---

## 警告标签

### 自动拒绝的情况

| 标签 | 说明 |
|---|---|
| `POA_document_NOT_SUPPORTED_FOR_APPLICATION` | 该文件类型不适用于您的应用程序 |
| `EXPIRED_document` | 文件已超过90天的有效期 |
| `INVALID DOCUMENT_TYPE` | 文件无法被处理 |
| `MISSING_ADDRESS_information` | 无法提取有效的地址信息 |

### 可配置的拒绝/审核/批准规则

| 标签 | 说明 |
|---|---|
| `NAME_MISMATCH_WITH_PROVIDED` | 提供的姓名与验证后的姓名不匹配 |
| `NAME_MISMATCH_ID_VERIFICATION` | 提供的姓名与身份证件上的姓名不匹配 |
| `POA_NAME_MISMATCH_BETWEEN_DOCUMENTS` | 多份地址证明文件中的姓名不一致 |
| `POOR DOCUMENT_QUALITY` | 文件质量太差 |
| `DOCUMENT_METADATA_MISMATCH` | 文件的数字签名或元数据存在篡改痕迹 |
| `SUSPECTED DOCUMENT_MANIPULATION` | 文件似乎被篡改 |
| `UNSUPPORTED DOCUMENTLANGUAGE` | 文件语言不受支持 |
| `ADDRESS_MISMATCH_WITH_PROVIDED` | 提供的地址与实际地址不符 |
| `UNABLE_TO_EXTRACT_ISSUE_DATE` | 无法确定文件的签发日期 |
| `ISSUER_NOT_identIFIED` | 无法识别文件签发机构 |
| `UNPARSABLE_OR_INVALID_ADDRESS` | 地址无法被解析 |
| `UNABLE_TO_VALIDATE DOCUMENT_AGE` | 无法确定文件的签发时间 |
| `FUTURE_ISSUE_DATE` | 文件的签发日期在未来 |

警告的严重程度：`error`（→ 拒绝），`warning`（→ 正在审核），`information`（→ 无影响）。

---

## 常见工作流程

### 基本地址验证

```
1. POST /v3/poa/ → {"document": utility_bill}
2. If "Approved" → address verified
   If "Declined" → check warnings:
     EXPIRED_DOCUMENT → ask for a more recent document
     MISSING_ADDRESS_INFORMATION → ask for clearer image
     NAME_MISMATCH → verify identity matches
```

### 完整的KYC流程（包含地址验证）

```
1. POST /v3/id-verification/ → verify identity document
2. POST /v3/passive-liveness/ → verify real person
3. POST /v3/poa/ → verify address
4. System auto-matches name between ID and PoA documents
5. All Approved → identity + address verified
```