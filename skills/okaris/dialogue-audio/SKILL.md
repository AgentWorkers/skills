---
name: dialogue-audio
description: |
  Multi-speaker dialogue audio creation with Dia TTS.
  Covers speaker tags, emotion control, pacing, conversation flow, and post-production.
  Use for: podcasts, audiobooks, explainers, character dialogue, conversational content.
  Triggers: dialogue audio, multi speaker, conversation audio, dia tts, two speakers,
  podcast audio, character voices, voice acting, dialogue generation, conversation tts,
  multi voice, speaker tags, dialogue recording
allowed-tools: Bash(infsh *)
---

# 对话音频

通过 [inference.sh](https://inference.sh) 命令行工具，利用 Dia TTS 创建逼真的多角色对话。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Two-speaker conversation
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] Have you tried the new feature yet? [S2] Not yet, but I heard it saves a ton of time. [S1] It really does. I cut my workflow in half. [S2] Okay, I am definitely trying it today."
}'
```

## 说话者标签

Dia TTS 使用 `[S1]` 和 `[S2]` 来区分不同的说话者。

| 标签 | 角色 | 语音 |
|-----|------|-------|
| `[S1]` | 说话者1 | 自动分配的语音A |
| `[S2]` | 说话者2 | 自动分配的语音B |

**规则：**
- 每个说话者的发言前必须加上相应的标签
- 标签必须大写：使用 `[S1]` 而不是 `[s1]`
- 每次对话生成中最多只能有2个说话者
- 同一对话过程中，每个说话者的语音要保持一致

## 情感与表达控制

Dia TTS 能够根据标点符号和非语言线索来调整情感表达：

### 标点符号的效果

| 标点符号 | 效果 | 例子 |
|-------------|--------|---------|
| `.` | 中性、陈述语气、适度的停顿 | “这很重要。” |
| `!` | 强调、兴奋、充满活力 | “太棒了！” |
| `?` | 语调上升、表示疑问 | “你确定吗？” |
| `...` | 犹豫、声音逐渐减弱、长时间的停顿 | “我以为会成功……但并没有。” |
| `,` | 短暂的停顿 | “首先，我们分析。然后，我们行动。” |
| `—` 或 `--` | 表示中断或话题转换 | “我本来想说——算了。” |

### 非语言声音

Dia TTS 支持使用括号来描述声音效果：

```
(laughs)      — laughter
(sighs)       — exasperation or relief
(clears throat) — attention-getting pause
(whispers)    — softer delivery
(gasps)       — surprise
```

### 带有情感的对话示例

```bash
# Excited conversation
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] Guess what happened today! [S2] What? Tell me! [S1] We hit ten thousand users! [S2] (gasps) No way! That is incredible! [S1] I know... I still cannot believe it."
}'

# Serious/thoughtful dialogue
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] We need to talk about the timeline. [S2] (sighs) I know. It is tight. [S1] Can we cut anything from the scope? [S2] Maybe... but it would mean dropping the analytics dashboard. [S1] That is a tough trade-off."
}'

# Teaching/explaining
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] So how does it actually work? [S2] Great question. Think of it like a pipeline. Data comes in on one end, gets processed in the middle, and comes out transformed on the other side. [S1] Like an assembly line? [S2] Exactly! Each step adds something."
}'
```

## 语速控制

### 停顿的层次结构

| 技巧 | 停顿时长 | 适用场景 |
|-----------|-------------|---------|
| 逗号 `,` | 约0.3秒 | 用于分隔从句或列表项 |
| 句号 `.` | 约0.5秒 | 用于分隔句子 |
| 省略号 `...` | 约1.0秒 | 用于制造戏剧性停顿、表示思考或犹豫 |
| 新说话者标签 | 约0.3秒 | 用于自然地切换说话者 |

### 速度控制

- **短句子** = 更快的语速 |
- **包含逗号的长句子** = 有节奏的、深思熟虑的语速 |
- **问题后接回答** = 产生互动的对话节奏

```bash
# Fast-paced, energetic
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] Ready? [S2] Ready. [S1] Let us go! Three features. Five minutes. [S2] Hit it! [S1] Feature one: real-time sync."
}'

# Slow, contemplative
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] I have been thinking about this for a while... and I think we need to change direction. [S2] What do you mean? [S1] The market has shifted. What worked last year... is not working now."
}'
```

## 对话结构模式

### 面试格式

```bash
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] Welcome to the show. Today we have a special guest. Tell us about yourself. [S2] Thanks for having me! I am a product designer, and I have been building tools for creators for about ten years. [S1] What got you started in design? [S2] Honestly? I was terrible at coding but loved making things look good. (laughs) So design was the natural path."
}'
```

### 教程/解释说明

```bash
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] Can you walk me through the setup process? [S2] Sure. Step one, install the CLI. It takes about thirty seconds. [S1] And then? [S2] Step two, run the login command. It will open your browser for authentication. [S1] That sounds simple. [S2] It is! Step three, you are ready to run your first app."
}'
```

### 辩论/讨论

```bash
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] I think we should go with option A. It is faster to implement. [S2] But option B scales better long-term. [S1] Sure, but we need something shipping this quarter. [S2] Fair point... what if we do A now with a migration path to B? [S1] That could work. Let us prototype it."
}'
```

## 后期制作技巧

### 音量标准化

两个说话者的音量应该保持一致。如果其中一个说话者的音量较大：

```bash
# Merge with balanced audio
infsh app run infsh/video-audio-merger --input '{
  "video": "talking-head.mp4",
  "audio": "dialogue.mp3",
  "audio_volume": 1.0
}'
```

### 添加背景音乐

```bash
# Merge dialogue with background music
infsh app run infsh/media-merger --input '{
  "media": ["dialogue.mp3", "background-music.mp3"]
}'
```

### 分割长对话

对于超过30秒的对话，建议分段生成：

```bash
# Segment 1: Introduction
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] Welcome back to another episode..."
}'

# Segment 2: Main content
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] So let us dive into today s topic..."
}'

# Segment 3: Wrap-up
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] Great conversation today..."
}'

# Merge all segments
infsh app run infsh/media-merger --input '{
  "media": ["segment1.mp3", "segment2.mp3", "segment3.mp3"]
}'
```

## 脚本编写技巧

| 应该做 | 不应该做 |
|----|-------|
| 用人们实际说话的方式编写脚本 | 用书面语言编写脚本 |
| 使用短句子（<15个词） | 使用冗长的学术句子 |
| 使用缩写（如“can't”、“won't”） | 使用正式的表述（如“cannot”、“will not” |
| 使用自然的填充词（如“So,”、“Well,） | 每个句子都结构完美 |
| 句子长度要多样化 | 所有句子长度相同 |
| 包含反应（如“Exactly!”, “Hmm.”） | 只使用单方面的独白 |
| 生成前先大声朗读 | 假设脚本听起来自然 |

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 独白超过3句话 | 听起来像讲座，而不是对话 | 将内容拆分成多个对话片段 |
| 没有情感变化 | 语气平淡、机械 | 使用标点符号和非语言线索来表达情感 |
| 缺少说话者标签 | 语音无法交替 | 每个说话者的发言前加上 `[S1]` 或 `[S2]` |
| 使用正式的书面语言 | 朗读时听起来不自然 | 使用缩写和短句子 |
| 主题转换时没有停顿 | 会让对话显得仓促 | 使用 `...` 或场景转换的停顿 |
| 语调始终不变 | 会显得单调 | 通过调整语速来营造不同的情绪氛围 |

## 相关技能

```bash
npx skills add inferencesh/skills@text-to-speech
npx skills add inferencesh/skills@ai-podcast-creation
npx skills add inferencesh/skills@ai-avatar-video
```

浏览所有应用程序：`infsh app list`