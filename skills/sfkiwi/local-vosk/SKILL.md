---
name: local-vosk
description: 使用 Vosk 进行本地语音转文本处理。该工具轻量级、运行速度快，且完全支持离线模式，非常适合转录 Telegram 的语音消息、音频文件，或任何不需要云服务的语音转文本任务。
---

# 本地 Vosk 语音转文本工具

这是一个基于 Vosk 的轻量级本地语音转文本工具，支持完全离线使用（模型下载完成后即可使用）。

## 使用场景

- **Telegram 语音消息**：自动转录 `.ogg` 格式的语音笔记  
- **音频文件**：支持任何 ffmpeg 能解码的音频格式  
- **离线转录**：无需 API 密钥，无需依赖云服务，完全免费  

## 快速入门

```bash
# Transcribe Telegram voice message
./skills/local-vosk/scripts/transcribe voice_message.ogg

# Transcribe any audio
./skills/local-vosk/scripts/transcribe audio.mp3

# With language (default: en-us)
./skills/local-vosk/scripts/transcribe audio.wav --lang en-us
```

## 支持的音频格式

任何 ffmpeg 能解码的音频格式：`.ogg`（Telegram 使用的格式）、mp3、wav、m4a、webm、flac 等  

## 模型

默认模型：`vosk-model-small-en-us-0.15`（大小约 40MB）  
更多模型可访问：https://alphacephei.com/vosk/models  

## 安装说明（如未安装）

```bash
pip3 install vosk --user --break-system-packages

# Download model
mkdir -p ~/vosk-models && cd ~/vosk-models
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
```

## 注意事项

- 适用于日常对话的语音转录，转录质量良好  
- 如需更高精度，可使用更大容量或性能更强的模型  
- 在普通硬件上，转录速度约为实时的 10 倍  
- Telegram 的语音消息为 `.ogg` 格式，可直接使用该工具进行转录