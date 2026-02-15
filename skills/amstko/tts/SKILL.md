---
name: tts
description: 使用 Hume AI（或 OpenAI）API 将文本转换为语音。当用户请求音频消息、语音回复，或希望以“自然语言”的方式听到某些内容时，可以使用该功能。
---

# 文本转语音（Text-to-Speech, TTS）

将文本转换为语音并生成音频文件（MP3格式）。

## Hume AI（推荐方案）

- **推荐语音**: `9e1f9e4f-691a-4bb0-b87c-e306a4c838ef`
- **密钥**: 存储在环境变量中，分别为 `HUME_API_KEY` 和 `HUME_SECRET_KEY`。

### 使用方法

```bash
HUME_API_KEY="..." HUME_SECRET_KEY="..." node {baseDir}/scripts/generate_hume_speech.js --text "Hello Jonathan" --output "output.mp3"
```

## OpenAI（旧版本）

- **推荐语音**: `nova`
- **使用方法**: `OPENAI_API_KEY="..." node {baseDir}/scripts/generate_speech.js --text "..." --output "..."`

## 通用说明

- 脚本会输出一条包含生成文件绝对路径的 `MEDIA:` 行。
- 可使用 `message` 工具将生成的音频文件发送给用户。