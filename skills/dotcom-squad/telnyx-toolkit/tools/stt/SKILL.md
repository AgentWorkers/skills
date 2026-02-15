---
name: telnyx-stt
description: 使用 Telnyx 的 Speech-to-Text API 将音频文件转换为文本。当您需要将音频记录、语音消息或口语内容转换为文本时，可以使用该服务。
metadata: {"openclaw":{"emoji":"🎤","requires":{"bins":["python3"],"env":["TELNYX_API_KEY"]},"primaryEnv":"TELNYX_API_KEY"}}
---

# Telnyx 语音转文本功能

使用 Telnyx 的 STT（Speech-to-Text）API（该 API 基于 Whisper 技术实现）将音频文件转换为文本。

## 使用方法

要转录音频文件，请运行以下命令：

```bash
{baseDir}/scripts/telnyx-stt.py /path/to/audio.mp3
```

脚本会将转录后的文本输出到标准输出（stdout）。

## 支持的音频格式

- MP3
- WAV
- OGG
- M4A
- WebM

## 示例

```bash
{baseDir}/scripts/telnyx-stt.py /tmp/voice-message.ogg
```

输出结果：
```
Hello, this is a test transcription.
```

## 环境要求

需要设置 `TELNYX_API_KEY` 环境变量。