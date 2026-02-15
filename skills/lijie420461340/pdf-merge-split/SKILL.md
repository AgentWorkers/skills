---
name: PDF Merge & Split
description: 合并多个 PDF 文件或将其拆分为单独的文件
author: claude-office-skills
version: "1.0"
tags: [pdf, merge, split, combine, extract, pages]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, file_operations]
---

# PDF合并与分割

将多个PDF文件合并为一个文件，或将PDF文件分割成多个独立的文档。

## 概述

本技能可帮助您：
- 将多个PDF文件合并为一个文件
- 按页码范围分割PDF文件
- 提取特定页面
- 重新排列PDF文件中的页面顺序
- 创建自定义的页面布局

## 使用方法

### 合并PDF文件
```
"Merge these 3 PDFs into one file"
"Combine document1.pdf and document2.pdf"
"Join all PDFs in this folder in alphabetical order"
```

### 分割PDF文件
```
"Split this PDF into individual pages"
"Extract pages 5-10 from this PDF"
"Split this PDF every 5 pages"
```

### 重新排列页面顺序
```
"Move page 3 to the end"
"Reorder pages: 1, 3, 2, 4, 5"
"Reverse the page order"
```

## 合并操作

### 基本合并
```markdown
## PDF Merge Plan

### Input Files
| Order | File | Pages | Size |
|-------|------|-------|------|
| 1 | cover.pdf | 1 | 50 KB |
| 2 | chapter1.pdf | 15 | 2.1 MB |
| 3 | chapter2.pdf | 22 | 3.4 MB |
| 4 | appendix.pdf | 8 | 1.2 MB |

### Output
- **Filename**: combined_document.pdf
- **Total Pages**: 46
- **Estimated Size**: ~6.7 MB

### Merge Options
- [ ] Add bookmarks for each source file
- [ ] Preserve original bookmarks
- [ ] Include blank page between files
- [ ] Optimize/compress output
```

### 高级合并
```markdown
## Advanced PDF Merge

### Custom Page Selection
| Source | Pages to Include | Insert Position |
|--------|------------------|-----------------|
| main.pdf | 1-10 | 1-10 |
| insert.pdf | All (5 pages) | After page 10 |
| main.pdf | 11-20 | 16-25 |
| appendix.pdf | 2-4 only | 26-28 |

### Output Configuration
- **Filename**: custom_merged.pdf
- **Page numbering**: Reset to 1 / Continue from original
- **Bookmarks**: Create from filenames / Preserve all

### Quality Settings
- Resolution: Original / Reduce to [X] DPI
- Compression: None / Low / Medium / High
```

## 分割操作

### 按页码范围分割
```markdown
## PDF Split Plan

### Source
- **File**: large_document.pdf
- **Total Pages**: 100

### Split Configuration
| Output File | Page Range | Pages |
|-------------|------------|-------|
| part1.pdf | 1-25 | 25 |
| part2.pdf | 26-50 | 25 |
| part3.pdf | 51-75 | 25 |
| part4.pdf | 76-100 | 25 |

### Naming Pattern
`[original_name]_part[N].pdf`
```

### 按文件大小分割
```markdown
## Split by File Size

### Source
- **File**: huge_report.pdf
- **Total Pages**: 500
- **File Size**: 250 MB

### Target
- **Max file size**: 25 MB
- **Estimated splits**: ~10 files

### Output
| File | Pages | Actual Size |
|------|-------|-------------|
| report_001.pdf | 1-52 | 24.8 MB |
| report_002.pdf | 53-98 | 23.2 MB |
| ... | ... | ... |
```

### 按书签分割
```markdown
## Split by Bookmarks/Chapters

### Source Structure
- large_manual.pdf
  - Chapter 1: Introduction (p.1)
  - Chapter 2: Setup (p.15)
  - Chapter 3: Usage (p.45)
  - Chapter 4: Advanced (p.120)
  - Appendix (p.180)

### Split Output
| File | Chapter | Pages |
|------|---------|-------|
| ch1_introduction.pdf | Introduction | 1-14 |
| ch2_setup.pdf | Setup | 15-44 |
| ch3_usage.pdf | Usage | 45-119 |
| ch4_advanced.pdf | Advanced | 120-179 |
| appendix.pdf | Appendix | 180-end |
```

### 提取特定页面
```markdown
## Page Extraction

### Source
- **File**: contract.pdf (20 pages)

### Pages to Extract
- [x] Page 1 (Cover)
- [x] Pages 5-7 (Terms)
- [x] Page 15 (Signatures)
- [x] Page 20 (Appendix A)

### Output
- **File**: contract_key_pages.pdf
- **Pages**: 6 total (1, 5, 6, 7, 15, 20)
```

## 页面操作

### 重新排列页面
```markdown
## Page Reorder Plan

### Current Order
1, 2, 3, 4, 5, 6, 7, 8, 9, 10

### New Order
1, 2, 4, 3, 5, 6, 8, 7, 9, 10

### Changes
- Page 3 ↔ Page 4 (swapped)
- Page 7 ↔ Page 8 (swapped)
```

### 删除页面
```markdown
## Page Deletion

### Source
- document.pdf (25 pages)

### Pages to Remove
- Page 3 (blank page)
- Pages 12-14 (outdated section)
- Page 25 (draft watermark)

### Result
- New page count: 20
- Output: document_cleaned.pdf
```

### 插入页面
```markdown
## Page Insertion

### Base Document
- main.pdf (10 pages)

### Insertions
| Insert | After Page | From |
|--------|------------|------|
| Cover page | 0 (beginning) | cover.pdf |
| Diagram | 5 | diagrams.pdf (page 2) |
| Appendix | 10 (end) | appendix.pdf |

### Result
- New page count: 14
```

### 旋转页面
```markdown
## Page Rotation

### File: scanned_doc.pdf

### Rotations Needed
| Page(s) | Current | Rotation | New |
|---------|---------|----------|-----|
| 3 | Portrait | 90° CW | Landscape |
| 7-9 | Upside down | 180° | Correct |
| 15 | Landscape | 90° CCW | Portrait |
```

## 批量处理

### 批量合并
```markdown
## Batch Merge Job

### Task: Merge PDFs by Project

### Folder Structure
```
/reports/
  /project-a/
    report1.pdf
    report2.pdf
  /project-b/
    summary.pdf
    details.pdf
```

### Output
| Merged File | Sources |
|-------------|---------|
| project-a_combined.pdf | report1.pdf, report2.pdf |
| project-b_combined.pdf | summary.pdf, details.pdf |
```

### 批量分割
```markdown
## Batch Split Job

### Input
- /monthly_reports/ (12 files, each ~50 pages)

### Operation
- Split each file into 5-page chunks

### Output
- /monthly_reports_split/
  - jan_001.pdf, jan_002.pdf, ...
  - feb_001.pdf, feb_002.pdf, ...
  - ...
```

## 工具推荐

### 免费工具
- **PDF24**：网页版和桌面版，功能齐全
- **ILovePDF**：基于网页的应用，易于使用
- **PDFsam Basic**：桌面版，开源软件
- **Preview (Mac)**：内置工具，支持拖放操作

### 专业工具
- **Adobe Acrobat Pro**：行业标准工具
- **Foxit PDF Editor**：功能强大的PDF编辑器
- **Nitro Pro**：适用于商务场景

### 命令行工具
- **pdftk**：经典工具，功能强大
- **qpdf**：处理速度快，支持脚本编写
- **pdfcpu**：基于Go语言的现代工具

## 限制

- 无法直接对文件进行实际操作（仅提供操作指导）
- 需要输入密码才能打开受保护的PDF文件
- 大文件可能需要分块处理
- 某些受限的PDF文件可能无法被修改
- 合并不同尺寸的页面时可能会出现问题