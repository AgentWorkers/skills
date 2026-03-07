---
name: PDF OCR using Gemini LLM
description: 使用 Google Gemini OCR 从 PDF 文件中提取文本。适用于从 PDF 文件中提取文本、对扫描文档进行 OCR 处理或处理基于图像的 PDF 文件的场景。
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

使用 `geminipdfocr` 通过 OCR（Google Gemini）从 PDF 文档中提取文本。

## 数据与隐私

PDF 页面会被分割并上传到 Google Gemini 进行 OCR 处理。请勿对高度敏感的文档使用该工具，除非您同意其内容会被发送到 Google 的 API。

## 设置（虚拟环境安装）

在首次使用之前，请创建并激活虚拟环境：

```bash
cd geminipdfocr && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

在运行程序之前，请在环境变量中设置 `GOOGLE_API_KEY`（例如：`export GOOGLE_API_KEY=your-key`）。

## 使用方法

当需要从 PDF 文件中提取文本或进行 OCR 处理时，请执行以下命令：

1. 进入项目目录：`cd geminipdfocr`
2. 激活虚拟环境：`source venv/bin/activate`
3. 运行脚本：`python -m geminipdfocr <path-to-pdf> [--json] [--output <file>]`

- `--json` 选项用于生成结构化数据。
- `--max-pages N` 选项用于限制处理的 PDF 页面数量（适用于测试或非常长的文档）。
- `--quiet` 选项用于抑制进度日志的输出。

## 系统要求

- 需要一个有效的 PDF 文件路径。
- 确保 `GOOGLE_API_KEY` 已在系统环境变量中设置（例如：`export GOOGLE_API_KEY=your-key`）。

## 命令行选项

| 选项 | 描述 |
|--------|-------------|
| `pdf_path` | 一个或多个 PDF 文件路径（作为参数传递） |
| `--max-pages N` | 限制每份 PDF 文件处理的页面数量 |
| `--json` | 生成结构化 JSON 数据而非纯文本 |
| `--output FILE` | 将处理结果写入指定文件（默认输出到标准输出） |
| `--quiet` | 抑制 INFO/DEBUG 日志的输出 |