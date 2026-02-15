---
name: ai-avatar-video
description: |
  Create AI avatar and talking head videos with OmniHuman, Fabric, PixVerse via inference.sh CLI.
  Models: OmniHuman 1.5, OmniHuman 1.0, Fabric 1.0, PixVerse Lipsync.
  Capabilities: audio-driven avatars, lipsync videos, talking head generation, virtual presenters.
  Use for: AI presenters, explainer videos, virtual influencers, dubbing, marketing videos.
  Triggers: ai avatar, talking head, lipsync, avatar video, virtual presenter,
  ai spokesperson, audio driven video, heygen alternative, synthesia alternative,
  talking avatar, lip sync, video avatar, ai presenter, digital human
allowed-tools: Bash(infsh *)
---

# 人工智能头像与语音视频

您可以通过 [inference.sh](https://inference.sh) 命令行界面（CLI）创建人工智能头像和语音视频。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Create avatar video from image + audio
infsh app run bytedance/omnihuman-1-5 --input '{
  "image_url": "https://portrait.jpg",
  "audio_url": "https://speech.mp3"
}'
```

## 可用模型

| 模型 | 应用 ID | 适用场景 |
|-------|--------|----------|
| OmniHuman 1.5 | `bytedance/omnihuman-1-5` | 多个角色，最高画质 |
| OmniHuman 1.0 | `bytedance/omnihuman-1-0` | 单个角色 |
| Fabric 1.0 | `falai/fabric-1-0` | 基于图像的配音服务 |
| PixVerse Lipsync | `falai/pixverse-lipsync` | 高度逼真的嘴唇同步效果 |

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

支持在多人图像中指定要控制的角色。

### Fabric 1.0（基于图像的配音）

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

能够根据任何音频生成高度逼真的嘴唇同步效果。

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

- **市场营销**：使用人工智能演示者进行产品展示
- **教育**：课程视频、教学讲解
- **本地化**：将内容配音为多种语言
- **社交媒体**：统一风格的虚拟主播
- **企业**：培训视频、公告发布

## 提示

- 使用高质量的肖像照片（正面朝向，光线良好）
- 音频应清晰，背景噪音尽可能低
- OmniHuman 1.5 支持在一张图像中显示多人
- LatentSync 是将现有视频与新音频同步的最佳工具

## 相关技能

```bash
# Full platform skill (all 150+ apps)
npx skills add inference-sh/agent-skills@inference-sh

# Text-to-speech (generate audio for avatars)
npx skills add inference-sh/agent-skills@text-to-speech

# Speech-to-text (transcribe for dubbing)
npx skills add inference-sh/agent-skills@speech-to-text

# Video generation
npx skills add inference-sh/agent-skills@ai-video-generation

# Image generation (create avatar images)
npx skills add inference-sh/agent-skills@ai-image-generation
```

浏览所有视频应用：`infsh app list --category video`

## 文档资料

- [运行应用](https://inference.sh/docs/apps/running) - 如何通过 CLI 运行应用
- [内容处理流程示例](https://inference.sh/docs/examples/content-pipeline) - 构建媒体工作流程
- [流式处理结果](https://inference.sh/docs/api/sdk/streaming) - 实时进度更新