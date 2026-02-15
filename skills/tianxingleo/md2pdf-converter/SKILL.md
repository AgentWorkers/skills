---
name: md2pdf-converter
description: 这是一个离线Markdown到PDF的转换工具，支持完整的Unicode编码。它使用了Pandoc、WeasyPrint以及本地的Twemoji缓存（包含3660种彩色表情符号）。该工具能够将Markdown文档转换为包含中文字体和彩色表情符号的专业PDF文件。适用于用户需要将Markdown报告或文档转换为PDF格式、生成支持表情符号的PDF文件、或在进行初始设置后离线使用的情况。
---
# Markdown to PDF 转换器（完整版本）

## 概述

本工具可将 Markdown 文档转换为专业的 PDF 文件，支持 **完整的 Unicode 字符集**、中文字体以及 **丰富多彩的emoji**（共 3660 个emoji，包含所有变体）。它基于 Pandoc 和 WeasyPrint 技术实现，并在首次运行后建立本地 Twemoji 缓存，从而支持离线转换。

## 快速入门

要将 Markdown 文件转换为 PDF，请执行以下命令：

```bash
bash scripts/md2pdf-local.sh input.md output.pdf
```

**首次运行时**：会从 GitHub 下载约 150MB 的 emoji 资源（Twemoji 14.0.0 版本），后续运行将支持离线转换。

**示例：**

```bash
bash scripts/md2pdf-local.sh report.md report.pdf
```

## 主要功能

- ✅ **完整的 Unicode 字符集支持**（包括中文、日文、韩文）
- ✅ **全面的 emoji 支持**（Twemoji 14.0.0 版本，3660 个彩色 PNG 图像）
- ✅ **支持所有 emoji 变体**（如肤色、发型、地区旗帜等）
- ✅ **首次设置完成后支持离线转换**
- ✅ 专业的 PDF 格式，包含页码
- ✅ 支持代码高亮显示、表格和块引用
- ✅ 通过 Python 生成的映射表实现准确的 emoji 显示

## 技术细节

### 依赖库

- **Pandoc**：通用文档转换工具
- **WeasyPrint**：CSS 到 PDF 的渲染引擎
- **Python 3**：用于生成 emoji 映射表
- **wget**：仅用于首次运行时下载 emoji 资源

### 工作原理

1. **首次运行**：将 Twemoji 14.0.0 下载到 `~/.cache/md2pdf/emojis/` 目录中。
2. **Python 脚本**：生成 emoji 与文件名的映射表（`emoji_mapping.json`）。
3. **Pandoc**：使用 Lua 过滤器将 Markdown 文件转换为 HTML，同时将 emoji 替换为本地图片。
4. **WeasyPrint**：使用以下方式将 HTML 文件渲染为 PDF：
   - 使用 AR PL UMing CN 字体显示中文字符
   - 使用本地生成的彩色 PNG emoji 图像（72x72px）
   - 应用专业的 CSS 样式

### emoji 缓存位置

```
~/.cache/md2pdf/
├── emojis/                    # 3660 colorful PNG files
│   ├── 0023-fe0f-20e3.png
│   ├── 1f600.png
│   └── ...
└── emoji_mapping.json         # Emoji to filename mapping
    {
      "🙀": "1f600.png",
      "⌛": "0023-fe0f-20e3.png",
      ...
    }
```

### emoji 映射机制

Python 脚本 `generate_emoji_mapping.py` 会扫描所有的 Twemoji 文件，生成 emoji 字符与 PNG 文件名之间的精确映射关系，确保即使对于复杂的 emoji 变体（如肤色和地区标志）也能正确显示。

### 使用的字体

- **主要中文字体**：AR PL UMing CN
- **备用字体**：Noto Sans SC、Noto Sans CJK SC、Microsoft YaHei
- **等宽字体**：Menlo、Monaco

## 版本历史

### v2.0（当前版本）

- ✅ 更换为 **Twemoji 14.0.0** 版本
- ✅ 支持 3660 个彩色 emoji（包含所有变体）
- ✅ 使用 Python 生成的映射表实现准确的 emoji 显示
- ✅ 修复了 emoji 显示为黑白的问题
- ✅ 完善了对 emoji 变体（如肤色、发型等）的支持

### v1.0（旧版本）

- 使用 emoji-datasource-google（约 2000-3000 个 emoji）
- 采用简单的十六进制文件名匹配方式（无法准确显示 emoji 变体）
- 部分 emoji 以黑白字符的形式显示

## 故障排除

### 字体问题

如果中文字符显示不正确，请确保已安装 AR PL UMing CN 字体：

```bash
# Ubuntu/Debian
sudo apt-get install fonts-arphic-uming

# Check if installed
fc-list | grep "AR PL UMing"
```

### emoji 未显示

1. 检查 emoji 缓存是否存在：`ls ~/.cache/md2pdf/emojis/`
2. 检查映射表是否存在：`ls ~/.cache/md2pdf/emoji_mapping.json`
3. 如果缓存缺失，请删除缓存并重新运行：`rm -rf ~/.cache/md2pdf`
4. 确认 emoji 文件是否存在：`ls ~/.cache/md2pdf/1f600.png`

### emoji 显示为黑白

此问题已在 v2.0 中得到修复。如果仍然遇到 emoji 显示为黑白的情况，请检查：
1. 确保使用的是 v2.0 版本的脚本：```bash
   grep "TWEMOJI_VERSION" scripts/md2pdf-local.sh
   # Should show: TWEMOJI_VERSION="14.0.0"
   ```
2. 清除缓存并重新运行程序：```bash
   rm -rf ~/.cache/md2pdf
   bash scripts/md2pdf-local.sh test.md test.pdf
   ```

### WeasyPrint 错误

如果遇到 WeasyPrint 运行错误，请安装缺失的依赖库：

```bash
# Ubuntu/Debian
sudo apt-get install python3-weasyprint

# Or via pip
pip3 install weasyprint
```

### Python 脚本错误

如果 `generate_emoji_mapping.py` 脚本执行失败，请检查相关错误信息：```bash
# Check Python version
python3 --version
# Should be Python 3.6+

# Check emoji cache
ls ~/.cache/md2pdf/emojis
```

## 资源文件

- **scripts/** 目录下包含以下脚本：
  - **md2pdf-local.sh**：主要转换脚本，负责自动下载和缓存 emoji
  - **generate_emoji_mapping.py**：生成 emoji 映射表的 Python 脚本

**使用方法**：可以从任意位置直接执行这些脚本（脚本使用绝对路径）：

```bash
bash /path/to/skills/md2pdf-converter/scripts/md2pdf-local.sh input.md output.pdf
```

**主要特点**：
- 自动下载和缓存 emoji
- 使用 Python 生成的 emoji 映射表（确保显示准确）
- 通过 Lua 过滤器替换 emoji
- 采用专业的 CSS 样式生成 PDF
- 自动清理临时文件

## v1.0 与 v2.0 的对比

| 特点 | v1.0（旧版本） | v2.0（新版本） |
|---------|----------------|---------------|
| emoji 来源 | emoji-datasource-google | Twemoji 14.0.0 |
| emoji 数量 | 约 2000-3000 个 | 3660 个 |
| 颜色显示 | 不稳定 | 稳定 |
| emoji 变体支持 | 不完整 | 完整 |
| 映射准确性 | 低 | 高 |
| 离线支持 | 首次运行后支持 | 首次运行后支持 |
| 首次运行所需空间 | 约 68MB | 约 150MB |

## 性能

- **首次运行**：下载约 150MB 数据，耗时 10-30 秒（取决于网络速度）
- **后续运行**：支持离线转换，转换速度极快
- **内存占用**： emoji 缓存占用约 150MB
- **PDF 生成时间**：每页约 1-5 秒

## 限制

- 新版本的 emoji（晚于 Twemoji 14.0.0 生成的）会以 Unicode 字符形式显示
- 首次运行需要网络连接（用于下载 emoji）
- emoji 缓存大小约为 150MB（包含 3660 个 72x72px 的 PNG 图像）