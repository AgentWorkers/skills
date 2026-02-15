---
name: elevenlabs
description: 通过 ElevenLabs API 实现文本转语音、音效生成、音乐制作、语音管理以及配额检查等功能。适用于使用 ElevenLabs 生成音频或管理语音资源时。
version: 1.3.3
homepage: https://github.com/odrobnik/elevenlabs-skill
metadata:
  {
    "openclaw":
      {
        "emoji": "🔊",
        "requires": { "bins": ["python3", "ffmpeg", "afplay"], "python": ["requests"], "env": ["ELEVENLABS_API_KEY"] },
        "primaryEnv": "ELEVENLABS_API_KEY",
      },
  }
---

# ElevenLabs Skill

这是一组用于与 ElevenLabs API 相互操作的核心工具，支持声音生成、音乐处理和语音管理功能。

## 设置

有关先决条件和设置说明，请参阅 [SETUP.md](SETUP.md)。

## 模型

| 模型 | ID | 使用场景 |
|-------|----|----------|
| **Eleven v3** | `eleven_v3` | 非常适合用于表达性/创意性的音频处理。支持音频标签（方括号格式）：`[laughs]`、`[sighs]`、`[whispers]`、`[excited]`、`[grumpy voice]`、`[clears throat]` 等。适用于故事讲述、角色配音和演示场景。 |
| Multilingual v2 | `eleven_multilingual_v2` | 支持多语言处理，稳定性较高，但不支持音频标签。适合简单的叙述用途。 |
| Turbo v2.5 | `eleven_turbo_v2_5` | 低延迟，适用于非英语语言（如德语）的语音合成。实时对话场景必备。 |
| Flash v2.5 | `eleven_flash_v2_5` | 处理速度最快，成本最低。 |

### v3 音频标签（使用方括号，不支持 XML/SSML 格式）

标签可以放置在文本的任何位置，并可自由组合。v3 能够深度理解音频的情感背景。

## 输出格式

所有脚本都支持通过 `--format` 参数设置多种输出格式：

| 格式 | 描述 |
|--------|-------------|
| `mp3_44100_128` | MP3 格式，44.1kHz 音频，128kbps（默认格式） |
| `mp3_44100_192` | MP3 格式，44.1kHz 音频，192kbps |
| `mp3_44100_96` | MP3 格式，44.1kHz 音频，96kbps |
| `mp3_44100_64` | MP3 格式，44.1kHz 音频，64kbps |
| `mp3_44100_32` | MP3 格式，44.1kHz 音频，32kbps |
| `mp3_24000_48` | MP3 格式，24kHz 音频，48kbps |
| `mp3_22050_32` | MP3 格式，22.05kHz 音频，32kbps |
| `opus_48000_192` | Opus 格式，48kHz 音频，192kbps（适合 AirPlay） |
| `opus_48000_128` | Opus 格式，48kHz 音频，128kbps |
| `opus_48000_96` | Opus 格式，48kHz 音频，96kbps |
| `opus_48000_64` | Opus 格式，48kHz 音频，64kbps |
| `opus_48000_32` | Opus 格式，48kHz 音频，32kbps |
| `pcm_16000` | 原始 PCM 格式，16kHz 音频 |
| `pcm_22050` | 原始 PCM 格式，22.05kHz 音频 |
| `pcm_24000` | 原始 PCM 格式，24kHz 音频 |
| `alaw_8000` | A-law 格式，8kHz 音频（适用于电话通信） |

## 工具

### 1. Speech (`speech.py`)
使用 ElevenLabs 提供的语音库实现文本转语音功能。

### 2. Sound Effects (`sfx.py`)
用于生成音效和简短的音频片段。

### 3. Music Generation (`music.py`)
用于生成完整的音乐作品或器乐曲目。

### 4. Voices (`voices.py`)
用于列出可用的语音资源及其对应的 ID。

### 5. Voice Cloning (`voiceclone.py`)
根据音频样本即时生成语音克隆版本。

**安全注意事项：** 默认情况下，该脚本仅从以下目录读取文件：`~/.openclaw/elevenlabs/voiceclone-samples/`。请将您的音频样本文件复制到该目录中（或通过 `--sample-dir` 参数指定其他路径）。脚本禁止读取该目录之外的文件。

### 6. Quota & Usage (`quota.py`)
用于检查订阅配额和使用情况统计信息。

### 输出结果

输出结果将按照指定的格式生成相应的音频文件。