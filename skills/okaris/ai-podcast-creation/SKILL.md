---
name: ai-podcast-creation
description: |
  Create AI-powered podcasts with text-to-speech, music, and audio editing.
  Tools: Kokoro TTS, DIA TTS, Chatterbox, AI music generation, media merger.
  Capabilities: multi-voice conversations, background music, intro/outro, full episodes.
  Use for: podcast production, audiobooks, voice content, audio newsletters.
  Triggers: podcast, ai podcast, text to speech podcast, audio content, voice over,
  ai audiobook, multi voice, conversation ai, notebooklm alternative, audio generation,
  podcast automation, ai narrator, voice content, audio newsletter, podcast maker
allowed-tools: Bash(infsh *)
---

# AI播客制作

通过[inference.sh](https://inference.sh)命令行工具（CLI），您可以创建由AI驱动的播客和音频内容。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate podcast segment
infsh app run infsh/kokoro-tts --input '{
  "text": "Welcome to the AI Frontiers podcast. Today we explore the latest developments in generative AI.",
  "voice": "am_michael"
}'
```

## 可用的语音合成引擎

### Kokoro TTS

| 语音ID | 描述 | 适合的场景 |
|----------|-------------|----------|
| `af_sarah` | 美国女性，温暖的语音 | 主播、旁白 |
| `af_nicole` | 美国女性，专业的语音 | 新闻、商业内容 |
| `am_michael` | 美国男性，权威的语音 | 纪录片、科技类内容 |
| `am_adam` | 美国男性，日常对话风格 | 休闲播客 |
| `bf_emma` | 英国女性，优雅的语音 | 有声书 |
| `bm_george` | 英国男性，经典的语音 | 正式场合的内容 |

### DIA TTS（对话风格）

| 语音ID | 描述 | 适合的场景 |
|----------|-------------|----------|
| `dia-conversational` | 自然对话风格 | 对话、访谈 |

### Chatterbox

| 语音ID | 描述 | 适合的场景 |
|----------|-------------|----------|
| `chatterbox-default` | 表情丰富的语音 | 休闲、娱乐类内容 |

## 播客工作流程

### 简单的旁白制作

```bash
# Single voice podcast segment
infsh app run infsh/kokoro-tts --input '{
  "text": "Your podcast script here. Make it conversational and engaging. Add natural pauses with punctuation.",
  "voice": "am_michael"
}'
```

### 多语音对话

```bash
# Host introduction
infsh app run infsh/kokoro-tts --input '{
  "text": "Welcome back to Tech Talk. Today I have a special guest to discuss AI developments.",
  "voice": "am_michael"
}' > host_intro.json

# Guest response
infsh app run infsh/kokoro-tts --input '{
  "text": "Thanks for having me. I am excited to share what we have been working on.",
  "voice": "af_sarah"
}' > guest_response.json

# Merge into conversation
infsh app run infsh/media-merger --input '{
  "audio_files": ["<host-url>", "<guest-url>"],
  "crossfade_ms": 500
}'
```

### 完整的播客制作流程

```bash
# 1. Generate script with Claude
infsh app run openrouter/claude-sonnet-45 --input '{
  "prompt": "Write a 5-minute podcast script about the impact of AI on creative work. Format as a two-person dialogue between HOST and GUEST. Include natural conversation, questions, and insights."
}' > script.json

# 2. Generate intro music
infsh app run infsh/ai-music --input '{
  "prompt": "Podcast intro music, upbeat, modern, tech feel, 15 seconds"
}' > intro_music.json

# 3. Generate host segments
infsh app run infsh/kokoro-tts --input '{
  "text": "<host-lines>",
  "voice": "am_michael"
}' > host.json

# 4. Generate guest segments
infsh app run infsh/kokoro-tts --input '{
  "text": "<guest-lines>",
  "voice": "af_sarah"
}' > guest.json

# 5. Generate outro music
infsh app run infsh/ai-music --input '{
  "prompt": "Podcast outro music, matching intro style, fade out, 10 seconds"
}' > outro_music.json

# 6. Merge everything
infsh app run infsh/media-merger --input '{
  "audio_files": [
    "<intro-music>",
    "<host>",
    "<guest>",
    "<outro-music>"
  ],
  "crossfade_ms": 1000
}'
```

### 从文档生成播客风格的讨论内容

```bash
# 1. Extract key points
infsh app run openrouter/claude-sonnet-45 --input '{
  "prompt": "Read this document and create a podcast script where two hosts discuss the key points in an engaging, conversational way. Include questions, insights, and natural dialogue.\n\nDocument:\n<your-document-content>"
}' > discussion_script.json

# 2. Generate Host A
infsh app run infsh/kokoro-tts --input '{
  "text": "<host-a-lines>",
  "voice": "am_michael"
}' > host_a.json

# 3. Generate Host B
infsh app run infsh/kokoro-tts --input '{
  "text": "<host-b-lines>",
  "voice": "af_sarah"
}' > host_b.json

# 4. Interleave and merge
infsh app run infsh/media-merger --input '{
  "audio_files": ["<host-a-1>", "<host-b-1>", "<host-a-2>", "<host-b-2>"],
  "crossfade_ms": 300
}'
```

### 有声书章节制作

```bash
# Long-form narration
infsh app run infsh/kokoro-tts --input '{
  "text": "Chapter One. It was a dark and stormy night when the first AI achieved consciousness...",
  "voice": "bf_emma",
  "speed": 0.9
}'
```

## 音频优化

### 添加背景音乐

```bash
# 1. Generate podcast audio
infsh app run infsh/kokoro-tts --input '{
  "text": "<podcast-script>",
  "voice": "am_michael"
}' > podcast.json

# 2. Generate ambient music
infsh app run infsh/ai-music --input '{
  "prompt": "Soft ambient background music for podcast, subtle, non-distracting, loopable"
}' > background.json

# 3. Mix with lower background volume
infsh app run infsh/media-merger --input '{
  "audio_files": ["<podcast-url>"],
  "background_audio": "<background-url>",
  "background_volume": 0.15
}'
```

### 添加音效

```bash
# Transition sounds between segments
infsh app run infsh/ai-music --input '{
  "prompt": "Short podcast transition sound, whoosh, 2 seconds"
}' > transition.json
```

## 脚本编写技巧

### 如何使用Claude生成脚本

```bash
infsh app run openrouter/claude-sonnet-45 --input '{
  "prompt": "Write a podcast script with these requirements:
  - Topic: [YOUR TOPIC]
  - Duration: 5 minutes (about 750 words)
  - Format: Two hosts (HOST_A and HOST_B)
  - Tone: Conversational, informative, engaging
  - Include: Hook intro, 3 main points, call to action
  - Mark speaker changes clearly

  Make it sound natural, not scripted. Add verbal fillers like \"you know\" and \"I mean\" occasionally."
}'
```

## 播客模板

### 面试格式

```
HOST: Introduction and welcome
GUEST: Thank you, happy to be here
HOST: First question about background
GUEST: Response with story
HOST: Follow-up question
GUEST: Deeper insight
... continue pattern ...
HOST: Closing question
GUEST: Final thoughts
HOST: Thank you and outro
```

### 单人播客

```
Introduction with hook
Topic overview
Point 1 with examples
Point 2 with examples
Point 3 with examples
Summary and takeaways
Call to action
Outro
```

### 新闻汇总

```
Intro music
Welcome and date
Story 1: headline + details
Story 2: headline + details
Story 3: headline + details
Analysis/opinion segment
Outro
```

## 最佳实践

1. **使用自然的标点符号** – 用逗号和句号来控制语速和节奏。
2. **使用简短的句子** – 更易于朗读和聆听。
3. **使用多种语音** – 不同的语音可以避免单调感。
4. **背景音乐** – 音量控制在10-15%之间。
5. **平滑过渡** – 在不同段落之间实现无缝切换。
6. **编辑脚本** – 在生成音频之前删除冗余内容。

## 相关技能

```bash
# Text-to-speech models
npx skills add inference-sh/agent-skills@text-to-speech

# AI music generation
npx skills add inference-sh/agent-skills@ai-music-generation

# LLM for scripts
npx skills add inference-sh/agent-skills@llm-models

# Content pipelines
npx skills add inference-sh/agent-skills@ai-content-pipeline

# Full platform skill
npx skills add inference-sh/agent-skills@inference-sh
```

查看所有应用程序：`infsh app list --category audio`