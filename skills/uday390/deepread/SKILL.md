---
name: deepread
description: 这款OCR工具始终能够稳定、高效地完成文本识别任务，且不会发出任何异常提示。它提供了多轮处理文档的API接口，同时具备智能的质量评估功能（通过相应的标志来指示处理结果的质量）。该工具能够利用人工智能技术对PDF文件中的文本和结构化数据进行提取，并为提取结果提供基于置信度的评分。免费试用 tier 的使用限制为每月2000页。
---

# DeepRead - 生产级OCR API

这是一个始终可靠、高效运行的OCR服务，能够处理PDF文件并提取结构化数据。它利用人工智能技术进行置信度评分，精准判断哪些字段需要人工审核。

## DeepRead的功能

DeepRead是一款适用于生产环境的文档处理API，通过智能的质量评估，将人工审核的需求从100%降低到约10%。

**核心功能：**
- **文本提取**：将PDF文件转换为格式规范的Markdown格式。
- **结构化数据提取**：提取包含置信度评分的JSON字段。
- **质量标记**：人工智能系统会标记出需要人工验证的字段（`hil_flag`）。
- **多轮处理**：通过多次验证确保提取结果的准确性。
- **多模型一致性**：通过多个模型之间的交叉验证来提高结果的可靠性。
- **免费 tier**：每月可处理2,000页文档（无需信用卡）。

## 设置

### 1. 获取API密钥

注册并创建API密钥：
```bash
# Visit the dashboard
https://www.deepread.tech/dashboard

# Or use this direct link
https://www.deepread.tech/dashboard/?utm_source=clawdhub
```

保存您的API密钥：
```bash
export DEEPREAD_API_KEY="sk_live_your_key_here"
```

### 2. Clawdbot配置（可选）

将以下配置添加到`clawdbot.config.json5`文件中：
```json5
{
  skills: {
    entries: {
      "deepread": {
        enabled: true,
        apiKey: "sk_live_your_key_here"
      }
    }
  }
}
```

### 3. 处理您的第一份文档

**选项A：使用Webhook（推荐）**
```bash
# Upload PDF with webhook notification
curl -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@document.pdf" \
  -F "webhook_url=https://your-app.com/webhooks/deepread"

# Returns immediately
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued"
}

# Your webhook receives results when processing completes (2-5 minutes)
```

**选项B：轮询结果**
```bash
# Upload PDF without webhook
curl -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@document.pdf"

# Returns immediately
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued"
}

# Poll until completed
curl https://api.deepread.tech/v1/jobs/550e8400-e29b-41d4-a716-446655440000 \
  -H "X-API-Key: $DEEPREAD_API_KEY"
```

## 使用示例

### 基本OCR（仅提取文本）

将PDF文件中的文本提取为Markdown格式：
```bash
# With webhook (recommended)
curl -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@invoice.pdf" \
  -F "webhook_url=https://your-app.com/webhook"

# OR poll for completion
curl -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@invoice.pdf"

# Then poll
curl https://api.deepread.tech/v1/jobs/JOB_ID \
  -H "X-API-Key: $DEEPREAD_API_KEY"
```

**处理完成后的响应：**
```json
{
  "id": "550e8400-...",
  "status": "completed",
  "result": {
    "text": "# INVOICE\n\n**Vendor:** Acme Corp\n**Total:** $1,250.00..."
  }
}
```

### 结构化数据提取

提取特定字段并附带置信度评分：
```bash
curl -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@invoice.pdf" \
  -F 'schema={
    "type": "object",
    "properties": {
      "vendor": {
        "type": "string",
        "description": "Vendor company name"
      },
      "total": {
        "type": "number",
        "description": "Total invoice amount"
      },
      "invoice_date": {
        "type": "string",
        "description": "Invoice date in MM/DD/YYYY format"
      }
    }
  }'
```

**响应中包含置信度标记：**
```json
{
  "status": "completed",
  "result": {
    "text": "# INVOICE\n\n**Vendor:** Acme Corp...",
    "data": {
      "vendor": {
        "value": "Acme Corp",
        "hil_flag": false,
        "found_on_page": 1
      },
      "total": {
        "value": 1250.00,
        "hil_flag": false,
        "found_on_page": 1
      },
      "invoice_date": {
        "value": "2024-10-??",
        "hil_flag": true,
        "reason": "Date partially obscured",
        "found_on_page": 1
      }
    },
    "metadata": {
      "fields_requiring_review": 1,
      "total_fields": 3,
      "review_percentage": 33.3
    }
  }
}
```

### 复杂数据结构（嵌套数据）

提取数组和嵌套对象：
```bash
curl -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@invoice.pdf" \
  -F 'schema={
    "type": "object",
    "properties": {
      "vendor": {"type": "string"},
      "total": {"type": "number"},
      "line_items": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "description": {"type": "string"},
            "quantity": {"type": "number"},
            "price": {"type": "number"}
          }
        }
      }
    }
  }'
```

### 分页处理

获取每页的OCR处理结果及质量标记：
```bash
curl -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@contract.pdf" \
  -F "include_pages=true"
```

**响应示例：**
```json
{
  "result": {
    "text": "Combined text from all pages...",
    "pages": [
      {
        "page_number": 1,
        "text": "# Contract Agreement\n\n...",
        "hil_flag": false
      },
      {
        "page_number": 2,
        "text": "Terms and C??diti??s...",
        "hil_flag": true,
        "reason": "Multiple unrecognized characters"
      }
    ],
    "metadata": {
      "pages_requiring_review": 1,
      "total_pages": 2
      }
  }
}
```

## 适用场景

### ✅ 适用于以下场景：
- **发票处理**：提取供应商信息、总计金额、明细项目。
- **收据识别**：解析商家信息、商品明细、总计金额。
- **合同分析**：提取合同双方信息、日期、条款。
- **表单数字化**：将纸质表单转换为结构化数据。
- **任何需要OCR和数据提取的流程**。
- **对结果准确性要求较高的应用**。

### ❌ 不适用以下场景：
- **实时处理**：处理时间约为2-5分钟（异步流程）。
- **每月处理量超过2,000页**：请升级至PRO或SCALE等级。

## 工作原理

### 多轮处理流程

DeepRead采用多轮处理流程，自动完成以下操作：
- 文档的旋转和方向校正。
- 多次验证以确保提取结果的准确性。
- 通过多个模型进行交叉验证以提高可靠性。
- 对每个字段进行置信度评分。

### 质量评估（`hil_flag`）

人工智能系统会将提取的文本与原始图像进行比对，并设置`hil_flag`：
- **`hil_flag: false`**：提取结果清晰、准确 → 自动完成处理。
- **`hil_flag: true`**：提取结果不确定 → 需要人工审核。

**以下情况会导致AI标记为“不确定”：**
- 文本为手写、模糊或质量较低。
- 同一字段存在多种可能的解释。
- 部分字符无法识别或清晰度不足。
- 文档中不存在该字段。

**此判断基于人工智能的智能分析，而非固定规则。**

## 高级功能

### 1. 架构蓝图（优化后的数据模型）

为特定类型的文档创建可重用的、优化后的数据模型：
```bash
# List your blueprints
curl https://api.deepread.tech/v1/blueprints \
  -H "X-API-Key: $DEEPREAD_API_KEY"

# Use blueprint instead of inline schema
curl -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@invoice.pdf" \
  -F "blueprint_id=660e8400-e29b-41d4-a716-446655440001"
```

**优势：**
- 相比基础模型，准确率提升20-30%。
- 可在类似文档中重复使用。
- 支持版本控制及回滚功能。

**如何创建架构蓝图：**
```bash
# Create a blueprint from training data
curl -X POST https://api.deepread.tech/v1/optimize \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "utility_invoice",
    "description": "Optimized for utility invoices",
    "document_type": "invoice",
    "initial_schema": {
      "type": "object",
      "properties": {
        "vendor": {"type": "string", "description": "Vendor name"},
        "total": {"type": "number", "description": "Total amount"}
      }
    },
    "training_documents": ["doc1.pdf", "doc2.pdf", "doc3.pdf"],
    "ground_truth_data": [
      {"vendor": "Acme Power", "total": 125.50},
      {"vendor": "City Electric", "total": 89.25}
    ],
    "target_accuracy": 95.0,
    "max_iterations": 5
  }'

# Returns: {"job_id": "...", "blueprint_id": "...", "status": "pending"}

# Check optimization status
curl https://api.deepread.tech/v1/blueprints/jobs/JOB_ID \
  -H "X-API-Key: $DEEPREAD_API_KEY"

# Use blueprint (once completed)
curl -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@invoice.pdf" \
  -F "blueprint_id=BLUEPRINT_ID"
```

### 2. Webhook（推荐用于生产环境）

处理完成后自动接收通知，无需频繁轮询：
```bash
curl -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@invoice.pdf" \
  -F "webhook_url=https://your-app.com/webhooks/deepread"
```

**处理完成后，Webhook会收到以下响应内容：**
```json
{
  "job_id": "550e8400-...",
  "status": "completed",
  "created_at": "2025-01-27T10:00:00Z",
  "completed_at": "2025-01-27T10:02:30Z",
  "result": {
    "text": "...",
    "data": {...}
  },
  "preview_url": "https://preview.deepread.tech/abc1234"
}
```

**优势：**
- 无需频繁轮询。
- 处理完成后立即收到通知。
- 降低延迟，更适合生产环境。

### 3. 公开预览URL

无需认证即可查看OCR处理结果：
```bash
# Request preview URL
curl -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@document.pdf" \
  -F "include_images=true"

# Get preview URL in response
{
  "result": {
    "text": "...",
    "data": {...}
  },
  "preview_url": "https://preview.deepread.tech/Xy9aB12"
}
```

**公开预览接口：**
```bash
# No authentication required
curl https://api.deepread.tech/v1/preview/Xy9aB12
```

## 计费规则

### 免费 tier
- 每月处理2,000页文档。
- 每分钟最多10次请求。
- 提供全部功能（OCR、结构化数据提取、架构蓝图）。

### 付费计划
- **PRO级**：每月处理50,000页文档，每分钟100次请求，费用为99美元。
- **SCALE级**：根据实际使用量定制价格（请联系销售团队）。

**升级方式：** https://www.deepread.tech/dashboard/billing?utm_source=clawdhub

### 计费相关头部信息

每个响应中都会包含计费相关信息：
```
X-RateLimit-Limit: 2000
X-RateLimit-Remaining: 1847
X-RateLimit-Used: 153
X-RateLimit-Reset: 1730419200
```

## 最佳实践

### 1. 生产环境推荐使用Webhook

**✅ 推荐使用Webhook进行通知：**
```bash
curl -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@document.pdf" \
  -F "webhook_url=https://your-app.com/webhook"
```

**仅在以下情况下使用轮询：**
- 测试/开发阶段。
- 无法公开Webhook接口。
- 需要实时响应。

### 2. 数据模型设计

**✅ 建议为字段添加描述性说明：**
```json
{
  "vendor": {
    "type": "string",
    "description": "Vendor company name. Usually in header or top-left of invoice."
  }
}
```

**不建议的做法：**
- 不为字段添加描述。**

### 3. 轮询策略（仅限无法使用Webhook的情况）

如果无法使用Webhook，请每5-10秒轮询一次：
```python
import time
import requests

def wait_for_result(job_id, api_key):
    while True:
        response = requests.get(
            f"https://api.deepread.tech/v1/jobs/{job_id}",
            headers={"X-API-Key": api_key}
        )
        result = response.json()

        if result["status"] == "completed":
            return result["result"]
        elif result["status"] == "failed":
            raise Exception(f"Job failed: {result.get('error')}")

        time.sleep(5)
```

### 4. 处理质量标记

将确认准确的字段与需要人工审核的字段区分开来：
```python
def process_extraction(data):
    confident = {}
    needs_review = []

    for field, field_data in data.items():
        if field_data["hil_flag"]:
            needs_review.append({
                "field": field,
                "value": field_data["value"],
                "reason": field_data.get("reason")
            })
        else:
            confident[field] = field_data["value"]

    # Auto-process confident fields
    save_to_database(confident)

    # Send uncertain fields to review queue
    if needs_review:
        send_to_review_queue(needs_review)
```

## 常见问题及解决方法

### 错误：`quota_exceeded`
**解决方法：** 升级至PRO等级或等待下一个计费周期。

### 错误：`invalid_schema`
**解决方法：** 确保数据模型为有效的JSON格式，并包含`type`和`properties`字段。

### 错误：`file_too_large`
**解决方法：** 压缩PDF文件或将其分割成较小的文件。

### 任务状态：`failed`
**常见原因：**
- PDF文件损坏。
- PDF文件受密码保护。
- PDF版本不支持OCR处理。
- 图像质量过低，无法进行OCR识别。

## 示例数据模型模板

### 发票数据模型
```json
{
  "type": "object",
  "properties": {
    "invoice_number": {
      "type": "string",
      "description": "Unique invoice ID"
    },
    "invoice_date": {
      "type": "string",
      "description": "Invoice date in MM/DD/YYYY format"
    },
    "vendor": {
      "type": "string",
      "description": "Vendor company name"
    },
    "total": {
      "type": "number",
      "description": "Total amount due including tax"
    },
    "line_items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "description": {"type": "string"},
          "quantity": {"type": "number"},
          "price": {"type": "number"}
        }
      }
    }
  }
}
```

### 收据数据模型
```json
{
  "type": "object",
  "properties": {
    "merchant": {
      "type": "string",
      "description": "Store or merchant name"
    },
    "date": {
      "type": "string",
      "description": "Transaction date"
    },
    "total": {
      "type": "number",
      "description": "Total amount paid"
    },
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "price": {"type": "number"}
        }
      }
    }
  }
}
```

### 合同数据模型
```json
{
  "type": "object",
  "properties": {
    "parties": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Names of all parties in the contract"
    },
    "effective_date": {
      "type": "string",
      "description": "Contract start date"
    },
    "term_length": {
      "type": "string",
      "description": "Duration of contract"
    },
    "termination_clause": {
      "type": "string",
      "description": "Conditions for termination"
    }
  }
}
```

## 技术支持与资源

- **GitHub仓库**：https://github.com/deepread-tech
- **问题反馈**：https://github.com/deepread-tech/deep-read-service/issues
- **联系邮箱**：hello@deepread.tech

### 重要提示：
- **处理时间**：2-5分钟（异步处理，非实时响应）。
- **建议使用Webhook或轮询机制**。
- **免费 tier的请求限制**：每分钟10次请求。
- **文件大小限制**：每份文件不超过50MB。
- **支持的文件格式**：PDF、JPG、JPEG、PNG。

**准备好开始使用了吗？** 请访问[https://www.deepread.tech/dashboard/?utm_source=clawdhub]获取您的免费API密钥。