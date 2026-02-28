---
name: voiceclaw
description: "OpenClaw代理的本地语音输入/输出功能：  
该功能利用内置的`whisper.cpp`模块转录传入的音频/语音消息，并通过`piper`模块生成语音回复。系统需预先安装`whisper`、`piper`和`ffmpeg`软件。所有推理处理都在设备本地完成，无需网络调用或使用云服务API，也无需API密钥。  
适用场景：  
- 当代理接收到语音/音频消息时，需要同时以语音和文本形式进行回复；  
- 当需要将文本回复合成成音频形式发送时；  
- 适用于处理语音消息、音频附件，或执行“用语音回复”、“以音频形式发送”等操作。  
触发条件：  
- 收到语音消息；  
- 需要以语音形式回应；  
- 需要将文本内容转换为音频并发送。"
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["whisper", "piper", "ffmpeg"] },
        "network": "none",
        "env":
          [
            { "name": "WHISPER_BIN", "description": "Path to whisper binary (default: auto-detected via which)" },
            { "name": "WHISPER_MODEL", "description": "Path to ggml-base.en.bin model file (default: ~/.cache/whisper/ggml-base.en.bin)" },
            { "name": "PIPER_BIN", "description": "Path to piper binary (default: auto-detected via which)" },
            { "name": "VOICECLAW_VOICES_DIR", "description": "Path to directory containing .onnx voice model files (default: ~/.local/share/piper/voices)" }
          ]
      }
  }
---
# VoiceClaw

这是一个专为 OpenClaw 代理设计的本地语音输入/输出工具。

- **语音转文本（STT）：** `transcribe.sh` — 通过本地的 `whisper` 二进制文件将音频转换为文本。
- **文本转语音（TTS）：** `speak.sh` — 通过本地的 `piper` 二进制文件将文本转换为语音。
- **无需网络调用** — 这两个脚本均完全在本地运行。
- **不使用任何云服务或 API，也无需 API 密钥。**

---

## 先决条件

在使用此功能之前，系统上必须安装以下软件：

| 软件 | 用途 |
|---|---|
| `whisper` 二进制文件 | 语音转文本功能 |
| `ggml-base.en.bin` 模型文件 | `whisper` 的语音转文本（STT）模型 |
| `piper` 二进制文件 | 文本转语音（TTS）功能 |
| `.onnx` 格式的语音模型文件 | `piper` 的语音合成模型 |
| `ffmpeg` | 音频格式转换工具 |

有关安装和配置的详细说明，请参阅 **README.md**。

---

## 环境变量

| 变量 | 默认值 | 用途 |
|---|---|---|
| `WHISPER_BIN` | 通过 `which` 命令自动检测 | `whisper` 二进制文件的路径 |
| `WHISPER_MODEL` | `~/.cache/whisper/ggml-base.en.bin` | `whisper` 模型文件的路径 |
| `PIPER_BIN` | 通过 `which` 命令自动检测 | `piper` 二进制文件的路径 |
| `VOICECLAW_VOICES_DIR` | `~/.local/share/piper/voices` | 包含 `.onnx` 语音模型文件的目录 |

---

## 验证设置

```bash
which whisper && echo "STT binary: OK"
which piper   && echo "TTS binary: OK"
which ffmpeg  && echo "ffmpeg: OK"
ls "${WHISPER_MODEL:-$HOME/.cache/whisper/ggml-base.en.bin}" && echo "STT model: OK"
ls "${VOICECLAW_VOICES_DIR:-$HOME/.local/share/piper/voices}"/*.onnx 2>/dev/null | head -1 && echo "TTS voices: OK"
```

---

## 收到语音消息时的处理（语音转文本）

```bash
# Transcribe audio → text (supports ogg, mp3, m4a, wav, flac)
TRANSCRIPT=$(bash scripts/transcribe.sh /path/to/audio.ogg)
```

（此处应包含处理语音消息的逻辑代码）

---

## 发出语音消息时的处理（文本转语音）

```bash
# Step 1: Generate WAV (local Piper — no network)
WAV=$(bash scripts/speak.sh "Your response here." /tmp/reply.wav en_US-lessac-medium)

# Step 2: Convert to OGG Opus (Telegram voice requirement)
ffmpeg -i "$WAV" -c:a libopus -b:a 32k /tmp/reply.ogg -y -loglevel error

# Step 3: Send via message tool (filePath=/tmp/reply.ogg)
```

（此处应包含生成语音回复的代码）

---

## 可用的语音合成引擎

| 语音 | 风格 |
|---|---|
| `en_US-lessac-medium` | 中性美式发音（默认） |
| `en_US-amy-medium` | 温暖的美式女性音色 |
| `en_US-joe-medium` | 美式男性音色 |
| `en_US-kusal-medium` | 表现力强的美式男性音色 |
| `en_US-danny-low` | 沉稳的美式男性音色（低沉） |
| `en_GB-alba-medium` | 英国女性音色 |
| `en_GB-northern_english_male-medium` | 北方英式男性音色 |

---

## 代理行为规则

1. **接收语音消息时**：总是同时发送语音回复和文本回复。
2. **包含文本转录结果**：在每条针对语音消息的文本回复开头显示 “🎙️ 我听到了：[转录内容]”。
3. **保持语音回复简洁**：`piper` 的 TTS 功能在处理约 200 个单词以下的文本时效果最佳；对于语音消息，建议进行简要总结；对于文本消息，则提供详细内容。
4. **仅使用本地工具**：严禁使用任何云端的 TTS/STT 服务，必须使用本地的 `whisper` 和 `piper` 二进制文件。
5. **先发送音频文件**：先发送音频文件，再发送文本回复。

---

## 完整示例

```bash
# 1. Transcribe inbound voice message
TRANSCRIPT=$(bash path/to/voiceclaw/scripts/transcribe.sh /path/to/voice.ogg)

# 2. Compose reply and generate audio
RESPONSE="Deployment complete. All checks passed."
WAV=$(bash path/to/voiceclaw/scripts/speak.sh "$RESPONSE" /tmp/reply_$$.wav)
ffmpeg -i "$WAV" -c:a libopus -b:a 32k /tmp/reply_$$.ogg -y -loglevel error

# 3. Send voice + text
# message(action=send, filePath=/tmp/reply_$$.ogg, ...)
# reply: "🎙️ I heard: $TRANSCRIPT\n\n$RESPONSE"
```

---

## 故障排除

| 问题 | 解决方案 |
|---|---|
| `whisper` 命令未找到 | 确保 `whisper` 二进制文件已安装，并且位于系统的 `PATH` 环境变量中。 |
| `whisper` 模型文件未找到 | 设置 `WHISPER_MODEL` 变量为 `~/.cache/whisper/ggml-base.en.bin`。 |
| `piper` 命令未找到 | 确保 `piper` 二进制文件已安装，并且位于系统的 `PATH` 环境变量中。 |
| 语音模型文件缺失 | 设置 `VOICECLAW_VOICES_DIR` 变量为包含语音模型文件的目录。 |
| 在 Telegram 上无法播放 OGG 文件 | 确保在 `ffmpeg` 命令中使用了 `-c:a libopus` 标志。 |