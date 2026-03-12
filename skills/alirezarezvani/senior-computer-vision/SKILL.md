---
name: "senior-computer-vision"
description: 计算机视觉工程技能，涵盖对象检测、图像分割以及视觉人工智能系统。内容包括卷积神经网络（CNN）和视觉变换器（Vision Transformer）架构、YOLO/Faster R-CNN/DETR等检测算法、Mask R-CNN/SAM等分割技术，以及使用ONNX/TensorRT进行生产环境部署。涉及PyTorch、vision torchvision、Ultralytics、Detectron2和MMDetection等框架。适用于构建检测流程、训练自定义模型、优化推理性能或部署视觉系统。
---
# 高级计算机视觉工程师

具备用于对象检测、图像分割以及视觉AI系统部署的生产级计算机视觉工程技术。

## 目录

- [快速入门](#quick-start)
- [核心专长](#core-expertise)
- [技术栈](#tech-stack)
- [工作流程1：对象检测流程](#workflow-1-object-detection-pipeline)
- [工作流程2：模型优化与部署](#workflow-2-model-optimization-and-deployment)
- [工作流程3：自定义数据集准备](#workflow-3-custom-dataset-preparation)
- [架构选择指南](#architecture-selection-guide)
- [参考文档](#reference-documentation)
- [常用命令](#common-commands)

## 快速入门

```bash
# Generate training configuration for YOLO or Faster R-CNN
python scripts/vision_model_trainer.py models/ --task detection --arch yolov8

# Analyze model for optimization opportunities (quantization, pruning)
python scripts/inference_optimizer.py model.pt --target onnx --benchmark

# Build dataset pipeline with augmentations
python scripts/dataset_pipeline_builder.py images/ --format coco --augment
```

## 核心专长

本技能涵盖以下方面的指导：

- **对象检测**：YOLO系列（v5-v11）、Faster R-CNN、DETR、RT-DETR
- **实例分割**：Mask R-CNN、YOLOACT、SOLOv2
- **语义分割**：DeepLabV3+、SegFormer、SAM（任意对象分割）
- **图像分类**：ResNet、EfficientNet、视觉Transformer（ViT、DeiT）
- **视频分析**：对象跟踪（ByteTrack、SORT）、动作识别
- **3D视觉**：深度估计、点云处理、NeRF
- **生产级部署**：ONNX、TensorRT、OpenVINO、CoreML

## 技术栈

| 类别 | 技术                |
|----------|-------------------|
| 框架        | PyTorch、torchvision、timm         |
| 检测        | Ultralytics（YOLO）、Detectron2、MMDetection |
| 分割        | segment-anything、mmsegmentation     |
| 优化        | ONNX、TensorRT、OpenVINO、torch.compile   |
| 图像处理      | OpenCV、Pillow、albumentations     |
| 注释        | CVAT、Label Studio、Roboflow       |
| 实验跟踪      | MLflow、Weights & Biases        |
| 服务        | Triton推理服务器、TorchServe       |

## 工作流程1：对象检测流程

当从零开始构建对象检测系统时，请使用此流程。

### 第1步：定义检测需求

分析检测任务的具体要求：

```
Detection Requirements Analysis:
- Target objects: [list specific classes to detect]
- Real-time requirement: [yes/no, target FPS]
- Accuracy priority: [speed vs accuracy trade-off]
- Deployment target: [cloud GPU, edge device, mobile]
- Dataset size: [number of images, annotations per class]
```

### 第2步：选择检测架构

根据需求选择合适的架构：

| 需求                | 推荐架构            | 原因                          |
|------------------|------------------|-----------------------------------------|
| 实时性（>30 FPS）        | YOLOv8/v11、RT-DETR        | 单阶段架构，专为速度优化                |
| 高精度            | Faster R-CNN、DINO         | 双阶段架构，定位更准确                |
| 小对象检测          | YOLO + SAHI、Faster R-CNN + FPN    | 多尺度检测能力                    |
| 边缘设备部署          | YOLOv8n、MobileNetV3-SSD       | 轻量级架构                      |
| 基于Transformer的架构    | DETR、DINO、RT-DETR        | 端到端架构，无需NMS                  |

### 第3步：准备数据集

将注释转换为所需格式：

```bash
# COCO format (recommended)
python scripts/dataset_pipeline_builder.py data/images/ \
    --annotations data/labels/ \
    --format coco \
    --split 0.8 0.1 0.1 \
    --output data/coco/

# Verify dataset
python -c "from pycocotools.coco import COCO; coco = COCO('data/coco/train.json'); print(f'Images: {len(coco.imgs)}, Categories: {len(coco.cats)}')"
```

### 第4步：配置训练环境

生成训练配置文件：

```bash
# For Ultralytics YOLO
python scripts/vision_model_trainer.py data/coco/ \
    --task detection \
    --arch yolov8m \
    --epochs 100 \
    --batch 16 \
    --imgsz 640 \
    --output configs/

# For Detectron2
python scripts/vision_model_trainer.py data/coco/ \
    --task detection \
    --arch faster_rcnn_R_50_FPN \
    --framework detectron2 \
    --output configs/
```

### 第5步：训练和验证模型

```bash
# Ultralytics training
yolo detect train data=data.yaml model=yolov8m.pt epochs=100 imgsz=640

# Detectron2 training
python train_net.py --config-file configs/faster_rcnn.yaml --num-gpus 1

# Validate on test set
yolo detect val model=runs/detect/train/weights/best.pt data=data.yaml
```

### 第6步：评估结果

关键评估指标包括：

| 指标            | 目标值            | 描述                          |
|------------------|------------------|-----------------------------------------|
| mAP@50            | >0.7              | IoU为0.5时的平均精度                  |
| mAP@50:95            | >0.5              | COCO数据集的主要评估指标                |
| 精确度            | >0.8              | 低误报率                      |
| 召回率            | >0.8              | 低漏检率                      |
| 推理时间          | <33ms            | 以实现30 FPS的实时性                  |

## 工作流程2：模型优化与部署

当准备将训练好的模型用于生产环境时，请使用此流程。

### 第1步：基准测试基础性能

```bash
# Measure current model performance
python scripts/inference_optimizer.py model.pt \
    --benchmark \
    --input-size 640 640 \
    --batch-sizes 1 4 8 16 \
    --warmup 10 \
    --iterations 100
```

预期输出：

```
Baseline Performance (PyTorch FP32):
- Batch 1: 45.2ms (22.1 FPS)
- Batch 4: 89.4ms (44.7 FPS)
- Batch 8: 165.3ms (48.4 FPS)
- Memory: 2.1 GB
- Parameters: 25.9M
```

### 第2步：选择优化策略

| 部署目标           | 优化路径                        |
|-------------------|---------------------------|
| NVIDIA GPU（云环境）       | PyTorch → ONNX → TensorRT（FP16）            |
| NVIDIA GPU（边缘设备）       | PyTorch → TensorRT（INT8）            |
| Intel CPU           | PyTorch → OpenVINO                   |
| Apple Silicon       | PyTorch → CoreML                    |
| 通用CPU           | PyTorch → ONNX Runtime                |
| 移动设备           | PyTorch → TFLite或ONNX Mobile             |

### 第3步：将模型导出为ONNX格式

```bash
# Export with dynamic batch size
python scripts/inference_optimizer.py model.pt \
    --export onnx \
    --input-size 640 640 \
    --dynamic-batch \
    --simplify \
    --output model.onnx

# Verify ONNX model
python -c "import onnx; model = onnx.load('model.onnx'); onnx.checker.check_model(model); print('ONNX model valid')"
```

### 第4步：应用量化（可选）

进行INT8量化并校准模型：

```bash
# Generate calibration dataset
python scripts/inference_optimizer.py model.onnx \
    --quantize int8 \
    --calibration-data data/calibration/ \
    --calibration-samples 500 \
    --output model_int8.onnx
```

量化对模型性能的影响分析：

| 精确度            | 处理规模            | 性能提升            | 精确度损失                    |
|------------------|------------------|------------------|----------------------|
| FP32             | 100%               | 不进行量化                     | 无损失                      |
| FP16             | 50%               | 性能提升1.5-2倍                   | 精确度损失<0.5%                 |
| INT8             | 25%               | 性能提升2-4倍                   | 精确度损失1-3%                   |

### 第5步：转换为目标运行时框架

```bash
# TensorRT (NVIDIA GPU)
trtexec --onnx=model.onnx --saveEngine=model.engine --fp16

# OpenVINO (Intel)
mo --input_model model.onnx --output_dir openvino/

# CoreML (Apple)
python -c "import coremltools as ct; model = ct.convert('model.onnx'); model.save('model.mlpackage')"
```

### 第6步：测试优化后的模型

```bash
python scripts/inference_optimizer.py model.engine \
    --benchmark \
    --runtime tensorrt \
    --compare model.pt
```

预期性能提升：

```
Optimization Results:
- Original (PyTorch FP32): 45.2ms
- Optimized (TensorRT FP16): 12.8ms
- Speedup: 3.5x
- Accuracy change: -0.3% mAP
```

## 工作流程3：自定义数据集准备

当需要为训练准备计算机视觉数据集时，请使用此流程。

### 第1步：审核原始数据

```bash
# Analyze image dataset
python scripts/dataset_pipeline_builder.py data/raw/ \
    --analyze \
    --output analysis/
```

分析报告内容包括：

```
Dataset Analysis:
- Total images: 5,234
- Image sizes: 640x480 to 4096x3072 (variable)
- Formats: JPEG (4,891), PNG (343)
- Corrupted: 12 files
- Duplicates: 45 pairs

Annotation Analysis:
- Format detected: Pascal VOC XML
- Total annotations: 28,456
- Classes: 5 (car, person, bicycle, dog, cat)
- Distribution: car (12,340), person (8,234), bicycle (3,456), dog (2,890), cat (1,536)
- Empty images: 234
```

### 第2步：数据清洗与验证

```bash
# Remove corrupted and duplicate images
python scripts/dataset_pipeline_builder.py data/raw/ \
    --clean \
    --remove-corrupted \
    --remove-duplicates \
    --output data/cleaned/
```

### 第3步：转换注释格式

```bash
# Convert VOC to COCO format
python scripts/dataset_pipeline_builder.py data/cleaned/ \
    --annotations data/annotations/ \
    --input-format voc \
    --output-format coco \
    --output data/coco/
```

支持的格式转换包括：

| 来源格式           | 目标格式                         |
|------------------|-----------------------------|
| Pascal VOC XML       | COCO JSON                         |
| YOLO TXT           | COCO JSON                         |
| COCO JSON         | YOLO TXT                         |
| LabelMe JSON         | COCO JSON                         |
| CVAT XML         | COCO JSON                         |

### 第4步：应用数据增强技术

```bash
# Generate augmentation config
python scripts/dataset_pipeline_builder.py data/coco/ \
    --augment \
    --aug-config configs/augmentation.yaml \
    --output data/augmented/
```

推荐用于对象检测的数据增强方法：

```yaml
# configs/augmentation.yaml
augmentations:
  geometric:
    - horizontal_flip: { p: 0.5 }
    - vertical_flip: { p: 0.1 }  # Only if orientation invariant
    - rotate: { limit: 15, p: 0.3 }
    - scale: { scale_limit: 0.2, p: 0.5 }

  color:
    - brightness_contrast: { brightness_limit: 0.2, contrast_limit: 0.2, p: 0.5 }
    - hue_saturation: { hue_shift_limit: 20, sat_shift_limit: 30, p: 0.3 }
    - blur: { blur_limit: 3, p: 0.1 }

  advanced:
    - mosaic: { p: 0.5 }  # YOLO-style mosaic
    - mixup: { p: 0.1 }   # Image mixing
    - cutout: { num_holes: 8, max_h_size: 32, max_w_size: 32, p: 0.3 }
```

### 第5步：划分训练集/验证集/测试集

```bash
python scripts/dataset_pipeline_builder.py data/augmented/ \
    --split 0.8 0.1 0.1 \
    --stratify \
    --seed 42 \
    --output data/final/
```

数据集划分建议：

| 数据集规模          | 训练集 | 验证集 | 测试集                         |
|------------------|------------------|---------------------------|
| <1,000张图片       | 70%           | 15%           | 15%                         |
| 1,000-10,000张图片       | 80%           | 10%           | 10%                         |
| >10,000张图片       | 90%           | 5%           | 5%                         |

### 第6步：生成数据集配置文件

```bash
# For Ultralytics YOLO
python scripts/dataset_pipeline_builder.py data/final/ \
    --generate-config yolo \
    --output data.yaml

# For Detectron2
python scripts/dataset_pipeline_builder.py data/final/ \
    --generate-config detectron2 \
    --output detectron2_config.py
```

## 架构选择指南

### 对象检测架构

| 架构            | 性能（ms） | 精确度（mAP） | 适用场景                         |
|------------------|---------|-----------|-----------------------------------------|
| YOLOv8n         | 1.2ms       | 37.3 mAP       | 边缘设备、移动设备、实时应用                |
| YOLOv8s         | 2.1ms       | 44.9 mAP       | 平衡了速度与精度                   |
| YOLOv8m         | 4.2ms       | 50.2 mAP       | 通用用途                     |
| YOLOv8l         | 6.8ms       | 52.9 mAP       | 高精度应用                     |
| YOLOv8x         | 10.1ms       | 53.9 mAP       | 最高精度应用                   |
| RT-DETR-L         | 5.3ms       | 53.0 mAP       | 基于Transformer的架构，无需NMS               |
| Faster R-CNN R50     | 46ms       | 40.2 mAP       | 双阶段架构，高质量检测                 |
| DINO-4scale       | 85ms       | 49.0 mAP       | 当前最佳性能的Transformer架构           |

### 分割架构

| 架构            | 分割类型         | 性能（ms） | 适用场景                         |
|------------------|-------------|------------------|-----------------------------------------|
| YOLOv8-seg        | 实例分割       | 4.5ms       | 实时实例分割                     |
| Mask R-CNN        | 实例分割       | 67ms       | 高质量掩码生成                   |
| SAM             | 提示式分割       | 50ms       | 零样本分割技术                   |
| DeepLabV3+         | 语义分割       | 25ms       | 场景解析                     |
| SegFormer        | 语义分割       | 15ms       | 高效的语义分割算法                 |

### CNN与视觉Transformer的对比

| 对比项            | CNN（YOLO、R-CNN） | ViT（DETR、DINO）                |
|------------------|------------------|-----------------------------------------|
| 所需训练数据量       | 1K-10K张图片       | 10K-100K+张图片                 |
| 训练时间         | 快速             | 较慢（需要更多训练周期）                 |
| 推理速度         | 更快             | 较慢                         |
| 小对象检测         | 使用FPN效果较好       | 需要多尺度处理                   |
| 全局上下文理解       | 有限             | 强大                         |
| 位置信息编码       | 隐式编码         | 显式编码                     |

## 参考文档
→ 详情请参阅`references/reference-docs-and-commands.md`

## 性能目标

| 指标            | 实时性（FPS）       | 高精度           | 边缘设备适用性                   |
|------------------|-------------|------------------|-----------------------------------------|
| FPS             | >30            | >10            | >15                          |
| mAP@50           | >0.6            | >0.8                          |
| 延迟时间（P99%）      | <50ms          | <150ms                         |
| GPU内存占用       | <4GB           | <8GB           | <2GB                         |
| 模型大小           | <50MB           | <200MB                         | <20MB                         |

## 资源

- **架构指南**：`references/computer_vision_architectures.md`
- **优化指南**：`references/object_detection_optimization.md`
- **部署指南**：`references/production_vision_systems.md`
- **自动化工具**：`scripts/`目录中包含相关脚本