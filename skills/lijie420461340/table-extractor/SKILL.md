---
name: table-extractor
description: 使用 camelot 从 PDF 文件中高精度地提取表格内容——能够处理复杂的表格结构
author: claude-office-skills
version: "1.0"
tags: [table, extraction, camelot, pdf, data]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: camelot-py
  url: https://github.com/camelot-dev/camelot
  stars: 4.2k
---

# 表格提取技能

## 概述

该技能利用 **camelot**（PDF表格提取领域的黄金标准工具）实现从PDF文档中精确提取表格的功能。能够高效处理包含合并单元格、无边框表格以及多页布局的复杂表格。

## 使用方法

1. 提供包含表格的PDF文件。
2. （可选）指定需要提取的页面或表格检测方法。
3. 表格将被提取为pandas DataFrame格式的数据结构。

**示例提示：**
- “从该PDF文件中提取所有表格。”
- “获取报告第5页的表格。”
- “从该文档中提取无边框的表格。”
- “将PDF表格转换为Excel格式。”

## 相关领域知识

### camelot基础知识
```python
import camelot

# Extract tables from PDF
tables = camelot.read_pdf('document.pdf')

# Access results
print(f"Found {len(tables)} tables")

# Get first table as DataFrame
df = tables[0].df
print(df)
```

### 提取方法

| 方法          | 适用场景            | 描述                                      |
|--------------|------------------|-----------------------------------------|
| `lattice`      | 有边框的表格          | 通过线条/边框来检测表格                          |
| `stream`       | 无边框的表格          | 利用文本位置信息进行检测                          |

```python
# Lattice method (default) - for tables with visible borders
tables = camelot.read_pdf('document.pdf', flavor='lattice')

# Stream method - for borderless tables
tables = camelot.read_pdf('document.pdf', flavor='stream')
```

### 页面选择
```python
# Single page
tables = camelot.read_pdf('document.pdf', pages='1')

# Multiple pages
tables = camelot.read_pdf('document.pdf', pages='1,3,5')

# Page range
tables = camelot.read_pdf('document.pdf', pages='1-5')

# All pages
tables = camelot.read_pdf('document.pdf', pages='all')
```

### 高级选项

#### Lattice选项
```python
tables = camelot.read_pdf(
    'document.pdf',
    flavor='lattice',
    line_scale=40,              # Line detection sensitivity
    copy_text=['h', 'v'],       # Copy text across merged cells
    shift_text=['l', 't'],      # Shift text alignment
    split_text=True,            # Split text at newlines
    flag_size=True,             # Flag super/subscripts
    strip_text='\n',            # Characters to strip
    process_background=False,   # Process background lines
)
```

#### Stream选项
```python
tables = camelot.read_pdf(
    'document.pdf',
    flavor='stream',
    edge_tol=500,               # Edge tolerance
    row_tol=10,                 # Row tolerance
    column_tol=0,               # Column tolerance
    strip_text='\n',            # Characters to strip
)
```

### 表格区域指定
```python
# Extract from specific area (x1, y1, x2, y2)
# Coordinates from bottom-left, in PDF points (72 points = 1 inch)
tables = camelot.read_pdf(
    'document.pdf',
    table_areas=['72,720,540,400'],  # One area
)

# Multiple areas
tables = camelot.read_pdf(
    'document.pdf',
    table_areas=['72,720,540,400', '72,380,540,200'],
)
```

### 列指定
```python
# Manually specify column positions (for stream method)
tables = camelot.read_pdf(
    'document.pdf',
    flavor='stream',
    columns=['100,200,300,400'],  # X positions of column separators
)
```

### 结果处理
```python
import camelot

tables = camelot.read_pdf('document.pdf')

for i, table in enumerate(tables):
    # Access DataFrame
    df = table.df
    
    # Table metadata
    print(f"Table {i+1}:")
    print(f"  Page: {table.page}")
    print(f"  Accuracy: {table.accuracy}")
    print(f"  Whitespace: {table.whitespace}")
    print(f"  Order: {table.order}")
    print(f"  Shape: {df.shape}")
    
    # Parsing report
    report = table.parsing_report
    print(f"  Report: {report}")
```

### 导出选项
```python
import camelot

tables = camelot.read_pdf('document.pdf')

# Export to CSV
tables[0].to_csv('table.csv')

# Export to Excel
tables[0].to_excel('table.xlsx')

# Export to JSON
tables[0].to_json('table.json')

# Export to HTML
tables[0].to_html('table.html')

# Export all tables
for i, table in enumerate(tables):
    table.to_excel(f'table_{i+1}.xlsx')
```

### 可视化调试
```python
import camelot

# Enable visual debugging
tables = camelot.read_pdf('document.pdf')

# Plot detected table areas
camelot.plot(tables[0], kind='contour').show()

# Plot text on table
camelot.plot(tables[0], kind='text').show()

# Plot detected lines (lattice only)
camelot.plot(tables[0], kind='joint').show()
camelot.plot(tables[0], kind='line').show()

# Save plot
fig = camelot.plot(tables[0])
fig.savefig('debug.png')
```

### 处理多页表格
```python
import camelot
import pandas as pd

def extract_multipage_table(pdf_path, pages='all'):
    """Extract and combine tables that span multiple pages."""
    
    tables = camelot.read_pdf(pdf_path, pages=pages)
    
    # Group tables by similar structure (columns)
    table_groups = {}
    
    for table in tables:
        cols = tuple(table.df.columns)
        if cols not in table_groups:
            table_groups[cols] = []
        table_groups[cols].append(table.df)
    
    # Combine similar tables
    combined = []
    for cols, dfs in table_groups.items():
        if len(dfs) > 1:
            # Combine and deduplicate header rows
            combined_df = pd.concat(dfs, ignore_index=True)
            combined.append(combined_df)
        else:
            combined.append(dfs[0])
    
    return combined
```

## 最佳实践

1. **两种方法结合使用**：对于有边框的表格使用`lattice`方法，对于无边框的表格使用`stream`方法。
2. **检查准确率**：准确率在90%以上通常表示提取效果良好。
3. **使用可视化调试工具**：帮助理解提取结果。
4. **指定提取区域**：对于包含多种表格类型的PDF文件，需要明确指定提取范围。
5. **处理表头**：表格的第一行通常需要特殊处理。

## 常见应用场景

### 批量提取表格
```python
import camelot
from pathlib import Path
import pandas as pd

def batch_extract_tables(input_dir, output_dir):
    """Extract tables from all PDFs in directory."""
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    results = []
    
    for pdf_file in input_path.glob('*.pdf'):
        try:
            tables = camelot.read_pdf(str(pdf_file), pages='all')
            
            for i, table in enumerate(tables):
                # Skip low accuracy tables
                if table.accuracy < 80:
                    continue
                
                output_file = output_path / f"{pdf_file.stem}_table_{i+1}.xlsx"
                table.to_excel(str(output_file))
                
                results.append({
                    'source': str(pdf_file),
                    'table': i + 1,
                    'page': table.page,
                    'accuracy': table.accuracy,
                    'output': str(output_file)
                })
        
        except Exception as e:
            results.append({
                'source': str(pdf_file),
                'error': str(e)
            })
    
    return results
```

### 自动检测表格方法
```python
import camelot

def smart_extract_tables(pdf_path, pages='1'):
    """Try both methods and return best results."""
    
    # Try lattice first
    lattice_tables = camelot.read_pdf(pdf_path, pages=pages, flavor='lattice')
    
    # Try stream
    stream_tables = camelot.read_pdf(pdf_path, pages=pages, flavor='stream')
    
    # Compare and return best
    results = []
    
    if lattice_tables and lattice_tables[0].accuracy > 70:
        results.extend(lattice_tables)
    elif stream_tables:
        results.extend(stream_tables)
    
    return results
```

## 示例

### 示例1：财务报表提取
```python
import camelot
import pandas as pd

def extract_financial_tables(pdf_path):
    """Extract financial tables from annual report."""
    
    # Extract all tables
    tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice')
    
    financial_data = {
        'income_statement': None,
        'balance_sheet': None,
        'cash_flow': None,
        'other_tables': []
    }
    
    for table in tables:
        df = table.df
        text = df.to_string().lower()
        
        # Identify table type
        if 'revenue' in text or 'sales' in text:
            if 'operating income' in text or 'net income' in text:
                financial_data['income_statement'] = df
        elif 'asset' in text and 'liabilities' in text:
            financial_data['balance_sheet'] = df
        elif 'cash flow' in text or 'operating activities' in text:
            financial_data['cash_flow'] = df
        else:
            financial_data['other_tables'].append({
                'page': table.page,
                'data': df,
                'accuracy': table.accuracy
            })
    
    return financial_data

financials = extract_financial_tables('annual_report.pdf')
if financials['income_statement'] is not None:
    print("Income Statement found:")
    print(financials['income_statement'])
```

### 示例2：科学数据提取
```python
import camelot
import pandas as pd

def extract_research_data(pdf_path, pages='all'):
    """Extract data tables from research paper."""
    
    # Try lattice for bordered tables
    tables = camelot.read_pdf(pdf_path, pages=pages, flavor='lattice')
    
    if not tables or all(t.accuracy < 70 for t in tables):
        # Fall back to stream for borderless
        tables = camelot.read_pdf(pdf_path, pages=pages, flavor='stream')
    
    extracted_data = []
    
    for table in tables:
        df = table.df
        
        # Clean up the DataFrame
        # Set first row as header if it looks like one
        if not df.iloc[0].str.contains(r'\d').any():
            df.columns = df.iloc[0]
            df = df[1:]
            df = df.reset_index(drop=True)
        
        extracted_data.append({
            'page': table.page,
            'accuracy': table.accuracy,
            'data': df
        })
    
    return extracted_data

data = extract_research_data('research_paper.pdf')
for i, item in enumerate(data):
    print(f"Table {i+1} (Page {item['page']}, Accuracy: {item['accuracy']}%):")
    print(item['data'].head())
```

### 示例3：发票明细项提取
```python
import camelot

def extract_invoice_items(pdf_path):
    """Extract line items from invoice."""
    
    # Usually invoices have bordered tables
    tables = camelot.read_pdf(pdf_path, flavor='lattice')
    
    line_items = []
    
    for table in tables:
        df = table.df
        
        # Look for table with typical invoice columns
        header_text = ' '.join(df.iloc[0].astype(str)).lower()
        
        if any(term in header_text for term in ['quantity', 'qty', 'amount', 'price', 'description']):
            # This looks like a line items table
            df.columns = df.iloc[0]
            df = df[1:]
            
            for _, row in df.iterrows():
                item = {}
                for col in df.columns:
                    col_lower = str(col).lower()
                    value = row[col]
                    
                    if 'desc' in col_lower or 'item' in col_lower:
                        item['description'] = value
                    elif 'qty' in col_lower or 'quantity' in col_lower:
                        item['quantity'] = value
                    elif 'price' in col_lower or 'rate' in col_lower:
                        item['unit_price'] = value
                    elif 'amount' in col_lower or 'total' in col_lower:
                        item['amount'] = value
                
                if item:
                    line_items.append(item)
    
    return line_items

items = extract_invoice_items('invoice.pdf')
for item in items:
    print(item)
```

### 示例4：表格对比
```python
import camelot
import pandas as pd

def compare_pdf_tables(pdf1_path, pdf2_path):
    """Compare tables between two PDF versions."""
    
    tables1 = camelot.read_pdf(pdf1_path)
    tables2 = camelot.read_pdf(pdf2_path)
    
    comparisons = []
    
    # Match tables by shape and position
    for t1 in tables1:
        best_match = None
        best_score = 0
        
        for t2 in tables2:
            if t1.df.shape == t2.df.shape:
                # Calculate similarity
                try:
                    similarity = (t1.df == t2.df).mean().mean()
                    if similarity > best_score:
                        best_score = similarity
                        best_match = t2
                except:
                    pass
        
        if best_match:
            comparisons.append({
                'page1': t1.page,
                'page2': best_match.page,
                'similarity': best_score,
                'identical': best_score == 1.0,
                'diff': pd.DataFrame(t1.df != best_match.df)
            })
    
    return comparisons

comparison = compare_pdf_tables('report_v1.pdf', 'report_v2.pdf')
```

## 注意事项

- 不支持加密的PDF文件。
- 基于图像的PDF文件需要先进行OCR预处理。
- 非常复杂的合并单元格可能需要调整提取参数。
- 旋转的表格需要预先处理。
- 大型PDF文件可能需要分页处理。

## 安装方法
```bash
pip install camelot-py[cv]

# Additional dependencies
# macOS
brew install ghostscript tcl-tk

# Ubuntu
apt-get install ghostscript python3-tk
```

## 参考资源

- [camelot官方文档](https://camelot-py.readthedocs.io/)
- [GitHub仓库](https://github.com/camelot-dev/camelot)
- [与其他工具的对比](https://camelot-py.readthedocs.io/en/master/user/intro.html#why-camelot)