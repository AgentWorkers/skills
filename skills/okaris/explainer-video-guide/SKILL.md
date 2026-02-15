---
name: explainer-video-guide
description: |
  Explainer video production guide: scripting, voiceover, visuals, and assembly.
  Covers script formulas, pacing rules, scene planning, and multi-tool pipelines.
  Use for: product demos, how-it-works videos, onboarding videos, social explainers.
  Triggers: explainer video, how to make explainer, product video, demo video,
  video production, video script, animated explainer, product demo video,
  tutorial video, onboarding video, walkthrough video, video pipeline
allowed-tools: Bash(infsh *)
---

# 解说视频制作指南

通过 [inference.sh](https://inference.sh) 命令行工具，从脚本到最终成品，您可以轻松制作出高质量的解释性视频。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a scene for an explainer
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Clean motion graphics style animation, abstract data flowing between connected nodes, blue and white color scheme, professional corporate aesthetic, smooth transitions"
}'
```

## 脚本编写规则

### “问题-激发-解决”（Problem-Agitate-Solve, PAS）——60秒

| 部分 | 时长 | 内容 | 词数 |
|---------|----------|---------|------------|
| **问题** | 10秒 | 说明观众面临的痛点 | 约25个词 |
| **问题加剧** | 10秒 | 阐明问题比观众想象的更严重 | 约25个词 |
| **解决方案** | 15秒 | 介绍您的产品/想法 | 约35个词 |
| **工作原理** | 20秒 | 展示3个关键步骤或功能 | 约50个词 |
| **行动号召** | 5秒 | 提供明确的下一步操作 | 约12个词 |

### “前后对比”（Before-After-Bridge, BAB）——90秒

| 部分 | 时长 | 内容 |
|---------|----------|---------|
| **现状** | 15秒 | 展示当前令人沮丧的情况 |
| **理想结果** | 15秒 | 展示理想的结果 |
| **实现过程** | 40秒 | 解释您的产品如何帮助观众达到理想状态 |
| **用户评价** | 10秒 | 简短的用户评价或数据统计 |
| **行动号召** | 10秒 | 明确的下一步行动 |

### **功能亮点**（Feature Spotlight）——30秒（适合社交媒体）

| 部分 | 时长 | 内容 |
|---------|----------|---------|
| **引人注意的部分** | 3秒 | 一个令人惊讶的事实或问题 |
| **功能介绍** | 15秒 | 展示一个功能如何解决问题 |
| **效果展示** | 7秒 | 展示功能带来的结果或好处 |
| **行动号召** | 5秒 | “立即尝试”或“了解更多”

## 语速控制规则

| 内容类型 | 每分钟词数 | 备注 |
|-------------|-----------------|-------|
| 常规叙述 | 150词/分钟 | 采用对话式的语速 |
| 复杂/技术性内容 | 120词/分钟 | 给观众足够的时间理解 |
| 活泼/社交类内容 | 170词/分钟 | 适合短片 |
| 儿童内容 | 100词/分钟 | 语言简洁、语速较慢 |

**关键规则：** 每个核心信息对应一个场景。不要在一个视觉元素中包含多个信息。

### 场景时长建议

- 建立场景：3-5秒  
- 功能演示：5-8秒  
- 屏幕上的文字/数据：3-4秒（必须清晰可读）  
- 过渡：0.5-1秒  
- 行动号召屏幕：3-5秒  

## 视觉元素制作

### 场景类型

```bash
# Product in context
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Clean product demonstration video, hands typing on a laptop showing a dashboard interface, bright modern office, soft natural lighting, professional"
}'

# Abstract concept visualization
infsh app run bytedance/seedance-1-5-pro --input '{
  "prompt": "Abstract motion graphics, colorful data streams connecting floating geometric shapes, smooth fluid animation, dark background with glowing elements, tech aesthetic"
}'

# Lifestyle/outcome shot
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Happy person relaxing on couch with laptop, smiling at screen, bright airy living room, warm afternoon light, satisfied customer feeling, lifestyle commercial style"
}'

# Before/after comparison
infsh app run falai/flux-dev-lora --input '{
  "prompt": "Split screen comparison, left side cluttered messy desk with papers and stress, right side clean organized minimalist workspace, dramatic difference, clean design"
}'
```

### 如何将图片转换为视频

```bash
# Generate a still frame first
infsh app run falai/flux-dev-lora --input '{
  "prompt": "Professional workspace with glowing holographic interface, futuristic but clean, blue accent lighting"
}'

# Animate it
infsh app run falai/wan-2-5-i2v --input '{
  "prompt": "Gentle camera push in, holographic elements subtly floating and rotating, soft ambient light shifts",
  "image": "path/to/workspace-still.png"
}'
```

## 旁白制作

### 脚本编写技巧

- 句子简短。每句不超过15个词。  
- 使用主动语态。例如：“您可以追踪自己的数据”，而不是“您的数据可以被追踪”。  
- 采用对话式的语气。大声朗读后，如果感觉生硬，请重新修改。  
- 每个视觉元素对应一个核心信息。  

### 旁白生成

```bash
# Professional narration with Dia TTS
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] Tired of spending hours on reports that nobody reads? There is a better way. Meet DataFlow. It turns your raw data into visual stories... in seconds. Just connect your source, pick a template, and share. Try DataFlow free today."
}'
```

### 语音合成中的语速控制

| 技巧 | 效果 | 例子 |
|-----------|--------|---------|
| 句号 `.` | 中等停顿 | “这会改变一切。具体方法如下。” |
| 省略号 `...` | 长停顿（增强戏剧效果） | “结果……令人难以置信。” |
| 逗号 `,` | 短停顿 | “快速、简单、强大。” |
| 感叹号 `!` | 强调/增加紧迫感 | “今天就开始行动吧！” |
| 问号 `?` | 提升语调 | “如果有一种更好的方法会怎样？” |

## 音乐与音频

### 背景音乐指南

- **音量**：比旁白低20-30%（当有语音时，音乐音量降低6-12分贝）  
- **风格**：与品牌调性匹配（企业风格 = 轻松的电子音乐；初创企业 = 明快的独立音乐）  
- **结构**：开头渐强（前3秒）→ 旁白期间播放轻柔的循环音乐 → 行动号召时音量再次增强  
- **无歌词**：旁白期间仅使用纯音乐  

```bash
# Generate background music
infsh app run <music-gen-app> --input '{
  "prompt": "upbeat corporate background music, modern electronic, 90 BPM, positive and professional, no vocals, suitable for product explainer video"
}'
```

## 视频制作流程

```bash
# 1. Generate voiceover
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] Your script here..."
}'

# 2. Generate scene visuals (in parallel)
infsh app run google/veo-3-1-fast --input '{"prompt": "scene 1 description"}' --no-wait
infsh app run google/veo-3-1-fast --input '{"prompt": "scene 2 description"}' --no-wait
infsh app run google/veo-3-1-fast --input '{"prompt": "scene 3 description"}' --no-wait

# 3. Merge scenes into sequence
infsh app run infsh/media-merger --input '{
  "media": ["scene1.mp4", "scene2.mp4", "scene3.mp4"]
}'

# 4. Add voiceover to video
infsh app run infsh/video-audio-merger --input '{
  "video": "merged-scenes.mp4",
  "audio": "voiceover.mp3"
}'

# 5. Add captions
infsh app run infsh/caption-videos --input '{
  "video": "final-with-audio.mp4",
  "caption_file": "captions.srt"
}'
```

## 不同格式的视频时长

| 格式 | 时长 | 适用平台 |
|--------|--------|----------|
| 社交媒体预告片 | 15-30秒 | TikTok、Instagram Reels、YouTube Shorts |
| 产品演示 | 60-90秒 | 网站、着陆页 |
| 功能说明视频 | 90-120秒 | YouTube、电子邮件 |
| 教程/操作指南 | 2-5分钟 | YouTube、帮助中心 |
| 投资者推介视频 | 2-3分钟 | 作为演示文稿的补充材料 |

## 过渡效果

| 过渡方式 | 使用场景 | 效果 |
|------------|-------------|--------|
| **直接切换** | 相关场景之间 | 清晰、专业 |
| **淡入/淡出** | 表示时间流逝或情绪转变 | 温和、引人思考 |
| **擦除** | 引入新主题或新部分 | 清晰的分界 |
| **放大/缩小** | 详细展示某个部分 | 有助于集中注意力 |
| **相似场景切换** | 视觉元素相似 | 创意且容易记忆 |

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 脚本过于冗长 | 旁白语速过快，观众难以理解 | 将每分钟字数控制在150词以内 |
| 开场3秒内没有吸引人的内容 | 观众会立即离开 | 从问题或令人惊讶的事实开始 |
| 视觉元素与旁白不同步 | 造成视觉与听觉的混乱 | 视觉元素应与旁白同步或略微提前 |
| 背景音乐音量过大 | 无法听清旁白 | 将音乐音量降低6-12分贝 |
| 无字幕 | 85%的社交视频观众不看字幕 | 必须添加字幕 |
| 内容过于复杂 | 观众无法记住要点 | 每个视频只传达一个核心信息 |

## 相关技能

```bash
npx skills add inferencesh/skills@ai-video-generation
npx skills add inferencesh/skills@video-prompting-guide
npx skills add inferencesh/skills@text-to-speech
npx skills add inferencesh/skills@prompt-engineering
```

浏览所有可用工具：`infsh app list`