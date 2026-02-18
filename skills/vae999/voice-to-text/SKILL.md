---
name: voice-to-text
version: 1.0.0
description: 使用 Vosk 的离线语音识别功能将语音消息和音频文件转换为文本。当用户发送语音消息或音频文件，或请求将语音内容转录为文本时，可以使用此功能。
homepage: https://alphacephei.com/vosk/
metadata:
  {
    "openclaw":
      {
        "emoji": "🎤",
        "os": ["darwin", "linux"],
        "requires": { "bins": ["ffmpeg"], "python": ["vosk"] },
        "install":
          [
            {
              "id": "brew-ffmpeg",
              "kind": "brew",
              "formula": "ffmpeg",
              "bins": ["ffmpeg"],
              "label": "Install ffmpeg via Homebrew",
            },
            {
              "id": "pip-vosk",
              "kind": "pip",
              "package": "vosk",
              "label": "Install Vosk via pip",
            },
          ],
      },
  }
---
# 语音转文本

使用 Vosk（一个离线语音识别工具包）将语音消息和音频文件转换为文本。

## 设置

1. 安装依赖项：
   ```bash
   # macOS
   brew install ffmpeg
   pip install vosk

   # Linux
   apt-get install ffmpeg
   pip install vosk
   ```

2. 下载 Vosk 模型：
   ```bash
   mkdir -p ~/.vosk/models && cd ~/.vosk/models

   # Chinese (small, fast)
   curl -LO https://alphacephei.com/vosk/models/vosk-model-small-cn-0.22.zip
   unzip vosk-model-small-cn-0.22.zip

   # English (small)
   curl -LO https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
   unzip vosk-model-small-en-us-0.15.zip
   ```

## 使用方法

当用户提供语音消息或音频文件路径时，运行以下命令进行转录：
```bash
python3 ~/skills/voice-to-text/transcribe.py "<audio_file_path>"
```

如需选择特定模型，请设置环境变量：
```bash
VOSK_MODEL_PATH=~/.vosk/models/vosk-model-cn-0.22 python3 ~/skills/voice-to-text/transcribe.py "<audio_file_path>"
```

## 支持的音频格式

- MP3、WAV、M4A、OGG、FLAC、AAC、WEBM
- 来自微信、Telegram、WhatsApp 等应用的语音消息

## 可用的模型

| 模型 | 语言 | 大小 | 说明 |
|-------|----------|------|-------|
| vosk-model-small-cn-0.22 | 中文 | 42MB | 速度快，准确率高 |
| vosk-model-cn-0.22 | 中文 | 1.3GB | 准确率高 |
| vosk-model-small-en-us-0.15 | 英文 | 40MB | 速度快，准确率高 |
| vosk-model-en-us-0.22 | 英文 | 1.8GB | 准确率高 |

模型下载地址：https://alphacephei.com/vosk/models

## 示例工作流程

1. 用户通过微信/Telegram 发送语音消息
2. OpenClaw 接收音频文件
3. 运行：`python3 transcribe.py /path/to/voice.ogg`
4. 将转录后的文本返回给用户

## 故障排除

- **找不到模型**：将模型下载到 `~/.vosk/models/` 目录下
- **找不到 ffmpeg**：通过 `brew install ffmpeg` 或 `apt install ffmpeg` 安装 ffmpeg
- **识别准确率低**：尝试使用更大的模型以获得更好的结果

## 注意事项

- 下载模型后即可完全离线使用
- 支持多种语言（下载相应的模型）
- 音频会被转换为 16kHz 单声道 WAV 格式进行处理