---
name: stirling-pdf
description: 通过 Stirling-PDF API 进行 PDF 操作：合并、分割、转换、OCR（光学字符识别）、压缩、签名、内容编辑等。支持自托管部署。
metadata:
  openclaw:
    emoji: 📄
    requires:
      bins: [node, curl]
    env: {
      STIRLING_PDF_URL: "http://localhost:8080",
      STIRLING_API_KEY: "",
    }
---

# Stirling-PDF 技能

这是一个自托管的 PDF 处理平台，通过 REST API 提供了 60 多种工具。

## 配置

设置以下环境变量：
- `STIRLING_PDF_URL` — 您的 Stirling-PDF 实例 URL（默认：`http://localhost:8080`）
- `STIRLING_API_KEY` — 如果启用了身份验证，则需要设置 API 密钥

## 文档

- **官方文档：** https://docs.stirlingpdf.com
- **Swagger UI：** 在您的部署环境中访问 `<your-instance>/swagger-ui/index.html`

## 快速命令

```bash
# Use the wrapper script
node ~/.openclaw/skills/stirling-pdf/scripts/pdf.js <operation> [options]

# Examples:
node pdf.js merge file1.pdf file2.pdf -o merged.pdf
node pdf.js split input.pdf -o ./output-dir
node pdf.js compress input.pdf -o compressed.pdf
node pdf.js ocr input.pdf -o searchable.pdf
node pdf.js convert-to-pdf document.docx -o output.pdf
node pdf.js pdf-to-word input.pdf -o output.docx
node pdf.js add-watermark input.pdf "DRAFT" -o watermarked.pdf
```

## 可用的操作

### 页面操作
- `merge` - 合并多个 PDF 文件
- `split` - 将 PDF 文件分割成多个部分
- `rotate` - 旋转页面
- `extract-pages` - 提取特定页面
- `reorder` - 重新排列页面顺序

### 转换
- `convert-to-pdf` - 将 Word、Excel、图片、HTML 文件转换为 PDF
- `pdf-to-word` - 将 PDF 文件转换为 Word 文档
- `pdf-to-image` - 将 PDF 文件转换为图片
- `pdf-to-text` - 从 PDF 文件中提取文本

### 内容操作
- `compress` - 压缩文件大小
- `ocr` - 使扫描的 PDF 文件可搜索
- `add-watermark` - 添加文本/图片水印
- `add-stamp` - 添加印章
- `redact` - 删除敏感内容
- `sign` - 添加签名

### 安全性
- `add-password` - 为 PDF 文件设置密码保护
- `remove-password` - 移除 PDF 文件的密码
- `sanitize` - 删除元数据/脚本

## 直接使用 API

对于脚本未涵盖的操作，可以直接调用 API：

```bash
curl -X POST "$STIRLING_PDF_URL/api/v1/general/merge-pdfs" \
  -H "X-API-KEY: $STIRLING_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  -F "fileInput=@file1.pdf" \
  -F "fileInput=@file2.pdf" \
  -o merged.pdf
```

请访问 `<your-instance>/swagger-ui/index.html` 查看所有可用的 API 端点。

## 常见 API 端点

| 操作        | API 端点                |
|------------|----------------------|
| 合并        | `/api/v1/general/merge-pdfs`       |
| 分割        | `/api/v1/general/split-pages`       |
| 压缩        | `/api/v1/misc/compress-pdf`       |
| OCR         | `/api/v1/misc/ocr-pdf`        |
| PDF 转图片     | `/api/v1/convert/pdf/img`       |
| 图片转 PDF     | `/api/v1/convert/img/pdf`       |
| 添加水印      | `/api/v1/security/add-watermark`     |
| 设置密码      | `/api/v1/security/add-password`     |

## 注意事项

- 大多数 API 端点使用 POST 请求，并支持 `multipart/form-data` 格式的数据传输
- 文件输入参数通常为 `fileInput`
- 响应结果为处理后的 PDF 文件
- 请查阅 Swagger UI 以获取每个操作的具体参数要求