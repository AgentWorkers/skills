---
name: aimlapi-voice
description: 使用 AIMLAPI 转录音频文件（格式包括 ogg、mp3、wav 等）。适用于用户提供音频消息或本地音频文件的情况。该工具提供了一个可靠的 Python 脚本，支持重试和轮询机制。
metadata:
  {
    "openclaw":
      {
        "emoji": "🎙️",
        "requires": { "bins": ["python"], "env": ["AIMLAPI_API_KEY"] },
        "primaryEnv": "AIMLAPI_API_KEY",
      },
  }
---
# AIMLAPI 语音转录

## 概述

这是一个强大的工具，通过 AIMLAPI 的专用语音转文本接口来实现音频转录功能。它支持任务排队、结果轮询以及自动检测 MIME 类型。

## 快速入门

```bash
# Set your API key first (if not in env)
# export AIMLAPI_API_KEY="your-key-here"

# Transcribe a file
python {baseDir}/scripts/transcribe.py path/to/audio.ogg
```

## 任务

### 处理语音消息

当接收到音频文件时，使用此脚本提取其中的文本。

```bash
python {baseDir}/scripts/transcribe.py <file_path> \
  --model "#g1_whisper-medium" \
  --verbose
```

### 参数

- `file`：（必填）音频文件的路径。
- `--model`：模型 ID（默认值：`#g1_whisper-medium`）。
- `--out`：保存转录文本的路径。
- `--poll-interval`：状态检查之间的间隔时间（以秒为单位）（默认值：5）。
- `--max-wait`：等待的最大时间（以秒为单位，超过此时间后将停止等待）（默认值：300）。

## 依赖项

- Python 3
- 环境变量中设置 `AIMLAPI_API_KEY`，或通过 `--apikey-file` 参数提供 API 密钥。