---
name: pdf-tools
description: **功能概述：**  
能够查看、提取、编辑和操作 PDF 文件。支持文本提取、文本编辑（包括文本的叠加和替换）、文件合并、文件分割、页面旋转以及获取 PDF 元数据。适用于需要阅读 PDF 内容、添加/编辑文本、重新组织页面、合并文件或提取信息的场景。  

**主要功能：**  
1. **文本提取与编辑**：可以方便地从 PDF 文件中提取文本，并对提取的文本进行编辑（如添加新文本、替换现有文本等）。  
2. **文件合并与分割**：支持将多个 PDF 文件合并为一个文件，或从一个文件中分割出多个独立的 PDF 文件。  
3. **页面操作**：支持旋转 PDF 文件的页面，以满足不同的阅读需求。  
4. **PDF 元数据获取**：能够获取 PDF 文件的元数据（如文件大小、创建日期、作者等）。  

**使用场景：**  
- **内容阅读**：用于快速查看 PDF 文件中的内容。  
- **文本编辑**：对 PDF 文件中的文本进行修改或添加新的注释。  
- **文件管理**：合并多个 PDF 文件以创建一个新的文档，或从单个 PDF 文件中提取所需的部分。  
- **页面调整**：根据需要调整 PDF 文件的页面布局或顺序。  
- **信息提取**：从 PDF 文件中提取关键数据或信息。  

**适用场景示例：**  
- **文档整理**：将多个相关的 PDF 文件合并成一个统一的文档格式。  
- **内容编辑**：对 PDF 文件中的文本进行修改或补充说明。  
- **报告制作**：从多个 PDF 文件中提取数据并整合到一份报告中。  
- **格式转换**：将 PDF 文件转换为其他格式（如 Word 或图片）以方便进一步处理。
---

# PDF工具

使用Python库（pdfplumber和PyPDF2）来查看、提取和编辑PDF文件的工具。

## 快速入门

所有脚本都需要依赖以下库：
```bash
pip3 install pdfplumber PyPDF2
```

## 核心操作

### 提取文本

从PDF中提取文本（所有页面或特定页面）：
```bash
scripts/extract_text.py document.pdf
scripts/extract_text.py document.pdf -p 1 3 5
scripts/extract_text.py document.pdf -o output.txt
```

### 获取PDF信息

查看元数据和结构：
```bash
scripts/pdf_info.py document.pdf
scripts/pdf_info.py document.pdf -f json
```

### 合并PDF

将多个PDF文件合并为一个：
```bash
scripts/merge_pdfs.py file1.pdf file2.pdf file3.pdf -o merged.pdf
```

### 分割PDF

将PDF文件分割成单独的页面：
```bash
scripts/split_pdf.py document.pdf -o output_dir/
```

### 按页码范围分割PDF

根据指定的页码范围分割PDF：
```bash
scripts/split_pdf.py document.pdf -o output_dir/ -m ranges -r "1-3,5-7,10-12"
```

### 旋转页面

旋转所有页面或特定页面：
```bash
scripts/rotate_pdf.py document.pdf -o rotated.pdf -r 90
scripts/rotate_pdf.py document.pdf -o rotated.pdf -r 180 -p 1 3 5
```

### 编辑文本

在页面上添加文本覆盖层：
```bash
scripts/edit_text.py document.pdf -o edited.pdf --overlay "New Text" --page 1 --x 100 --y 700
scripts/edit_text.py document.pdf -o edited.pdf --overlay "Watermark" --page 1 --x 200 --y 400 --font-size 20
```

替换文本（功能有限，适用于简单情况）：
```bash
scripts/edit_text.py document.pdf -o edited.pdf --replace "Old Text" "New Text"
```

**注意：**由于PDF格式的特殊性，文本编辑较为复杂。使用文本覆盖层的方法比直接替换文本更可靠。

## 工作流程模式

### 查看PDF内容

1. 获取基本信息：`scripts/pdf_info.py file.pdf`
2. 提取文本以进行预览：`scripts/extract_text.py file.pdf -p 1`
3. 如需提取全部文本：`scripts/extract_text.py file.pdf -o content.txt`

### 重新组织PDF文件

1. 将PDF文件分割成单独的页面：`scripts/split_pdf.py input.pdf -o pages/`
2. 合并选定的页面：`scripts/merge_pdfs.py pages/page_1.pdf pages/page_3.pdf -o reordered.pdf`

### 提取PDF中的特定部分

1. 获取页面数量：`scripts/pdf_info.py document.pdf`
2. 按指定范围分割PDF：`scripts/split_pdf.py document.pdf -o sections/ -m ranges -r "1-5,10-15"`

## 高级用法

有关库的详细文档和高级使用方法，请参阅[references/libraries.md](references/libraries.md)。

## 注意事项

- 所有脚本中的页码都是从1开始的（第1页为第1页）
- 文本提取功能适用于基于文本的PDF文件（非扫描图像）
- 旋转角度支持：90度、180度、270度或-90度（逆时针方向）
- 所有脚本在处理前都会验证文件是否存在