---
name: paddleocr-doc-parsing
description: 使用 PaddleOCR 的 API 解析文档。
homepage: https://www.paddleocr.com
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "os": ["darwin", "linux"],
        "requires":
          {
            "bins": ["curl", "base64", "jq"],
            "env": ["PADDLEOCR_API_URL", "PADDLEOCR_ACCESS_TOKEN"],
          },
      },
  }
---

# PaddleOCR 文档解析

使用 PaddleOCR 的 API 解析图像和 PDF 文件。支持多种文档解析算法，并提供结构化的输出结果。

## 资源链接

| 资源              | 链接                                                                           |
| --------------------- | ------------------------------------------------------------------------------ |
| **官方网站**  | [https://www.paddleocr.com](https://www.paddleocr.com)                                     |
| **API 文档** | [https://ai.baidu.com/ai-doc/AISTUDIO/Cmkz2m0ma](https://ai.baidu.com/ai-doc/AISTUDIO/Cmkz2m0ma)         |
| **GitHub**            | [https://github.com/PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) |

## 主要特性

- **多格式支持**：支持 PDF 和图像文件（JPG、PNG、BMP、TIFF）
- **布局分析**：自动检测文本块、表格和公式
- **多语言支持**：支持 110 多种语言
- **结构化输出**：以 Markdown 格式输出文档内容，同时保留文档的结构和格式

## 设置

1. 从 [PaddleOCR 官网](https://www.paddleocr.com) 获取凭据。点击“API”按钮，选择所需的算法（例如 PP-StructureV3、PaddleOCR-VL-1.5），然后复制 API URL 和访问令牌。
2. 设置环境变量：

```bash
export PADDLEOCR_API_URL="https://your-endpoint-here"
export PADDLEOCR_ACCESS_TOKEN="your_access_token"
```

## 使用示例

### 运行脚本

```bash
# Parse local image
{baseDir}/paddleocr_parse.sh document.jpg

# Parse local PDF file
{baseDir}/paddleocr_parse.sh -t pdf document.pdf

# Parse document from URL
{baseDir}/paddleocr_parse.sh -t pdf https://example.com/document.pdf

# Output to stdout (default)
{baseDir}/paddleocr_parse.sh document.jpg

# Save output to file
{baseDir}/paddleocr_parse.sh -o result.json document.jpg
```

### 响应结构

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

**重要字段：**

- **`prunedResult`**：包含详细的布局元素信息，如位置、类别等。
- **`markdown`**：以 Markdown 格式存储文档内容，同时保留结构和格式。

## 配额信息

请参阅官方文档：https://ai.baidu.com/ai-doc/AISTUDIO/Xmjclapam