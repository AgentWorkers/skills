---
name: piper-tts
description: 使用 Piper 的 ONNX 语音库实现本地文本转语音功能——快速、私密，无需依赖云服务。
metadata: {"openclaw":{"emoji":"🔊","requires":{"bins":["ffmpeg"]}}}
---

# 本地文本转语音（Piper）

使用 [Piper](https://github.com/rhasspy/piper) 和 ONNX 语音模型实现快速本地文本转语音功能。完全离线运行，无需依赖云服务。支持多种语言和语音风格。

## 使用方法

```bash
# Default voice (en_US-amy-medium)
~/.openclaw/skills/piper-tts/scripts/piper-tts.py "Hello, how are you today?"

# Select a specific voice
~/.openclaw/skills/piper-tts/scripts/piper-tts.py "Guten Tag" -v de_DE-thorsten-medium

# Pipe text from stdin
echo "Read this aloud" | ~/.openclaw/skills/piper-tts/scripts/piper-tts.py -

# Custom output path and format
~/.openclaw/skills/piper-tts/scripts/piper-tts.py "Hello" -o greeting.mp3 -f mp3

# Adjust speaking rate and send to Matrix room
~/.openclaw/skills/piper-tts/scripts/piper-tts.py "Slow and steady" --rate 0.8 --room-id '!abc:matrix.org'

# List available downloaded voices
~/.openclaw/skills/piper-tts/scripts/piper-tts.py --list-voices

# Quiet mode (suppress progress)
~/.openclaw/skills/piper-tts/scripts/piper-tts.py "Hello" --quiet
```

## 参数选项

- `-v/--voice`：语音模型名称（默认：`en_US-amy-medium`）
- `-o/--output`：输出文件路径（默认：自动生成在 `/tmp` 目录）
- `-f/--format`：输出格式：`wav`、`mp3`、`ogg`（默认：`wav`）
- `--rate`：语速倍率（0.5–2.0，默认：1.0）
- `--room-id`：音频发送到的房间 ID
- `--list-voices`：列出已下载的语音模型
- `-q/--quiet`：抑制进度信息

## 语音模型

Piper 支持 60 多种语言的 900 多种语音模型（详见 [https://rhasspy.github.io/piper-samples/](https://rhasspy.github.io/piper-samples/)。首次使用时，语音模型会自动从 HuggingFace 下载。

### 常用语音模型

| 语音模型 | 语言 | 语音质量 |
|---------|--------|--------|
| `en_US-amy-medium`（默认） | 英语（美国） | 中等 |
| `en_US-lessac-high` | 英语（美国） | 高音质 |
| `en_GB-alba-medium` | 英语（英国） | 中等 |
| `de_DE-thorsten-medium` | 德语 | 中等 |
| `fr_FR-siwis-medium` | 法语 | 中等 |
| `es_ES-davefx-medium` | 西班牙语 | 中等 |

## 性能测试

| 语音质量 | 合成时间（100 个单词） | 相比 OpenClaw 的性能提升 |
|---------|-------------------|---------|
| 中等 | 约 0.3 秒 | 提升 0.04 倍 |
| 高音质 | 约 0.8 秒 | 提升 0.10 倍 |

## openclaw.json

```json
{
  "tools": {
    "media": {
      "tts": {
        "enabled": true,
        "models": [
          {
            "type": "cli",
            "command": "~/.openclaw/skills/piper-tts/scripts/piper-tts.py",
            "args": ["--quiet", "-f", "ogg", "-o", "{{OutputPath}}", "{{Text}}"],
            "timeoutSeconds": 30
          }
        ]
      }
    }
  }
}
```