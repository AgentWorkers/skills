---
name: openocr-skills
description: 使用 OpenOCR 从图片、文档和扫描的 PDF 文件中提取文本。
  - a lightweight and efficient OCR system with document parsing model requiring
  only 0.1B parameters, capable of running recognition on personal PCs. Supports
  text detection, recognition, universal VLM recognition, and document parsing 
  with layout analysis
author: openocr
version: 0.1.4
tags: [ocr, text-detection, text-recognition, document-parsing, vlm, unirec, 
      layout-analysis, formula, table]
tools: [computer, code_execution, file_operations]
library:
  name: OpenOCR
  url: https://github.com/Topdu/OpenOCR
  stars: 1k+
---

# OpenOCR 技能

## 概述

该技能利用 **OpenOCR**（一个精确且高效的通用 OCR 系统）实现智能文本提取、文档解析和通用识别功能。它提供了一个统一的接口，支持文本检测、文本识别、端到端 OCR 处理、基于 VLM 的通用识别（包括文本、公式和表格）以及带有布局分析的文档解析。支持中文、英文等多种语言。

## 使用方法

1. 提供图像、扫描的文档或 PDF 文件。
2. （可选）指定任务类型（如检测、识别、OCR 或综合识别、文档解析）。
3. 该技能将提取文本中的文字、公式、表格或整个文档的结构。

**示例提示：**
- “从这张图片中提取所有文本。”
- “检测这张照片中的文本区域。”
- “识别截图中的公式。”
- “解析这份带有布局分析的 PDF 文档。”
- “将这张扫描的页面转换为 Markdown 格式。”

## 相关领域知识

### OpenOCR 基础知识
```python
from openocr import OpenOCR

# Initialize with a specific task
engine = OpenOCR(task='ocr')

# Run OCR on an image (callable interface)
results, time_dicts = engine(image_path='image.jpg')

# Results contain detected boxes with recognized text
for result in results:
    for line in result:
        box = line[0]       # Bounding box coordinates
        text = line[1][0]   # Recognized text
        conf = line[1][1]   # Confidence score
        print(f"{text} ({conf:.2f})")
```

### 支持的任务类型
```python
# Available task types
tasks = {
    'det':    'Text Detection - detect text regions with bounding boxes',
    'rec':    'Text Recognition - recognize text from cropped images',
    'ocr':    'End-to-End OCR - detection + recognition pipeline',
    'unirec': 'Universal Recognition - VLM-based text/formula/table recognition (0.1B params)',
    'doc':    'Document Parsing - layout analysis + universal recognition (0.1B params)',
}

# Task selection via parameter
det_engine = OpenOCR(task='det')
rec_engine = OpenOCR(task='rec')
ocr_engine = OpenOCR(task='ocr')
unirec_engine = OpenOCR(task='unirec')
doc_engine = OpenOCR(task='doc')
```

### 配置选项
```python
from openocr import OpenOCR

# === Text Detection ===
detector = OpenOCR(
    task='det',
    backend='onnx',                          # 'onnx' (default) or 'torch'
    onnx_det_model_path=None,                # Custom detection model (auto-downloads if None)
    use_gpu='auto',                          # 'auto', 'true', or 'false'
)

# === Text Recognition ===
recognizer = OpenOCR(
    task='rec',
    mode='mobile',                           # 'mobile' (fast) or 'server' (accurate)
    backend='onnx',                          # 'onnx' (default) or 'torch'
    onnx_rec_model_path=None,                # Custom recognition model
    use_gpu='auto',
)

# === End-to-End OCR ===
ocr = OpenOCR(
    task='ocr',
    mode='mobile',                           # 'mobile' or 'server'
    backend='onnx',                          # 'onnx' or 'torch'
    onnx_det_model_path=None,                # Custom detection model
    onnx_rec_model_path=None,                # Custom recognition model
    drop_score=0.5,                          # Confidence threshold for filtering
    det_box_type='quad',                     # 'quad' or 'poly' (for curved text)
    use_gpu='auto',
)

# === Universal Recognition (UniRec) ===
unirec = OpenOCR(
    task='unirec',
    unirec_encoder_path=None,                # Custom encoder ONNX model
    unirec_decoder_path=None,                # Custom decoder ONNX model
    tokenizer_mapping_path=None,             # Custom tokenizer mapping JSON
    max_length=2048,                         # Max generation length
    auto_download=True,                      # Auto-download missing models
    use_gpu='auto',
)

# === Document Parsing (OpenDoc) ===
doc = OpenOCR(
    task='doc',
    layout_model_path=None,                  # Custom layout detection model (PP-DocLayoutV2)
    unirec_encoder_path=None,                # Custom UniRec encoder
    unirec_decoder_path=None,                # Custom UniRec decoder
    tokenizer_mapping_path=None,             # Custom tokenizer mapping
    layout_threshold=0.5,                    # Layout detection threshold
    use_layout_detection=True,               # Enable layout analysis
    max_parallel_blocks=4,                   # Max parallel VLM blocks
    auto_download=True,                      # Auto-download missing models
    use_gpu='auto',
)
```

### 任务特定用法

#### 文本检测
```python
from openocr import OpenOCR

detector = OpenOCR(task='det', backend='onnx')

# Detect text regions
results = detector(image_path='image.jpg')

boxes = results[0]['boxes']      # np.ndarray of bounding boxes
elapse = results[0]['elapse']    # Processing time in seconds

print(f"Found {len(boxes)} text regions in {elapse:.3f}s")
for box in boxes:
    print(f"  Box: {box.tolist()}")
```

#### 文本识别
```python
from openocr import OpenOCR

# Mobile mode (fast, ONNX)
recognizer = OpenOCR(task='rec', mode='mobile', backend='onnx')

# Server mode (accurate, requires torch)
# recognizer = OpenOCR(task='rec', mode='server', backend='torch')

results = recognizer(image_path='word.jpg', batch_num=1)

text = results[0]['text']        # Recognized text string
score = results[0]['score']      # Confidence score
elapse = results[0]['elapse']    # Processing time

print(f"Text: {text}, Score: {score:.3f}, Time: {elapse:.3f}s")
```

#### 端到端 OCR 处理
```python
from openocr import OpenOCR

ocr = OpenOCR(task='ocr', mode='mobile', backend='onnx')

# Run OCR with visualization
results, time_dicts = ocr(
    image_path='image.jpg',
    save_dir='./output',
    is_visualize=True,
    rec_batch_num=6,
)

# Process results
for result in results:
    for line in result:
        box, (text, confidence) = line[0], line[1]
        print(f"{text} ({confidence:.2f})")
```

#### 通用识别（UniRec）
```python
from openocr import OpenOCR

unirec = OpenOCR(task='unirec')

# Image input
result_text, generated_ids = unirec(image_path='formula.jpg', max_length=2048)
print(f"Result: {result_text}")

# PDF input (returns list of tuples, one per page)
results = unirec(image_path='document.pdf', max_length=2048)
for page_text, page_ids in results:
    print(f"Page: {page_text[:100]}...")
```

#### 文档解析（OpenDoc）
```python
from openocr import OpenOCR

doc = OpenOCR(task='doc', use_layout_detection=True)

# Parse a document image
result = doc(image_path='document.jpg')

# Save outputs in multiple formats
doc.save_to_markdown(result, './output')
doc.save_to_json(result, './output')
doc.save_visualization(result, './output')

# Parse a PDF (returns list of dicts, one per page)
results = doc(image_path='document.pdf')
for page_result in results:
    doc.save_to_markdown(page_result, './output')
```

### 命令行接口
```bash
# Text Detection
openocr --task det --input_path image.jpg --is_vis

# Text Recognition
openocr --task rec --input_path word.jpg --mode server --backend torch

# End-to-End OCR
openocr --task ocr --input_path image.jpg --is_vis --output_path ./results

# Universal Recognition
openocr --task unirec --input_path formula.jpg --max_length 2048

# Document Parsing
openocr --task doc --input_path document.pdf \
    --use_layout_detection --save_vis --save_json --save_markdown

# Launch Gradio Demos
openocr --task launch_openocr_demo --share --server_port 7860
openocr --task launch_unirec_demo --share --server_port 7861
openocr --task launch_opendoc_demo --share --server_port 7862
```

### 处理不同类型的输入数据

#### 图像文件
```python
from openocr import OpenOCR

ocr = OpenOCR(task='ocr')

# Single image
results, _ = ocr(image_path='image.jpg')

# Directory of images
results, _ = ocr(image_path='./images/', save_dir='./output', is_visualize=True)
```

#### PDF 文件
```python
from openocr import OpenOCR

# UniRec handles PDFs natively
unirec = OpenOCR(task='unirec')
results = unirec(image_path='document.pdf', max_length=2048)

# OpenDoc handles PDFs natively with layout analysis
doc = OpenOCR(task='doc', use_layout_detection=True)
results = doc(image_path='document.pdf')

# Save each page
for page_result in results:
    doc.save_to_markdown(page_result, './output')
    doc.save_to_json(page_result, './output')
```

#### Numpy 数组输入
```python
import cv2
from openocr import OpenOCR

ocr = OpenOCR(task='ocr')

# Read image as numpy array
img = cv2.imread('image.jpg')

# Pass numpy array directly
results, _ = ocr(img_numpy=img)
```

### 结果格式
```python
# Detection result format
det_result = [{'boxes': np.ndarray, 'elapse': float}]

# Recognition result format
rec_result = [{'text': str, 'score': float, 'elapse': float}]

# OCR result format (detection + recognition)
ocr_result = (results_list, time_dicts)
# results_list: [[[box, (text, confidence)], ...], ...]

# UniRec result format
# Image: (text: str, generated_ids: list)
# PDF:   [(text: str, generated_ids: list), ...]  # one per page

# Doc result format
# Image: dict with layout blocks and recognized content
# PDF:   [dict, ...]  # one per page
```

## 最佳实践

1. **选择合适的任务类型**：使用 `ocr` 处理普通文本，`unirec` 处理公式和表格，`doc` 处理完整文档。
2. **使用移动模式以提高速度**：`mode='mobile'` 速度更快；仅在需要高精度时使用 `mode='server'`。
3. **使用 ONNX 后端**：默认的 ONNX 后端可在 CPU 上运行，无需额外依赖。
4. **设置合适的阈值**：根据实际需求调整 `drop_score`（OCR）和 `layout_threshold`（文档解析）。
5. **启用布局检测**：对于包含文本、公式和表格的混合文档，务必启用 `use_layout_detection`。
6. **批量处理**：使用 `rec_batch_num` 控制批处理数量以优化处理效率。
7. **利用 GPU 加速**：安装 `onnxruntime-gpu` 或带有 CUDA 的 PyTorch 可显著提升性能。

## 常见应用场景

### 完整文档处理流程
```python
from openocr import OpenOCR
import os

def process_documents(input_dir, output_dir):
    """Process all documents in a directory."""
    doc = OpenOCR(task='doc', use_layout_detection=True)

    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.jpg', '.png', '.pdf', '.bmp')):
            filepath = os.path.join(input_dir, filename)
            print(f"Processing: {filename}")

            result = doc(image_path=filepath)

            # Handle PDF (list) vs image (dict)
            if isinstance(result, list):
                for page_result in result:
                    doc.save_to_markdown(page_result, output_dir)
                    doc.save_to_json(page_result, output_dir)
            else:
                doc.save_to_markdown(result, output_dir)
                doc.save_to_json(result, output_dir)

    print(f"All results saved to {output_dir}")

process_documents('./docs', './output')
```

### 带有自定义后处理的 OCR 处理
```python
from openocr import OpenOCR
import re

def extract_structured_text(image_path, drop_score=0.5):
    """Extract and structure text from an image."""
    ocr = OpenOCR(task='ocr', drop_score=drop_score)
    results, _ = ocr(image_path=image_path)

    lines = []
    for result in results:
        for line in result:
            box = line[0]
            text = line[1][0]
            confidence = line[1][1]

            # Calculate bounding box center
            y_center = sum(p[1] for p in box) / 4

            lines.append({
                'text': text,
                'confidence': confidence,
                'y_center': y_center,
                'box': box,
            })

    # Sort by vertical position (top to bottom)
    lines.sort(key=lambda x: x['y_center'])

    return lines

result = extract_structured_text('page.jpg')
for line in result:
    print(f"{line['text']} ({line['confidence']:.2f})")
```

### 公式识别
```python
from openocr import OpenOCR

def recognize_formula(image_path):
    """Recognize mathematical formula from image."""
    unirec = OpenOCR(task='unirec')
    text, ids = unirec(image_path=image_path, max_length=2048)

    # UniRec outputs LaTeX for formulas
    print(f"LaTeX: {text}")
    return text

latex = recognize_formula('formula.png')
# Output: \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
```

### 表格提取
```python
from openocr import OpenOCR

def extract_table(image_path):
    """Extract table content from image."""
    unirec = OpenOCR(task='unirec')
    text, ids = unirec(image_path=image_path, max_length=2048)

    # UniRec outputs LaTeX table format
    print(f"Table: {text}")
    return text

table_latex = extract_table('table.png')
```

## 示例

### 示例 1：批量 OCR 处理并显示进度
```python
from openocr import OpenOCR
import os

def batch_ocr(image_dir, output_dir='./ocr_results'):
    """OCR all images in a directory."""
    ocr = OpenOCR(task='ocr', mode='mobile')

    os.makedirs(output_dir, exist_ok=True)

    image_files = [
        f for f in os.listdir(image_dir)
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff'))
    ]

    all_results = {}
    for i, filename in enumerate(image_files):
        filepath = os.path.join(image_dir, filename)
        print(f"[{i+1}/{len(image_files)}] Processing: {filename}")

        results, time_dicts = ocr(
            image_path=filepath,
            save_dir=output_dir,
            is_visualize=True,
        )

        texts = []
        for result in results:
            for line in result:
                texts.append(line[1][0])

        all_results[filename] = texts
        print(f"  Found {len(texts)} text lines")

    # Save all text
    with open(os.path.join(output_dir, 'all_text.txt'), 'w') as f:
        for filename, texts in all_results.items():
            f.write(f"--- {filename} ---\n")
            f.write('\n'.join(texts))
            f.write('\n\n')

    return all_results

results = batch_ocr('./images')
```

### 示例 2：将文档转换为 Markdown 格式
```python
from openocr import OpenOCR
import os

def doc_to_markdown(input_path, output_dir='./markdown_output'):
    """Convert document images or PDFs to Markdown."""
    doc = OpenOCR(
        task='doc',
        use_layout_detection=True,
        use_chart_recognition=True,
    )

    os.makedirs(output_dir, exist_ok=True)

    result = doc(image_path=input_path)

    if isinstance(result, list):
        # PDF: multiple pages
        for page_result in result:
            doc.save_to_markdown(page_result, output_dir)
        print(f"Converted {len(result)} pages to Markdown")
    else:
        # Single image
        doc.save_to_markdown(result, output_dir)
        print("Converted image to Markdown")

    print(f"Output saved to: {output_dir}")

# Convert a scanned PDF
doc_to_markdown('paper.pdf')

# Convert a document image
doc_to_markdown('page.jpg')
```

### 示例 3：多任务处理对比
```python
from openocr import OpenOCR

def compare_tasks(image_path):
    """Compare results from different OpenOCR tasks."""

    # 1. Detection only
    det = OpenOCR(task='det')
    det_result = det(image_path=image_path)
    num_boxes = len(det_result[0]['boxes'])
    print(f"Detection: Found {num_boxes} text regions")

    # 2. End-to-End OCR
    ocr = OpenOCR(task='ocr')
    ocr_results, _ = ocr(image_path=image_path)
    ocr_texts = [line[1][0] for result in ocr_results for line in result]
    print(f"OCR: Extracted {len(ocr_texts)} text lines")
    for t in ocr_texts[:5]:
        print(f"  - {t}")

    # 3. Universal Recognition
    unirec = OpenOCR(task='unirec')
    text, _ = unirec(image_path=image_path)
    print(f"UniRec: {text[:200]}...")

    return {
        'det_boxes': num_boxes,
        'ocr_texts': ocr_texts,
        'unirec_text': text,
    }

compare_tasks('document.jpg')
```

### 示例 4：使用 Gradio 进行演示
```python
from openocr import launch_openocr_demo, launch_unirec_demo, launch_opendoc_demo

# Launch OCR demo
launch_openocr_demo(share=True, server_port=7860, server_name='0.0.0.0')

# Launch UniRec demo
launch_unirec_demo(share=True, server_port=7861)

# Launch OpenDoc demo
launch_opendoc_demo(share=True, server_port=7862)
```

## 限制因素

- 文本识别精度受图像质量影响。
- 非常小或严重旋转的文本可能导致识别精度下降。
- `server` 模式需要 PyTorch，且速度较 `mobile` 模式慢。
- UniRec 和 Doc 任务使用 0.1B 大小的 VLM 模型，更大模型可能获得更好的识别效果。
- PDF 处理过程会将页面转换为图像格式，大型 PDF 文件可能会占用大量内存。
- 复杂的手写文本识别效果可能不稳定。
- 建议使用 GPU 以获得最佳性能，尤其是对于 Doc 和 UniRec 任务。

## 安装方法
```bash
# Basic installation (CPU, ONNX backend)
pip install openocr-python

# GPU-accelerated ONNX inference
pip install openocr-python[onnx-gpu]

# PyTorch backend (for server mode)
pip install openocr-python[pytorch]

# Gradio demos
pip install openocr-python[gradio]

# All optional dependencies
pip install openocr-python[all]

# From source
git clone https://github.com/Topdu/OpenOCR.git
cd OpenOCR
python build_package.py
pip install ./build/dist/openocr_python-*.whl
```

## 参考资源

- [OpenOCR GitHub 仓库](https://github.com/Topdu/OpenOCR)
- [PyPI 包](https://pypi.org/project/openocr-python/)
- [UniRec 项目文档](https://github.com/Topdu/OpenOCR#unirec)
- [OpenDoc 文档](https://github.com/Topdu/OpenOCR#opendoc)
- [模型库及配置文件](https://github.com/Topdu/OpenOCR/tree/main/configs)