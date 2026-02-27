---
name: deepread-form-fill
title: image.png
description: 基于人工智能的PDF表单填写功能：只需上传PDF表单以及以JSON格式提交的数据，AI会自动识别表单中的字段，对数据进行语义分析，完成表单填写并执行质量检查，最终生成一份完整的PDF文件。该功能支持扫描后的表单、手写模板以及任何格式的PDF文件，无需使用AcroForm格式的表单字段。
disable-model-invocation: true
metadata:
  {"openclaw":{"requires":{"env":["DEEPREAD_API_KEY"]},"primaryEnv":"DEEPREAD_API_KEY","homepage":"https://www.deepread.tech"}}
---
# DeepRead表单填写——基于AI的PDF表单填充API

您可以上传任何PDF表单以及您的JSON数据。AI会自动识别表单中的字段，将您的数据填充到相应的位置，对填充结果进行质量检查，然后返回一个可下载的已完成PDF文件。

**支持所有类型的PDF**——无论是扫描的纸质表单、政府发布的PDF文件，还是自定义模板。无需使用AcroForm格式的表单。

## 该服务的功能

您需要提供：
1. 一个空的PDF表单（用于上传）
2. 您的数据（以JSON格式，例如：`{"full_name": "Jane Doe", "dob": "1990-03-15"}`）

DeepRead会返回：
- 一个已填充的PDF文件，其中您的数据会被正确地放入相应的字段中
- 一份质量报告，说明哪些字段已成功填写，哪些需要人工审核

**无需进行字段映射或配置**——AI会自动判断数据应放置的位置。

## 设置

### 获取您的API密钥

```bash
# Sign up (free — 2,000 pages/month, no credit card)
# https://www.deepread.tech/dashboard/?utm_source=clawdhub
```

请保存您的API密钥：
```bash
export DEEPREAD_API_KEY="sk_live_your_key_here"
```

## 快速入门

### 填写表单（只需3行代码）

```bash
# 1. Submit form + data
curl -X POST https://api.deepread.tech/v1/form-fill \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@application.pdf" \
  -F 'form_fields={"full_name": "Jane Doe", "date_of_birth": "03/15/1990", "address": "123 Main St, Portland OR 97201"}'

# Response (immediate):
# {"id": "<job_id>", "status": "queued"}

# 2. Poll for result (use the id from step 1)
curl https://api.deepread.tech/v1/form-fill/<job_id> \
  -H "X-API-Key: $DEEPREAD_API_KEY"

# 3. Download the filled PDF from filled_form_url in the response
```

## API参考

### POST /v1/form-fill — 提交表单进行填充

**认证方式：** 必须在请求头中添加`X-API-Key`
**请求类型：** `multipart/form-data`

**参数：**

| 参数 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| `file` | 文件 | 是 | 需要填充的PDF表单 |
| `form_fields` | JSON字符串 | 是 | `{"field_name": "value"}` — 您的数据 |
| `webhook_url` | 字符串 | 否 | 填写完成后用于接收结果的URL |
| `idempotency_key` | 字符串 | 否 | 用于防止重复提交 |
| `url_expires_in` | 整数 | 否 | 签名的URL的有效期（以秒为单位，默认为604800秒=7天，最小值3600秒，最大值604800秒） |

**示例：**
```bash
curl -X POST https://api.deepread.tech/v1/form-fill \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@tax_form.pdf" \
  -F 'form_fields={
    "taxpayer_name": "Jane Doe",
    "ssn": "123-45-6789",
    "filing_status": "Single",
    "total_income": "85000",
    "tax_year": "2025"
  }' \
  -F "webhook_url=https://your-app.com/webhooks/form-fill"
```

**响应（立即返回）：**
```json
{
  "id": "<job_id>",
  "status": "queued"
}
```

处理过程是**异步的**——您可以通过GET请求或Webhook来获取处理进度。

### GET /v1/form-fill/{job_id} — 获取任务状态和结果

**认证方式：** 必须在请求头中添加`X-API-Key`
**请求频率限制：** 每60秒内最多20次请求

```bash
curl https://api.deepread.tech/v1/form-fill/<job_id> \
  -H "X-API-Key: $DEEPREAD_API_KEY"
```

**处理完成后的响应：**
```json
{
  "id": "<job_id>",
  "status": "completed",
  "file_name": "tax_form.pdf",
  "created_at": "2025-06-15T10:00:00Z",
  "completed_at": "2025-06-15T10:00:18Z",
  "filled_form_url": "https://storage.deepread.tech/form_fill/.../filled.pdf",
  "fields_detected": 25,
  "fields_filled": 23,
  "fields_verified": 21,
  "fields_hil_flagged": 2,
  "duration_seconds": 18.3,
  "report": {
    "summary": {
      "fields_detected": 25,
      "fields_filled": 23,
      "fields_verified": 21,
      "fields_hil_flagged": 2,
      "mappings_created": 23,
      "unmapped_keys": 0,
      "adjustments_made": 3
    },
    "fields": [
      {
        "field_index": 0,
        "label": "Taxpayer Name",
        "field_type": "text",
        "page": 1,
        "value": "Jane Doe",
        "hil_flag": false,
        "verified": true
      },
      {
        "field_index": 8,
        "label": "Total Income",
        "field_type": "text",
        "page": 2,
        "value": "85000",
        "hil_flag": true,
        "verified": false,
        "reason": "Text overlaps adjacent field"
      }
    ],
    "mappings": [
      {
        "user_key": "taxpayer_name",
        "field_index": 0,
        "value_to_fill": "Jane Doe",
        "confidence": 0.95
      }
    ],
    "unmapped_user_keys": [],
    "adjustments_made": ["Field 8: reduced font size from 12pt to 8pt"],
    "qa_feedback": ["Total Income: text overlaps adjacent field"],
    "errors": []
  },
  "errors": null,
  "error_message": null
}
```

**状态代码及其含义：**

| 状态 | 含义 |
| --- | --- |
| `queued` | 等待处理 |
| `processing` | AI正在填充表单 |
| `completed` | 已完成 — 请从`filled_form_url`下载结果 |
| `failed` | 出现错误 — 请查看`error_message`以获取详细信息 |

**建议每隔5-10秒检查一次状态，直到状态变为`completed`或`failed`。**

### Webhook通知（可选）

如果您提供了`webhook_url`，DeepRead会在任务完成后通过Webhook发送通知：

**完成通知：**
```json
{
  "job_id": "<job_id>",
  "status": "completed",
  "created_at": "<ISO 8601 timestamp>",
  "completed_at": "<ISO 8601 timestamp>",
  "result": {
    "filled_form_url": "<signed URL to download filled PDF>",
    "fields_detected": 25,
    "fields_filled": 23,
    "fields_verified": 21,
    "fields_hil_flagged": 2,
    "report": { ... }
  }
}
```

**失败通知：**
```json
{
  "job_id": "<job_id>",
  "status": "failed",
  "created_at": "<ISO 8601 timestamp>",
  "completed_at": "<ISO 8601 timestamp>",
  "error": "Form fill timed out after 600s",
  "errors": ["Form fill timed out after 600s"]
}
```

## 工作原理（内部实现）

**关键说明：** 这个服务基于视觉识别技术进行表单填充，而非AcroForm格式。它适用于**所有类型的PDF文件**——无论是扫描的纸质表单、政府发布的PDF文件（即使没有可编辑字段），还是自定义模板。

## 使用示例

### 贷款申请
```bash
curl -X POST https://api.deepread.tech/v1/form-fill \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@loan_application.pdf" \
  -F 'form_fields={
    "applicant_name": "Jane Doe",
    "date_of_birth": "03/15/1990",
    "ssn": "123-45-6789",
    "employer": "Acme Corp",
    "annual_income": "95000",
    "loan_amount": "350000",
    "property_address": "456 Oak Ave, Portland OR 97201",
    "loan_type": "30-Year Fixed"
  }'
```

### 保险索赔
```bash
curl -X POST https://api.deepread.tech/v1/form-fill \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@claim_form.pdf" \
  -F 'form_fields={
    "policy_number": "INS-2025-78901",
    "insured_name": "Jane Doe",
    "date_of_loss": "06/01/2025",
    "description": "Water damage to basement from pipe burst",
    "estimated_damage": "12500",
    "photos_attached": "true"
  }'
```

### 政府表格（如W-4、I-9等）
```bash
curl -X POST https://api.deepread.tech/v1/form-fill \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@w4_form.pdf" \
  -F 'form_fields={
    "first_name": "Jane",
    "last_name": "Doe",
    "ssn": "123-45-6789",
    "address": "123 Main St",
    "city": "Portland",
    "state": "OR",
    "zip": "97201",
    "filing_status": "Single",
    "multiple_jobs": "false"
  }'
```

### 批量处理（相同模板，不同数据）
```python
import json
import os
import requests
import time

API_KEY = os.environ["DEEPREAD_API_KEY"]
FORM_TEMPLATE = "application.pdf"

applicants = [
    {"full_name": "Jane Doe", "email": "jane@example.com", "dob": "1990-03-15"},
    {"full_name": "John Smith", "email": "john@example.com", "dob": "1985-07-22"},
    {"full_name": "Alice Chen", "email": "alice@example.com", "dob": "1992-11-08"},
]

jobs = []
for i, applicant in enumerate(applicants):
    with open(FORM_TEMPLATE, "rb") as f:
        resp = requests.post(
            "https://api.deepread.tech/v1/form-fill",
            headers={"X-API-Key": API_KEY},
            files={"file": (FORM_TEMPLATE, f, "application/pdf")},
            data={
                "form_fields": json.dumps(applicant),
                "idempotency_key": f"batch-2025-06-{i}",
            },
        )
    job_id = resp.json()["id"]
    jobs.append(job_id)
    print(f"Submitted: {applicant['full_name']} → job {job_id}")

# Poll for results
for job_id in jobs:
    while True:
        result = requests.get(
            f"https://api.deepread.tech/v1/form-fill/{job_id}",
            headers={"X-API-Key": API_KEY},
        ).json()
        if result["status"] in ("completed", "failed"):
            print(f"Job {job_id}: {result['status']}")
            if result["status"] == "completed":
                print(f"  Download: {result['filled_form_url']}")
                print(f"  Fields: {result['fields_filled']}/{result['fields_detected']} filled, "
                      f"{result['fields_hil_flagged']} need review")
            break
        time.sleep(5)
```

## 理解报告结果

### 各个指标的含义

| 指标 | 含义 |
| --- | --- |
| `fields_detected` | AI在PDF中检测到的总字段数 |
| `fields_filled` | 您的数据被填充到的字段数 |
| `fields_verified` | 经过视觉质量检查的字段数（文本可读且位置正确） |
| `fields_hil_flagged` | 需要人工审核的字段数（AI无法完全验证） |

**典型结果：** 90-95%的字段通过验证，2-5%的字段需要人工审核。

### “HIL”标志（需要人工审核的字段）

当出现以下情况时，字段会被标记为`hil_flag: true`：
- 文本与相邻字段重叠 |
- 字体需要大幅缩小 |
- 值与字段的预期内容不匹配 |
- 修复尝试未能解决问题

**每个被标记的字段都会附带一个`reason`（原因），说明为何需要人工审核。**

### 未匹配的字段

如果您的JSON数据中包含的键与表单中的字段不匹配，这些键会显示在`unmapped_user_keys`中。这可能表示：
- 表单中不存在对应的字段 |
- 或者字段标签不够明确

## 避免重复提交

使用`idempotency_key`来防止重复提交：
```bash
# First request
curl -X POST https://api.deepread.tech/v1/form-fill \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@form.pdf" \
  -F 'form_fields={"name": "Jane"}' \
  -F "idempotency_key=submission-abc-123"
# → {"id": "<job_id>", "status": "queued"}

# Retry (same key) — returns the same job, no duplicate
curl -X POST https://api.deepread.tech/v1/form-fill \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@form.pdf" \
  -F 'form_fields={"name": "Jane"}' \
  -F "idempotency_key=submission-abc-123"
# → {"id": "<same job_id as above>", "status": "queued"}  ← SAME JOB
```

## 适用场景

### 适用于以下场景：
- **贷款/抵押贷款申请** — 使用CRM数据填写20多页的表单 |
- **保险索赔** — 自动填写索赔表格 |
- **政府表格**（如W-4、I-9、税务表格等） |
- **法律文件**（包含字段占位符的合同、协议） |
- **新员工入职资料**（来自HR系统的文件） |
- **批量处理**（相同模板，处理大量申请）

### 不适用场景：
- **从头开始创建PDF文件** — 该服务仅用于填充现有表单，不生成新的PDF文件 |
- **实时处理（<1秒）** — 处理时间约为15-30秒（异步操作） |
- **非PDF格式的文件** — 仅支持PDF格式（DOCX格式的支持即将推出）

## 使用限制与定价

### 免费套餐（无需信用卡）
- 每月2,000页 |
- 全功能使用权限

### 付费套餐
- **PRO套餐**：每月50,000页，费用为99美元 |
- **SCALE套餐**：根据使用量定制价格

**升级方式：** https://www.deepread.tech/dashboard/billing?utm_source=clawdhub

## 常见问题及解决方法

### 错误：400 “仅支持PDF文件”
请上传`.pdf`格式的文件。其他格式的文件目前不受支持。

### 错误：400 “form_fields中的JSON格式无效”
请检查JSON语法，确保它是一个有效的JSON对象（而非数组）：
```
✅ {"name": "Jane Doe", "dob": "1990-03-15"}
❌ ["name", "dob"]
❌ "just a string"
```

### 错误：429 “每月使用量超出限制”
请升级到PRO套餐或等待下一个计费周期。

### 状态码“failed”（表示处理失败）
- 表单内容过于复杂或页面过多。可以尝试将表单拆分成更小的部分。
- `fields_fields`中的JSON数据格式不正确。

### 字段未正确填充
请在JSON数据中添加更详细的字段名称。AI会根据您提供的键名来匹配表单字段：
```
✅ {"applicant_full_name": "Jane Doe"}  — clear, matches form labels
❌ {"field1": "Jane Doe"}  — ambiguous, hard to map
```

### 有些字段被标记为需要审核
对于2-5%的字段，这是正常现象。请查看`report.fields`中的`reason`以获取具体原因。

## 使用的API端点

| 端点 | 方法 | 认证方式 | 功能 |
| --- | --- | --- | --- |
| `https://api.deepread.tech/v1/form-fill` | POST | API密钥 | 提交表单和数据 |
| `https://api.deepread.tech/v1/form-fill/{job_id}` | GET | API密钥 | 查询任务状态和结果 |

## 帮助资源

- **控制台：** https://www.deepread.tech/dashboard |
- **问题反馈：** https://github.com/deepread-tech/deep-read-service/issues |
- **邮箱：** hello@deepread.tech

---

**立即免费试用：** https://www.deepread.tech/dashboard/?utm_source=clawdhub