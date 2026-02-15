---
name: data-extractor
description: 使用非结构化的、统一的文档处理方法，从任何文档格式中提取结构化数据。
author: claude-office-skills
version: "1.0"
tags: [extraction, unstructured, data, parsing, documents]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: unstructured
  url: https://github.com/Unstructured-IO/unstructured
  stars: 14k
---

# 数据提取技能

## 概述

该技能能够使用 **unstructured** 库从任何文档格式中提取结构化数据。**unstructured** 是一个统一的库，可用于处理 PDF、Word 文档、电子邮件、HTML 等多种格式的文件。无论输入格式如何，都能获得一致且结构化的输出结果。

## 使用方法

1. 提供需要处理的文档。
2. （可选）指定提取选项。
3. 该工具会提取包含元数据的结构化元素。

**示例提示：**
- “从这份 PDF 中提取所有文本和表格。”
- “解析这封电子邮件，获取邮件正文、附件和元数据。”
- “将这页 HTML 页面转换为结构化数据。”
- “从这些混合格式的文档中提取数据。”

## 领域知识

### unstructured 的基础知识

```python
from unstructured.partition.auto import partition

# Automatically detect and process any document
elements = partition("document.pdf")

# Access extracted elements
for element in elements:
    print(f"Type: {type(element).__name__}")
    print(f"Text: {element.text}")
    print(f"Metadata: {element.metadata}")
```

### 支持的格式

| 格式 | 功能 | 备注 |
|--------|----------|-------|
| PDF | `partition_pdf` | 支持原生 PDF 和扫描 PDF 格式 |
| Word | `partition_docx` | 完整提取 Word 文档的结构 |
| PowerPoint | `partition_pptx` | 提取 PowerPoint 幻灯片和备注 |
| Excel | `partition_xlsx` | 提取 Excel 工作表的数据 |
| 电子邮件 | `partition_email` | 提取邮件正文和附件 |
| HTML | `partition_html` | 保留 HTML 标签 |
| Markdown | `partition_md` | 保留 Markdown 的结构 |
| 纯文本 | `partition_text` | 基本文本解析 |
| 图片 | `partition_image` | 通过 OCR 技术提取图片中的文本 |

### 元数据类型

```python
from unstructured.documents.elements import (
    Title,
    NarrativeText,
    Text,
    ListItem,
    Table,
    Image,
    Header,
    Footer,
    PageBreak,
    Address,
    EmailAddress,
)

# Elements have consistent structure
element.text           # Raw text content
element.metadata       # Rich metadata
element.category       # Element type
element.id            # Unique identifier
```

### 自动分割功能

```python
from unstructured.partition.auto import partition

# Process any file type
elements = partition(
    filename="document.pdf",
    strategy="auto",          # or "fast", "hi_res", "ocr_only"
    include_metadata=True,
    include_page_breaks=True,
)

# Filter by type
titles = [e for e in elements if isinstance(e, Title)]
tables = [e for e in elements if isinstance(e, Table)]
```

### 特定格式的分割方法

```python
# PDF with options
from unstructured.partition.pdf import partition_pdf

elements = partition_pdf(
    filename="document.pdf",
    strategy="hi_res",              # High quality extraction
    infer_table_structure=True,     # Detect tables
    include_page_breaks=True,
    languages=["en"],               # OCR language
)

# Word documents
from unstructured.partition.docx import partition_docx

elements = partition_docx(
    filename="document.docx",
    include_metadata=True,
)

# HTML
from unstructured.partition.html import partition_html

elements = partition_html(
    filename="page.html",
    include_metadata=True,
)
```

### 处理表格数据

```python
from unstructured.partition.auto import partition

elements = partition("report.pdf", infer_table_structure=True)

# Extract tables
for element in elements:
    if element.category == "Table":
        print("Table found:")
        print(element.text)
        
        # Access structured table data
        if hasattr(element, 'metadata') and element.metadata.text_as_html:
            print("HTML:", element.metadata.text_as_html)
```

### 元数据访问

```python
from unstructured.partition.auto import partition

elements = partition("document.pdf")

for element in elements:
    meta = element.metadata
    
    # Common metadata fields
    print(f"Page: {meta.page_number}")
    print(f"Filename: {meta.filename}")
    print(f"Filetype: {meta.filetype}")
    print(f"Coordinates: {meta.coordinates}")
    print(f"Languages: {meta.languages}")
```

### 为 AI/RAG 应用进行数据分块

```python
from unstructured.partition.auto import partition
from unstructured.chunking.title import chunk_by_title
from unstructured.chunking.basic import chunk_elements

# Partition document
elements = partition("document.pdf")

# Chunk by title (semantic chunks)
chunks = chunk_by_title(
    elements,
    max_characters=1000,
    combine_text_under_n_chars=200,
)

# Or basic chunking
chunks = chunk_elements(
    elements,
    max_characters=500,
    overlap=50,
)

for chunk in chunks:
    print(f"Chunk ({len(chunk.text)} chars):")
    print(chunk.text[:100] + "...")
```

### 批量处理

```python
from unstructured.partition.auto import partition
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def process_document(file_path):
    """Process single document."""
    try:
        elements = partition(str(file_path))
        return {
            'file': str(file_path),
            'status': 'success',
            'elements': len(elements),
            'text': '\n\n'.join([e.text for e in elements])
        }
    except Exception as e:
        return {
            'file': str(file_path),
            'status': 'error',
            'error': str(e)
        }

def batch_process(input_dir, max_workers=4):
    """Process all documents in directory."""
    input_path = Path(input_dir)
    files = list(input_path.glob('*'))
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_document, files))
    
    return results
```

### 导出格式

```python
from unstructured.partition.auto import partition
from unstructured.staging.base import elements_to_json, elements_to_dicts

elements = partition("document.pdf")

# To JSON string
json_str = elements_to_json(elements)

# To list of dicts
dicts = elements_to_dicts(elements)

# To DataFrame
import pandas as pd
df = pd.DataFrame(dicts)
```

## 最佳实践

1. **谨慎选择策略**：选择“fast”模式以加快处理速度，或选择“hi_res”模式以提高提取准确性。
2. **启用表格检测**：对于包含表格的文档，启用此功能。
3. **指定语言**：对于非英文文档，指定相应的语言以获得更好的 OCR 效果。
4. **为 AI 应用进行数据分块**：使用语义分块技术来处理数据。
5. **处理错误**：某些格式可能无法成功提取数据，但系统会优雅地处理这些错误情况。

## 常见应用场景

- **将文档转换为 JSON 格式**  
- **解析电子邮件内容**  
- **构建文档语料库**  

## 示例

- **示例 1：研究论文数据提取**  
- **示例 2：发票数据提取**  
- **示例 3：文档语料库构建**  

## 限制因素

- 复杂的文档布局可能需要人工审核。
- OCR 的质量受图片质量影响。
- 大文件可能需要分块处理。
- 一些专有格式可能不被支持。
- 云处理服务可能有 API 使用频率限制。

## 安装方法

```bash
# Basic installation
pip install unstructured

# With all dependencies
pip install "unstructured[all-docs]"

# For PDF processing
pip install "unstructured[pdf]"

# For specific formats
pip install "unstructured[docx,pptx,xlsx]"
```

## 资源

- [unstructured GitHub 仓库](https://github.com/Unstructured-IO/unstructured)
- [官方文档](https://unstructured-io.github.io/unstructured/)
- [Unstructured API 文档](https://unstructured.io/api-key)