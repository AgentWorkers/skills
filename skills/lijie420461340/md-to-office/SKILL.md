---
name: md-to-office
description: 使用 Pandoc 将 Markdown 文档转换为 Word、PowerPoint 和 PDF 格式——Pandoc 是一款通用的文档转换工具。
author: claude-office-skills
version: "1.0"
tags: [markdown, conversion, pandoc, word, pdf, powerpoint]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: pandoc
  url: https://github.com/jgm/pandoc
  stars: 42k
---

# 将 Markdown 文本转换为 Office 文档的技巧

## 概述

本技巧利用 **Pandoc**（一款通用的文档转换工具）将 Markdown 格式的内容转换为各种 Office 格式（如 Word 文档、PowerPoint 演示文稿、PDF 等），同时保留原有的格式和结构。

## 使用方法

1. 提供 Markdown 内容或对应的 Markdown 文件。
2. 指定目标格式（如 docx、pptx、pdf 等）。
3. （可选）提供用于样式设计的参考模板。
4. 我会使用 Pandoc 并设置最佳参数来完成转换。

**示例指令：**
- “将这个 README.md 文件转换为专业的 Word 文档。”
- “将我的 Markdown 笔记转换成 PowerPoint 演示文稿。”
- “使用自定义样式从这个 Markdown 文件生成 PDF。”
- “根据公司模板从这个 Markdown 文件创建 Word 文档。”

## 相关知识

### Pandoc 基础知识
```bash
# Basic conversion
pandoc input.md -o output.docx
pandoc input.md -o output.pdf
pandoc input.md -o output.pptx

# With template
pandoc input.md --reference-doc=template.docx -o output.docx

# Multiple inputs
pandoc ch1.md ch2.md ch3.md -o book.docx
```

### 支持的转换格式

| 输入格式 | 输出格式 | 命令                |
|---------|------------|-------------------|
| Markdown | Word     | `pandoc in.md -o out.docx`     |
| Markdown | PDF       | `pandoc in.md -o out.pdf`     |
| Markdown | PowerPoint | `pandoc in.md -o out.pptx`     |
| Markdown | HTML      | `pandoc in.md -o out.html`     |
| Markdown | LaTeX     | `pandoc in.md -o out.tex`     |
| Markdown | EPUB       | `pandoc in.md -o out.epub`     |

### 将 Markdown 转换为 Word (.docx) 文档

#### 基本转换
```bash
pandoc document.md -o document.docx
```

#### 使用参考模板
```bash
# First create a template by converting sample
pandoc sample.md -o reference.docx

# Edit reference.docx styles in Word, then use it
pandoc input.md --reference-doc=reference.docx -o output.docx
```

#### 添加目录
```bash
pandoc document.md --toc --toc-depth=3 -o document.docx
```

#### 添加元数据
```bash
pandoc document.md \
  --metadata title="My Report" \
  --metadata author="John Doe" \
  --metadata date="2024-01-15" \
  -o document.docx
```

### 将 Markdown 转换为 PDF 文档

#### 使用 LaTeX （最高质量）
```bash
# Requires LaTeX installation
pandoc document.md -o document.pdf

# With custom settings
pandoc document.md \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize=12pt \
  -o document.pdf
```

#### 使用 wkhtmltopdf 工具
```bash
pandoc document.md \
  --pdf-engine=wkhtmltopdf \
  --css=style.css \
  -o document.pdf
```

#### PDF 转换选项
```bash
pandoc document.md \
  -V papersize:a4 \
  -V geometry:margin=2cm \
  -V fontfamily:libertinus \
  -V colorlinks:true \
  --toc \
  -o document.pdf
```

### 将 Markdown 转换为 PowerPoint (.pptx) 文档

#### 基本转换
```bash
pandoc slides.md -o presentation.pptx
```

#### 幻灯片的结构要求
```markdown
---
title: Presentation Title
author: Author Name
date: January 2024
---

# Section Header (creates section divider)

## Slide Title

- Bullet point 1
- Bullet point 2
  - Sub-bullet

## Another Slide

Content here

::: notes
Speaker notes go here (not visible in slides)
:::

## Slide with Image

![Description](image.png){width=80%}

## Two Column Slide

:::::::::::::: {.columns}
::: {.column width="50%"}
Left column content
:::

::: {.column width="50%"}
Right column content
:::
::::::::::::::
```

#### 使用模板
```bash
# Use corporate PowerPoint template
pandoc slides.md --reference-doc=template.pptx -o presentation.pptx
```

### 使用 YAML 作为文档元数据

在 Markdown 文件的开头添加元数据：
```yaml
---
title: "Document Title"
author: "Author Name"
date: "2024-01-15"
abstract: "Brief description"
toc: true
toc-depth: 2
numbersections: true
geometry: margin=1in
fontsize: 11pt
documentclass: report
---

# First Chapter
...
```

### Python 集成

```python
import subprocess
import os

def md_to_docx(input_path, output_path, template=None):
    """Convert Markdown to Word document."""
    cmd = ['pandoc', input_path, '-o', output_path]
    
    if template:
        cmd.extend(['--reference-doc', template])
    
    subprocess.run(cmd, check=True)
    return output_path

def md_to_pdf(input_path, output_path, **options):
    """Convert Markdown to PDF with options."""
    cmd = ['pandoc', input_path, '-o', output_path]
    
    if options.get('toc'):
        cmd.append('--toc')
    
    if options.get('margin'):
        cmd.extend(['-V', f"geometry:margin={options['margin']}"])
    
    subprocess.run(cmd, check=True)
    return output_path

def md_to_pptx(input_path, output_path, template=None):
    """Convert Markdown to PowerPoint."""
    cmd = ['pandoc', input_path, '-o', output_path]
    
    if template:
        cmd.extend(['--reference-doc', template])
    
    subprocess.run(cmd, check=True)
    return output_path
```

### pypandoc（Python 包）

```python
import pypandoc

# Simple conversion
output = pypandoc.convert_file('input.md', 'docx', outputfile='output.docx')

# With options
output = pypandoc.convert_file(
    'input.md', 
    'docx',
    outputfile='output.docx',
    extra_args=['--toc', '--reference-doc=template.docx']
)

# From string
md_content = "# Hello\n\nThis is markdown."
output = pypandoc.convert_text(md_content, 'docx', format='md', outputfile='output.docx')
```

## 最佳实践

1. **使用模板**：创建统一的模板以保持品牌一致性。
2. **规范标题结构**：使用一致的标题级别（## 用于幻灯片，# 用于章节）。
3. **逐步测试**：先转换较小的部分以验证格式是否正确。
4. **添加元数据**：使用 YAML 在文件开头指定文档属性。
5. **处理图片**：使用相对路径并指定图片尺寸。

## 常见用法

### 批量转换
```python
import subprocess
from pathlib import Path

def batch_convert(input_dir, output_format, output_dir=None):
    """Convert all markdown files in a directory."""
    input_path = Path(input_dir)
    output_path = Path(output_dir) if output_dir else input_path
    
    for md_file in input_path.glob('*.md'):
        output_file = output_path / md_file.with_suffix(f'.{output_format}').name
        subprocess.run([
            'pandoc', str(md_file), '-o', str(output_file)
        ], check=True)
        print(f"Converted: {md_file.name} -> {output_file.name}")

batch_convert('./docs', 'docx', './output')
```

### 报告生成
```python
def generate_report(title, sections, output_path, template=None):
    """Generate Word report from structured data."""
    
    # Build markdown
    md_content = f"""---
title: "{title}"
date: "{datetime.now().strftime('%B %d, %Y')}"
---

"""
    for section_title, content in sections.items():
        md_content += f"# {section_title}\n\n{content}\n\n"
    
    # Write temp file
    with open('temp_report.md', 'w') as f:
        f.write(md_content)
    
    # Convert
    cmd = ['pandoc', 'temp_report.md', '-o', output_path, '--toc']
    if template:
        cmd.extend(['--reference-doc', template])
    
    subprocess.run(cmd, check=True)
    os.remove('temp_report.md')
```

## 示例

### 示例 1：技术文档
```python
import subprocess

# Create comprehensive markdown
doc = """---
title: "API Documentation"
author: "Dev Team"
date: "2024-01-15"
toc: true
toc-depth: 2
---

# Introduction

This document describes the REST API for our service.

## Authentication

All API requests require an API key in the header:

```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### GET /users

Retrieve all users.

**Response:**

| Field | Type | Description |
|-------|------|-------------|
| id | integer | User ID |
| name | string | Full name |
| email | string | Email address |

### POST /users

Create a new user.

**Request Body:**

```
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 500 | Server Error |
"""

# Save markdown
with open('api_docs.md', 'w') as f:
    f.write(doc)

# Convert to Word
subprocess.run([
    'pandoc', 'api_docs.md',
    '-o', 'api_documentation.docx',
    '--toc',
    '--reference-doc', 'company_template.docx'
], check=True)

# Convert to PDF
subprocess.run([
    'pandoc', 'api_docs.md',
    '-o', 'api_documentation.pdf',
    '--toc',
    '-V', 'geometry:margin=1in',
    '-V', 'fontsize=11pt'
], check=True)
```

### 示例 2：从 Markdown 生成 PowerPoint 演示文稿
```python
slides_md = """---
title: "Q4 Business Review"
author: "Sales Team"
date: "January 2024"
---

# Overview

## Agenda

- Q4 Performance Summary
- Regional Highlights
- 2024 Outlook
- Q&A

# Q4 Performance

## Key Metrics

- Revenue: $12.5M (+15% YoY)
- New Customers: 250
- Retention Rate: 94%

## Regional Performance

:::::::::::::: {.columns}
::: {.column width="50%"}
**North America**

- Revenue: $6.2M
- Growth: +18%
:::

::: {.column width="50%"}
**Europe**

- Revenue: $4.1M
- Growth: +12%
:::
::::::::::::::

# 2024 Outlook

## Strategic Priorities

1. Expand APAC presence
2. Launch new product line
3. Improve customer onboarding

## Revenue Targets

| Quarter | Target |
|---------|--------|
| Q1 | $13M |
| Q2 | $14M |
| Q3 | $15M |
| Q4 | $16M |

# Thank You

## Questions?

Contact: sales@company.com
"""

with open('presentation.md', 'w') as f:
    f.write(slides_md)

subprocess.run([
    'pandoc', 'presentation.md',
    '-o', 'q4_review.pptx',
    '--reference-doc', 'company_slides.pptx'
], check=True)
```

## 注意事项

- 复杂的 Word 格式可能无法完美转换。
- PDF 转换需要依赖 LaTeX 或 wkhtmltopdf 工具。
- PowerPoint 中的动画功能可能无法保留。
- 部分高级表格可能需要手动调整。
- 图片的定位可能比较复杂。

## 安装方法
```bash
# macOS
brew install pandoc

# Ubuntu/Debian
sudo apt-get install pandoc

# Windows
choco install pandoc

# Python wrapper
pip install pypandoc
```

## 参考资源

- [Pandoc 用户手册](https://pandoc.org/MANUAL.html)
- [GitHub 仓库](https://github.com/jgm/pandoc)
- [Pandoc 模板](https://github.com/jgm/pandoc-templates)
- [pypandoc 文档](https://github.com/JessicaTegworthy/pypandoc)