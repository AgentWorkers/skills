---
name: pdf_compressor
description: "将给定的 PDF 文件压缩以减小其大小。"
version: "1.0.0"
runtime: shell
entrypoint: "uv run src/main.py"

inputs:
  - name: pdf_path
    type: string
    description: "The absolute path to the PDF file to be compressed."
    required: true
  - name: compression_level
    type: integer
    description: "Compression level (1=Low, 2=Medium, 3=High). Defaults to 2."
    required: false
    default: 2

output:
  type: json
  description: "JSON object containing compression success status and data like the compressed file path, original size, and compressed size."
---
# PDF压缩技能

该技能旨在使用标准优化参数来压缩PDF文件，从而减小其体积。它基于PyMuPDF实现，并提供了三种可调节的压缩级别，以满足用户的不同需求。

## 使用指南
在使用该技能压缩PDF文件时，您需要提供`pdf_path`（目标PDF文件的绝对路径），以及可选的`compression_level`（范围为1到3）。该技能会返回新生成的压缩PDF文件的输出路径。

- **级别1（低）**：基础压缩，压缩速度最快。
- **级别2（中）**：优化压缩，兼顾压缩速度和文件大小缩减（默认级别）。
- **级别3（高）**：深度压缩，以实现最大的文件大小缩减。