---
name: ai-avatar-video
description: "使用 `inference.sh` CLI，可以通过 OmniHuman、Fabric 和 PixVerse 创建 AI 阿凡达及语音视频。支持的模型包括：OmniHuman 1.5、OmniHuman 1.0、Fabric 1.0 以及 PixVerse Lipsync。功能包括：基于音频的动画生成、口型同步视频制作、语音播报功能以及虚拟主持人的创建。适用场景包括：AI 演讲者、解释性视频、虚拟 influencer（网红）、配音、营销视频等。相关术语包括：AI 阿凡达（AI Avatar）、语音播报（Talking Head）、口型同步（Lipsync）、虚拟主持人（Virtual Presenter）、音频驱动视频（Audio-Driven Video）等。"
allowed-tools: Bash(infsh *)
---
# 人工智能头像与语音视频

您可以通过 [inference.sh](https://inference.sh) 命令行界面（CLI）创建人工智能头像和语音视频。

![人工智能头像与语音视频](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kg0tszs96s0n8z5gy8y5mbg7.jpeg)

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Create avatar video from image + audio
infsh app run bytedance/omnihuman-1-5 --input '{
  "image_url": "https://portrait.jpg",
  "audio_url": "https://speech.mp3"
}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可选择 [手动安装与验证](https://dist.inference.sh/cli/checksums.txt)。

## 可用模型

| 模型 | 应用 ID | 适用场景 |
|-------|--------|----------|
| OmniHuman 1.5 | `bytedance/omnihuman-1-5` | 支持多角色展示，画质最佳 |
| OmniHuman 1.0 | `bytedance/omnihuman-1-0` | 仅支持单角色展示 |
| Fabric 1.0 | `falai/fabric-1-0` | 图像结合口型同步技术 |
| PixVerse Lipsync | `falai/pixverse-lipsync` | 生成高度逼真的口型同步效果 |

## 搜索头像应用

```bash
infsh app list --search "omnihuman"
infsh app list --search "lipsync"
infsh app list --search "fabric"
```

## 示例

### OmniHuman 1.5（多角色）

```bash
infsh app run bytedance/omnihuman-1-5 --input '{
  "image_url": "https://portrait.jpg",
  "audio_url": "https://speech.mp3"
}'
```

支持在多人图像中指定要展示的角色。

### Fabric 1.0（图像语音合成）

```bash
infsh app run falai/fabric-1-0 --input '{
  "image_url": "https://face.jpg",
  "audio_url": "https://audio.mp3"
}'
```

### PixVerse Lipsync

```bash
infsh app run falai/pixverse-lipsync --input '{
  "image_url": "https://portrait.jpg",
  "audio_url": "https://speech.mp3"
}'
```

能够根据任何音频生成高度逼真的口型同步效果。

## 完整工作流程：文本转语音（TTS）+ 头像

```bash
# 1. Generate speech from text
infsh app run infsh/kokoro-tts --input '{
  "text": "Welcome to our product demo. Today I will show you..."
}' > speech.json

# 2. Create avatar video with the speech
infsh app run bytedance/omnihuman-1-5 --input '{
  "image_url": "https://presenter-photo.jpg",
  "audio_url": "<audio-url-from-step-1>"
}'
```

## 完整工作流程：将视频配音为另一种语言

```bash
# 1. Transcribe original video
infsh app run infsh/fast-whisper-large-v3 --input '{"audio_url": "https://video.mp4"}' > transcript.json

# 2. Translate text (manually or with an LLM)

# 3. Generate speech in new language
infsh app run infsh/kokoro-tts --input '{"text": "<translated-text>"}' > new_speech.json

# 4. Lipsync the original video with new audio
infsh app run infsh/latentsync-1-6 --input '{
  "video_url": "https://original-video.mp4",
  "audio_url": "<new-audio-url>"
}'
```

## 应用场景

- **市场营销**：使用人工智能演示产品
- **教育**：课程视频、教学资料
- **本地化**：将内容配音为多种语言
- **社交媒体**：统一风格的虚拟博主
- **企业**：培训视频、公告发布

## 提示

- 使用高质量的肖像照片（正面拍摄，光线充足）
- 音频应清晰，背景噪音尽量减少
- OmniHuman 1.5 支持在同一图像中展示多人
- LatentSync 功能适用于将现有视频与新的音频同步

## 相关技能

```bash
# Full platform skill (all 150+ apps)
npx skills add inference-sh/skills@inference-sh

# Text-to-speech (generate audio for avatars)
npx skills add inference-sh/skills@text-to-speech

# Speech-to-text (transcribe for dubbing)
npx skills add inference-sh/skills@speech-to-text

# Video generation
npx skills add inference-sh/skills@ai-video-generation

# Image generation (create avatar images)
npx skills add inference-sh/skills@ai-image-generation
```

查看所有视频应用：`infsh app list --category video`

## 文档资料

- [运行应用](https://inference.sh/docs/apps/running) - 如何通过 CLI 运行应用
- [内容处理流程示例](https://inference.sh/docs/examples/content-pipeline) - 构建媒体处理工作流程
- [流式处理结果](https://inference.sh/docs/api/sdk/streaming) - 实时进度更新