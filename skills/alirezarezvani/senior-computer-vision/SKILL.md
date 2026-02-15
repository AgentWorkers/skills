---
name: senior-computer-vision
description: 计算机视觉工程技能，专注于目标检测、图像分割和视觉人工智能系统。涵盖卷积神经网络（CNN）与视觉变换器（Vision Transformer）架构，以及YOLO/Faster R-CNN/DETR等目标检测算法、Mask R-CNN/SAM等图像分割技术，并涉及使用ONNX/TensorRT进行系统部署。相关工具包括PyTorch、torchvision、Ultralytics、Detectron2和MMDetection等框架。这些技能适用于构建目标检测流程、训练自定义模型、优化推理性能或部署视觉系统。
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
- **图像分类**：ResNet、EfficientNet、视觉变换器（ViT、DeiT）
- **视频分析**：对象跟踪（ByteTrack、SORT）、动作识别
- **3D视觉**：深度估计、点云处理、NeRF
- **生产环境部署**：ONNX、TensorRT、OpenVINO、CoreML

## 技术栈

| 类别 | 技术                |
|----------|-------------------|
| 框架        | PyTorch、vision torchvision、timm       |
| 检测        | Ultralytics（YOLO）、Detectron2、MMDetection |
| 分割        | segment-anything、mmsegmentation     |
| 优化        | ONNX、TensorRT、OpenVINO、torch.compile   |
| 图像处理      | OpenCV、Pillow、albumentations     |
| 注释        | CVAT、Label Studio、Roboflow       |
| 实验跟踪      | MLflow、Weights & Biases       |
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

| 需求                | 推荐架构                | 原因                          |
|------------------|------------------|-------------------------------------------|
| 实时性（>30 FPS）       | YOLOv8/v11、RT-DETR           | 单阶段架构，优化速度                   |
| 高精度            | Faster R-CNN、DINO           | 双阶段架构，更精确的定位                 |
| 小对象检测        | YOLO + SAHI、Faster R-CNN + FPN     | 多尺度检测                     |
| 边缘设备部署        | YOLOv8n、MobileNetV3-SSD       | 轻量级架构                     |
| 基于Transformer的架构    | DETR、DINO、RT-DETR           | 端到端架构，无需NMS                   |

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

### 第4步：配置训练

生成训练配置：

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

### 第5步：训练与验证

```bash
# Ultralytics training
yolo detect train data=data.yaml model=yolov8m.pt epochs=100 imgsz=640

# Detectron2 training
python train_net.py --config-file configs/faster_rcnn.yaml --num-gpus 1

# Validate on test set
yolo detect val model=runs/detect/train/weights/best.pt data=data.yaml
```

### 第6步：评估结果

关键评估指标：

| 指标        | 目标值                | 描述                          |
|-------------|------------------|-------------------------------------------|
| mAP@50       | >0.7                | IoU为0.5时的平均精度                     |
| mAP@50:95       | >0.5                | COCO主要评估指标                     |
| 精确度        | >0.8                | 低误报率                         |
| 召回率        | >0.8                | 低漏检率                         |
| 推理时间        | <33ms                | 以实现30 FPS的实时性                   |

## 工作流程2：模型优化与部署

当准备将训练好的模型用于生产环境部署时，请使用此流程。

### 第1步：基准测试基线性能

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

| 部署目标        | 优化路径                        |
|-------------------|-------------------------------------------|
| NVIDIA GPU（云端）     | PyTorch → ONNX → TensorRT FP16                |
| NVIDIA GPU（边缘设备）     | PyTorch → TensorRT INT8                   |
| Intel CPU        | PyTorch → OpenVINO                     |
| Apple Silicon     | PyTorch → CoreML                     |
| 通用CPU        | PyTorch → ONNX Runtime                   |
| 移动设备        | PyTorch → TFLite或ONNX Mobile                |

### 第3步：导出为ONNX格式

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

进行INT8量化并校准：

```bash
# Generate calibration dataset
python scripts/inference_optimizer.py model.onnx \
    --quantize int8 \
    --calibration-data data/calibration/ \
    --calibration-samples 500 \
    --output model_int8.onnx
```

量化对性能的影响：

| 精确度        | 大小                  | 速度                      | 精确度下降                      |
|-------------|------------------|-----------------------------------------|
| FP32          | 100%                    | 1倍                         | 0%                          |
| FP16          | 50%                    | 1.5-2倍                         | <0.5%                        |
| INT8          | 25%                    | 2-4倍                         | 1-3%                        |

### 第5步：转换为目标运行时格式

```bash
# TensorRT (NVIDIA GPU)
trtexec --onnx=model.onnx --saveEngine=model.engine --fp16

# OpenVINO (Intel)
mo --input_model model.onnx --output_dir openvino/

# CoreML (Apple)
python -c "import coremltools as ct; model = ct.convert('model.onnx'); model.save('model.mlpackage')"
```

### 第6步：基准测试优化后的模型

```bash
python scripts/inference_optimizer.py model.engine \
    --benchmark \
    --runtime tensorrt \
    --compare model.pt
```

预期加速效果：

```
Optimization Results:
- Original (PyTorch FP32): 45.2ms
- Optimized (TensorRT FP16): 12.8ms
- Speedup: 3.5x
- Accuracy change: -0.3% mAP
```

## 工作流程3：自定义数据集准备

当为训练准备计算机视觉数据集时，请使用此流程。

### 第1步：审核原始数据

```bash
# Analyze image dataset
python scripts/dataset_pipeline_builder.py data/raw/ \
    --analyze \
    --output analysis/
```

分析报告包括：

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

支持的格式转换：

| 来源格式       | 目标格式                     |
|-------------|-------------------------|
| Pascal VOC XML    | COCO JSON                     |
| YOLO TXT       | COCO JSON                     |
| COCO JSON     | YOLO TXT                     |
| LabelMe JSON     | COCO JSON                     |
| CVAT XML     | COCO JSON                     |

### 第4步：应用数据增强

```bash
# Generate augmentation config
python scripts/dataset_pipeline_builder.py data/coco/ \
    --augment \
    --aug-config configs/augmentation.yaml \
    --output data/augmented/
```

推荐的检测数据增强方法：

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

### 第5步：创建训练/验证/测试数据集划分

```bash
python scripts/dataset_pipeline_builder.py data/augmented/ \
    --split 0.8 0.1 0.1 \
    --stratify \
    --seed 42 \
    --output data/final/
```

数据集划分指南：

| 数据集规模       | 训练集 | 验证集 | 测试集                         |
|--------------|--------|--------|---------------------------|
| <1,000张图片     | 70%     | 15%     | 15%                         |
| 1,000-10,000张图片 | 80%     | 10%     | 10%                         |
| >10,000张图片     | 90%     | 5%     | 5%                         |

### 第6步：生成数据集配置

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

| 架构         | 速度        | 精确度      | 最适合的应用场景                   |
|--------------|-----------|-----------|---------------------------|
| YOLOv8n       | 1.2ms     | 37.3 mAP     | 边缘设备、移动设备、实时应用             |
| YOLOv8s       | 2.1ms     | 44.9 mAP     | 平衡速度与精确度                 |
| YOLOv8m       | 4.2ms     | 50.2 mAP     | 通用用途                     |
| YOLOv8l       | 6.8ms     | 52.9 mAP     | 高精度应用                   |
| YOLOv8x       | 10.1ms     | 53.9 mAP     | 最高精度应用                   |
| RT-DETR-L      | 5.3ms     | 53.0 mAP     | 基于Transformer的架构，无需NMS             |
| Faster R-CNN R50    | 46ms     | 40.2 mAP     | 双阶段架构，高质量检测                 |
| DINO-4scale    | 85ms     | 49.0 mAP     | 当前最佳Transformer架构               |

### 分割架构

| 架构         | 类型        | 速度        | 最适合的应用场景                   |
|--------------|-----------|-----------|---------------------------|
| YOLOv8-seg     | 实例分割    | 4.5ms     | 实时实例分割                   |
| Mask R-CNN     | 实例分割    | 67ms     | 高质量掩膜生成                   |
| SAM          | 提示式分割    | 50ms     | 零样本分割技术                   |
| DeepLabV3+      | 语义分割    | 25ms     | 场景解析                     |
| SegFormer     | 语义分割    | 15ms     | 高效语义分割                   |

### CNN与视觉变换器的权衡

| 对比项       | CNN（YOLO、R-CNN） | ViT（DETR、DINO）                |
|-------------|------------------|-----------------------------------------|
| 所需训练数据量    | 1K-10K张图片       | 10K-100K+张图片                 |
| 训练时间      | 快速           | 较慢（需要更多训练周期）                 |
| 推理速度      | 更快           | 较慢                         |
| 小对象检测能力    | 使用FPN时表现良好     | 需要多尺度处理                   |
| 全局上下文理解   | 较有限         | 非常出色                     |
| 位置编码方式    | 隐式编码       | 显式编码                     |

## 参考文档

### 1. 计算机视觉架构

请参阅`references/computer_vision_architectures.md`，了解：

- CNN基础架构（ResNet、EfficientNet、ConvNeXt）
- 视觉变换器变体（ViT、DeiT、Swin）
- 检测头（基于锚点的与无锚点的）
- 特征金字塔网络（FPN、BiFPN、PANet）
- 用于多尺度检测的颈部架构

### 2. 对象检测优化

请参阅`references/object_detection_optimization.md`，了解：

- 非最大值抑制方法（NMS、Soft-NMS、DIoU-NMS）
- 锚点优化及无锚点检测方法
- 损失函数设计（focal loss、GIoU、CIoU、DIoU）
- 训练策略（热身训练、余弦退火、EMA）
- 数据增强方法（mosaic、mixup、copy-paste）

### 3. 生产级视觉系统

请参阅`references/production_vision_systems.md`，了解：

- ONNX导出与优化方法
- TensorRT部署流程
- 批量推理优化
- 边缘设备部署（Jetson、Intel NCS）
- 使用Triton进行模型服务
- 视频处理流程

## 常用命令

### Ultralytics YOLO

```bash
# Training
yolo detect train data=coco.yaml model=yolov8m.pt epochs=100 imgsz=640

# Validation
yolo detect val model=best.pt data=coco.yaml

# Inference
yolo detect predict model=best.pt source=images/ save=True

# Export
yolo export model=best.pt format=onnx simplify=True dynamic=True
```

### Detectron2

```bash
# Training
python train_net.py --config-file configs/COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml \
    --num-gpus 1 OUTPUT_DIR ./output

# Evaluation
python train_net.py --config-file configs/faster_rcnn.yaml --eval-only \
    MODEL.WEIGHTS output/model_final.pth

# Inference
python demo.py --config-file configs/faster_rcnn.yaml \
    --input images/*.jpg --output results/ \
    --opts MODEL.WEIGHTS output/model_final.pth
```

### MMDetection

```bash
# Training
python tools/train.py configs/faster_rcnn/faster-rcnn_r50_fpn_1x_coco.py

# Testing
python tools/test.py configs/faster_rcnn.py checkpoints/latest.pth --eval bbox

# Inference
python demo/image_demo.py demo.jpg configs/faster_rcnn.py checkpoints/latest.pth
```

### 模型优化

```bash
# ONNX export and simplify
python -c "import torch; model = torch.load('model.pt'); torch.onnx.export(model, torch.randn(1,3,640,640), 'model.onnx', opset_version=17)"
python -m onnxsim model.onnx model_sim.onnx

# TensorRT conversion
trtexec --onnx=model.onnx --saveEngine=model.engine --fp16 --workspace=4096

# Benchmark
trtexec --loadEngine=model.engine --batch=1 --iterations=1000 --avgRuns=100
```

## 性能目标

| 指标        | 实时性       | 高精度     | 边缘设备适用性       |
|-------------|-----------|-----------|---------------------------|
| FPS         | >30        | >10         | >15                          |
| mAP@50       | >0.6        | >0.8                          |
| 延迟（P99百分位数） | <50ms       | <150ms                        |
| GPU内存占用    | <4GB        | <8GB                        | <2GB                        |
| 模型大小       | <50MB       | <200MB                        | <20MB                        |

## 资源

- **架构指南**：`references/computer_vision_architectures.md`
- **优化指南**：`references/object_detection_optimization.md`
- **部署指南**：`references/production_vision_systems.md`
- **自动化工具脚本**：`scripts/`目录