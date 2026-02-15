---
name: walkie-talkie
description: **功能说明：**  
该功能支持在 WhatsApp 上进行语音对语音的通话。系统会自动转录传入的语音，并使用本地的文本转语音（TTS）技术生成回应音频。非常适合用户希望在聊天时选择“说话”而非打字的情况。
---

# 对讲机模式（Walkie-Talkie Mode）

该功能利用本地转录技术和语音合成技术（TTS），实现WhatsApp上的语音对讲功能。

## 工作流程：

1. **接收音频消息**：当用户发送音频文件（格式为 `.audio`、`.ogg` 或 `.opus`）时：
   - 使用 `tools/transcribe_voice.sh` 命令将音频文件转换为文本。
   - 将转换后的文本作为普通用户提示信息进行处理。

2. **发送语音回复**：
   - 不使用文本回复，而是通过 `bin/sherpa-onnx-tts` 命令将文本转换为语音。
   - 将生成的语音文件（格式为 `.ogg`）作为语音消息发送回用户。

## 触发条件：
- 用户发送音频消息。
- 用户输入指令 “activa modo walkie-talkie” 或 “hablemos por voz”。

## 限制条件：
- 仅使用本地工具（`ffmpeg`、`whisper-cpp`、`sherpa-onnx-tts`）。
- 确保响应时间快速（RTF < 0.5 秒）。
- 必须同时发送文本和语音回复，以便用户更清晰地接收信息。

## 手动执行方式（内部操作）：
若需要手动发送语音回复，请执行以下操作：
```bash
bin/sherpa-onnx-tts /tmp/reply.ogg "Tu mensaje aquí"
```
然后通过 `message` 工具，使用 `filePath` 参数发送 `/tmp/reply.ogg` 文件作为语音回复。