---
name: pdf-to-docx
description: 使用 `pdf2docx` 将 PDF 文件转换为可编辑的 Word 文档
author: claude-office-skills
version: "1.0"
tags: [pdf, word, conversion, pdf2docx, editable]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: pdf2docx
  url: https://github.com/dothinking/pdf2docx
  stars: 3.3k
---

# 将PDF转换为Word的技能

## 概述

该技能使用`pdf2docx`（一个Python库）将PDF文件转换为可编辑的Word文档，同时保留布局、表格、图片和文本格式。与基于OCR的解决方案不同，`pdf2docx`直接提取PDF文件的原始内容，从而实现更准确的转换。

## 使用方法

1. 提供您想要转换的PDF文件。
2. （可选）指定需要转换的页面或转换选项。
3. 我会将文件转换为可编辑的Word文档。

**示例提示：**
- “将这份PDF报告转换为可编辑的Word文档。”
- “将这份PDF的第1-5页转换为Word格式。”
- “将这份扫描的文档提取为可编辑的文本。”
- “将这份PDF合同转换为Word格式以便编辑。”

## 相关领域知识

### `pdf2docx`基础

```python
from pdf2docx import Converter

# Basic conversion
cv = Converter('input.pdf')
cv.convert('output.docx')
cv.close()

# Or using context manager
with Converter('input.pdf') as cv:
    cv.convert('output.docx')
```

### 转换选项

```python
from pdf2docx import Converter

cv = Converter('input.pdf')

# Full document
cv.convert('output.docx')

# Specific pages (0-indexed)
cv.convert('output.docx', start=0, end=5)

# Single page
cv.convert('output.docx', pages=[0])

# Multiple specific pages
cv.convert('output.docx', pages=[0, 2, 4])

cv.close()
```

### 高级选项

```python
from pdf2docx import Converter

cv = Converter('input.pdf')

cv.convert(
    'output.docx',
    start=0,                    # Start page (0-indexed)
    end=None,                   # End page (None = last page)
    pages=None,                 # Specific pages list
    password=None,              # PDF password if encrypted
    min_section_height=20.0,    # Minimum height for section
    connected_border_tolerance=0.5,  # Border detection tolerance
    line_overlap_threshold=0.9, # Line merging threshold
    line_break_width_ratio=0.5, # Line break detection
    line_break_free_space_ratio=0.1,
    line_separate_threshold=5,  # Vertical line separation
    new_paragraph_free_space_ratio=0.85,
    float_image_ignorable_gap=5,
    page_margin_factor_top=0.5,
    page_margin_factor_bottom=0.5,
)

cv.close()
```

### 处理不同类型的PDF文件

#### 原生PDF文件（基于文本的）
```python
# Works best with native PDFs
cv = Converter('native_pdf.pdf')
cv.convert('output.docx')
cv.close()
```

#### 扫描PDF文件（基于图片的）
```python
# For scanned PDFs, use OCR first
# pdf2docx works best with native text PDFs
# Consider using pytesseract or PaddleOCR first

import pytesseract
from pdf2image import convert_from_path

# Convert PDF pages to images
images = convert_from_path('scanned.pdf')

# OCR each page
text = ''
for img in images:
    text += pytesseract.image_to_string(img)

# Then create Word document from text
```

### Python集成

```python
from pdf2docx import Converter
import os

def pdf_to_word(pdf_path, output_path=None, pages=None):
    """Convert PDF to Word document."""
    if output_path is None:
        output_path = pdf_path.replace('.pdf', '.docx')
    
    cv = Converter(pdf_path)
    
    if pages:
        cv.convert(output_path, pages=pages)
    else:
        cv.convert(output_path)
    
    cv.close()
    
    return output_path

# Usage
result = pdf_to_word('document.pdf')
print(f"Created: {result}")
```

### 批量转换

```python
from pdf2docx import Converter
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def convert_single(pdf_path, output_dir):
    """Convert single PDF to Word."""
    output_path = output_dir / pdf_path.with_suffix('.docx').name
    
    try:
        cv = Converter(str(pdf_path))
        cv.convert(str(output_path))
        cv.close()
        return f"Success: {pdf_path.name}"
    except Exception as e:
        return f"Error: {pdf_path.name} - {e}"

def batch_convert(input_dir, output_dir, max_workers=4):
    """Convert all PDFs in directory."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    pdf_files = list(input_path.glob('*.pdf'))
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(convert_single, pdf, output_path)
            for pdf in pdf_files
        ]
        
        for future in futures:
            print(future.result())

batch_convert('./pdfs', './word_docs')
```

### 解析PDF结构

```python
from pdf2docx import Converter

def analyze_pdf(pdf_path):
    """Analyze PDF structure before conversion."""
    cv = Converter(pdf_path)
    
    for i, page in enumerate(cv.pages):
        print(f"Page {i+1}:")
        print(f"  Size: {page.width} x {page.height}")
        print(f"  Blocks: {len(page.blocks)}")
        
        for block in page.blocks:
            if hasattr(block, 'text'):
                print(f"    Text block: {block.text[:50]}...")
            elif hasattr(block, 'image'):
                print(f"    Image block")
    
    cv.close()

analyze_pdf('document.pdf')
```

## 最佳实践

1. **检查PDF类型**：原生PDF文件的转换效果更好。
2. **先预览**：在完全转换之前先测试几页内容。
3. **处理表格**：复杂的表格可能需要手动调整。
4. **图片质量**：图片会以原始分辨率提取。
5. **字体处理**：某些字体可能会被替换为系统默认字体。

## 常见用法

### 带进度提示的转换
```python
from pdf2docx import Converter

def convert_with_progress(pdf_path, output_path):
    """Convert PDF with progress tracking."""
    cv = Converter(pdf_path)
    
    total_pages = len(cv.pages)
    print(f"Converting {total_pages} pages...")
    
    for i in range(total_pages):
        cv.convert(output_path, start=i, end=i+1)
        progress = (i + 1) / total_pages * 100
        print(f"Progress: {progress:.1f}%")
    
    cv.close()
    print("Conversion complete!")
```

### 仅提取表格
```python
from pdf2docx import Converter
from docx import Document

def extract_tables_to_word(pdf_path, output_path):
    """Extract only tables from PDF to Word."""
    cv = Converter(pdf_path)
    
    # First do full conversion
    temp_path = 'temp_full.docx'
    cv.convert(temp_path)
    cv.close()
    
    # Open and extract tables
    doc = Document(temp_path)
    new_doc = Document()
    
    for table in doc.tables:
        # Copy table to new document
        new_table = new_doc.add_table(rows=0, cols=len(table.columns))
        
        for row in table.rows:
            new_row = new_table.add_row()
            for i, cell in enumerate(row.cells):
                new_row.cells[i].text = cell.text
        
        new_doc.add_paragraph()  # Add spacing
    
    new_doc.save(output_path)
    os.remove(temp_path)
```

## 示例

### 示例1：合同转换
```python
from pdf2docx import Converter
import os

def convert_contract(pdf_path):
    """Convert contract PDF to editable Word with metadata."""
    
    # Define output path
    base_name = os.path.splitext(pdf_path)[0]
    output_path = f"{base_name}_editable.docx"
    
    # Convert
    cv = Converter(pdf_path)
    
    # Check page count
    page_count = len(cv.pages)
    print(f"Processing {page_count} pages...")
    
    # Convert all pages
    cv.convert(output_path)
    cv.close()
    
    print(f"Created: {output_path}")
    print(f"File size: {os.path.getsize(output_path) / 1024:.1f} KB")
    
    return output_path

# Usage
result = convert_contract('contract.pdf')
```

### 示例2：选择性页面转换
```python
from pdf2docx import Converter

def convert_selected_pages(pdf_path, page_ranges, output_path):
    """Convert specific page ranges to Word.
    
    page_ranges: List of tuples like [(1, 3), (5, 7)] for pages 1-3 and 5-7
    """
    cv = Converter(pdf_path)
    
    # Convert pages (0-indexed internally)
    all_pages = []
    for start, end in page_ranges:
        all_pages.extend(range(start - 1, end))  # Convert to 0-indexed
    
    cv.convert(output_path, pages=all_pages)
    cv.close()
    
    print(f"Converted pages: {page_ranges}")
    return output_path

# Convert pages 1-5 and 10-15
convert_selected_pages(
    'long_document.pdf',
    [(1, 5), (10, 15)],
    'selected_pages.docx'
)
```

### 示例3：将PDF报告转换为可编辑模板
```python
from pdf2docx import Converter
from docx import Document

def pdf_to_template(pdf_path, output_path):
    """Convert PDF report to Word template with placeholders."""
    
    # Convert PDF to Word
    cv = Converter(pdf_path)
    cv.convert(output_path)
    cv.close()
    
    # Open and add placeholder fields
    doc = Document(output_path)
    
    # Replace common fields with placeholders
    replacements = {
        'Company Name': '[COMPANY_NAME]',
        'Date:': 'Date: [DATE]',
        'Prepared by:': 'Prepared by: [AUTHOR]',
    }
    
    for para in doc.paragraphs:
        for old, new in replacements.items():
            if old in para.text:
                para.text = para.text.replace(old, new)
    
    # Also check tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for old, new in replacements.items():
                    if old in cell.text:
                        cell.text = cell.text.replace(old, new)
    
    doc.save(output_path)
    print(f"Template created: {output_path}")

pdf_to_template('annual_report.pdf', 'report_template.docx')
```

### 示例4：批量处理发票
```python
from pdf2docx import Converter
from pathlib import Path
import json

def process_invoices(input_folder, output_folder):
    """Convert PDF invoices to editable Word documents."""
    
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(exist_ok=True)
    
    results = []
    
    for pdf_file in input_path.glob('*.pdf'):
        output_file = output_path / pdf_file.with_suffix('.docx').name
        
        try:
            cv = Converter(str(pdf_file))
            cv.convert(str(output_file))
            cv.close()
            
            results.append({
                'file': pdf_file.name,
                'status': 'success',
                'output': str(output_file)
            })
            
        except Exception as e:
            results.append({
                'file': pdf_file.name,
                'status': 'error',
                'error': str(e)
            })
    
    # Save results log
    with open(output_path / 'conversion_log.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Summary
    success = sum(1 for r in results if r['status'] == 'success')
    print(f"Converted {success}/{len(results)} files")
    
    return results

results = process_invoices('./invoices_pdf', './invoices_word')
```

## 限制

- 扫描PDF文件需要先进行OCR预处理。
- 复杂的布局可能无法完美转换。
- 一些字体可能无法被正确显示。
- PDF中的水印会一起被转换进来。
- 受保护的/加密的PDF文件需要密码才能转换。

## 安装方法

```bash
pip install pdf2docx

# For image handling
pip install Pillow
```

## 资源

- [GitHub仓库](https://github.com/dothinking/pdf2docx)
- [文档](https://pdf2docx.readthedocs.io/)
- [PyPI包](https://pypi.org/project/pdf2docx/)