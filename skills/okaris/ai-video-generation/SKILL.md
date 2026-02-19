---
name: ai-video-generation
description: "使用 `inference.sh` CLI，可以通过 Google Veo、Seedance、Wan、Grok 等 40 多个模型生成 AI 视频。支持的模型包括：Veo 3.1、Veo 3、Seedance 1.5 Pro、Wan 2.5、Grok Imagine Video、OmniHuman、Fabric、HunyuanVideo。该工具具备以下功能：文本转视频、图片转视频、口型同步、虚拟形象动画、视频放大、音效处理等。适用于制作社交媒体视频、营销内容、讲解视频、产品演示以及 AI 虚拟形象等场景。可执行的命令包括：生成视频、文本转视频、图片转视频、视频处理等。"
allowed-tools: Bash(infsh *)
---
# 人工智能视频生成

您可以通过 [inference.sh](https://inference.sh) 命令行工具，使用 40 多个人工智能模型来生成视频。

![人工智能视频生成](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kg2c0egyg243mnyth4y6g51q.jpeg)

## 快速入门

```bash
# Install CLI
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a video with Veo
infsh app run google/veo-3-1-fast --input '{"prompt": "drone shot flying over a forest"}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可以选择 [手动安装及验证](https://dist.inference.sh/cli/checksums.txt)。

## 可用模型

### 文本转视频

| 模型 | 应用 ID | 适用场景 |
|-------|--------|----------|
| Veo 3.1 Fast | `google/veo-3-1-fast` | 生成速度快，支持可选音频 |
| Veo 3.1 | `google/veo-3-1` | 生成质量最高，支持帧插值 |
| Veo 3 | `google/veo-3` | 生成高质量视频，支持音频 |
| Veo 3 Fast | `google/veo-3-fast` | 生成速度快，支持音频 |
| Veo 2 | `google/veo-2` | 生成逼真视频 |
| Grok Video | `xai/grok-imagine-video` | 基于 xAI 技术，支持自定义时长 |
| Seedance 1.5 Pro | `bytedance/seedance-1-5-pro` | 支持对首帧进行控制 |
| Seedance 1.0 Pro | `bytedance/seedance-1-0-pro` | 支持最高 1080p 分辨率 |

### 图片转视频

| 模型 | 应用 ID | 适用场景 |
|-------|--------|----------|
| Wan 2.5 | `falai/wan-2-5` | 可将任何图片转换为视频 |
| Wan 2.5 I2V | `falai/wan-2-5-i2v` | 生成高质量的视频 |
| Seedance Lite | `bytedance/seedance-1-0-lite` | 轻量级应用，支持 720p 分辨率 |

### 虚拟形象/口型同步

| 模型 | 应用 ID | 适用场景 |
|-------|--------|----------|
| OmniHuman 1.5 | `bytedance/omnihuman-1-5` | 支持多人物形象 |
| OmniHuman 1.0 | `bytedance/omnihuman-1-0` | 支持单人形象 |
| Fabric 1.0 | `falai/fabric-1-0` | 图像与口型同步 |
| PixVerse Lipsync | `falai/pixverse-lipsync` | 生成逼真的口型同步效果 |

### 工具

| 工具 | 应用 ID | 功能描述 |
|------|--------|-------------|
| HunyuanVideo Foley | `infsh/hunyuanvideo-foley` | 为视频添加音效 |
| Topaz Upscaler | `falai/topaz-video-upscaler` | 提升视频画质 |
| Media Merger | `infsh/media-merger` | 合并视频并添加过渡效果 |

## 浏览所有视频生成工具

```bash
infsh app list --category video
```

## 示例

### 使用 Veo 模型进行文本转视频

```bash
infsh app run google/veo-3-1-fast --input '{
  "prompt": "A timelapse of a flower blooming in a garden"
}'
```

### 使用 Grok Video 模型

```bash
infsh app run xai/grok-imagine-video --input '{
  "prompt": "Waves crashing on a beach at sunset",
  "duration": 5
}'
```

### 使用 Wan 2.5 模型进行图片转视频

```bash
infsh app run falai/wan-2-5 --input '{
  "image_url": "https://your-image.jpg"
}'
```

### 使用虚拟形象/说话头模型

```bash
infsh app run bytedance/omnihuman-1-5 --input '{
  "image_url": "https://portrait.jpg",
  "audio_url": "https://speech.mp3"
}'
```

### 使用 Fabric 模型进行口型同步

```bash
infsh app run falai/fabric-1-0 --input '{
  "image_url": "https://face.jpg",
  "audio_url": "https://audio.mp3"
}'
```

### 使用 PixVerse 模型进行口型同步

```bash
infsh app run falai/pixverse-lipsync --input '{
  "image_url": "https://portrait.jpg",
  "audio_url": "https://speech.mp3"
}'
```

### 视频画质提升

```bash
infsh app run falai/topaz-video-upscaler --input '{"video_url": "https://..."}'
```

### 添加音效（Foley）

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
npx skills add inference-sh/skills@inference-sh

# Google Veo specific
npx skills add inference-sh/skills@google-veo

# AI avatars & lipsync
npx skills add inference-sh/skills@ai-avatar-video

# Text-to-speech (for video narration)
npx skills add inference-sh/skills@text-to-speech

# Image generation (for image-to-video)
npx skills add inference-sh/skills@ai-image-generation

# Twitter (post videos)
npx skills add inference-sh/skills@twitter-automation
```

- 浏览所有可用工具：`infsh app list`

## 文档资料

- [运行应用程序](https://inference.sh/docs/apps/running) - 如何通过命令行运行应用程序
- [实时进度更新](https://inference.sh/docs/api/sdk/streaming) - 实时进度监控
- [内容处理流程示例](https://inference.sh/docs/examples/content-pipeline) - 媒体工作流程构建指南