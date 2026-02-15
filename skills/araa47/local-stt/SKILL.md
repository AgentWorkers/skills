---
name: local-stt
description: 本地语音转文本（STT）功能支持多种后端选择：Parakeet（准确率最高）或Whisper（转换速度最快，支持多语言）。
metadata: {"openclaw":{"emoji":"🎙️","requires":{"bins":["ffmpeg"]}}}
---

# 本地语音转文本（Parakeet / Whisper）

通过 ONNX Runtime 实现统一的本地语音转文本功能，并采用 int8 量化技术。您可以选择以下后端之一：

- **Parakeet**（默认）：针对英语具有最高的准确性，能够准确识别人名和填充词。
- **Whisper**：推理速度最快，支持 99 种语言。

## 使用方法

```bash
# Default: Parakeet v2 (best English accuracy)
~/.openclaw/skills/local-stt/scripts/local-stt.py audio.ogg

# Explicit backend selection
~/.openclaw/skills/local-stt/scripts/local-stt.py audio.ogg -b whisper
~/.openclaw/skills/local-stt/scripts/local-stt.py audio.ogg -b parakeet -m v3

# Quiet mode (suppress progress)
~/.openclaw/skills/local-stt/scripts/local-stt.py audio.ogg --quiet
```

## 参数选项

- `-b/--backend`：`parakeet`（默认），`whisper`
- `-m/--model`：模型版本（详见下文）
- `--no-int8`：禁用 int8 量化
- `-q/--quiet`：抑制进度显示
- `--room-id`：用于直接消息传递的房间 ID

## 模型

### Parakeet（默认后端）
| 模型 | 描述 |
|-------|-------------|
| **v2**（默认） | 仅支持英语，具有最高的准确性 |
| v3 | 支持多种语言 |

### Whisper
| 模型 | 描述 |
|-------|-------------|
| tiny | 推理速度最快，但准确性较低 |
| **base**（默认） | 性能与准确性之间的平衡较好 |
| small | 准确性更高 |
| large-v3-turbo | 转换质量最佳，但速度较慢 |

## 基准测试（24 秒音频）

| 后端/模型 | 处理时间 | RTF（实时转文本） | 备注 |
|---------------|------|-----|-------|
| Whisper Base int8 | 0.43 秒 | 0.018 倍 | 推理速度最快 |
| **Parakeet v2 int8** | 0.60 秒 | 0.025 倍 | 准确性最高 |
| Parakeet v3 int8 | 0.63 秒 | 0.026 倍 | 支持多种语言 |

## openclaw.json

```json
{
  "tools": {
    "media": {
      "audio": {
        "enabled": true,
        "models": [
          {
            "type": "cli",
            "command": "~/.openclaw/skills/local-stt/scripts/local-stt.py",
            "args": ["--quiet", "{{MediaPath}}"],
            "timeoutSeconds": 30
          }
        ]
      }
    }
  }
}
```