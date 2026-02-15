---
name: kokoro-tts
description: 使用本地的Kokoro TTS引擎将文本转换为语音。当用户要求“朗读”某些内容、请求语音消息，或者希望将文本转换为语音时，可以使用此功能。
---

# Kokoro TTS

此技能允许您使用本地或远程的Kokoro-TTS实例生成高质量的人工智能语音。

## 配置

该技能使用`KOKORO_API_URL`环境变量来定位API的地址。

- **默认值：** `http://localhost:8880/v1/audio/speech`
- **配置方法：** 将`KOKORO_API_URL=http://your-server:port/v1/audio/speech`添加到您的`.env`文件或环境变量中。

## 使用方法

要生成语音，请运行随附的Node.js脚本。

### 命令

```bash
node skills/kokoro-tts/scripts/tts.js "<text>" [voice] [speed]
```

- **text**：要朗读的文本。请用引号括起来。
- **voice**：（可选）语音ID。默认值为`af_heart`。
- **speed**：（可选）语音速度（范围：0.25至4.0）。默认值为`1.0`。

### 示例

```bash
node skills/kokoro-tts/scripts/tts.js "Hello Ed, this is Theosaurus speaking." af_nova
```

### 输出结果

脚本将输出一行内容，开头为`MEDIA:`，后跟生成的MP3文件的路径。OpenClaw会自动获取该文件并将其作为音频附件发送。

示例输出：
`MEDIA: media/tts_1706745000000.mp3`

## 可用的语音

常见的语音选项：
- `af_heart`（默认值，女性，温暖音色）
- `af_nova`（女性，专业音色）
- `am_adam`（男性，低沉音色）
- `bf_alice`（英国女性）

如需完整列表，请参阅[references/voices.md]或查询API。