---
name: PDF Converter
description: 将 PDF 文件转换为 Word、Excel、图片等格式，以及将其他格式的文件转换为 PDF 格式。
author: claude-office-skills
version: "1.0"
tags: [pdf, conversion, document, format, export, import]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, file_operations]
---

# PDF转换工具

能够将PDF文件转换为多种格式，反之亦然，同时保持文件原有的格式。

## 概述

本技能可帮助您：
- 将PDF文件转换为可编辑的格式（如Word、Excel）
- 将其他格式的文档转换为PDF
- 从PDF文件中提取图片
- 优化转换质量
- 执行批量转换操作

## 支持的转换类型

### PDF转换为其他格式
| 目标格式 | 适用场景 | 转换质量 |
|---------------|------------|---------|
| **Word (.docx)** | 以文本为主的文档 | 非常出色 |
| **Excel (.xlsx)** | 表格和数据 | 非常出色 |
| **PowerPoint (.pptx)** | 演示文稿 | 非常出色 |
| **图片 (.png/.jpg)** | 图片文件 | 非常出色 |
| **文本 (.txt)** | 纯文本文件 | 非常出色 |
| **HTML** | 网页内容 | 非常出色 |
| **Markdown (.md)** | 结构化文本 | 非常出色 |

### 其他格式转换为PDF
| 源格式 | 转换质量说明 |
|---------------|-------------------|
| **Word (.docx)** | 保留格式效果非常好 |
| **Excel (.xlsx)** | 保留格式效果较好，但需注意分页问题 |
| **PowerPoint (.pptx)** | 动画效果会丢失，但格式基本保留 |
| **图片** | 转换效果取决于图片分辨率 |
| **HTML** | 转换效果因CSS样式不同而有所差异 |
| **文本 (.txt)** | 转换效果完美，但格式较为简单 |

## 使用方法

### 基本转换
```
"Convert this PDF to Word"
"Save this document as PDF"
"Extract this PDF as images"
```

### 带参数的转换
```
"Convert PDF to Word, preserve exact formatting"
"Export PDF pages 1-5 as PNG images at 300 DPI"
"Convert Excel to PDF, fit all columns on one page"
```

### 批量转换
```
"Convert all PDFs in this folder to Word documents"
"Create PDFs from these 10 Word files"
```

## 转换注意事项

### PDF转换为Word
```markdown
## PDF to Word Conversion

### Best Practices
1. **Check source PDF type**:
   - Native PDF (from Word/etc): Best results
   - Scanned PDF: Use OCR first
   - Image-based: Limited accuracy

2. **Formatting considerations**:
   - Complex layouts may shift
   - Fonts substitute if not installed
   - Tables may need adjustment
   - Headers/footers require review

### Quality Settings
| Setting | Result |
|---------|--------|
| **Exact** | Matches layout precisely, harder to edit |
| **Editable** | Optimized for editing, may shift layout |
| **Text only** | Plain text, no formatting |

### Common Issues
| Issue | Solution |
|-------|----------|
| Text as image | Run OCR before converting |
| Missing fonts | Embed or substitute fonts |
| Broken tables | Manually adjust in Word |
| Lost colors | Check color profile settings |
```

### PDF转换为Excel
```markdown
## PDF to Excel Conversion

### Ideal Sources
- PDF with clear table structure
- Financial statements
- Data reports
- Invoices with line items

### Extraction Methods
| Method | Use When |
|--------|----------|
| **Auto-detect tables** | Clear table borders |
| **Select area** | Tables without borders |
| **Full page** | Entire page is data |

### Quality Tips
1. Ensure PDF has selectable text (not scanned)
2. Clean table borders help detection
3. Merged cells may cause issues
4. Multi-page tables need manual merge

### Data Cleanup
After conversion, check:
- [ ] Column alignment
- [ ] Number formatting
- [ ] Date formats
- [ ] Merged cell handling
- [ ] Header row detection
```

### PDF转换为图片
```markdown
## PDF to Image Conversion

### Resolution Settings
| DPI | Use Case | File Size |
|-----|----------|-----------|
| 72 | Screen viewing | Small |
| 150 | Email/web | Medium |
| 300 | Print quality | Large |
| 600 | High-quality print | Very large |

### Format Selection
| Format | Best For |
|--------|----------|
| **PNG** | Text, graphics, transparency |
| **JPG** | Photos, smaller files |
| **TIFF** | Print production |
| **WebP** | Web optimization |

### Output Options
- All pages → separate images
- Specific pages → selected images
- Page range → batch export
```

### 将其他格式转换为PDF
```markdown
## Converting to PDF

### From Word
**Settings**:
- [ ] Embed fonts
- [ ] Include bookmarks
- [ ] Set PDF/A for archival
- [ ] Compress images (optional)

### From Excel
**Settings**:
- [ ] Define print area
- [ ] Set page breaks
- [ ] Choose orientation
- [ ] Fit to page options

### From PowerPoint
**Settings**:
- [ ] Slide range
- [ ] Include notes (optional)
- [ ] Quality level
- [ ] Handout format (optional)

### Universal Tips
1. Review in print preview first
2. Check page breaks
3. Ensure fonts are embedded
4. Verify hyperlinks work
```

## 批量处理

### 批量转换模板
```markdown
## Batch Conversion Job

**Source**: [Folder path]
**Target Format**: [Format]
**Output Folder**: [Path]

### Files to Convert
| File | Pages | Status |
|------|-------|--------|
| document1.pdf | All | ✅ Complete |
| document2.pdf | All | ✅ Complete |
| document3.pdf | 1-5 | ⏳ Processing |

### Settings Applied
- Resolution: [X] DPI
- Quality: [High/Medium/Low]
- Naming: [Original name]_converted.[ext]

### Summary
- Total files: [X]
- Successful: [Y]
- Failed: [Z]
```

## 常见问题及解决方法

| 问题 | 原因 | 解决方法 |
|---------|--------|-----------|
| 文本无法选中 | 文件为扫描PDF | 先使用OCR软件进行文字识别 |
| 部分字符缺失 | 字体问题 | 嵌入相应字体或重新转换文件 |
| 图片质量较差 | 分辨率过低 | 提高图片分辨率 |
| 文件体积过大 | 文件未压缩 | 对文件进行压缩 |
| 格式丢失 | 文件布局复杂 | 选择“精确转换”模式 |

## 转换质量检查

转换完成后，请检查以下内容：
- 所有文本是否完整且可读 |
- 格式是否基本保持不变 |
- 图片是否正确嵌入 |
- 表格结构是否清晰 |
- 链接是否正常工作（如适用） |
- 页数是否与源文件一致 |

## 工具推荐

### 在线工具
- Adobe Acrobat（转换质量最高） |
- SmallPDF（易于使用） |
- ILovePDF（支持批量转换） |
- PDF24（免费，转换质量不错） |

### 桌面软件
- Adobe Acrobat Pro |
- Microsoft Office（内置PDF转换功能） |
- LibreOffice（免费软件） |
- Foxit PDF Editor |

### 命令行工具
- Pandoc（用于文本格式转换） |
- ImageMagick（用于图片处理） |
- pdftk（用于PDF文件操作） |
- Poppler（相关转换工具）

## 限制事项

- 该工具本身不执行实际的文件转换，仅提供转换指导 |
- 扫描生成的PDF文件需要先进行OCR处理 |
- 复杂的文件布局可能无法完美转换 |
- 加密保护的PDF文件需要输入密码 |
- 某些格式在转换过程中可能会丢失 |
- 转换质量受源PDF文件类型的影响