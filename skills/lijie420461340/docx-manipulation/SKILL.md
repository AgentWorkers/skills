---
name: docx-manipulation
description: 使用 `python-docx` 库，可以以编程方式创建、编辑和操作 Word 文档。
author: claude-office-skills
version: "1.0"
tags: [document, word, docx, python-docx, automation]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: python-docx
  url: https://github.com/python-openxml/python-docx
  stars: 5.4k
---

# DOCX 文档处理技能

## 概述

该技能利用 **python-docx** 库，实现 Microsoft Word (.docx) 文档的程序化创建、编辑和操作。无需手动编辑，即可生成具有正确格式、样式、表格和图片的专业文档。

## 使用方法

1. 描述您希望在 Word 文档中创建或修改的内容。
2. 提供所需的源内容（文本、数据、图片）。
3. 我将生成相应的 python-docx 代码并执行它。

**示例提示：**
- “创建一份包含标题、标题页和表格的专业报告”
- “为该文档添加页眉和页脚”
- “生成一份包含占位符的合同文档”
- “将此 Markdown 内容转换为格式化的 Word 文档”

## 相关领域知识

### python-docx 基础知识
```python
from docx import Document
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

# Create new document
doc = Document()

# Or open existing
doc = Document('existing.docx')
```

### 文档结构
```
Document
├── sections (margins, orientation, size)
├── paragraphs (text with formatting)
├── tables (rows, cells, merged cells)
├── pictures (inline images)
└── styles (predefined formatting)
```

### 添加内容

#### 段落与标题
```python
# Add heading (level 0-9)
doc.add_heading('Main Title', level=0)
doc.add_heading('Section Title', level=1)

# Add paragraph
para = doc.add_paragraph('Normal text here')

# Add styled paragraph
doc.add_paragraph('Note: Important!', style='Intense Quote')

# Add with inline formatting
para = doc.add_paragraph()
para.add_run('Bold text').bold = True
para.add_run(' and ')
para.add_run('italic text').italic = True
```

#### 表格
```python
# Create table
table = doc.add_table(rows=3, cols=3)
table.style = 'Table Grid'

# Add content
table.cell(0, 0).text = 'Header 1'
table.rows[0].cells[1].text = 'Header 2'

# Add row dynamically
row = table.add_row()
row.cells[0].text = 'New data'

# Merge cells
a = table.cell(0, 0)
b = table.cell(0, 2)
a.merge(b)
```

#### 图片
```python
# Add image with size
doc.add_picture('image.png', width=Inches(4))

# Add to specific paragraph
para = doc.add_paragraph()
run = para.add_run()
run.add_picture('logo.png', width=Inches(1.5))
```

### 格式设置

#### 段落格式
```python
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Inches

para = doc.add_paragraph('Formatted text')
para.alignment = WD_ALIGN_PARAGRAPH.CENTER
para.paragraph_format.line_spacing = 1.5
para.paragraph_format.space_after = Pt(12)
para.paragraph_format.first_line_indent = Inches(0.5)
```

#### 字符格式
```python
run = para.add_run('Styled text')
run.bold = True
run.italic = True
run.underline = True
run.font.name = 'Arial'
run.font.size = Pt(14)
run.font.color.rgb = RGBColor(0x00, 0x00, 0xFF)  # Blue
```

#### 页面设置
```python
from docx.enum.section import WD_ORIENT
from docx.shared import Inches

section = doc.sections[0]
section.page_width = Inches(11)
section.page_height = Inches(8.5)
section.orientation = WD_ORIENT.LANDSCAPE
section.left_margin = Inches(1)
section.right_margin = Inches(1)
```

### 页眉与页脚
```python
section = doc.sections[0]

# Header
header = section.header
header.paragraphs[0].text = "Company Name"
header.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

# Footer with page numbers
footer = section.footer
para = footer.paragraphs[0]
para.text = "Page "
# Add page number field
run = para.add_run()
fldChar1 = OxmlElement('w:fldChar')
fldChar1.set(qn('w:fldCharType'), 'begin')
run._r.append(fldChar1)
# ... (field code for page number)
```

### 样式
```python
# Use built-in styles
doc.add_paragraph('Heading', style='Heading 1')
doc.add_paragraph('Quote', style='Quote')
doc.add_paragraph('List item', style='List Bullet')

# Common styles:
# - 'Normal', 'Heading 1-9', 'Title', 'Subtitle'
# - 'Quote', 'Intense Quote', 'List Bullet', 'List Number'
# - 'Table Grid', 'Light Shading', 'Medium Grid 1'
```

## 最佳实践

1. **先规划结构**：在编写代码之前先设计文档的层次结构。
2. **使用样式**：通过样式进行统一的格式设置，而非手动调整。
3. **频繁保存**：对于大型文档，定期调用 `doc.save()` 保存进度。
4. **处理错误**：在打开文件前检查文件是否存在。
5. **清理占位符**：填写内容后删除模板中的占位符。

## 常见应用模式

### 报告模板
```python
def create_report(title, sections):
    doc = Document()
    doc.add_heading(title, 0)
    doc.add_paragraph(f'Generated: {datetime.now()}')
    
    for section_title, content in sections.items():
        doc.add_heading(section_title, 1)
        doc.add_paragraph(content)
    
    return doc
```

### 根据数据生成表格
```python
def add_data_table(doc, headers, rows):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Table Grid'
    
    # Headers
    for i, header in enumerate(headers):
        table.rows[0].cells[i].text = header
        table.rows[0].cells[i].paragraphs[0].runs[0].bold = True
    
    # Data rows
    for row_data in rows:
        row = table.add_row()
        for i, value in enumerate(row_data):
            row.cells[i].text = str(value)
    
    return table
```

### 邮件合并功能
```python
def fill_template(template_path, replacements):
    doc = Document(template_path)
    
    for para in doc.paragraphs:
        for key, value in replacements.items():
            if f'{{{key}}}' in para.text:
                para.text = para.text.replace(f'{{{key}}}', value)
    
    return doc
```

## 示例

### 示例 1：创建商务信函
```python
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime

doc = Document()

# Letterhead
doc.add_paragraph('ACME Corporation')
doc.add_paragraph('123 Business Ave, Suite 100')
doc.add_paragraph('New York, NY 10001')
doc.add_paragraph()

# Date
doc.add_paragraph(datetime.now().strftime('%B %d, %Y'))
doc.add_paragraph()

# Recipient
doc.add_paragraph('Mr. John Smith')
doc.add_paragraph('XYZ Company')
doc.add_paragraph('456 Industry Blvd')
doc.add_paragraph('Chicago, IL 60601')
doc.add_paragraph()

# Salutation
doc.add_paragraph('Dear Mr. Smith,')
doc.add_paragraph()

# Body
body = """We are pleased to inform you that your proposal has been accepted...

[Letter body continues...]

Thank you for your continued partnership."""

for para_text in body.split('\n\n'):
    doc.add_paragraph(para_text)

doc.add_paragraph()
doc.add_paragraph('Sincerely,')
doc.add_paragraph()
doc.add_paragraph()
doc.add_paragraph('Jane Doe')
doc.add_paragraph('CEO, ACME Corporation')

doc.save('business_letter.docx')
```

### 示例 2：创建包含表格的报告
```python
from docx import Document
from docx.shared import Inches

doc = Document()
doc.add_heading('Q4 Sales Report', 0)

# Executive Summary
doc.add_heading('Executive Summary', 1)
doc.add_paragraph('Q4 2024 showed strong growth across all regions...')

# Sales Table
doc.add_heading('Regional Performance', 1)

table = doc.add_table(rows=1, cols=4)
table.style = 'Medium Grid 1 Accent 1'

headers = ['Region', 'Q3 Sales', 'Q4 Sales', 'Growth']
for i, header in enumerate(headers):
    table.rows[0].cells[i].text = header

data = [
    ['North America', '$1.2M', '$1.5M', '+25%'],
    ['Europe', '$800K', '$950K', '+18%'],
    ['Asia Pacific', '$600K', '$750K', '+25%'],
]

for row_data in data:
    row = table.add_row()
    for i, value in enumerate(row_data):
        row.cells[i].text = value

doc.save('sales_report.docx')
```

## 限制

- 无法执行宏或 VBA 代码。
- 复杂的模板可能会导致部分格式丢失。
- 对高级功能（如 SmartArt、图表）的支持有限。
- 不支持直接转换为 PDF 格式（需使用其他工具）。
- 阅读时的版本跟踪功能有限。

## 安装方法
```bash
pip install python-docx
```

## 资源

- [python-docx 文档](https://python-docx.readthedocs.io/)
- [GitHub 仓库](https://github.com/python-openxml/python-docx)
- [Office Open XML 规范](https://docs.microsoft.com/en-us/office/open-xml/open-xml-sdk)