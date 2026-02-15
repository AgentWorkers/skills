---
name: aimlapi-media-gen
description: 通过 AIMLAPI（兼容 OpenAI）根据提示生成图像或视频。当 Codex 需要调用 AI/ML API 的媒体端点、批量处理图像/视频任务，或使用 AIMLAPI 凭据从文本提示生成媒体文件时，可以使用此功能。
---

# AIMLAPI 媒体生成

## 概述

通过兼容 OpenAI 的 AIMLAPI，使用可重用的脚本生成图片和视频。这些脚本负责处理身份验证、数据传输以及媒体文件的下载。

## 快速入门

```bash
export AIMLAPI_API_KEY="sk-aimlapi-..."
python3 {baseDir}/scripts/gen_image.py --prompt "ultra-detailed studio photo of a lobster astronaut"
python3 {baseDir}/scripts/gen_video.py --prompt "slow drone shot of a foggy forest" --model aimlapi/<provider>/<video-model>
```

## 任务

### 生成图片

使用 `scripts/gen_image.py` 调用 `/images/generations` 端点，并将结果保存到本地。

```bash
python3 {baseDir}/scripts/gen_image.py \
  --prompt "cozy cabin in a snowy forest" \
  --model aimlapi/openai/gpt-image-1 \
  --size 1024x1024 \
  --count 2 \
  --out-dir ./out/images
```

**注意：**

- 如果您的 AIMLAPI 端点不同，请修改 `--base-url` 参数。
- 使用 `--extra-json` 参数传递特定于提供商的参数，无需修改脚本本身。

### 生成视频

使用 `scripts/gen_video.py` 调用视频生成端点，并保存返回的媒体文件。

```bash
python3 {baseDir}/scripts/gen_video.py \
  --prompt "time-lapse of clouds over a mountain range" \
  --model aimlapi/<provider>/<video-model> \
  --endpoint videos/generations \
  --out-dir ./out/videos \
  --extra-json '{"duration": 6, "size": "1024x576"}'
```

**注意：**

- 视频生成端点和所需的数据字段因提供商而异。请查阅您的 AIMLAPI 文档以确认正确的端点和字段，然后通过 `--endpoint` 和 `--extra-json` 参数传递这些信息。

## 参考资料

- `references/aimlapi-media.md`：包含端点和数据传输的详细说明，以及故障排除技巧。