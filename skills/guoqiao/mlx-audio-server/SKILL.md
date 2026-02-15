---
name: mlx-audio-server
description: 本地24/7全天候运行的OpenAI兼容API服务器，支持语音转文本（STT）和文本转语音（TTS）功能，由MLX技术驱动，可在您的Mac上使用。
metadata: {"openclaw":{"always":true,"emoji":"🦞","homepage":"https://github.com/guoqiao/skills/blob/main/mlx-audio-server/mlx-audio-server/SKILL.md","os":["darwin"],"requires":{"bins":["brew"]}}}
---

# MLX Audio Server

这是一个本地运行的、24小时不间断的OpenAI兼容API服务器，支持文本转语音（STT）和语音转文本（TTS）功能，由MLX框架在您的Mac上提供支持。

[mlx-audio](https://github.com/Blaizzy/mlx-audio): 基于Apple的MLX框架构建的最佳音频处理库，可在Apple Silicon平台上实现快速高效的语音转换功能。

[guoqiao/tap/mlx-audio-server](https://github.com/guoqiao/homebrew-tap/blob/main/Formula/mlx-audio-server.rb): 一个Homebrew公式，用于通过`brew`安装`mlx-audio`，并使其作为LaunchAgent服务在macOS上运行。

## 系统要求

- 必须使用搭载Apple Silicon的macOS系统。
- 需要安装`brew`，以便在缺少某些依赖库时进行自动安装。

## 安装过程

```bash
bash ${baseDir}/install.sh
```
该脚本将执行以下操作：
- 如果系统中缺少`ffmpeg`和`jq`，则使用`brew`进行安装。
- 从`guoqiao/tap`仓库安装`mlx-audio-server` Homebrew公式。
- 启动`mlx-audio-server`的`brew`服务。

## 使用方法

**文本转语音（STT）**（默认模型：**mlx-community/glm-asr-nano-2512-8bit**）:
```bash
# input will be converted to wav with ffmpeg, if not yet.
# output will be transcript text only.
bash ${baseDir}/run_stt.sh <audio_or_video_path>
```

**语音转文本（TTS）**（默认模型：**mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16**）:
```bash
# audio will be saved into a tmp dir, with default name `speech.wav`, and print to stdout.
bash ${baseDir}/run_tts.sh "Hello, Human!"
# or you can specify a output dir
bash ${baseDir}/run_tts.sh "Hello, Human!" ./output
# output will be audio path only.
```

您可以直接使用这两个脚本，也可以将它们作为参考示例。