---
name: background-removal
description: "使用 `inference.sh` CLI 命令，通过 BiRefNet 模型去除图片中的背景。该模型具有高精度的背景去除能力，适用于以下场景：产品照片、肖像照、电子商务、透明 PNG 图像以及照片编辑。相关命令包括：`remove background`、`background removal`、`remove bg`、`transparent background`、`cut out image`、`background remover`、`rembg`、`product photo editing`、`cutout`、`transparent png`、`bg removal`、`photo cutout`。"
allowed-tools: Bash(infsh *)
---
# 背景去除

通过 [inference.sh](https://inference.sh) 命令行工具（CLI）去除图片中的背景。

![背景去除效果](https://cloud.inference.sh/u/33sqbmzt3mrg2xxphnhw5g5ear/01k8d7y07rpmnv85hz2xvhjvbb.png)

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

infsh app run infsh/birefnet --input '{"image_url": "https://your-photo.jpg"}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可以选择 [手动安装及验证](https://dist.inference.sh/cli/checksums.txt)。

## 使用方法

使用 Reve 进行图片编辑（包括背景替换）：

```bash
infsh app run falai/reve --input '{
  "prompt": "remove the background, make it transparent",
  "image_url": "https://portrait.jpg"
}'
```

或直接更换图片背景：

```bash
infsh app run falai/reve --input '{
  "prompt": "change the background to a beach",
  "image_url": "https://product-photo.jpg"
}'
```

## 工作流程：生成 -> 编辑

```bash
# 1. Generate an image
infsh app run falai/flux-dev-lora --input '{"prompt": "a cute robot mascot"}' > robot.json

# 2. Edit with Reve
infsh app run falai/reve --input '{
  "prompt": "remove background, transparent",
  "image_url": "<url-from-step-1>"
}'
```

## 应用场景

- **电子商务**：清理产品图片
- **肖像**：专业头像
- **市场营销**：设计用图
- **社交媒体**：个人资料图片
- **设计**：用于图片组合的元素

## 输出结果

生成的图片为 PNG 格式，背景为透明。

## 相关技能

```bash
# Full platform skill (all 150+ apps)
npx skills add inference-sh/skills@inference-sh

# Image generation
npx skills add inference-sh/skills@ai-image-generation

# FLUX models (including inpainting)
npx skills add inference-sh/skills@flux-image

# Upscaling
npx skills add inference-sh/skills@image-upscaling
```

查看所有图像处理工具：`infsh app list --category image`

## 文档资料

- [运行应用程序](https://inference.sh/docs/apps/running) - 通过 CLI 运行应用程序的方法
- [图片生成示例](https://inference.sh/docs/examples/image-generation) - 完整的图片处理工作流程指南
- [应用程序概述](https://inference.sh/docs/apps/overview) - 了解应用程序生态系统