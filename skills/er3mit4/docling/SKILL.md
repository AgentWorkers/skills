---
name: docling
description: 使用带有 GPU 加速功能的 `docling` CLI 从网页、PDF 文件、文档（docx、pptx）以及图片中提取并解析内容。当需要从特定 URL 中提取结构清晰、格式整齐的文本时，应优先使用 `docling` 而非 `web_fetch`。若需搜索或发现网页内容，可以使用 Brave（`web_search`）。只有在拥有 URL 且需要解析其内容时，才应使用 `docling`。
version: 1.0.2
metadata:
  requires:
    bins: ["docling"]
---

# Docling - 文档与网页内容提取工具

这是一个命令行工具（CLI），用于将文档和网页解析为结构清晰、易于阅读的文本。该工具利用GPU加速技术进行光学字符识别（OCR）和机器学习（ML）处理。

## 先决条件

- 必须安装 `docling` 命令行工具（例如，通过 `pipx install docling`）。
- 如需使用GPU加速功能，需要配备支持CUDA驱动程序的NVIDIA GPU。

## 使用场景

- **从URL提取内容** → 使用 `docling`。
- **搜索信息** → 使用 `web_search`（Brave浏览器）。
- **解析PDF、DOCX、PPTX文件** → 使用 `docling`。
- **对图片进行OCR处理** → 使用 `docling`。

## 常用命令

### 将网页内容转换为Markdown格式（默认行为）
```bash
docling "<URL>" --from html --to md
```
输出结果：会在当前目录下生成一个`.md`文件（也可使用 `--output` 参数指定输出路径）。

### 将网页内容转换为纯文本格式
```bash
docling "<URL>" --from html --to text --output /tmp/docling_out
```

### 对PDF文件进行OCR处理
```bash
docling "/path/to/file.pdf" --ocr --device cuda --output /tmp/docling_out
```

## 主要选项

| 选项          | 值            | 说明                                      |
|----------------|-----------------------------|
| `--from`       | html, pdf, docx, pptx, image, md, csv, xlsx | 输入文件格式                         |
| `--to`       | md, text, json, yaml, html       | 输出文件格式                         |
| `--device`      | auto, cuda, cpu         | 加速方式（默认：auto）                         |
| `--output`     | path            | 输出目录（建议使用临时目录）                         |
| `--ocr`       | flag           | 是否对图片或扫描的PDF文件进行OCR处理                 |
| `--tables`     | flag           | 是否提取表格内容                         |

## 安全提示

⚠️ **除非您完全信任数据来源，否则请避免使用以下选项：**
- `--enable-remote-services`：可能会将数据发送到远程服务器。
- `--allow-external-plugins`：会加载第三方插件。
- 使用包含不可信数据的自定义 `--headers` 参数：可能导致请求被重定向。

## 工作流程

1. **提取网页内容**：执行 `docling "<URL>" --from html --to text --output /tmp/docling_out`。
2. 从指定的输出目录中读取处理后的文件。
3. 读取完成后，请清理输出目录。

## GPU加速支持

Docling支持通过CUDA（NVIDIA GPU）进行加速。请确认您的系统已安装并配置好CUDA驱动程序：
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

## 完整的命令行参考文档

有关所有选项的详细信息，请参阅 [references/cli-reference.md](references/cli-reference.md)。