---
name: image-upscaling
description: "使用 `inference.sh` CLI 命令，通过 Real-ESRGAN、Thera、Topaz 和 FLUX Upscaler 等工具对图像进行放大和优化。支持的模型包括：Real-ESRGAN、Thera（支持任意尺寸）、FLUX Dev Upscaler 和 Topaz Image Upscaler。这些工具可用于提升低分辨率图像的质量、放大 AI 生成的艺术作品、修复旧照片以及提高图像的分辨率。相关操作包括：图像放大、图像优化、分辨率提升等。"
allowed-tools: Bash(infsh *)
---
# 图像放大

通过 [inference.sh](https://inference.sh) 命令行界面（CLI）来放大和优化图像。

![图像放大效果](https://cloud.inference.sh/u/33sqbmzt3mrg2xxphnhw5g5ear/01k8d77p126y82zfecnt46hy4h.png)

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

infsh app run infsh/real-esrgan --input '{"image_url": "https://your-image.jpg"}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可以选择 [手动安装及验证](https://dist.inference.sh/cli/checksums.txt)。

## 可用的图像放大工具

| 模型 | 应用 ID | 适用场景 |
|-------|--------|----------|
| Topaz 图像放大器 | `falai/topaz-image-upscaler` | 专业级质量，适用于所有类型的图像 |

## 示例

### 放大任意图像

```bash
infsh app run falai/topaz-image-upscaler --input '{"image_url": "https://low-res-image.jpg"}'
```

### 工作流程：生成图像 → 放大图像

```bash
# 1. Generate image with FLUX Klein (fast)
infsh app run falai/flux-2-klein-lora --input '{"prompt": "landscape painting"}' > image.json

# 2. Upscale the result
infsh app run falai/topaz-image-upscaler --input '{"image_url": "<url-from-step-1>"}'
```

## 使用场景

- **AI 艺术**：放大生成的图像以用于打印
- **老照片**：恢复并提升图像分辨率
- **网页图像**：为高 DPI 显示屏优化图像
- **打印**：提高大尺寸打印图像的分辨率
- **缩略图**：创建高分辨率的缩略图版本

## 相关技能

```bash
# Full platform skill (all 150+ apps)
npx skills add inference-sh/skills@inference-sh

# Image generation (generate then upscale)
npx skills add inference-sh/skills@ai-image-generation

# FLUX models
npx skills add inference-sh/skills@flux-image

# Background removal
npx skills add inference-sh/skills@background-removal
```

查看所有图像处理工具：`infsh app list --category image`

## 文档资料

- [运行应用程序](https://inference.sh/docs/apps/running) - 如何通过 CLI 运行应用程序
- [图像生成示例](https://inference.sh/docs/examples/image-generation) - 完整的图像处理工作流程指南
- [应用程序概述](https://inference.sh/docs/apps/overview) - 了解应用程序生态系统