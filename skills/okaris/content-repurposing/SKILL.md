---
name: content-repurposing
description: "**内容原子化**——将一篇内容转换为多种格式。具体包括：将博客文章转换为帖子、将博客文章转换为轮播图、将播客内容转换为博客文章、将视频内容转换为引用等。适用于：内容营销、社交媒体推广、多平台分发以及内容策略的制定。相关功能包括：内容再利用、内容转换、内容回收利用、实现“一变多”的效果（即同一内容可适用于多个平台或形式）、跨平台发布、内容改编以及重新格式化等。"
allowed-tools: Bash(infsh *)
---
# 内容再利用

通过 [inference.sh](https://inference.sh) 命令行工具，可以将一篇内容转换为多种格式。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a quote card from a blog pull-quote
infsh app run falai/flux-dev-lora --input '{
  "prompt": "minimal quote card design, dark navy background, large white quotation marks, clean sans-serif typography space, modern professional design, social media post format",
  "width": 1024,
  "height": 1024
}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可通过 [手动安装与验证](https://dist.inference.sh/cli/checksums.txt) 进行操作。

## 内容转化方法

一篇原始内容可以生成 10 种以上的衍生形式：

```
            ┌──────────┐
            │ LONG-FORM │  Blog post, podcast, video, whitepaper
            │  SOURCE   │
            └─────┬─────┘
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
   ┌─────────┐ ┌──────┐ ┌──────────┐
   │ MEDIUM  │ │MEDIUM│ │  MEDIUM  │  Newsletter, LinkedIn, email
   │ FORMAT  │ │FORMAT│ │  FORMAT  │
   └────┬────┘ └──┬───┘ └────┬─────┘
        │         │          │
   ┌────┼────┐    │     ┌────┼────┐
   ▼    ▼    ▼    ▼     ▼    ▼    ▼
 ┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐  Tweets, quotes, audiograms,
 │   ││   ││   ││   ││   ││   ││   │  short clips, infographic tiles
 └───┘└───┘└───┘└───┘└───┘└───┘└───┘
```

## 转换方案

### 博文 -> 推特/微博帖子

**提取 5-8 个关键观点，每条推文分享一个观点，并添加引导语。**

| 元素 | 规则 |
|---------|------|
| 引导语推文 | 采用列表式、反传统或承诺性的格式 |
| 正文推文 | 每条推文分享一个关键观点，最多 280 个字符 |
| 视觉元素 | 每 3-4 条推文添加一张图片 |
| 最终推文 | 包含呼吁行动（CTA）的内容，并提示“如果觉得有用请转发第一条推文” |

**调整建议：**
- 去除细节和注意事项（推文需要简洁明了）
- 添加数字和具体例子（推文需要便于快速浏览）
- 避免使用学术性语言（推文应更通俗易懂）

```bash
# Generate a visual for the thread
infsh app run falai/flux-dev-lora --input '{
  "prompt": "clean infographic tile, single statistic 60% highlighted in large bold text, minimal dark background, data visualization style, professional",
  "width": 1024,
  "height": 1024
}'

# Post the thread
infsh app run x/post-create --input '{
  "text": "I analyzed 500 landing pages.\n\nHere are 7 patterns the top converters all share:\n\n🧵 Thread:"
}'
```

### 博文 -> LinkedIn 轮播图

**每个部分对应一张幻灯片，总共 8-12 张幻灯片。**

| 幻灯片 | 内容 |
|-------|---------|
| 1（引导语） | 标题中的重点声明或问题 |
| 2-9（正文） | 每张幻灯片展示一个关键点，配以辅助视觉元素 |
| 10（总结） | 回顾关键内容 |
| 11（呼吁行动） | “关注以获取更多内容” / “保存此内容” / “请分享您的想法” |

**规格：** 1080x1080（正方形）或 1080x1350（4:5 比例，以获得更多显示空间）

```bash
# Generate carousel slides
for i in {1..10}; do
  infsh app run falai/flux-dev-lora --input "{
    \"prompt\": \"clean minimal presentation slide, dark gradient background, large text area, professional business design, slide $i of 10, consistent style\",
    \"width\": 1024,
    \"height\": 1024
  }" --no-wait
done
```

### 博文 -> 通讯文章

**3 行的摘要 + “为什么这很重要” + 链接**

```
## This Week's Feature: [Title]

[1-2 sentence summary of the key insight]

**Why it matters:** [1 sentence connecting to reader's work/life]

→ [Read the full post](link)
```

### 博文 -> 简短视频脚本

**问题 + 关键观点 + 呼吁行动。时长不超过 60 秒。**

| 部分 | 时长 | 内容 |
|---------|----------|---------|
| 引导语 | 3 秒 | “大多数人误解了[主题]。” |
| 问题描述 | 10 秒 | 说明常见的错误 |
| 观点阐述 | 25 秒 | 介绍您的关键发现或建议 |
| 证据支持 | 10 秒 | 提供一个数据或例子 |
| 呼吁行动 | 5 秒 | “关注以获取更多内容” / “在个人资料中分享此链接” |

```bash
# Generate voiceover
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] Most landing pages make this mistake. They put the features above the fold instead of the outcome. Top converting pages show what life looks like AFTER using the product. Try it and watch your conversion rate climb."
}'

# Generate video
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Screen recording style, scrolling through a well-designed landing page, clean modern UI, smooth scroll, professional website"
}'
```

### 博文 -> 有声书

**提取最佳引语并生成音频文件，同时添加波形图作为视觉辅助。**

```bash
# Generate audio of the key quote
infsh app run falai/dia-tts --input '{
  "prompt": "[S1] The number one mistake I see on landing pages... is putting features above the fold. The best pages show the outcome. Not what your product does, but what life looks like after."
}'
```

### 播客剧集 -> 博文

```bash
# 1. Transcribe the episode
infsh app run <stt-app> --input '{
  "audio": "episode-42.mp3"
}'

# 2. Edit transcript into blog format:
# - Remove filler words (um, uh, like, you know)
# - Add headers at topic changes
# - Break into paragraphs
# - Add intro and conclusion
# - Add links mentioned in the episode
```

### 播客剧集 -> 引语卡片

**展示 3-5 条最佳引语，并标注演讲者信息。**

```bash
# Generate quote card backgrounds
infsh app run falai/flux-dev-lora --input '{
  "prompt": "minimal quote card background, subtle gradient from dark blue to black, large quotation mark watermark, clean modern design, social media square format",
  "width": 1080,
  "height": 1080
}'
```

### 视频 -> GIF 图片

**选取视频中的关键片段，时长 3-5 秒，文件大小不超过 5MB。**

适合制作 GIF 的场景包括：
- 观众的反应瞬间
- 事情发生前的/后的画面
- 关键演示步骤
- 有趣或令人惊讶的瞬间

### 长视频 -> 短片段

```bash
# Extract the best 15-60 second segments for Reels/TikTok/Shorts
# Focus on self-contained moments that make sense without context:
# - A single tip or insight
# - A surprising stat reveal
# - A demonstration of one feature
# - A strong opinion or hot take
```

## 重要原则

**切勿在不同平台之间直接复制粘贴内容。**每个平台都有其独特的特性：

| 平台 | 注意力持续时间 | 语言风格 | 格式要求 |
|----------|---------------|------|--------|
| 博文 | 5-10 分钟 | 详细、深入 | 长段落可接受 |
| 推特/微博 | 每条推文 5-30 秒 | 简洁、直接 | 最多 280 个字符 |
| LinkedIn | 1-3 分钟 | 专业、有深度 | 短段落，使用换行符 |
| 通讯文章 | 5-7 分钟 | 精选内容，个人化表达 | 分段式结构 |
| TikTok/Reels | 15-60 秒 | 生动、直接 | 需要在 1 秒内吸引观众注意 |
| 播客 | 20-60 分钟 | 对话式、深入讨论 | 允许插入故事和旁白 |

## 内容再利用检查清单

对于每篇长篇内容，应创建以下多种形式：
- [ ] 推特/微博帖子（5-8 条推文）
- [ ] LinkedIn 发布内容或轮播图
- [ ] 通讯文章中的摘要部分
- [ ] 3-5 张用于社交媒体的引语卡片
- [ ] 简短视频脚本（30-60 秒）
- [ ] 用于邮件推广的简短内容片段
- [ ] 用于内部演示的幻灯片

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 在不同平台之间直接复制粘贴 | 显得偷懒，且格式不正确 | 为每个平台重新编写内容 |
| 重复使用质量较差的内容 | 会削弱内容的价值 | 只应重新利用高质量的内容 |
| 同一天在所有平台发布 | 观众群体重叠可能导致重复内容 | 分散发布时间（几天或几周内） |
| 丢失核心信息 | 衍生内容会偏离原意 | 首先确定最重要的一个关键观点 |
| 不进行视觉改编 | 在视觉平台上仅使用纯文本 | 为每个平台制作专属的视觉素材 |
| 忘记标注来源 | 侵犯原作者的版权 | 必须注明内容来源 |

## 相关技能

```bash
npx skills add inference-sh/skills@ai-social-media-content
npx skills add inference-sh/skills@ai-image-generation
npx skills add inference-sh/skills@text-to-speech
npx skills add inference-sh/skills@twitter-automation
```

浏览所有可用工具：`infsh app list`