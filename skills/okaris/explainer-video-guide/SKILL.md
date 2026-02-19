---
name: explainer-video-guide
description: "**解释型视频制作指南：脚本编写、旁白录制、视觉效果设计与视频剪辑**  
本指南涵盖了脚本编写技巧、视频节奏控制、场景规划以及多工具协同使用的流程。适用于以下场景：产品演示、操作流程说明视频、新员工入职培训视频、社交媒体宣传视频等。  
**相关术语说明：**  
- **解释型视频（Explainer Video）**：用于清晰、简洁地解释复杂概念或操作步骤的视频。  
- **脚本编写（Scripting）**：为视频内容编写详细的文字脚本。  
- **旁白录制（Voiceover）**：为视频添加解说音轨。  
- **视觉效果（Visuals）**：包括图片、动画、图表等用于辅助讲解的视觉元素。  
- **多工具协作（Multi-Tool Pipeline）**：使用多种视频编辑工具来完成视频制作的整个流程。  
**主要内容：**  
1. **脚本编写**：  
   - 学习如何编写结构清晰、逻辑严谨的脚本。  
   - 了解脚本中的关键元素（如标题、段落、列表、引言等）。  
   - 掌握如何处理复杂的逻辑和交互式内容。  
2. **视频节奏控制**：  
   - 学习如何根据视频内容调整节奏，确保观众能够轻松理解。  
   - 熟悉常见的视频节奏模式（如快速讲解、逐步引导、重复强调等）。  
3. **场景规划**：  
   - 设计合理的视频结构，确保每个部分都能有效地传达信息。  
   - 规划视频的过渡和衔接，提高观看体验。  
4. **多工具协作流程**：  
   - 介绍常用的视频编辑工具（如Adobe Premiere Pro、Final Cut Pro等）。  
   - 学习如何使用这些工具协同工作，提高视频制作效率。  
**适用场景：**  
- **产品演示**：向用户展示产品的功能和使用方法。  
- **操作指南**：提供详细的操作步骤。  
- **新员工入职**：帮助新员工快速熟悉工作流程。  
- **社交媒体**：用视频吸引观众，提高内容传播效果。  
**使用建议：**  
- 根据实际需求调整制作流程和工具选择。  
- 定期练习和优化，提升视频制作能力。  
**适用人群：**  
- 视频制作人、产品经理、内容创作者、新员工等需要制作解释型视频的人士。"
allowed-tools: Bash(infsh *)
---
# 解说视频制作指南

通过 [inference.sh](https://inference.sh) 命令行工具，您可以从脚本制作到最终完成的解说视频。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a scene for an explainer
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Clean motion graphics style animation, abstract data flowing between connected nodes, blue and white color scheme, professional corporate aesthetic, smooth transitions"
}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需提升权限或运行后台进程。也可选择 [手动安装与验证](https://dist.inference.sh/cli/checksums.txt)。

## 脚本结构

### 问题-激化-解决（PAS）——60 秒

| 部分 | 时长 | 内容 | 词数 |
|---------|----------|---------|------------|
| **问题** | 10 秒 | 说明观众面临的痛点 | 约 25 个词 |
| **激化问题** | 10 秒 | 说明问题比观众想象的更严重 | 约 25 个词 |
| **解决方案** | 15 秒 | 介绍您的产品/想法 | 约 35 个词 |
| **工作原理** | 20 秒 | 展示 3 个关键步骤或功能 | 约 50 个词 |
| **行动号召（CTA）** | 5 秒 | 明确的下一步行动 | 约 12 个词 |

### 从前到后的对比（BAB）——90 秒

| 部分 | 时长 | 内容 |
|---------|----------|---------|
| **现状** | 15 秒 | 展示当前令人沮丧的情况 |
| **理想结果** | 15 秒 | 展示理想的结果 |
| **解决方案** | 40 秒 | 解释您的产品如何帮助实现理想结果 |
| **用户评价** | 10 秒 | 快速展示用户评价或数据 |
| **行动号召（CTA）** | 10 秒 | 明确的下一步行动 |

### 功能亮点（社交媒体适用）——30 秒

| 部分 | 时长 | 内容 |
|---------|----------|---------|
| **引入** | 3 秒 | 一个令人惊讶的事实或问题 |
| **功能** | 15 秒 | 展示一个功能如何解决问题 |
| **结果** | 7 秒 | 展示功能带来的效果或好处 |
| **行动号召（CTA）** | 5 秒 | “立即尝试”或“了解更多”

## 语速控制规则

| 内容类型 | 每分钟词数 | 备注 |
|-------------|-----------------|-------|
| 标准旁白 | 150 词/分钟 | 采用对话式的语速 |
| 复杂/技术性内容 | 120 词/分钟 | 给观众足够的时间理解 |
| 活泼/社交类内容 | 170 词/分钟 | 适合简短的视频 |
| 儿童内容 | 100 词/分钟 | 语言简洁明了 |

**关键规则：** 每个核心信息对应一个场景。不要在一个视觉元素中包含多个信息。

### 场景时长建议

- 建立场景：3-5 秒 |
- 功能演示：5-8 秒 |
- 屏幕上的文字/数据：3-4 秒（必须清晰可读） |
- 过渡：0.5-1 秒 |
- 行动号召（CTA）场景：3-5 秒

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

### 将图片转换为视频

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

- 句子简短。每句不超过 15 个词。
- 使用主动语态。例如：“您可以追踪自己的数据”，而不是“您的数据可以被追踪”。
- 采用对话式的语气。大声朗读后，如果感觉生硬，请重新修改。
- 每个视觉元素对应一个核心信息。

### 生成旁白

```bash
# Professional narration with Dia TTS
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] Tired of spending hours on reports that nobody reads? There is a better way. Meet DataFlow. It turns your raw data into visual stories... in seconds. Just connect your source, pick a template, and share. Try DataFlow free today."
}'
```

### 语音合成（TTS）中的语速控制

| 技巧 | 效果 | 例子 |
|-----------|--------|---------|
| 句号（.`） | 中等停顿 | “这会改变一切。具体方法如下。” |
| 省略号（...） | 长停顿（增强戏剧效果） | “结果……令人难以置信。” |
| 逗号（`,） | 短停顿 | “快速、简单、强大。” |
| 感叹号（!） | 强调/增加活力 | “今天就开始行动吧！” |
| 问号（?） | 上升的语调 | “如果有一种更好的方法会怎样？”

## 音乐与音频

### 背景音乐建议

- **音量**：比旁白低 20-30%（语音播放时降低 6-12 分贝） |
- **风格**：与品牌调性匹配（企业风格 = 轻柔的电子音乐，创业公司 = 明快的独立音乐） |
- **结构**：开头逐渐增强音量（前 3 秒）→ 旁白期间保持柔和的循环音效 → 行动号召时音量再次增强 |
- **无人声**：旁白期间仅使用纯音乐

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

## 不同格式的视频时长建议

| 格式 | 时长 | 适用平台 |
|--------|--------|----------|
| 社交媒体预告片 | 15-30 秒 | TikTok、Instagram Reels、YouTube Shorts |
| 产品演示 | 60-90 秒 | 网站、着陆页 |
| 功能讲解 | 90-120 秒 | YouTube、电子邮件 |
| 教程/操作指南 | 2-5 分钟 | YouTube、帮助中心 |
| 投资者推介视频 | 2-3 分钟 | 用于补充演示文稿 |

## 过渡效果

| 过渡方式 | 使用时机 | 效果 |
|------------|-------------|--------|
| **直接切换** | 相关场景之间 | 清晰、专业 |
| **淡入/淡出** | 表示时间流逝或情绪转变 | 温和、引人思考 |
| **擦除** | 进入新主题或新部分 | 清晰的分界 |
| **放大/缩小** | 展示细节 | 使观众注意力集中 |
| **相似场景切换** | 视觉元素相似 | 巧妙且容易记忆 |

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 脚本过于冗长 | 旁白语速过快，观众难以理解 | 保持每分钟 150 个词左右的语速 |
| 开场 3 秒内没有吸引人的内容 | 观众会立即离开 | 从问题或令人惊讶的事实开始 |
| 视觉元素与旁白不同步 | 造成混乱 | 视觉元素应与旁白同步或稍微提前 |
| 背景音乐太响 | 无法听清旁白 | 降低音乐音量 6-12 分贝 |
| 无字幕 | 85% 的社交视频观众不看字幕 | 必须添加字幕 |
| 内容过多 | 观众无法记住重点 | 每个视频只传达一个核心信息 |

## 相关技能

```bash
npx skills add inference-sh/skills@ai-video-generation
npx skills add inference-sh/skills@video-prompting-guide
npx skills add inference-sh/skills@text-to-speech
npx skills add inference-sh/skills@prompt-engineering
```

查看所有可用工具：`infsh app list`