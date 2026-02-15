---
name: image-upscaling
description: |
  Upscale and enhance images with Real-ESRGAN, Thera, Topaz, FLUX Upscaler via inference.sh CLI.
  Models: Real-ESRGAN, Thera (any size), FLUX Dev Upscaler, Topaz Image Upscaler.
  Use for: enhance low-res images, upscale AI art, restore old photos, increase resolution.
  Triggers: upscale image, image upscaler, enhance image, increase resolution,
  real esrgan, ai upscale, super resolution, image enhancement, upscaling,
  enlarge image, higher resolution, 4k upscale, hd upscale
allowed-tools: Bash(infsh *)
---

# 图像放大

通过 [inference.sh](https://inference.sh) 命令行界面（CLI）来放大和优化图像。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

infsh app run infsh/real-esrgan --input '{"image_url": "https://your-image.jpg"}'
```

## 可用的图像放大工具

| 工具名称 | 应用 ID | 适用场景 |
|---------|---------|---------|
| Topaz Image Upscaler | `falai/topaz-image-upscaler` | 专业品质，适用于任何类型的图像 |

## 示例

### 放大任意图像

```bash
infsh app run falai/topaz-image-upscaler --input '{"image_url": "https://low-res-image.jpg"}'
```

### 工作流程：生成并放大图像

```bash
# 1. Generate image with FLUX Klein (fast)
infsh app run falai/flux-2-klein-lora --input '{"prompt": "landscape painting"}' > image.json

# 2. Upscale the result
infsh app run falai/topaz-image-upscaler --input '{"image_url": "<url-from-step-1>"}'
```

## 使用场景

- **AI艺术创作**：放大生成的图像以用于打印
- **老照片**：恢复并提升图像分辨率
- **网页图像**：为高分辨率显示做准备
- **打印**：提高图像分辨率以适应大幅打印
- **缩略图**：创建高分辨率的缩略图版本

## 相关技能

```bash
# Full platform skill (all 150+ apps)
npx skills add inference-sh/agent-skills@inference-sh

# Image generation (generate then upscale)
npx skills add inference-sh/agent-skills@ai-image-generation

# FLUX models
npx skills add inference-sh/agent-skills@flux-image

# Background removal
npx skills add inference-sh/agent-skills@background-removal
```

查看所有图像处理工具：`infsh app list --category image`

## 文档资料

- [运行应用程序](https://inference.sh/docs/apps/running) - 如何通过 CLI 运行应用程序
- [图像生成示例](https://inference.sh/docs/examples/image-generation) - 完整的图像处理工作流程指南
- [应用程序概述](https://inference.sh/docs/apps/overview) - 了解应用程序生态系统