---
name: background-removal
description: |
  Remove backgrounds from images with BiRefNet via inference.sh CLI.
  Model: BiRefNet (high accuracy background removal).
  Use for: product photos, portraits, e-commerce, transparent PNGs, photo editing.
  Triggers: remove background, background removal, remove bg, transparent background,
  cut out image, background remover, rembg, product photo editing, cutout,
  transparent png, bg removal, photo cutout
allowed-tools: Bash(infsh *)
---

# 背景去除

通过 [inference.sh](https://inference.sh) 命令行工具（CLI）从图像中去除背景。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

infsh app run infsh/birefnet --input '{"image_url": "https://your-photo.jpg"}'
```

## 使用方法

使用 Reve 进行图像编辑（包括背景替换）：

```bash
infsh app run falai/reve --input '{
  "prompt": "remove the background, make it transparent",
  "image_url": "https://portrait.jpg"
}'
```

或者直接替换背景：

```bash
infsh app run falai/reve --input '{
  "prompt": "change the background to a beach",
  "image_url": "https://product-photo.jpg"
}'
```

## 工作流程：生成与编辑

```bash
# 1. Generate an image
infsh app run falai/flux-dev-lora --input '{"prompt": "a cute robot mascot"}' > robot.json

# 2. Edit with Reve
infsh app run falai/reve --input '{
  "prompt": "remove background, transparent",
  "image_url": "<url-from-step-1>"
}'
```

## 使用场景

- **电子商务**：清理产品图片
- **肖像摄影**：专业头像
- **市场营销**：设计素材
- **社交媒体**：个人资料图片
- **设计**：构图元素

## 输出结果

返回一个背景透明的 PNG 图像。

## 相关技能

```bash
# Full platform skill (all 150+ apps)
npx skills add inference-sh/agent-skills@inference-sh

# Image generation
npx skills add inference-sh/agent-skills@ai-image-generation

# FLUX models (including inpainting)
npx skills add inference-sh/agent-skills@flux-image

# Upscaling
npx skills add inference-sh/agent-skills@image-upscaling
```

浏览所有图像处理工具：`infsh app list --category image`

## 文档资料

- [运行应用程序](https://inference.sh/docs/apps/running) - 如何通过 CLI 运行应用程序
- [图像生成示例](https://inference.sh/docs/examples/image-generation) - 完整的图像处理工作流程指南
- [应用程序概览](https://inference.sh/docs/apps/overview) - 了解应用程序生态系统