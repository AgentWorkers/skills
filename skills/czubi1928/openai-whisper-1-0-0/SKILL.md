---
name: openai-whisper
description: 使用 Whisper CLI 进行本地语音转文本操作（无需 API 密钥）。
homepage: https://openai.com/research/whisper
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"bins":["whisper"]},"install":[{"id":"brew","kind":"brew","formula":"openai-whisper","bins":["whisper"],"label":"Install OpenAI Whisper (brew)"}]}}
---

# Whisper (命令行工具)

使用 `whisper` 可以在本地将音频文件转录为文本。

**快速入门：**
- `whisper /path/audio.mp3 --model medium --output_format txt --output_dir .`
- `whisper /path/audio.m4a --task translate --output_format srt`

**注意事项：**
- 首次运行时，模型文件会被下载到 `~/.cache/whisper` 目录中。
- 在此安装版本中，`--model` 的默认值为 `turbo`。
- 使用较小的模型可以提高转录速度，但准确性会降低；使用较大的模型则可以提高准确性，但速度会变慢。