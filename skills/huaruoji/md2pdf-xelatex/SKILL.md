---
name: md2pdf
description: 将 Markdown 文件转换为支持完整 LaTeX 数学公式渲染以及 CJK（中文/日文/韩文）显示的 PDF 文件。适用于用户需要将 Markdown 转换为 PDF、将报告渲染为 PDF、将笔记导出为 PDF 或从 Markdown 生成可打印文档的场景。该工具能够处理 `$...$` 和 `$$...$$` 格式的内联数学公式、代码块、表格以及混合 CJK/拉丁文文本。需要安装 pandoc 和 texlive-xetex 工具。
---
# md2pdf

通过 Pandoc 和 XeLaTeX 将 Markdown 文件转换为 PDF 格式。支持完整的 LaTeX 数学公式和中文（CJK）字符。

## 先决条件

系统软件包（使用 apt 包管理器安装）：

```
pandoc texlive-xetex texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra texlive-lang-chinese
```

## 快速转换

```bash
bash <skill_dir>/scripts/md2pdf.sh input.md output.pdf
```

该脚本会自动检测中文（CJK）内容，选择合适的字体，处理表情符号（emoji），生成目录（TOC），并配置 XeLaTeX 的相关设置。

## 手动使用 Pandoc 命令

如需更精细的控制，可以直接运行 Pandoc 命令：

```bash
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -f markdown-smart \
  -H header.tex \
  -V mainfont="DejaVu Sans" \
  -V monofont="DejaVu Sans Mono" \
  -V geometry:margin=20mm \
  -V fontsize=10pt \
  -V colorlinks=true \
  --highlight-style=tango \
  --toc -V toc-title="Table of Contents"
```

其中 `header.tex` 文件包含以下内容：

```latex
\usepackage{xeCJK}
\setCJKmainfont{<CJK font name>}
```

## 主要特性

- **数学公式**：Pandoc 可以直接将 `$...$`（内联公式）和 `$$...$$`（显示公式）转换为 LaTeX 数学公式，无需使用 MathJax 或 KaTeX。
- **中文字体**：脚本会自动从以下字体中选择合适的中文字体：Noto Sans CJK SC > WenQuanYi Micro Hei > Droid Sans Fallback > AR PL UMing CN。
- **表情符号**：由于大多数 LaTeX 字体不支持表情符号，因此会将其替换为相应的文本（例如 `✅` → `[Y]`，`❌` → `[N]`，`⭐` → `*`）。
- **智能引号**：使用 `-f markdown-smart` 选项可以避免引号显示问题。
- **长表格**：Pandoc 在处理复杂表格时可能会出现问题；建议保持表格结构简单，或使用 `longtable` LaTeX 包来生成表格。

## 常见问题及解决方法

| 问题 | 解决方法 |
|---------|-----|
| 缺少字符的警告 | 检查 `fc-list :lang=zh` 以确认可用的中文字体；如有需要，安装 `fonts-noto-cjk`。 |
| 无法找到 XeLaTeX | 安装 `texlive-xetex`。 |
| PDF 文件中的数学公式无法显示 | 确保在 Markdown 中使用 `$...$` 或 `$$...$$` 标签来表示数学公式（而非 HTML 格式的数学标签）。 |
| 表格布局混乱 | 简化表格内容，或添加 `-V geometry:margin=15mm` 选项以增加表格宽度。 |