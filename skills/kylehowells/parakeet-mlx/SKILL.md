---
name: parakeet-mlx
description: 使用 Parakeet MLX（ASR）在 Apple Silicon 设备上进行本地语音转文本功能（无需 API 密钥）。
homepage: https://github.com/senstella/parakeet-mlx
metadata: {"clawdbot":{"emoji":"🦜","requires":{"bins":["parakeet-mlx"]},"install":[{"id":"uv-tool","kind":"uv","formula":"parakeet-mlx","bins":["parakeet-mlx"],"label":"Install Parakeet MLX CLI (uv tool install)"}]}}
---

# Parakeet MLX (命令行接口)

使用 `parakeet-mlx` 可以在 Apple Silicon 平台上本地转录音频文件。

**快速入门：**
- `parakeet-mlx /path/audio.mp3 --output-format txt` ：将音频文件转录为文本格式。
- `parakeet-mlx /path/audio.m4a --output-format vtt --highlight-words`：将音频文件转录为 VTT 格式，并突出显示其中的关键词。
- `parakeet-mlx *.mp3 --output-format all`：将所有指定的 MP3 文件同时转录为多种格式（txt、srt、vtt 或 json）。

**注意事项：**
- 使用以下命令安装 CLI：`uv tool install parakeet-mlx -U`（而非 `uv add` 或 `pip install`）。
- 使用 `parakeet-mlx --help` 查看所有可用选项（注意使用 `--help`，而非 `-h`）。
- 首次运行时，模型会从 Hugging Face 下载到 `~/.cache/huggingface` 目录中。
- 默认使用的模型是 `mlx-community/parakeet-tdt-0.6b-v3`，该模型针对 Apple Silicon 平台进行了优化。
- 该工具需要 `ffmpeg` 来处理音频文件。
- 支持的输出格式包括 txt、srt、vtt 和 json。
- 使用 `--verbose` 选项可查看详细的处理进度和置信度评分结果。
- 支持批量处理文件（支持使用通配符，如 `*.mp3`）。