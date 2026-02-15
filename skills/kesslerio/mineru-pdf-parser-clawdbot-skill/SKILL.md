---
name: mineru-pdf
description: 使用 MinerU 在本地（CPU 上）将 PDF 文件解析为 Markdown 或 JSON 格式。MinerU 会为每个文档创建单独的输出文件夹，并支持提取表格和图片内容。
---

# MinerU PDF

## 概述
使用 MinerU（基于 CPU 的工具）在本地解析 PDF 文件。默认输出格式为 Markdown 和 JSON；仅在需要时才会包含表格和图片。

## 快速入门（单份 PDF 文件）
```bash
# Run from the skill directory
./scripts/mineru_parse.sh /path/to/file.pdf
```

可选示例：
```bash
./scripts/mineru_parse.sh /path/to/file.pdf --format json
./scripts/mineru_parse.sh /path/to/file.pdf --tables --images
```

## 何时查阅参考资料
如果使用的参数与您的工具包设置不同，或者您需要更高级的配置选项（如后端、方法、设备、线程或格式映射），请参考：
- `references/mineru-cli.md`

## 输出规范
- 默认输出目录为 `./mineru-output/`。
- MinerU 会在输出目录下为每个解析的 PDF 文件创建一个子文件夹（例如：`./mineru-output/<文件名>/...`）。

## 批量处理
默认情况下，MinerU 仅支持单份 PDF 文件的解析。如需批量处理多个 PDF 文件，请确保已正确配置相关功能。