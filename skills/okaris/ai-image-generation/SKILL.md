---
name: ai-image-generation
description: "使用 `inference.sh` CLI 命令，可以通过 FLUX、Gemini、Grok、Seedream、Reve 以及 50 多个其他模型生成 AI 图像。支持的模型包括：FLUX Dev LoRA、FLUX.2 Klein LoRA、Gemini 3 Pro Image、Grok Imagine、Seedream 4.5、Reve 和 ImagineArt。这些模型具备以下功能：文本到图像（text-to-image）、图像到图像（image-to-image）、图像修复（image inpainting）、LoRA 技术、图像编辑、图像放大（image scaling）、文本渲染（text rendering）等。应用场景包括：AI 艺术创作、产品原型设计、概念艺术制作、社交媒体图形设计、营销视觉素材、插图制作等。触发命令包括：`flux`、`image generation`、`ai image`、`text to image`、`stable diffusion`、`generate image`、`ai art`、`midjourney alternative`、`dall-e alternative`、`text2img`、`t2i`、`image generator`、`create image with ai`、`generative ai`、`ai illustration`、`grok image`、`gemini image`。"
allowed-tools: Bash(infsh *)
---
# 人工智能图像生成

通过 [inference.sh](https://inference.sh) 命令行界面（CLI），可以使用 50 多个 AI 模型生成图像。

![人工智能图像生成](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kg0v0nz7wv0qwqjtq1cam52z.jpeg)

## 快速入门

```bash
# Install CLI
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate an image with FLUX
infsh app run falai/flux-dev-lora --input '{"prompt": "a cat astronaut in space"}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可以选择 [手动安装并验证](https://dist.inference.sh/cli/checksums.txt)。

## 可用模型

| 模型 | 应用 ID | 适用场景 |
|-------|--------|----------|
| FLUX Dev LoRA | `falai/flux-dev-lora` | 高质量图像，支持自定义风格 |
| FLUX.2 Klein LoRA | `falai/flux-2-klein-lora` | 快速生成图像，支持 LoRA 算法（4B/9B 数据量） |
| Gemini 3 Pro | `google/gemini-3-pro-image-preview` | Google 最新的图像生成模型 |
| Gemini 2.5 Flash | `google/gemini-2-5-flash-image` | 高效的 Google 图像生成模型 |
| Grok Imagine | `xai/grok-imagine-image` | xAI 开发的模型，支持多方面图像处理 |
| Seedream 4.5 | `bytedance/seedream-4-5` | 生成 2K/4K 质量的图像 |
| Seedream 4.0 | `bytedance/seedream-4-0` | 高质量的 2K/4K 图像生成工具 |
| Seedream 3.0 | `bytedance/seedream-3-0-t2i` | 支持准确的文本渲染 |
| Reve | `falai/reve` | 用于自然语言处理和文本渲染 |
| ImagineArt 1.5 Pro | `falai/imagine-art-1-5-pro-preview` | 超高清 4K 图像生成工具 |
| Topaz Upscaler | `falai/topaz-image-upscaler` | 专业的图像放大工具 |

## 浏览所有图像生成应用

```bash
infsh app list --category image
```

## 示例

### 使用 FLUX 从文本生成图像

```bash
infsh app run falai/flux-dev-lora --input '{
  "prompt": "professional product photo of a coffee mug, studio lighting"
}'
```

### 使用 FLUX Klein 快速生成图像

```bash
infsh app run falai/flux-2-klein-lora --input '{"prompt": "sunset over mountains"}'
```

### 使用 Google Gemini 3 Pro 生成图像

```bash
infsh app run google/gemini-3-pro-image-preview --input '{
  "prompt": "photorealistic landscape with mountains and lake"
}'
```

### 使用 Grok Imagine 生成图像

```bash
infsh app run xai/grok-imagine-image --input '{
  "prompt": "cyberpunk city at night",
  "aspect_ratio": "16:9"
}'
```

### 使用 Reve 生成图像（包含文本渲染功能）

```bash
infsh app run falai/reve --input '{
  "prompt": "A poster that says HELLO WORLD in bold letters"
}'
```

### 使用 Seedream 4.5 生成 4K 质量图像

```bash
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "cinematic portrait of a woman, golden hour lighting"
}'
```

### 图像放大

```bash
infsh app run falai/topaz-image-upscaler --input '{"image_url": "https://..."}'
```

### 合并多张图像

```bash
infsh app run infsh/stitch-images --input '{
  "images": ["https://img1.jpg", "https://img2.jpg"],
  "direction": "horizontal"
}'
```

## 相关技能

```bash
# Full platform skill (all 150+ apps)
npx skills add inference-sh/skills@inference-sh

# FLUX-specific skill
npx skills add inference-sh/skills@flux-image

# Upscaling & enhancement
npx skills add inference-sh/skills@image-upscaling

# Background removal
npx skills add inference-sh/skills@background-removal

# Video generation
npx skills add inference-sh/skills@ai-video-generation

# AI avatars from images
npx skills add inference-sh/skills@ai-avatar-video
```

- 浏览所有可用应用：`infsh app list`

## 文档资料

- [运行应用](https://inference.sh/docs/apps/running) - 如何通过 CLI 运行这些应用
- [图像生成示例](https://inference.sh/docs/examples/image-generation) - 完整的图像生成指南
- [应用概览](https://inference.sh/docs/apps/overview) - 了解整个应用生态系统