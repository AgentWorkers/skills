---
name: deepread
description: 这是一个原生支持人工智能（AI）的OCR（光学字符识别）平台，能够在几分钟内将文档转换为高精度的数据。通过采用多模型协同处理技术，DeepRead的识别准确率可达到95%以上，并且仅标记出需要人工审核的不确定字段，从而将手动处理的工作量从100%降低到5%-10%。该平台完全不需要任何提示工程（prompt engineering）的设置。
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["DEEPREAD_API_KEY"]
      },
      "primaryEnv": "DEEPREAD_API_KEY",
      "homepage": "https://www.deepread.tech"
    }
  }
---

# DeepRead – 生产级OCR API

DeepRead是一个基于人工智能的OCR平台，能够在几分钟内将文档转换成高精度的数据。通过多模型协同处理，DeepRead的准确率可达到95%以上，并仅标记出需要人工审核的不确定字段，从而将手动工作量从100%降低到5-10%。无需进行任何提示工程（prompt engineering）设置。

## 该技能的功能

DeepRead是一个适用于生产环境的文档处理API，能够在几分钟内提供高精度、结构化的数据输出，并通过人工审核来标记需要处理的异常情况，从而将人工审核的范围限制在标记出的异常字段内。

**核心功能：**
- **文本提取**：将PDF文件和图片转换为格式清晰的Markdown格式。
- **结构化数据**：提取带有置信度评分的JSON字段。
- **质量标记**：对不确定的字段进行人工审核标记（`hil_flag`）。
- **多轮处理**：通过多次验证来确保最高的准确率。
- **多模型协同**：通过模型间的交叉验证来提高可靠性。
- **免费 tier**：每月2000页（无需信用卡）。

## 设置

### 1. 获取您的API密钥

注册并创建一个API密钥：
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

将以下配置添加到您的`clawdbot.config.json5`文件中：
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

将文本提取为格式清晰的Markdown格式：
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

获取每页的OCR结果及质量标记：
```bash
curl -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@contract.pdf" \
  -F "include_pages=true"
```

**响应：**
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
- **发票处理**：提取供应商信息、总金额、明细项目。
- **收据OCR**：解析商家信息、商品项目、总金额。
- **合同分析**：提取合同各方信息、日期、条款。
- **表单数字化**：将纸质表单转换为结构化数据。
- **任何需要OCR和数据提取的流程**。
- **对准确性要求较高的应用**：需要了解哪些提取内容存在不确定性时。

### ❌ 不适用于以下场景：
- **实时处理**：处理时间需要2-5分钟（异步工作流程）。
- **每月处理量超过2000页**：请升级到PRO或SCALE等级。

## 工作原理

### 多轮处理流程

该流程自动完成以下操作：
- 文档的旋转和方向校正。
- 多轮验证以确保准确率。
- 通过模型间的交叉验证来提高可靠性。
- 对每个字段进行置信度评分。

### 质量审核（`hil_flag`）

AI会将提取的文本与原始图片进行比对，并设置`hil_flag`：
- **`hil_flag: false`**：提取内容清晰、准确 → 自动处理。
- **`hil_flag: true`**：提取内容不确定 → 需要人工审核。

**AI会在以下情况下标记需要审核的内容：**
- 文本为手写、模糊或质量较低。
- 存在多种可能的解释。
- 部分字符不可见或不清楚。
- 文档中不存在该字段。

**这是基于人工智能的判断，而非基于规则的判断。**

## 高级功能

### 1. 设计蓝图（优化后的数据结构）

为特定类型的文档创建可重用的、优化后的数据结构：
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
- 与基础数据结构相比，准确率提高20-30%。
- 可在类似文档中重复使用。
- 支持版本控制及回滚功能。

**如何创建蓝图：**
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

处理完成后接收通知，无需轮询：
```bash
curl -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@invoice.pdf" \
  -F "webhook_url=https://your-app.com/webhooks/deepread"
```

**处理完成后，您的Webhook会收到以下数据：**
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
- 无需轮询。
- 处理完成后立即收到通知。
- 延迟更低。
- 更适合生产环境。

### 3. 公开预览URL

无需认证即可共享OCR结果：
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

**公开预览端点：**
```bash
# No authentication required
curl https://api.deepread.tech/v1/preview/Xy9aB12
```

## 计费限制与价格

### 免费 tier
- 每月2000页。
- 每分钟10次请求。
- 全部功能可用（OCR + 结构化数据提取 + 设计蓝图）。

### 付费计划
- **PRO**：每月50,000页，每分钟100次请求，费用为99美元/月。
- **SCALE**：根据使用量定制价格（请联系销售团队）。

**升级方式：** https://www.deepread.tech/dashboard/billing?utm_source=clawdhub

### 计费限制相关头信息

每个响应都会包含计费限制信息：
```
X-RateLimit-Limit: 2000
X-RateLimit-Remaining: 1847
X-RateLimit-Used: 153
X-RateLimit-Reset: 1730419200
```

## 最佳实践

### 1. 生产环境中建议使用Webhook

**✅ 推荐使用Webhook通知：**
```bash
curl -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@document.pdf" \
  -F "webhook_url=https://your-app.com/webhook"
```

**仅在以下情况下使用轮询：**
- 测试/开发阶段。
- 无法公开Webhook端点。
- 需要同步响应。

### 2. 数据结构设计

**✅ 好的设计：** 为字段提供详细的描述。
```json
{
  "vendor": {
    "type": "string",
    "description": "Vendor company name. Usually in header or top-left of invoice."
  }
}
```

**❌ 不好的设计：** 不提供字段描述。
```json
{
  "vendor": {"type": "string"}
}
```

### 3. 轮询策略（如需使用）

仅在无法使用Webhook的情况下，每5-10秒轮询一次：
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

将准确提取的字段与不确定的字段区分开来：
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

## 故障排除

### 错误：`quota_exceeded`
**解决方法：** 升级到PRO等级或等待下一个计费周期。

### 错误：`invalid_schema`
**解决方法：** 确保数据结构是有效的JSON格式，并包含`type`和`properties`字段。

### 错误：`file_too_large`
**解决方法：** 压缩PDF文件或将其分割成较小的文件。

### 任务状态：`failed`
**常见原因：**
- PDF文件损坏。
- PDF文件受密码保护。
- PDF版本不支持OCR处理。
- 图像质量过低，无法进行OCR处理。

## 示例数据结构模板

### 发票数据结构
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

### 收据数据结构
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

### 合同数据结构
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

## 支持与资源

- **GitHub**：https://github.com/deepread-tech
- **问题反馈**：https://github.com/deepread-tech/deep-read-service/issues
- **邮箱**：hello@deepread.tech

### 重要说明
- **处理时间**：2-5分钟（异步处理，非实时）。
- **建议使用Webhook或轮询机制。**
- **免费 tier的请求限制**：每分钟10次请求。
- **文件大小限制**：每份文件不超过50MB。
- **支持的格式**：PDF、JPG、JPEG、PNG。

---

**准备好开始使用了吗？** 请访问 [https://www.deepread.tech/dashboard/?utm_source=clawdhub] 获取您的免费API密钥。