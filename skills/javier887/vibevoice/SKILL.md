---
name: vibevoice
description: 使用 Microsoft VibeVoice 实现本地西班牙语语音合成（TTS）。该功能可将文本转换为自然的语音音频，特别适用于 WhatsApp 的语音消息。
metadata:
  author: estudiosdurero
  version: "1.0.0"
  homepage: https://github.com/microsoft/VibeVoice
  openclaw:
    emoji: "🎙️"
    requires:
      bins: ["ffmpeg", "python3"]
      env: []
    install:
      - id: "vibevoice-clone"
        kind: "manual"
        label: "Clone VibeVoice repo and setup venv"
        instructions: |
          git clone https://github.com/microsoft/VibeVoice.git ~/VibeVoice
          cd ~/VibeVoice
          python3 -m venv venv
          source venv/bin/activate
          pip install -e .
          pip install torch torchaudio
---

# VibeVoice TTS

使用微软的VibeVoice模型实现本地文本转语音功能。该模型能够生成自然流畅的西班牙语语音音频，非常适合用于WhatsApp的语音消息。

## 快速入门

```bash
# Basic usage
{baseDir}/scripts/vv.sh "Hola, esto es una prueba" -o /tmp/audio.ogg

# From file
{baseDir}/scripts/vv.sh -f texto.txt -o /tmp/audio.ogg

# Different voice
{baseDir}/scripts/vv.sh "Texto" -v en-Wayne -o /tmp/audio.ogg

# Adjust speed (0.5-2.0)
{baseDir}/scripts/vv.sh "Texto" -s 1.2 -o /tmp/audio.ogg
```

## 配置

| 设置 | 默认值 | 说明 |
|---------|---------|-------------|
| 语音 | `sp-Spk1_man` | 西班牙男性语音（带有轻微的墨西哥口音） |
| 语速 | `1.15` | 比正常速度快15% |
| 格式 | `.ogg` | 使用Opus编码格式，兼容WhatsApp |

## 可用的语音

西班牙语：
- `sp-Spk1_man` - 男性语音（带有轻微的墨西哥口音，默认选择）

英语：
- `en-Wayne` - 男性语音
- `en-Denise` - 女性语音
- 其他语音可在 `~/VibeVoice/demo/voices/streaming_model/` 目录下找到

## 输出格式

- `.ogg` - Opus编码格式（兼容WhatsApp，推荐使用）
- `.mp3` - MP3格式
- `.wav` - 未压缩的WAV格式

## 在WhatsApp中使用

请务必使用`.ogg`格式，并在消息发送时设置 `asVoice=true`：

```bash
# Generate
{baseDir}/scripts/vv.sh "Tu mensaje aquí" -o /tmp/mensaje.ogg

# Send via message tool
message action=send channel=whatsapp to="+34XXXXXXXXX" filePath=/tmp/mensaje.ogg asVoice=true
```

## 系统要求

- **GPU**：NVIDIA显卡，建议显存容量约为2GB
- **VibeVoice**：需安装在 `~/VibeVoice` 目录下
- **ffmpeg**：用于音频转换
- **Python 3.10+**：需要安装 `torch` 和 `torchaudio` 库

## 性能

- 生成速度：约为实时速度的0.24倍
- 1分钟的音频文件大约需要15秒来生成

## 注意事项

- 首次运行时模型加载时间约为10秒，后续运行会更快
- 音频规则：仅当用户主动请求或通过语音输入时才会生成语音
- 为保证最佳音质，请将文本长度控制在1500个字符以内