---
name: local-whisper-cpp
description: 使用 `whisper-cli`（whisper.cpp）实现本地语音转文本功能。
metadata:
  {
    "openclaw":
      {
        "emoji": "🌬️",
        "requires": { "bins": ["whisper-cli"] },
      },
  }
---
# Local Whisper (cpp)

使用 `whisper-cli` 和 `large-v3-turbo` 模型在本地转录音频文件。

## 使用方法

您可以使用以下封装脚本：
- `scripts/whisper-local.sh <音频文件>`

或者直接调用二进制文件：
- `whisper-cli -m /usr/share/whisper.cpp-model-large-v3-turbo/ggml-large-v3-turbo.bin -f <文件> -l auto -nt`

## 脚本

- **位置：** `scripts/whisper-local.sh`（位于 `skill` 文件夹内）
- **模型：** `/usr/share/whisper.cpp-model-large-v3-turbo/ggml-large-v3-turbo.bin`
- **GPU：** 可通过 `whisper-cli` 启用

## 设置

将模型下载到 `/usr/share/whisper.cpp-model-large-v3-turbo/` 目录：
```bash
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin?download=true -O /usr/share/whisper.cpp-model-large-v3-turbo/ggml-large-v3-turbo.bin
```