---
name: docstrange
description: Nanonets提供的文档提取API：能够将PDF文件和图像转换为Markdown、JSON或CSV格式，并附带置信度评分。适用于需要进行OCR处理、提取发票信息、解析收据内容或将表格数据转换为结构化格式的场景。
---

# DocStrange 由 Nanonets 提供

**文档提取 API** — 将 PDF、图片和文档转换为 Markdown、JSON 或 CSV 格式，并为每个字段提供置信度评分。

> **获取您的 API 密钥：** https://docstrange.nanonets.com/app

## 快速入门

```bash
curl -X POST "https://extraction-api.nanonets.com/api/v1/extract/sync" \
  -H "Authorization: Bearer $DOCSTRANGE_API_KEY" \
  -F "file=@document.pdf" \
  -F "output_format=markdown"
```

**响应：**
```json
{
  "success": true,
  "record_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "result": {
    "markdown": {
      "content": "# Invoice\n\n**Invoice Number:** INV-2024-001..."
    }
  }
}
```

## 设置

### 1. 获取您的 API 密钥

```bash
# Visit the dashboard
https://docstrange.nanonets.com/app
```

**保存您的 API 密钥：**
```bash
export DOCSTRANGE_API_KEY="your_api_key_here"
```

### 2. OpenClaw 配置（可选）

**推荐：使用环境变量**（最安全的方式）：
```json5
{
  skills: {
    entries: {
      "docstrange": {
        enabled: true,
        // API key loaded from environment variable DOCSTRANGE_API_KEY
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
      "docstrange": {
        enabled: true,
        env: {
          DOCSTRANGE_API_KEY: "your_api_key_here",
        },
      },
    },
  },
}
```

**安全提示：** 如果将 API 密钥存储在 `~/.openclaw/openclaw.json` 中：  
- 设置文件权限：`chmod 600 ~/.openclaw/openclaw.json`  
- 绝不要将此文件提交到版本控制系统中  
- 尽可能使用环境变量或代理的秘密存储机制  
- 定期更换 API 密钥，并在支持的情况下限制 API 密钥的权限

## 常见任务

### 提取到 Markdown 格式

```bash
curl -X POST "https://extraction-api.nanonets.com/api/v1/extract/sync" \
  -H "Authorization: Bearer $DOCSTRANGE_API_KEY" \
  -F "file=@document.pdf" \
  -F "output_format=markdown"
```

**访问内容：`response["result"]["markdown"]["content"]`

### 提取 JSON 字段**

**简单的字段列表：**
```bash
curl -X POST "https://extraction-api.nanonets.com/api/v1/extract/sync" \
  -H "Authorization: Bearer $DOCSTRANGE_API_KEY" \
  -F "file=@invoice.pdf" \
  -F "output_format=json" \
  -F 'json_options=["invoice_number", "date", "total_amount", "vendor"]' \
  -F "include_metadata=confidence_score"
```

**使用 JSON 架构：**
```bash
curl -X POST "https://extraction-api.nanonets.com/api/v1/extract/sync" \
  -H "Authorization: Bearer $DOCSTRANGE_API_KEY" \
  -F "file=@invoice.pdf" \
  -F "output_format=json" \
  -F 'json_options={"type": "object", "properties": {"invoice_number": {"type": "string"}, "total_amount": {"type": "number"}}}'
```

**包含置信度评分的响应：**
```json
{
  "result": {
    "json": {
      "content": {
        "invoice_number": "INV-2024-001",
        "total_amount": 500.00
      },
      "metadata": {
        "confidence_score": {
          "invoice_number": 98,
          "total_amount": 99
        }
      }
    }
  }
}
```

### 将表格提取到 CSV 格式

```bash
curl -X POST "https://extraction-api.nanonets.com/api/v1/extract/sync" \
  -H "Authorization: Bearer $DOCSTRANGE_API_KEY" \
  -F "file=@table.pdf" \
  -F "output_format=csv" \
  -F "csv_options=table"
```

### 异步提取（大型文档）**

对于超过 5 页的文档，请使用异步提取方式：

**排队处理文档：**
```bash
curl -X POST "https://extraction-api.nanonets.com/api/v1/extract/async" \
  -H "Authorization: Bearer $DOCSTRANGE_API_KEY" \
  -F "file=@large-document.pdf" \
  -F "output_format=markdown"

# Returns: {"record_id": "12345", "status": "processing"}
```

**获取结果：**
```bash
curl -X GET "https://extraction-api.nanonets.com/api/v1/extract/results/12345" \
  -H "Authorization: Bearer $DOCSTRANGE_API_KEY"

# Returns: {"status": "completed", "result": {...}}
```

## 高级功能

### 获取元素坐标（用于布局分析）  
```bash
-F "include_metadata=bounding_boxes"
```

### 提取文档结构（章节、表格、键值对）  
```bash
-F "json_options=hierarchy_output"
```

### 金融文档模式  
**增强表格和数字格式化：**  
```bash
-F "markdown_options=financial-docs"
```

### 自定义指令  
**通过提示指导提取过程：**  
```bash
-F "custom_instructions=Focus on financial data. Ignore headers."
-F "prompt_mode=append"
```

### 多种格式  
**一次请求多种格式：**  
```bash
-F "output_format=markdown,json"
```

## 适用场景

### 适用于以下场景：  
- 发票和收据处理  
- 合同文本提取  
- 银行对账单解析  
- 表单数字化  
- 图像 OCR（扫描文档）  

### 不适用场景：  
- 超过 5 页的文档（建议使用异步提取）  
- 视频/音频转录  
- 非文档类型的图片  

## 最佳实践

| 文档大小 | API 端点 | 备注 |
|---------------|----------|-------|
| ≤5 页 | `/extract/sync` | 即时响应 |
| >5 页 | `/extract/async` | 异步获取结果 |

**JSON 提取：**  
- 字段列表：`["field1", "field2"]` — 快速提取  
- JSON 架构：`{"type": "object", ...}` — 严格的数据类型定义和嵌套结构  

**置信度评分：**  
- 使用 `include_metadata=confidence_score` 参数  
- 每个字段的评分范围为 0-100  
- 对评分低于 80 分的字段需手动审核  

## 架构模板

### 发票  
```json
{
  "type": "object",
  "properties": {
    "invoice_number": {"type": "string"},
    "date": {"type": "string"},
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
}
```

### 收据  
```json
{
  "type": "object",
  "properties": {
    "merchant": {"type": "string"},
    "date": {"type": "string"},
    "total": {"type": "number"},
    "items": {
      "type": "array",
      "items": {"type": "object", "properties": {"name": {"type": "string"}, "price": {"type": "number"}}}
    }
  }
}
```

## 安全与隐私

### 数据处理

**重要提示：** 上传到 DocStrange 的文档会被传输到 `https://extraction-api.nanonets.com` 并在外部服务器上进行处理。**

**在上传敏感文档之前：**  
- 查看 Nanonets 的隐私政策和数据保留政策：https://docstrange.nanonets.com/docs  
- 确认数据在传输过程中（使用 HTTPS）和存储时都经过加密  
- 确认数据删除/保留的时间安排  
- 先使用非敏感样本文档进行测试  

**最佳实践：**  
- 在确认服务的安全性和合规性之前，切勿上传高度敏感的个人信息（如 SSN、医疗记录、财务账户号码）  
- 如果可能，使用权限和范围有限的 API 密钥  
- 定期更换 API 密钥（建议每 90 天更换一次）  
- 监控 API 使用日志，防止未经授权的访问  
- 绝不要将 API 密钥记录或提交到代码库或示例文件中  

### 文件大小限制  

- **同步端点：** 适用于 ≤5 页的文档  
- **异步端点：** 适用于超过 5 页的文档，以避免超时  
- **大文件：** 考虑使用公开可访问的 URL（`file_url`）而不是直接上传大文件  

### 操作安全措施  

- 始终使用环境变量或安全的秘密存储机制来管理 API 密钥  
- 绝不要在代码示例或文档中包含真实的 API 密钥  
- 在示例中使用占位符值（如 `"your_api_key_here"`）  
- 为配置文件设置适当的文件权限（JSON 配置文件权限设置为 600）  
- 启用 API 密钥的定期更换功能，并通过仪表板监控使用情况  

## 故障排除

**400 错误：**  
- 请提供以下其中一项输入：`file`、`file_url` 或 `file_base64`  
- 确保 API 密钥有效  

**同步超时：**  
- 对于超过 5 页的文档，请使用异步提取方式  
- 使用 `/extract/results/{record_id}` 来获取结果  

**缺少置信度评分：**  
- 需要设置 `json_options` 参数（字段列表或 JSON 架构）  
- 添加 `include_metadata=confidence_score` 参数  

**认证错误：**  
- 确保设置了 `DOCSTRANGE_API_KEY` 环境变量  
- 检查 API 密钥是否过期或已被吊销  
- 确保 API 密钥的值中没有多余的空白字符  

## 发布前的安全检查清单

在发布或更新此技能之前，请确认以下内容：  
- [ ] `package.json` 文件中声明了 `requiredEnv` 和 `primaryEnv`，并指定了 `DOCSTRANGE_API_KEY`  
- [ ] `package.json` 文件中的 `endpoints` 数组中列出了所有 API 端点  
- **所有代码示例** 都使用了占位符值（如 `"your_api_key_here"`，而非真实密钥  
- **SKILL.md` 和 `package.json` 中没有包含任何 API 密钥或敏感信息  
- **安全与隐私部分** 包含了数据处理的注意事项和风险说明  
- **配置示例** 中包含了关于明文存储的安全警告  
- **配置文件** 中提供了文件权限设置的相关指导  

## 参考资料  

- **API 文档：** https://docstrange.nanonets.com/docs  
- **获取 API 密钥：** https://docstrange.nanonets.com/app  
- **隐私政策：** https://docstrange.nanonets.com/docs （查看隐私/数据政策链接）