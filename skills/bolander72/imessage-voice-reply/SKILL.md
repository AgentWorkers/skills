---
name: imessage-voice-reply
version: 1.0.1
description: >
  **使用本地 Kokoro-ONNX TTS 在 iMessage 中发送语音消息回复**  
  该功能允许您使用 Kokoro-ONNX TTS 在 iMessage 中生成原生的语音消息（格式为 CAF/Opus），这些语音文件会直接嵌入到消息中并播放，而无需作为附件发送。适用于接收语音消息后希望用语音回复的情况，从而实现语音对语音的 iMessage 对话或发送音频回应。  
  **特点：**  
  - 全部语音转换过程在本地完成，无需额外费用。  
  - 需要在 OpenClaw 中配置 BlueBubbles 通道以使用该功能。  
  **使用方法：**  
  1. 当您在 iMessage 中收到语音消息时，选择“回复”选项。  
  2. 系统会自动启动 Kokoro-ONNX TTS，让您选择要使用的语音合成引擎（如 Kokoro-ONNX）。  
  3. 您可以选择预先录制的语音文件或使用实时语音合成功能来生成新的语音回复。  
  4. 生成的语音文件会以 CAF 或 Opus 格式嵌入到 iMessage 消息中，实现即时播放。  
  **适用场景：**  
  - 适用于希望实现语音交互的 iMessage 应用或功能。  
  **注意事项：**  
  - 请确保您的设备已安装并配置了适当的 TTS 插件（如 Kokoro-ONNX）。  
  - 不同设备或操作系统可能对 TTS 支持程度有所不同，请参考相关文档以获取详细信息。
---
# iMessage 语音回复

使用本地的 Kokoro TTS 生成并发送原生的 iMessage 语音消息。这些语音消息会以可播放的泡泡形式显示在聊天界面中，并附带波形图——与在 Messages.app 中录制的语音消息完全相同。

## 工作原理

```
Your text response → Kokoro TTS (local) → afconvert (native Apple encoder) → CAF/Opus → BlueBubbles → iMessage voice bubble
```

## 设置

```bash
bash ${baseDir}/scripts/setup.sh
```

需要安装的软件：kokoro-onnx、soundfile、numpy。Kokoro 模型（约 136MB）将被下载到 `~/.cache/kokoro-onnx/` 目录中。

**注意事项：** 需要在 OpenClaw 中配置 BlueBubbles 通道（`channels.bluebubbles`）。

## 生成并发送语音回复

### 第一步：生成音频文件

将回复内容写入临时文件，然后通过 `--text-file` 参数传递该文件，以避免 shell 注入风险：

```bash
echo "Your response text here" > /tmp/voice_text.txt
${baseDir}/.venv/bin/python ${baseDir}/scripts/generate_voice_reply.py --text-file /tmp/voice_text.txt --output /tmp/voice_reply.caf
```

或者，可以直接传递文本（请确保正确处理了 shell 转义字符）：

```bash
${baseDir}/.venv/bin/python ${baseDir}/scripts/generate_voice_reply.py --text "Your response text here" --output /tmp/voice_reply.caf
```

**可选参数：**
- `--voice af_heart` — 使用 Kokoro 的女性声音（默认值：af_heart）
- `--speed 1.15` — 播放速度（默认值：1.15）
- `--lang en-us` — 语言代码（默认值：en-us）

**安全提示：** 该 Python 脚本使用了 `argparse` 和 `subprocess.run`，并且不使用 `shell=True`。输入内容在脚本内部得到了安全处理。如果从 shell 中调用该脚本，请使用 `--text-file` 参数来处理不可信的输入，以避免 shell 元字符问题。

### 第二步：通过 BlueBubbles 发送消息

使用 `message` 工具发送消息：

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

这三个参数都是必需的，这样才能让 iMessage 将消息显示为带有波形图的内联语音泡泡，而不是文件附件。

## 可用的语音选项

| 语言 | 女性声音 | 男性声音 |
|----------|--------|------|
| 英语 | af_heart ⭐ | am_puck |
| 西班牙语 | ef_dora | em_alex |
| 法语 | ff_siwis | — |
| 日语 | jf_alpha | jm_beta |
| 中文 | zf_xiaobei | zm_yunjian |

## 何时使用语音回复

在以下情况下使用语音回复：
- 用户给你发送了语音消息时
- 用户明确要求你提供音频或语音回复时

请务必同时提供文字回复，以确保用户能够方便地理解信息。

## 音频格式

- **macOS：** 使用 CAF 容器格式，Opus 编解码器，48kHz 单声道，32kbps 的音频文件。这种格式与 Messages.app 生成的音频格式相同。
- **备用方案：** 可以使用 ffmpeg 将音频文件转换为 MP3 格式，但可能无法在所有版本的 iMessage 中显示为原生语音泡泡。

## 成本

完全免费。Kokoro TTS 的语音生成过程完全在本地完成，无需调用任何外部 API。

## 常见问题解决方法

- **语音消息显示为文件附件**：请确保设置了以下三个参数：`filename="Audio Message.caf"`、`contentType="audio/x-caf"`、`asVoice=true`。
- **首词被截断**：脚本会自动在音频开头添加 150 毫秒的静音。如果仍然存在截断现象，请在脚本中调整静音时长。
- **Kokoro 模型未找到**：运行 `bash ${baseDir}/scripts/setup.sh` 进行配置。
- **afconvert 未找到**：该工具仅适用于 macOS。在 Linux 系统上，脚本会自动切换到使用 ffmpeg/MP3 格式。