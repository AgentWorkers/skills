---
name: ocr
description: Optical Character Recognition (OCR) tool, supports Chinese and English text extraction from PDFs and images. Use cases: (1) extract text from scanned PDFs, (2) recognize text from images, (3) extract text content from invoices, contracts, and other documents
---

# OCR文本识别

该技能使用PaddleOCR进行文本识别，支持中文和英文。

## 快速入门

### 基本用法

直接对图像或PDF文件进行OCR识别：

```python
from paddleocr import PaddleOCR

ocr = PaddleOCR(lang='ch')
result = ocr.predict("file_path.jpg")
```

## 依赖项安装

首次使用前，请先安装相关依赖项：

```bash
pip3 install paddlepaddle paddleocr
```

## 输出格式

识别结果以JSON格式返回，包含以下内容：
- `rec_texts`：所有被识别出的文本列表
- `rec_scores`：每段文本的置信度分数

## 典型使用场景

1. **PDF扫描**：先使用PyMuPDF提取图片，再进行OCR识别
2. **图像文本识别**：直接对图像进行OCR处理
3. **多页PDF**：逐页处理

## 脚本

常见的脚本位于`scripts/`目录中。