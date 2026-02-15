---
name: mlx-whisper
version: 1.0.0
description: 使用 MLX Whisper 实现本地语音转文本功能（针对 Apple Silicon 优化，无需 API 密钥）。
homepage: https://github.com/ml-explore/mlx-examples/tree/main/whisper
metadata: {"clawdbot":{"emoji":"🍎","requires":{"bins":["mlx_whisper"]},"install":[{"id":"pip","kind":"pip","package":"mlx-whisper","bins":["mlx_whisper"],"label":"Install mlx-whisper (pip)"}]}}
---

# MLX Whisper

这是一个使用 Apple MLX 技术实现的本地语音转文本工具，专为 Apple Silicon Mac 电脑优化设计。

## 快速入门

```bash
mlx_whisper /path/to/audio.mp3 --model mlx-community/whisper-large-v3-turbo
```

## 常见用法

```bash
# Transcribe to text file
mlx_whisper audio.m4a -f txt -o ./output

# Transcribe with language hint
mlx_whisper audio.mp3 --language en --model mlx-community/whisper-large-v3-turbo

# Generate subtitles (SRT)
mlx_whisper video.mp4 -f srt -o ./subs

# Translate to English
mlx_whisper foreign.mp3 --task translate
```

## 模型（首次使用时需要下载）

| 模型 | 大小 | 转换速度 | 转换质量 |
|-------|------|---------|---------|
| mlx-community/whisper-tiny | 约 75MB | 最快 | 基础质量 |
| mlx-community/whisper-base | 约 140MB | 快速 | 良好质量 |
| mlx-community/whisper-small | 约 470MB | 中等质量 | 更佳效果 |
| mlx-community/whisper-medium | 约 1.5GB | 转换速度稍慢 | 优秀质量 |
| mlx-community/whisper-large-v3 | 约 3GB | 转换速度最慢 | 最佳质量 |
| mlx-community/whisper-large-v3-turbo | 约 1.6GB | 转换速度较快 | 极佳质量（推荐使用） |

## 注意事项

- 仅支持运行在 Apple Silicon Mac（M1/M2/M3/M4）上。
- 所有模型数据会被缓存到 `~/.cache/huggingface/` 目录中。
- 默认使用的模型是 `mlx-community/whisper-tiny`；如需最佳效果，请使用 `--model mlx-community/whisper-large-v3-turbo` 参数。