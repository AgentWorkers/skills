---
name: markdown-exporter
description: 这是一个Markdown导出工具，可以将Markdown格式的文本导出为DOCX、PPTX、XLSX、PDF、PNG、HTML、IPYNB、MD、CSV、JSON、JSONL、XML等多种格式的文件。同时，它还可以将Markdown中的代码块提取出来，并保存为Python、Bash、JavaScript等格式的文件。该工具也被称为“md_exporter”。
disable: false
metadata:
  openclaw:
    homepage: https://github.com/bowenliang123/md_exporter/
    emoji: 🖨
    requires:
      bins: [markdown-exporter]
    install:
      - kind: uv
        package: md-exporter
        bins: [markdown-exporter]
---

## ✨ 什么是 Markdown 导出器？

**Markdown 导出器**（Markdown Exporter）是一种代理技能（Agent Skill），它可以将您的 Markdown 文本转换为多种专业格式。无论您需要创建精美的报告、引人注目的演示文稿、结构化的电子表格还是代码文件，这款工具都能满足您的需求。

### 可用的工具及支持的格式

| 工具 | 输入（Markdown 文本或样式的文件路径） | 输出（导出文件的文件路径） |
|------|-------|--------|
| `md_to_docx` | 📝 Markdown 文本 | 📄 Word 文档 (.docx) |
| `md_to_html` | 📝 Markdown 文本 | 🌐 HTML 文件 (.html) |
| `md_to_html_text` | 📝 Markdown 文本 | 🌐 HTML 文本字符串 |
| `md_to_pdf` | 📝 Markdown 文本 | 📑 PDF 文件 (.pdf) |
| `md_to_png` | 📝 Markdown 文本 | 🖼️ PDF 页面的 PNG 图像 |
| `md_to_md` | 📝 Markdown 文本 | 📝 Markdown 文件 (.md) |
| `md_to_ipynb` | 📝 Markdown 文本 | 📓 Jupyter 笔记本 (.ipynb) |
| `md_to_pptx` | 📝 [Pandoc 样式的 Markdown 幻灯片](https://pandoc.org/MANUAL.html#slide-shows) | 🎯 PowerPoint (.pptx) |
| `md_to_xlsx` | 📋 [Markdown 表格](https://www.markdownguide.org/extended-syntax/#tables) | 📊 Excel 电子表格 (.xlsx) |
| `md_to_csv` | 📋 [Markdown 表格](https://www.markdownguide.org/extended-syntax/#tables) | 📋 CSV 文件 (.csv) |
| `md_to_json` | 📋 [Markdown 表格](https://www.markdownguide.org/extended-syntax/#tables) | 📦 JSON/JSONL 文件 (.json) |
| `md_to_xml` | 📋 [Markdown 表格](https://www.markdownguide.org/extended-syntax/#tables) | 🏷️ XML 文件 (.xml) |
| `md_to_latex` | 📋 [Markdown 表格](https://www.markdownguide.org/extended-syntax/#tables) | 📝 LaTeX 文件 (.tex) |
| `md_to_codeblock` | 💻 [Markdown 中的代码块](https://www.markdownguide.org/extended-syntax/#fenced-code-blocks) | 📁 按语言分类的代码文件 (.py, .js, .sh 等) |

## 先决条件

要使用 Markdown 导出器，请确保已安装以下软件：
- Python 3.11 或更高版本
- （可选）uv 包管理器

## 📦 使用方法

### 概述
Markdown 导出器现在作为一个 PyPI 包提供，通过命令行即可轻松使用其所有功能。

### 安装
您可以直接使用 pip 从 PyPI 安装该包：

```bash
pip install md-exporter
```

### 基本用法
安装完成后，您可以使用 `markdown-exporter` 命令来使用所有工具：

```bash
markdown-exporter <subcommand> <args> [options]
```

### 重要说明
- 所有命令仅支持文件路径作为输入参数
- 该包会自动处理所有依赖关系的管理
- 您可以在系统的任何位置运行命令，无需进入项目目录

## 🔧 脚本示例

### `md_to_csv` - 将 Markdown 表格转换为 CSV 格式

将 Markdown 表格转换为 CSV 格式。

**用法：**
```bash
markdown-exporter md_to_csv <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 CSV 文件路径

**选项：**
- `--strip-wrapper` - 如果存在代码块包装层，则将其删除

**示例：**
```bash
markdown-exporter md_to_csv /path/input.md /path/output.csv
```

### `md_to_pdf` - 将 Markdown 文本转换为 PDF 格式

将 Markdown 文本转换为 PDF 格式，支持中文、日文等多种语言。

**用法：**
```bash
markdown-exporter md_to_pdf <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 PDF 文件路径

**选项：**
- `--strip-wrapper` - 如果存在代码块包装层，则将其删除

**示例：**
```bash
markdown-exporter md_to_pdf /path/input.md /path/output.pdf
```

### `md_to_docx` - 将 Markdown 文本转换为 DOCX 格式

使用 pandoc 将 Markdown 文本转换为 DOCX 格式。

**用法：**
```bash
markdown-exporter md_to_docx <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 DOCX 文件路径

**选项：**
- `--template` - DOCX 模板文件的路径（可选）
- `--strip-wrapper` - 如果存在代码块包装层，则将其删除

**示例：**
```bash
markdown-exporter md_to_docx /path/input.md /path/output.docx
markdown-exporter md_to_docx /path/input.md /path/output.docx --template /path/template.docx
```

### `md_to_xlsx` - 将 Markdown 表格转换为 XLSX 格式

将 Markdown 表格转换为支持多个工作表的 XLSX 格式。

**用法：**
```bash
markdown-exporter md_to_xlsx <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 XLSX 文件路径

**选项：**
- `--force-text` - 将单元格值转换为文本类型（默认值：True）
- `--strip-wrapper` - 如果存在代码块包装层，则将其删除

**示例：**
```bash
markdown-exporter md_to_xlsx /path/input.md /path/output.xlsx
```

### `md_to_pptx` - 将 Markdown 文本转换为 PPTX 格式

使用 pandoc 将 Markdown 文本转换为 PPTX 格式。

**用法：**
```bash
markdown-exporter md_to_pptx <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 PPTX 文件路径

**选项：**
- `--template` - PPTX 模板文件的路径（可选）

**示例：**
```bash
markdown-exporter md_to_pptx /path/input.md /path/output.pptx
```

### `md_to_codeblock` - 从 Markdown 中提取代码块并保存为单独的文件

从 Markdown 中提取代码块，并将它们保存为单独的文件。

**用法：**
```bash
markdown-exporter md_to_codeblock <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出文件或目录路径

**选项：**
- `--compress` - 将所有代码块压缩到一个 ZIP 文件中

**示例：**
```bash
markdown-exporter md_to_codeblock /path/input.md /path/output_dir
markdown-exporter md_to_codeblock /path/input.md /path/output.zip --compress
```

### `md_to_json` - 将 Markdown 表格转换为 JSON 格式

将 Markdown 表格转换为 JSON 或 JSONL 格式。

**用法：**
```bash
markdown-exporter md_to_json <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 JSON 文件路径

**选项：**
- `--style` - JSON 输出格式：`jsonl`（默认）或 `json_array`
- `--strip-wrapper` - 如果存在代码块包装层，则将其删除

**示例：**
```bash
markdown-exporter md_to_json /path/input.md /path/output.json
markdown-exporter md_to_json /path/input.md /path/output.json --style json_array
```

### `md_to_xml` - 将 Markdown 文本转换为 XML 格式

将 Markdown 文本转换为 XML 格式。

**用法：**
```bash
markdown-exporter md_to_xml <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 XML 文件路径

**选项：**
- `--strip-wrapper` - 如果存在代码块包装层，则将其删除

**示例：**
```bash
markdown-exporter md_to_xml /path/input.md /path/output.xml
```

### `md_to_latex` - 将 Markdown 表格转换为 LaTeX 格式

将 Markdown 表格转换为 LaTeX 格式。

**用法：**
```bash
markdown-exporter md_to_latex <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 LaTeX 文件路径

**选项：**
- `--strip-wrapper` - 如果存在代码块包装层，则将其删除

**示例：**
```bash
markdown-exporter md_to_latex /path/input.md /path/output.tex
```

### `md_to_html` - 使用 pandoc 将 Markdown 文本转换为 HTML 格式**

将 Markdown 文本转换为 HTML 格式。

**用法：**
```bash
markdown-exporter md_to_html <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 HTML 文件路径

**选项：**
- `--strip-wrapper` - 如果存在代码块包装层，则将其删除

**示例：**
```bash
markdown-exporter md_to_html /path/input.md /path/output.html
```

### `md_to_html_text` - 将 Markdown 文本转换为 HTML 文本并输出到标准输出（stdout）

将 Markdown 文本转换为 HTML 文本，并输出到标准输出。

**用法：**
```bash
markdown-exporter md_to_html_text <input>
```

**参数：**
- `input` - 输入 Markdown 文件路径

**示例：**
```bash
markdown-exporter md_to_html_text /path/input.md
```

### `md_to_png` - 将 Markdown 文本转换为 PNG 图像**

将 Markdown 文本转换为 PNG 图像（每页一张图片）。

**用法：**
```bash
markdown-exporter md_to_png <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 PNG 文件路径或目录路径

**选项：**
- `--compress` - 将所有 PNG 图像压缩到一个 ZIP 文件中
- `--strip-wrapper` - 如果存在代码块包装层，则将其删除

**示例：**
```bash
markdown-exporter md_to_png /path/input.md /path/output.png
markdown-exporter md_to_png /path/input.md /path/output.png --compress
```

### `md_to_md` - 将 Markdown 文本保存为 .md 文件**

将 Markdown 文本保存为 .md 文件。

**用法：**
```bash
markdown-exporter md_to_md <input> <output>
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 MD 文件路径

**示例：**
```bash
markdown-exporter md_to_md /path/input.md /path/output.md
```

### `md_to_ipynb` - 将 Markdown 文本转换为 Jupyter 笔记本 (.ipynb) 格式**

将 Markdown 文本转换为 Jupyter 笔记本 (.ipynb) 格式。

**用法：**
```bash
markdown-exporter md_to_ipynb <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 IPYNB 文件路径

**选项：**
- `--strip-wrapper` - 如果存在代码块包装层，则将其删除

**示例：**
```bash
markdown-exporter md_to_ipynb /path/input.md /path/output.ipynb
```

## 📝 注意事项
- 所有脚本仅支持文件路径作为输入参数
- 对于生成多个文件的脚本（例如，包含多个表格或代码块的文档），输出文件的名称会自动编号
- 使用 `--strip-wrapper` 选项可以删除输入 Markdown 中的代码块包装层（````