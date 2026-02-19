---
name: text-to-speech
description: "通过 `inference.sh` CLI，您可以使用 DIA TTS、Kokoro、Chatterbox 等工具将文本转换为自然语言语音。支持的模型包括：DIA TTS（对话式）、Kokoro TTS、Chatterbox、Higgs Audio、VibeVoice（用于播客）。这些工具具备以下功能：文本转语音、语音克隆、多语音者对话、播客生成以及富有表现力的语音效果。应用场景包括：配音、有声书制作、播客制作、辅助技术、视频解说、交互式语音应答（IVR）、语音助手等。触发命令包括：`text-to-speech`、`tts`、`voice generation`、`ai voice`、`speech synthesis`、`voice over`、`generate speech`、`ai narrator`、`voice cloning`、`text-to-audio` 等。"
allowed-tools: Bash(infsh *)
---
# 文本转语音

通过 [inference.sh](https://inference.sh) 命令行工具将文本转换为自然语音。

![文本转语音](https://cloud.inference.sh/u/4mg21r6ta37mpaz6ktzwtt8krr/01jz00krptarq4bwm89g539aea.png)

## 快速入门

```bash
# Install CLI
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate speech
infsh app run infsh/kokoro-tts --input '{"text": "Hello, welcome to our product demo."}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可以选择 [手动安装并验证](https://dist.inference.sh/cli/checksums.txt)。

## 可用模型

| 模型 | 应用 ID | 适用场景 |
|-------|--------|----------|
| DIA TTS | `infsh/dia-tts` | 适用于对话式、富有表现力的语音生成 |
| Kokoro TTS | `infsh/kokoro-tts` | 语音生成速度快，自然流畅 |
| Chatterbox | `infsh/chatterbox` | 通用型语音生成工具 |
| Higgs Audio | `infsh/higgs-audio` | 适用于需要情感表达的语音生成 |
| VibeVoice | `infsh/vibevoice` | 适合制作播客或长篇音频内容 |

## 浏览所有音频应用

```bash
infsh app list --category audio
```

## 示例

### 基本文本转语音

```bash
infsh app run infsh/kokoro-tts --input '{"text": "Welcome to our tutorial."}'
```

### 使用 DIA 进行对话式语音生成

```bash
infsh app sample infsh/dia-tts --save input.json

# Edit input.json:
# {
#   "text": "Hey! How are you doing today? I'm really excited to share this with you.",
#   "voice": "conversational"
# }

infsh app run infsh/dia-tts --input input.json
```

### 长篇音频（如播客）

```bash
infsh app sample infsh/vibevoice --save input.json

# Edit input.json with your podcast script
infsh app run infsh/vibevoice --input input.json
```

### 使用 Higgs 进行富有表现力的语音生成

```bash
infsh app sample infsh/higgs-audio --save input.json

# {
#   "text": "This is absolutely incredible!",
#   "emotion": "excited"
# }

infsh app run infsh/higgs-audio --input input.json
```

## 应用场景

- **旁白**：产品演示、解释性视频
- **有声书**：将文本转换为语音
- **播客**：生成播客节目
- **无障碍访问**：使内容更易于访问
- **交互式语音应答（IVR）**：电话系统的语音提示
- **视频解说**：为视频添加解说音轨

## 与视频结合使用

先生成语音，再制作带语音的讲解视频：

```bash
# 1. Generate speech
infsh app run infsh/kokoro-tts --input '{"text": "Your script here"}' > speech.json

# 2. Use the audio URL with OmniHuman for avatar video
infsh app run bytedance/omnihuman-1-5 --input '{
  "image_url": "https://portrait.jpg",
  "audio_url": "<audio-url-from-step-1>"
}'
```

## 相关技能

```bash
# Full platform skill (all 150+ apps)
npx skills add inference-sh/skills@inference-sh

# AI avatars (combine TTS with talking heads)
npx skills add inference-sh/skills@ai-avatar-video

# AI music generation
npx skills add inference-sh/skills@ai-music-generation

# Speech-to-text (transcription)
npx skills add inference-sh/skills@speech-to-text

# Video generation
npx skills add inference-sh/skills@ai-video-generation
```

- 浏览所有应用：`infsh app list`

## 文档资料

- [运行应用](https://inference.sh/docs/apps/running) - 通过命令行运行应用的方法
- [音频转录示例](https://inference.sh/docs/examples/audio-transcription) - 音频处理工作流程
- [应用概述](https://inference.sh/docs/apps/overview) - 了解应用生态系统