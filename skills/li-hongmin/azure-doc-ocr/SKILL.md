---
name: azure-doc-ocr
description: >
  使用 Azure Document Intelligence（前身为 Form Recognizer）从文档中提取文本和结构化数据。  
  支持对 PDF 文件、图片、扫描文档、手写文本、中文（CJK）语言、表格、表单、发票、收据、身份证件、名片以及税务表格进行光学字符识别（OCR）处理。  
  该服务基于 REST API v4.0（2024-11-30）进行开发，针对各种文档类型提供了预先构建的模型。  
  支持的功能包括：  
  - OCR（光学字符识别）  
  - 文本提取  
  - Azure Document Intelligence  
  - PDF 文件的 OCR 处理  
  - 图片的 OCR 处理  
  - 手写文本识别  
  - 中文（CJK）文本提取  
  - 表格提取  
  - 发票处理  
  - 收据扫描  
  - 身份证件识别  
  - 文档解析  
  - 表单提取  
  - Azure Form Recognizer（用于表单数据的提取和处理）
---
# Azure Document Intelligence OCR

使用 Azure Document Intelligence 的 REST API 从文档中提取文本和结构化数据。

## 快速入门

### 1. 环境设置

配置您的 Azure Document Intelligence 凭据：

```bash
export AZURE_DOC_INTEL_ENDPOINT="https://your-resource.cognitiveservices.azure.com"
export AZURE_DOC_INTEL_KEY="your-api-key"
```

### 2. 单个文件 OCR

```bash
# Basic text extraction from PDF
python scripts/ocr_extract.py document.pdf

# Extract with layout (tables, structure)
python scripts/ocr_extract.py document.pdf --model prebuilt-layout --format markdown

# Process invoice
python scripts/ocr_extract.py invoice.pdf --model prebuilt-invoice --format json

# OCR from URL
python scripts/ocr_extract.py --url "https://example.com/document.pdf"

# Save output to file
python scripts/ocr_extract.py document.pdf --output result.txt

# Extract specific pages
python scripts/ocr_extract.py document.pdf --pages 1-3,5
```

### 3. 批量处理

```bash
# Process all documents in a folder
python scripts/batch_ocr.py ./documents/

# Custom output directory and format
python scripts/batch_ocr.py ./documents/ --output-dir ./extracted/ --format markdown

# Use layout model with 8 workers
python scripts/batch_ocr.py ./documents/ --model prebuilt-layout --workers 8

# Filter specific extensions
python scripts/batch_ocr.py ./documents/ --ext .pdf,.png
```

## 模型选择指南

| 文档类型 | 推荐模型 | 使用场景 |
|---------------|-------------------|----------|
| 通用文本 | `prebuilt-read` | 纯文本提取，适用于任何文档 |
| 结构化文档 | `prebuilt-layout` | 表格、表单、段落、图表 |
| 发票 | `prebuilt-invoice` | 供应商信息、项目明细、总计金额 |
| 收据 | `prebuilt-receipt` | 商户信息、项目明细、总计金额、日期 |
| 身份证/护照 | `prebuilt-idDocument` | 身份证明文件 |
| 名片 | `prebuilt-businessCard` | 联系信息 |
| W-2 表格 | `prebuilt-tax.us.w2` | 美国税务文件 |
| 保险卡 | `prebuilt-healthInsuranceCard.us` | 健康保险信息 |

有关详细模型文档，请参阅 [references/models.md](references/models.md)。

## 支持的输入格式

- **PDF**: `.pdf`（包括扫描的 PDF 文件）
- **图片**: `.png`, `.jpg`, `.jpeg`, `.tiff`, `.bmp`
- **URL**: 文档的直接链接

## 输出格式

- **文本**: 所有提取内容的纯文本拼接
- **markdown**: 带有标题和表格的结构化输出（使用布局模型效果最佳）
- **json**: 包含完整提取细节的原始 API 响应

## 特性

- **手写识别**: 可同时识别手写文本和印刷文本
- **支持 CJK 字符**: 完全支持中文、日文、韩文字符
- **表格提取**: 保留表格结构（使用布局模型）
- **多页处理**: 支持处理多页文档
- **并发处理**: 批量脚本支持并行处理
- **URL 输入**: 直接从 URL 处理文档

## 环境变量

| 变量 | 是否必填 | 描述 |
|----------|----------|-------------|
| `AZURE_DOC_INTEL_ENDPOINT` | 是 | Azure Document Intelligence 的 API 端点 URL |
| `AZURE_DOC_INTEL_KEY` | 是 | API 订阅密钥 |

## 错误处理

- 无效凭据: 检查 API 端点 URL 和密钥
- 不支持的格式: 确保文件扩展名与支持的类型匹配
- 超时: 大型文档可能需要更长的处理时间（最长 300 秒）
- 速率限制: 批量处理时请减少并发任务的数量

## 示例

### 从扫描的 PDF 文件中提取文本

```bash
python scripts/ocr_extract.py scanned_contract.pdf --model prebuilt-read
```

### 处理发票并生成结构化输出

```bash
python scripts/ocr_extract.py invoice.pdf --model prebuilt-invoice --format json --output invoice_data.json
```

### 使用布局分析进行批量处理

```bash
python scripts/batch_ocr.py ./reports/ --model prebuilt-layout --format markdown --workers 4
```

### 从大型文档中提取特定页面

```bash
python scripts/ocr_extract.py large_doc.pdf --pages 1,3-5,10 --format text
```