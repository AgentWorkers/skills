---
name: video-subtitle-generator
description: 使用 WhisperX 和 LLM 翻译功能生成视频字幕。在处理视频文件时，该工具可用于创建 `.srt` 格式的字幕文件。支持多语言转录（自动检测源语言）、翻译成任意目标语言以及生成双语字幕。
---
# 视频字幕生成工具

这是一个基于 WhisperX 构建的多语言视频字幕生成和翻译工具包。

## 主要功能

- **语音转录**：从视频中提取音频，并自动检测语言后将其转录为字幕。
- **多语言翻译**：将字幕从任意源语言翻译成可配置的目标语言。
- **双语字幕**：生成源语言和目标语言的双语字幕。

## 前提条件

- Python 3.9 或更高版本。
- [ffmpeg](https://ffmpeg.org/)（WhisperX 需要此工具来提取音频）。

```bash
# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg

# Windows (Chocolatey)
choco install ffmpeg

# Windows (Scoop)
scoop install ffmpeg
```

## 资源需求

在运行之前，请确保用户了解以下成本：

| 资源 | 详情 |
|----------|---------|
| **磁盘空间** | ffmpeg 约 80 MB；Python 包（如 torch、whisperx 等）约 2–5 GB；Whisper 模型文件大小在 39 MB 到 1.5 GB 之间 |
| **CPU / GPU** | WhisperX 会在本地运行模型推理。对于“中等”和“大型”模型，强烈建议使用 CUDA GPU。CPU 和 Apple MPS 也可以使用，但速度较慢 |
| **网络 / API**：翻译步骤会调用远程的 LLM API 并产生基于令牌的费用。一旦模型下载完成，转录步骤不需要网络连接 |

**在安装包或下载模型之前，请务必与用户确认**，因为这些操作会消耗存储空间和带宽。

**翻译需要使用 LLM API，会产生费用。** 在执行翻译步骤之前，请：
1. 询问用户 API 提供商、密钥和基础 URL；或展示自动检测到的配置供用户审核。
2. 告知用户翻译会调用远程 LLM 并会消耗令牌（即需要支付费用）。
3. **只有在用户明确确认提供商并同意费用后，才能继续进行翻译**。

## 使用方法

### 1. 环境设置

```bash
# Install dependencies (requires ~2–5 GB disk space for PyTorch and WhisperX)
pip install -r requirements.txt

# Set the API key (used for translation)
# macOS / Linux
export OPENAI_API_KEY="your-api-key"
export OPENAI_BASE_URL="https://openrouter.ai/api/v1"  # Optional, defaults to OpenRouter

# Windows (PowerShell)
$env:OPENAI_API_KEY="your-api-key"
$env:OPENAI_BASE_URL="https://openrouter.ai/api/v1"
```

> 在 Windows 上，所有命令中请使用 `python` 而不是 `python3`。

### 2. 转录视频（自动检测语言）

```bash
python3 scripts/transcribe.py "/path/to/video.mp4" -o ./output -m small
```

输出文件：`video.{检测到的语言}.srt`（例如：`video.en.srt`、`video.ja.srt`）

参数：
- `-o`：输出目录
- `-m`：模型大小（`tiny`、`base`、`small`、`medium`、`large`）
- `-d`：运行设备（`cuda`、`cpu`、`mps`），默认为自动检测
- `-l`：强制指定源语言代码（例如：`en`、`ja`、`zh`）。如果省略则自动检测

### 3. 批量处理目录

```bash
python3 scripts/transcribe.py "/path/to/video/folder" -o ./output -m small
```

### 4. 翻译字幕

> **费用提示**：此步骤会调用远程 LLM API。请确保用户在运行前已确认 API 提供商、密钥及相关费用信息。

```bash
# Translate to Chinese (default)
python3 scripts/translate.py ./output -o ./translated

# Translate to Japanese
python3 scripts/translate.py ./output -o ./translated -t ja

# Only generate bilingual subtitles
python3 scripts/translate.py ./output -o ./translated --bilingual
```

参数：
- `-t`, `--target-lang`：目标语言代码（默认：`zh`）
- `--bilingual`：生成双语字幕（源语言 + 目标语言）
- `--target-only`：仅生成目标语言的字幕
- `--model`：翻译模型（默认：`google/gemini-3-flash-preview`）
- `--batch-size`：批量处理的大小（默认：`10`）

如果未指定 `--bilingual` 或 `--target-only`，则会同时生成双语和目标语言的字幕。

### 5. 运行完整流程

```bash
python3 scripts/run.py

# Customize via environment variables
VIDEO_DIR="/path/to/videos" TARGET_LANG=en python3 scripts/run.py
```

`run.py` 的环境变量：
- `VIDEO_DIR`：视频源目录（默认：`./videos`）
- `OUTPUT_DIR`：转录输出目录（默认：`./output`）
- `TRANSLATED_DIR`：翻译输出目录（默认：`./translated`）
- `TARGET_LANG`：目标语言代码（默认：`zh`）
- `WHISPER_MODEL`：Whisper 模型大小（默认：`medium`）

## 模型选择

| 模型 | 大小 | 速度 | 精确度 | 适用场景 |
|------|------|------|--------|----------|
| tiny | 39 MB | 最快 | 一般 | 快速测试 |
| base | 74 MB | 快速 | 良好 | 实时使用 |
| small | 244 MB | 中等 | 良好 | **推荐** |
| medium | 769 MB | 较慢 | 非常好 | 更高质量 |
| large | 1550 MB | 最慢 | 最佳 | 专业用途 |

## 输出文件

对于每个视频，该工具会生成以下文件：
- `*.{语言}.srt`：源语言字幕（语言自动检测，例如：`video.en.srt`）
- `*.json`：包含时间戳的完整转录数据
- `*.bilingual.srt`：翻译后的双语字幕（源语言 + 目标语言）
- `*.{目标语言}.srt`：翻译后的目标语言字幕（例如：`video.zh.srt`）

## 脚本概述

### scripts/transcribe.py

使用 WhisperX 进行语音转录，支持：
- 自动检测源语言（或通过 `-l` 参数手动指定）
- 时间戳对齐
- 支持跨文件批量处理并重用模型

### scripts/translate.py

使用 LLM API 进行字幕翻译，支持：
- 可配置的目标语言（`-t` 参数）
- 为了提高效率支持批量翻译
- 可生成双语或仅目标语言的字幕
- 支持自定义模型和 API 端点
- 在 API 失败时自动重试并采用指数级退避策略

### scripts/run.py

这是一个跨平台的命令行工具，可以自动执行转录和翻译流程。路径、目标语言和模型大小可以通过环境变量进行配置。