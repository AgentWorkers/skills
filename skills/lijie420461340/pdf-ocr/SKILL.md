---
name: PDF OCR Extraction
description: 使用光学字符识别（OCR）技术从扫描的PDF文件中提取文本。
author: claude-office-skills
version: "1.0"
tags: [pdf, ocr, text-extraction, scanning, document]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, file_operations]
---

# PDF 文本提取（OCR 技术）

使用 OCR 技术从扫描文档和基于图像的 PDF 文件中提取文本。

## 概述

此技能可帮助您：
- 从扫描文档中提取文本
- 使图像 PDF 可搜索
- 将纸质文档数字化
- 处理手写文本（功能有限）
- 批量处理多份文档

## 使用方法

### 基础 OCR
```
"Extract text from this scanned PDF"
"OCR this document image"
"Make this PDF searchable"
```

### 带有选项的 OCR
```
"Extract text from pages 1-10, English language"
"OCR this document, preserve layout"
"Extract and output as structured data"
```

## 文档类型

### 不同文档类型的 OCR 质量
| 文档类型 | 预期质量 | 注意事项 |
|---------------|------------------|------|
| **打字文档** | ⭐⭐⭐⭐⭐ 95%+ | 效果最佳 |
| **印刷书籍** | ⭐⭐⭐⭐ 90%+ | 注意文本老化问题 |
| **表格/数据** | ⭐⭐⭐ 80%+ | 需可能需手动调整表格结构 |
| **手写文档（字迹清晰）** | ⭐⭐ 60-80% | 结果因字迹清晰度而异 |
| **手写文档（字迹潦草）** | ⭐ 30-60% | 通常需要手动审核 |
| **混合内容** | ⭐⭐⭐ 75%+ | 效果取决于内容复杂性 |

## 输出格式

### 纯文本提取
```markdown
## OCR Result: [Document Name]

**Pages Processed**: [X]
**Language**: [Detected/Specified]
**Confidence**: [X]%

---

[Extracted text content here]

---

### Notes
- [Any issues or uncertainties]
- [Characters that may be incorrect]
```

### 结构化数据提取
```markdown
## OCR Extraction: [Document Name]

### Document Info
| Field | Value |
|-------|-------|
| Title | [Extracted or inferred] |
| Date | [If found] |
| Author | [If found] |

### Content by Section

#### [Header 1]
[Content under this header]

#### [Header 2]
[Content under this header]

### Tables Found
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| [Data] | [Data] | [Data] |

### Uncertain Text
| Page | Original | Confidence | Possible |
|------|----------|------------|----------|
| 3 | "teh" | 70% | "the" |
| 5 | "l0ve" | 65% | "love" |
```

### 可搜索的 PDF 输出
```markdown
## OCR to Searchable PDF

**Source**: [filename.pdf]
**Output**: [filename_searchable.pdf]

### Processing Summary
| Metric | Value |
|--------|-------|
| Pages | [X] |
| Words extracted | [Y] |
| Average confidence | [Z]% |
| Processing time | [T] seconds |

### Quality Report
- [X] pages with 95%+ confidence
- [Y] pages with 80-94% confidence
- [Z] pages with <80% confidence (review recommended)

### Searchability
✅ Document is now text-searchable
✅ Original images preserved
✅ Text layer added behind images
```

## 预处理建议

### 图像质量检查
在进行 OCR 处理之前，请确保：
- [ ] **分辨率**：至少 300 DPI（小字体时建议 600 DPI）
- [ ] **对比度**：黑色文字在白色背景上清晰可见
- [ ] **对齐**：文档无倾斜
- **完整性**：无裁剪边缘
- **清晰度**：无污渍、标记或阴影

### 常见预处理步骤
| 问题 | 解决方案 |
|-------|----------|
| 分辨率低 | 先对图像进行放大处理 |
| 文档倾斜/旋转 | 自动校正倾斜 |
| 对比度差 | 调整图像的对比度 |
| 图像中有噪声/斑点 | 应用降噪处理 |
| 图像中有阴影 | 平衡图像的明暗 |
| 颜色文档 | 将文档转换为灰度图像 |

## 语言支持

- **支持的语言**：
  - **优秀支持**：英语、西班牙语、法语、德语、意大利语
  - **良好支持**：中文（简体/繁体）、日语、韩语
  - **中等支持**：阿拉伯语、希伯来语（右-to-left 文本方向）、印地语
  - **基本支持**：其他多种语言，但质量可能有所不同

## 多语言文档处理
```
"OCR this document, detect language automatically"
"Extract text, primary: English, secondary: Chinese"
```

## 处理特定类型的内容

### 表格和复选框
```markdown
## Form Extraction: [Form Name]

### Field Values
| Field | Value | Confidence |
|-------|-------|------------|
| Name | John Smith | 98% |
| Date | 01/15/2026 | 95% |
| Address | 123 Main St | 92% |

### Checkboxes
| Question | Checked |
|----------|---------|
| Option A | ☑️ Yes |
| Option B | ☐ No |
| Option C | ☑️ Yes |

### Signature
[Signature detected on page X - cannot extract text]
```

### 表格数据提取
```markdown
## Table Extraction

### Table 1 (Page 2)
| Header A | Header B | Header C |
|----------|----------|----------|
| Value 1 | Value 2 | Value 3 |
| Value 4 | Value 5 | Value 6 |

**Table confidence**: 85%
**Note**: Column 3 may have alignment issues
```

### 手写文本处理
```markdown
## Handwritten Text Extraction

**Legibility Assessment**: [Good/Fair/Poor]
**Recommended**: Manual review

### Extracted Text (Confidence: 65%)
[Extracted text with uncertain words marked]

### Uncertain Words
| Original | Best Guess | Alternatives |
|----------|------------|--------------|
| [image] | "meeting" | "meeting", "meaning" |
| [image] | "Tuesday" | "Tuesday", "Thursday" |

⚠️ **Low confidence extraction - please verify manually**
```

## 批量处理

### 批量 OCR 任务
```markdown
## Batch OCR Processing

**Folder**: [Path]
**Total Documents**: [X]
**Status**: [In Progress/Complete]

### Results
| File | Pages | Confidence | Status |
|------|-------|------------|--------|
| doc1.pdf | 5 | 96% | ✅ Complete |
| doc2.pdf | 12 | 88% | ✅ Complete |
| doc3.pdf | 3 | 72% | ⚠️ Review |
| doc4.pdf | 8 | - | ❌ Failed |

### Issues
- doc3.pdf: Pages 2-3 have handwriting
- doc4.pdf: File corrupted

### Summary
- Successful: [X]
- Need Review: [Y]
- Failed: [Z]
```

## 工具推荐

### 云服务
- **Google Cloud Vision**（准确率极高）
- **Amazon Textract**（适用于表格数据）
- **Azure Computer Vision**（性能均衡）
- **Adobe Acrobat**（内置 OCR 功能）

### 桌面软件
- **ABBYY FineReader**（准确率最高）
- **Adobe Acrobat Pro**（可靠性高）
- **Readiris**（性价比高）
- **Tesseract**（免费开源工具）

### 编程库
- **pytesseract**（Python + Tesseract）
- **EasyOCR**（Python，支持多种语言）
- **PaddleOCR**（Python，适用于亚洲语言）

## 注意事项

- 无法保证 100% 的准确率
- 手写文本的识别效果较差
- 非常小的文字可能无法被正确识别
- 装饰性字体可能导致识别困难
- 背景图像会影响识别效果
- 复杂图形中的文字可能无法被识别
- 文档页数越多，处理时间越长