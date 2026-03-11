---
name: tts-router
description: 适用于 Apple Silicon 的本地 TTS（文本到语音）服务：可以拉取 TTS 模型、提供与 OpenAI 兼容的 API、合成语音以及克隆声音功能。当用户请求“生成语音”、“将文本转换为语音”、“启动 TTS 服务器”、“拉取 TTS 模型”、“克隆声音”或以某人的声音说话等功能时，均可使用该服务。适用于 macOS 系统。
---
# tts-router — 适用于 Apple Silicon 的本地 TTS（文本转语音）路由器

这是一个命令行工具（CLI），用于在 Apple Silicon（MLX）设备上管理和提供多个 TTS（文本转语音）模型。这些模型是从 HuggingFace Hub 下载的，并通过兼容 OpenAI 和 DashScope 的 API 进行服务的。

## 前提条件

- 安装了支持 Apple Silicon（M1/M2/M3/M4）的 macOS 系统。
- 安装了 `uv` 工具：请参考 [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/) 进行安装（例如：`brew install uv` 或使用官方安装程序）。
- 安装了 `ffmpeg` 工具：`brew install ffmpeg`。

## 安装

```bash
# From PyPI (requires --prerelease=allow due to mlx-audio upstream dep)
uvx --prerelease=allow tts-router list

# Or install with pip
pip install tts-router
```

## 命令

### `tts-router list` — 显示可用的模型

```bash
tts-router list
```

### `tts-router pull <model>` — 下载模型权重文件

```bash
tts-router pull qwen3-tts
tts-router pull kokoro
```

模型文件会被缓存到 `~/.cache/huggingface/hub/` 目录中，无需重复下载。

### `tts-router serve` — 启动 TTS API 服务器

```bash
# Default: qwen3-tts on port 8091
tts-router serve

# Custom model and port
tts-router serve --model kokoro --port 9000
```

在启动服务器之前，需要先下载相应的模型文件。

### `tts-router say` — 通过 CLI 合成语音

```bash
tts-router say "Hello world" -o hello.wav
tts-router say "Hello" --voice Vivian --model kokoro -o out.wav
```

## 可用模型

| 简称                | 功能                                      |
| ------------------ | ----------------------------------------------- |
| `qwen3-tts`        | 支持多语音源、情感表达、指令控制（默认模型）         |
| `qwen3-tts-design`     | 自由形式的语音描述功能                       |
| `qwen3-tts-clone`     | 基于参考音频进行语音克隆                     |
| `kokoro`           | 快速、轻量级的多语言语音服务                 |
| `dia`              | 支持多语音源对话、笑声/情感音效                   |
| `chatterbox`       | 支持 23 种语言、情感控制及语音克隆                |
| `orpheus`          | 具有情感标签的 TTS 服务                     |

## 代理（Agent）快速入门

```bash
# 1. Pull the default model
tts-router pull qwen3-tts

# 2. Start the server
tts-router serve

# 3. Generate speech (OpenAI format)
curl -X POST http://localhost:8091/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello world", "voice": "Vivian"}' \
  --output output.wav
```

## API 端点（在服务器运行时）

| 端点                          | 方法        | 描述                                      |
| ----------------------------- | ------------ | ----------------------------------------- |
| `GET /`                          | GET        | 提供测试用 UI                          |
| `POST /v1/audio/speech`      | POST        | 使用 OpenAI 技术进行语音合成                   |
| `GET /v1/audio/voices`      | GET        | 显示可用的语音资源                        |
| `GET /health`                        | GET        | 检查服务器运行状态                        |
| `POST /v1/audio/clone`      | POST        | 生成新语音克隆                         |
| `POST /v1/audio/references/upload` | POST        | 上传参考音频文件                         |
| `POST /v1/audio/references/from-url` | POST        | 通过 URL 下载参考音频                         |

## 高级用法

如需了解更复杂的工作流程，请参阅相关参考文档：

- **从任意 URL（如 YouTube、Bilibili、播客或直接音频链接）克隆语音** → 请阅读 [references/voice-cloning.md](https://docs.astral.sh/references/voice-cloning.md)
- **将 `tts-router` 作为 OpenClaw 的 TTS 提供者使用** → 请阅读 [references/openclaw.md](https://docs.astral.sh/references/openclaw.md)