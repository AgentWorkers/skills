---
name: eachlabs-video-edit
description: 使用 EachLabs 的 AI 模型来编辑、转换、扩展、提升视频质量，并对其进行增强处理。该工具支持唇形同步、视频翻译、字幕生成、音频合并、风格转换以及视频格式调整等功能。适用于用户需要对现有视频内容进行编辑或处理的场景。
metadata:
  author: eachlabs
  version: "1.0"
---

# EachLabs 视频编辑

通过 EachLabs 的 Predictions API，使用 25 种以上的 AI 模型来编辑、转换和优化现有视频。

## 认证

```
Header: X-API-Key: <your-api-key>
```

请设置 `EACHLABS_API_KEY` 环境变量。您可以在 [eachlabs.ai](https://eachlabs.ai) 获取该密钥。

## 模型选择指南

### 视频扩展

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Veo 3.1 Extend | `veo3-1-extend-video` | 用于提高视频质量 |
| Veo 3.1 Fast Extend | `veo3-1-fast-extend-video` | 快速视频扩展工具 |
| PixVerse v5 Extend | `pixverse-v5-extend` | PixVerse 视频扩展工具 |
| PixVerse v4.5 Extend | `pixverse-v4-5-extend` | 适用于旧版本的 PixVerse 视频 |

### 唇部同步与语音合成

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Sync Lipsync v2 Pro | `sync-lipsync-v2-pro` | 提供最高质量的唇部同步效果 |
| PixVerse Lip Sync | `pixverse-lip-sync` | PixVerse 提供的唇部同步功能 |
| LatentSync | `latentsync` | 开源的唇部同步工具 |
| Video Retalking | `video-retalking` | 基于音频的唇部同步功能 |

### 视频转换

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Runway Gen4 Aleph | `runway-gen4-aleph` | 视频转换工具 |
| Kling O1 Video Edit | `kling-o1-video-to-video-edit` | AI 视频编辑工具 |
| Kling O1 V2V Reference | `kling-o1-video-to-video-reference` | 基于参考帧的视频编辑工具 |
| ByteDance Video Stylize | `bytedance-video-stylize` | 视频风格转换工具 |
| Wan v2.2 Animate Move | `wan-v2-2-14b-animate-move` | 视频动画工具 |
| Wan v2.2 Animate Replace | `wan-v2-2-14b-animate-replace` | 视频中的物体替换工具 |

### 视频放大与优化

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Topaz Upscale Video | `topaz-upscale-video` | 最高质量的视频放大工具 |
| Luma Ray 2 Video Reframe | `luma-dream-machine-ray-2-video-reframe` | 视频重新帧工具 |
| Luma Ray 2 Flash Reframe | `luma-dream-machine-ray-2-flash-video-reframe` | 快速视频重新帧工具 |

### 音频与字幕

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| FFmpeg Merge Audio Video | `ffmpeg-api-merge-audio-video` | 合并音频和视频文件 |
| MMAudio V2 | `mm-audio-v-2` | 为视频添加音频 |
| MMAudio | `mmaudio` | 为视频添加音频 |
| Auto Subtitle | `auto-subtitle` | 生成字幕 |
| Merge Videos | `merge-videos` | 连接多个视频文件 |

### 视频翻译

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Heygen Video Translate | `heygen-video-translate` | 视频语音翻译工具 |

### 动作迁移

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Motion Fast | `motion-fast` | 快速动作迁移工具 |
| Infinitalk V2V | `infinitalk-video-to-video` | 从视频中提取语音并合成新的视频 |

### 面部替换（视频）

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Faceswap Video | `faceswap-video` | 视频中的面部替换功能 |

## 预测流程

1. **检查模型**：`GET https://api.eachlabs.ai/v1/model?slug=<slug>` — 确认模型存在，并获取包含精确输入参数的 `request_schema`。在创建预测请求之前，请务必执行此步骤以确保输入正确。
2. **发送请求**：`POST https://api.eachlabs.ai/v1/prediction`，提供模型 slug、版本 `"0.0.1"` 以及符合 schema 的输入数据。
3. **等待结果**：`GET https://api.eachlabs.ai/v1/prediction/{id}`，直到状态变为 `"success"` 或 `"failed"`。
4. **提取输出结果**：从响应中提取输出视频的 URL。

## 示例

### 使用 Veo 3.1 扩展视频质量

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "veo3-1-extend-video",
    "version": "0.0.1",
    "input": {
      "video_url": "https://example.com/video.mp4",
      "prompt": "Continue the scene with the camera slowly pulling back"
    }
  }'
```

### 使用 Sync v2 Pro 进行唇部同步

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "sync-lipsync-v2-pro",
    "version": "0.0.1",
    "input": {
      "video_url": "https://example.com/talking-head.mp4",
      "audio_url": "https://example.com/new-audio.mp3"
    }
  }'
```

### 添加字幕

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "auto-subtitle",
    "version": "0.0.1",
    "input": {
      "video_url": "https://example.com/video.mp4"
    }
  }'
```

### 将音频与视频合并

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "ffmpeg-api-merge-audio-video",
    "version": "0.0.1",
    "input": {
      "video_url": "https://example.com/video.mp4",
      "audio_url": "https://example.com/music.mp3",
      "start_offset": 0
    }
  }'
```

### 使用 Topaz 工具放大视频

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "topaz-upscale-video",
    "version": "0.0.1",
    "input": {
      "video_url": "https://example.com/low-res-video.mp4"
    }
  }'
```

## 参数参考

有关每个模型的完整参数详情，请参阅 [references/MODELS.md](references/MODELS.md)。