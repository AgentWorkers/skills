---
name: talking-head-production
description: "使用人工智能头像、对口型表演和旁白来制作演讲者视频。涵盖了头像要求、音频质量、OmniHuman技术、PixVerse对口型系统以及Dia TTS（文本转语音）等相关内容。适用于：发言人视频、课程内容、社交媒体、演示文稿等场景。相关术语包括：演讲者视频（talking head video）、人工智能头像（AI avatar）、对口型表演（lip sync）、人工智能发言人（AI spokesperson）、虚拟主持人（virtual presenter）、OmniHuman技术（OmniHuman）、AI面部识别技术（AI face recognition）等。"
allowed-tools: Bash(infsh *)
---
# Talking Head Production

使用 [inference.sh](https://inference.sh) 命令行工具，结合 AI 阵容和口型同步功能，制作具有对话效果的视频。

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

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可以[手动安装并验证](https://dist.inference.sh/cli/checksums.txt)。

## 脸部图像要求

源图像的质量对视频效果至关重要。图像质量差会导致视频效果不佳。

### 必须满足的条件

| 条件 | 原因 | 规格 |
|------------|-----|------|
| **画面居中** | 阵容的脸部位置需要固定 | 面部必须在画面中央 |
| **仅显示头部和肩膀** | 以便展示自然的手势 | 剪裁图像至胸部以下 |
| **眼睛朝向镜头** | 与观众建立联系 | 需要直视镜头 |
| **表情中性** | 作为动画的起点 | 轻微微笑可以，但禁止大笑或皱眉 |
| **面部清晰** | 模型需要能够识别面部特征 | 不能有太阳镜、浓重的阴影或遮挡物 |
| **高分辨率** | 以保留细节 | 至少 512x512 的面部区域，理想情况下为 1024x1024 或更高 |

### 背景选择

| 背景类型 | 适用场景 |
|------|-------------|
| 单色背景 | 专业、简洁，易于合成 |
| 柔和的散景效果 | 营造自然的生活场景 |
| 办公室/工作室风格 | 适用于商务场景 |
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

音频质量直接影响口型同步的准确性。音频质量越高，口型同步越精确。

### 音频要求

| 参数 | 目标 | 原因 |
|-----------|--------|-----|
| 背景噪音 | 无或最小 | 噪音会影响口型同步的准确性 |
| 音量 | 全程保持一致 | 避免同步偏差 |
| 采样率 | 44.1kHz 或 48kHz | 标准质量 |
| 格式 | MP3 128kbps 或 WAV | 与所有工具兼容 |

### 音频生成

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

| 模型 | 应用 ID | 适用场景 | 最长录制时间 |
|-------|--------|----------|-------------|
| OmniHuman 1.5 | `bytedance/omnihuman-1-5` | 支持多角色、手势，高质量 | 每段视频约 30 秒 |
| OmniHuman 1.0 | `bytedance/omnihuman-1-0` | 支持单角色，操作简单 | 每段视频约 30 秒 |
| PixVerse Lipsync | `falai/pixverse-lipsync` | 可快速为现有视频添加口型同步效果 | 适用于短片 |
| Fabric | `falai/fabric-1-0` | 可为带有布料的图像添加动画效果 | 适用于短片 |

## 制作流程

### 基础流程：面部图像 + 音频 -> 视频

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

### 带字幕的视频制作

```bash
# 1-2. Same as above

# 3. Add captions to the talking head video
infsh app run infsh/caption-videos --input '{
  "video": "talking-head.mp4",
  "caption_file": "captions.srt"
}'
```

### 长视频（分段处理）

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

OmniHuman 1.5 支持最多两个角色的对话：

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

## 常见问题及解决方法

| 问题 | 原因 | 解决方法 |
|---------|---------|-----|
| 图像分辨率低 | 面部模糊，口型同步效果差 | 使用至少 1024x1024 的面部区域 |
| 从侧面或侧面角度拍摄 | 口型同步难以准确捕捉 | 应选择正面或接近正面的拍摄角度 |
| 音频质量差 | 口型同步不准确 | 录制清晰音频或使用文本转语音（TTS） |
| 视频过长 | 超过 30 秒后视频质量下降 | 将视频分割成多个片段后再合成 |
| 佩戴太阳镜或面部有遮挡物 | 面部特征无法被识别 | 确保面部清晰可见 |
| 照明不均匀 | 动画效果不自然 | 使用均匀、柔和的照明 |
| 未添加字幕 | 无声或移动设备用户无法观看 | 必须添加字幕 |

## 相关技能

```bash
npx skills add inference-sh/skills@ai-avatar-video
npx skills add inference-sh/skills@ai-video-generation
npx skills add inference-sh/skills@text-to-speech
```

查看所有可用应用：`infsh app list`