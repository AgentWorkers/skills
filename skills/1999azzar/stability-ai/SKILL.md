---
name: stability-ai
description: 通过 Stability AI API（SDXL、SD3、Stable Image Core）生成高质量图像。当用户请求“生成图像”、“制作图片”或“绘制这个内容”时，可以使用该功能。
---

# Stability AI 技能

## 设置
1. 将 `.env.example` 复制到 `.env` 文件中。
2. 在 `.env` 文件中设置 `STABILITY_API_KEY`。
3. （可选）如果使用自定义端点，请设置 `API_HOST`。

## 使用方法
- **角色**：数字艺术家。
- **触发指令**：例如：“画一只猫”、“生成赛博朋克城市”、“创建一张图片”。
- **输出**：生成的图片的本地文件路径以及 JSON 格式的元数据。

## 命令
（脚本在首次运行时会自动处理依赖关系）

```bash
# Basic generation
scripts/generate "A futuristic city with neon lights"

# Aspect ratio (1:1, 16:9, 9:16, 21:9, 4:3, 3:4)
scripts/generate "Landscape painting" --ratio 16:9

# Style preset
scripts/generate "Portrait of a warrior" --style photographic

# Seed for reproducibility
scripts/generate "Abstract art" --seed 42

# Negative prompt
scripts/generate "Beautiful sunset" --negative "blurry, low quality"

# Output format (png, jpg, webp)
scripts/generate "Nature scene" --format webp

# Advanced: Custom model, steps, CFG scale
scripts/generate "Fantasy landscape" \
  --model stable-diffusion-3-medium \
  --steps 50 \
  --cfg 7.0 \
  --ratio 21:9

# V2 API (experimental)
scripts/generate "Modern architecture" --v2

# Combined options
scripts/generate "Cyberpunk street at night" \
  --ratio 16:9 \
  --style neon-punk \
  --seed 123 \
  --format jpg \
  --steps 45 \
  --cfg 6.5
```

## 功能

### 风格预设
可选的风格包括：enhance、anime、photographic、digital-art、comic-book、fantasy-art、line-art、analog-film、neon-punk、isometric、low-poly、origami、modeling-compound、cinematic、3d-model、pixel-art、tile-texture

### 宽高比
支持的宽高比：1:1（默认）、16:9、9:16、21:9、4:3、3:4

### 输出格式
- PNG（默认格式，无损压缩）
- JPEG/JPG（有损压缩，文件体积较小）
- WebP（现代格式，压缩效率高）

### 元数据
每张生成的图片都会附带一个 JSON 格式的元数据文件，其中包含：
- 用户输入的提示语（prompt）和否定提示语（negative prompt）
- 使用的模型、参数及设置信息
- 生成时间戳
- 所使用的 API 版本

## 模型
- 默认模型：SDXL 1.0 (`stable-diffusion-xl-1024-v1-0`)
- 有关完整模型列表、API 版本及使用费用的信息，请参阅 `references/models.md`。

## 自动清理
系统会自动保留最近生成的 20 张图片。旧的图片及其元数据会被删除，以节省磁盘空间。