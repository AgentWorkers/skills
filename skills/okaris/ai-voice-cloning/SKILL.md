---
name: ai-voice-cloning
description: "通过 `inference.sh` 命令行工具实现 AI 语音生成、文本转语音（TTS）及语音合成功能。支持的模型包括：Kokoro TTS、DIA、Chatterbox、Higgs、VibeVoice，可生成自然流畅的语音。功能特点包括：支持多种语音风格、情感表达、口音设置，支持长篇叙述及对话场景。应用场景包括：配音、有声书制作、播客录制、视频解说以及提升内容的可访问性（如为视障用户提供语音描述）。相关命令包括：语音克隆、文本转语音、AI 语音生成、语音合成等。"
allowed-tools: Bash(infsh *)
---
# 人工智能语音生成

通过 [inference.sh](https://inference.sh) 命令行工具生成自然的人造语音。

![人工智能语音生成](https://cloud.inference.sh/u/4mg21r6ta37mpaz6ktzwtt8krr/01jz00krptarq4bwm89g539aea.png)

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate speech
infsh app run infsh/kokoro-tts --input '{
  "text": "Hello! This is an AI-generated voice that sounds natural and engaging.",
  "voice": "af_sarah"
}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可以选择 [手动安装并验证](https://dist.inference.sh/cli/checksums.txt)。

## 可用模型

| 模型 | 应用 ID | 适用场景 |
|-------|--------|----------|
| Kokoro TTS | `infsh/kokoro-tts` | 自然音色，多种语音风格 |
| DIA | `infsh/dia-tts` | 适合对话场景，表达力强 |
| Chatterbox | `infsh/chatterbox` | 适合休闲娱乐场景 |
| Higgs | `infsh/higgs-tts` | 适合专业旁白 |
| VibeVoice | `infsh/vibevoice` | 适合表达情感的语音 |

## Kokoro 语音库

### 美式英语

| 语音 ID | 性别 | 风格 |
|----------|--------|-------|
| `af_sarah` | 女性 | 温暖、友好 |
| `af_nicole` | 女性 | 专业 |
| `af_sky` | 女性 | 年轻人风格 |
| `am_michael` | 男性 | 权威感强 |
| `am_adam` | 男性 | 适合对话 |
| `am_echo` | 男性 | 语气清晰、中性 |

### 英式英语

| 语音 ID | 性别 | 风格 |
|----------|--------|-------|
| `bf_emma` | 女性 | 优雅 |
| `bf_isabella` | 女性 | 温暖 |
| `bm_george` | 男性 | 古典风格 |
| `bm_lewis` | 男性 | 现代风格 |

## 语音生成示例

### 专业旁白

```bash
infsh app run infsh/kokoro-tts --input '{
  "text": "Welcome to our quarterly earnings call. Today we will discuss the financial performance and strategic initiatives for the past quarter.",
  "voice": "am_michael",
  "speed": 1.0
}'
```

### 对话风格

```bash
infsh app run infsh/dia-tts --input '{
  "text": "Hey, so I was thinking about that project we discussed. What if we tried a different approach?",
  "voice": "conversational"
}'
```

### 有声书旁白

```bash
infsh app run infsh/kokoro-tts --input '{
  "text": "Chapter One. The morning mist hung low over the valley as Sarah made her way down the winding path. She had been walking for hours.",
  "voice": "bf_emma",
  "speed": 0.9
}'
```

### 视频旁白

```bash
infsh app run infsh/kokoro-tts --input '{
  "text": "Introducing the next generation of productivity. Work smarter, not harder.",
  "voice": "af_nicole",
  "speed": 1.1
}'
```

### 播客主持人

```bash
infsh app run infsh/kokoro-tts --input '{
  "text": "Welcome back to Tech Talk! Im your host, and today we are diving deep into the world of artificial intelligence.",
  "voice": "am_adam"
}'
```

## 多语音对话

```bash
# Generate dialogue between two speakers
# Speaker 1
infsh app run infsh/kokoro-tts --input '{
  "text": "Have you seen the latest AI developments? Its incredible how fast things are moving.",
  "voice": "am_michael"
}' > speaker1.json

# Speaker 2
infsh app run infsh/kokoro-tts --input '{
  "text": "I know, right? Just last week I tried that new image generator and was blown away.",
  "voice": "af_sarah"
}' > speaker2.json

# Merge conversation
infsh app run infsh/media-merger --input '{
  "audio_files": ["<speaker1-url>", "<speaker2-url>"],
  "crossfade_ms": 300
}'
```

## 长篇内容处理

- 如果内容超过 5000 个字符，请将其分割成多个部分进行处理：

```bash
# Process long text in chunks
TEXT="Your very long text here..."

# Split and generate
# Chunk 1
infsh app run infsh/kokoro-tts --input '{
  "text": "<chunk-1>",
  "voice": "bf_emma"
}' > chunk1.json

# Chunk 2
infsh app run infsh/kokoro-tts --input '{
  "text": "<chunk-2>",
  "voice": "bf_emma"
}' > chunk2.json

# Merge chunks
infsh app run infsh/media-merger --input '{
  "audio_files": ["<chunk1-url>", "<chunk2-url>"],
  "crossfade_ms": 100
}'
```

## 语音与视频结合的工作流程

### 为视频添加旁白

```bash
# 1. Generate voiceover
infsh app run infsh/kokoro-tts --input '{
  "text": "This stunning footage shows the beauty of nature in its purest form.",
  "voice": "am_michael"
}' > voiceover.json

# 2. Merge with video
infsh app run infsh/media-merger --input '{
  "video_url": "https://your-video.mp4",
  "audio_url": "<voiceover-url>"
}'
```

### 创建动画角色（Talking Head）

```bash
# 1. Generate speech
infsh app run infsh/kokoro-tts --input '{
  "text": "Hi, Im excited to share some updates with you today.",
  "voice": "af_sarah"
}' > speech.json

# 2. Animate with avatar
infsh app run bytedance/omnihuman-1-5 --input '{
  "image_url": "https://portrait.jpg",
  "audio_url": "<speech-url>"
}'
```

## 语速与节奏控制

| 语速 | 效果 | 适用场景 |
|-------|--------|---------|
| 0.8 | 语速较慢 | 适合有声书、冥想 |
| 0.9 | 语速稍慢 | 教育类内容、教程 |
| 1.0 | 正常语速 | 通用场景 |
| 1.1 | 语速稍快 | 商业广告、需要活力的场景 |
| 1.2 | 语速很快 | 快速公告 |

```bash
# Slow narration
infsh app run infsh/kokoro-tts --input '{
  "text": "Take a deep breath. Let yourself relax.",
  "voice": "bf_emma",
  "speed": 0.8
}'
```

## 使用标点符号控制节奏

- 使用标点符号来控制语音的节奏：
| 标点符号 | 效果 |
|-------------|--------|
| 句号 `.` | 长暂停 |
| 逗号 `,` | 短暂停 |
| `...` | 长暂停 |
| `!` | 强调 |
| `?` | 提问语气 |
| `-` | 快速停顿 |

```bash
infsh app run infsh/kokoro-tts --input '{
  "text": "Wait... Did you hear that? Something is coming. Something big!",
  "voice": "am_adam"
}'
```

## 最佳实践

1. **根据内容选择合适的语音**：商务场景使用专业语音，社交场景使用自然的语音风格。
2. **使用标点符号**：通过句号和逗号来控制语速和节奏。
3. **保持句子简短**：这样更容易生成语音，听起来也更自然。
4. **测试不同的语音**：同样的文本用不同的语音表达出来效果可能不同。
5. **调整语速**：通常语速稍慢会让人感觉更自然。
6. **分段处理长内容**：将长内容分成小块进行处理，以保持一致性。

## 应用场景

- **旁白**：视频解说、商业广告
- **有声书**：整本书的朗读
- **播客**：AI 主播和嘉宾角色
- **电子学习**：课程讲解
- **无障碍技术**：屏幕阅读器的辅助内容
- **交互式语音应答（IVR）**：电话系统的语音提示
- **内容本地化**：文本的翻译和语音化

## 相关技能

```bash
# All TTS models
npx skills add inference-sh/skills@text-to-speech

# Podcast creation
npx skills add inference-sh/skills@ai-podcast-creation

# AI avatars
npx skills add inference-sh/skills@ai-avatar-video

# Video generation
npx skills add inference-sh/skills@ai-video-generation

# Full platform skill
npx skills add inference-sh/skills@inference-sh
```

查看音频应用：`infsh app list --category audio`