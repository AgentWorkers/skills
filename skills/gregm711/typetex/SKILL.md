---
name: Typst & LaTeX Compiler
description: 通过API将Typst和LaTeX文档编译为PDF格式。提交源代码后，会收到生成的PDF文件。
metadata:
  clawdbot:
    config:
      requiredEnv: []
      stateDirs: []
---

# Typst 和 LaTeX 编译器

使用 TypeTex 编译 API 将 Typst (.typ) 和 LaTeX (.tex) 文档编译为 PDF 格式。

## API 端点

**基础 URL:** `https://studio-intrinsic--typetex-compile-app.modal.run`

## 端点

### 编译 Typst 文档

```
POST /public/compile/typst
Content-Type: application/json
```

**请求体:**
```json
{
  "content": "#set page(paper: \"a4\")\n\n= Hello World\n\nThis is a Typst document.",
  "main_filename": "main.typ",
  "auxiliary_files": {}
}
```

**成功响应:**
```json
{
  "success": true,
  "pdf_base64": "JVBERi0xLjQK..."
}
```

**失败响应:**
```json
{
  "success": false,
  "error": "error: file not found: missing.typ"
}
```

### 编译 LaTeX 文档

```
POST /public/compile/latex
Content-Type: application/json
```

**请求体:**
```json
{
  "content": "\\documentclass{article}\n\\begin{document}\nHello World\n\\end{document}",
  "main_filename": "main.tex",
  "auxiliary_files": {}
}
```

**成功响应:**
```json
{
  "success": true,
  "pdf_base64": "JVBERi0xLjQK..."
}
```

**失败响应:**
```json
{
  "success": false,
  "error": "! LaTeX Error: Missing \\begin{document}.",
  "log_output": "This is pdfTeX..."
}
```

### 健康检查

```
GET /public/compile/health
```

如果服务正在运行，将返回 `{"status": "ok", "service": "public-compile"}`。

## 使用示例

### 简单的 Typst 文档

```python
import requests
import base64

response = requests.post(
    "https://studio-intrinsic--typetex-compile-app.modal.run/public/compile/typst",
    json={
        "content": """
#set page(paper: "a4", margin: 2cm)
#set text(font: "New Computer Modern", size: 11pt)

= My Document

This is a paragraph with *bold* and _italic_ text.

== Section 1

- Item 1
- Item 2
- Item 3
""",
        "main_filename": "main.typ"
    }
)

result = response.json()
if result["success"]:
    pdf_bytes = base64.b64decode(result["pdf_base64"])
    with open("output.pdf", "wb") as f:
        f.write(pdf_bytes)
    print("PDF saved to output.pdf")
else:
    print(f"Compilation failed: {result['error']}")
```

### 简单的 LaTeX 文档

```python
import requests
import base64

response = requests.post(
    "https://studio-intrinsic--typetex-compile-app.modal.run/public/compile/latex",
    json={
        "content": r"""
\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath}

\title{My Document}
\author{Author Name}

\begin{document}
\maketitle

\section{Introduction}

This is a LaTeX document with math: $E = mc^2$

\end{document}
""",
        "main_filename": "main.tex"
    }
)

result = response.json()
if result["success"]:
    pdf_bytes = base64.b64decode(result["pdf_base64"])
    with open("output.pdf", "wb") as f:
        f.write(pdf_bytes)
else:
    print(f"Compilation failed: {result['error']}")
    if result.get("log_output"):
        print(f"Log: {result['log_output']}")
```

### 多文件项目（Typst）

```python
import requests
import base64

response = requests.post(
    "https://studio-intrinsic--typetex-compile-app.modal.run/public/compile/typst",
    json={
        "content": """
#import "template.typ": *

#show: project.with(title: "My Report")

= Introduction

#include "chapter1.typ"
""",
        "main_filename": "main.typ",
        "auxiliary_files": {
            "template.typ": """
#let project(title: none, body) = {
  set page(paper: "a4")
  set text(font: "New Computer Modern")

  align(center)[
    #text(size: 24pt, weight: "bold")[#title]
  ]

  body
}
""",
            "chapter1.typ": """
== Chapter 1

This is the first chapter.
"""
        }
    }
)

result = response.json()
if result["success"]:
    pdf_bytes = base64.b64decode(result["pdf_base64"])
    with open("report.pdf", "wb") as f:
        f.write(pdf_bytes)
```

### 包含图片

对于图片等二进制文件，需要使用 base64 对其进行编码：

```python
import requests
import base64

# Read and encode an image
with open("figure.png", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode("utf-8")

response = requests.post(
    "https://studio-intrinsic--typetex-compile-app.modal.run/public/compile/typst",
    json={
        "content": """
#set page(paper: "a4")

= Document with Image

#figure(
  image("figure.png", width: 80%),
  caption: [A sample figure]
)
""",
        "main_filename": "main.typ",
        "auxiliary_files": {
            "figure.png": image_base64
        }
    }
)
```

### 使用 curl 进行请求

```bash
# Typst compilation
curl -X POST https://studio-intrinsic--typetex-compile-app.modal.run/public/compile/typst \
  -H "Content-Type: application/json" \
  -d '{
    "content": "#set page(paper: \"a4\")\n\n= Hello World\n\nThis is Typst.",
    "main_filename": "main.typ"
  }' | jq -r '.pdf_base64' | base64 -d > output.pdf

# LaTeX compilation
curl -X POST https://studio-intrinsic--typetex-compile-app.modal.run/public/compile/latex \
  -H "Content-Type: application/json" \
  -d '{
    "content": "\\documentclass{article}\n\\begin{document}\nHello World\n\\end{document}",
    "main_filename": "main.tex"
  }' | jq -r '.pdf_base64' | base64 -d > output.pdf
```

## 支持的功能

### Typst
- 完整的 Typst 语言支持
- 支持包含多个文件的项目
- 支持图片（PNG、JPG、SVG 格式）
- 自定义字体（如 New Computer Modern）
- 数学公式
- 表格和图表
- 参考文献（使用 Hayagriva 格式）

### LaTeX
- 通过 Tectonic 提供完整的 TeX Live 分发环境
- 支持多文件项目（使用 `\input` 和 `\include` 指令）
- 支持 BibTeX/BibLaTeX 格式的参考文献
- 自定义样式文件（.sty、.cls）
- 所有标准包（如 amsmath、graphicx 等）
- TikZ/PGFPlots 图形格式
- 支持图片（PNG、JPG、PDF、EPS 格式）

## 错误处理

编译失败时，响应中会包含以下信息：
- `success: false`
- `error`: 便于人类阅读的错误信息
- `log_output`（仅限 LaTeX）：完整的编译日志，用于调试

常见错误：
- **语法错误**：请检查源代码中的拼写错误
- **文件缺失**：确保所有导入的文件都在 `auxiliary_files` 目录中
- **找不到包**：大多数常用包都已包含在内；如需添加其他包，请联系支持团队
- **超时**：复杂文档可能在 60 秒后超时

## 限制

- 无需身份验证
- 请合理使用共享资源
- 如需大量使用，请联系支持团队

## 代理使用建议

1. 在访问 `pdf_base64` 之前，请务必检查 `success` 值
2. 解析错误信息，以便向用户提供有用的反馈
- 测试时使用简单的文档——复杂文档的编译时间较长
- 如果多次编译相同内容，请缓存结果
- 对于多文件项目，请确保所有依赖项都包含在 `auxiliary_files` 目录中

## 相关资源

- [Typst 文档](https://typst.app/docs/)
- [LaTeX 维基教科书](https://en.wikibooks.org/wiki/LaTeX)
- [TypeTex](https://typetex.app)：具备人工智能辅助功能的完整文档编辑器