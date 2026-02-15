---
name: md2pdf-converter
description: 这是一个离线Markdown到PDF的转换工具，支持完整的Unicode编码。它利用Pandoc、WeasyPrint以及本地的emoji缓存机制，将Markdown文档转换为包含中文字体和彩色emoji的专业PDF格式。适用于用户需要将Markdown报告或文档转换为PDF格式、生成支持emoji的PDF文件、确保PDF中的中文字符正确显示，或者在完成初始设置后进行离线使用的场景。
---

# Markdown to PDF 转换器

## 概述

该工具可将 Markdown 文档转换为支持完整 Unicode 字符集、中文字体以及彩色表情符号的专业 PDF 文件。它基于 Pandoc 和 WeasyPrint 技术实现，并在首次运行后建立本地表情符号缓存，从而实现离线转换功能。

## 快速入门

要将 Markdown 文件转换为 PDF 文件，请执行以下命令：

```bash
bash scripts/md2pdf-local.sh input.md output.pdf
```

**仅首次运行时**：会从 npmmirror.com（一个适合中国的镜像网站）下载约 68MB 的表情符号资源。后续运行将无需联网。

**示例：**

```bash
bash scripts/md2pdf-local.sh report.md report.pdf
```

## 主要功能

- 完整的 Unicode 字符集支持（包括中文、日文、韩文）
- 彩色表情符号渲染（采用 Google 风格，64px 大小）
- 初始设置完成后可离线使用
- 适合中国的镜像网站（npmmirror.com）
- 专业的 PDF 格式（包含页码）
- 代码高亮显示、表格支持、块引用功能
- 自动检测并转换表情符号

## 技术细节

### 依赖库

- **Pandoc**：通用文档转换工具
- **WeasyPrint**：用于将 CSS 样式转换为 PDF 的渲染引擎
- **wget**：用于在首次运行时下载表情符号资源

### 工作原理

1. **首次运行**：将 emoji-datasource-google（版本 15.0.0）下载到 `~/.cache/md2pdf/emojis/` 目录中。
2. **Pandoc** 使用 Lua 过滤器将 Markdown 文件转换为 HTML 文件，同时将表情符号替换为对应的本地图片文件。
3. **WeasyPrint** 使用以下方式将 HTML 文件渲染为 PDF：
   - 使用 AR PL UMing CN 字体显示中文字符
   - 使用本地生成的 64px 大小的表情符号图片
   - 应用专业的 CSS 样式

### 表情符号缓存位置

```
~/.cache/md2pdf/emojis/
└── 1f600.png, 1f601.png, ... (all emoji PNGs)
```

### 使用的字体

- **主要中文字体**：AR PL UMing CN
- **备用字体**：Noto Sans SC、Noto Sans CJK SC、Microsoft YaHei
- **等宽字体**：Menlo、Monaco

## 限制

- 仅支持 emoji-datasource-google 15.0.0 中包含的表情符号（约 3600 个）
- 未包含的表情符号会以 Unicode 字符的形式显示
- 首次运行时需要联网（用于下载表情符号）

## 故障排除

### 字体问题

如果中文字符显示不正确，请确保已安装 AR PL UMing CN 字体：

```bash
# Ubuntu/Debian
sudo apt-get install fonts-arphic-uming

# Check if installed
fc-list | grep "AR PL UMing"
```

### 表情符号未显示

- 检查表情符号缓存是否存在：`ls ~/.cache/md2pdf/emojis/`
- 如果缓存缺失，请删除缓存并重新运行：`rm -rf ~/.cache/md2pdf`
- 确认表情符号图片文件是否存在：`ls ~/.cache/md2pdf/1f600.png`

### WeasyPrint 错误

如果遇到 WeasyPrint 错误，请安装缺失的依赖库：

```bash
# Ubuntu/Debian
sudo apt-get install python3-weasyprint

# Or via pip
pip3 install weasyprint
```

## 资源文件

### 脚本

**md2pdf-local.sh**：主要的转换脚本，支持自动表情符号缓存功能

**使用方法**：直接执行该脚本即可，无需将其添加到其他脚本环境中（除非需要进行调试或修改）。

**主要特点**：
- 自动下载并缓存表情符号
- 使用 Lua 过滤器替换表情符号
- 应用专业的 CSS 样式生成 PDF 文件
- 自动清理临时文件