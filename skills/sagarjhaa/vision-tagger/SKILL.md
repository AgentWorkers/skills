---
name: vision-tagger
description: 使用 Apple Vision 框架（仅限 macOS）对图像进行标记和注释。该框架能够检测人脸、人体、手部、文本（OCR）、条形码、物体、场景标签以及图像中的显著区域。适用于图像分析、照片标注、姿态监测，或任何需要计算机视觉处理的任务。
homepage: https://clawhub.ai/skills/vision-tagger
metadata: {"clawdbot":{"emoji":"👁️","requires":{"os":"macos","bins":["swiftc","python3"]},"install":[{"id":"xcode","kind":"shell","command":"xcode-select --install","label":"Install Xcode CLI tools"},{"id":"pillow","kind":"shell","command":"pip3 install Pillow","label":"Install Pillow"}]}}
---
# Vision Tagger

这是一个基于苹果Vision框架的macOS原生图像分析工具。所有处理都在本地完成，无需使用云服务或API密钥。

## 系统要求

- macOS 12或更高版本（Monterey或后续版本）
- Xcode命令行工具
- 安装了Pillow库的Python 3

## 首次设置（只需执行一次）

```bash
# Install Xcode CLI tools if needed
xcode-select --install

# Install Pillow
pip3 install Pillow

# Compile the Swift binary
cd scripts/
swiftc -O -o image_tagger image_tagger.swift
```

## 使用方法

### 分析图像 → 生成JSON格式的结果

```bash
./scripts/image_tagger /path/to/photo.jpg
```

输出内容包括：
- **面部特征**：面部边界框、旋转/偏航/俯仰角度、关键点（眼睛、鼻子、嘴巴）
- **身体结构**：18个骨骼关节及其置信度
- **手部特征**：每只手21个关节（左侧/右侧）
- **文本识别**：带有边界框的OCR识别结果
- **场景分类**：图像中的物体类型（如桌子、室外环境、衣物等）
- **条形码识别**：QR码、UPC码等
- **显著性区域**：图像中具有视觉重要性的区域

### 用颜色框标注图像

```bash
python3 scripts/annotate_image.py photo.jpg output.jpg
```

可以使用不同颜色的框来标注图像中的元素：
- 🟢 绿色：面部
- 🟠 橙色：身体骨骼
- 🟣 紫红色：手部
- 🔵 青色：文本区域
- 🟡 黄色：其他矩形物体
- 图像底部会显示场景分类标签

### 与Python的集成

```python
import subprocess, json

def analyze(path):
    r = subprocess.run(['./scripts/image_tagger', path], capture_output=True, text=True)
    return json.loads(r.stdout[r.stdout.find('{'):])

tags = analyze('photo.jpg')
print(tags['labels'])  # [{'label': 'desk', 'confidence': 0.85}, ...]
print(tags['faces'])   # [{'bbox': {...}, 'confidence': 0.99, 'yaw': 5.2}]
```

## 示例JSON输出格式

```json
{
  "dimensions": {"width": 1920, "height": 1080},
  "faces": [{"bbox": {"x": 0.3, "y": 0.4, "width": 0.15, "height": 0.2}, "confidence": 0.99, "roll": -2, "yaw": 5}],
  "bodies": [{"joints": {"head_joint": {"x": 0.5, "y": 0.7, "confidence": 0.9}, "left_shoulder": {...}}, "confidence": 1}],
  "hands": [{"chirality": "left", "joints": {"VNHLKWRI": {"x": 0.4, "y": 0.3, "confidence": 0.85}}}],
  "text": [{"text": "HELLO", "confidence": 0.95, "bbox": {...}}],
  "labels": [{"label": "outdoor", "confidence": 0.88}, {"label": "sky", "confidence": 0.75}],
  "saliency": {"attentionBased": [{"x": 0.2, "y": 0.1, "width": 0.6, "height": 0.8}]}
}
```

## 检测功能

| 检测类型 | 详细信息 |
|---------|---------|
| 面部特征 | 带有边界框的面部信息、置信度、旋转/偏航/俯仰角度、76个关键点 |
| 身体结构 | 18个关节（头部、颈部、肩膀、肘部、手腕、臀部、膝盖、脚踝） |
| 手部特征 | 每只手21个关节（区分左右手） |
| 文本识别 | 带有置信度和边界框的识别文本 |
| 场景分类 | 超过1000种物体/场景类型（如衣物、家具、室外环境等） |
| 条形码识别 | 支持多种条形码格式（QR码、UPC码、EAN码、Code128码、PDF417码、Aztec码、DataMatrix码） |
| 显著性区域 | 基于视觉注意力和物体特征的显著性区域 |

## 应用场景

- **图片标注**：自动为图片添加检测到的物体或场景标签
- **姿态监测**：跟踪面部和身体的位置以评估人体工程学状况
- **文档扫描**：从图片中提取文本
- **安全监控**：检测摄像头画面中的人员
- **辅助阅读**：描述图片中的内容