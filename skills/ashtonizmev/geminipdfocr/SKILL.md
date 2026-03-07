---
name: PDF OCR using Gemini LLM
description: 使用 Google Gemini OCR 从 PDF 文件中提取文本。适用于从 PDF 文件中提取文本、对扫描的文档进行 OCR 处理，或处理基于图像的 PDF 文件。
metadata:
  openclaw:
    requires:
      env:
        - GOOGLE_API_KEY
    primaryEnv: GOOGLE_API_KEY
    install:
      - kind: uv
        package: google-genai
        label: "Python deps"
      - kind: uv
        package: pymupdf
      - kind: uv
        package: pydantic
      - kind: uv
        package: pydantic-settings
---
## 使用目的

使用 `geminipdfocr` 通过 OCR（Google Gemini）技术从 PDF 文档中提取文本。

## 数据与隐私

**完整的页面图像/文件会被发送到 Google 的 API。** PDF 文件会被分割成单页文件，每页都会上传到 Google Gemini 进行 OCR 处理。该工具没有隐藏的数据提取端点或其他数据收集行为。请勿对高度敏感的文档使用此工具，除非您同意其内容会被发送到 Google。**

## 设置（虚拟环境安装）

首次使用前，请创建并激活虚拟环境：

```bash
cd geminipdfocr && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

在运行程序之前，请将 `GOOGLE_API_KEY` 设置在环境变量中（例如：`export GOOGLE_API_KEY=your-key`）。

## 使用方法

当需要从 PDF 文件中提取文本或进行 OCR 处理时，请执行以下命令：

1. 运行：`cd geminipdfocr && source venv/bin/activate && python -m geminipdfocr <path-to-pdf> [--json] [--output <file>]`
2. 使用 `--json` 选项可获取结构化数据。
3. 使用 `--max-pages N` 选项可限制处理的页面数量（适用于较长的文档）。
4. 使用 `--quiet` 选项可抑制进度日志的输出。

## 系统要求

- 需要一个有效的 PDF 文件路径。
- 确保 `GOOGLE_API_KEY` 已在系统环境变量中设置（例如：`export GOOGLE_API_KEY=your-key`）。

## 命令行选项

| 选项          | 描述                                      |
|---------------|-------------------------------------------|
| `pdf_path`       | 一个或多个 PDF 文件路径                            |
| `--max-pages N`     | 限制每份 PDF 文件处理的页面数量                   |
| `--json`        | 以结构化 JSON 格式输出结果                        |
| `--output FILE`     | 将结果写入指定文件（默认为标准输出）                     |
| `--quiet`       | 抑制 INFO/DEBUG 级别的日志输出                    |