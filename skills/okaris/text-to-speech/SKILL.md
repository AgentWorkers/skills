---
name: text-to-speech
description: |
  Convert text to natural speech with DIA TTS, Kokoro, Chatterbox, and more via inference.sh CLI.
  Models: DIA TTS (conversational), Kokoro TTS, Chatterbox, Higgs Audio, VibeVoice (podcasts).
  Capabilities: text-to-speech, voice cloning, multi-speaker dialogue, podcast generation, expressive speech.
  Use for: voiceovers, audiobooks, podcasts, accessibility, video narration, IVR, voice assistants.
  Triggers: text to speech, tts, voice generation, ai voice, speech synthesis, voice over,
  generate speech, ai narrator, voice cloning, text to audio, elevenlabs alternative,
  voice ai, ai voiceover, speech generator, natural voice
allowed-tools: Bash(infsh *)
---

# 文本转语音

通过 [inference.sh](https://inference.sh) 命令行工具将文本转换为自然语音。

## 快速入门

```bash
# Install CLI
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate speech
infsh app run infsh/kokoro-tts --input '{"text": "Hello, welcome to our product demo."}'
```

## 可用模型

| 模型 | 应用 ID | 适用场景 |
|-------|--------|----------|
| DIA TTS | `infsh/dia-tts` | 适用于对话式、富有表现力的语音合成 |
| Kokoro TTS | `infsh/kokoro-tts` | 语音合成速度快，自然流畅 |
| Chatterbox | `infsh/chatterbox` | 通用型语音合成工具 |
| Higgs Audio | `infsh/higgs-audio` | 适用于需要情感表达的语音合成 |
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

### 使用 DIA 进行对话式语音合成

```bash
infsh app sample infsh/dia-tts --save input.json

# Edit input.json:
# {
#   "text": "Hey! How are you doing today? I'm really excited to share this with you.",
#   "voice": "conversational"
# }

infsh app run infsh/dia-tts --input input.json
```

### 长篇音频（播客）

```bash
infsh app sample infsh/vibevoice --save input.json

# Edit input.json with your podcast script
infsh app run infsh/vibevoice --input input.json
```

### 使用 Higgs 进行富有表现力的语音合成

```bash
infsh app sample infsh/higgs-audio --save input.json

# {
#   "text": "This is absolutely incredible!",
#   "emotion": "excited"
# }

infsh app run infsh/higgs-audio --input input.json
```

## 应用场景

- **旁白**：产品演示、讲解视频
- **有声书**：将文本转换为音频形式
- **播客**：生成播客节目
- **无障碍技术**：提升内容的可访问性
- **交互式语音应答（IVR）**：电话系统的语音提示
- **视频解说**：为视频添加旁白

## 结合视频使用

先生成语音，再制作带语音解说的视频：

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
npx skills add inference-sh/agent-skills@inference-sh

# AI avatars (combine TTS with talking heads)
npx skills add inference-sh/agent-skills@ai-avatar-video

# AI music generation
npx skills add inference-sh/agent-skills@ai-music-generation

# Speech-to-text (transcription)
npx skills add inference-sh/agent-skills@speech-to-text

# Video generation
npx skills add inference-sh/agent-skills@ai-video-generation
```

浏览所有应用：`infsh app list`

## 文档资料

- [运行应用](https://inference.sh/docs/apps/running) - 如何通过命令行运行应用
- [音频转录示例](https://inference.sh/docs/examples/audio-transcription) - 音频处理工作流程
- [应用概览](https://inference.sh/docs/apps/overview) - 了解应用生态系统