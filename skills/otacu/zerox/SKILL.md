---
name: zerox
description: 使用 zerox 库将文档（PDF、DOCX、PPTX、图片等）转换为 Markdown 格式。当用户需要从文档文件中提取文本内容时，可以使用此方法。
homepage: https://github.com/getomni-ai/zerox
metadata: {"clawdbot":{"emoji":"📄","requires":{"bins":["node"],"env":["APIYI_API_KEY"]},"primaryEnv":"APIYI_API_KEY"}}
---

# Zerox 文档转换器

使用 zerox 库和 GPT-4o 视觉模型，将各种文档格式转换为 Markdown 格式。

## 支持的格式

- PDF（扫描文件和纯文本文件）
- Microsoft Word（DOCX）
- Microsoft PowerPoint（PPTX）
- 图片（PNG、JPG 等）
- 以及通过 OCR 转换的其他格式

## 背景转换（适用于大文件）

对于文件较小的情况（转换时间 < 30 秒）：

```bash
node {baseDir}/scripts/convert.mjs <filePath> [outputPath]
```

### 示例

```bash
# Convert PDF - saves to {baseDir}/output/document.md by default
node {baseDir}/scripts/convert.mjs "/path/to/document.pdf"

# Convert PDF with custom output path
node {baseDir}/scripts/convert.mjs "/path/to/document.pdf" "/path/to/output.md"

# Convert Word document - saves to {baseDir}/output/document.md
node {baseDir}/scripts/convert.mjs "/path/to/document.docx"
```

## 背景转换（适用于大文件或需要较长时间处理的扫描 PDF 文件）

对于文件较大或需要较长时间处理的扫描 PDF 文件：

```bash
node {baseDir}/scripts/convert-bg.mjs <filePath> [outputPath]
```

### 特点

- 在后台运行转换（无超时问题）
- 将转换进度记录到 `{baseDir}/output/convert-bg.log` 文件中
- 转换完成后会发送 macOS 通知
- 可安全地关闭终端程序

### 示例

```bash
# Convert large scanned PDF in background
node {baseDir}/scripts/convert-bg.mjs "/path/to/scanned-document.pdf"

# Monitor progress
tail -f {baseDir}/output/convert-bg.log
```

## 所需条件

- `APIYI_API_KEY`：您的 OpenAI 兼容 API 密钥（环境变量）

## 注意事项

- 转换过程使用 GPT-4o 视觉模型提取文本，因此即使是对扫描文档也能正常工作
- 大文件可能需要较长时间才能完成转换
- 输出结果为纯 Markdown 格式的文本