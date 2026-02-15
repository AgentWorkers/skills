---
name: markdown-converter
description: 使用 markitdown 将文档和文件转换为 Markdown 格式。适用于将 PDF、Word（.docx）、PowerPoint（.pptx）、Excel（.xlsx, .xls）、HTML、CSV、JSON、XML、带有 EXIF/OCR 标签的图片、带有文字转录的音频文件、ZIP 压缩包、YouTube 链接或 EPub 格式的文件转换为 Markdown 格式，以便用于大型语言模型（LLM）的处理或文本分析。
---

# Markdown 转换器

使用 `uvx markitdown` 将文件转换为 Markdown 格式——无需安装任何软件。

## 基本用法

```bash
# Convert to stdout
uvx markitdown input.pdf

# Save to file
uvx markitdown input.pdf -o output.md
uvx markitdown input.docx > output.md

# From stdin
cat input.pdf | uvx markitdown
```

## 支持的格式

- **文档**：PDF、Word (.docx)、PowerPoint (.pptx)、Excel (.xlsx, .xls)
- **网页/数据**：HTML、CSV、JSON、XML
- **媒体**：图片（包含 EXIF 信息及 OCR 解析）、音频（包含 EXIF 信息及文字转录）
- **其他**：ZIP 文件（可遍历文件内容）、YouTube 链接、EPub 格式

## 选项

```bash
-o OUTPUT      # Output file
-x EXTENSION   # Hint file extension (for stdin)
-m MIME_TYPE   # Hint MIME type
-c CHARSET     # Hint charset (e.g., UTF-8)
-d             # Use Azure Document Intelligence
-e ENDPOINT    # Document Intelligence endpoint
--use-plugins  # Enable 3rd-party plugins
--list-plugins # Show installed plugins
```

## 示例

```bash
# Convert Word document
uvx markitdown report.docx -o report.md

# Convert Excel spreadsheet
uvx markitdown data.xlsx > data.md

# Convert PowerPoint presentation
uvx markitdown slides.pptx -o slides.md

# Convert with file type hint (for stdin)
cat document | uvx markitdown -x .pdf > output.md

# Use Azure Document Intelligence for better PDF extraction
uvx markitdown scan.pdf -d -e "https://your-resource.cognitiveservices.azure.com/"
```

## 注意事项

- 转换后的输出会保留文档的结构：标题、表格、列表、链接等
- 首次运行时会缓存依赖项，后续运行速度会更快
- 对于结构复杂的 PDF 文件（提取效果不佳的情况），建议使用 `-d` 选项并结合 Azure Document Intelligence 工具进行转换