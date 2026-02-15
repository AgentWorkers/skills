---
name: whisper-transcribe
description: 使用 OpenAI Whisper 将音频文件转录为文本。该工具支持语音转文本功能，并具备自动语言检测能力；支持多种输出格式（txt、srt、vtt、json），支持批量处理，同时允许用户选择不同的模型（从简单到高级的模型）。适用于转录音频录音、播客、语音消息、讲座、会议内容或任何音频/视频文件。支持的音频格式包括 mp3、wav、m4a、ogg、flac、webm、opus、aac。
---

# Whisper Transcribe

使用 `scripts/transcribe.sh` 脚本转录音频：

```bash
# Basic (auto-detect language, base model)
scripts/transcribe.sh recording.mp3

# German, small model, SRT subtitles
scripts/transcribe.sh --model small --language de --format srt lecture.wav

# Batch process, all formats
scripts/transcribe.sh --format all --output-dir ./transcripts/ *.mp3

# Word-level timestamps
scripts/transcribe.sh --timestamps interview.m4a
```

## 模型

| 模型 | 内存占用（RAM） | 处理速度 | 精确度 | 适用场景 |
|-------|----------------|----------------|-----------|-------------------------|
| tiny | 约1GB | 非常快 | ★★ | 快速草稿，已知语言的转录 |
| base | 约1GB | 较快 | ★★★ | 通用用途（默认模型） |
| small | 约2GB | 较快 | ★★★★ | 精确度较高 |
| medium | 约5GB | 适中 | ★★★★ | 高精确度 |
| large | 约10GB | 最快 | ★★★★ | 最高的精确度（但在树莓派（Pi）上运行较慢） |

## 输出格式

- **txt** — 纯文本转录结果
- **srt** — SubRip字幕格式（用于视频）
- **vtt** — WebVTT字幕格式
- **json** — 包含时间戳和置信度的详细JSON数据
- **all** — 一次性生成所有格式的输出文件

## 所需软件

- `whisper` 命令行工具（通过 `pip install openai-whisper` 安装）
- `ffmpeg`（用于音频解码）

**注意：** 首次运行时，系统会下载相应的模型文件（base模型约150MB）。