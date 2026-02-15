---
name: Office to Markdown
description: 将 PDF、DOCX 和 PPTX 文件转换为 Markdown 格式。
---
# 将 Office 文档转换为 Markdown 的功能

该功能允许您将各种 Office 文档格式转换为 Markdown 格式。

## 支持的格式
- **PDF** (.pdf)：从 PDF 文件中提取文本。
- **Word** (.docx)：将 Word 文档转换为 Markdown，同时保留基本格式。
- **旧版 Word** (.doc)：从旧版 Word 文件（Office 97-2003）中提取文本。
- **PowerPoint** (.pptx)：从 PowerPoint 演示文稿中提取文本。

## 所需依赖库
- `pdf-parse`
- `mammoth`
- `turndown`
- `office-text-extractor`
- `word-extractor`

## 使用方法

要使用此功能，请运行 `convert.js` 脚本，并提供您希望转换的文件的路径。

```bash
node convert.js <path-to-file>
```

### 示例

```bash
node convert.js ./documents/report.pdf
```

脚本会在同一目录下生成一个新文件，文件名与源文件相同，但扩展名为 `.md`（例如：`./documents/report.md`）。

## 注意事项
- **PDF 转换**：仅提取原始文本，格式保留有限。
- **DOCX 转换**：首先使用 `mammoth` 将文件转换为 HTML，然后再使用 `turndown` 将 HTML 转换为 Markdown。对于简单的文档，布局通常能够得到较好的保留。
- **PPTX 转换**：目前仅提取文本内容，幻灯片的结构可能无法在 Markdown 输出中完全保留。