---
name: talking-head-production
description: |
  Talking head video production with AI avatars, lipsync, and voiceover.
  Covers portrait requirements, audio quality, OmniHuman, PixVerse lipsync, Dia TTS.
  Use for: spokesperson videos, course content, social media, presentations, demos.
  Triggers: talking head, avatar video, lipsync, lip sync, ai spokesperson,
  virtual presenter, ai presenter, omnihuman, talking avatar, video presenter,
  ai talking head, presenter video, ai face video
allowed-tools: Bash(infsh *)
---

# Talking Head Production

使用 [inference.sh](https://inference.sh) 命令行工具，可以通过 AI 阵容和口型同步功能来制作谈话类视频。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate dialogue audio
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] Welcome to our product tour. Today I will show you three features that will save you hours every week."
}'

# Create talking head video with OmniHuman
infsh app run bytedance/omnihuman-1-5 --input '{
  "image": "path/to/portrait.png",
  "audio": "path/to/dialogue.mp3"
}'
```

## 肖像要求

源肖像图片的质量至关重要。肖像质量差会导致视频效果不佳。

### 必备条件

| 条件 | 原因 | 规格 |
|------------|-----|------|
| **画面居中** | 阵容的脸部需要位于可预测的位置 | 脸部需在画面正中央 |
| **仅显示头部和肩膀** | 以便展示自然的肢体动作 | 剪裁至胸部以下 |
| **眼睛朝向镜头** | 与观众建立联系 | 需要直视镜头 |
| **表情中性** | 作为动画的起点 | 轻微微笑可以，但禁止大笑或皱眉 |
| **面部清晰** | 模型需要能够识别面部特征 | 不能有太阳镜、浓重的阴影或遮挡物 |
| **高分辨率** | 以保持细节清晰 | 至少 512x512 的面部区域，理想为 1024x1024 或更高 |

### 背景

| 类型 | 适用场景 |
|------|-------------|
| 单色背景 | 专业、干净，易于合成 |
| 柔和的散景效果 | 自然、生活化的氛围 |
| 办公室/工作室背景 | 商业场景 |
| 透明背景（通过去除背景实现） | 可以与其他场景合成 |

```bash
# Generate a professional portrait background
infsh app run falai/flux-dev-lora --input '{
  "prompt": "professional headshot photograph of a friendly business person, soft studio lighting, clean grey background, head and shoulders, direct eye contact, neutral pleasant expression, high quality portrait photography"
}'

# Or remove background from existing portrait
infsh app run <bg-removal-app> --input '{
  "image": "path/to/portrait-with-background.png"
}'
```

## 音频质量

音频质量直接影响口型同步的准确性。清晰的音频能够确保口型动作与视频同步。

### 要求

| 参数 | 目标 | 原因 |
|-----------|--------|-----|
| 背景噪音 | 无或最小 | 噪音会干扰口型同步的时机 |
| 音量 | 全程保持一致 | 防止同步偏差 |
| 采样率 | 44.1kHz 或 48kHz | 标准音质 |
| 格式 | MP3 128kbps 或 WAV | 与所有工具兼容 |

### 生成音频

```bash
# Simple narration
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] Hi there! I am excited to share something with you today. We have been working on a feature that our users have been requesting for months... and it is finally here."
}'

# With emotion and pacing
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] You know what is frustrating? Spending hours on tasks that should take minutes. (sighs) We have all been there. But what if I told you... there is a better way?"
}'
```

## 模型选择

| 模型 | 应用ID | 适用场景 | 最大时长 |
|-------|--------|----------|-------------|
| OmniHuman 1.5 | `bytedance/omnihuman-1-5` | 支持多角色、肢体动作，高质量 | 每个片段约 30 秒 |
| OmniHuman 1.0 | `bytedance/omnihuman-1-0` | 支持单角色，操作简单 | 每个片段约 30 秒 |
| PixVerse Lipsync | `falai/pixverse-lipsync` | 可快速为现有视频添加口型同步效果 | 适用于短片段 |
| Fabric | `falai/fabric-1-0` | 可为肖像添加布料动画效果 | 适用于短片段 |

## 制作流程

### 基本流程：肖像 + 音频 -> 视频

```bash
# 1. Generate or prepare audio
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] Your narration script here."
}'

# 2. Generate talking head
infsh app run bytedance/omnihuman-1-5 --input '{
  "image": "portrait.png",
  "audio": "narration.mp3"
}'
```

### 添加字幕

```bash
# 1-2. Same as above

# 3. Add captions to the talking head video
infsh app run infsh/caption-videos --input '{
  "video": "talking-head.mp4",
  "caption_file": "captions.srt"
}'
```

### 长视频（多片段合成）

对于时长超过 30 秒的视频，建议将其分割成多个片段：

```bash
# Generate audio segments
infsh app run falai/dia-tts --input '{"prompt": "[S1] Segment one script."}' --no-wait
infsh app run falai/dia-tts --input '{"prompt": "[S1] Segment two script."}' --no-wait
infsh app run falai/dia-tts --input '{"prompt": "[S1] Segment three script."}' --no-wait

# Generate talking head for each segment (same portrait for consistency)
infsh app run bytedance/omnihuman-1-5 --input '{"image": "portrait.png", "audio": "segment1.mp3"}' --no-wait
infsh app run bytedance/omnihuman-1-5 --input '{"image": "portrait.png", "audio": "segment2.mp3"}' --no-wait
infsh app run bytedance/omnihuman-1-5 --input '{"image": "portrait.png", "audio": "segment3.mp3"}' --no-wait

# Merge all segments
infsh app run infsh/media-merger --input '{
  "media": ["segment1.mp4", "segment2.mp4", "segment3.mp4"]
}'
```

### 多角色对话

OmniHuman 1.5 支持最多 2 个角色的对话：

```bash
# 1. Generate dialogue with two speakers
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] So tell me about the new feature. [S2] Sure! We built a dashboard that shows real-time analytics. [S1] That sounds great. How long did it take? [S2] About two weeks from concept to launch."
}'

# 2. Create video with two characters
infsh app run bytedance/omnihuman-1-5 --input '{
  "image": "two-person-portrait.png",
  "audio": "dialogue.mp3"
}'
```

## 拍摄指南

```
┌─────────────────────────────────┐
│          Headroom (minimal)     │
│  ┌───────────────────────────┐  │
│  │                           │  │
│  │     ● ─ ─ Eyes at 1/3 ─ ─│─ │ ← Eyes at top 1/3 line
│  │    /|\                    │  │
│  │     |   Head & shoulders  │  │
│  │    / \  visible           │  │
│  │                           │  │
│  └───────────────────────────┘  │
│       Crop below chest          │
└─────────────────────────────────┘
```

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 肖像分辨率低 | 脸部模糊，口型同步效果差 | 使用至少 1024x1024 的面部区域 |
| 侧面或斜角拍摄 | 口型同步难以准确追踪 | 应使用正面或接近正面的拍摄角度 |
| 音频质量差 | 口型同步不准确，看起来不自然 | 录制清晰的声音或使用文本转语音（TTS） |
| 视频过长 | 超过 30 秒后质量下降 | 将视频分割成多个片段后再合成 |
| 有太阳镜或遮挡物 | 面部特征被遮挡 | 需要确保面部清晰可见 |
| 照明不均匀 | 动画效果不自然 | 使用均匀、柔和的照明 |
| 未添加字幕 | 无声或移动设备观众无法理解内容 | 必须添加字幕 |

## 相关技能

```bash
npx skills add inferencesh/skills@ai-avatar-video
npx skills add inferencesh/skills@ai-video-generation
npx skills add inferencesh/skills@text-to-speech
```

查看所有可用应用：`infsh app list`