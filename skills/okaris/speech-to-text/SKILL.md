---
name: speech-to-text
description: "使用 `inference.sh` CLI 命令，可以通过 Whisper 模型将音频转换为文本。支持的模型包括：Fast Whisper Large V3 和 Whisper V3 Large。该工具具备以下功能：音频转录、文本翻译、多语言支持以及添加时间戳。适用场景包括：会议记录、字幕制作、播客转录、语音笔记等。触发命令包括：语音转文本（speech to text）、音频转文本（audio to text）、自动转录（automatic transcription）等。"
allowed-tools: Bash(infsh *)
---
# 语音转文本

通过 [inference.sh](https://inference.sh) 命令行工具将音频转换为文本。

![语音转文本](https://cloud.inference.sh/u/4mg21r6ta37mpaz6ktzwtt8krr/01jz025e88nkvw55at1rqtj5t8.png)

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

infsh app run infsh/fast-whisper-large-v3 --input '{"audio_url": "https://audio.mp3"}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可以选择 [手动安装及验证](https://dist.inference.sh/cli/checksums.txt)。

## 可用的模型

| 模型 | 应用 ID | 适用场景 |
|-------|--------|----------|
| Fast Whisper V3 | `infsh/fast-whisper-large-v3` | 快速转录 |
| Whisper V3 Large | `infsh/whisper-v3-large` | 最高的准确率 |

## 示例

### 基本转录

```bash
infsh app run infsh/fast-whisper-large-v3 --input '{"audio_url": "https://meeting.mp3"}'
```

### 带时间戳的转录

```bash
infsh app sample infsh/fast-whisper-large-v3 --save input.json

# {
#   "audio_url": "https://podcast.mp3",
#   "timestamps": true
# }

infsh app run infsh/fast-whisper-large-v3 --input input.json
```

### 翻译（英文）

```bash
infsh app run infsh/whisper-v3-large --input '{
  "audio_url": "https://french-audio.mp3",
  "task": "translate"
}'
```

### 从视频中转录

```bash
# Extract audio from video first
infsh app run infsh/video-audio-extractor --input '{"video_url": "https://video.mp4"}' > audio.json

# Transcribe the extracted audio
infsh app run infsh/fast-whisper-large-v3 --input '{"audio_url": "<audio-url>"}'
```

## 工作流程：为视频添加字幕

```bash
# 1. Transcribe video audio
infsh app run infsh/fast-whisper-large-v3 --input '{
  "audio_url": "https://video.mp4",
  "timestamps": true
}' > transcript.json

# 2. Use transcript for captions
infsh app run infsh/caption-videos --input '{
  "video_url": "https://video.mp4",
  "captions": "<transcript-from-step-1>"
}'
```

## 支持的语言

Whisper 支持 99 种以上的语言，包括：
英语、西班牙语、法语、德语、意大利语、葡萄牙语、中文、日语、韩语、阿拉伯语、印地语、俄语等。

## 使用场景

- **会议**：转录会议记录
- **播客**：生成播客文字稿
- **字幕**：为视频添加字幕
- **语音笔记**：将语音内容转换为可搜索的文本
- **面试**：为研究目的进行转录
- **无障碍访问**：使音频内容更易于访问

## 输出格式

返回 JSON 格式的数据，包含：
- `text`：完整的转录文本
- `segments`：带时间戳的转录片段（如需）
- `language`：检测到的语言

## 相关技能

```bash
# Full platform skill (all 150+ apps)
npx skills add inference-sh/skills@inference-sh

# Text-to-speech (reverse direction)
npx skills add inference-sh/skills@text-to-speech

# Video generation (add captions)
npx skills add inference-sh/skills@ai-video-generation

# AI avatars (lipsync with transcripts)
npx skills add inference-sh/skills@ai-avatar-video
```

查看所有音频应用程序：`infsh app list --category audio`

## 文档

- [运行应用程序](https://inference.sh/docs/apps/running) - 通过命令行运行应用程序的方法
- [音频转录示例](https://inference.sh/docs/examples/audio-transcription) - 完整的转录指南
- [应用程序概述](https://inference.sh/docs/apps/overview) - 了解应用程序生态系统