---
name: audio-transcriber
description: 使用 Groq 的 Whisper API 来转录音频文件（快速且基于云端）。适用于用户发送语音消息、音频文件（ogg、mp3、wav、m4a 等）或请求语音转文字服务的场景。需要设置 GROQ_API_KEY 环境变量。
---

# 音频转录器

## 概述

该技能利用 Groq 的 Whisper API 实现快速音频转录功能。转录过程在云端完成，通过 Groq 的基础设施进行处理，因此比使用本地 Whisper 模型能够获得更快的结果。

## 快速入门

当用户发送音频文件或语音消息时：

1. 确保环境变量中已设置 `GROQ_API_KEY`。
2. 使用 `scripts/transcribe.py` 脚本：`scripts/transcribe.py /path/to/audio.ogg`
3. 将转录后的文本返回给用户。

## 使用方法

### 基本转录

```bash
export GROQ_API_KEY="your-key-here"
python3 /path/to/audio-transcriber/scripts/transcribe.py /path/to/audio.ogg
```

该脚本：
- 支持所有音频格式（ogg、mp3、wav、m4a 等）。
- 如果安装了 ffmpeg，会自动将音频文件转换为 WAV 格式（16kHz、单声道）。
- 将转换后的音频文件发送到 Groq 的 Whisper API 进行转录。
- 将转录结果以纯文本形式输出到标准输出（stdout）。

### 支持的音频格式

- **语音消息**：OGG（来自 Telegram、Signal 等平台）。
- **常见格式**：MP3、WAV、M4A、FLAC、AAC。
- **容器格式**：如果安装了 ffmpeg，脚本会自动进行格式转换。
- **未安装 ffmpeg 的情况**：仅支持 WAV 格式的音频文件。

## 设置要求

使用该技能需要配置以下内容：

### 1. Groq API 密钥

从 https://console.groq.com/ 获取 API 密钥，并将其设置为环境变量：

```bash
export GROQ_API_KEY="your-key-here"
```

若需永久保存设置，请将其添加到 shell 配置文件（如 ~/.zshrc 或 ~/.bashrc）中：

```bash
echo 'export GROQ_API_KEY="your-key-here"' >> ~/.zshrc
```

### 2. ffmpeg（推荐）

```bash
brew install ffmpeg
```

如果未安装 ffmpeg，仅支持 WAV 格式的音频文件。ffmpeg 用于在发送之前将其他格式的音频文件转换为 WAV 格式。

## 资源

### scripts/transcribe.py

主要转录脚本，包含以下功能：
- 验证 `GROQ_API_KEY` 环境变量的有效性。
- 检查是否安装了 ffmpeg（建议安装）。
- 根据需要将音频文件转换为 WAV 格式。
- 将音频文件发送到 Groq 的 Whisper API（使用 `whisper-large-v3` 模型）。
- 提取并输出转录后的纯文本。

可以直接从命令行运行该脚本，也可以通过 exec 工具来执行。

## 性能说明

- **速度**：比使用本地 Whisper 模型快得多（处理短音频文件通常不到 1 秒）。
- **模型**：通过 Groq API 使用 `whisper-large-v3` 模型，具有较高的转录准确性。
- **延迟**：基于云端服务，受网络连接影响。
- **费用**：Groq 提供免费 tier；请查看当前定价以了解使用限制。
- **准确性**：适用于一般语音转录需求，能够处理：
  - 多种口音和方言
  - 多个说话者的声音
  - 噪音环境中的语音
  - 技术术语

## 故障排除

### “未设置 GROQ_API_KEY 环境变量”
```bash
export GROQ_API_KEY="your-key-here"
```

### “未找到 ffmpeg”
```bash
brew install ffmpeg
```

### API 错误
- 确认您的 Groq API 密钥有效。
- 检查 Groq 账户的剩余使用额度。
- 检查网络连接是否正常。

## 安全提示

切勿将 `GROQ_API_KEY` 存储在版本控制系统中。建议使用环境变量或安全的密钥管理工具来存储该密钥。