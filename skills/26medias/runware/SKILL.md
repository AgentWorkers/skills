---
name: runware
description: 通过 Runware API 生成图像和视频。支持使用 FLUX、Stable Diffusion、Kling AI 等顶尖模型。支持文本到图像、图像到图像、图像放大、文本到视频以及图像到视频的转换功能。适用于生成图像、根据提示或现有图像创建视频、放大图像或进行人工智能图像处理等场景。
---

# Runware

通过 Runware 的统一 API 生成图片和视频。支持使用 FLUX、Stable Diffusion XL、Kling AI 等工具。

## 设置

请设置 `RUNWARE_API_KEY` 环境变量，或在脚本中传递 `--api-key` 参数。

获取 API 密钥：https://runware.ai

## 图片生成

### 文本转图片

```bash
python3 scripts/image.py gen "a cyberpunk city at sunset, neon lights, rain" --count 2 -o ./images
```

选项：
- `--model`：模型 ID（默认：`runware:101@1` / FLUX.1 Dev）
- `--width/--height`：图片尺寸（默认：1024x1024）
- `--steps`：推理步骤数（默认：25）
- `--cfg`：CFG 缩放比例（默认：7.5）
- `--count/-n`：生成图片的数量
- `--negative`：负向提示（用于生成负面内容）
- `--seed`：可复制的随机数种子
- `--lora`：LoRA 模型 ID
- `--format`：图片格式（png/jpg/webp）

### 图片转图片（用于修改现有图片）

```bash
python3 scripts/image.py img2img ./photo.jpg "watercolor painting style" --strength 0.7
```

- `--strength`：修改程度（0=保持原图；1=完全替换）

## 图片放大

```bash
python3 scripts/image.py upscale ./small.png --factor 4 -o ./large.png
```

## 模型列表

```bash
python3 scripts/image.py models
```

## 视频生成

### 文本转视频

```bash
python3 scripts/video.py gen "a cat playing with yarn, cute, high quality" --duration 5 -o ./cat.mp4
```

选项：
- `--model`：模型 ID（默认：`klingai:5@3` / Kling AI 1.6 Pro）
- `--duration`：视频时长（秒）
- `--width/--height`：视频分辨率（默认：1920x1080）
- `--negative`：负向提示（用于生成负面内容）
- `--format`：视频格式（mp4/webm/mov）
- `--max-wait`：轮询超时时间（默认：600 秒）

### 图片转视频（用于动画处理或帧间插值）

```bash
# Single image (becomes first frame)
python3 scripts/video.py img2vid ./start.png --prompt "zoom out slowly" -o ./animated.mp4

# Two images (first and last frame)
python3 scripts/video.py img2vid ./start.png ./end.png --duration 5
```

## 视频模型列表

```bash
python3 scripts/video.py models
```

## 热门模型

### 图片模型
| 模型 | ID |
|-------|-----|
| FLUX.1 Dev | `runware:101@1` |
| FLUX.1 Schnell (快速) | `runware:100@1` |
| FLUX.1 Kontext | `runware:106@1` |
| Stable Diffusion XL | `civitai:101055@128080` |
| RealVisXL | `civitai:139562@297320` |

### 视频模型
| 模型 | ID |
|-------|-----|
| Kling AI 1.6 Pro | `klingai:5@3` |
| Kling AI 1.5 Pro | `klingai:3@2` |
| Runway Gen-3 | `runwayml:1@1` |

查看所有模型：https://runware.ai/models

## 注意事项：

- 视频生成是异步的；脚本会持续轮询直到生成完成。
- 不同模型的价格有所不同，请查看：https://runware.ai/pricing
- FLUX 模型生成的图片质量较高；Schnell 模型生成速度更快。
- 为了获得更好的视频效果，请使用包含动作描述的提示语。