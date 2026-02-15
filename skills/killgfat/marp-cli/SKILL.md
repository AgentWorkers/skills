---
name: marp-cli
description: 通过命令行界面（CLI）将 Markdown 文件转换为演示文稿。支持输出格式包括 HTML、PDF、PowerPoint（PPTX）以及图片（PNG/JPEG）。
homepage: https://github.com/marp-team/marp-cli
metadata:
  {
    "openclaw":
      {
        "emoji": "📽️",
        "requires": { "anyBins": ["marp"] },
      },
  }
---

# Marp CLI

Marp CLI 是一个命令行工具，用于将 Markdown 文档转换为多种格式的演示文稿（HTML、PDF、PowerPoint（PPTX）和图片（PNG/JPEG）。

**浏览器要求：** 标有 🌐 的转换功能需要您的系统上安装了兼容的浏览器（Chrome、Edge 或 Firefox）。

## 快速入门

```bash
# Convert to HTML
marp slide-deck.md

# Convert to PDF (requires browser)
marp --pdf slide-deck.md

# Convert to PowerPoint
marp --pptx slide-deck.md

# Convert to images
marp --images png slide-deck.md
```

📖 **详细指南：** [QUICKSTART.md](QUICKSTART.md)

## 格式转换

### HTML
```bash
marp slide-deck.md
marp slide-deck.md -o output.html
```

### PDF 🌐
```bash
marp --pdf slide-deck.md
marp slide-deck.md -o output.pdf

# With PDF outlines
marp --pdf --pdf-outlines slide-deck.md

# Includes presenter notes as annotations on lower-left
marp --pdf --pdf-notes slide-deck.md
```

### PowerPoint (PPTX) 🌐
```bash
marp --pptx slide-deck.md
marp slide-deck.md -o output.pptx

# Editable PPTX (experimental, requires LibreOffice Impress)
marp --pptx --pptx-editable slide-deck.md
```

### 图片 🌐
```bash
# Multiple images
marp --images png slide-deck.md
marp --images jpeg slide-deck.md

# Title slide image only
marp --image png slide-deck.md
marp slide-deck.md -o output.png

# High resolution (scale factor)
marp slide-deck.md -o title.png --image-scale 2
```

### 演示者备注
```bash
marp --notes slide-deck.md
marp slide-deck.md -o output.txt
```

## 观看模式

```bash
# Watch file and auto-convert on changes
marp -w slide-deck.md

# Watch with browser preview
marp -w -p slide-deck.md
```

## 服务器模式

```bash
# Serve directory with on-demand conversion
marp -s ./slides

# Specify port via environment
PORT=5000 marp -s ./slides

# Access converted formats via query strings
# http://localhost:8080/deck.md?pdf
# http://localhost:8080/deck.md?pptx
```

## 预览窗口

```bash
# Open preview window (automatically enables watch mode)
marp -p slide-deck.md

# Preview with PDF output
marp -p --pdf slide-deck.md
```

## 多个文件

```bash
# Convert multiple files
marp slide1.md slide2.md slide3.md

# Convert directory
marp ./slides/

# Use glob patterns
marp **/*.md

# Convert with parallelism (default: 5 concurrent)
marp -P 10 ./*.md

# Disable parallelism
marp --no-parallel ./*.md
```

## 选项

| 选项 | 描述 |
|--------|-------------|
| `-o, --output <路径>` | 输出文件路径 |
| `-w, --watch` | 观看模式 - 文件更改时自动转换 |
| `-s, --server <目录>` | 服务器模式 - 提供目录访问服务 |
| `-p, --preview` | 打开预览窗口 |
| `--pdf` | 转换为 PDF 格式（需要 Chrome/Edge/Firefox） |
| `--pptx` | 转换为 PowerPoint PPTX 格式（需要浏览器） |
| `--pptx-editable` | 生成可编辑的 PPTX 文件（实验性功能） |
| `--images [png\|jpeg]` | 将所有页面转换为图片 |
| `--image` | 将标题页转换为单独的图片 |
| `--image-scale <缩放因子>` | 图片的缩放比例 |
| `--notes` | 将演示者备注导出为 TXT 文件 |
| `--pdf-notes` | 为 PDF 文件添加注释 |
| `--pdf-outlines` | 为 PDF 文件添加大纲/书签 |
| `--allow-local-files` | 允许访问本地文件（安全提示） |
| `--browser <chrome\|edge\|firefox>` | 选择用于转换的浏览器 |
| `--browser-path <路径>` | 指定浏览器的可执行文件路径 |
| `-P, --parallel <数量>` | 并行转换数量 |
| `--no-parallel` | 禁用并行转换 |
| `--template <名称>` | HTML 模板（默认：自定义模板） |

## 常见用法示例

```bash
# Watch and preview while editing
marp -w -p deck.md

# Serve slides directory
marp -s ./presentations

# Convert all slides to PDF
marp --pdf *.md

# Create OG image from title
marp deck.md -o og.png --image-scale 3

# Export presenter notes
marp --notes deck.md
```

## 文档资源

| 文档 | 描述 |
|----------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | 快速入门指南 |
| [EXAMPLES.md](EXAMPLES.md) | 使用示例 |
| [README.md](README.md) | 项目概述 |
| 官方文档 | https://github.com/marp-team/marp-cli |