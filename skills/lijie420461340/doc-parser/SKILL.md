---
name: doc-parser
description: 使用 IBM 的 docling 工具解析复杂的文档——支持处理表格、图表以及多列布局。
author: claude-office-skills
version: "1.0"
tags: [document-parsing, docling, ibm, tables, layout]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: docling
  url: https://github.com/DS4SD/docling
  stars: 51.5k
---

# 文档解析技能

## 概述

该技能利用 **docling**（IBM 的先进文档理解库）实现高级文档解析功能。能够解析复杂的 PDF、Word 文档和图片，同时保留文档结构，提取表格、图表，并处理多列布局。

## 使用方法

1. 提供需要解析的文档。
2. 指定您想要提取的内容（文本、表格、图表等）。
3. 系统会对其进行解析并返回结构化数据。

**示例提示：**
- “解析这份 PDF 并提取所有表格。”
- “将这篇学术论文转换为结构化的 Markdown 格式。”
- “从这份文档中提取图表及其标题。”
- “解析这份报告并保留其原始结构。”

## 相关领域知识

### docling 基础知识

```python
from docling.document_converter import DocumentConverter

# Initialize converter
converter = DocumentConverter()

# Convert document
result = converter.convert("document.pdf")

# Access parsed content
doc = result.document
print(doc.export_to_markdown())
```

### 支持的格式

| 格式 | 扩展名 | 说明 |
|--------|-----------|-------|
| PDF | .pdf | 支持原生 PDF 和扫描文档 |
| Word | .docx | 完整保留文档结构 |
| PowerPoint | .pptx | 幻灯片按章节进行解析 |
| 图片 | .png, .jpg | 支持 OCR 和布局分析 |
| HTML | .html | 保留文档结构 |

### 基本用法

```python
from docling.document_converter import DocumentConverter

# Create converter
converter = DocumentConverter()

# Convert single document
result = converter.convert("report.pdf")

# Access document
doc = result.document

# Export options
markdown = doc.export_to_markdown()
text = doc.export_to_text()
json_doc = doc.export_to_dict()
```

### 高级配置

```python
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions

# Configure pipeline
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = True
pipeline_options.do_table_structure = True
pipeline_options.table_structure_options.do_cell_matching = True

# Create converter with options
converter = DocumentConverter(
    allowed_formats=[InputFormat.PDF, InputFormat.DOCX],
    pdf_backend_options=pipeline_options
)

result = converter.convert("document.pdf")
```

### 文档结构

```python
# Document hierarchy
doc = result.document

# Access metadata
print(doc.name)
print(doc.origin)

# Iterate through content
for element in doc.iterate_items():
    print(f"Type: {element.type}")
    print(f"Text: {element.text}")
    
    if element.type == "table":
        print(f"Rows: {len(element.data.table_cells)}")
```

### 提取表格

```python
from docling.document_converter import DocumentConverter
import pandas as pd

def extract_tables(doc_path):
    """Extract all tables from document."""
    converter = DocumentConverter()
    result = converter.convert(doc_path)
    doc = result.document
    
    tables = []
    
    for element in doc.iterate_items():
        if element.type == "table":
            # Get table data
            table_data = element.export_to_dataframe()
            tables.append({
                'page': element.prov[0].page_no if element.prov else None,
                'dataframe': table_data
            })
    
    return tables

# Usage
tables = extract_tables("report.pdf")
for i, table in enumerate(tables):
    print(f"Table {i+1} on page {table['page']}:")
    print(table['dataframe'])
```

### 提取图表

```python
def extract_figures(doc_path, output_dir):
    """Extract figures with captions."""
    import os
    
    converter = DocumentConverter()
    result = converter.convert(doc_path)
    doc = result.document
    
    figures = []
    os.makedirs(output_dir, exist_ok=True)
    
    for element in doc.iterate_items():
        if element.type == "picture":
            figure_info = {
                'caption': element.caption if hasattr(element, 'caption') else None,
                'page': element.prov[0].page_no if element.prov else None,
            }
            
            # Save image if available
            if hasattr(element, 'image'):
                img_path = os.path.join(output_dir, f"figure_{len(figures)+1}.png")
                element.image.save(img_path)
                figure_info['path'] = img_path
            
            figures.append(figure_info)
    
    return figures
```

### 处理多列布局

```python
from docling.document_converter import DocumentConverter

def parse_multicolumn(doc_path):
    """Parse document with multi-column layout."""
    
    converter = DocumentConverter()
    result = converter.convert(doc_path)
    doc = result.document
    
    # docling automatically handles column detection
    # Text is returned in reading order
    
    structured_content = []
    
    for element in doc.iterate_items():
        content_item = {
            'type': element.type,
            'text': element.text if hasattr(element, 'text') else None,
            'level': element.level if hasattr(element, 'level') else None,
        }
        
        # Add bounding box if available
        if element.prov:
            content_item['bbox'] = element.prov[0].bbox
            content_item['page'] = element.prov[0].page_no
        
        structured_content.append(content_item)
    
    return structured_content
```

### 导出格式

```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("document.pdf")
doc = result.document

# Markdown export
markdown = doc.export_to_markdown()
with open("output.md", "w") as f:
    f.write(markdown)

# Plain text
text = doc.export_to_text()

# JSON/dict format
json_doc = doc.export_to_dict()

# HTML format (if supported)
# html = doc.export_to_html()
```

### 批量处理

```python
from docling.document_converter import DocumentConverter
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def batch_parse(input_dir, output_dir, max_workers=4):
    """Parse multiple documents in parallel."""
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    converter = DocumentConverter()
    
    def process_single(doc_path):
        try:
            result = converter.convert(str(doc_path))
            md = result.document.export_to_markdown()
            
            out_file = output_path / f"{doc_path.stem}.md"
            with open(out_file, 'w') as f:
                f.write(md)
            
            return {'file': str(doc_path), 'status': 'success'}
        except Exception as e:
            return {'file': str(doc_path), 'status': 'error', 'error': str(e)}
    
    docs = list(input_path.glob('*.pdf')) + list(input_path.glob('*.docx'))
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_single, docs))
    
    return results
```

## 最佳实践

1. **选择合适的处理流程**：根据文档类型进行配置。
2. **处理大型文档**：如有需要，可分块处理。
3. **验证表格提取结果**：复杂表格可能需要人工审核。
4. **检查 OCR 质量**：对于扫描文档，启用 OCR 功能。
5. **缓存解析结果**：将解析后的文档存储起来以供后续使用。

## 常见应用场景

### 学术论文解析

```python
def parse_academic_paper(pdf_path):
    """Parse academic paper structure."""
    
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    doc = result.document
    
    paper = {
        'title': None,
        'abstract': None,
        'sections': [],
        'references': [],
        'tables': [],
        'figures': []
    }
    
    current_section = None
    
    for element in doc.iterate_items():
        text = element.text if hasattr(element, 'text') else ''
        
        if element.type == 'title':
            paper['title'] = text
        
        elif element.type == 'heading':
            if 'abstract' in text.lower():
                current_section = 'abstract'
            elif 'reference' in text.lower():
                current_section = 'references'
            else:
                paper['sections'].append({
                    'title': text,
                    'content': ''
                })
                current_section = 'section'
        
        elif element.type == 'paragraph':
            if current_section == 'abstract':
                paper['abstract'] = text
            elif current_section == 'section' and paper['sections']:
                paper['sections'][-1]['content'] += text + '\n'
        
        elif element.type == 'table':
            paper['tables'].append({
                'caption': element.caption if hasattr(element, 'caption') else None,
                'data': element.export_to_dataframe() if hasattr(element, 'export_to_dataframe') else None
            })
    
    return paper
```

### 报告转换为结构化数据

```python
def parse_business_report(doc_path):
    """Parse business report into structured format."""
    
    converter = DocumentConverter()
    result = converter.convert(doc_path)
    doc = result.document
    
    report = {
        'metadata': {
            'title': None,
            'date': None,
            'author': None
        },
        'executive_summary': None,
        'sections': [],
        'key_metrics': [],
        'recommendations': []
    }
    
    # Parse document structure
    for element in doc.iterate_items():
        # Implement parsing logic based on document structure
        pass
    
    return report
```

## 示例

### 示例 1：解析财务报告

```python
from docling.document_converter import DocumentConverter

def parse_financial_report(pdf_path):
    """Extract structured data from financial report."""
    
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    doc = result.document
    
    financial_data = {
        'income_statement': None,
        'balance_sheet': None,
        'cash_flow': None,
        'notes': []
    }
    
    # Extract tables
    tables = []
    for element in doc.iterate_items():
        if element.type == 'table':
            table_df = element.export_to_dataframe()
            
            # Identify table type
            if 'revenue' in str(table_df).lower() or 'income' in str(table_df).lower():
                financial_data['income_statement'] = table_df
            elif 'asset' in str(table_df).lower() or 'liabilities' in str(table_df).lower():
                financial_data['balance_sheet'] = table_df
            elif 'cash' in str(table_df).lower():
                financial_data['cash_flow'] = table_df
            else:
                tables.append(table_df)
    
    # Extract markdown for notes
    financial_data['markdown'] = doc.export_to_markdown()
    
    return financial_data

report = parse_financial_report('annual_report.pdf')
print("Income Statement:")
print(report['income_statement'])
```

### 示例 2：技术文档解析

```python
from docling.document_converter import DocumentConverter

def parse_technical_docs(doc_path):
    """Parse technical documentation."""
    
    converter = DocumentConverter()
    result = converter.convert(doc_path)
    doc = result.document
    
    documentation = {
        'title': None,
        'version': None,
        'sections': [],
        'code_blocks': [],
        'diagrams': []
    }
    
    current_section = None
    
    for element in doc.iterate_items():
        if element.type == 'title':
            documentation['title'] = element.text
        
        elif element.type == 'heading':
            current_section = {
                'title': element.text,
                'level': element.level if hasattr(element, 'level') else 1,
                'content': []
            }
            documentation['sections'].append(current_section)
        
        elif element.type == 'code':
            if current_section:
                current_section['content'].append({
                    'type': 'code',
                    'content': element.text
                })
            documentation['code_blocks'].append(element.text)
        
        elif element.type == 'picture':
            documentation['diagrams'].append({
                'page': element.prov[0].page_no if element.prov else None,
                'caption': element.caption if hasattr(element, 'caption') else None
            })
    
    return documentation

docs = parse_technical_docs('api_documentation.pdf')
print(f"Title: {docs['title']}")
print(f"Sections: {len(docs['sections'])}")
```

### 示例 3：合同内容分析

```python
from docling.document_converter import DocumentConverter

def analyze_contract(pdf_path):
    """Parse contract document for key clauses."""
    
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    doc = result.document
    
    contract = {
        'parties': [],
        'clauses': [],
        'dates': [],
        'amounts': [],
        'full_text': doc.export_to_text()
    }
    
    import re
    
    # Extract dates
    date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b'
    contract['dates'] = re.findall(date_pattern, contract['full_text'], re.IGNORECASE)
    
    # Extract monetary amounts
    amount_pattern = r'\$[\d,]+(?:\.\d{2})?|\b\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:USD|dollars)\b'
    contract['amounts'] = re.findall(amount_pattern, contract['full_text'], re.IGNORECASE)
    
    # Parse sections as clauses
    for element in doc.iterate_items():
        if element.type == 'heading':
            contract['clauses'].append({
                'title': element.text,
                'content': ''
            })
        elif element.type == 'paragraph' and contract['clauses']:
            contract['clauses'][-1]['content'] += element.text + '\n'
    
    return contract

contract_data = analyze_contract('agreement.pdf')
print(f"Key dates: {contract_data['dates']}")
print(f"Amounts: {contract_data['amounts']}")
```

## 限制因素

- 非常大的文档可能需要分块处理。
- 手写内容需要经过 OCR 预处理。
- 复杂的嵌套表格可能需要人工审核。
- 某些 PDF 格式（加密格式）可能不被支持。
- 为获得最佳性能，建议使用 GPU。

## 安装方法

```bash
pip install docling

# For full functionality
pip install docling[all]

# For OCR support
pip install docling[ocr]
```

## 资源

- [docling GitHub 仓库](https://github.com/DS4SD/docling)
- [官方文档](https://ds4sd.github.io/docling/)
- [IBM 研究博客](https://research.ibm.com/)