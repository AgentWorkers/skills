---
name: local-pandoc
description: 使用 pandoc 命令行工具将 Markdown 文件转换为 PDF 文件。当用户需要将 `.md` 或 Markdown 格式的文件转换为 `.pdf` 文件时，可以使用此方法。
---

# 本地 Pandoc 转换技巧

本技巧使用 `pandoc` 命令行工具在多种标记格式之间转换文档。

## 基本用法

`pandoc` 命令的基本结构如下：

```bash
pandoc [options] [input-file]…
```

### 简单转换

要将 Markdown 文件转换为 HTML 文件，可以使用以下命令：

```bash
pandoc -o output.html input.md
```

### 指定格式

虽然 `pandoc` 可以根据文件扩展名自动识别格式，但也可以通过 `-f`（源格式）和 `-t`（目标格式）选项明确指定转换格式：

```bash
# Convert HTML to Markdown
pandoc -f html -t markdown input.html
```

### 独立文档

要创建包含完整页眉和页脚的文档（例如，一个完整的 HTML 文件），可以使用 `-s` 或 `--standalone` 选项：

```bash
pandoc -s -o output.html input.md
```

## 高级示例

以下示例摘自 Pandoc 官方用户指南：

### PDF 输出

要生成 PDF 文件，`pandoc` 通常会使用 LaTeX 引擎。请确保已安装 LaTeX。

```bash
# Basic PDF creation
pandoc input.md -o output.pdf

# Control PDF engine and style via variables
pandoc input.md -o output.pdf --pdf-engine=xelatex -V geometry:margin=1in -V fontsize=12pt
```

### 文档结构与元数据

Pandoc 可以自动生成目录并使用文档元数据。

```bash
# Create a document with a Table of Contents (up to level 3 headings)
pandoc --toc --toc-depth=3 -o output.docx input.md

# Set metadata fields from the command line
pandoc -M title:"My Report" -M author:"Galactus" -o output.pdf input.md
```

### 模板与样式

您可以使用模板和其他选项来控制最终输出的结构和样式：

```bash
# Use a custom template for HTML output
pandoc -s --template=my-template.html -o output.html input.md

# For HTML output, link to a custom CSS file
pandoc -s --css=styles.css -o output.html input.md

# For DOCX output, use a reference document for styling
pandoc --reference-doc=reference.docx -o output.docx input.md
```

### 从网页读取内容

Pandoc 可以直接从 URL 获取内容并进行转换：

```bash
pandoc -f html -t markdown https://www.fsf.org
```

### 其他有用选项

```bash
# Preserve tabs instead of converting them to spaces
pandoc --preserve-tabs ...

# Control line wrapping in the output source code
pandoc --wrap=none ...

# Shift heading levels (e.g., make all H1s into H2s, H2s into H3s)
pandoc --shift-heading-level-by=1 ...
```

这份详细的文档为使用 `pandoc` 提供了更坚实的基础。