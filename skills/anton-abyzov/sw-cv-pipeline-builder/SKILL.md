---
name: cv-pipeline-builder
description: |
  Computer vision ML pipelines for image classification, object detection, semantic segmentation, and image generation. Activates for "computer vision", "image classification", "object detection", "CNN", "ResNet", "YOLO", "image segmentation", "image preprocessing", "data augmentation". Builds end-to-end CV pipelines with PyTorch/TensorFlow, integrated with SpecWeave increments.
---

# 计算机视觉管道构建器

## 概述

专为计算机视觉任务设计的机器学习（ML）管道。支持图像预处理、数据增强、卷积神经网络（CNN）架构、迁移学习以及生产环境中的部署。

## 支持的计算机视觉任务

### 1. 图像分类

```python
from specweave import CVPipeline

# Binary or multi-class classification
pipeline = CVPipeline(
    task="classification",
    num_classes=10,
    increment="0042"
)

# Automatically configures:
# - Image preprocessing (resize, normalize)
# - Data augmentation (rotation, flip, color jitter)
# - CNN architecture (ResNet, EfficientNet, ViT)
# - Transfer learning from ImageNet
# - Training loop with validation
# - Inference pipeline

pipeline.fit(train_images, train_labels)
```

### 2. 目标检测

```python
# Detect multiple objects in images
pipeline = CVPipeline(
    task="object_detection",
    classes=["person", "car", "dog", "cat"],
    increment="0042"
)

# Uses: YOLO, Faster R-CNN, or RetinaNet
# Returns: Bounding boxes + class labels + confidence scores
```

### 3. 语义分割

```python
# Pixel-level classification
pipeline = CVPipeline(
    task="segmentation",
    num_classes=21,
    increment="0042"
)

# Uses: U-Net, DeepLab, or SegFormer
# Returns: Segmentation mask for each pixel
```

## 计算机视觉的最佳实践

### 数据增强

```python
from specweave import ImageAugmentation

aug = ImageAugmentation(increment="0042")

# Standard augmentations
aug.add_transforms([
    "random_rotation",  # ±15 degrees
    "random_flip_horizontal",
    "random_brightness",  # ±20%
    "random_contrast",  # ±20%
    "random_crop"
])

# Advanced augmentations
aug.add_advanced([
    "mixup",  # Mix two images
    "cutout",  # Random erasing
    "autoaugment"  # Learned augmentation
])
```

### 迁移学习

```python
# Start from pre-trained ImageNet models
pipeline = CVPipeline(task="classification")

# Option 1: Feature extraction (freeze backbone)
pipeline.use_pretrained(
    model="resnet50",
    freeze_backbone=True
)

# Option 2: Fine-tuning (unfreeze after few epochs)
pipeline.use_pretrained(
    model="resnet50",
    freeze_backbone=False,
    fine_tune_after_epoch=3
)
```

### 模型选择

**图像分类**：
- 小型数据集（<10K样本）：ResNet18、MobileNetV2
- 中型数据集（10K-100K样本）：ResNet50、EfficientNet-B0
- 大型数据集（>100K样本）：EfficientNet-B3、Vision Transformer

**目标检测**：
- 实时检测（>30 FPS）：YOLOv8、SSDLite
- 高精度检测：Faster R-CNN、RetinaNet

**语义分割**：
- 医学成像：U-Net
- 场景分割：DeepLabV3、SegFormer

## 与SpecWeave的集成

```python
# CV increment structure
.specweave/increments/0042-image-classifier/
├── spec.md
├── data/
│   ├── train/
│   ├── val/
│   └── test/
├── models/
│   ├── model-v1.pth
│   └── model-v2.pth
├── experiments/
│   ├── baseline-resnet18/
│   ├── resnet50-augmented/
│   └── efficientnet-b0/
└── deployment/
    ├── onnx_model.onnx
    └── inference.py
```

## 命令

```bash
/ml:cv-pipeline --task classification --model resnet50
/ml:cv-evaluate 0042  # Evaluate on test set
/ml:cv-deploy 0042    # Export to ONNX
```

提供快速设置功能，帮助您构建适用于生产环境的计算机视觉项目。