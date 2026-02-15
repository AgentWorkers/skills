---
name: paddleocr-doc-parsing
description: 使用 PaddleOCR 的 API 解析文档。支持对图片和 PDF 文件进行同步（sync）和异步（async）解析。
homepage: https://www.paddleocr.com
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "os": ["darwin", "linux"],
        "requires":
          {
            "bins": ["curl", "base64", "jq", "python3"],
            "env": ["PADDLEOCR_ACCESS_TOKEN", "PADDLEOCR_API_URL"],
          },
      },
  }
---

# PaddleOCR 文档解析

使用 PaddleOCR 的 API 解析图片和 PDF 文件。支持同步和异步解析模式，并提供结构化的输出结果。

## 资源链接

| 资源              | 链接                                                                           |
| --------------------- | ------------------------------------------------------------------------------ |
| **官方网站**  | [https://www.paddleocr.com](https://www.paddleocr.com)                                     |
| **API 文档** | [https://ai.baidu.com/ai-doc/AISTUDIO/Cmkz2m0ma](https://ai.baidu.com/ai-doc/AISTUDIO/Cmkz2m0ma)         |
| **GitHub**            | [https://github.com/PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) |

## 主要特性

- **多格式支持**：PDF 和图片文件（JPG、PNG、BMP、TIFF）
- **两种解析模式**：
  - **同步模式**：适用于小文件，响应速度快（超时时间 < 600 秒）
  - **异步模式**：适用于大文件，支持进度监控
- **布局分析**：自动检测文本块、表格和公式
- **多语言支持**：支持 110 多种语言
- **结构化输出**：以 Markdown 格式输出，保留文档结构

## 设置

1. 访问 [PaddleOCR](https://www.paddleocr.com) 获取 API 凭据
2. 设置环境变量：

```bash
export PADDLEOCR_ACCESS_TOKEN="your_token_here"
export PADDLEOCR_API_URL="https://your-endpoint.aistudio-app.com/layout-parsing"

# Optional: For async mode
export PADDLEOCR_JOB_URL="https://your-job-endpoint.aistudio-app.com/api/v2/ocr/jobs"
export PADDLEOCR_MODEL="PaddleOCR-VL-1.5"
```

## 使用示例

### 同步模式（默认）

适用于小文件和快速处理：

```bash
# Parse local image
{baseDir}/paddleocr_parse.sh document.jpg

# Parse PDF
{baseDir}/paddleocr_parse.sh -t pdf document.pdf

# Parse from URL
{baseDir}/paddleocr_parse.sh https://example.com/document.jpg

# Save output to file
{baseDir}/paddleocr_parse.sh -o result.json document.jpg

# Verbose output
{baseDir}/paddleocr_parse.sh -v document.jpg
```

### 异步模式

适用于大文件，并支持进度跟踪：

```bash
# Parse large PDF with async mode
{baseDir}/paddleocr_parse.sh --async large-document.pdf

# Parse from URL with async mode
{baseDir}/paddleocr_parse.sh --async -t pdf https://example.com/doc.pdf

# Save async result to file
{baseDir}/paddleocr_parse.sh --async -o result.json document.pdf
```

### 直接使用 Python 脚本

```bash
# Sync mode
python3 {baseDir}/paddleocr_parse.py document.jpg

# Async mode
python3 {baseDir}/paddleocr_parse.py --async-mode document.pdf

# With output file
python3 {baseDir}/paddleocr_parse.py -o result.json --async-mode document.pdf
```

## 响应结构

```json
{
  "logId": "unique_request_id",
  "errorCode": 0,
  "errorMsg": "Success",
  "result": {
    "layoutParsingResults": [
      {
        "prunedResult": [...],
        "markdown": {
          "text": "# Document Title\n\nParagraph content...",
          "images": {}
        },
        "outputImages": [...],
        "inputImage": "http://input-image"
      }
    ],
    "dataInfo": {...}
  }
}
```

**重要字段**：

- **`prunedResult`**：包含详细的布局元素信息（位置、类别等）
- **`markdown`**：以 Markdown 格式存储文档内容，保留结构和格式

## 模式选择指南

| 使用场景 | 推荐模式 |
|----------|-----------------|
| 小图片（< 10MB） | 同步 |
| 单页 PDF | 同步 |
| 大文件（> 10MB） | 异步 |
| 多页文档 | 异步 |
| 批量处理 | 异步 |
| 快速提取文本 | 同步 |

## 错误处理

在以下情况下，脚本将退出并显示错误信息：
- 缺少必要的环境变量
- 文件未找到
- API 认证失败
- JSON 响应无效
- API 错误代码（非零）

## 配额信息

请参阅官方文档：https://ai.baidu.com/ai-doc/AISTUDIO/Xmjclapam