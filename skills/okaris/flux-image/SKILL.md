---
name: flux-image
description: "使用 `inference.sh` CLI 命令通过 FLUX 模型（Black Forest Labs）生成图像。支持的模型包括：FLUX Dev LoRA、FLUX.2 Klein LoRA，以及支持自定义风格适配的版本。功能包括：文本到图像、图像到图像的转换；LoRA 模型的微调；以及自定义图像风格的应用。触发命令包括：`flux`、`flux.2`、`flux dev`、`flux schnell`、`flux pro`、`black forest labs`、`flux image`、`flux ai`、`flux model`、`flux lora`。"
allowed-tools: Bash(infsh *)
---
# FLUX 图像生成

您可以使用 [inference.sh](https://inference.sh) 命令行工具，通过 FLUX 模型生成图像。

![FLUX 图像生成](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kg0v0nz7wv0qwqjtq1cam52z.jpeg)

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

infsh app run falai/flux-dev-lora --input '{"prompt": "a futuristic city at night"}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需提升权限或启动后台进程。也可以选择[手动安装并验证](https://dist.inference.sh/cli/checksums.txt)。

## FLUX 模型

| 模型 | 应用 ID | 速度 | 图像质量 | 使用场景 |
|-------|--------|-------|---------|----------|
| FLUX Dev LoRA | `falai/flux-dev-lora` | 中等 | 最高画质 | 适用于生产环境及自定义样式 |
| FLUX.2 Klein LoRA | `falai/flux-2-klein-lora` | 最快 | 图像质量良好 | 适用于快速迭代，支持 4B/9B 大小的图像生成 |

## 示例

### 高质量图像生成

```bash
infsh app run falai/flux-dev-lora --input '{
  "prompt": "professional product photo of headphones, studio lighting, white background"
}'
```

### 快速生成（Klein 模型）

```bash
infsh app run falai/flux-2-klein-lora --input '{"prompt": "abstract art, colorful"}'
```

### 使用 LoRA 模型生成自定义样式的图像

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
npx skills add inference-sh/skills@inference-sh

# All image generation models
npx skills add inference-sh/skills@ai-image-generation

# Upscaling
npx skills add inference-sh/skills@image-upscaling
```

- 查看所有可用应用：`infsh app list`

## 文档说明

- [运行应用](https://inference.sh/docs/apps/running) - 如何通过命令行运行应用
- [图像生成示例](https://inference.sh/docs/examples/image-generation) - 完整的图像生成指南
- [实时进度更新](https://inference.sh/docs/api/sdk/streaming) - 实时显示处理进度