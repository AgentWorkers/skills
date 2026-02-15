---
name: PDF Compress
description: 在保持可接受质量的同时减小PDF文件的大小
author: claude-office-skills
version: "1.0"
tags: [pdf, compression, optimization, file-size, performance]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, file_operations]
---

# PDF压缩

减小PDF文件大小，以便于分享、加快加载速度并提高存储效率。

## 概述

本技能可帮助您：
- 显著减小PDF文件大小
- 在文件质量和大小之间取得平衡
- 根据具体用途（网页、打印、归档）进行优化
- 批量压缩多个文件
- 了解压缩过程中的权衡因素

## 使用方法

### 基本压缩
```
"Compress this PDF to reduce file size"
"Make this PDF smaller for email"
"Optimize this PDF for web viewing"
```

### 带目标参数的压缩
```
"Compress this PDF to under 5 MB"
"Reduce file size by at least 50%"
"Optimize for minimum file size"
```

### 质量级别
```
"Compress with high quality (minimal loss)"
"Compress for screen viewing"
"Maximum compression, quality not critical"
```

## 压缩级别

### 预设值
| 压缩级别 | 使用场景 | 图像质量 | 文件大小缩减比例 |
|-------|------------|---------------|----------------|
| **最低** | 归档 | 保持原样 | 5-15% |
| **低** | 打印 | 接近原样 | 15-30% |
| **中** | 通用用途 | 良好质量 | 30-50% |
| **高** | 电子邮件/网页 | 可接受的质量 | 50-70% |
| **最高** | 仅用于预览 | 大幅减小文件大小 | 70-90% |

### 使用场景推荐
| 使用场景 | 推荐压缩级别 | 原因 |
|----------|-------------------|--------|
| 打印文件 | 最低/低 | 对质量要求较高 |
| 电子邮件附件 | 中/高 | 在文件大小和质量之间取得平衡 |
| 网页下载 | 高 | 加快加载速度 |
| 快速预览 | 最高 | 优先考虑加载速度 |
| 归档 | 低 | 长期保存时保持文件质量 |
| 演示文稿 | 中 | 适合在屏幕上查看 |

## 压缩技术

### 图像优化
```markdown
## Image Compression Settings

### Resolution Reduction
| Target | DPI | Use For |
|--------|-----|---------|
| Screen | 72 | Web viewing |
| eBook | 150 | Digital documents |
| Print-basic | 200 | Office printing |
| Print-quality | 300 | Professional print |
| Original | N/A | No reduction |

### Format Conversion
| From | To | Savings | Quality Impact |
|------|-----|---------|----------------|
| TIFF | JPEG | 70-90% | Some loss |
| PNG | JPEG | 50-80% | Some loss |
| BMP | JPEG | 90%+ | Some loss |
| JPEG | JPEG (recompress) | 20-50% | Cumulative loss |

### Quality Levels
| Setting | JPEG Quality | Visual Impact |
|---------|--------------|---------------|
| Maximum | 90-100 | Imperceptible |
| High | 75-89 | Minimal |
| Medium | 50-74 | Noticeable on zoom |
| Low | 25-49 | Visible artifacts |
```

### 内容优化
```markdown
## Additional Optimizations

### Font Optimization
- [ ] Subset fonts (remove unused characters)
- [ ] Convert to standard fonts where possible
- [ ] Remove duplicate font instances

### Structure Optimization
- [ ] Remove unused objects
- [ ] Clean up metadata
- [ ] Linearize for web (fast web view)
- [ ] Remove bookmarks (optional)
- [ ] Remove comments/annotations (optional)

### Content Removal (Caution)
- [ ] Remove hidden layers
- [ ] Remove JavaScript
- [ ] Remove form fields
- [ ] Remove embedded files
```

## 输出报告

### 压缩报告
```markdown
## PDF Compression Report

### File Summary
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **File Size** | 45.2 MB | 8.7 MB | -81% |
| **Pages** | 120 | 120 | - |
| **Images** | 89 | 89 | - |

### Compression Applied
| Technique | Savings |
|-----------|---------|
| Image downsampling (150 DPI) | 28.5 MB |
| JPEG compression (75%) | 5.2 MB |
| Font subsetting | 1.8 MB |
| Object cleanup | 1.0 MB |
| **Total Savings** | **36.5 MB (81%)** |

### Quality Assessment
| Aspect | Rating | Notes |
|--------|--------|-------|
| Text clarity | ⭐⭐⭐⭐⭐ | No change |
| Image sharpness | ⭐⭐⭐⭐ | Slight softening |
| Color accuracy | ⭐⭐⭐⭐⭐ | Preserved |
| Zoom quality | ⭐⭐⭐ | Pixelation at 400%+ |

### Recommendations
✅ Suitable for: Email, web, screen viewing
⚠️ Not recommended for: High-quality print, archival
```

### 优化计划
```markdown
## Compression Strategy: [Document Name]

### Current State
- File size: 150 MB
- Pages: 200
- Issue: Too large for email (limit: 25 MB)

### Target
- Max size: 20 MB
- Maintain readability

### Recommended Approach
1. **Images**: Reduce to 150 DPI, JPEG 70%
   - Expected savings: ~100 MB
2. **Fonts**: Subset embedded fonts
   - Expected savings: ~5 MB
3. **Cleanup**: Remove metadata, optimize structure
   - Expected savings: ~5 MB

### Expected Result
- Final size: ~20 MB
- Quality: Good for screen/general use
```

## 批量压缩

### 批量压缩任务模板
```markdown
## Batch Compression Job

### Input
- **Folder**: /documents/reports/
- **Files**: 45 PDFs
- **Total Size**: 2.3 GB

### Settings
- Compression level: Medium
- Target: Email-friendly (<10 MB each)
- Image DPI: 150
- JPEG quality: 75%

### Progress
| File | Original | Compressed | Reduction |
|------|----------|------------|-----------|
| report_q1.pdf | 85 MB | 12 MB | 86% |
| report_q2.pdf | 120 MB | 18 MB | 85% |
| report_q3.pdf | 95 MB | 14 MB | 85% |
| ... | ... | ... | ... |

### Summary
| Metric | Value |
|--------|-------|
| Files processed | 45 |
| Total before | 2.3 GB |
| Total after | 380 MB |
| Average reduction | 83% |
| Files under 10 MB | 42/45 |

### Large Files (Need Review)
| File | Size | Recommendation |
|------|------|----------------|
| annual_photos.pdf | 25 MB | Split or higher compression |
| tech_diagrams.pdf | 18 MB | Reduce image count |
| charts_hires.pdf | 15 MB | Acceptable |
```

## 质量对比

### 压缩前后的效果对比
```markdown
## Quality Comparison Guide

### Image Quality at Different Levels

**Original (300 DPI, no compression)**
- Sharp at all zoom levels
- File size: Large

**High Quality (200 DPI, JPEG 85%)**
- Sharp at 100-200% zoom
- Minor softening at high zoom
- File size: Medium-large

**Medium Quality (150 DPI, JPEG 70%)**
- Good at 100% zoom
- Noticeable softening at 200%+
- File size: Medium

**Low Quality (96 DPI, JPEG 50%)**
- Acceptable at 100%
- Pixelation visible
- File size: Small

### Text Remains Sharp
Note: Text (when vector) remains crisp at all compression levels.
Only embedded text images are affected.
```

## 工具推荐

### 在线工具
- **SmallPDF**：操作简单，压缩效果良好
- **ILovePDF**：免费，支持批量压缩
- **PDF24**：提供丰富的配置选项
- **Adobe Online**：压缩效果专业

### 桌面软件
- **Adobe Acrobat Pro**：压缩控制最精细
- **Foxit PDF Editor**：优秀的替代工具
- **PDF-XChange**：功能多样
- **Preview (Mac)**：内置压缩功能

### 命令行工具
- **Ghostscript**：功能强大，支持脚本操作
- **qpdf**：压缩速度快，支持无损压缩
- **pdfcpu**：基于Go语言的现代压缩工具
- **img2pdf**：专门用于图像文件的压缩

## 限制因素

- 该工具本身不执行实际的压缩操作，仅提供压缩指导
- 某些PDF文件的可压缩内容较少
- 扫描文档主要由图像组成，压缩效果有限
- 已经压缩过的PDF文件进一步压缩的空间有限
- 过度压缩会影响文件质量
- 矢量图形难以被有效压缩