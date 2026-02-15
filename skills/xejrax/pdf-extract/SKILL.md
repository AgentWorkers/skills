---
name: pdf-extract
description: "从 PDF 文件中提取文本以供大型语言模型（LLM）处理"
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "requires": { "bins": ["pdftotext"] },
        "install":
          [
            {
              "id": "dnf",
              "kind": "dnf",
              "package": "poppler-utils",
              "bins": ["pdftotext"],
              "label": "Install via dnf",
            },
          ],
      },
  }
---

# PDF提取

从PDF文件中提取文本以供大型语言模型（LLM）处理。使用`poppler-utils`包中的`pdftotext`工具将PDF文档转换为纯文本。

## 命令

```bash
# Extract all text from a PDF
pdf-extract "document.pdf"

# Extract text from specific pages
pdf-extract "document.pdf" --pages 1-5
```

## 安装

```bash
sudo dnf install poppler-utils
```