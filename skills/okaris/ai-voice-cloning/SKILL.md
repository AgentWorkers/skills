---
name: ai-voice-cloning
description: |
  AI voice generation, text-to-speech, and voice synthesis via inference.sh CLI.
  Models: Kokoro TTS, DIA, Chatterbox, Higgs, VibeVoice for natural speech.
  Capabilities: multiple voices, emotions, accents, long-form narration, conversation.
  Use for: voiceovers, audiobooks, podcasts, video narration, accessibility.
  Triggers: voice cloning, tts, text to speech, ai voice, voice generation,
  voice synthesis, voice over, narration, speech synthesis, ai narrator,
  elevenlabs alternative, natural voice, realistic speech, voice ai
allowed-tools: Bash(infsh *)
---

# 人工智能语音生成

通过 [inference.sh](https://inference.sh) 命令行界面（CLI）生成自然的语音效果。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate speech
infsh app run infsh/kokoro-tts --input '{
  "text": "Hello! This is an AI-generated voice that sounds natural and engaging.",
  "voice": "af_sarah"
}'
```

## 可用模型

| 模型 | 应用 ID | 适用场景 |
|-------|--------|----------|
| Kokoro TTS | `infsh/kokoro-tts` | 自然的语音效果，支持多种声音 |
| DIA | `infsh/dia-tts` | 适合对话场景，表达力强 |
| Chatterbox | `infsh/chatterbox` | 适合休闲娱乐场景 |
| Higgs | `infsh/higgs-tts` | 适合专业旁白场景 |
| VibeVoice | `infsh/vibevoice` | 具备丰富的情感表现力 |

## Kokoro 语音库

### 美式英语

| 语音 ID | 性别 | 语音风格 |
|----------|--------|-------|
| `af_sarah` | 女性 | 温暖、友好的语气 |
| `af_nicole` | 女性 | 专业的语气 |
| `af_sky` | 女性 | 年轻人风格 |
| `am_michael` | 男性 | 权威性强的语气 |
| `am_adam` | 男性 | 适合对话的语气 |
| `am_echo` | 男性 | 清晰、中立的语气 |

### 英式英语

| 语音 ID | 性别 | 语音风格 |
|----------|--------|-------|
| `bf_emma` | 女性 | 优雅的语气 |
| `bf_isabella` | 女性 | 温暖的语气 |
| `bm_george` | 男性 | 古典的语气 |
| `bm_lewis` | 男性 | 现代的语气 |

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

- 如果内容超过 5000 个字符，建议将其分割成多个部分进行处理：

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

## 语音与视频的结合

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
| 0.8 | 语速较慢 | 适合有声书、冥想场景 |
| 0.9 | 语速稍慢 | 适合教育、教程内容 |
| 1.0 | 正常语速 | 通用场景 |
| 1.1 | 语速稍快 | 适合广告、需要活力的场景 |
| 1.2 | 语速很快 | 适合快速公告 |

```bash
# Slow narration
infsh app run infsh/kokoro-tts --input '{
  "text": "Take a deep breath. Let yourself relax.",
  "voice": "bf_emma",
  "speed": 0.8
}'
```

## 使用标点符号控制语速节奏

- 标点符号可以帮助控制语音的节奏：
  - 句号（.`）：表示完整的停顿 |
  - 逗号（`,`）：表示短暂的停顿 |
  - …（`...`）：表示较长的停顿 |
  - 句号（`!`）：表示强调 |
  - 问号（`?`）：表示疑问的语气 |
  - 破折号（`-`）：表示短暂的停顿 |

```bash
infsh app run infsh/kokoro-tts --input '{
  "text": "Wait... Did you hear that? Something is coming. Something big!",
  "voice": "am_adam"
}'
```

## 最佳实践

1. **根据内容选择合适的语音**：商务场景使用专业语音，社交场景使用自然的语音。
2. **使用标点符号**：通过句号和逗号来控制语速节奏。
3. **保持句子简短**：这样更容易生成自然的语音效果。
4. **测试不同的语音**：同样的文本用不同的语音表达出来会有不同的效果。
5. **调整语速**：通常语速稍慢会显得更自然。
6. **分段处理长内容**：将长内容分成小段进行处理，以保持一致性。

## 应用场景

- **旁白**：视频解说、广告
- **有声书**：整本书的朗读
- **播客**：AI 播客主持人及嘉宾
- **电子学习**：课程讲解
- **无障碍阅读**：为屏幕阅读器生成语音内容
- **交互式语音应答（IVR）**：电话系统中的语音消息
- **内容本地化**：将文本翻译并转化为语音

## 相关技能

```bash
# All TTS models
npx skills add inference-sh/agent-skills@text-to-speech

# Podcast creation
npx skills add inference-sh/agent-skills@ai-podcast-creation

# AI avatars
npx skills add inference-sh/agent-skills@ai-avatar-video

# Video generation
npx skills add inference-sh/agent-skills@ai-video-generation

# Full platform skill
npx skills add inference-sh/agent-skills@inference-sh
```

查看音频应用：`infsh app list --category audio`