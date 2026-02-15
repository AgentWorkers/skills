# MXE 技能 - Markdown 导出工具

该工具可将 Markdown 文件转换为 PDF、DOCX 或 HTML 格式，并提供多种高级功能。

## 使用场景

当用户需要执行以下操作时，可以使用 MXE：
- 将 Markdown 文件转换为格式美观的 PDF 文件；
- 导出包含 Mermaid 图表的文档；
- 生成带有目录结构的 PDF 文件；
- 从 Markdown 文件创建专业文档；
- 下载网页文章并将其保存为 Markdown 格式。

## 安装检查

```bash
which mxe || echo "Not installed"
```

如果尚未安装，请执行以下操作：
```bash
cd /Users/tuan/.openclaw/workspace/mxe && npm run build && npm link
```

## 基本用法

```bash
# Simple PDF conversion
mxe document.md

# With table of contents
mxe document.md --toc

# Specify output directory
mxe document.md -o ./output
```

## 字体选项

```bash
# Custom body font
mxe document.md --font roboto

# Custom code font  
mxe document.md --mono-font fira-code

# Both
mxe document.md --font inter --mono-font jetbrains-mono
```

**可用的正文字体：** `inter`（默认）、`roboto`、`lato`、`opensans`、`source-sans`、`merriweather`

**可用的单色字体：** `jetbrains-mono`（默认）、`fira-code`、`source-code`

## Mermaid 图表

```bash
# Default theme
mxe document.md

# Forest theme
mxe document.md --mermaid-theme forest

# Hand-drawn style
mxe document.md --hand-draw

# Dark theme with ELK layout
mxe document.md --mermaid-theme dark --mermaid-layout elk
```

**主题选项：** `default`、`forest`、`dark`、`neutral`、`base`

## 完整示例

```bash
# Professional PDF with all features
mxe report.md \
  --toc \
  --font roboto \
  --mono-font fira-code \
  --mermaid-theme forest \
  -o ./output
```

## 输出格式

```bash
mxe doc.md -f pdf      # PDF (default)
mxe doc.md -f docx     # Word document
mxe doc.md -f html     # HTML file
mxe doc.md -f clipboard # Copy to clipboard
```

## 下载网页文章

```bash
# Download and convert URL to PDF
mxe https://example.com/article

# Download as Markdown only
mxe https://example.com/article -f clipboard
```

## 使用技巧：
1. **Mermaid 需要 mmdc**：请使用 `npm i -g @mermaid-js/mermaid-cli` 进行安装。
2. **图片的嵌入方式**：本地图片会以 Base64 编码的形式嵌入到 PDF 文件中。
3. **自定义样式**：可以使用 `-s style.css` 文件来应用自定义样式。
4. **书签**：PDF 文件会自动生成书签（可通过 `--no-bookmarks` 选项禁用此功能）。

## 工具位置

工具源代码位于：`/Users/tuan/.openclaw/workspace/mxe`