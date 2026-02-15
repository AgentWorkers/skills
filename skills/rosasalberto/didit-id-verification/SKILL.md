---
name: didit-id-verification
description: >
  Integrate Didit ID Verification standalone API to verify identity documents.
  Use when the user wants to verify an ID, passport, driver's license, residence permit,
  or identity document using Didit, or mentions ID verification, document verification,
  OCR extraction, MRZ parsing, KYC document checks, or document authenticity validation.
  Supports 4000+ document types across 220+ countries.
version: 1.2.0
metadata:
  openclaw:
    requires:
      env:
        - DIDIT_API_KEY
    primaryEnv: DIDIT_API_KEY
    emoji: "📋"
    homepage: https://docs.didit.me
---

# Didit ID验证API

## 概述

该API通过提交身份证件的正面和背面图片来进行身份验证。它支持OCR文字提取、机器可读区（MRZ）解析、真实性检查以及文档活性检测（即判断图片是否为实时拍摄）。

**主要要求：**
- 支持的文件格式：JPEG、PNG、WebP、TIFF
- 每张图片的最大文件大小为5MB
- 所有文档的角都必须清晰可见，图片应为全彩，且无反光或阴影
- 仅接受原始的实时拍摄照片（禁止使用截图、扫描件或数字副本）

**验证范围：**涵盖4,000多种文档类型、220多个国家和地区、130多种语言。支持的文档类型包括护照、身份证、驾驶执照和居留证。

**处理流程：**
1. 智能图像捕捉与文档类型识别
2. OCR文字提取及MRZ/条形码解析
3. 模板匹配、安全特性验证及篡改检测
4. 文档活性检测（识别是否为屏幕截图、打印副本或经过图像处理的图片）

**API参考文档：**https://docs.didit.me/reference/id-verification-standalone-api

---

## 认证要求

所有请求都必须包含`x-api-key`头部信息。您可以从[Didit业务控制台](https://business.didit.me)获取API密钥。

---

## API端点

```
POST https://verification.didit.me/v3/id-verification/
```

### 请求头

| 头部信息 | 值 | 是否必填 |
| --- | --- | --- |
| `x-api-key` | 您的API密钥 | 是 |
| `Content-Type` | `multipart/form-data` | 是 |

### 请求参数（multipart/form-data格式）

| 参数 | 类型 | 是否必填 | 默认值 | 限制条件 | 说明 |
| --- | --- | --- | --- | --- |
| `front_image` | 文件 | 是 | — | 文件格式：JPEG/PNG/WebP/TIFF，最大5MB | 身份证件的正面图片 |
| `back_image` | 文件 | 否 | — | 如适用，请提供身份证件的背面图片 |
| `save_api_request` | 布尔值 | 否 | `true` | 是否将验证结果保存到业务控制台进行人工审核 |
| `vendor_data` | 字符串 | 否 | — | 用于会话跟踪的唯一标识符 |

### 示例请求

```python
import requests

response = requests.post(
    "https://verification.didit.me/v3/id-verification/",
    headers={"x-api-key": "YOUR_API_KEY"},
    files={
        "front_image": ("front.jpg", open("front.jpg", "rb"), "image/jpeg"),
        "back_image": ("back.jpg", open("back.jpg", "rb"), "image/jpeg"),
    },
    data={"vendor_data": "user-123"},
)
```

```typescript
const formData = new FormData();
formData.append("front_image", frontImageFile);
formData.append("back_image", backImageFile);
formData.append("vendor_data", "user-123");

const response = await fetch("https://verification.didit.me/v3/id-verification/", {
  method: "POST",
  headers: { "x-api-key": "YOUR_API_KEY" },
  body: formData,
});
```

### 响应（200 OK）

```json
{
  "request_id": "a1b2c3d4-...",
  "id_verification": {
    "status": "Approved",
    "document_type": "Identity Card",
    "document_number": "YZA123456",
    "personal_number": "X9876543L",
    "first_name": "Elena",
    "last_name": "Martínez Sánchez",
    "full_name": "Elena Martínez Sánchez",
    "date_of_birth": "1985-03-15",
    "age": 40,
    "gender": "F",
    "nationality": "ESP",
    "issuing_state": "ESP",
    "issuing_state_name": "Spain",
    "expiration_date": "2030-08-21",
    "date_of_issue": "2020-08-21",
    "address": "Calle Mayor 10, Madrid",
    "formatted_address": "Calle Mayor 10, 28013 Madrid, Spain",
    "place_of_birth": "Valencia",
    "portrait_image": "<base64>",
    "front_document_image": "<base64>",
    "back_document_image": "<base64>",
    "mrz": {
      "surname": "MARTINEZ SANCHEZ",
      "given_name": "ELENA",
      "document_type": "I",
      "document_number": "YZA123456",
      "country": "ESP",
      "nationality": "ESP",
      "birth_date": "850315",
      "expiry_date": "300821",
      "sex": "F"
    },
    "parsed_address": {"city": "Madrid", "region": "...", "postal_code": "28013", "country": "ES"},
    "warnings": []
  },
  "created_at": "2025-05-01T13:11:07.977806Z"
}
```

### 状态码及其含义

| 状态码 | 含义 |
| --- | --- |
| `"Approved"` | 文档验证成功 |
| `"Declined"` | 验证失败（请查看`warnings`字段） |
| `"In Review"` | 需要人工审核 |

### 错误响应

| 错误代码 | 含义 | 应对措施 |
| --- | --- | --- |
| `400` | 请求无效 | 请检查文件格式、大小及参数 |
| `401` | API密钥无效 | 请确认`x-api-key`头部信息是否正确 |
| `403` | 信用额度不足 | 请在business.didit.me充值 |

---

## 响应字段说明

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `status` | 字符串 | `"Approved"`, `"Declined"`, `"In Review"` |
| `document_type` | 字符串 | `"Passport"`, `"Identity Card"`, `"Driver's License"`, `"Residence Permit"` |
| `document_number` | 字符串 | 文档编号 |
| `personal_number` | 字符串 | 个人/国民身份证号码 |
| `first_name`, `last_name`, `full_name` | 字符串 | 提取的姓名字段 |
| `date_of_birth` | 字符串 | 出生日期（格式：YYYY-MM-DD） |
| `age` | 整数 | 计算出的年龄 |
| `gender` | 字符串 | `"M"`, `"F"`, `"U"` |
| `nationality`, `issuing_state` | 字符串 | 国家代码（ISO 3166-1 alpha-3） |
| `expiration_date`, `date_of_issue` | 字符串 | 有效期/签发日期（格式：YYYY-MM-DD） |
| `portrait_image` | 字符串 | 从文档中提取的肖像图像（Base64编码） |
| `mrz` | 对象 | 机器可读区数据 |
| `parsed_address` | 对象 | 地理编码地址（格式：`{city, region, postal_code, country, street_1}` |
| `warnings` | 数组 | 错误信息（包含风险等级、错误类型及详细描述） |

---

## 警告标签

### 自动拒绝的情况

| 标签 | 说明 |
| --- | --- |
| `ID_document_IN_BLOCKLIST` | 文档被列入黑名单 |
| `PORTRAIT_IMAGE_NOT_DETECTED` | 文档中未检测到肖像 |
| `DOCUMENT_EXPIRED` | 文档已过期 |
| `DOCUMENT_NOT_SUPPORTED_FOR_APPLICATION` | 该文档类型不被支持 |

### 可配置的拒绝/审核/批准规则

| 类别 | 相关标签 |
| --- | --- |
| **文档活性** | `SCREEN_CAPTURE_DETECTED`, `PRINTED_COPY_DETECTED`, `PORTRAIT_MANIPULATION_DETECTED` |
| **MRZ问题** | `MRZ_NOT_DETECTED`, `MRZ_VALIDATION_FAILED`, `MRZ_AND_DATA_EXTRACTED_FROM_OCR_NOT_SAME` |
| **数据问题** | `NAME_NOT_DETECTED`, `DATE_OF_BIRTH_NOT_DETECTED`, `DOCUMENT_NUMBER_NOT_DETECTED`, `DATA_INCONSISTENT` |
| **重复记录** | `POSSIBLE_DUPLICATED_USER` |
| **信息不一致** | `FULL_NAME_MISMATCH_WITH_PROVIDED`, `DOB_MISMATCH_WITH_PROVIDED`, `GENDER_MISMATCH_WITH_PROVIDED` |
| **地理位置** | `DOCUMENT_country_MISMATCH` |

---

## 常见使用场景

### 基本身份验证流程

```
1. POST /v3/id-verification/ → front_image (+ back_image if applicable)
2. If "Approved" → extract first_name, last_name, date_of_birth, document_number
   If "Declined" → check warnings:
     DOCUMENT_EXPIRED → ask for valid document
     SCREEN_CAPTURE_DETECTED → ask for real photo of physical document
     MRZ_VALIDATION_FAILED → ask for clearer image
```

### 完整的身份验证流程

```
1. POST /v3/id-verification/ → verify document
2. POST /v3/passive-liveness/ → verify real person
3. POST /v3/face-match/ → compare selfie to document portrait
4. POST /v3/aml/ → screen extracted name/DOB/nationality
5. All Approved → fully verified identity
```

---

## 实用脚本

```bash
export DIDIT_API_KEY="your_api_key"

python scripts/verify_id.py front.jpg
python scripts/verify_id.py front.jpg back.jpg --vendor-data user-123
```