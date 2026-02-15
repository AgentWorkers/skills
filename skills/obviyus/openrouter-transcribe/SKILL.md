---
name: openrouter-transcribe
description: 通过 OpenRouter 使用具备音频处理能力的模型（如 Gemini、GPT-4o-audio 等）来转录音频文件。
homepage: https://openrouter.ai/docs
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"bins":["curl","ffmpeg","base64","jq"],"env":["OPENROUTER_API_KEY"]},"primaryEnv":"OPENROUTER_API_KEY"}}
---

# OpenRouter 音频转录功能

使用 OpenRouter 的聊天补全 API（`input_audio` 内容类型）来转录音频文件。该功能适用于任何支持音频处理的模型。

## 快速入门

```bash
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a
```

转录结果会输出到标准输出（stdout）。

## 有用的参数/标志

```bash
# Custom model (default: google/gemini-2.5-flash)
{baseDir}/scripts/transcribe.sh audio.ogg --model openai/gpt-4o-audio-preview

# Custom instructions
{baseDir}/scripts/transcribe.sh audio.m4a --prompt "Transcribe with speaker labels"

# Save to file
{baseDir}/scripts/transcribe.sh audio.m4a --out /tmp/transcript.txt

# Custom caller identifier (for OpenRouter dashboard)
{baseDir}/scripts/transcribe.sh audio.m4a --title "MyApp"
```

## 工作原理

1. 使用 ffmpeg 将音频文件转换为 WAV 格式（单声道，16kHz）。
2. 对音频文件进行 Base64 编码。
3. 使用 `input_audio` 参数将编码后的音频数据发送到 OpenRouter 的聊天补全服务。
4. 从响应中提取转录结果。

## API 密钥

请设置环境变量 `OPENROUTER_API_KEY`，或在 `~/.clawdbot/clawdbot.json` 文件中进行配置：

```json5
{
  skills: {
    "openrouter-transcribe": {
      apiKey: "YOUR_OPENROUTER_KEY"
    }
  }
}
```

## 请求头

脚本会向 OpenRouter 发送以下识别信息：
- `X-Title`：调用者名称（默认值：“Peanut/Clawdbot”）
- `HTTP-Referer`：引用 URL（默认值：“https://clawdbot.com”）

这些信息会显示在 OpenRouter 的控制面板中，便于追踪请求来源。

## 常见问题及解决方法

- **ffmpeg 格式错误**：脚本会使用临时文件夹来保存音频文件（而非使用 `mktemp -t file.wav` 命令），因为 macOS 的 `mktemp` 命令会在文件扩展名后添加随机后缀，导致格式识别失败。
- **参数列表过长**：较大的音频文件会产生过长的 Base64 编码字符串，超出 shell 的参数长度限制。此时脚本会将音频数据写入临时文件（使用 `--rawfile` 参数给 jq 命令，或使用 `@file` 参数给 curl 命令），而不是直接作为参数传递。
- **API 返回空响应**：如果收到 “Empty response from API”的错误信息，脚本会输出原始的 API 响应内容以帮助调试。常见原因包括：
  - API 密钥无效
  - 所选模型不支持音频输入
  - 音频文件过大或损坏