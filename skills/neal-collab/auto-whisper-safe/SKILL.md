---
name: auto-whisper-safe
version: 1.0.0
description: **RAM安全的语音转录功能，支持自动分块处理**  
——即使在16GB内存的机器上也能正常运行，不会出现系统崩溃的情况。
emoji: 🎙️
tags:
  - whisper
  - transcription
  - voice
  - audio
  - ram-safe
requires:
  bins:
    - whisper
    - ffmpeg
---

# Auto-Whisper Safe — 适合低内存环境的语音转录工具

使用 OpenAI Whisper 对语音消息和长音频文件进行转录，**而不会导致您的机器崩溃**。该工具专为配备 16GB 内存的系统设计，这些系统同时运行着其他进程（如 OpenClaw 代理程序）。

## 问题所在

OpenAI Whisper 的 `turbo` 和 `large` 模型需要 6-10GB 的内存。在配备 16GB 内存的机器上，如果同时运行 OpenClaw、Ollama 及其他服务，可能会导致内存不足（OOM）而引发系统崩溃。现有的 Whisper 工具无法解决这一问题。

## 解决方案

1. **通过 ffprobe 自动检测音频长度**。
2. **将超过 10 分钟的音频文件自动分割成 10 分钟的片段**。
3. **默认使用 `base` 模型**（约 1.5GB 内存占用——适用于所有 16GB 内存的机器）。
4. **无缝合并转录结果**，无间隙、无重复内容。
5. **自动清理临时文件**。

## 使用方法

```bash
# Basic usage
./transcribe.sh /path/to/audio.ogg

# Custom model (if you have more RAM)
WHISPER_MODEL=small ./transcribe.sh /path/to/audio.ogg

# Custom language
WHISPER_LANG=en ./transcribe.sh /path/to/audio.ogg

# Custom output directory
./transcribe.sh /path/to/audio.ogg /path/to/output/
```

## 各模型的内存占用情况

| 模型 | 内存占用 | 转录速度 | 精确度 | 适用场景 |
|-------|---------|---------|---------|-----------------|
| `tiny` | 约 1GB | 非常快 | 非常高 | 适用于快速预览、内存有限的系统 |
| `base` | 约 1.5GB | 快速 | 非常高 | **默认推荐模型** |
| `small` | 约 2.5GB | 快速 | 非常高 | 当精确度要求较高时适用 |
| `medium` | 约 5GB | 一般 | 非常高 | 仅适用于 32GB 及以上内存的机器 |
| `turbo` | 约 6GB | 一般 | 非常高 | 专为高性能转录任务设计 |

## 与 OpenClaw 的集成方法

将以下代码添加到您的代理程序的 `BOOTSTRAP.md` 文件中：

```markdown
## Voice Message Handling

When you receive `<media:audio>`, ALWAYS transcribe first:

1. Run: `./skills/auto-whisper-safe/transcribe.sh <audio-path>`
2. Read the output transcript file
3. Respond based on the transcribed content

Do this automatically — voice messages are meant to be transcribed.
```

## 环境变量设置

| 变量 | 默认值 | 说明 |
|---------|---------|-------------------|
| `WHISPER_MODEL` | `base` | 所使用的 Whisper 模型 |
| `WHISPER_LANG` | `en` | 音频语言（ISO 代码） |

## 分割音频文件的工作原理

- 如果音频时长 ≤ 10 分钟，直接进行转录（无需分割）。
- 如果音频时长超过 10 分钟，使用 ffmpeg 将其分割成 10 分钟的片段。
- 每个片段分别进行转录。
- 转录完成后，片段会按顺序合并。
- 程序退出时会自动清理临时文件（即使出现错误也是如此）。

## 安装方法

```bash
# macOS
brew install openai-whisper ffmpeg

# Ubuntu/Debian
pip install openai-whisper
apt install ffmpeg

# Verify
whisper --help && ffmpeg -version
```

## 为什么选择这个工具而非其他 Whisper 工具？

- ✅ **内存友好**：不会导致 16GB 内存的机器崩溃。
- ✅ **自动分片功能**：能够顺利处理长达 1 小时的音频文件。
- ✅ **自动清理临时文件**：不会留下任何临时文件。
- ✅ **进度显示**：会实时显示每个片段的转录进度。
- ✅ **可配置**：可以通过环境变量设置使用的模型和语言。
- ✅ **与 OpenClaw 兼容**：可以直接添加到任何代理程序的 `BOOTSTRAP.md` 文件中。

## 实际使用效果

在 Ubuntu 22.04 系统（16GB 内存）上测试，同时运行 OpenClaw（10 个代理程序）和 Ollama 的情况下，测试结果如下：

| 音频时长 | 使用的模型 | 最大内存占用 | 转录时间 | 转录效果 |
|---------|---------|-----------------|---------|
| 2 分钟的语音备忘录 | `base` | 1.4GB | 约 15 秒 | 转录完美 |
| 12 分钟的播客片段 | `base` | 1.5GB（分段处理） | 约 90 秒 | 分成 2 个片段，转录流畅 |
| 45 分钟的采访录音 | `base` | 1.5GB（分段处理） | 约 6 分钟 | 分成 5 个片段，转录流畅 |
| 2 分钟的语音备忘录 | `tiny` | 0.9GB | 约 8 秒 | 转录效果良好，适合快速阅读 |

## 支持的音频格式

ffmpeg 可以处理多种音频格式，因此几乎所有格式都支持：
- ✅ `.ogg`（Telegram 的语音消息格式）
- ✅ `.mp3`, `.m4a`, `.wav`, `.flac`
- ✅ `.webm`（浏览器录制的音频文件）
- ✅ `.opus`（WhatsApp 的语音消息格式）

## 更新日志

### v1.0.0
- 首次发布
- 支持对长音频文件（超过 10 分钟）进行自动分片处理。
- 默认使用内存占用较低的 `base` 模型（1.5GB）。
- 实时显示每个片段的转录进度。
- 自动清理临时文件。
- 允许通过环境变量配置使用的模型和语言。