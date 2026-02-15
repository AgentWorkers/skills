---
name: tts-whatsapp
version: 1.0.0
description: 您可以使用该功能在 WhatsApp 上以 40 多种语言发送高质量的语音消息，并实现自动发送。
user-invocable: true
disable-model-invocation: false
tags:
  - whatsapp
  - tts
  - voice
  - messaging
  - multilingual
  - audio
author: Community
repository: https://github.com/clawdbot/clawdhub
---

# 🎙️ TTS WhatsApp - 支持40多种语言的语音消息

您可以使用该工具在WhatsApp上发送高质量的语音消息，系统会自动完成发送过程。支持40多种语言，包括个人消息和群组广播。

## ✨ 主要功能

- 🎙️ **高质量的语音合成**：由Piper技术提供支持（支持40多种语言）
- 🎵 **自动转换格式**：将语音文件转换为WhatsApp支持的OGG/Opus格式
- 📤 **自动发送**：通过Clawdbot机器人完成发送
- 👥 **群组支持**：可以发送给单个用户或WhatsApp群组
- 🌍 **多语言支持**：包括法语、英语、西班牙语、德语等40多种语言
- 🧹 **智能清理**：发送成功后自动删除相关文件
- ⚡ **快速响应**：从接收命令到实际发送仅需2-3秒

## 📦 先决条件

1. **Piper TTS**：`pip3 install --user piper-tts`
2. **FFmpeg**：在macOS上使用`brew install ffmpeg`，在Linux上使用`apt install ffmpeg`
3. **语音模型**：请从[Hugging Face](https://huggingface.co/rhasspy/piper-voices)下载相应的语音模型，并将其放置在`~/.clawdbot/skills/piper-tts/models/`目录下
   - 例如：`fr_FR-siwis-medium.onnx`

## 🚀 快速入门

### 基本用法
```bash
tts-whatsapp "Hello, this is a test" --target "+15555550123"
```

### 向WhatsApp群组发送消息
```bash
tts-whatsapp "Hello everyone" --target "120363257357161211@g.us"
```

### 更改语言
```bash
tts-whatsapp "Hola mundo" --lang es_ES --voice carlfm --target "+34..."
```

### 调整语音质量
```bash
tts-whatsapp "High quality" --quality high --target "+1..."
```

## 🌍 支持的语言列表

- 🇫🇷 法语 (`fr_FR`): siwis, upmc, tom
- 🇬🇧 英语（英式） (`en_GB`): alan, alba
- 🇺🇸 英语（美式） (`en_US`): lessac, amy, joe
- 🇪🇸 西班牙语 (`es_ES`, `es_MX`): carlfm, davefx
- 🇩🇪 德语 (`de_DE`): thorsten, eva_k
- 🇮🇹 意大利语 (`it_IT`): riccardo
- 🇵🇹 葡萄牙语 (`pt_BR`, `pt_PT`): faber
- 🇳🇱 荷兰语 (`nl_NL`): mls, rdh
- 🇷🇺 俄语 (`ru_RU`): dmitri, irina
- 以及更多语言！

[完整语言列表 →](https://rhasspy.github.io/piper-samples/)

## 🔧 配置说明

请在`~/.clawdbot/clawdbot.json`文件中进行配置：

```json
{
  "skills": {
    "entries": {
      "tts_whatsapp": {
        "enabled": true,
        "env": {
          "WHATSAPP_DEFAULT_TARGET": "+15555550123",
          "PIPER_DEFAULT_LANG": "en_US",
          "PIPER_DEFAULT_VOICE": "lessac",
          "PIPER_DEFAULT_QUALITY": "medium"
        }
      }
    }
  }
}
```

## 🎛️ 其他选项

```
--target NUMBER       WhatsApp number or group ID
--message TEXT        Text message with audio
--lang LANGUAGE       Language (default: fr_FR)
--voice VOICE         Voice name (default: auto)
--quality QUALITY     x_low, low, medium, high
--speed SPEED         Playback speed (default: 1.0)
--no-send            Don't send automatically
```

## 📊 性能说明

发送一条10秒长的消息的总耗时约为2.3秒：
- 语音合成时间：约1秒
- 格式转换时间：约0.2秒
- WhatsApp发送时间：约1秒

## 📚 完整文档

请参阅[README.md](README.md)以获取完整文档、使用示例和故障排除方法。