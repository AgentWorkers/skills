---
name: document-handler
description: Read, extract, and convert document files (PDF, DOCX, XLSX, PPTX, EPUB, RTF, ODT, ODS, ODP). Use when working with any document format: extracting text, metadata, converting formats, or processing content. Triggers on mentions of document files, file paths with document extensions, or requests to read/convert documents.
---

# 文档处理工具

能够从任何格式的文档中提取文本、元数据和内容。

## 支持的格式

| 格式 | 扩展名 | 文本提取 | 元数据 | 转换方式 |
|--------|------------|--------------|----------|---------|
| PDF | .pdf | ✅ pdftotext | ✅ pdfinfo | ✅ pdftoppm |
| Word | .docx | ✅ unzip + xml | ✅ | ✅ |
| Excel | .xlsx | ✅ unzip + xml | ✅ | ✅ |
| PowerPoint | .pptx | ✅ unzip + xml | ✅ | ✅ |
| EPUB | .epub | ✅ unzip + html | ✅ | ✅ |
| RTF | .rtf | ✅ textutil | ✅ | ✅ |
| OpenDocument | .odt, .ods, .odp | ✅ unzip + xml | ✅ | ✅ |

## 快速命令

### PDF

```bash
# Extract text
pdftotext -layout input.pdf output.txt

# Get metadata
pdfinfo input.pdf

# Convert to images (for OCR or viewing)
pdftoppm -png input.pdf output_prefix

# Extract specific pages
pdftotext -f 5 -l 10 -layout input.pdf output.txt
```

### DOCX/XLSX/PPTX (Office Open XML)

```bash
# Extract text from DOCX
unzip -p input.docx word/document.xml | sed 's/<[^>]*>//g' | tr -s ' \n'

# Extract text from XLSX (all sheets)
unzip -p input.xlsx xl/sharedStrings.xml | sed 's/<[^>]*>//g' | tr -s '\n'

# Extract text from PPTX
unzip -p input.pptx ppt/slides/*.xml | sed 's/<[^>]*>//g' | tr -s ' \n'

# Get metadata
unzip -p input.docx docProps/core.xml
```

### RTF (macOS)

```bash
# Convert RTF to plain text
textutil -convert txt input.rtf -output output.txt

# Convert RTF to HTML
textutil -convert html input.rtf -output output.html
```

### EPUB

```bash
# Extract and read EPUB content
unzip -l input.epub                    # List contents
unzip -p input.epub "*.html" | lynx -stdin -dump  # Text via lynx
unzip -p input.epub "*.xhtml" | sed 's/<[^>]*>//g'  # Raw text
```

### OpenDocument (ODT/ODS/ODP)

```bash
# Extract text from ODT
unzip -p input.odt content.xml | sed 's/<[^>]*>//g' | tr -s ' \n'

# Extract from ODS
unzip -p input.ods content.xml | sed 's/<[^>]*>//g'

# Get metadata
unzip -p input.odt meta.xml
```

## 脚本

### extract_document.sh

从任何支持的文档格式中提取文本和元数据。

```bash
~/Dropbox/jarvis/skills/document-handler/scripts/extract_document.sh <file>
```

**输出结果：**
- 文本内容输出到标准输出（stdout）
- 元数据以 JSON 格式输出（作为注释）

### pdf_to_images.sh

将 PDF 页面转换为图像，以便进行 OCR 或视觉处理。

```bash
~/Dropbox/jarvis/skills/document-handler/scripts/pdf_to_images.sh <pdf> <output_dir> [dpi]
```

## 工作流程

1. **识别文档格式** — 检查文件扩展名
2. **提取文本** — 使用相应的工具
3. **获取元数据** — 作者、日期、页数等
4. **处理文档内容** — 摘要、搜索、转换等

## 注意事项：

- 包含扫描图片的 PDF 文件需要使用 OCR 工具（如 pdftoppm 和 tesseract）
- 加密过的 PDF 文件需要输入密码才能提取内容
- 复杂的文档格式可能会导致文本提取不完整
- 对于 PDF 中的表格，可以考虑使用 tabula 或 camelot 等工具进行处理