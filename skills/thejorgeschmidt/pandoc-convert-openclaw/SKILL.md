---
name: pandoc-convert
description: 使用 pandoc CLI 可以在 40 多种格式之间转换文档。它支持 Markdown、Word、PDF、HTML、LaTeX 和 EPUB 格式，并提供了智能的默认设置、专业的模板以及全面的工具支持。
tags: [documents, conversion, productivity, pandoc]
---

# 📄 Pandoc Convert（集成版）

**一个集成了统一Python工具和模块化bash实用程序的通用文档转换器。**

**pandoc-convert**技能提供了使用pandoc在40多种格式之间转换文档的智能工作流程。这个集成版本包含了：**
- **统一的Python转换器**（convert.py）：适用于大多数转换任务的强大工具
- **模块化的bash实用程序**（batch_convert.sh, validate.sh）：用于特定任务的脚本
- **全面的模板**：包括LaTeX学术格式和现代CSS格式的模板
- **专业文档支持**：提供完整的指南、故障排除方法和参考资料

## ✨ 主要特性

- **支持40多种格式**：Markdown、Word、PDF、HTML、LaTeX、EPUB、RST、AsciiDoc、Org-mode等
- **双工具组合**：使用Python进行智能转换，使用bash进行验证/批量处理
- **专业模板**：提供12种模板，适用于学术、商业和网页用途
- **全面的文档支持**：包括格式指南、故障排除方法、模板和快速参考
- **智能默认设置**：为每种转换路径优化了配置
- **元数据保留**：在不同格式间保持标题、作者和日期等信息的一致性
- **错误处理**：提供详细的错误信息和恢复机制

## 🔧 先决条件

### 必需安装
- **pandoc**（建议使用v2.19及以上版本）
- **Python 3.8及以上**（用于convert.py脚本）

### 可选安装（针对特定格式）
- **LaTeX**（TeX Live或MiKTeX）：生成PDF格式时需要
- **wkhtmltopdf**：用于将HTML转换为PDF的替代工具
- **librsvg**：支持SVG格式
- **epubcheck**：用于EPUB格式的验证

详细安装说明请参阅`INSTALL.md`。

## 📚 快速入门

### 推荐使用Python脚本（convert.py）

```bash
# Single file conversion
python scripts/convert.py input.md output.pdf

# With custom template
python scripts/convert.py report.md report.pdf --template business --toc

# Batch convert
python scripts/convert.py --batch *.md --format pdf --output-dir ./pdfs
```

### 使用bash实用程序（batch_convert.sh, validate.sh）

```bash
# Batch convert with validation
./scripts/batch_convert.sh input/*.md pdf output/

# Validate output
./scripts/validate.sh output/document.pdf
./scripts/validate.sh output/book.epub
```

### 直接使用pandoc命令

```bash
# Markdown → PDF
pandoc input.md -o output.pdf

# Markdown → Word
pandoc input.md -o output.docx

# Word → Markdown
pandoc input.docx -o output.md --extract-media=./media
```

## 🎯 常见工作流程

详细步骤指南请参阅`references/conversion-guides.md`：
- 将Markdown转换为专业PDF（适用于商业报告或学术论文）
- 将Word转换为Markdown（便于版本控制）
- 将Markdown转换为EPUB格式（用于电子书）
- 将多个Markdown文件合并为单个PDF文件
- 将Markdown转换为HTML5格式（独立网页）

## 🎨 模板

### LaTeX模板（学术/专业用途）
- `academic-paper.tex`：学术论文模板
- `business-letter.tex`：商务信函模板
- `technical-report.tex`：技术文档模板
- `resume.tex`：简历模板
- `professional.tex`：通用专业文档模板
- `report-template.tex`：报告结构模板

### CSS模板（网页/现代风格）
- `github.css`：GitHub Markdown样式
- `blog-style.css`：简洁的博客样式
- `epub-style.css`：电子书样式
- `presentation.html`：HTML演示文稿模板
- `ebook.css`：增强型电子书布局

### 参考文档
- `reference-styles.docx`：Word格式的参考样式文档

所有模板均位于`templates/`目录中。

## 🔧 工具参考

### convert.py（Python）
- 集成转换工具，具有智能默认设置

```bash
python scripts/convert.py [OPTIONS] INPUT OUTPUT

Options:
  --format FORMAT       Force output format
  --template TEMPLATE   Use named template
  --toc                 Include table of contents
  --number-sections     Number headings
  --title TITLE         Document title
  --author AUTHOR       Document author
  --batch               Batch mode
  --validate            Validate output
  --verbose             Detailed output
```

### batch_convert.sh（Bash）
- 支持批量处理，并可跟踪处理进度

```bash
./scripts/batch_convert.sh INPUT_DIR FORMAT OUTPUT_DIR [OPTIONS]

# Example
./scripts/batch_convert.sh ./docs/ pdf ./output/ --toc --number-sections
```

### validate.sh（Bash）
- 转换后的文档验证工具

```bash
./scripts/validate.sh FILE

# Validates:
# - PDF structure and readability
# - EPUB spec compliance (requires epubcheck)
# - HTML validity
# - File integrity
```

## 📊 格式支持

### 输入格式
- **Markdown**：`markdown`, `gfm`, `markdown_mmd`
- **Word**：`docx`, `odt`, `rtf`
- **Web**：`html`, `html5`
- **LaTeX**：`latex`, `tex`
- **纯文本**：`txt`, `rst`, `textile`, `asciidoc`
- **学术格式**：`jats`, `docbook`
- **演示文稿**：`pptx`
- **电子书**：`epub`
- **其他格式**：`json`, `csv`, `org`, `mediawiki`, `man`

### 输出格式
- 所有支持的输入格式
- **PDF**
- **EPUB**
- **RevealJS**
- **Beamer**

完整的格式转换矩阵请参阅`references/format-matrix.md`。

## 🗂️ 目录结构

```
pandoc-convert-integrated/
├── SKILL.md              # This file
├── INSTALL.md            # Detailed installation guide
├── README.md             # Quick start guide
├── scripts/
│   ├── convert.py        # Unified Python converter
│   ├── batch_convert.sh  # Bash batch processor
│   └── validate.sh       # Validation utility
├── templates/
│   ├── *.tex             # LaTeX templates (6)
│   ├── *.css             # CSS templates (3)
│   ├── *.html            # HTML templates (1)
│   └── *.docx            # Word reference (1)
└── references/
    ├── format-guide.md         # Format details
    ├── format-matrix.md        # Compatibility matrix
    ├── conversion-guides.md    # Step-by-step guides
    ├── format-support.md       # Supported features
    ├── quick-reference.md      # Cheat sheet
    ├── templates.md            # Template documentation
    └── troubleshooting.md      # Problem solving
```

## 🐛 故障排除

### 常见问题
- **“pandoc: command not found”**：请安装pandoc（详见INSTALL.md）
- **“pdflatex not found”**：请安装LaTeX相关软件
- **PDF中的Unicode显示问题**：使用`--pdf-engine=xelatex`选项
- **图片缺失**：检查文件路径，并使用`--resource-path`选项
- **EPUB格式验证失败**：运行`epubcheck`工具进行排查

详细解决方案请参阅`references/troubleshooting.md`。

## 📖 参考资料

- **INSTALL.md**：针对不同平台的安装指南
- **references/format-guide.md**：各格式的详细说明和限制
- **references/conversion-guides.md**：详细的转换步骤指南
- **references/quick-reference.md**：快速参考手册
- **references/templates.md**：模板的使用和自定义方法
- **references/troubleshooting.md**：高级问题解决方法

## 🎯 最佳实践
- 使用YAML格式编写文档的开头部分（包含元数据，如标题、作者和日期）
- 在分享前验证转换结果（尤其是EPUB和PDF格式）
- 对源代码进行版本控制（控制Markdown文件，而非转换后的输出文件）
- 在批量处理前先测试模板
- 在执行批量操作前备份数据

## 🚀 性能优化
- 使用`batch_convert.sh`并行处理多个文件
- 将模板缓存到`~/.pandoc/templates/`目录
- 采用增量式构建方式（仅重新转换已更改的文件）
- 对于非常大的文档（超过10MB），请增加系统内存限制

## 📜 许可证

本工具属于OpenClaw项目的一部分。pandoc本身采用GPL许可证。

---

**快速使用示例**：
- 使用Python脚本转换：`python scripts/convert.py input.md output.pdf`
- 批量转换：`./scripts/batch_convert.sh *.md pdf ./output/`
- 验证转换结果：`./scripts/validate.sh output.pdf`
- 更多帮助信息请参阅`README.md`及`references/`目录。