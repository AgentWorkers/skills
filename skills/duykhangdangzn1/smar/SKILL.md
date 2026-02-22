---
name: smart-ocr
description: 使用 PaddleOCR 从图像和扫描的文档中提取文本——支持 100 多种语言
author: claude-office-skills
version: "1.0"
tags: [ocr, paddleocr, text-extraction, multilingual, image]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: PaddleOCR
  url: https://github.com/PaddlePaddle/PaddleOCR
  stars: 69k
---
# 智能OCR技能

## 概述

该技能利用**PaddleOCR**（一款支持100多种语言的领先OCR引擎）从图片和扫描文档中智能提取文本。能够高精度地从照片、截图、扫描的PDF文件以及手写文档中提取文本。

## 使用方法

1. 提供图片或扫描的文档。
2. （可选）指定需要检测的语言。
3. 系统将提取文本，并附带文本的位置和置信度信息。

**示例指令：**
- “从这张截图中提取所有文本”
- “对这份扫描的PDF文件进行OCR处理”
- “读取这张名片图片中的文本”
- “从这张图片中提取中文和英文文本”

## 领域知识

### PaddleOCR基础

```python
from paddleocr import PaddleOCR

# 初始化OCR引擎
ocr = PaddleOCR/use_angle_cls=True, lang='en')

# 对图片进行OCR处理
result = ocr.ocr('image.png', cls=True)

# 结果结构：[[box, (text, confidence)], ...]
for line in result[0]:
    box = line[0]      # [x1,y1], [x2,y2], [x3,y3], [x4,y4]]
    text = line[1][0]  # 提取的文本
    conf = line[1][1]  # 置信度分数
    print(f"{text} ({conf:.2f})")
```

### 支持的语言

```python
# 常见语言代码
languages = {
    'en': 'English',
    'ch': 'Chinese (Simplified)',
    'cht': 'Chinese (Traditional)',
    'japan': 'Japanese',
    'korean': 'Korean',
    'french': 'French',
    'german': 'German',
    'spanish': 'Spanish',
    'russian': 'Russian',
    'arabic': 'Arabic',
    'hindi': 'Hindi',
    'vi': 'Vietnamese',
    'th': 'Thai',
    # ... 支持100多种语言
}

# 使用特定语言
ocr = PaddleOCR(lang='ch')  # 中文
ocr = PaddleOCR(lang='japan')  # 日文
ocr = PaddleOCR(lang='multilingual')  # 自动检测语言
```

### 配置选项

```python
from paddleocr import PaddleOCR

ocr = PaddleOCR(
    # 检测设置
    det_model_dir=None,         # 自定义检测模型
    det_limit_side_len=960,     # 检测的最大边长
    det_db_thresh=0.3,          # 二值化阈值
    det_db_box_thresh=0.5,      # 盒子得分阈值

    # 识别设置
    rec_model_dir=None,         # 自定义识别模型
    rec_char_dict_path=None,    # 自定义字符字典

    # 角度分类
    use_angle_cls=True,         # 启用角度分类
    cls_model_dir=None,         # 自定义分类模型

    # 语言
    lang='en',                  # 语言代码

    # 性能
    use_gpu=True,               # 如有GPU则使用GPU
    gpu_mem=500,                # GPU内存限制（MB）
    enable_mkldnn=True,         # CPU优化

    # 输出
    show_log=False,             # 抑制日志
)
```

### 处理不同来源的图像

#### 图片文件

```python
# 单张图片
result = ocr.ocr('image.png')

# 多张图片
images = ['img1.png', 'img2.png', 'img3.png']
for img in images:
    result = ocr.ocr(img)
    process_result(result)
```

#### 扫描的PDF文件

```python
from pdf2image import convert_from_path

def ocr_pdf(pdf_path):
    """对扫描的PDF文件进行OCR处理."""
    # 将PDF页面转换为图片
    images = convert_from_path(pdf_path)

    all_text = []
    for i, img in enumerate(images):
        # 保存临时图片
        temp_path = f'temp_page_{i}.png'
        img.save(temp_path)

        # 对图片进行OCR处理
        result = ocr.ocr(temp_path)

        # 提取文本
        page_text = '\n'.join([line[1][0] for line in result[0])
        all_text.append(f"--- 第{i+1}页 ---\n{page_text}")

        # 删除临时文件
        os.remove(temp_path)

    return '\n\n'.join(all_text)
```

#### URL和字节数据

```python
import requests
from io import BytesIO

# 从URL获取图片
response = requests.get('https://example.com/image.png')
result = ocr.ocr(BytesIO(response.content))

# 从字节数据读取图片
with open('image.png', 'rb') as f:
    img_bytes = f.read()
result = ocr.ocr(BytesIO(img_bytes)
```

### 结果处理

```python
def process_ocr_result(result):
    """将OCR结果处理为结构化数据."""
    lines = []
    for line in result[0]:
        box = line[0]
        text = line[1][0]
        confidence = line[1][1]

        # 计算边界框
        x_coords = [p[0] for p in box]
        y_coords = [p[1] for p in box]

        lines.append({
            'text': text,
            'confidence': confidence,
            'bbox': {
                'left': min(x_coords),
                'top': min(y_coords),
                'right': max(x_coords),
                'bottom': max(y_coords),
            },
            'raw_box': box
        })

    # 按位置排序（从上到下，从左到右）
    def sort_by_position(lines):
        return sorted(lines, key=lambda x: (x['bbox']['top'], x['bbox']['left'])

    # 重建文本布局
    def reconstruct_layout(result, line_threshold=10):
        """根据OCR结果重建文本布局."""
        lines = process_ocr_result(result)
        lines = sort_by_position(lines)

        # 将文本按逻辑分组
        text_lines = []
        current_line = []
        current_y = None

        for line in lines:
            y = line['bbox']['top']

            if current_y is None or abs(y - current_y) < line_threshold:
                current_line.append(line)
                current_y = y
            else:
                # 新行
                text_lines.append(' '.join([l['text'] for l in current_line])
                current_line = [line]
                current_y = y

        # 添加最后一行
        if current_line:
            text_lines.append(' '.join([l['text'] for l in current_line])

    return '\n'.join(text_lines)
```

## 最佳实践

1. **预处理图片**：在OCR处理前优化图片质量。
2. **选择正确的语言**：指定语言以提高准确性。
3. **处理多列文本**：分别处理每列文本。
4. **过滤低置信度的结果**：忽略置信度低于设定阈值的结果。
5. **批量处理**：高效处理多张图片。

## 常见技巧

### 图像预处理

```python
from PIL import Image, ImageEnhance, ImageFilter

def preprocess_image(image_path):
    """对图片进行预处理以提高OCR效果."""
    img = Image.open(image_path)

    # 转换为灰度图像
    img = img.convert('L')

    # 提高对比度
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)

    # 锐化图像
    img = img.filter(ImageFilter.SHARPEN)

    # 保存预处理后的图片
    preprocessed_path = 'preprocessed.png'
    img.save(preprocessed_path)
    return preprocessed_path
```

### 并行处理多张图片

```python
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def batch_ocr(image_paths, max_workers=4):
    """并行处理多张图片。"""

    results = {}

    def process_single(img_path):
        result = ocr.ocr(img_path)
        return img_path, result

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_single, p) for p in image_paths]

    for future in tqdm(futures, desc="处理OCR"):
        path, result = future.result()
        results[path] = result

    return results
```

## 示例

### 示例1：名片读取器

```python
from paddleocr import PaddleOCR
import re

def read_business_card(image_path):
    """从名片中提取联系信息."""
    ocr = PaddleOCR/use_angle_cls=True, lang='en')
    result = ocr.ocr(image_path)

    # 提取所有文本
    all_text = []
    for line in result[0]:
        all_text.append(line[1][0])

    full_text = '\n'.join(all_text)

    # 解析联系信息
    contact = {
        'name': None,
        'email': None,
        'phone': None,
        'company': None,
        'title': None,
        'raw_text': full_text
    }

    # 电子邮件匹配
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', full_text)
    if email_match:
        contact['email'] = email_match.group()

    # 电话号码匹配
    phone_match = re.search(r'[\+\d][\d\s\-\(\)]{8,}', full_text)
    if phone_match:
        contact['phone'] = phone_match.group().strip()

    # 名称通常是最长的文本
    if all_text:
        contact['name'] = all_text[0]

    return contact

card_info = read_business_card('business_card.jpg')
print(f"姓名: {card_info['name']}")
print(f"电子邮件: {card_info['email']}")
print(f"电话: {card_info['phone']}")
```

### 示例2：收据扫描

```python
from paddleocr import PaddleOCR
import re

def scanreceipt(image_path):
    """从收据中提取商品信息和总计金额。」
    ocr = PaddleOCR/use_angle_cls=True, lang='en')
    result = ocr.ocr(image_path)

    lines = []
    for line in result[0]:
        text = line[1][0]
        y_pos = line[0][0][1]
        lines.append({'text': text, 'y': y_pos})

    # 按垂直位置排序
    lines.sort(key=lambda x: x['y'])

    receipt = {
        '商品': [],
        '小计': None,
        '税': None,
        '总计': None
    }

    for line in lines:
        text = line['text']

        # 查找总计金额
        if '总计' in text.lower():
            amount = re.search(r'\$?([\d,]+\.?\d*)', text)
            if amount:
                if 'sub' in text.lower():
                    receipt['小计'] = float(amount.group(1).replace(',', '')
                else:
                    receipt['总计'] = float(amount.group(1).replace(',', '')

        # 查找商品信息
        else:
            item_match = re.search(r'(.+?)\s+\$?([\d,]+\.?\d+)$', text)
            if item_match:
                receipt['商品'].append({
                    '名称': item_match.group(1).strip(),
                    '价格': float(item_match.group(2).replace(',', '')
                })

    return receipt

receipt_data = scanreceipt('receipt.jpg')
print(f"商品数量: {len(receipt_data['商品'])}")
print(f"总计金额: ${receipt_data['总计']}")
```

### 示例3：多语言文档

```python
from paddleocr import PaddleOCR

def ocr_multilingual(image_path, languages=['en', 'ch'):
    """对包含多种语言的文档进行OCR处理。」
    all_results = {}

    for lang in languages:
        ocr = PaddleOCR/use_angle_cls=True, lang=lang)
        result = ocr.ocr(image_path)

        texts = []
        for line in result[0]:
            texts.append({
                'text': line[1][0],
                'confidence': line[1][1]
            })

        all_results[lang] = texts

    # 合并结果，保留置信度最高的文本
    merged = {}

    for lang, texts in all_results.items():
        for item in texts:
            text = item['text']
            conf = item['confidence']

            if text not in merged or merged[text]['confidence'] < conf:
                merged[text] = {'confidence': conf, '语言': lang}

    return merged

result = ocr_multilingual('bilingual_document.png')
for text, info in result.items():
    print(f"[{info['语言']}] {text} ({info['confidence']:.2f}")
```

## 局限性

- 手写文本的识别准确性可能不稳定。
- 非常小的文本可能无法被识别。
- 复杂的背景会降低识别效果。
- 旋转的文本需要角度分类才能正确识别。
- 建议使用GPU以获得最佳性能。

## 安装

```bash
# 适用于CPU的版本
pip install paddlepaddle paddleocr

# 适用于GPU的版本（CUDA 11.x）
pip install paddlepaddle-gpu paddleocr

# 额外依赖库
pip install pdf2image Pillow
```

## 资源

- [PaddleOCR GitHub仓库](https://github.com/PaddlePaddle/PaddleOCR)
- [模型库](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/doc/doc_en/models_list_en.md)
- [多语言支持文档](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/doc/doc_en/multi_languages_en.md)