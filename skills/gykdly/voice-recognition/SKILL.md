---
name: voice-recognition
description: 使用 OpenAI Whisper CLI 进行本地语音转文本功能。支持中文、英文以及 100 多种语言的语音转文本服务，同时提供翻译和摘要功能。
version: 1.0.0
---

# 语音识别（Whisper）

使用 OpenAI Whisper CLI 进行本地语音转文本操作。

## 特点

- **本地处理**：无需 API 密钥，完全免费
- **多语言支持**：中文、英文及 100 多种语言
- **翻译功能**：可将其转换为英文
- **摘要生成**：可快速生成文本摘要

## 使用方法

### 基本用法

```bash
# Chinese recognition
python3 /Users/liyi/.openclaw/workspace/scripts/voice识别_升级版.py audio.m4a

# Force Chinese
python3 /Users/liyi/.openclaw/workspace/scripts/voice识别_升级版.py audio.m4a --zh

# English recognition  
python3 /Users/liyi/.openclaw/workspace/scripts/voice识别_升级版.py audio.m4a --en

# Translate to English
python3 /Users/liyi/.openclaw/workspace/scripts/voice识别_升级版.py audio.m4a --translate

# With summary
python3 /Users/liyi/.openclaw/workspace/scripts/voice识别_升级版.py audio.m4a --summarize
```

### 快速命令（添加到 ~/.zshrc 文件中）

```bash
alias voice="python3 /Users/liyi/.openclaw/workspace/scripts/voice识别_升级版.py"
```

之后，使用以下命令：

```bash
voice ~/Downloads/audio.m4a --zh
```

## 系统要求

- OpenAI Whisper CLI：`brew install openai-whisper`
- Python 3.10 或更高版本

## 相关文件

- `scripts/voice识别_升级版.py`：主要脚本
- `scripts/voice_tool_readME.md`：使用说明文档

## 支持的音频格式

- MP3、M4A、WAV、OGG、FLAC、WebM

## 语言支持

支持 100 多种语言，包括：
- 中文 (zh)
- 英文 (en)
- 日文 (ja)
- 韩文 (ko)
- 以及更多语言...

## 注意事项

- 默认模型：`medium`（在速度和准确性之间取得平衡）
- 首次运行时，系统会将模型下载到 `~/.cache/whisper` 目录
- 处理时间取决于音频长度和模型大小