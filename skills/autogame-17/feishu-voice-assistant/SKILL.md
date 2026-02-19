---
name: feishu-voice-assistant
description: 使用 Duby TTS 将语音消息（音频文件）发送到 Feishu 聊天中。
tags: [feishu, voice, tts, audio]
---
# Feishu 语音助手

使用 Duby AI 将文本转换为语音，并以原生语音消息（音频）的形式发送到 Feishu。

## 使用方法

### 发送语音消息
```bash
node skills/feishu-voice-assistant/index.js --text "Hello, this is a voice message!" --target "$TARGET_USER_ID"
```

### 参数选项
- `--text`：需要转换为语音的文本。
- `--target`：Feishu 用户 ID（格式为 `ou_...`）或聊天 ID（格式为 `oc_...`）。
- `--voice`：（可选）Duby 语音服务的 ID。默认值为 Xinduo。

## 所需依赖库
- `duby`：用于文本转语音（TTS）功能。
- `feishu-common`：用于 API 认证。
- `form-data`：用于文件上传。

## 配置要求
需要在 `.env` 文件中配置 `DUBY_API_KEY` 以及 Feishu 的认证信息。