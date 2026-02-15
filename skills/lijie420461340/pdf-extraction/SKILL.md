---
name: pdf-extraction
description: 使用 `pdfplumber` 从 PDF 文件中提取文本、表格和元数据
author: claude-office-skills
version: "1.0"
tags: [pdf, extraction, pdfplumber, tables, text]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: pdfplumber
  url: https://github.com/jsvine/pdfplumber
  stars: 9.6k
---

# PDF提取技能

## 概述

该技能利用 **pdfplumber**（一个用于PDF数据提取的Go语言库）实现从PDF文档中精确提取文本、表格和元数据的功能。与普通的PDF阅读器不同，pdfplumber提供了详细的字符级定位功能、准确的表格检测机制以及可视化的调试工具。

## 使用方法

1. 提供您希望从中提取数据的PDF文件。
2. 指定您需要提取的内容：文本、表格、图片还是元数据。
3. 我将生成相应的pdfplumber代码并执行它。

**示例提示：**
- “从这份财务报告中提取所有表格。”
- “获取该文档第5到10页的文本。”
- “从这份PDF中找到并提取发票总金额。”
- “将这张PDF中的表格转换为CSV/Excel格式。”

## 相关领域知识

### pdfplumber基础
```python
import pdfplumber

# Open PDF
with pdfplumber.open('document.pdf') as pdf:
    # Access pages
    first_page = pdf.pages[0]
    
    # Document metadata
    print(pdf.metadata)
    
    # Number of pages
    print(len(pdf.pages))
```

### PDF结构
```
PDF Document
├── metadata (title, author, creation date)
├── pages[]
│   ├── chars (individual characters with position)
│   ├── words (grouped characters)
│   ├── lines (horizontal/vertical lines)
│   ├── rects (rectangles)
│   ├── curves (bezier curves)
│   └── images (embedded images)
└── outline (bookmarks/TOC)
```

### 文本提取

#### 基本文本提取
```python
with pdfplumber.open('document.pdf') as pdf:
    # Single page
    text = pdf.pages[0].extract_text()
    
    # All pages
    full_text = ''
    for page in pdf.pages:
        full_text += page.extract_text() or ''
```

#### 高级文本提取选项
```python
# With layout preservation
text = page.extract_text(
    x_tolerance=3,      # Horizontal tolerance for grouping
    y_tolerance=3,      # Vertical tolerance
    layout=True,        # Preserve layout
    x_density=7.25,     # Chars per unit width
    y_density=13        # Chars per unit height
)

# Extract words with positions
words = page.extract_words(
    x_tolerance=3,
    y_tolerance=3,
    keep_blank_chars=False,
    use_text_flow=False
)

# Each word includes: text, x0, top, x1, bottom, etc.
for word in words:
    print(f"{word['text']} at ({word['x0']}, {word['top']})")
```

#### 字符级访问
```python
# Get all characters
chars = page.chars

for char in chars:
    print(f"'{char['text']}' at ({char['x0']}, {char['top']})")
    print(f"  Font: {char['fontname']}, Size: {char['size']}")
```

### 表格提取

#### 基本表格提取
```python
with pdfplumber.open('report.pdf') as pdf:
    page = pdf.pages[0]
    
    # Extract all tables
    tables = page.extract_tables()
    
    for i, table in enumerate(tables):
        print(f"Table {i+1}:")
        for row in table:
            print(row)
```

#### 高级表格设置
```python
# Custom table detection
table_settings = {
    "vertical_strategy": "lines",      # or "text", "explicit"
    "horizontal_strategy": "lines",
    "explicit_vertical_lines": [],     # Custom line positions
    "explicit_horizontal_lines": [],
    "snap_tolerance": 3,
    "snap_x_tolerance": 3,
    "snap_y_tolerance": 3,
    "join_tolerance": 3,
    "edge_min_length": 3,
    "min_words_vertical": 3,
    "min_words_horizontal": 1,
    "intersection_tolerance": 3,
    "text_tolerance": 3,
    "text_x_tolerance": 3,
    "text_y_tolerance": 3,
}

tables = page.extract_tables(table_settings)
```

#### 表格定位
```python
# Find tables (without extracting)
table_finder = page.find_tables()

for table in table_finder:
    print(f"Table at: {table.bbox}")  # (x0, top, x1, bottom)
    
    # Extract specific table
    data = table.extract()
```

### 可视化调试
```python
# Create visual debug image
im = page.to_image(resolution=150)

# Draw detected objects
im.draw_rects(page.chars)        # Character bounding boxes
im.draw_rects(page.words)        # Word bounding boxes
im.draw_lines(page.lines)        # Lines
im.draw_rects(page.rects)        # Rectangles

# Save debug image
im.save('debug.png')

# Debug tables
im.reset()
im.debug_tablefinder()
im.save('table_debug.png')
```

### 裁剪与过滤

#### 按区域裁剪
```python
# Define bounding box (x0, top, x1, bottom)
bbox = (0, 0, 300, 200)

# Crop page
cropped = page.crop(bbox)

# Extract from cropped area
text = cropped.extract_text()
tables = cropped.extract_tables()
```

#### 按位置过滤
```python
# Filter characters by region
def within_bbox(obj, bbox):
    x0, top, x1, bottom = bbox
    return (obj['x0'] >= x0 and obj['x1'] <= x1 and
            obj['top'] >= top and obj['bottom'] <= bottom)

bbox = (100, 100, 400, 300)
filtered_chars = [c for c in page.chars if within_bbox(c, bbox)]
```

#### 按字体过滤
```python
# Get text by font
def extract_by_font(page, font_name):
    chars = [c for c in page.chars if font_name in c['fontname']]
    return ''.join(c['text'] for c in chars)

# Extract bold text (often "Bold" in font name)
bold_text = extract_by_font(page, 'Bold')

# Extract by size
large_chars = [c for c in page.chars if c['size'] > 14]
```

### 元数据和结构
```python
with pdfplumber.open('document.pdf') as pdf:
    # Document metadata
    meta = pdf.metadata
    print(f"Title: {meta.get('Title')}")
    print(f"Author: {meta.get('Author')}")
    print(f"Created: {meta.get('CreationDate')}")
    
    # Page info
    for i, page in enumerate(pdf.pages):
        print(f"Page {i+1}: {page.width} x {page.height}")
        print(f"  Rotation: {page.rotation}")
```

## 最佳实践

1. **可视化调试**：使用 `to_image()` 功能来理解PDF的结构。
2. **调整表格提取设置**：根据具体的PDF文件调整相关参数。
3. **处理扫描生成的PDF文件**：建议先使用OCR工具进行文字识别（本技能适用于纯文本PDF）。
4. **分页处理**：对于大型PDF文件，避免一次性加载所有内容。
5. **验证文本内容**：某些PDF文件实际上是图片格式，请确保其中确实包含可提取的文本。

## 常见应用场景

### 将所有表格提取到DataFrame中
```python
import pandas as pd

def pdf_tables_to_dataframes(pdf_path):
    """Extract all tables from PDF as pandas DataFrames."""
    dfs = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            
            for j, table in enumerate(tables):
                if table and len(table) > 1:
                    # First row as header
                    df = pd.DataFrame(table[1:], columns=table[0])
                    df['_page'] = i + 1
                    df['_table'] = j + 1
                    dfs.append(df)
    
    return dfs
```

### 提取特定区域的内容
```python
def extract_invoice_amount(pdf_path):
    """Extract amount from typical invoice layout."""
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        
        # Search for "Total" and get nearby numbers
        words = page.extract_words()
        
        for i, word in enumerate(words):
            if 'total' in word['text'].lower():
                # Look at next few words
                for next_word in words[i+1:i+5]:
                    text = next_word['text'].replace(',', '').replace('$', '')
                    try:
                        return float(text)
                    except ValueError:
                        continue
    
    return None
```

### 多列布局的表格处理
```python
def extract_columns(page, num_columns=2):
    """Extract text from multi-column layout."""
    width = page.width
    col_width = width / num_columns
    
    columns = []
    for i in range(num_columns):
        x0 = i * col_width
        x1 = (i + 1) * col_width
        
        cropped = page.crop((x0, 0, x1, page.height))
        columns.append(cropped.extract_text())
    
    return columns
```

## 示例

### 示例1：财务报告中的表格提取
```python
import pdfplumber
import pandas as pd

def extract_financial_tables(pdf_path):
    """Extract tables from financial report and save to Excel."""
    
    with pdfplumber.open(pdf_path) as pdf:
        all_tables = []
        
        for page_num, page in enumerate(pdf.pages):
            # Debug: save table visualization
            im = page.to_image()
            im.debug_tablefinder()
            im.save(f'debug_page_{page_num+1}.png')
            
            # Extract tables
            tables = page.extract_tables({
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
                "snap_tolerance": 5,
            })
            
            for table in tables:
                if table and len(table) > 1:
                    # Clean data
                    clean_table = []
                    for row in table:
                        clean_row = [cell.strip() if cell else '' for cell in row]
                        clean_table.append(clean_row)
                    
                    df = pd.DataFrame(clean_table[1:], columns=clean_table[0])
                    df['Source Page'] = page_num + 1
                    all_tables.append(df)
        
        # Save to Excel with multiple sheets
        with pd.ExcelWriter('extracted_tables.xlsx') as writer:
            for i, df in enumerate(all_tables):
                df.to_excel(writer, sheet_name=f'Table_{i+1}', index=False)
        
        return all_tables

tables = extract_financial_tables('annual_report.pdf')
print(f"Extracted {len(tables)} tables")
```

### 示例2：发票数据的提取
```python
import pdfplumber
import re
from datetime import datetime

def extract_invoice_data(pdf_path):
    """Extract structured data from invoice PDF."""
    
    data = {
        'invoice_number': None,
        'date': None,
        'total': None,
        'line_items': []
    }
    
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
        
        # Extract invoice number
        inv_match = re.search(r'Invoice\s*#?\s*:?\s*(\w+)', text, re.IGNORECASE)
        if inv_match:
            data['invoice_number'] = inv_match.group(1)
        
        # Extract date
        date_match = re.search(r'Date\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text)
        if date_match:
            data['date'] = date_match.group(1)
        
        # Extract total
        total_match = re.search(r'Total\s*:?\s*\$?([\d,]+\.?\d*)', text, re.IGNORECASE)
        if total_match:
            data['total'] = float(total_match.group(1).replace(',', ''))
        
        # Extract line items from table
        tables = page.extract_tables()
        for table in tables:
            if table and any('description' in str(row).lower() for row in table[:2]):
                # Found line items table
                for row in table[1:]:  # Skip header
                    if row and len(row) >= 3:
                        data['line_items'].append({
                            'description': row[0],
                            'quantity': row[1] if len(row) > 1 else None,
                            'amount': row[-1]
                        })
    
    return data

invoice = extract_invoice_data('invoice.pdf')
print(f"Invoice #{invoice['invoice_number']}")
print(f"Total: ${invoice['total']}")
```

### 示例3：简历/简历文件的解析
```python
import pdfplumber

def parse_resume(pdf_path):
    """Extract structured sections from resume."""
    
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ''
        for page in pdf.pages:
            full_text += (page.extract_text() or '') + '\n'
        
        # Common resume sections
        sections = {
            'contact': '',
            'summary': '',
            'experience': '',
            'education': '',
            'skills': ''
        }
        
        # Split by common headers
        import re
        section_patterns = {
            'summary': r'(summary|objective|profile)',
            'experience': r'(experience|employment|work history)',
            'education': r'(education|academic)',
            'skills': r'(skills|competencies|technical)'
        }
        
        lines = full_text.split('\n')
        current_section = 'contact'
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if line is a section header
            for section, pattern in section_patterns.items():
                if re.match(pattern, line_lower):
                    current_section = section
                    break
            
            sections[current_section] += line + '\n'
        
        return sections

resume = parse_resume('resume.pdf')
print("Skills:", resume['skills'])
```

## 限制

- 无法从扫描或图片格式的PDF文件中提取数据（请先使用OCR工具）。
- 复杂的PDF布局可能需要手动调整提取参数。
- 部分PDF加密格式可能不被支持。
- 嵌入的字体可能会影响文本提取的准确性。
- 该工具不提供直接的PDF编辑功能。

## 安装方法
```bash
pip install pdfplumber

# For image debugging (optional)
pip install Pillow
```

## 资源链接

- [pdfplumber官方文档](https://github.com/jsvine/pdfplumber)
- [表格提取指南](https://github.com/jsvine/pdfplumber#extracting-tables)
- [可视化调试功能说明](https://github.com/jsvine/pdfplumber#visual-debugging)