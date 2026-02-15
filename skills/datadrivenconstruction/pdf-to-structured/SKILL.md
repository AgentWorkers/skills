---
name: "pdf-to-structured"
description: "从建筑相关的PDF文件中提取结构化数据。将规格书、物料清单（BOM）、进度表和报告从PDF格式转换为Excel、CSV或JSON格式。对于扫描后的文档，可以使用OCR技术进行识别；对于普通的PDF文件，则可以使用pdfplumber工具进行处理。"
---

# PDF到结构化数据的转换

## 概述

本技能基于DDC方法论（第2.4章），将非结构化的PDF文档转换为适合分析和集成的结构化格式。建设项目会产生大量的PDF文档——如规范、物料清单（BOM）、进度表和报告——这些文档需要被提取并进行处理。

**参考书籍**：《数据转换成结构化格式》（"Преобразование данных в структурированную форму"）

> “将数据从非结构化格式转换为结构化格式既是一门艺术，也是一门科学。这一过程通常占据了数据工程师工作的重要部分。”
> —— DDC书籍，第2.4章

## ETL流程概述

转换过程遵循ETL模式：
1. **提取**：加载PDF文档
2. **转换**：解析并组织文档内容
3. **加载**：将结果保存为CSV、Excel或JSON格式

## 快速入门

```python
import pdfplumber
import pandas as pd

# Extract table from PDF
with pdfplumber.open("construction_spec.pdf") as pdf:
    page = pdf.pages[0]
    table = page.extract_table()
    df = pd.DataFrame(table[1:], columns=table[0])
    df.to_excel("extracted_data.xlsx", index=False)
```

## 安装

```bash
# Core libraries
pip install pdfplumber pandas openpyxl

# For scanned PDFs (OCR)
pip install pytesseract pdf2image
# Also install Tesseract OCR: https://github.com/tesseract-ocr/tesseract

# For advanced PDF operations
pip install pypdf
```

## 原生PDF提取工具（pdfplumber）

### 从PDF中提取所有表格

```python
import pdfplumber
import pandas as pd

def extract_tables_from_pdf(pdf_path):
    """Extract all tables from a PDF file"""
    all_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for table_num, table in enumerate(tables):
                if table and len(table) > 1:
                    # First row as header
                    df = pd.DataFrame(table[1:], columns=table[0])
                    df['_page'] = page_num + 1
                    df['_table'] = table_num + 1
                    all_tables.append(df)

    if all_tables:
        return pd.concat(all_tables, ignore_index=True)
    return pd.DataFrame()

# Usage
df = extract_tables_from_pdf("material_specification.pdf")
df.to_excel("materials.xlsx", index=False)
```

### 带有布局的文本提取

```python
import pdfplumber

def extract_text_with_layout(pdf_path):
    """Extract text preserving layout structure"""
    full_text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)

    return "\n\n--- Page Break ---\n\n".join(full_text)

# Usage
text = extract_text_with_layout("project_report.pdf")
with open("report_text.txt", "w", encoding="utf-8") as f:
    f.write(text)
```

### 按位置提取特定表格

```python
import pdfplumber
import pandas as pd

def extract_table_from_area(pdf_path, page_num, bbox):
    """
    Extract table from specific area on page

    Args:
        pdf_path: Path to PDF file
        page_num: Page number (0-indexed)
        bbox: Bounding box (x0, top, x1, bottom) in points
    """
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        cropped = page.within_bbox(bbox)
        table = cropped.extract_table()

        if table:
            return pd.DataFrame(table[1:], columns=table[0])
    return pd.DataFrame()

# Usage - extract table from specific area
# bbox format: (left, top, right, bottom) in points (1 inch = 72 points)
df = extract_table_from_area("drawing.pdf", 0, (50, 100, 550, 400))
```

## 扫描PDF的处理（OCR）

### 从扫描PDF中提取文本

```python
import pytesseract
from pdf2image import convert_from_path
import pandas as pd

def ocr_scanned_pdf(pdf_path, language='eng'):
    """
    Extract text from scanned PDF using OCR

    Args:
        pdf_path: Path to scanned PDF
        language: Tesseract language code (eng, deu, rus, etc.)
    """
    # Convert PDF pages to images
    images = convert_from_path(pdf_path, dpi=300)

    extracted_text = []
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image, lang=language)
        extracted_text.append({
            'page': i + 1,
            'text': text
        })

    return pd.DataFrame(extracted_text)

# Usage
df = ocr_scanned_pdf("scanned_specification.pdf", language='eng')
df.to_csv("ocr_results.csv", index=False)
```

### OCR表格提取

```python
import pytesseract
from pdf2image import convert_from_path
import pandas as pd
import cv2
import numpy as np

def ocr_table_from_scanned_pdf(pdf_path, page_num=0):
    """Extract table from scanned PDF using OCR with table detection"""
    # Convert specific page to image
    images = convert_from_path(pdf_path, first_page=page_num+1,
                                last_page=page_num+1, dpi=300)
    image = np.array(images[0])

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Apply thresholding
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Extract text with table structure
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(gray, config=custom_config)

    # Parse text into table structure
    lines = text.strip().split('\n')
    data = [line.split() for line in lines if line.strip()]

    if data:
        # Assume first row is header
        df = pd.DataFrame(data[1:], columns=data[0] if len(data[0]) > 0 else None)
        return df
    return pd.DataFrame()

# Usage
df = ocr_table_from_scanned_pdf("scanned_bom.pdf")
print(df)
```

## 与建筑项目相关的特定数据提取

### 物料清单（BOM）提取

```python
import pdfplumber
import pandas as pd
import re

def extract_bom_from_pdf(pdf_path):
    """Extract Bill of Materials from construction PDF"""
    all_items = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if not table or len(table) < 2:
                    continue

                # Find header row (look for common BOM headers)
                header_keywords = ['item', 'description', 'quantity', 'unit', 'material']
                for i, row in enumerate(table):
                    if row and any(keyword in str(row).lower() for keyword in header_keywords):
                        # Found header, process remaining rows
                        headers = [str(h).strip() for h in row]
                        for data_row in table[i+1:]:
                            if data_row and any(cell for cell in data_row if cell):
                                item = dict(zip(headers, data_row))
                                all_items.append(item)
                        break

    return pd.DataFrame(all_items)

# Usage
bom = extract_bom_from_pdf("project_bom.pdf")
bom.to_excel("bom_extracted.xlsx", index=False)
```

### 项目进度表提取

```python
import pdfplumber
import pandas as pd
from datetime import datetime

def extract_schedule_from_pdf(pdf_path):
    """Extract project schedule/gantt data from PDF"""
    with pdfplumber.open(pdf_path) as pdf:
        all_tasks = []

        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if not table:
                    continue

                # Look for schedule-like table
                headers = table[0] if table else []

                # Check if it looks like a schedule
                schedule_keywords = ['task', 'activity', 'start', 'end', 'duration']
                if any(kw in str(headers).lower() for kw in schedule_keywords):
                    for row in table[1:]:
                        if row and any(cell for cell in row if cell):
                            task = dict(zip(headers, row))
                            all_tasks.append(task)

    df = pd.DataFrame(all_tasks)

    # Try to parse dates
    date_columns = ['Start', 'End', 'Start Date', 'End Date', 'Finish']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    return df

# Usage
schedule = extract_schedule_from_pdf("project_schedule.pdf")
print(schedule)
```

### 规范解析

```python
import pdfplumber
import pandas as pd
import re

def parse_specification_pdf(pdf_path):
    """Parse construction specification document"""
    specs = []

    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    # Parse sections (common spec format)
    section_pattern = r'(\d+\.\d+(?:\.\d+)?)\s+([A-Z][^\n]+)'
    sections = re.findall(section_pattern, full_text)

    for num, title in sections:
        specs.append({
            'section_number': num,
            'title': title.strip(),
            'level': len(num.split('.'))
        })

    return pd.DataFrame(specs)

# Usage
specs = parse_specification_pdf("technical_spec.pdf")
print(specs)
```

## 批量处理

### 处理多个PDF文件

```python
import pdfplumber
import pandas as pd
from pathlib import Path

def batch_extract_tables(folder_path, output_folder):
    """Process all PDFs in folder and extract tables"""
    pdf_files = Path(folder_path).glob("*.pdf")
    results = []

    for pdf_path in pdf_files:
        print(f"Processing: {pdf_path.name}")
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    tables = page.extract_tables()
                    for table_num, table in enumerate(tables):
                        if table and len(table) > 1:
                            df = pd.DataFrame(table[1:], columns=table[0])
                            df['_source_file'] = pdf_path.name
                            df['_page'] = page_num + 1

                            # Save individual table
                            output_name = f"{pdf_path.stem}_p{page_num+1}_t{table_num+1}.xlsx"
                            df.to_excel(Path(output_folder) / output_name, index=False)
                            results.append(df)
        except Exception as e:
            print(f"Error processing {pdf_path.name}: {e}")

    # Combined output
    if results:
        combined = pd.concat(results, ignore_index=True)
        combined.to_excel(Path(output_folder) / "all_tables.xlsx", index=False)

    return len(results)

# Usage
count = batch_extract_tables("./pdf_documents/", "./extracted/")
print(f"Extracted {count} tables")
```

## 提取后的数据清洗

```python
import pandas as pd

def clean_extracted_data(df):
    """Clean common issues in PDF-extracted data"""
    # Remove completely empty rows
    df = df.dropna(how='all')

    # Strip whitespace from string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()

    # Remove rows where all cells are empty strings
    df = df[df.apply(lambda row: any(cell != '' for cell in row), axis=1)]

    # Convert numeric columns
    for col in df.columns:
        # Try to convert to numeric
        numeric_series = pd.to_numeric(df[col], errors='coerce')
        if numeric_series.notna().sum() > len(df) * 0.5:  # More than 50% numeric
            df[col] = numeric_series

    return df

# Usage
df = extract_tables_from_pdf("document.pdf")
df_clean = clean_extracted_data(df)
df_clean.to_excel("clean_data.xlsx", index=False)
```

## 导出选项

```python
import pandas as pd
import json

def export_to_multiple_formats(df, base_name):
    """Export DataFrame to multiple formats"""
    # Excel
    df.to_excel(f"{base_name}.xlsx", index=False)

    # CSV
    df.to_csv(f"{base_name}.csv", index=False, encoding='utf-8-sig')

    # JSON
    df.to_json(f"{base_name}.json", orient='records', indent=2)

    # JSON Lines (for large datasets)
    df.to_json(f"{base_name}.jsonl", orient='records', lines=True)

# Usage
df = extract_tables_from_pdf("document.pdf")
export_to_multiple_formats(df, "extracted_data")
```

## 快速参考

| 任务 | 工具 | 代码 |
|------|------|------|
| 提取表格 | pdfplumber | `page.extract_table()` |
| 提取文本 | pdfplumber | `page.extract_text()` |
| OCR扫描 | pytesseract | `pytesseract.image_to_string(image)` |
| 合并PDF文件 | pypdf | `writer.add_page(page)` |
| 转换为图像 | pdf2image | `convert_from_path(pdf)` |

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| 未检测到表格 | 调整表格设置：`page.extract_table(table_settings={})` |
| 列对齐错误 | 使用可视化调试工具：`page.to_image().draw_rects()` |
| OCR质量差 | 提高DPI、预处理图像、使用正确的语言 |
| 内存问题 | 一次处理一个页面，处理完成后关闭PDF文件 |

## 资源

- **书籍**：Artem Boiko所著的《数据驱动的建造》（"Data-Driven Construction"），第2.4章
- **网站**：https://datadrivenconstruction.io
- **pdfplumber文档**：https://github.com/jsvine/pdfplumber
- **Tesseract OCR**：https://github.com/tesseract-ocr/tesseract

## 下一步

- 查看`image-to-data`以了解图像处理方法
- 查看`cad-to-data`以了解CAD/BIM数据提取方法
- 查看`etl-pipeline`以了解自动化处理工作流程
- 查看`data-quality-check`以了解提取数据的验证方法