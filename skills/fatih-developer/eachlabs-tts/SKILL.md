---
name: eachlabs-tts
description: 使用 EachLabs 的 Speech-to-Text (Scribe v1) 从 URL 中转录音频。
homepage: https://eachlabs.ai/
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"bins":["curl"],"env":["EACHLABS_API_KEY"]},"primaryEnv":"EACHLABS_API_KEY"}}
---

# EachLabs ElevenLabs 语音转文本

使用 EachLabs 与 ElevenLabs Scribe v1 模型的集成来转录音频文件。支持对话记录功能以及精确的时间戳标注。

## 快速入门

```bash
# Basic transcription from URL
{baseDir}/scripts/transcribe.sh https://storage.googleapis.com/magicpoint/inputs/elevenlabs-s2t-input.mp3

# With speaker diarization
{baseDir}/scripts/transcribe.sh https://.../audio.mp3 --diarize

# Specify language (improves accuracy)
{baseDir}/scripts/transcribe.sh https://.../audio.mp3 --lang en

# Full JSON output with timestamps (word-level)
{baseDir}/scripts/transcribe.sh https://.../audio.mp3 --json
```

## 参数选项

| 参数 | 说明 |
|------|-------------|
| `--diarize` | 识别不同的说话者 |
| `--lang CODE` | ISO 语言代码（例如：en, pt, es） |
| `--json` | 以 JSON 格式输出包含单词时间戳的完整数据 |
| `--events` | 为音频中的事件（如笑声、音乐等）添加标签 |

## 支持的输入格式

目前仅支持 **音频 URL**。该音频文件必须可以通过 HTTP/HTTPS 公开访问。

## API 密钥

设置 `EACHLABS_API_KEY` 环境变量，或在 `clawdbot.json` 中进行配置：

```json5
{
  skills: {
    entries: {
      "eachlabs-elevenlabs-stt": {
        apiKey: "el_..."
      }
    }
  }
}
```