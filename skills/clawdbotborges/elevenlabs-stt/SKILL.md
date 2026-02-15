---
name: elevenlabs-stt
description: 使用 ElevenLabs 的 Speech-to-Text (Scribe v2) 服务来转录音频文件。
homepage: https://elevenlabs.io/speech-to-text
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"bins":["curl"],"env":["ELEVENLABS_API_KEY"]},"primaryEnv":"ELEVENLABS_API_KEY"}}
---

# ElevenLabs 语音转文本

使用 ElevenLabs 的 Scribe v2 模型转录音频文件。支持 90 多种语言，并能区分不同的说话者。

## 快速入门

```bash
# Basic transcription
{baseDir}/scripts/transcribe.sh /path/to/audio.mp3

# With speaker diarization
{baseDir}/scripts/transcribe.sh /path/to/audio.mp3 --diarize

# Specify language (improves accuracy)
{baseDir}/scripts/transcribe.sh /path/to/audio.mp3 --lang en

# Full JSON output with timestamps
{baseDir}/scripts/transcribe.sh /path/to/audio.mp3 --json
```

## 参数选项

| 参数 | 说明 |
|------|-------------|
| `--diarize` | 识别不同的说话者 |
| `--lang CODE` | ISO 语言代码（例如：en, pt, es） |
| `--json` | 以 JSON 格式输出转录结果，包含单词的时间戳 |
| `--events` | 为音频中的事件（如笑声、音乐等）添加标签 |

## 支持的格式

所有主要的音频/视频格式：mp3、m4a、wav、ogg、webm、mp4 等。

## API 密钥

设置 `ELEVENLABS_API_KEY` 环境变量，或在 `clawdbot.json` 中进行配置：

```json5
{
  skills: {
    entries: {
      "elevenlabs-stt": {
        apiKey: "sk_..."
      }
    }
  }
}
```

## 使用示例

```bash
# Transcribe a WhatsApp voice note
{baseDir}/scripts/transcribe.sh ~/Downloads/voice_note.ogg

# Meeting recording with multiple speakers
{baseDir}/scripts/transcribe.sh meeting.mp3 --diarize --lang en

# Get JSON for processing
{baseDir}/scripts/transcribe.sh podcast.mp3 --json > transcript.json
```