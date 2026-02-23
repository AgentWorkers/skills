---
name: markdown-exporter
description: 将 Markdown 文本转换为 DOCX、PPTX、XLSX、PDF、PNG、HTML、IPYNB、MD、CSV、JSON、JSONL、XML 文件，并将 Markdown 中的代码块提取到 Python、Bash、JavaScript 等文件中。
license: Apache-2.0
metadata:
   author: bowenliang123
   openclaw:
      homepage: https://github.com/bowenliang123/markdown-exporter
      emoji: 🖨
      requires:
         bins: [ markdown-exporter ]
      install:
         - kind: uv
           package: md-exporter
           bins: [ markdown-exporter ]
---

# Markdown 导出工具

Markdown 导出工具（Markdown Exporter）是一种代理技能（Agent Skill），它可以将 Markdown 文本转换为多种专业格式的文件。

这个用于代理技能的 [SKILL.md](https://github.com/bowenliang123/markdown-exporter/blob/main/SKILL.md) 文件、命令行工具以及 [Python 包 `markdown-exporter`](https://pypi.org/project/md-exporter/) 都由 [bowenliang123](https://github.com/bowenliang123) 在 GitHub 仓库 [bowenliang123/markdown-exporter](https://github.com/bowenliang123) 中维护。

### 工具及支持的格式

| 工具          | 输入（Markdown 文本或样式的文件路径） | 输出（导出文件的文件路径） |
|------------------|------------------|----------------------|
| `md_to_docx`     | 📝 Markdown 文本        | 📄 Word 文档 (.docx)         |
| `md_to_html`     | 📝 Markdown 文本        | 🌐 HTML 文件 (.html)         |
| `md_to_html_text`    | 📝 Markdown 文本        | 🌐 HTML 文本字符串         |
| `md_to_pdf`     | 📝 Markdown 文本        | 📑 PDF 文件 (.pdf)          |
| `md_to_png`     | 📝 Markdown 文本        | 🖼️ PDF 页面的 PNG 图像        |
| `md_to_md`     | 📝 Markdown 文本        | 📝 Markdown 文件 (.md)         |
| `md_to_ipynb`     | 📝 Markdown 文本        | 📓 Jupyter 笔记本 (.ipynb)       |
| `md_to_pptx`     | 📝 Markdown 幻灯片（[Pandoc 格式](https://pandoc.org/MANUAL.html#slide-shows) | 🎯 PowerPoint (.pptx)        |
| `md_to_xlsx`     | 📋 Markdown 表格        | 📊 Excel 电子表格 (.xlsx)       |
| `md_to_csv`     | 📋 Markdown 表格        | 📋 CSV 文件 (.csv)          |
| `md_to_json`     | 📋 Markdown 表格        | 📦 JSON/JSONL 文件 (.json)        |
| `md_to_xml`     | 📋 Markdown 表格        | 🏷️ XML 文件 (.xml)          |
| `md_to_latex`     | 📋 Markdown 表格        | 📝 LaTeX 文件 (.tex)         |
| `md_to_codeblock`    | 💻 Markdown 中的代码块       | 📁 按语言分隔的代码文件 (.py, .js, .sh 等) |

## 📦 使用方法

### 概述
Markdown 导出工具作为一个 PyPI 包提供，通过命令行界面可以方便地使用其所有功能。

### 安装
```bash
# with pip
pip install md-exporter

# with uv 
uv tool install md-exporter

# on OpenClaw
npx clawhub install markdown-exporter
```

查看 `markdown-exporter` 的命令及用法：
```
markdown-exporter -h

markdown-exporter <subcommand> -h
```

### 基本用法
使用 `markdown-exporter` 命令来使用所有工具：
```bash
markdown-exporter <subcommand> <args> [options]
```

### 重要说明
- 所有命令仅支持文件路径作为输入
- 该包会自动处理所有依赖关系的管理
- 你可以在系统的任何位置运行命令，无需导航到项目目录

## 🔧 脚本

### `md_to_csv` - 将 Markdown 表格转换为 CSV
将 Markdown 表格转换为 CSV 格式的文件。

**用法：**
```bash
markdown-exporter md_to_csv <input> <output> [options]
```

**参数：**
- `input` - 包含表格的输入 Markdown 文件路径
- `output` - 输出 CSV 文件路径

**选项：**
- `--strip-wrapper` - 如果存在，移除代码块的包装层

**示例：**
1. **基本转换**：
   ```bash
   markdown-exporter md_to_csv /path/input.md /path/output.csv
   ```
   这会将输入 Markdown 文件中的所有表格转换为 CSV 格式。

2. **移除代码块包装层**：
   ```bash
   markdown-exporter md_to_csv /path/input.md /path/output.csv --strip-wrapper
   ```
   在处理 Markdown 之前，会移除所有的代码块包装层（```）。

**示例 Markdown 输入：**
使用下面的 [Sample Markdown Inputs - Basic Text and Tables](#basic-text-and-tables) 部分中的“Basic Text and Tables”示例。

---

### `md_to_pdf` - 将 Markdown 转换为 PDF
将 Markdown 文本转换为 PDF 格式，支持中文、日文等多种语言。

**用法：**
```bash
markdown-exporter md_to_pdf <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 PDF 文件路径

**选项：**
- `--strip-wrapper` - 如果存在，移除代码块的包装层

**示例：**
1. **基本转换**：
   ```bash
   markdown-exporter md_to_pdf /path/input.md /path/output.pdf
   ```
   这会将整个 Markdown 文件转换为 PDF 文档。

2. **移除代码块包装层**：
   ```bash
   markdown-exporter md_to_pdf /path/input.md /path/output.pdf --strip-wrapper
   ```
   在处理 Markdown 之前，会移除所有的代码块包装层（```）。

**示例 Markdown 输入：**
使用下面的 [Sample Markdown Inputs - Basic Text and Tables](#basic-text-and-tables) 部分中的“Basic Text and Tables”示例。

---

### `md_to_docx` - 将 Markdown 转换为 DOCX
将 Markdown 文本转换为 DOCX 格式的文件。

**用法：**
```bash
markdown-exporter md_to_docx <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 DOCX 文件路径

**选项：**
- `--template` - DOCX 模板文件的路径（可选）
- `--strip-wrapper` - 如果存在，移除代码块的包装层

**示例：**
1. **基本转换**：
   ```bash
   markdown-exporter md_to_docx /path/input.md /path/output.docx
   ```
   这会将整个 Markdown 文件转换为 DOCX 文档。

2. **使用自定义模板**：
   ```bash
   markdown-exporter md_to_docx /path/input.md /path/output.docx --template /path/template.docx
   ```
   使用自定义的 DOCX 模板进行样式设置。

3. **移除代码块包装层**：
   ```bash
   markdown-exporter md_to_docx /path/input.md /path/output.docx --strip-wrapper
   ```
   在处理 Markdown 之前，会移除所有的代码块包装层（```）。

**示例 Markdown 输入：**
使用下面的 [Sample Markdown Inputs - Basic Text and Tables](#basic-text-and-tables) 部分中的“Basic Text and Tables”示例。

---

### `md_to_xlsx` - 将 Markdown 表格转换为 XLSX
将 Markdown 表格转换为支持多个工作表的 XLSX 格式。

**用法：**
```bash
markdown-exporter md_to_xlsx <input> <output> [options]
```

**参数：**
- `input` - 包含表格的输入 Markdown 文件路径
- `output` - 输出 XLSX 文件路径

**选项：**
- `--force-text` - 将单元格值转换为文本类型（默认：True）
- `--strip-wrapper` - 如果存在，移除代码块的包装层

**示例：**
1. **基本转换**：
   ```bash
   markdown-exporter md_to_xlsx /path/input.md /path/output.xlsx
   ```
   这会将输入 Markdown 文件中的所有表格转换为 XLSX 工作簿，每个表格都在单独的工作表中。

2. **移除代码块包装层**：
   ```bash
   markdown-exporter md_to_xlsx /path/input.md /path/output.xlsx --strip-wrapper
   ```
   在处理 Markdown 之前，会移除所有的代码块包装层（```）。

3. **禁用 force-text**：
   ```bash
   markdown-exporter md_to_xlsx /path/input.md /path/output.xlsx --force-text False
   ```
   这允许 Excel 自动确定单元格类型。

**示例 Markdown 输入：**
使用下面的 [Sample Markdown Inputs - Basic Text and Tables](#basic-text-and-tables) 部分中的“Basic Text and Tables”示例。

---

### `md_to_pptx` - 将 Markdown 转换为 PPTX
将 Markdown 文本转换为 PPTX 格式的文件。

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
   这会将 Markdown 文件转换为 PowerPoint 演示文稿。

2. **使用自定义模板**：
   ```bash
   markdown-exporter md_to_pptx /path/input.md /path/output.pptx --template /path/template.pptx
   ```
   使用自定义的 PowerPoint 模板进行样式设置。

**示例 Markdown 输入：**
使用下面的 [Sample Markdown Inputs - Slides (for PPTX)](#slides-for-pptx) 部分中的“Slides (for PPTX)”示例。

---

### `md_to_codeblock` - 从 Markdown 中提取代码块并保存为单独的文件
从 Markdown 中提取代码块，并将它们保存为单独的文件。

**用法：**
```bash
markdown-exporter md_to_codeblock <input> <output> [options]
```

**参数：**
- `input` - 包含代码块的输入 Markdown 文件路径
- `output` - 输出目录路径或 ZIP 文件路径

**选项：**
- `--compress` - 将所有代码块压缩到一个 ZIP 文件中

**示例：**
1. **提取到目录**：
   ```bash
   markdown-exporter md_to_codeblock /path/input.md /path/output_dir
   ```
   这会将所有代码块提取到指定的目录中。

2. **提取到 ZIP 文件**：
   ```bash
   markdown-exporter md_to_codeblock /path/input.md /path/output.zip --compress
   ```
   这会将所有代码块提取并压缩到一个 ZIP 文件中。

**示例 Markdown 输入：**
使用下面的 [Sample Markdown Inputs - Code Blocks](#code-blocks) 部分中的“Code Blocks”示例。

---

### `md_to_json` - 将 Markdown 表格转换为 JSON
将 Markdown 表格转换为 JSON 或 JSONL 格式的文件。

**用法：**
```bash
markdown-exporter md_to_json <input> <output> [options]
```

**参数：**
- `input` - 包含表格的输入 Markdown 文件路径
- `output` - 输出 JSON 文件路径

**选项：**
- `--style` - JSON 输出格式：`jsonl`（默认）或 `json_array`
- `--strip-wrapper` - 如果存在，移除代码块的包装层

**示例：**
1. **基本转换（JSONL 格式）**：
   ```bash
   markdown-exporter md_to_json /path/input.md /path/output.json
   ```
   这会将表格转换为 JSON 行格式（每行一个 JSON 对象）。

2. **转换为 JSON 数组**：
   ```bash
   markdown-exporter md_to_json /path/input.md /path/output.json --style json_array
   ```
   这会将表格转换为单个 JSON 数组。

3. **移除代码块包装层**：
   ```bash
   markdown-exporter md_to_json /path/input.md /path/output.json --strip-wrapper
   ```
   在处理 Markdown 之前，会移除所有的代码块包装层（```）。

**示例 Markdown 输入：**
使用下面的 [Sample Markdown Inputs - Basic Text and Tables](#basic-text-and-tables) 部分中的“Basic Text and Tables”示例。

---

### `md_to_xml` - 将 Markdown 转换为 XML
将 Markdown 文本转换为 XML 格式的文件。

**用法：**
```bash
markdown-exporter md_to_xml <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 XML 文件路径

**选项：**
- `--strip-wrapper` - 如果存在，移除代码块的包装层

**示例：**
1. **基本转换**：
   ```bash
   markdown-exporter md_to_xml /path/input.md /path/output.xml
   ```
   这会将整个 Markdown 文件转换为 XML 文档。

2. **移除代码块包装层**：
   ```bash
   markdown-exporter md_to_xml /path/input.md /path/output.xml --strip-wrapper
   ```
   在处理 Markdown 之前，会移除所有的代码块包装层（```）。

**示例 Markdown 输入：**
使用下面的 [Sample Markdown Inputs - Basic Text and Tables](#basic-text-and-tables) 部分中的“Basic Text and Tables”示例。

---

### `md_to_latex` - 将 Markdown 表格转换为 LaTeX 格式
将 Markdown 表格转换为 LaTeX 格式的文件。

**用法：**
```bash
markdown-exporter md_to_latex <input> <output> [options]
```

**参数：**
- `input` - 包含表格的输入 Markdown 文件路径
- `output` - 输出 LaTeX 文件路径

**选项：**
- `--strip-wrapper` - 如果存在，移除代码块的包装层

**示例：**
1. **基本转换**：
   ```bash
   markdown-exporter md_to_latex /path/input.md /path/output.tex
   ```
   这会将输入 Markdown 文件中的所有表格转换为 LaTeX 格式。

2. **移除代码块包装层**：
   ```bash
   markdown-exporter md_to_latex /path/input.md /path/output.tex --strip-wrapper
   ```
   在处理 Markdown 之前，会移除所有的代码块包装层（```）。

**示例 Markdown 输入：**
使用下面的 [Sample Markdown Inputs - Basic Text and Tables](#basic-text-and-tables) 部分中的“Basic Text and Tables”示例。

---

### `md_to_html` - 将 Markdown 转换为 HTML
将 Markdown 文本转换为 HTML 格式的文件。

**用法：**
```bash
markdown-exporter md_to_html <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 HTML 文件路径

**选项：**
- `--strip-wrapper` - 如果存在，移除代码块的包装层

**示例：**
1. **基本转换**：
   ```bash
   markdown-exporter md_to_html /path/input.md /path/output.html
   ```
   这会将整个 Markdown 文件转换为 HTML 文档。

2. **移除代码块包装层**：
   ```bash
   markdown-exporter md_to_html /path/input.md /path/output.html --strip-wrapper
   ```
   在处理 Markdown 之前，会移除所有的代码块包装层（```）。

**示例 Markdown 输入：**
使用下面的 [Sample Markdown Inputs - Basic Text and Tables](#basic-text-and-tables) 部分中的“Basic Text and Tables”示例。

---

### `md_to_html_text` - 将 Markdown 文本转换为 HTML 并输出到 stdout
将 Markdown 文本转换为 HTML 并输出到 stdout。

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

**示例 Markdown 输入：**
使用下面的 [Sample Markdown Inputs - Basic Text and Tables](#basic-text-and-tables) 部分中的“Basic Text and Tables”示例。

---

### `md_to_png` - 将 Markdown 转换为 PNG 图像
将 Markdown 文本转换为 PNG 图像（每页一张）。

**用法：**
```bash
markdown-exporter md_to_png <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 PNG 文件路径或目录路径

**选项：**
- `--compress` - 将所有 PNG 图像压缩到一个 ZIP 文件中
- `--strip-wrapper` - 如果存在，移除代码块的包装层

**示例：**
1. **基本转换**：
   ```bash
   markdown-exporter md_to_png /path/input.md /path/output.png
   ```
   这会将 Markdown 文件转换为 PNG 图像（每页一张）。

2. **压缩**：
   ```bash
   markdown-exporter md_to_png /path/input.md /path/output.png --compress
   ```
   这会将 Markdown 文件转换为 PNG 图像，并将它们压缩到一个 ZIP 文件中。

3. **移除代码块包装层**：
   ```bash
   markdown-exporter md_to_png /path/input.md /path/output.png --strip-wrapper
   ```
   在处理 Markdown 之前，会移除所有的代码块包装层（```）。

**示例 Markdown 输入：**
使用下面的 [Sample Markdown Inputs - Basic Text and Tables](#basic-text-and-tables) 部分中的“Basic Text and Tables”示例。

---

### `md_to_md` - 将 Markdown 转换为 MD 文件
将 Markdown 文本保存为 `.md` 文件。

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

**示例 Markdown 输入：**
使用下面的 [Sample Markdown Inputs - Basic Text and Tables](#basic-text-and-tables) 部分中的“Basic Text and Tables”示例。

---

### `md_to_ipynb` - 将 Markdown 转换为 Jupyter 笔记本 (.ipynb) 格式的文件

**用法：**
```bash
markdown-exporter md_to_ipynb <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 IPYNB 文件路径

**选项：**
- `--strip-wrapper` - 如果存在，移除代码块的包装层

**示例：**
1. **基本转换**：
   ```bash
   markdown-exporter md_to_ipynb /path/input.md /path/output.ipynb
   ```
   这会将 Markdown 文件转换为 Jupyter 笔记本格式。

2. **移除代码块包装层**：
   ```bash
   markdown-exporter md_to_ipynb /path/input.md /path/output.ipynb --strip-wrapper
   ```
   在处理 Markdown 之前，会移除所有的代码块包装层（```）。

**示例 Markdown 输入：**
使用下面的 [Sample Markdown Inputs - Code Blocks](#code-blocks) 部分中的“Code Blocks”示例。

### 示例 Markdown 输入
为了帮助你测试各种工具，下面是一些常见的 Markdown 输入示例，这些示例代表了输入文件的内容：

#### 基本文本和表格
```markdown
# Test Markdown File

This is a test markdown file for testing various export tools.

## Table Test

| Name | Description | Price |
|------|-------------|-------|
| Item 1 | First item | $10 |
| Item 2 | Second item | $20 |
| Item 3 | Third item | $30 |

## Text Test

This is a paragraph with **bold** and *italic* text.

- List item 1
- List item 2
- List item 3

> This is a blockquote.
```

#### 代码块
````markdown
# Test Markdown File

## Code Block Test

```python
print("Hello, World!")
def add(a, b):
    return a + b

# 测试函数
result = add(5, 3)
print(f"Result: {result}")
```

```bash
# Bash 脚本示例
echo "Hello from Bash"
ls -la
```

```javascript
// JavaScript 示例
console.log("Hello from JavaScript");
function multiply(a, b) {
    return a * b;
}
```
```

#### PPTX 幻灯片
````markdown
---
title: Markdown Exporter
author: Bowen Liang
---

# Introduction

## Welcome Slide

Welcome to our Markdown Exporter!

::: notes
Remember to greet the audience warmly.
:::

---

# Section 1: Basic Layouts

## Title and Content

- This is a basic slide with bullet points
- It uses the "Title and Content" layout
- Perfect for simple content presentation

## Two Column Layout

::::: columns
::: column
Left column content:
- Point 1
- Point 2
:::
::: column
Right column content:
- Point A
- Point B
:::
:::::

## Comparison Layout

::::: columns
::: column
Text followed by an image:

![Test Image](https://example.com/image.jpg)
:::
::: column
- This triggers the "Comparison" layout
- Useful for side-by-side comparisons
:::
:::::

## Content with Caption

Here's some explanatory text about the image below.

![Test Image](https://example.com/image.jpg "fig:Test Image")

---

# Section 2: Advanced Features

## Code Block

Here's a Python code block:

```python
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))
```

## Table Example

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Row 1    | Data     | More     |
| Row 2    | Info     | Stuff    |

## Incremental List

::: incremental
- This point appears first
- Then this one
- And finally this one
:::

## {background-image="https://example.com/image.jpg"}

::: notes
This is a slide with a background image and speaker notes only.
The "Blank" layout will be used.
:::

# Conclusion

## Thank You

Thank you for viewing this kitchen sink presentation!

::: notes
Remember to thank the audience and invite questions.
:::
````

## 📝 注意事项
- 所有脚本仅支持文件路径作为输入
- 对于生成多个文件的脚本（例如，多个表格、多个代码块），输出文件名会自动编号
- 使用 `--strip-wrapper` 选项可以从输入 Markdown 中移除代码块的包装层（```）