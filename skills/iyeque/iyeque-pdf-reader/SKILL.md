---
name: pdf-reader
description: 从PDF文件中提取文本、在其中进行搜索，并生成摘要。
homepage: "https://www.pymupdf.com"
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "requires": { "bins": ["python3"], "pip": ["PyMuPDF"] },
        "install":
          [
            {
              "id": "pymupdf",
              "kind": "pip",
              "package": "PyMuPDF",
              "label": "Install PyMuPDF",
            },
          ],
      },
  }
---

# PDF阅读器技能

`pdf-reader`技能提供了提取PDF文件中的文本、在PDF内进行搜索、生成文档摘要以及检索元数据的功能。

## 工具API

该技能提供了四个功能：

### extract_text
从指定的PDF文件中提取纯文本。

- **参数：**
  - `file_path` (string): 需要提取文本的PDF文件路径。
  - `max_pages` (integer, 可选): 最大提取页数。

```python
from pdfminer.high_level import extract_text

def extract_text_from_pdf(file_path: str, max_pages=None) -> str:
    """Extracts text from a PDF, up to max_pages."""
    return extract_text(file_path, maxpages=max_pages)
```

### search
在PDF文件中搜索特定的术语或短语。

- **参数：**
  - `file_path` (string): PDF文件的路径。
  - `query` (string): 需要在文档中搜索的术语或短语。

```python
from typing import List

def search_pdf(file_path: str, query: str) -> List[str]:
    """Searches for a term in the PDF and returns lines containing it."""
    pdf_text = extract_text_from_pdf(file_path)
    return [line.strip() for line in pdf_text.split("\n") if query.lower() in line.lower()]
```

### summarize
将文档分割成易于理解的片段，生成文档摘要。

- **参数：**
  - `file_path` (string): PDF文件的路径。

```python
from typing import List

def chunk_text(text: str, max_tokens=2000) -> List[str]:
    """Divides text into manageable chunks for processing."""
    words = text.split()
    max_word_count = max_tokens
    chunks = []
    current_chunk = []

    for word in words:
        if len(current_chunk) + len(word.split()) <= max_word_count:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def summarize_pdf(file_path: str) -> str:
    """Summarizes a PDF file by processing its text."""
    pdf_text = extract_text_from_pdf(file_path)
    chunks = chunk_text(pdf_text)
    summaries = [call_llm("Summarize this:", chunk) for chunk in chunks]
    return "\n".join(summaries)
```

### metadata
检索关于该文档的元数据。

- **参数：**
  - `file_path` (string): PDF文件的路径。

```python
from PyPDF2 import PdfReader

def get_pdf_metadata(file_path: str) -> dict:
    """Extracts metadata from a PDF file."""
    reader = PdfReader(file_path)
    metadata = reader.metadata
    return {
        "title": metadata.get("/Title", "Unknown"),
        "author": metadata.get("/Author", "Unknown"),
        "pages": len(reader.pages),
    }
```

## 测试
使用示例PDF文件来确保所有功能都能正常运行并输出准确的结果：

- 测试不同布局格式下的文本提取功能。
- 验证摘要是否涵盖了文档的关键内容。
- 确认搜索结果是否包含所有相关内容。

请确保摘要和搜索结果基于用户的特定输入，并符合用户的期望。