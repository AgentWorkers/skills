---
name: layout-analyzer
description: 使用 surya 分析文档结构和布局——检测文本块、表格以及阅读顺序
author: claude-office-skills
version: "1.0"
tags: [layout, surya, structure, document-analysis, detection]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: surya
  url: https://github.com/VikParuchuri/surya
  stars: 19k
---

# 布局分析技能

## 概述

该技能利用 **surya**（一个先进的文档理解系统）来分析文档的布局。它可以检测文本块、表格、图表、标题，并确定复杂文档中的阅读顺序。

## 使用方法

1. 提供文档的图片或 PDF 文件。
2. 指定需要检测的布局元素。
3. 我将分析文档结构并返回检测到的区域。

**示例提示：**
- “分析此文档页面的布局。”
- “检测此图片中的所有表格和文本块。”
- “确定此 PDF 页面的阅读顺序。”
- “查找此文档中的标题和段落。”

## 领域知识

### surya 基础知识

```python
from surya.detection import DetectionPredictor
from surya.layout import LayoutPredictor
from surya.reading_order import ReadingOrderPredictor
from PIL import Image

# Load image
image = Image.open("document.png")

# Detect layout elements
layout_predictor = LayoutPredictor()
layout_result = layout_predictor([image])
```

### 布局元素类型

| 元素        | 描述                                      |
|-------------|-----------------------------------------|
| 文本        | 普通段落文本                                      |
| 标题        | 文档/章节的标题                                    |
| 节标题       | 节的标题                                      |
| 列表项       | 项目符号/编号列表项                                  |
| 表格        | 表格数据                                      |
| 图表        | 图片/图表                                      |
| 图表标题     | 图表/表格的说明文字                                |
| 脚注        | 文档中的脚注                                    |
| 公式        | 数学公式                                      |
| 页面标题     | 页面顶部或底部的标题                              |
| 页面底部     | 页面底部的注释或信息                              |

### 文本检测

```python
from surya.detection import DetectionPredictor
from PIL import Image

# Initialize detector
detector = DetectionPredictor()

# Load image
image = Image.open("document.png")

# Detect text regions
results = detector([image])

# Access results
for page_result in results:
    for bbox in page_result.bboxes:
        print(f"Text region: {bbox.bbox}")
        print(f"Confidence: {bbox.confidence}")
```

### 布局分析

```python
from surya.layout import LayoutPredictor
from PIL import Image

# Initialize layout predictor
layout_predictor = LayoutPredictor()

# Analyze layout
image = Image.open("document.png")
layout_results = layout_predictor([image])

# Process results
for page_result in layout_results:
    for element in page_result.bboxes:
        print(f"Type: {element.label}")
        print(f"Bbox: {element.bbox}")
        print(f"Confidence: {element.confidence}")
```

### 阅读顺序检测

```python
from surya.reading_order import ReadingOrderPredictor
from surya.layout import LayoutPredictor
from PIL import Image

# Get layout first
layout_predictor = LayoutPredictor()
image = Image.open("document.png")
layout_results = layout_predictor([image])

# Determine reading order
reading_order_predictor = ReadingOrderPredictor()
order_results = reading_order_predictor([image], layout_results)

# Access ordered elements
for page_result in order_results:
    for i, element in enumerate(page_result.ordered_bboxes):
        print(f"{i+1}. {element.label}: {element.bbox}")
```

### 带布局的 OCR 处理

```python
from surya.ocr import OCRPredictor
from surya.layout import LayoutPredictor
from PIL import Image

# Initialize predictors
ocr_predictor = OCRPredictor()
layout_predictor = LayoutPredictor()

# Load image
image = Image.open("document.png")

# Get layout
layout_results = layout_predictor([image])

# Run OCR
ocr_results = ocr_predictor([image])

# Combine results
for layout, ocr in zip(layout_results, ocr_results):
    for layout_elem in layout.bboxes:
        print(f"Element: {layout_elem.label}")
        
        # Find OCR text within this layout element
        for text_line in ocr.text_lines:
            if boxes_overlap(layout_elem.bbox, text_line.bbox):
                print(f"  Text: {text_line.text}")
```

### PDF 文件处理

```python
from surya.layout import LayoutPredictor
from pdf2image import convert_from_path

def analyze_pdf_layout(pdf_path):
    """Analyze layout of all pages in PDF."""
    
    # Convert PDF to images
    images = convert_from_path(pdf_path)
    
    # Initialize predictor
    layout_predictor = LayoutPredictor()
    
    # Analyze all pages
    results = layout_predictor(images)
    
    document_structure = []
    
    for page_num, page_result in enumerate(results):
        page_elements = []
        
        for element in page_result.bboxes:
            page_elements.append({
                'type': element.label,
                'bbox': element.bbox,
                'confidence': element.confidence
            })
        
        document_structure.append({
            'page': page_num + 1,
            'elements': page_elements
        })
    
    return document_structure

structure = analyze_pdf_layout("document.pdf")
```

### 可视化

```python
from surya.layout import LayoutPredictor
from PIL import Image, ImageDraw, ImageFont

def visualize_layout(image_path, output_path):
    """Visualize detected layout elements."""
    
    image = Image.open(image_path)
    layout_predictor = LayoutPredictor()
    results = layout_predictor([image])
    
    # Create drawing context
    draw = ImageDraw.Draw(image)
    
    # Color mapping for element types
    colors = {
        'Text': 'blue',
        'Title': 'red',
        'Table': 'green',
        'Figure': 'purple',
        'Section-header': 'orange',
        'List-item': 'cyan',
    }
    
    for element in results[0].bboxes:
        bbox = element.bbox
        color = colors.get(element.label, 'gray')
        
        # Draw rectangle
        draw.rectangle(bbox, outline=color, width=2)
        
        # Add label
        draw.text((bbox[0], bbox[1] - 15), 
                  f"{element.label} ({element.confidence:.2f})",
                  fill=color)
    
    image.save(output_path)
    return output_path
```

## 最佳实践

1. **使用高清晰度图片**：建议使用 150 DPI 以上的图片以获得最佳效果。
2. **必要时进行预处理**：校正文档的倾斜或旋转。
3. **验证结果**：检查检测到的区域的置信度评分。
4. **处理多页文档**：逐页进行处理。
5. **结合 OCR**：从检测到的区域中提取文本。

## 常见模式

### 文档结构提取

```python
def extract_document_structure(image_path):
    """Extract hierarchical document structure."""
    
    from surya.layout import LayoutPredictor
    from surya.reading_order import ReadingOrderPredictor
    
    image = Image.open(image_path)
    
    # Get layout
    layout_predictor = LayoutPredictor()
    layout_results = layout_predictor([image])
    
    # Get reading order
    order_predictor = ReadingOrderPredictor()
    order_results = order_predictor([image], layout_results)
    
    structure = {
        'title': None,
        'sections': [],
        'tables': [],
        'figures': []
    }
    
    current_section = None
    
    for element in order_results[0].ordered_bboxes:
        if element.label == 'Title':
            structure['title'] = element
        elif element.label == 'Section-header':
            current_section = {'header': element, 'content': []}
            structure['sections'].append(current_section)
        elif element.label == 'Table':
            structure['tables'].append(element)
        elif element.label == 'Figure':
            structure['figures'].append(element)
        elif current_section and element.label in ['Text', 'List-item']:
            current_section['content'].append(element)
    
    return structure
```

### 表格区域提取

```python
def extract_table_regions(image_path):
    """Extract table regions from document."""
    
    from surya.layout import LayoutPredictor
    
    image = Image.open(image_path)
    layout_predictor = LayoutPredictor()
    results = layout_predictor([image])
    
    tables = []
    
    for element in results[0].bboxes:
        if element.label == 'Table':
            bbox = element.bbox
            
            # Crop table region
            table_image = image.crop(bbox)
            
            tables.append({
                'bbox': bbox,
                'image': table_image,
                'confidence': element.confidence
            })
    
    return tables
```

## 示例

### 示例 1：学术论文分析

```python
from surya.layout import LayoutPredictor
from surya.reading_order import ReadingOrderPredictor
from pdf2image import convert_from_path

def analyze_academic_paper(pdf_path):
    """Analyze structure of academic paper."""
    
    images = convert_from_path(pdf_path)
    
    layout_predictor = LayoutPredictor()
    order_predictor = ReadingOrderPredictor()
    
    paper_structure = {
        'pages': [],
        'element_counts': {
            'Title': 0,
            'Section-header': 0,
            'Text': 0,
            'Table': 0,
            'Figure': 0,
            'Formula': 0,
            'Footnote': 0
        }
    }
    
    layout_results = layout_predictor(images)
    order_results = order_predictor(images, layout_results)
    
    for page_num, (layout, order) in enumerate(zip(layout_results, order_results)):
        page_structure = {
            'page': page_num + 1,
            'elements': []
        }
        
        for element in order.ordered_bboxes:
            page_structure['elements'].append({
                'type': element.label,
                'bbox': element.bbox,
                'order': element.position
            })
            
            # Count element types
            if element.label in paper_structure['element_counts']:
                paper_structure['element_counts'][element.label] += 1
        
        paper_structure['pages'].append(page_structure)
    
    return paper_structure

paper = analyze_academic_paper('research_paper.pdf')
print(f"Total tables: {paper['element_counts']['Table']}")
print(f"Total figures: {paper['element_counts']['Figure']}")
```

### 示例 2：表单字段检测

```python
from surya.layout import LayoutPredictor
from PIL import Image

def detect_form_fields(image_path):
    """Detect form fields and labels."""
    
    image = Image.open(image_path)
    
    layout_predictor = LayoutPredictor()
    results = layout_predictor([image])
    
    form_fields = []
    
    for element in results[0].bboxes:
        # Look for text elements that might be labels
        if element.label == 'Text':
            # Check if there's a box/line nearby (potential input field)
            form_fields.append({
                'type': 'potential_label',
                'bbox': element.bbox,
                'confidence': element.confidence
            })
    
    return form_fields

fields = detect_form_fields('form.png')
print(f"Found {len(fields)} potential form elements")
```

### 示例 3：多列文章

```python
from surya.layout import LayoutPredictor
from surya.reading_order import ReadingOrderPredictor
from PIL import Image

def process_multicolumn_article(image_path):
    """Process multi-column article layout."""
    
    image = Image.open(image_path)
    
    layout_predictor = LayoutPredictor()
    order_predictor = ReadingOrderPredictor()
    
    layout_results = layout_predictor([image])
    order_results = order_predictor([image], layout_results)
    
    # Group elements by column
    image_width = image.width
    column_threshold = image_width / 2
    
    columns = {
        'left': [],
        'right': [],
        'full_width': []
    }
    
    for element in order_results[0].ordered_bboxes:
        bbox = element.bbox
        element_center = (bbox[0] + bbox[2]) / 2
        element_width = bbox[2] - bbox[0]
        
        # Determine column
        if element_width > column_threshold * 1.5:
            columns['full_width'].append(element)
        elif element_center < column_threshold:
            columns['left'].append(element)
        else:
            columns['right'].append(element)
    
    return {
        'layout': 'multi-column',
        'columns': columns,
        'reading_order': order_results[0].ordered_bboxes
    }

article = process_multicolumn_article('newspaper_page.png')
print(f"Left column: {len(article['columns']['left'])} elements")
print(f"Right column: {len(article['columns']['right'])} elements")
```

## 限制

- 手写内容的布局可能检测不准确。
- 非常小的文本区域可能会被遗漏。
- 复杂的嵌套布局较难处理。
- 建议使用 GPU 进行批量处理。
- 对多语言的支持程度因版本而异。

## 安装

```bash
pip install surya-ocr

# For PDF processing
pip install pdf2image
```

## 资源

- [surya GitHub 仓库](https://github.com/VikParuchuri/surya)
- [模型文档](https://github.com/VikParuchuri/surya#models)
- [示例代码](https://github.com/VikParuchuri/surya/tree/master/examples)