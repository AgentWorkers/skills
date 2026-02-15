---
name: ai-music-generation
description: |
  Generate AI music and songs with Diffrythm, Tencent Song Generation via inference.sh CLI.
  Models: Diffrythm (fast song generation), Tencent Song Generation (full songs with vocals).
  Capabilities: text-to-music, song generation, instrumental, lyrics to song, soundtrack creation.
  Use for: background music, social media content, game soundtracks, podcasts, royalty-free music.
  Triggers: music generation, ai music, generate song, ai composer, text to music, song generator,
  create music with ai, suno alternative, udio alternative, ai song, ai soundtrack,
  generate soundtrack, ai jingle, music ai, beat generator
allowed-tools: Bash(infsh *)
---

# 人工智能音乐生成

通过 [inference.sh](https://inference.sh) 命令行界面（CLI）生成音乐和歌曲。

## 快速入门

```bash
# Install CLI
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a song
infsh app run infsh/diffrythm --input '{"prompt": "upbeat electronic dance track"}'
```

## 可用模型

| 模型 | 应用 ID | 适用场景 |
|-------|--------|----------|
| Diffrythm | `infsh/diffrythm` | 快速生成歌曲 |
| Tencent Song | `infsh/tencent-song-generation` | 带有人声的完整歌曲 |

## 浏览音频应用

```bash
infsh app list --category audio
```

## 示例

### 纯器乐曲

```bash
infsh app run infsh/diffrythm --input '{
  "prompt": "cinematic orchestral soundtrack, epic and dramatic"
}'
```

### 带有人声的歌曲

```bash
infsh app sample infsh/tencent-song-generation --save input.json

# Edit input.json:
# {
#   "prompt": "pop song about summer love",
#   "lyrics": "Walking on the beach with you..."
# }

infsh app run infsh/tencent-song-generation --input input.json
```

### 视频背景音乐

```bash
infsh app run infsh/diffrythm --input '{
  "prompt": "calm lo-fi hip hop beat, study music, relaxing"
}'
```

### 播客开场曲

```bash
infsh app run infsh/diffrythm --input '{
  "prompt": "short podcast intro jingle, professional, tech themed, 10 seconds"
}'
```

### 游戏原声带

```bash
infsh app run infsh/diffrythm --input '{
  "prompt": "retro 8-bit video game music, adventure theme, chiptune"
}'
```

## 提示建议

**音乐类型关键词**：流行、摇滚、电子、爵士、古典、嘻哈、低保真、环境音乐、管弦乐

**情绪关键词**：快乐、悲伤、充满活力、平静、戏剧性、宏大、神秘、振奋人心

**乐器关键词**：钢琴、吉他、合成器、鼓、弦乐、铜管乐器、合唱团

**音乐结构关键词**：引子、主歌、副歌、过渡段、尾声、循环

## 使用场景

- **社交媒体**：视频背景音乐
- **播客**：开场/结尾音乐
- **游戏**：原声带和音效
- **视频**：背景音乐
- **广告**：商业广告音乐
- **内容创作**：免版税音乐

## 相关技能

```bash
# Full platform skill (all 150+ apps)
npx skills add inference-sh/agent-skills@inference-sh

# Text-to-speech
npx skills add inference-sh/agent-skills@text-to-speech

# Video generation (add music to videos)
npx skills add inference-sh/agent-skills@ai-video-generation

# Speech-to-text
npx skills add inference-sh/agent-skills@speech-to-text
```

浏览所有应用：`infsh app list`

## 文档资料

- [运行应用](https://inference.sh/docs/apps/running) - 如何通过 CLI 运行应用
- [内容处理流程示例](https://inference.sh/docs/examples/content-pipeline) - 构建媒体工作流程
- [应用概览](https://inference.sh/docs/apps/overview) - 了解应用生态系统