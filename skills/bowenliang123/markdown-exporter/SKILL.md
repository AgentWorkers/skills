---
name: markdown-exporter
description: 这是一个Markdown导出工具，可以将Markdown文本导出为DOCX、PPTX、XLSX、PDF、PNG、HTML、MD、CSV、JSON、JSONL、XML等多种格式的文件，并能够将Markdown中的代码块提取出来，分别保存为Python、Bash、JavaScript等格式的文件。该工具也被称为“md_exporter”。
allowed-tools: 
disable: false
---

## ✨ 什么是 Markdown 导出器？

**Markdown 导出器** 是一种代理技能（Agent Skill），它可以将您的 Markdown 文本转换为多种专业格式。无论您需要创建精美的报告、引人注目的演示文稿、结构化的电子表格还是代码文件，这款工具都能满足您的需求。

### 工具及支持的格式

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
| `md_to_codeblock` | 💻 [Markdown 中的代码块](https://www.markdownguide.org/extended-syntax/#fenced-code-blocks) | 📁 按语言分组的代码文件 (.py, .js, .sh 等) |

## 先决条件

要使用 Markdown 导出器技能，请确保已安装以下先决条件：
- Python 3.11 或更高版本
- （可选）uv 包管理器


## 📦 使用方法

### 概述
该项目提供的所有脚本都是位于 `scripts/` 目录中的 Python 脚本。所有必需的 Python 依赖项都在项目的 [pyproject.toml](./pyproject.toml) 文件中声明。

### 推荐的执行方法 - 使用 Bash 脚本
我们强烈推荐使用位于 `scripts/` 目录中的 Bash 脚本。这些脚本通过自动处理依赖项管理和执行，提供了无缝的使用体验：

1. **自动依赖项管理**：当您从 `scripts/` 目录运行 Bash 脚本时，它会：
   - 首先检查是否安装了 `uv` 包管理器
   - 如果 `uv` 可用，它将使用 `uv run` 一次性自动安装依赖项并执行 Python 脚本
   - 如果 `uv` 不可用，它将转而使用 `pip` 从 `requirements.txt` 安装依赖项，然后再执行脚本
   - 在使用 `pip` 时，会检查是否已安装 Python 3.11 或更高版本

2. **使用 bash 执行脚本**：
   ```bash
   scripts/md-exporter <script_name> <args> [options]
   ```

### 替代执行方法 - 直接执行 Python 脚本
您也可以直接运行 Python 脚本，但需要自行管理依赖项：

1. **使用 uv**（如果直接运行推荐使用）：
   ```bash
   # Enter the directory of current skill
   cd $SKILL_HOME_MARKDOWN_EXPORTER
   # Install dependencies first
   uv sync
   # Then run the script
   uv run python scripts/parser/<script_name>.py <args> [options]
   ```

2. **使用 pip**：
   ```bash
   # Enter the directory of current skill
   cd $SKILL_HOME_MARKDOWN_EXPORTER
   # Install dependencies first
   pip install -r requirements.txt
   # Then run the script
   python scripts/parser/<script_name>.py <args> [options]
   ```

### 重要说明
- 在执行任何脚本之前，请始终导航到项目的根目录。
- `scripts/` 目录中的 Bash 脚本提供了最便捷的执行方式，因为它们会自动处理所有依赖项管理。
- 所有脚本仅支持文件路径作为输入


## 🔧 脚本

### md_to_csv - 将 Markdown 表格转换为 CSV

将 Markdown 表格转换为 CSV 格式。

**用法：**
```bash
scripts/md-exporter md_to_csv <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 CSV 文件路径

**选项：**
- `--strip-wrapper` - 如果存在代码块包装层，则将其删除

**示例：**
```bash
scripts/md-exporter md_to_csv /path/input.md /path/output.csv
```


### md_to_pdf - 将 Markdown 转换为 PDF

将 Markdown 文本转换为 PDF 格式，支持中文、日文等多种语言。

**用法：**
```bash
scripts/md-exporter md_to_pdf <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 PDF 文件路径

**选项：**
- `--strip-wrapper` - 如果存在代码块包装层，则将其删除

**示例：**
```bash
scripts/md-exporter md_to_pdf /path/input.md /path/output.pdf
```


### md_to_docx - 将 Markdown 转换为 DOCX

使用 pandoc 将 Markdown 文本转换为 DOCX 格式。

**用法：**
```bash
scripts/md-exporter md_to_docx <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 DOCX 文件路径

**选项：**
- `--template` - DOCX 模板文件的路径（可选）
- `--strip-wrapper` - 如果存在代码块包装层，则将其删除

**示例：**
```bash
scripts/md-exporter md_to_docx /path/input.md /path/output.docx
scripts/md-exporter md_to_docx /path/input.md /path/output.docx --template /path/template.docx
```


### md_to_xlsx - 将 Markdown 表格转换为 XLSX

将 Markdown 表格转换为支持多个工作表的 XLSX 格式。

**用法：**
```bash
scripts/md-exporter md_to_xlsx <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 XLSX 文件路径

**选项：**
- `--force-text` - 将单元格值转换为文本类型（默认：True）
- `--strip-wrapper` - 如果存在代码块包装层，则将其删除

**示例：**
```bash
scripts/md-exporter md_to_xlsx /path/input.md /path/output.xlsx
```


### md_to_pptx - 将 Markdown 转换为 PPTX

使用 pandoc 将 Markdown 文本转换为 PPTX 格式。

**用法：**
```bash
scripts/md-exporter md_to_pptx <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 PPTX 文件路径

**选项：**
- `--template` - PPTX 模板文件的路径（可选）

**示例：**
```bash
scripts/md-exporter md_to_pptx /path/input.md /path/output.pptx
```


### md_to_codeblock - 从 Markdown 中提取代码块并保存为单独的文件

从 Markdown 中提取代码块，并将它们保存为单独的文件。

**用法：**
```bash
scripts/md-exporter md_to_codeblock <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出文件或目录路径

**选项：**
- `--compress` - 将所有代码块压缩到一个 ZIP 文件中

**示例：**
```bash
scripts/md-exporter md_to_codeblock /path/input.md /path/output_dir
scripts/md-exporter md_to_codeblock /path/input.md /path/output.zip --compress
```


### md_to_json - 将 Markdown 表格转换为 JSON

将 Markdown 表格转换为 JSON 或 JSONL 格式。

**用法：**
```bash
scripts/md-exporter md_to_json <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 JSON 文件路径

**选项：**
- `--style` - JSON 输出格式：`jsonl`（默认）或 `json_array`
- `--strip-wrapper` - 如果存在代码块包装层，则将其删除

**示例：**
```bash
scripts/md-exporter md_to_json /path/input.md /path/output.json
scripts/md-exporter md_to_json /path/input.md /path/output.json --style json_array
```


### md_to_xml - 将 Markdown 转换为 XML

将 Markdown 文本转换为 XML 格式。

**用法：**
```bash
scripts/md-exporter md_to_xml <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 XML 文件路径

**选项：**
- `--strip-wrapper` - 如果存在代码块包装层，则将其删除

**示例：**
```bash
scripts/md-exporter md_to_xml /path/input.md /path/output.xml
```


### md_to_latex - 将 Markdown 表格转换为 LaTeX

将 Markdown 表格转换为 LaTeX 格式。

**用法：**
```bash
scripts/md-exporter md_to_latex <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 LaTeX 文件路径

**选项：**
- `--strip-wrapper` - 如果存在代码块包装层，则将其删除

**示例：**
```bash
scripts/md-exporter md_to_latex /path/input.md /path/output.tex
```


### md_to_html - 将 Markdown 转换为 HTML

使用 pandoc 将 Markdown 文本转换为 HTML 格式。

**用法：**
```bash
scripts/md-exporter md_to_html <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 HTML 文件路径

**选项：**
- `--strip-wrapper` - 如果存在代码块包装层，则将其删除

**示例：**
```bash
scripts/md-exporter md_to_html /path/input.md /path/output.html
```


### md_to_html_text - 将 Markdown 文本转换为 HTML 并输出到 stdout

将 Markdown 文本转换为 HTML 并输出到 stdout。

**用法：**
```bash
scripts/md-exporter md_to_html_text <input>
```

**参数：**
- `input` - 输入 Markdown 文件路径

**示例：**
```bash
scripts/md-exporter md_to_html_text /path/input.md
```


### md_to/png - 将 Markdown 转换为 PNG 图像

将 Markdown 文本转换为 PNG 图像（每页一张图片）。

**用法：**
```bash
scripts/md-exporter md_to_png <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 PNG 文件路径或目录路径

**选项：**
- `--compress` - 将所有 PNG 图像压缩到一个 ZIP 文件中
- `--strip-wrapper` - 如果存在代码块包装层，则将其删除

**示例：**
```bash
scripts/md-exporter md_to_png /path/input.md /path/output.png
scripts/md-exporter md_to_png /path/input.md /path/output.png --compress
```


### md_to_md - 将 Markdown 转换为 MD 文件

将 Markdown 文本保存为 .md 文件。

**用法：**
```bash
scripts/md-exporter md_to_md <input> <output>
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 MD 文件路径

**示例：**
```bash
scripts/md-exporter md_to_md /path/input.md /path/output.md
```


### md_to_ipynb - 将 Markdown 转换为 Jupyter 笔记本 (.ipynb) 格式

将 Markdown 文本转换为 Jupyter 笔记本 (.ipynb) 格式。

**用法：**
```bash
scripts/md-exporter md_to_ipynb <input> <output> [options]
```

**参数：**
- `input` - 输入 Markdown 文件路径
- `output` - 输出 IPYNB 文件路径

**选项：**
- `--strip-wrapper` - 如果存在代码块包装层，则将其删除

**示例：**
```bash
scripts/md-exporter md_to_ipynb /path/input.md /path/output.ipynb
```


## 📝 注意事项

- 所有脚本仅支持文件路径作为输入
- 对于生成多个文件的脚本（例如，多个表格、多个代码块），输出文件的名称将自动编号
- 使用 `--strip-wrapper` 选项可以删除输入 Markdown 中的代码块包装层（````