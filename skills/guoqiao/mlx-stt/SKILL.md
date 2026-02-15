---
name: mlx-stt
description: 使用 MLX（苹果自研的硅芯片）以及开源模型（默认为 GLM-ASR-Nano-2512）实现语音转文本功能，并在本地进行处理。
version: 1.0.7
author: guoqiao
metadata: {"openclaw":{"always":true,"emoji":"🦞","homepage":"https://github.com/guoqiao/skills/blob/main/mlx-stt/mlx-stt/SKILL.md","os":["darwin"],"requires":{"bins":["brew"]}}}
triggers:
- "/mlx-stt <audio>"
- "STT ..."
- "ASR ..."
- "Transcribe ..."
- "Convert audio to text ..."
---

# MLX STT

使用 MLX（基于苹果硅架构）和开源模型（默认为 GLM-ASR-Nano-2512）实现语音转文本（Speech-to-Text/Automatic Speech Recognition/Transcribe）功能，支持本地运行。

完全免费且准确，无需 API 密钥或服务器。

## 系统要求

- 系统：安装了苹果硅架构的 macOS。
- 必需安装 `brew` 工具，用于在缺少某些依赖库时自动安装它们。

## 安装

```bash
bash ${baseDir}/install.sh
```
如果系统缺少以下工具，此脚本会使用 `brew` 来安装它们：
- `ffmpeg`：用于在需要时转换音频格式。
- `uv`：用于安装 Python 包并运行相关 Python 脚本。
- `mlx_audio`：负责执行实际的语音转文本处理任务。

## 使用方法

要转录一个音频文件，请运行以下脚本：

```bash
bash  ${baseDir}/mlx-stt.sh <audio_file_path>
```

- 首次运行时可能会稍慢，因为系统需要下载相关模型文件。
- 转录结果会直接输出到标准输出（stdout）中。