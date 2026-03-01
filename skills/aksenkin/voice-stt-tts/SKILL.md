---
name: voice-stt-tts
description: 使用 faster-whisper 和 Edge TTS 为 OpenClaw 设置完整的语音消息功能（STT + TTS）
homepage: https://docs.openclaw.ai/nodes/audio
metadata:
  {
    "openclaw":
      {
        "emoji": "🎙️",
        "install": [
          {
            "id": "faster-whisper-venv",
            "kind": "bash",
            "label": "Install faster-whisper in venv",
            "command": "python3 -m venv ~/.openclaw/workspace/voice-messages && ~/.openclaw/workspace/voice-messages/bin/pip install faster-whisper"
          },
          {
            "id": "transcribe-script",
            "kind": "bash",
            "label": "Create transcribe.py script",
            "command": "cat > ~/.openclaw/workspace/voice-messages/transcribe.py << 'EOF'\n#!/usr/bin/env python3\nimport argparse\nfrom faster_whisper import WhisperModel\n\ndef transcribe(audio_path: str, model_name: str = \"small\", lang: str = \"en\", device: str = \"cpu\") -> str:\n    model = WhisperModel(\n        model_name,\n        device=device,\n        compute_type=\"int8\" if device == \"cpu\" else \"float16\",\n    )\n    segments, _ = model.transcribe(audio_path, language=lang, vad_filter=True)\n    text = \" \".join(seg.text.strip() for seg in segments if seg.text and seg.text.strip()).strip()\n    return text\n\ndef main():\n    p = argparse.ArgumentParser()\n    p.add_argument(\"--audio\", required=True)\n    p.add_argument(\"--model\", default=\"small\")\n    p.add_argument(\"--lang\", default=\"en\")\n    p.add_argument(\"--device\", default=\"cpu\", choices=[\"cpu\", \"cuda\"])\n    args = p.parse_args()\n    text = transcribe(args.audio, args.model, args.lang, args.device)\n    print(text if text else \"\")\nif __name__ == \"__main__\":\n    main()\nEOF"
          }
        ]
      }
  }
---
# OpenClaw的语音消息功能（STT + TTS）🎙️

通过使用**faster-whisper**进行语音转录，以及**Edge TTS**生成语音回复，实现完整的语音消息处理功能。

## 需要配置的内容

- ✅ **STT**（语音转文本）——使用faster-whisper将语音消息转录为文本
- ✅ **TTS**（文本转语音）——使用Edge TTS生成语音回复
- 🎯 **处理流程**：语音 → 文本 → 语音回复

---

## 安装过程

### 1. 创建虚拟环境（venv）

对于Ubuntu系统，创建一个隔离的虚拟环境：

```bash
python3 -m venv ~/.openclaw/workspace/voice-messages
```

### 2. 安装faster-whisper

在虚拟环境中安装相关包：

```bash
~/.openclaw/workspace/voice-messages/bin/pip install faster-whisper
```

**安装内容：**
- `faster-whisper`：用于语音转录的Python库
- 依赖库：`ctranslate2`、`onnxruntime`、`huggingface-hub`、`av`、`numpy`等
- 大小：约250 MB

---

## 转录脚本

### 脚本路径及内容

**文件路径：**`~/.openclaw/workspace/voice-messages/transcribe.py`

```python
#!/usr/bin/env python3
import argparse
from faster_whisper import WhisperModel


def transcribe(audio_path: str, model_name: str = "small", lang: str = "en", device: str = "cpu") -> str:
    model = WhisperModel(
        model_name,
        device=device,
        compute_type="int8" if device == "cpu" else "float16",
    )
    segments, _ = model.transcribe(audio_path, language=lang, vad_filter=True)
    text = " ".join(seg.text.strip() for seg in segments if seg.text and seg.text.strip()).strip()
    return text


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--audio", required=True)
    p.add_argument("--model", default="small")
    p.add_argument("--lang", default="en")
    p.add_argument("--device", default="cpu", choices=["cpu", "cuda"])
    args = p.parse_args()

    text = transcribe(args.audio, args.model, args.lang, args.device)
    print(text if text else "")


if __name__ == "__main__":
    main()
```

**脚本功能：**
1. 接受音频文件路径（参数`--audio`）
2. 加载Whisper模型（默认使用`small`模型）
3. 设置语言（参数`--lang`，例如`en`表示英语）
4. 使用VAD（语音活动检测）功能进行转录
5. 将转录后的文本输出到标准输出（stdout）

### 使脚本可执行

```bash
chmod +x ~/.openclaw/workspace/voice-messages/transcribe.py
```

---

## OpenClaw配置

### 1. 配置STT（`tools.media.audio`）

在`~/.openclaw/openclaw.json`文件中添加以下配置：

```json5
{
  "tools": {
    "media": {
      "audio": {
        "enabled": true,
        "maxBytes": 20971520,
        "models": [
          {
            "type": "cli",
            "command": "~/.openclaw/workspace/voice-messages/bin/python",
            "args": [
              "~/.openclaw/workspace/voice-messages/transcribe.py",
              "--audio",
              "{{MediaPath}}",
              "--lang",
              "en",
              "--model",
              "small"
            ],
            "timeoutSeconds": 120
          }
        ]
      }
    }
  }
}
```

**参数说明：**
| 参数 | 值 | 说明 |
|---------|------|---------|
| `enabled` | `true` | 启用语音转录功能 |
| `maxBytes` | `20971520` | 最大文件大小（20 MB） |
| `type` | `"cli"` | 模型类型（CLI命令） |
| `command` | Python脚本路径 | 虚拟环境中的Python脚本路径 |
| `args` | 命令参数 | 脚本的参数 |
| `{{MediaPath}}` | 占位符 | 将被替换为实际音频文件路径 |
| `timeoutSeconds` | `120` | 转录超时时间（2分钟） |

### 2. 配置TTS（`messages.tts`）

在`~/.openclaw/openclaw.json`文件中添加以下配置：

```json5
{
  "messages": {
    "tts": {
      "auto": "inbound",
      "provider": "edge",
      "edge": {
        "voice": "en-US-JennyNeural",
        "lang": "en-US"
      }
    }
  }
}
```

**参数说明：**
| 参数 | 值 | 说明 |
|---------|------|---------|
| `auto` | `"inbound"` | **关键设置！**——仅对传入的语音消息生成语音回复 |
| `provider` | `"edge"` | TTS服务提供商（免费，无需API密钥） |
| `voice` | `"en-US-JennyNeural"` | 可选语音源（例如：JennyNeural） |
| `lang` | `"en-US"` | 语言设置（en-US表示美式英语） |

### 完整配置示例

```json5
{
  "tools": {
    "media": {
      "audio": {
        "enabled": true,
        "maxBytes": 20971520,
        "models": [
          {
            "type": "cli",
            "command": "~/.openclaw/workspace/voice-messages/bin/python",
            "args": [
              "~/.openclaw/workspace/voice-messages/transcribe.py",
              "--audio",
              "{{MediaPath}}",
              "--lang",
              "en",
              "--model",
              "small"
            ],
            "timeoutSeconds": 120
          }
        ]
      }
    },
  },
  "messages": {
    "tts": {
      "auto": "inbound",
      "provider": "edge",
      "edge": {
        "voice": "en-US-JennyNeural",
        "lang": "en-US"
      }
    },
    "ackReactionScope": "group-mentions"
  }
}
```

---

## 应用配置更改

### 重启OpenClaw的网关服务

```bash
# Method 1: via openclaw CLI
openclaw gateway restart

# Method 2: via systemd
systemctl --user restart openclaw-gateway

# Check status
systemctl --user status openclaw-gateway
# Should show: active (running)
```

---

## 测试

### 测试STT（语音转文本）

**操作步骤：**向您的Telegram机器人发送语音消息

**预期结果：**
```
[Audio] User text: [Telegram ...] <media:audio> Transcript: <transcribed text>
```

**示例回复：**
```
[Audio] User text: [Telegram kd (@someuser) id:12345678 +5s ...] <media:audio> Transcript: Hello. How are you?
```

### 测试TTS（语音回复）

**操作步骤：**在语音消息成功转录后，机器人应发送语音回复

**预期结果：**
- 音频文件会发送到Telegram中
- 会显示一个语音回复提示（圆形气泡）

**预期行为：**
- 收到语音消息时，机器人会以语音形式回复
- 收到文本消息时，机器人仍会以文本形式回复（这是正常行为！）

---

## 可用的Edge TTS语音源

### 女性语音

| 语音源 | ID | 适用场景 |
|--------|-----|------------------|
| Jenny | `en-US-JennyNeural` | 当前默认语音 |
| Ana | `en-US-AnaNeural` | 更柔和的语音 |

### 男性语音

| 语音源 | ID | 适用场景 |
|--------|-----|------------------|
| Dmitry | `en-US-RogerNeural` | 低沉的男性语音 |

**如何更换语音源：**
```bash
cat ~/.openclaw/openclaw.json | \
  jq '.messages.tts.edge.voice = "en-US-MichelleNeural"' > ~/.openclaw/openclaw.json.tmp
mv ~/.openclaw/openclaw.json.tmp ~/.openclaw/openclaw.json
systemctl --user restart openclaw-gateway
```

## Edge TTS的其他参数

### 调整语音速度、音调和音量

```json5
{
  "messages": {
    "tts": {
      "edge": {
        "voice": "en-US-JennyNeural",
        "lang": "en-US",
        "rate": "+10%",      // Speed: -50% to +100%
        "pitch": "-5%",     // Pitch: -50% to +50%
        "volume": "+5%"     // Volume: -100% to +100%
      }
    }
  }
}
```

---

## 故障排除

### 问题：语音无法转录

**日志提示：**
```
[ERROR] Transcription failed
```

**可能原因：**
1. **文件过大**（超过20 MB） → 请检查文件大小。
   ```bash
   # Solution: Increase maxBytes in config
   maxBytes: 52428800  # 50 MB
   ```

2. **转录超时**（超过2分钟） → 检查转录是否超时。
   ```bash
   # Solution: Increase timeoutSeconds
   timeoutSeconds: 180  # 3 minutes
   ```

3. **模型未下载**（首次运行时） → 确保模型已正确下载。
   ```bash
   # Solution: Wait while it downloads (1-2 minutes)
   # Models are cached in ~/.cache/huggingface/
   ```

### 问题：没有语音回复

**可能原因：**
1. **回复内容太短**（少于10个字符） → TTS可能忽略此类回复。
   - 这是正常现象。
2. **`auto: "inbound"`设置**：只有在接收到语音消息时才会生成语音回复。
   - 文本消息仍会以文本形式回复。
3. **Edge TTS服务不可用** → 检查TTS服务是否正常运行。
   ```bash
   # Check
   curl -s "https://speech.platform.bing.com/consumer/api/v1/tts" | head -c 100
   # If error — temporarily unavailable
   ```

---

## 性能测试

### 转录时间（Raspberry Pi 4/ARM平台）

| Whisper模型 | 预计时间 | 转录质量 |
|-----------|--------------|---------|
| `tiny` | 约5-10秒 | 转录速度较慢 |
| `base` | 约10-20秒 | 转录速度中等 |
| `small` | 约20-40秒 | 转录速度较快 |
| `medium` | 约40-80秒 | 转录速度较快 |
| `large` | 约80-160秒 | 转录速度最慢 |

**建议：**对于Raspberry Pi，建议使用`small`或`base`模型。`medium`和`large`模型会导致较慢的转录速度。

### Whisper模型的存储位置

```bash
~/.cache/huggingface/
```

模型会在首次运行时自动下载。

## 完成配置！🎉

完成以上步骤后：
1. `faster-whisper`已成功安装到虚拟环境中。
2. `transcribe.py`脚本已创建。
3. OpenClaw的STT和TTS功能已配置完成。
4. 网关服务已重启。
5. 语音消息功能现已可用。

现在，您的Telegram机器人可以：
- 🎙️ 接受语音输入并使用faster-whisper进行转录。
- 🎤 以语音形式回复用户。
- 💬 接受文本输入时，仍以文本形式回复用户。

---

**参考链接：**
- OpenClaw官方文档：https://docs.openclaw.ai
- TTS相关文档：https://docs.openclaw.ai/tts
- 音频相关文档：https://docs.openclaw.ai/nodes/audio
- 安装技能命令：`npx clawhub search voice`

---

*创建日期：2026-03-01，适用于OpenClaw 2026.2.26版本*