---
name: eachlabs-video-generation
description: 使用 EachLabs AI 模型，可以根据文本提示、图片或参考输入生成新的视频。该平台支持文本转视频、图片转视频、视频过渡效果、动态人物（talking head）以及虚拟角色（avatar）的生成功能。当用户需要创建新的视频内容时，可以选用此服务。如需编辑现有视频，请参考 eachlabs-video-edit。
metadata:
  author: eachlabs
  version: "1.0"
---

# EachLabs 视频生成

通过 EachLabs Predictions API，可以使用 165 种以上的人工智能模型根据文本提示、图片或参考输入生成新的视频。如需编辑现有视频（如缩放、对口型、添加字幕等），请参阅 `eachlabs-video-edit` 技能。

## 认证

```
Header: X-API-Key: <your-api-key>
```

请设置 `EACHLABS_API_KEY` 环境变量或直接传递该密钥。您可以在 [eachlabs.ai](https://eachlabs.ai) 获取密钥。

## 快速入门

### 1. 创建预测请求

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "pixverse-v5-6-text-to-video",
    "version": "0.0.1",
    "input": {
      "prompt": "A golden retriever running through a meadow at sunset, cinematic slow motion",
      "resolution": "720p",
      "duration": "5",
      "aspect_ratio": "16:9"
    }
  }'
```

### 2. 查看结果

```bash
curl https://api.eachlabs.ai/v1/prediction/{prediction_id} \
  -H "X-API-Key: $EACHLABS_API_KEY"
```

持续查询直到状态变为 `"success"` 或 `"failed"`。输出视频的 URL 会在响应中提供。

## 模型选择指南

### 文本转视频

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Pixverse v5.6 | `pixverse-v5-6-text-to-video` | 通用用途，支持音频生成 |
| XAI Grok Imagine | `xai-grok-imagine-text-to-video` | 快速创意生成 |
| Kandinsky 5 Pro | `kandinsky5-pro-text-to-video` | 艺术风格，高质量视频 |
| Seedance v1.5 Pro | `seedance-v1-5-pro-text-to-video` | 电影级画质 |
| Wan v2.6 | `wan-v2-6-text-to-video` | 适合长篇或叙事性内容 |
| Kling v2.6 Pro | `kling-v2-6-pro-text-to-video` | 支持动态效果 |
| Pika v2.2 | `pika-v2-2-text-to-video` | 具有风格化的视频效果 |
| Minimax Hailuo V2.3 Pro | `minimax-hailuo-v2-3-pro-text-to-video` | 高保真度视频 |
| Sora 2 Pro | `sora-2-text-to-video-pro` | 优质视频制作 |
| Veo 3 | `veo-3` | Google 最优质的模型 |
| Veo 3.1 | `veo3-1-text-to-video` | Google 最新的模型 |
| LTX v2 Fast | `ltx-v-2-text-to-video-fast` | 最快速的生成工具 |
| Moonvalley Marey | `moonvalley-marey-text-to-video` | 电影风格视频 |
| Ovi | `ovi-text-to-video` | 通用用途 |

### 图片转视频

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Pixverse v5.6 | `pixverse-v5-6-image-to-video` | 通用用途 |
| XAI Grok Imagine | `xai-grok-imagine-image-to-video` | 创意视频编辑 |
| Wan v2.6 Flash | `wan-v2-6-image-to-video-flash` | 最快速的转换工具 |
| Wan v2.6 | `wan-v2-6-image-to-video` | 高质量视频 |
| Seedance v1.5 Pro | `seedance-v1-5-pro-image-to-video` | 电影级画质 |
| Kandinsky 5 Pro | `kandinsky5-pro-image-to-video` | 艺术风格视频 |
| Kling v2.6 Pro I2V | `kling-v2-6-pro-image-to-video` | Kling 模型的最佳效果 |
| Kling O1 | `kling-o1-image-to-video` | Kling 最新的模型 |
| Pika v2.2 I2V | `pika-v2-2-image-to-video` | 具有特效的视频 |
| Minimax Hailuo V2.3 Pro | `minimax-hailuo-v2-3-pro-image-to-video` | 高保真度视频 |
| Sora 2 I2V | `sora-2-image-to-video` | 优质视频制作 |
| Veo 3.1 I2V | `veo3-1-image-to-video` | Google 最新的模型 |
| Runway Gen4 Turbo | `gen4-turbo` | 快速生成，适合社交媒体发布 |
| Veed Fabric 1.0 | `veed-fabric-1-0` | 适合社交媒体的视频格式 |

### 过渡效果与特效

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Pixverse v5.6 Transition | `pixverse-v5-6-transition` | 平滑的过渡效果 |
| Pika v2.2 PikaScenes | `pika-v2-2-pikascenes` | 场景特效 |
| Pixverse v4.5 Effect | `pixverse-v4-5-effect` | 视频特效 |
| Veo 3.1 First Last Frame | `veo3-1-first-last-frame-to-video` | 视频帧的插值处理 |

### 动态控制与动画

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Kling v2.6 Pro Motion | `kling-v2-6-pro-motion-control` | 高级动态控制 |
| Kling v2.6 Standard Motion | `kling-v2-6-standard-motion-control` | 标准动态效果 |
| Motion Fast | `motion-fast` | 快速的动态效果转换 |
| Motion Video 14B | `motion-video-14b` | 高质量的动态效果 |
| Wan v2.6 R2V | `wan-v2-6-reference-to-video` | 基于参考图像的动画 |
| Kling O1 Reference I2V | `kling-o1-reference-image-to-video` | 基于参考图像的动画 |

### 语音合成与对口型

| 模型 | Slug | 适用场景 |
|-------|------|----------|
| Bytedance Omnihuman v1.5 | `bytedance-omnihuman-v1-5` | 全身动画 |
| Creatify Aurora | `creatify-aurora` | 基于音频的虚拟形象 |
| Infinitalk I2V | `infinitalk-image-to-video` | 图像驱动的语音合成 |
| Infinitalk V2V | `infinitalk-video-to-video` | 视频驱动的语音合成 |
| Sync Lipsync v2 Pro | `sync-lipsync-v2-pro` | 高质量的对口型效果 |
| Kling Avatar v2 Pro | `kling-avatar-v2-pro` | 专业级虚拟形象 |
| Kling Avatar v2 Standard | `kling-avatar-v2-standard` | 标准虚拟形象 |
| Echomimic V3 | `echomimic-v3` | 面部动画效果 |
| Stable Avatar | `stable-avatar` | 稳定的语音合成效果 |

## 预测流程

1. **检查模型**：`GET https://api.eachlabs.ai/v1/model?slug=<slug>` — 确认模型存在，并获取包含精确输入参数的 `request_schema`。在创建预测请求前务必执行此操作，以确保输入正确。
2. **发送预测请求**：`POST https://api.eachlabs.ai/v1/prediction`，提供模型 Slug、版本 `"0.0.1"` 以及符合 schema 的输入参数。
3. **查询结果**：`GET https://api.eachlabs.ai/v1/prediction/{id}`，直到状态变为 `"success"` 或 `"failed"`。
4. **提取输出视频 URL**：从响应中获取输出视频的 URL。

## 示例

### 使用 Wan v2.6 Flash 从图片生成视频

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "wan-v2-6-image-to-video-flash",
    "version": "0.0.1",
    "input": {
      "image_url": "https://example.com/photo.jpg",
      "prompt": "The person turns to face the camera and smiles",
      "duration": "5",
      "resolution": "1080p"
    }
  }'
```

### 使用 Pixverse 实现视频过渡效果

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "pixverse-v5-6-transition",
    "version": "0.0.1",
    "input": {
      "prompt": "Smooth morphing transition between the two images",
      "first_image_url": "https://example.com/start.jpg",
      "end_image_url": "https://example.com/end.jpg",
      "duration": "5",
      "resolution": "720p"
    }
  }'
```

### 使用 Kling v2.6 进行动态控制

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "kling-v2-6-pro-motion-control",
    "version": "0.0.1",
    "input": {
      "image_url": "https://example.com/character.jpg",
      "video_url": "https://example.com/dance-reference.mp4",
      "character_orientation": "video"
    }
  }'
```

### 使用 Bytedance Omnihuman 创建语音合成效果

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "bytedance-omnihuman-v1-5",
    "version": "0.0.1",
    "input": {
      "image_url": "https://example.com/portrait.jpg",
      "audio_url": "https://example.com/speech.mp3",
      "resolution": "1080p"
    }
  }'
```

## 提示建议：

- 对动态效果进行具体描述：例如使用“相机缓慢向左平移”而非“流畅的镜头移动”。
- 使用风格相关的关键词，如“电影级”、“动漫风格”、“3D 动画”或“赛博朋克风格”。
- 明确说明时间控制要求，例如“慢动作”、“延时拍摄”或“快节奏”。
- 对于图片转视频的任务，描述静态图片中需要变化的部分。
- 如模型支持，可以使用否定性提示来排除不需要的元素。

## 参数参考

有关每个模型的完整参数详情，请参阅 [references/MODELS.md](references/MODELS.md)。