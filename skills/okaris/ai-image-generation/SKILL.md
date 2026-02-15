---
name: ai-image-generation
description: |
  Generate AI images with FLUX, Gemini, Grok, Seedream, Reve and 50+ models via inference.sh CLI.
  Models: FLUX Dev LoRA, FLUX.2 Klein LoRA, Gemini 3 Pro Image, Grok Imagine, Seedream 4.5, Reve, ImagineArt.
  Capabilities: text-to-image, image-to-image, inpainting, LoRA, image editing, upscaling, text rendering.
  Use for: AI art, product mockups, concept art, social media graphics, marketing visuals, illustrations.
  Triggers: flux, image generation, ai image, text to image, stable diffusion, generate image,
  ai art, midjourney alternative, dall-e alternative, text2img, t2i, image generator, ai picture,
  create image with ai, generative ai, ai illustration, grok image, gemini image
allowed-tools: Bash(infsh *)
---

# 人工智能图像生成

通过 [inference.sh](https://inference.sh) 命令行界面（CLI），可以使用 50 多个 AI 模型生成图像。

## 快速入门

```bash
# Install CLI
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate an image with FLUX
infsh app run falai/flux-dev-lora --input '{"prompt": "a cat astronaut in space"}'
```

## 可用的模型

| 模型 | 应用 ID | 适用场景 |
|-------|--------|----------|
| FLUX Dev LoRA | `falai/flux-dev-lora` | 高质量图像，支持自定义风格 |
| FLUX.2 Klein LoRA | `falai/flux-2-klein-lora` | 快速生成图像，支持 LoRA 技术（4B/9B 大小模型） |
| Gemini 3 Pro | `google/gemini-3-pro-image-preview` | Google 最新的图像生成模型 |
| Gemini 2.5 Flash | `google/gemini-2-5-flash-image` | 高性能的 Google 图像生成模型 |
| Grok Imagine | `xai/grok-imagine-image` | xAI 开发的模型，支持多种图像生成效果 |
| Seedream 4.5 | `bytedance/seedream-4-5` | 生成 2K/4K 高质量图像 |
| Seedream 4.0 | `bytedance/seedream-4-0` | 生成高质量 2K/4K 图像 |
| Seedream 3.0 | `bytedance/seedream-3-0-t2i` | 准确的文本渲染功能 |
| Reve | `falai/reve` | 支持自然语言处理和文本渲染 |
| ImagineArt 1.5 Pro | `falai/imagine-art-1-5-pro-preview` | 超高保真度的 4K 图像生成 |
| Topaz Upscaler | `falai/topaz-image-upscaler` | 专业的图像放大工具 |

## 浏览所有图像生成应用

```bash
infsh app list --category image
```

## 示例

### 使用 FLUX 模型将文本转换为图像

```bash
infsh app run falai/flux-dev-lora --input '{
  "prompt": "professional product photo of a coffee mug, studio lighting"
}'
```

### 使用 FLUX Klein 模型快速生成图像

```bash
infsh app run falai/flux-2-klein-lora --input '{"prompt": "sunset over mountains"}'
```

### 使用 Google Gemini 3 Pro 模型生成图像

```bash
infsh app run google/gemini-3-pro-image-preview --input '{
  "prompt": "photorealistic landscape with mountains and lake"
}'
```

### 使用 Grok Imagine 模型生成图像

```bash
infsh app run xai/grok-imagine-image --input '{
  "prompt": "cyberpunk city at night",
  "aspect_ratio": "16:9"
}'
```

### 使用 Reve 模型（包含文本渲染功能）

```bash
infsh app run falai/reve --input '{
  "prompt": "A poster that says HELLO WORLD in bold letters"
}'
```

### 使用 Seedream 4.5 模型生成 4K 质量图像

```bash
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "cinematic portrait of a woman, golden hour lighting"
}'
```

### 图像放大功能

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
npx skills add inference-sh/agent-skills@inference-sh

# FLUX-specific skill
npx skills add inference-sh/agent-skills@flux-image

# Upscaling & enhancement
npx skills add inference-sh/agent-skills@image-upscaling

# Background removal
npx skills add inference-sh/agent-skills@background-removal

# Video generation
npx skills add inference-sh/agent-skills@ai-video-generation

# AI avatars from images
npx skills add inference-sh/agent-skills@ai-avatar-video
```

- 浏览所有可用应用：`infsh app list`

## 文档资料

- [如何运行应用程序](https://inference.sh/docs/apps/running) - 通过 CLI 运行应用程序的指南
- [图像生成示例](https://inference.sh/docs/examples/image-generation) - 完整的图像生成流程说明
- [应用程序概览](https://inference.sh/docs/apps/overview) - 了解整个应用程序生态系统