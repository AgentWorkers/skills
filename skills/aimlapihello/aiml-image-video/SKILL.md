---
name: aimlapi-media-gen
description: 通过 AIMLAPI 根据提示生成图像或视频。当 Codex 需要可靠的 AI/ML API 媒体生成功能时，该工具可以提供重试机制、明确的 User-Agent 标头以及异步视频轮询功能。
env:
  - AIMLAPI_API_KEY
primaryEnv: AIMLAPI_API_KEY
---

# AIMLAPI 媒体生成

## 概述

通过 AIMLAPI 生成图片和视频。相关脚本支持重试机制、API 密钥文件的备用方案、详细的日志记录，并在每次请求时添加必要的 `User-Agent` 头信息。

## 快速入门

```bash
export AIMLAPI_API_KEY="sk-aimlapi-..."
python3 {baseDir}/scripts/gen_image.py --prompt "ultra-detailed studio photo of a lobster astronaut"
python3 {baseDir}/scripts/gen_video.py --prompt "slow drone shot of a foggy forest"
```

## 任务

### 生成图片

使用 `scripts/gen_image.py` 并指定路径 `/v1/images/generations`。

```bash
python3 {baseDir}/scripts/gen_image.py \
  --prompt "cozy cabin in a snowy forest" \
  --model aimlapi/openai/gpt-image-1 \
  --size 1024x1024 \
  --count 2 \
  --retry-max 4 \
  --user-agent "openclaw-custom/1.0" \
  --out-dir ./out/images
```

### 生成视频（异步 AIMLAPI 流程）

使用 `scripts/gen_video.py` 和以下异步流程：

1. 发送 `POST` 请求到 `/v2/video/generations`（创建生成任务）。
2. 发送 `GET` 请求到 `/v2/video/generations?generation_id=...`（查询任务状态）。
3. 当任务状态完成时，下载生成的视频文件（路径为 `video.url`）。

```bash
python3 {baseDir}/scripts/gen_video.py \
  --model google/veo-3.1-t2v-fast \
  --prompt "time-lapse of clouds over a mountain range" \
  --poll-interval 10 \
  --max-wait 1000 \
  --user-agent "openclaw-custom/1.0" \
  --out-dir ./out/videos
```

## 参考资料

- `references/aimlapi-media.md`：包含端点说明、异步请求状态查询方法及故障排除信息。
- `README.md`：以变更日志的形式总结了新增的指令和功能。