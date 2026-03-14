---
slug: muapi-edit
name: muapi-media-editing
version: "0.1.0"
description: 使用 muapi.ai 通过人工智能编辑和优化图片及视频——支持基于提示的编辑、图像放大、背景去除、人脸替换、口型同步、视频效果等功能。
acceptLicenseTerms: true
---
# ✏️ MuAPI 媒体编辑与增强工具

**针对图片和视频的高级编辑与增强功能。**

支持对现有媒体内容应用基于人工智能的编辑、增强效果及特效处理。支持通过 Flux Kontext、GPT-4o 和 Midjourney 等工具进行基于提示的编辑操作，同时提供一键式功能，如图像放大、背景去除等。

## 可用脚本

| 脚本 | 功能描述 |
| :--- | :--- |
| `edit-image.sh` | 基于提示的图片编辑（支持 Flux Kontext、GPT-4o、Midjourney、Qwen 等工具） |
| `enhance-image.sh` | 一键式操作：图像放大、背景去除、人脸替换、上色、日式动画风格处理、产品图片特效 |
| `lipsync.sh` | 将视频中的嘴唇动作与音频同步（支持 Sync Labs、LatentSync、Creatify、Veed 等工具） |
| `video-effects.sh` | 视频/图片特效处理：Wan AI、人脸替换、舞蹈效果、服装更换、Luma 色彩调整/画面裁剪 |

## 快速入门

```bash
# Edit an image with a prompt
bash edit-image.sh --image-url "https://..." --prompt "add sunglasses" --model flux-kontext-pro

# Upscale an image
bash enhance-image.sh --op upscale --image-url "https://..."

# Remove background
bash enhance-image.sh --op background-remove --image-url "https://..."

# Lipsync a video
bash lipsync.sh --video-url "https://..." --audio-url "https://..." --model sync

# Apply dance effect
bash video-effects.sh --op dance --image-url "https://..." --audio-url "https://..."
```

## 常用参数

所有脚本均支持以下参数：`--async`、`--json`、`--timeout N`、`--help`

## 运行要求

- 需设置 `MUAPI_KEY` 环境变量（通过 `core/platform/setup.sh` 脚本配置） |
- 确保系统中安装了 `curl`、`jq` 和 `python3` 工具。