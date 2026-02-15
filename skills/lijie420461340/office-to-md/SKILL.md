---
name: office-to-md
description: 使用 Microsoft 的 markitdown 工具将 Office 文档（Word、Excel、PowerPoint、PDF）转换为 Markdown 格式。
author: claude-office-skills
version: "1.0"
tags: [markdown, conversion, markitdown, microsoft, office]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: markitdown
  url: https://github.com/microsoft/markitdown
  stars: 86k
---

# 将 Office 文档转换为 Markdown 的技能

## 概述

该技能支持使用 **markitdown**（微软开源的文档转 Markdown 工具）将各种 Office 格式的文件转换为 Markdown 格式。这非常适合让 Office 文档具备可搜索性、版本控制功能，并且更易于被人工智能处理。

## 使用方法

1. 提供需要转换的 Office 文件（如 Word、Excel、PowerPoint、PDF 等）。
2. （可选）指定转换选项。
3. 我会将文件转换为格式规范的 Markdown 格式。

**示例命令：**
- “将这个 Word 文档转换为 Markdown。”
- “将这个 PowerPoint 文件转换为 Markdown 格式的笔记。”
- “从这个 PDF 文件中提取内容并转换为 Markdown。”
- “将这个 Excel 文件转换为 Markdown 格式的表格。”

## 相关知识

### markitdown 基础知识
```python
from markitdown import MarkItDown

# Initialize converter
md = MarkItDown()

# Convert file
result = md.convert("document.docx")
print(result.text_content)

# Save to file
with open("output.md", "w") as f:
    f.write(result.text_content)
```

### 支持的格式

| 格式 | 扩展名 | 说明 |
|--------|-----------|-------|
| Word | .docx | 包含纯文本、表格和基本格式。 |
| Excel | .xlsx | 可转换为 Markdown 表格。 |
| PowerPoint | .pptx | 幻灯片内容会被分割成独立的段落。 |
| PDF | .pdf | 可提取文本内容。 |
| HTML | .html | 生成格式规范的 Markdown。 |
| 图片 | .jpg, .png | 可通过视觉模型进行OCR处理（生成图片描述）。 |
| 音频 | .mp3, .wav | 可进行语音转文字处理。 |
| ZIP | .zip | 会处理压缩文件内的所有内容。 |

### 基本使用方法

#### Python API
```python
from markitdown import MarkItDown

# Simple conversion
md = MarkItDown()
result = md.convert("document.docx")

# Access content
markdown_text = result.text_content

# With options
md = MarkItDown(
    llm_client=None,      # Optional LLM for enhanced processing
    llm_model=None        # Model name if using LLM
)
```

#### 命令行工具
```bash
# Install
pip install markitdown

# Convert file
markitdown document.docx > output.md

# Or with output file
markitdown document.docx -o output.md
```

### Word 文档转换方法
```python
from markitdown import MarkItDown

md = MarkItDown()

# Convert Word document
result = md.convert("report.docx")

# Output preserves:
# - Headings (as # headers)
# - Bold/italic formatting
# - Lists (bulleted and numbered)
# - Tables (as markdown tables)
# - Hyperlinks

print(result.text_content)
```

**示例输出：**
```markdown
# Annual Report 2024

## Executive Summary

This report summarizes the key achievements and challenges...

### Key Metrics

| Metric | 2023 | 2024 | Change |
|--------|------|------|--------|
| Revenue | $10M | $12M | +20% |
| Users | 50K | 75K | +50% |

## Detailed Analysis

The following sections provide...
```

### Excel 文件转换方法
```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("data.xlsx")

# Each sheet becomes a section
# Data becomes markdown tables
print(result.text_content)
```

**示例输出：**
```markdown
## Sheet1

| Name | Department | Salary |
|------|------------|--------|
| John | Engineering | $80,000 |
| Jane | Marketing | $75,000 |

## Sheet2

| Product | Q1 | Q2 | Q3 | Q4 |
|---------|----|----|----|----|
| Widget A | 100 | 120 | 150 | 180 |
```

### PowerPoint 文件转换方法
```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("presentation.pptx")

# Each slide becomes a section
# Speaker notes included if present
print(result.text_content)
```

**示例输出：**
```markdown
# Slide 1: Company Overview

Our mission is to...

## Key Points
- Innovation first
- Customer focused
- Global reach

---

# Slide 2: Market Analysis

The market opportunity is significant...

**Notes:** Mention the competitor analysis here
```

### PDF 文件转换方法
```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("document.pdf")

# Extracts text content
# Tables converted where detected
print(result.text_content)
```

### 图片转换方法（使用视觉模型）
```python
from markitdown import MarkItDown
import anthropic

# Use Claude for image description
client = anthropic.Anthropic()

md = MarkItDown(
    llm_client=client,
    llm_model="claude-sonnet-4-20250514"
)

result = md.convert("diagram.png")
print(result.text_content)

# Output: Description of the image content
```

### 批量转换
```python
from markitdown import MarkItDown
from pathlib import Path

def batch_convert(input_dir, output_dir):
    """Convert all Office files to Markdown."""
    md = MarkItDown()
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    extensions = ['.docx', '.xlsx', '.pptx', '.pdf']
    
    for ext in extensions:
        for file in input_path.glob(f'*{ext}'):
            try:
                result = md.convert(str(file))
                output_file = output_path / f"{file.stem}.md"
                
                with open(output_file, 'w') as f:
                    f.write(result.text_content)
                
                print(f"Converted: {file.name}")
            except Exception as e:
                print(f"Error converting {file.name}: {e}")

batch_convert('./documents', './markdown')
```

## 使用建议

1. **检查转换结果的质量**：仔细核对转换后的 Markdown 文件是否准确无误。
2. **处理表格**：复杂的表格可能需要手动调整。
3. **保持结构一致**：在源文档中使用统一的标题层级。
4. **处理图片**：对于重要的图片，建议使用视觉模型进行识别处理。
5. **版本控制**：将转换后的 Markdown 文件存储在 Git 中以便追踪修改历史。

## 常见应用场景

- **文档归档**：将多种格式的文档统一转换为 Markdown 格式。
- **构建适合 AI 处理的语料库**：将文档转换为适合人工智能分析的格式。

## 实例

- **示例 1：文档集转换**：将一系列文档转换为 Markdown 格式。
- **示例 2：会议记录处理**：将会议笔记转换为 Markdown 格式。
- **示例 3：Excel 数据转换为文档**：将 Excel 数据转换为结构化的 Markdown 文档。

## 注意事项

- 复杂的格式可能会被简化。
- 图片不会被直接嵌入到转换后的 Markdown 中（需要使用视觉模型生成图片描述）。
- 一些表格结构可能无法完美转换。
- Word 文档中的修订痕迹可能无法被保留。
- 文档中的注释可能无法被提取出来。

## 安装方法
```bash
pip install markitdown

# For image/audio processing
pip install markitdown[all]

# For specific features
pip install markitdown[images]  # Image OCR
pip install markitdown[audio]   # Audio transcription
```

## 参考资源

- [GitHub 仓库](https://github.com/microsoft/markitdown)
- [PyPI 包](https://pypi.org/project/markitdown/)
- [支持的格式列表](https://github.com/microsoft/markitdown#supported-formats)