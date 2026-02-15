---
name: content-repurposing
description: |
  Content atomization — turn one piece of content into many formats.
  Covers blog-to-thread, blog-to-carousel, podcast-to-blog, video-to-quotes, and more.
  Use for: content marketing, social media, multi-platform distribution, content strategy.
  Triggers: content repurposing, repurpose content, content atomization, content recycling,
  one to many content, multi platform content, cross post, adapt content, reformat content,
  blog to thread, blog to video, podcast to blog, content multiplication
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

## 内容金字塔

一篇原始内容可以生成 10 多种衍生作品：

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

## 转换方法

### 博文 -> Twitter/X 线程

**提取 5-8 个关键观点，每个推文分享一个观点，并添加引导语。**

| 元素 | 规则 |
|---------|------|
| 引导语推文 | 采用列表文章、反向观点或承诺的形式 |
| 正文推文 | 每条推文分享一个观点，最多 280 个字符 |
| 视觉元素 | 每 3-4 条推文添加一张图片 |
| 最终推文 | 包含呼吁行动（CTA）以及“如果觉得有用，请转发第一条推文”的提示 |

**调整建议：**
- 去除细节和注意事项（线程内容需要简洁明了）
- 添加数字和具体信息（线程内容需要便于快速浏览）
- 减少学术性语言的使用（线程内容应更具有对话性）

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
| 1（引导语） | 标题中的醒目陈述或问题 |
| 2-9（正文） | 每张幻灯片展示一个关键点，并附上支持性的视觉元素 |
| 10（总结） | 回顾关键内容 |
| 11（呼吁行动） | “关注以获取更多内容” / “保存此内容” / “分享你的想法” |

**规格要求：** 1080x1080（方形）或 1080x1350（4:5 比例，以获得更多显示空间）

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

**3 行的摘要 + “为什么这很重要” + 链接。**

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
| 引导语 | 3 秒 | “大多数人误解了 [主题]。” |
| 问题 | 10 秒 | 说明常见的错误 |
| 观点 | 25 秒 | 你的关键发现或建议 |
| 证据 | 10 秒 | 一个统计数据或例子 |
| 呼吁行动 | 5 秒 | “关注以获取更多内容” / “在个人资料中添加链接” |

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

**展示 3-5 条最佳引语，并注明演讲者的名字。**

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
- 事情发生前的/后的对比画面
- 关键的操作步骤
- 有趣或令人惊讶的瞬间

### 长视频 -> 短片

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
| 博文 | 5-10 分钟 | 详细、深入 | 长段落可以接受 |
| Twitter/X | 每条推文 5-30 秒 | 简洁、直接 | 最多 280 个字符 |
| LinkedIn | 1-3 分钟 | 专业、有深度 | 短段落，适当使用换行 |
| 通讯文章 | 5-7 分钟 | 精选内容，个人化表达 | 分段式结构 |
| TikTok/Reels | 15-60 秒 | 有趣、直接 | 需要在 1 秒内吸引观众注意力 |
| 播客 | 20-60 分钟 | 对话式、深入探讨 | 允许插入故事和旁白 |

## 内容再利用检查清单

对于每篇长篇内容，需要创建以下多种形式：
- [ ] Twitter/X 线程（5-8 条推文）
- [ ] LinkedIn 发布内容或轮播图
- [ ] 通讯文章中的摘要部分
- [ ] 3-5 张用于社交媒体的引语卡片
- [ ] 短视频脚本（30-60 秒）
- [ ] 用于邮件营销的简短内容片段
- [ ] 用于内部演示的幻灯片

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 在不同平台之间直接复制粘贴 | 显得偷懒，且格式不正确 | 为每个平台重新编写内容 |
| 重复利用质量较差的内容 | 只会放大平庸的效果 | 仅重新利用质量最好的内容 |
| 在同一天将内容发布到所有平台 | 重复内容可能导致受众流失 | 分散发布时间（几天或几周） |
| 忽略核心信息 | 衍生内容会偏离原意 | 首先确定一个关键观点 |
| 不进行视觉改编 | 在视觉平台上仅使用纯文本 | 为每个平台制作专属的视觉素材 |
| 忘记标注来源 | 构成抄袭 | 必须注明原文链接 |

## 相关技能

```bash
npx skills add inferencesh/skills@ai-social-media-content
npx skills add inferencesh/skills@ai-image-generation
npx skills add inferencesh/skills@text-to-speech
npx skills add inferencesh/skills@twitter-automation
```

浏览所有可用工具：`infsh app list`