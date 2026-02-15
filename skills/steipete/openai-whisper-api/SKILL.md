---
name: openai-whisper-api
description: 通过 OpenAI 的 Audio Transcriptions API（Whisper）来转录音频内容。
homepage: https://platform.openai.com/docs/guides/speech-to-text
metadata: {"clawdbot":{"emoji":"☁️","requires":{"bins":["curl"],"env":["OPENAI_API_KEY"]},"primaryEnv":"OPENAI_API_KEY"}}
---

# OpenAI Whisper API (curl)

通过 OpenAI 的 `/v1/audio/transcriptions` 端点转录音频文件。

## 快速入门

```bash
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a
```

默认参数：
- 模型：`whisper-1`
- 输出格式：`<input>.txt`

## 有用的参数

```bash
{baseDir}/scripts/transcribe.sh /path/to/audio.ogg --model whisper-1 --out /tmp/transcript.txt
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a --language en
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a --prompt "Speaker names: Peter, Daniel"
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a --json --out /tmp/transcript.json
```

## API 密钥

请设置 `OPENAI_API_KEY`，或在 `~/.clawdbot/clawdbot.json` 文件中配置它：

```json5
{
  skills: {
    "openai-whisper-api": {
      apiKey: "OPENAI_KEY_HERE"
    }
  }
}
```