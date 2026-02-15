---
slug: "pdf-construction"
display_name: "PDF Construction"
description: "**建筑文档的PDF处理：**  
包括请求报价（RFIs）、提交文件、技术规范以及图纸包。  
主要功能包括：  
- 提取数据；  
- 合并多个文件包；  
- 填写表格。"
---

# 用于建筑行业的PDF处理工具

## 概述

本工具基于Anthropic的PDF处理技能开发，专为建筑行业文档工作流程而设计。

## 建筑行业应用场景

### 1. 信息请求（RFI）处理
从信息请求（Request for Information）文档中提取结构化数据。

```python
from pypdf import PdfReader
import re

def extract_rfi_data(pdf_path: str) -> dict:
    """Extract RFI fields from PDF."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    # Parse common RFI fields
    rfi_data = {
        'rfi_number': re.search(r'RFI\s*#?\s*(\d+)', text),
        'subject': re.search(r'Subject:?\s*(.+?)(?:\n|$)', text),
        'from': re.search(r'From:?\s*(.+?)(?:\n|$)', text),
        'to': re.search(r'To:?\s*(.+?)(?:\n|$)', text),
        'date': re.search(r'Date:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text),
        'spec_section': re.search(r'Spec(?:ification)?\s*Section:?\s*(.+?)(?:\n|$)', text),
        'drawing_ref': re.search(r'Drawing\s*(?:Ref)?:?\s*(.+?)(?:\n|$)', text),
    }

    return {k: v.group(1) if v else None for k, v in rfi_data.items()}
```

### 2. 提交文件包生成
将多个PDF文件合并成有序的提交文件包。

```python
from pypdf import PdfWriter, PdfReader
from pathlib import Path

def create_submittal_package(
    cover_sheet: str,
    product_data: list,
    shop_drawings: list,
    output_path: str
) -> str:
    """Create organized submittal package."""
    writer = PdfWriter()

    # Add cover sheet
    writer.append(cover_sheet)

    # Add bookmarked sections
    page_num = len(PdfReader(cover_sheet).pages)

    # Product Data section
    writer.add_outline_item("Product Data", page_num)
    for pdf in product_data:
        writer.append(pdf)
        page_num += len(PdfReader(pdf).pages)

    # Shop Drawings section
    writer.add_outline_item("Shop Drawings", page_num)
    for pdf in shop_drawings:
        writer.append(pdf)
        page_num += len(PdfReader(pdf).pages)

    with open(output_path, "wb") as output:
        writer.write(output)

    return output_path
```

### 3. 规范内容提取
提取规范文件中的相关内容以供分析。

```python
import pdfplumber

def extract_spec_sections(pdf_path: str) -> dict:
    """Extract specification sections by division."""
    sections = {}

    with pdfplumber.open(pdf_path) as pdf:
        current_section = None
        current_text = []

        for page in pdf.pages:
            text = page.extract_text()

            # Match CSI MasterFormat sections
            for line in text.split('\n'):
                # Match section headers like "03 30 00 - Cast-in-Place Concrete"
                match = re.match(r'^(\d{2}\s?\d{2}\s?\d{2})\s*[-–]\s*(.+)$', line)
                if match:
                    if current_section:
                        sections[current_section] = '\n'.join(current_text)
                    current_section = match.group(1).replace(' ', '')
                    current_text = [match.group(2)]
                elif current_section:
                    current_text.append(line)

        if current_section:
            sections[current_section] = '\n'.join(current_text)

    return sections
```

### 4. 图纸文件提取
按图纸类型将图纸文件分开。

```python
def split_drawing_package(pdf_path: str, output_dir: str) -> list:
    """Split drawing package into individual sheets."""
    reader = PdfReader(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    sheets = []
    for i, page in enumerate(reader.pages):
        # Extract sheet number from page (if text-based)
        text = page.extract_text()
        sheet_match = re.search(r'([A-Z]+[-]?\d+)', text[:500])
        sheet_name = sheet_match.group(1) if sheet_match else f"Page_{i+1:03d}"

        writer = PdfWriter()
        writer.add_page(page)

        output_file = output_dir / f"{sheet_name}.pdf"
        with open(output_file, "wb") as f:
            writer.write(f)

        sheets.append(str(output_file))

    return sheets
```

## 与DDC流程的集成

```python
# Example: Process RFI and add to tracking spreadsheet
import pandas as pd

# Extract RFI data
rfi_data = extract_rfi_data("RFI_045.pdf")

# Load existing tracker
tracker = pd.read_excel("RFI_Log.xlsx")

# Add new entry
new_row = pd.DataFrame([rfi_data])
tracker = pd.concat([tracker, new_row], ignore_index=True)

# Save updated tracker
tracker.to_excel("RFI_Log.xlsx", index=False)
```

## 所需依赖库

```bash
pip install pypdf pdfplumber reportlab
```

## 参考资源

- **原始来源**：Anthropic PDF处理技能
- **PyPDF文档**：https://pypdf.readthedocs.io/
- **PDFPlumber**：https://github.com/jsvine/pdfplumber