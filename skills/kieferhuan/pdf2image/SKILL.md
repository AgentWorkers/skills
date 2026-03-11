---
name: pdf-to-long-image
description: >
  将多页PDF文件转换为单个垂直的长图像，方法是将所有页面连接在一起。  
  适用于用户需要将PDF文件转换为长图像、将多个PDF页面合并成一张图片，或从PDF文档中生成可滚动的截图的情况。
---
# 将PDF文件转换为长图像

该工具可将多页PDF文件转换为单张垂直长图像，适用于分享文档（作为可滚动图像）或创建视觉摘要。

## 快速入门

```bash
# Basic usage
uv run python ~/.openclaw/skills/pdf-to-long-image/scripts/pdf_to_long_image.py input.pdf

# Specify output path
uv run python ~/.openclaw/skills/pdf-to-long-image/scripts/pdf_to_long_image.py input.pdf output.png

# Higher resolution
uv run python ~/.openclaw/skills/pdf-to-long-image/scripts/pdf_to_long_image.py input.pdf output.png --scale 3
```

## 工作原理

1. 使用pymupdf（基于fitz库）打开PDF文件。
2. 按指定比例（默认为2倍，以获得更清晰的图像）渲染每一页。
3. 将所有页面垂直拼接成一张图像。
4. 以优化后的PNG格式保存图像。

## 参数选项

| 参数 | 默认值 | 说明 |
|--------|---------|-------------|
| `input` | （必填） | PDF文件的路径 |
| `output` | `input_long.png` | 输出图像的路径 |
| `--scale` | 2.0 | 渲染比例因子（数值越大，图像细节越丰富） |

## 所需依赖库

该脚本需要以下依赖库（使用uv工具安装）：

```bash
uv pip install pymupdf pillow
```

## 示例输出

```
Converting 32 pages from document.pdf...
  Page 1/32: 1684x1190
  Page 2/32: 1684x1190
  ...
Done! Saved to: document_long.png
  Dimensions: 1684x38112 pixels
  File size: 11.23 MB
```

## 脚本位置

```
~/.openclaw/skills/pdf-to-long-image/scripts/pdf_to_long_image.py
```