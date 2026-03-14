---
name: vector-text-fixer
description: 修复 PDF/SVG 矢量图形中的乱码，以便进行 AI 最终编辑。在保持原始格式和布局的同时，检测、替换并修复矢量图形文件中的乱码。
  Detect, replace and repair garbled text in vector graphic files while maintaining
  original formatting and layout.
version: 1.0.0
category: Visual
tags:
- pdf
- svg
- vector
- text-fix
- garbled-text
- document-repair
- encoding
author: AIPOCH
license: MIT
status: Draft
risk_level: Medium
skill_type: Tool/Script
owner: AIPOCH
reviewer: ''
last_updated: '2026-02-06'
---
# 向量文本修复工具

该工具可修复PDF/SVG矢量图形中的乱码问题，使其能够在人工智能（AI）工具中编辑。

## 主要功能

- **乱码检测**：自动识别PDF/SVG文件中的乱码内容。
- **智能修复**：根据上下文推断原始文本内容。
- **批量处理**：支持对文件夹中的多个文件进行批量处理。
- **格式保留**：修复后的文件保持原有的矢量格式和布局。
- **AI辅助编辑**：输出可导入AI编辑器的中间格式。

## 支持的场景

### 1. PDF乱码修复
- 由于字体嵌入问题导致的方框/问号等问题。
- 由于编码转换错误引起的乱码。
- 由于缺少字体替换而生成的异常字符。
- 多语言混合编码问题。

### 2. SVG乱码修复
- 文本实体编码错误。
- 特殊字符转义问题。
- 由于无效字体引用导致的显示异常。
- XML编码声明错误。

## 使用方法

### 命令行界面

```bash
# Fix a single PDF file
python scripts/main.py --input document.pdf --output fixed.pdf

# Fix a single SVG file
python scripts/main.py --input diagram.svg --output fixed.svg

# Batch process folder
python scripts/main.py --batch ./input_folder --output ./output_folder

# Interactive repair (manually specify replacement content)
python scripts/main.py --input doc.pdf --interactive

# Export as editable format (JSON)
python scripts/main.py --input doc.pdf --export-json editable.json
```

### Python API

```python
from scripts.main import VectorTextFixer

# Create fixer instance
fixer = VectorTextFixer()

# Fix PDF
result = fixer.fix_pdf("input.pdf", "output.pdf")

# Fix SVG
result = fixer.fix_svg("input.svg", "output.svg")

# Batch processing
results = fixer.batch_fix("./input_folder", "./output_folder")

# Get text map (for AI editing)
text_map = fixer.extract_text_map("input.pdf")
```

## 输入参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|------|------|
| `--input` | str | 是* | 输入文件路径（PDF或SVG） |
| `--batch` | str | 否 | 批量处理的输入文件夹 |
| `--output` | str | 是* | 输出文件/文件夹路径 |
| `--interactive` | bool | 否 | 启用交互式修复模式 |
| `--export-json` | str | 否 | 导出可编辑的JSON格式 |
| `--encoding` | str | 否 | 指定源文件编码（默认：自动检测） |
| `--font-substitution` | dict | 否 | 字体替换映射 |
| `--repair-level` | str | 否 | 修复级别：最小化、标准、激进（默认：标准） |

*至少需要指定`--input`和`--batch`中的一个参数。

## 输出格式

### 修复后的PDF/SVG
- 保持原有的矢量格式。
- 乱码被替换为可读的内容。
- 字体和布局保持不变。

### JSON输出格式
```json
{
  "file_type": "pdf",
  "pages": [
    {
      "page_num": 1,
      "text_blocks": [
        {
          "id": "tb_001",
          "bbox": [100, 200, 300, 220],
          "original_text": "�����",
          "detected_encoding": "UTF-8",
          "confidence": 0.3,
          "suggested_fix": "Sample Text"
        }
      ]
    }
  ],
  "fonts_used": ["Arial", "SimSun"],
  "repair_summary": {
    "total_blocks": 15,
    "fixed_blocks": 12,
    "skipped_blocks": 3
  }
}
```

## 乱码检测规则

该工具使用以下规则来检测乱码：

1. **替换字符检测**：识别U+FFFD（�）和方框字符。
2. **控制字符过滤**：排除非打印控制字符。
3. **编码一致性**：检测由混合编码引起的异常。
4. **字体回退检测**：识别由于缺少字体而生成的替换字符。
5. **概率模型**：根据字符频率评估乱码的可能性。

## 修复策略

### 最小化级别
- 仅修复明显的错误（替换字符、空字节）。
- 最大程度保留原始文本的完整性。
- 适用于轻微的乱码问题。

### 标准级别
- 修复常见的编码问题。
- 智能字体替换。
- 平衡修复速度和准确性。

### 激进级别
- 全面重新编码文本。
- 使用OCR辅助识别。
- 适用于严重损坏的文档。

## 示例

### 修复单页PDF

**输入**：
```bash
python scripts/main.py --input report.pdf --output fixed_report.pdf
```

**输出**：
```
✓ Processing: report.pdf
✓ Detected 5 garbled text blocks
✓ Fixed 4 blocks automatically
⚠ 1 block requires manual review
✓ Output saved: fixed_report.pdf
✓ Report saved: fixed_report_repair_log.json
```

### 导出可编辑的JSON

**输入**：
```bash
python scripts/main.py --input diagram.svg --export-json editable.json
```

**输出JSON结构**：
```json
{
  "file_type": "svg",
  "svg_info": {
    "width": 800,
    "height": 600,
    "viewBox": "0 0 800 600"
  },
  "text_elements": [
    {
      "id": "text_1",
      "x": 100,
      "y": 200,
      "font_family": "Arial",
      "font_size": 14,
      "original": "�����",
      "user_editable": "",
      "confidence": 0.25
    }
  ]
}
```

## 依赖项

```
pdfplumber>=0.10.0      # PDF parsing
PyMuPDF>=1.23.0         # PDF processing (fitz)
cairosvg>=2.7.0         # SVG conversion
beautifulsoup4>=4.12.0  # SVG parsing
fonttools>=4.40.0       # Font processing
chardet>=5.0.0          # Encoding detection
Pillow>=10.0.0          # Image processing
```

## 限制

- 加密PDF需要密码解密后才能处理。
- 严重损坏的矢量文件可能无法完全修复。
- 一些罕见的字体可能无法正确显示。
- 扫描的PDF需要先进行OCR识别。

## 版本信息

- **版本**：1.0.0
- **最后更新时间**：2026-02-06
- **状态**：可用

## 风险评估

| 风险指标 | 评估结果 | 风险等级 |
|----------------|------------|-------|
| 代码执行 | 在本地执行Python/R脚本 | 中等 |
| 网络访问 | 无外部API调用 | 低 |
| 文件系统访问 | 读取输入文件、写入输出文件 | 中等 |
| 指令篡改 | 有标准的提示指南 | 低 |
| 数据泄露 | 输出文件保存在工作区 | 低 |

## 安全检查清单

- [ ] 无硬编码的凭据或API密钥。
- [ ] 无未经授权的文件系统访问。
- [ ] 输出文件不暴露敏感信息。
- [ ] 有防止脚本注入的保护措施。
- [ ] 输入文件路径经过验证（防止遍历上级目录）。
- [ ] 输出目录限制在工作区内。
- [ ] 脚本在沙箱环境中执行。
- [ ] 错误信息经过处理（不显示堆栈跟踪）。
- [ ] 依赖项已审核。

## 先决条件

```bash
# Python dependencies
pip install -r requirements.txt
```

## 评估标准

### 成功指标
- [ ] 成功执行主要功能。
- [ ] 输出符合质量标准。
- [ ] 良好处理边缘情况。
- [ ] 性能可接受。

### 测试用例
1. **基本功能**：标准输入 → 预期输出。
2. **边缘情况**：无效输入 → 良好的错误处理。
3. **性能**：处理大量数据集时 → 处理时间可接受。

## 生命周期状态

- **当前阶段**：草案阶段。
- **下一次审查日期**：2026-03-06。
- **已知问题**：无。
- **计划中的改进**：
  - 性能优化。
  - 支持更多功能。