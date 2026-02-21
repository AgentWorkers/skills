---
name: imessage-voice-reply
description: 使用本地的Kokoro-ONNX TTS在iMessage中发送语音回复。该功能会生成原生的iMessage语音气泡（CAF/Opus格式），这些语音内容会直接与波形数据一起播放，而不会以文件附件的形式发送。适用于在收到语音消息时希望用语音回复、实现语音对语音的iMessage对话，或发送音频回应的场景。完全免费——所有TTS处理都在本地完成。需要先在OpenClaw中配置BlueBubbles频道。
---
# iMessage 语音回复

使用本地的 Kokoro TTS 生成并发送原生的 iMessage 语音消息。这些语音消息会以内联可播放的形式显示，带有波形图——与在 Messages.app 中录制的语音消息完全相同。

## 工作原理

```
Your text response → Kokoro TTS (local) → afconvert (native Apple encoder) → CAF/Opus → BlueBubbles → iMessage voice bubble
```

## 设置

```bash
bash ${baseDir}/scripts/setup.sh
```

需要安装的软件：kokoro-onnx、soundfile、numpy。Kokoro 模型（约 136MB）会下载到 `~/.cache/kokoro-onnx/` 目录中。

**要求：** OpenClaw 中必须配置了 BlueBubbles 通道（`channels.bluebubbles`）。

## 生成并发送语音回复

### 第一步：生成音频文件

```bash
${baseDir}/.venv/bin/python ${baseDir}/scripts/generate_voice_reply.py "Your response text here" /tmp/voice_reply.caf
```

可选参数：
- `--voice af_heart` — 使用 Kokoro 的女性语音（默认：af_heart）
- `--speed 1.15` — 播放速度（默认：1.15）
- `--lang en-us` — 语言代码（默认：en-us）

### 第二步：通过 BlueBubbles 发送

使用 `message` 工具进行发送：

```json
{
  "action": "sendAttachment",
  "channel": "bluebubbles",
  "target": "+1XXXXXXXXXX",
  "path": "/tmp/voice_reply.caf",
  "filename": "Audio Message.caf",
  "contentType": "audio/x-caf",
  "asVoice": true
}
```

**生成原生语音消息的关键参数：**
- `filename` 必须为 `"Audio Message.caf"`
- `contentType` 必须为 `"audio/x-caf"`
- `asVoice` 必须设置为 `true`

这三个参数都是必需的，以便 iMessage 能将消息显示为带有波形图的内联语音消息，而不是文件附件。

## 语音选项

| 语言 | 女性 | 男性 |
|----------|--------|------|
| 英语 | af_heart ⭐ | am_puck |
| 西班牙语 | ef_dora | em_alex |
| 法语 | ff_siwis | — |
| 日语 | jf_alpha | jm_beta |
| 中文 | zf_xiaobei | zm_yunjian |

## 何时使用语音回复

- 当用户向你发送语音消息时
- 当用户明确要求你提供音频/语音回复时

请务必在语音消息旁边附上文字回复，以确保信息的可访问性。

## 音频格式

- **macOS：** 使用 CAF 容器格式，Opus 编解码器，48kHz 单声道，32kbps — 由 Apple 的内置 `afconvert` 工具进行编码。这与 Messages.app 生成的格式相同。
- **备用方案：** 使用 ffmpeg 将音频文件转换为 MP3 格式（虽然可以发送，但可能无法在所有版本的 iMessage 中显示为原生语音消息）。

## 成本

免费。Kokoro TTS 完全在本地运行，无需进行任何 API 调用。

## 常见问题解决方法

- **语音消息显示为文件附件**：请确保设置了以下三个参数：`filename="Audio Message.caf"`、`contentType="audio/x-caf"`、`asVoice=true`。
- **首词被截断**：脚本会自动在音频文件前添加 150 毫秒的静音片段。如果仍然存在截断现象，请增加脚本中的静音时长。
- **Kokoro 模型未找到**：运行 `bash ${baseDir}/scripts/setup.sh` 进行配置。
- **afconvert 未找到**：该工具仅适用于 macOS。在 Linux 上，脚本会自动切换到使用 ffmpeg/MP3 格式进行音频处理。