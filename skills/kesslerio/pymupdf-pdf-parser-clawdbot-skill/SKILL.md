---
name: pymupdf-pdf
description: 使用 PyMuPDF (fitz) 进行快速的本地 PDF 解析，支持生成 Markdown/JSON 格式的输出结果，并可添加图片或表格。适用于对解析速度要求较高、而对解析稳定性要求不高的场景；或者在更复杂的 PDF 解析器不可用时作为备用方案。默认情况下，程序会逐个文件进行 PDF 解析，并将解析结果保存在相应的文件夹中。
---

# PyMuPDF PDF

## 概述
使用 PyMuPDF 在本地解析 PDF 文件，支持将内容快速、便捷地提取为 Markdown 格式。默认情况下，提取结果会以 Markdown 格式输出；同时也可以选择将图像和表格数据以 JSON 或表格格式保存到每个文档对应的目录中。

## 先决条件 / 参考资料
如果遇到导入错误（PyMuPDF 未安装）或 Nix 系统中的 `libstdc++` 相关问题，请参阅：
- `references/pymupdf-notes.md`

## 快速入门（处理单个 PDF 文件）
```bash
# Run from the skill directory
./scripts/pymupdf_parse.py /path/to/file.pdf \
  --format md \
  --outroot ./pymupdf-output
```

## 参数选项
- `--format md|json|both` （默认值：`md`）：指定输出格式（Markdown 或 JSON）
- `--images`：提取 PDF 中的图像
- `--tables`：提取 PDF 中的表格数据（以简单的 JSON 格式输出）
- `--outroot DIR`：指定输出文件的根目录
- `--lang`：在 JSON 输出元数据中添加语言信息

## 输出格式规范
- 默认情况下，输出文件结构如下：
  - `./pymupdf-output/<pdf-basename>/`
    - Markdown 输出文件：`output.md`
    - JSON 输出文件：`output.json`（包含语言信息）
    - 图像文件：`images/`
    - 表格数据文件：`tables.json`（以简单的 JSON 格式保存）

## 注意事项
- PyMuPDF 解析速度较快，但在处理复杂 PDF 文件时稳定性较低。
- 如果需要更强大的解析能力，可以尝试使用专业的 OCR 解析工具（例如 MinerU，如果已安装的话）。