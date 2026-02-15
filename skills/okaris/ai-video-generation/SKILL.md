---
name: ai-video-generation
description: |
  Generate AI videos with Google Veo, Seedance, Wan, Grok and 40+ models via inference.sh CLI.
  Models: Veo 3.1, Veo 3, Seedance 1.5 Pro, Wan 2.5, Grok Imagine Video, OmniHuman, Fabric, HunyuanVideo.
  Capabilities: text-to-video, image-to-video, lipsync, avatar animation, video upscaling, foley sound.
  Use for: social media videos, marketing content, explainer videos, product demos, AI avatars.
  Triggers: video generation, ai video, text to video, image to video, veo, animate image,
  video from image, ai animation, video generator, generate video, t2v, i2v, ai video maker,
  create video with ai, runway alternative, pika alternative, sora alternative, kling alternative
allowed-tools: Bash(infsh *)
---

# 人工智能视频生成

您可以使用 [inference.sh](https://inference.sh) 命令行工具，通过40多种人工智能模型生成视频。

## 快速入门

```bash
# Install CLI
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a video with Veo
infsh app run google/veo-3-1-fast --input '{"prompt": "drone shot flying over a forest"}'
```

## 可用的模型

### 文本转视频

| 模型 | 应用ID | 适用场景 |
|-------|--------|----------|
| Veo 3.1 Fast | `google/veo-3-1-fast` | 生成速度快，支持可选音频 |
| Veo 3.1 | `google/veo-3-1` | 视频质量最高，支持帧插值 |
| Veo 3 | `google/veo-3` | 高质量视频，支持音频 |
| Veo 3 Fast | `google/veo-3-fast` | 生成速度快，支持音频 |
| Veo 2 | `google/veo-2` | 生成逼真视频 |
| Grok Video | `xai/grok-imagine-video` | 基于xAI技术，支持自定义时长 |
| Seedance 1.5 Pro | `bytedance/seedance-1-5-pro` | 支持对第一帧进行控制 |
| Seedance 1.0 Pro | `bytedance/seedance-1-0-pro` | 支持最高1080p分辨率 |

### 图片转视频

| 模型 | 应用ID | 适用场景 |
|-------|--------|----------|
| Wan 2.5 | `falai/wan-2-5` | 可将任何图片转换为视频 |
| Wan 2.5 I2V | `falai/wan-2-5-i2v` | 高质量的图片转视频功能 |
| Seedance Lite | `bytedance/seedance-1-0-lite` | 轻量级应用，支持720p分辨率 |

### 虚拟形象/口型同步

| 模型 | 应用ID | 适用场景 |
|-------|--------|----------|
| OmniHuman 1.5 | `bytedance/omnihuman-1-5` | 支持多角色虚拟形象 |
| OmniHuman 1.0 | `bytedance/omnihuman-1-0` | 支持单一角色虚拟形象 |
| Fabric 1.0 | `falai/fabric-1-0` | 图像与虚拟形象同步说话 |
| PixVerse Lipsync | `falai/pixverse-lipsync` | 逼真的口型同步效果 |

### 辅助工具

| 工具 | 应用ID | 功能描述 |
|------|--------|-------------|
| HunyuanVideo Foley | `infsh/hunyuanvideo-foley` | 为视频添加音效 |
| Topaz Upscaler | `falai/topaz-video-upscaler` | 提升视频分辨率 |
| Media Merger | `infsh/media-merger` | 合并视频并添加过渡效果 |

## 浏览所有视频生成工具

```bash
infsh app list --category video
```

## 示例

### 使用Veo模型将文本转换为视频

```bash
infsh app run google/veo-3-1-fast --input '{
  "prompt": "A timelapse of a flower blooming in a garden"
}'
```

### 使用Grok Video模型生成视频

```bash
infsh app run xai/grok-imagine-video --input '{
  "prompt": "Waves crashing on a beach at sunset",
  "duration": 5
}'
```

### 使用Wan 2.5模型将图片转换为视频

```bash
infsh app run falai/wan-2-5 --input '{
  "image_url": "https://your-image.jpg"
}'
```

### 使用虚拟形象模型生成视频

```bash
infsh app run bytedance/omnihuman-1-5 --input '{
  "image_url": "https://portrait.jpg",
  "audio_url": "https://speech.mp3"
}'
```

### 使用Fabric模型实现口型同步

```bash
infsh app run falai/fabric-1-0 --input '{
  "image_url": "https://face.jpg",
  "audio_url": "https://audio.mp3"
}'
```

### 使用PixVerse模型实现口型同步

```bash
infsh app run falai/pixverse-lipsync --input '{
  "image_url": "https://portrait.jpg",
  "audio_url": "https://speech.mp3"
}'
```

### 视频分辨率提升

```bash
infsh app run falai/topaz-video-upscaler --input '{"video_url": "https://..."}'
```

### 为视频添加音效

```bash
infsh app run infsh/hunyuanvideo-foley --input '{
  "video_url": "https://silent-video.mp4",
  "prompt": "footsteps on gravel, birds chirping"
}'
```

### 合并视频

```bash
infsh app run infsh/media-merger --input '{
  "videos": ["https://clip1.mp4", "https://clip2.mp4"],
  "transition": "fade"
}'
```

## 相关技能

```bash
# Full platform skill (all 150+ apps)
npx skills add inference-sh/agent-skills@inference-sh

# Google Veo specific
npx skills add inference-sh/agent-skills@google-veo

# AI avatars & lipsync
npx skills add inference-sh/agent-skills@ai-avatar-video

# Text-to-speech (for video narration)
npx skills add inference-sh/agent-skills@text-to-speech

# Image generation (for image-to-video)
npx skills add inference-sh/agent-skills@ai-image-generation

# Twitter (post videos)
npx skills add inference-sh/agent-skills@twitter-automation
```

**查看所有可用工具：** `infsh app list`

## 文档资料

- [运行应用程序](https://inference.sh/docs/apps/running) - 如何通过命令行工具运行应用程序
- [实时进度更新](https://inference.sh/docs/api/sdk/streaming) - 应用程序的实时运行状态
- [内容处理流程示例](https://inference.sh/docs/examples/content-pipeline) - 如何构建媒体处理工作流程