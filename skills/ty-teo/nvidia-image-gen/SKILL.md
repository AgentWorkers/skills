---
name: nvidia-image-gen
version: 1.0.0
description: 使用 NVIDIA FLUX 模型生成和编辑图像。当用户需要生成图像、创建图片、编辑照片或使用人工智能修改现有图像时，可以使用该功能。支持基于文本提示的图像生成和图像编辑。
---

# NVIDIA 图像生成

使用 NVIDIA 的 FLUX 模型生成和编辑图像。

## 模型

| 模型 | 用途 | 速度 | 质量 |
|-------|----------|-------|---------|
| `dev` | 高质量的文本到图像转换 | 中等 | 最佳 |
| `schnell` | 快速的文本到图像转换 | 快速 | 良好 |
| `kontext` | 图像编辑 | 中等 | 最佳 |

## 快速入门

```bash
# Generate an image
python scripts/generate.py "A cute cat in space"

# Edit an existing image
python scripts/generate.py "Add sunglasses" -i photo.jpg -o edited.png
```

## 参数

### 文本到图像（dev/schnell）

| 参数 | 缩写 | 默认值 | 说明 |
|-----------|-------|---------|-------------|
| `prompt` | | （必填） | 文本描述 |
| `-o, --output` | | 输出文件路径 |
| `--width` | | 1024 | 输出图像的宽度（像素） |
| `--height` | | 1024 | 输出图像的高度（像素） |
| `--aspect-ratio` | `-ar` | 1:1 | 宽高比预设 |
| `--steps` | `-s` | 30 | 扩散步骤数 |
| `--seed` | | 0 | 随机种子（0 表示随机生成） |
| `--model` | `-m` | auto | 自动选择模型 |

### 图像编辑（kontext）

| 参数 | 缩写 | 默认值 | 说明 |
|-----------|-------|---------|-------------|
| `prompt` | | （必填） | 编辑指令 |
| `-i, --input` | | （必填） | 输入图像路径 |
| `-o, --output` | | 输出文件路径 |
| `--steps` | `-s` | 30 | 扩散步骤数 |
| `--cfg` | | 3.5 | 指导比例 |
| `--seed` | | 0 | 随机种子 |

## 支持的宽高比

| 宽高比 | 分辨率 |
|-------|------------|
| 1:1 | 1024×1024 |
| 16:9 | 1344×768 |
| 9:16 | 768×1344 |
| 4:3 | 1216×832 |
| 3:4 | 832×1216 |

## 示例

### 基本生成
```bash
python scripts/generate.py "A mountain landscape at sunset"
```

### 宽屏格式（16:9）
```bash
python scripts/generate.py "A panoramic beach view" -ar 16:9
```

### 肖像模式（9:16）
```bash
python scripts/generate.py "A professional headshot" -ar 9:16
```

### 自定义尺寸
```bash
python scripts/generate.py "A banner image" --width 1344 --height 768
```

### 快速生成
```bash
python scripts/generate.py "Quick sketch of a robot" -m schnell
```

### 编辑图像
```bash
python scripts/generate.py "Make the background a sunset" -i input.jpg -o output.png
```

### 可重复的结果
```bash
python scripts/generate.py "A robot" --seed 12345
```

## 输出结果

脚本会将生成的图像输出到 `MEDIA:/path/to/image.png`，可以直接发送到聊天应用中。

## API 密钥

API 密钥已内置于脚本中。如需使用其他密钥，请设置 `NVIDIA_API_KEY` 环境变量。