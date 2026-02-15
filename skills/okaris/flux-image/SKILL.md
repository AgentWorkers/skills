---
name: flux-image
description: |
  Generate images with FLUX models (Black Forest Labs) via inference.sh CLI.
  Models: FLUX Dev LoRA, FLUX.2 Klein LoRA with custom style adaptation.
  Capabilities: text-to-image, image-to-image, LoRA fine-tuning, custom styles.
  Triggers: flux, flux.2, flux dev, flux schnell, flux pro, black forest labs,
  flux image, flux ai, flux model, flux lora
allowed-tools: Bash(infsh *)
---

# FLUX 图像生成

您可以通过 [inference.sh](https://inference.sh) 命令行界面（CLI）使用 FLUX 模型生成图像。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

infsh app run falai/flux-dev-lora --input '{"prompt": "a futuristic city at night"}'
```

## FLUX 模型

| 模型 | 应用 ID | 生成速度 | 图像质量 | 适用场景 |
|-------|--------|-------|---------|----------|
| FLUX Dev LoRA | `falai/flux-dev-lora` | 中等 | 最高画质 | 适用于生产环境及自定义样式 |
| FLUX.2 Klein LoRA | `falai/flux-2-klein-lora` | 生成速度最快 | 图像质量良好 | 适用于快速迭代，支持 4B/9B 大小的图像 |

## 示例

### 高画质生成

```bash
infsh app run falai/flux-dev-lora --input '{
  "prompt": "professional product photo of headphones, studio lighting, white background"
}'
```

### 快速生成（Klein 模型）

```bash
infsh app run falai/flux-2-klein-lora --input '{"prompt": "abstract art, colorful"}'
```

### 使用 LoRA 自定义样式生成图像

```bash
infsh app sample falai/flux-dev-lora --save input.json

# Edit to add lora_url for custom style
infsh app run falai/flux-dev-lora --input input.json
```

### 图像到图像的转换

```bash
infsh app run falai/flux-dev-lora --input '{
  "prompt": "transform to watercolor style",
  "image_url": "https://your-image.jpg"
}'
```

## 其他图像处理任务

```bash
# Image editing with natural language
infsh app run falai/reve --input '{"prompt": "change background to beach"}'

# Upscaling
infsh app run falai/topaz-image-upscaler --input '{"image_url": "https://..."}'
```

## 相关技能

```bash
# Full platform skill (all 150+ apps)
npx skills add inference-sh/agent-skills@inference-sh

# All image generation models
npx skills add inference-sh/agent-skills@ai-image-generation

# Upscaling
npx skills add inference-sh/agent-skills@image-upscaling
```

- 查看所有可用应用：`infsh app list`

## 文档资料

- [运行应用](https://inference.sh/docs/apps/running) - 如何通过 CLI 运行应用
- [图像生成示例](https://inference.sh/docs/examples/image-generation) - 完整的图像生成指南
- [实时进度更新](https://inference.sh/docs/api/sdk/streaming) - 实时进度显示功能