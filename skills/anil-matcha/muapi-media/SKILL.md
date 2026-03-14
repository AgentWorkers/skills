---
slug: muapi-media
name: muapi-media-generation
version: "0.1.0"
description: 通过 muapi.ai，您可以在终端中生成 AI 图像、视频、音乐和音频。该工具支持 100 多种模型，包括 Flux、Midjourney v7、Kling 3.0、Veo3 和 Suno V5。
acceptLicenseTerms: true
---
# 🎨 MuAPI 媒体生成工具

**基于模式的图像、视频和音频生成功能**

您可以直接在终端中使用 100 多种最先进的 AI 模型来生成专业级别的媒体文件。所有脚本均依赖于 `schema_data.json` 文件，以实现动态的模型选择和端点配置。

## 可用的脚本

| 脚本 | 描述 | 默认模型 |
| :--- | :--- | :--- |
| `generate-image.sh` | 文本转图像生成 | `flux-dev` |
| `generate-video.sh` | 文本转视频生成 | `minimax-pro` |
| `image-to-video.sh` | 将静态图像转换为视频 | `kling-pro` |
| `create-music.sh` | 音乐创作、混音、扩展功能；支持文本/视频转音频 | Suno V5 |
| `upload.sh` | 将本地文件上传到 CDN，以便与其他工具一起使用 | — |

## 快速入门

```bash
# Generate an image
bash generate-image.sh --prompt "a sunset over mountains" --model flux-dev --view

# Generate a video
bash generate-video.sh --prompt "ocean waves at golden hour" --model minimax-pro --view

# Animate an image
bash image-to-video.sh --image-url "https://..." --prompt "camera slowly pans right" --model kling-pro

# Create music
bash create-music.sh --style "lo-fi hip hop" --prompt "chill beats for studying"

# Upload a local file
bash upload.sh --file ./my-image.jpg
```

## 常用参数

所有脚本都支持以下参数：`--async`、`--view`、`--json`、`--timeout N`、`--help`

## 使用要求

- 需要设置 `MUAPI_KEY` 环境变量（通过 `core/platform/setup.sh` 文件设置）
- 确保系统已安装 `curl`、`jq` 和 `python3` 工具