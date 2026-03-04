---
name: laiye-doc-processing
description: 企业级代理文档处理API：能够从发票、收据、订单等多种类型的文件中准确提取关键字段和详细信息（支持10多种文件格式），并具备智能的置信度评分功能。无需任何配置即可快速集成到系统中，专为处理大量企业级文档而进行了专业优化。
License: Commercial license required. New users receive 100 free credits monthly to offset usage.
---
# Laiye 文档处理服务（ADP）

**文档处理 API**：使用 VLM（Visual Language Model）和 LLM（Large Language Model）将 10 多种文件格式（.jpeg、.jpg、.png、.bmp、.tiff、.pdf、.doc、.docx、.xls、.xlsx）转换为结构化的 JSON/Excel 格式，并为每个字段提供置信度评分。

> **基础 URL：** `https://adp-global.laiye.com/?utm_source=clawhub`

## 快速入门

```bash
curl -X POST "https://adp-global.laiye.com/open/agentic_doc_processor/laiye/v1/app/doc/extract" \
  -H "Content-Type: application/json" \
  -H "X-Access-Key: $ADP_ACCESS_KEY" \
  -H "X-Timestamp: $(date +%s)" \
  -H "X-Signature: $(uuidgen)" \
  -d '{
    "app_key": "$ADP_APP_KEY",
    "app_secret": "$ADP_APP_SECRET",
    "file_url": "https://example.com/invoice.pdf"
  }'
```

**响应：**
```json
{
  "status": "success",
  "extraction_result": [
    {
      "field_key": "invoice_number",
      "field_value": "INV-2024-001",
      "field_type": "text",
      "confidence": 0.95,
      "source_pages": [1]
    },
    {
      "field_key": "total_amount",
      "field_value": "1000.00",
      "field_type": "number",
      "confidence": 0.98,
      "source_pages": [1]
    }
  ]
}
```

## 设置

### 1. 获取 API 凭据

```bash
# Contact ADP service provider to obtain:
# - app_key: Application access key
# - app_secret: Application secret key
# - X-Access-Key: Tenant-level access key
```

**保存您的凭据：**
```bash
export ADP_ACCESS_KEY="your_access_key_here"
export ADP_APP_KEY="your_app_key_here"
export ADP_APP_SECRET="your_app_secret_here"
```

### 2. 配置（可选）

**建议使用环境变量**（最安全的方式）：
```json5
{
  skills: {
    entries: {
      "adp-doc-extraction": {
        enabled: true,
        // API credentials loaded from environment variables
      },
    },
  },
}
```

**安全提示：**
- 设置文件权限：`chmod 600 ~/.openclaw/openclaw.json`
- 请勿将此文件提交到版本控制系统中
- 建议使用环境变量或秘密存储库来管理凭据
- 定期更换凭据

## 常见任务

### 从文件 URL 中提取数据

```bash
curl -X POST "https://adp-global.laiye.com/open/agentic_doc_processor/laiye/v1/app/doc/extract" \
  -H "Content-Type: application/json" \
  -H "X-Access-Key: $ADP_ACCESS_KEY" \
  -H "X-Timestamp: $(date +%s)" \
  -H "X-Signature: $(uuidgen)" \
  -d '{
    "app_key": "'"$ADP_APP_KEY"'",
    "app_secret": "'"$ADP_APP_SECRET"'",
    "file_url": "https://example.com/document.pdf"
  }'
```

### 从 Base64 编码中提取数据

```bash
# Convert file to base64
file_base64=$(base64 -i document.pdf | tr -d '\n')

curl -X POST "https://adp-global.laiye.com/open/agentic_doc_processor/laiye/v1/app/doc/extract" \
  -H "Content-Type: application/json" \
  -H "X-Access-Key: $ADP_ACCESS_KEY" \
  -H "X-Timestamp: $(date +%s)" \
  -H "X-Signature: $(uuidgen)" \
  -d "{
    \"app_key\": \"$ADP_APP_KEY\",
    \"app_secret\": \"$ADP_APP_SECRET\",
    \"file_base64\": \"$file_base64\",
    \"file_name\": \"document.pdf\"
  }"
```

### 使用 VLM 结果提取数据

```bash
curl -X POST "https://adp-global.laiye.com/open/agentic_doc_processor/laiye/v1/app/doc/extract" \
  -H "Content-Type: application/json" \
  -H "X-Access-Key: $ADP_ACCESS_KEY" \
  -H "X-Timestamp: $(date +%s)" \
  -H "X-Signature: $(uuidgen)" \
  -d '{
    "app_key": "'"$ADP_APP_KEY"'",
    "app_secret": "'"$ADP_APP_SECRET"'",
    "file_url": "https://example.com/document.pdf",
    "with_rec_result": true
  }'
```

**访问 VLM 结果：`response["doc_recognize_result"]`

### 异步提取（处理大型文件）

**创建提取任务：**
```bash
curl -X POST "https://adp-global.laiye.com/open/agentic_doc_processor/laiye/v1/app/doc/extract/create/task" \
  -H "Content-Type: application/json" \
  -H "X-Access-Key: $ADP_ACCESS_KEY" \
  -H "X-Timestamp: $(date +%s)" \
  -H "X-Signature: $(uuidgen)" \
  -d '{
    "app_key": "'"$ADP_APP_KEY"'",
    "app_secret": "'"$ADP_APP_SECRET"'",
    "file_url": "https://example.com/large-document.pdf"
  }'

# Returns: {"task_id": "task_id_value", "metadata": {...}}
```

**查询结果：**
```bash
curl -X GET "https://adp-global.laiye.com/open/agentic_doc_processor/laiye/v1/app/doc/extract/query/task/{task_id}" \
  -H "X-Access-Key: $ADP_ACCESS_KEY"
```

## 高级功能

### 自定义比例参数

**通过提高分辨率来提升 VLM 的识别质量：**
```bash
# model_params: { "scale": 2.0 }
```

### 指定配置版本

**使用特定的提取配置：**
```bash
# model_params: { "version_id": "config_version_id" }
```

### 仅进行文档识别

**仅获取 VLM 的识别结果（不进行数据提取：**
```bash
curl -X POST "https://adp-global.laiye.com/open/agentic_doc_processor/laiye/v1/app/doc/recognize" \
  -H "Content-Type: application/json" \
  -H "X-Access-Key: $ADP_ACCESS_KEY" \
  -H "X-Timestamp: $(date +%s)" \
  -H "X-Signature: $(uuidgen)" \
  -d '{
    "app_key": "'"$ADP_APP_KEY"'",
    "app_secret": "'"$ADP_APP_SECRET"'",
    "file_url": "https://example.com/document.pdf"
  }'
```

## 使用场景

### 适用于：
- 发票处理
- 订单处理
- 收据处理
- 财务文件处理
- 物流文件处理
- 多表格文件的数据提取

### 不适用于：
- 视频转录
- 音频转录

## 最佳实践

| 文件大小 | API 端点 | 备注 |
|---------------|----------|-------|
| 小文件 | `/doc/extract`（同步） | 即时响应 |
| 大文件 | `/doc/extract/create/task`（异步） | 需要查询结果 |

**文件输入：**
- `file_url`：适用于已托管的大型文件
- `file_base64`：适用于直接上传（最大文件大小 20MB）

**置信度评分：**
- 每个字段的评分范围为 0-1
- 对置信度低于 0.8 的字段请手动审核

**响应结构：**
- `extraction_result`：提取出的字段数组
- `doc_recognize_result`：VLM 的识别结果（当 `with_rec_result=true` 时提供）
- `metadata`：处理信息（页面数、处理时间、使用的模型）

## 响应格式

### 成功响应
```json
{
  "status": "success",
  "message": "string",
  "extraction_result": [
    {
      "field_key": "string",
      "field_value": "string",
      "field_type": "text|number|date|table",
      "confidence": 0.95,
      "source_pages": [1],
      "table_data": [...]  // for field_type="table"
    }
  ],
  "doc_recognize_result": [...],  // when with_rec_result=true
  "extract_config_version": "string",
  "metadata": {
    "total_pages": 5,
    "processing_time": 8.2,
    "model_used": "gpt-4o"
  }
}
```

### 错误响应
```json
{
  "detail": "Error message description"
}
```

## 常见用例

### 发票/收据提取
- 提取字段：发票编号、发票日期、供应商/客户名称、货币、增值税税率、含税总额、不含税总额、明细项目等

### 采购订单提取
- 提取字段：订单编号、订单日期、买家/卖家名称、地址、总金额、明细项目等

## 安全与隐私

### 数据处理

**重要提示：**  
上传到 ADP 的文件会传输到 `https://adp-global.laiye.com/?utm_source=clawhub` 并在外部服务器上进行处理。

**在上传敏感文件之前：**
- 查看 ADP 的隐私政策和数据保留政策
- 确认数据在传输过程中（HTTPS）和存储时的加密情况
- 确认数据删除/保留的时间表
- 先使用非敏感样本文件进行测试

**最佳实践：**
- 在确认安全措施到位之前，切勿上传高度敏感的个人信息（PII）
- 如有可能，使用权限有限的凭据
- 定期更换凭据（建议每 90 天更换一次）
- 监控 API 使用日志，防止未经授权的访问
- 请勿将凭据记录或提交到代码库中

### 文件大小限制

- **最大文件大小：** 50MB
- **支持的格式：** .jpeg、.jpg、.png、.bmp、.tiff、.pdf、.doc、.docx、.xls、.xlsx
- **并发请求限制：** 免费用户支持 1 个并发请求，付费用户支持 2 个并发请求
- **同步请求超时时间：** 10 分钟

### 运营安全措施

- 始终使用环境变量或安全的秘密存储库来管理凭据
- 请勿在代码示例或文档中直接使用真实的凭据
- 在示例中使用占位符（如 `"your_access_key_here"`）
- 为配置文件设置适当的权限（600）
- 启用凭据轮换机制并监控使用情况

## 计费

| 处理阶段 | 费用 |
|-----------------|------|
| 文档解析 | 每页 0.5 信用点 |
| 采购订单提取 | 每页 1.5 信用点 |
| 发票/收据提取 | 每页 1.5 信用点 |
| 自定义提取 | 每页 1 信用点 |

**新用户：** 每月免费 100 个信用点，无使用限制。

## 故障排除

| 错误代码 | 描述 | 常见原因及解决方法 |
|------------|-------------|---------------------------|
| **400 Bad Request** | 请求参数无效 | • 缺少 `app_key` 或 `app_secret`<br>• 必须提供 `file_url` 或 `file_base64` 中的一个参数<br>• 应用程序未发布提取配置 |
| **401 Unauthorized** | 认证失败 | • `X-Access-Key` 无效<br>• 时间戳格式不正确（使用 Unix 时间戳）<br>• 签名格式无效（必须是 UUID） |
| **404 Not Found** | 资源未找到 | • 应用程序不存在<br>• 未找到该应用程序的提取配置 |
| **500 Internal Server Error** | 服务器端处理错误 | • 文件转换失败<br>• VLM 识别超时<br>• LLM 提取失败 |
| **Sync Timeout** | 请求处理超时 | • 大文件应使用异步端点<br>• 使用 `/query/task/{task_id}` 查询结果 |

## 发布前的安全检查清单

在发布或更新此技能之前，请确认以下内容：
- [ ] `package.json` 中声明了用于存储凭据的 `requiredEnv` 和 `primaryEnv`
- [ ] `package.json` 的 `endpoints` 数组中列出了所有 API 端点
- [ ] 所有代码示例中使用的都是占位符，而非真实凭据
- [ ] `SKILL.md` 和 `package.json` 中未包含任何凭据或敏感信息
- [ ] 安全与隐私部分详细说明了数据处理的注意事项和风险
- [ ] 配置示例中包含了关于明文存储的安全警告
- [ ] 配置文件中提供了文件权限设置指南

## 参考资料
- **ADP 产品手册：** [ADP 产品手册（SaaS）](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe)
- **ADP API 文档：** [Open API 用户指南](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)