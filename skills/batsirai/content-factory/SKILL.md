---
name: content-factory
description: "多代理内容生成系统：一份原始内容可以生成多种格式，如社交媒体帖子、电子邮件、脚本、标题等。系统配备了五种专门的代理角色：作家（Writer）、混音师（Remixer）、编辑器（Editor）、编剧（Scriptwriter）和标题生成器（Headline Machine）。"
requiredEnv: []
permissions:
  - network: None required (optional — if spawning sub-agents via cloud API)
  - filesystem: Reads source content and writes output drafts to working directory
source:
  url: https://github.com/Batsirai/carson-skills
  author: Carson Jarvis (@CarsonJarvisAI)
  github: https://github.com/Batsirai/carson-skills
  verified: true
security:
  note: No API keys required for base operation. Sub-agent spawning is optional.
---
# 内容工厂 —— 多代理内容生产系统

> 一个来源 → 多种格式。一个系统 → 一致的品牌语言。

---

## 什么是内容工厂

内容工厂是一个结构化的内容生产系统。它不是由一个代理完成所有工作，而是由五个专门的代理角色分别处理内容制作的各个环节——每个角色都有特定的职责、模板和质量标准。

在以下情况下使用此功能：
- 用户希望从零开始创建内容，或者根据某个主题或研究资料来生成内容；
- 用户已经有一段内容，但希望将其适配到多个平台上；
- 用户希望在各种格式中保持一致的品牌语言；
- 用户希望有一个可重复的内容生产流程。

---

## 代理角色列表

| 代理 | 职责 | 输入 | 输出 |
|-------|------|-------|--------|
| **作家** | 创作长篇内容草稿 | 主题 + 研究资料 | 文章、论文、指南、新闻通讯 |
| **改编者** | 将内容适配到多个平台 | 已完成的原始内容 | Twitter帖子、LinkedIn帖子、电子邮件正文、图片说明文字、脚本 |
| **编辑** | 提高内容的清晰度与可读性 | 草稿内容 | 可发布的内容 |
| **编剧** | 创作视频和动画脚本 | 主题或原始内容 | 30秒的吸引人的开头、剧集脚本 |
| **标题生成器** | 生成吸引人的标题 | 主题 + 目标受众 + 表达角度 | 按预估点击率排序的20个标题 |

---

## 内容制作流程

```
Topic/Research/Brain Dump
        ↓
    [WRITER] → Long-form draft
        ↓
    [EDITOR] → Clarity + polish pass
        ↓
    [REMIXER] → Twitter, LinkedIn, email, captions, slides
    [SCRIPTWRITER] → Video scripts + animation hooks
    [HEADLINE MACHINE] → Distribution hooks for each format
```

您可以运行整个流程，也可以直接选择任何一个代理来开始工作。

---

## 如何触发每个代理

告诉代理应采用的角色，提供相应的输入内容，并指定所需的输出格式。

```
# Full pipeline
"Run the content factory on this article: [paste or link]. I need LinkedIn, Twitter thread, email, and 3 headline options."

# Just the writer
"Act as the Writer agent. Write a 1,200-word article on [topic] for [target audience]. Use the first-draft template."

# Just the remixer
"Act as the Remixer. Take this article and produce: Twitter thread, LinkedIn post, email newsletter section, and 5 pull quotes."

# Just the editor
"Act as the Editor. Cut this draft by 30%, sharpen the voice, and flag anything unclear."

# Just the scriptwriter
"Act as the Scriptwriter. Write a 30-second hook script for this article. Include visual direction notes."

# Just the headline machine
"Act as the Headline Machine. Generate 20 headlines for this article using the headline formulas."
```

---

## 代理使用说明

### 作家 —— 草稿创作引擎

**职责：** 根据研究资料、笔记或灵感创作长篇内容。

**工作流程：**
1. **从读者的需求出发** —— 而不是从主题开始。他们面临什么问题？
2. **用故事吸引读者** —— 用一个他们能产生共鸣的瞬间来吸引他们。
3. **采用易于阅读的结构** —— 使用小标题和短段落，每个段落只表达一个主要观点。
4. **给出行动建议** —— 阅读完内容后，读者应该采取什么行动？

**可用模板：**
- `prompts/first-draft.md` —— 用于将笔记转化为文章
- `prompts/argument-builder.md` —— 用于撰写有说服力的观点性文章
- `prompts/research-pipeline.md` —— 用于基于研究的文章
- `prompts/story-overlay.md` —— 当内容需要叙事结构时使用

**质量标准：**
- 避免冗长的段落；如果某个部分没有实际意义，就删除它。
- 使用具体而非抽象的语言。
- 统计数据需要来源；观点需要明确的框架。
- 将输出内容大声朗读一遍。如果听起来平淡无味，就重新编写。

**输出格式：**
```markdown
# [Headline]

[Hook — 1-2 sentences, specific moment or question]

[Body — structured with H2 subheadings]

[Closing — action step or reflection prompt]

---
Meta:
- Word count: [X]
- Target audience: [who]
- Voice: [whose voice / what tone]
```

---

### 改编者 —— 格式转换专家

**职责：** 将一段原始内容转换为多个平台适合的格式。

**工作流程：**
1. **提取核心信息** —— 用一句话概括主要内容。
2. **找出能吸引读者的关键点** —— 什么能让他们停下浏览的元素？
3. **根据平台调整语言风格** —— 每个平台都有其独特的语言风格。
4. **保持信息的完整性** —— 内容的核心观点不变，只是表现形式不同。

**输出格式：**

#### Twitter/X帖子
- 第一条推文：用一个能吸引读者的开头吸引他们继续阅读。
- 每条推文只表达一个主要观点。
- 最后一条推文包含行动号召或总结。
- 不使用标签。避免长篇大论。
- 长度：6–12条推文。

#### LinkedIn帖子
- 以深刻的见解开头，而不是“我一直在思考……”
- 150–300字适合广泛传播；故事较长时使用更多字数。
- 每1–2句后换行。
- 以一个问题结尾，鼓励读者评论。
- 文末使用3–5个标签。

#### 电子邮件新闻通讯
- 标题要引起读者的好奇心（测试：你会打开这封邮件吗？）
- 采用个人化的语气，就像是在给某个朋友写信一样。
- 包含一个明确、具体的行动号召。
- 200–350字。

#### Instagram图片说明文字
- 第一行是吸引人的开头（必须能激发读者点击的兴趣）。
- 100–200字。
- 适当换行以提高可读性。
- 文末使用5–10个相关的标签。

#### 30秒视频脚本
- 开场吸引人的部分：3秒（抓住读者的注意力）。
- 核心信息：20秒（提供价值）。
- 结尾部分：7秒（包含行动号召或总结）。
- 为每个部分提供视觉方向的指导。

#### 幻灯片大纲
- 每张幻灯片只表达一个主要观点。
- 使用项目符号，避免长段落。
- 附上演讲者的备注以提供背景信息。

#### 摘录（5种格式）
- 独立摘录，无需上下文即可引用。
- 每条摘录不超过280个字符。

#### 常见问题解答（5个问题）
- 针对读者实际会提出的问题。
- 直接给出答案，避免含糊其辞。

**平台规则：**
- **Twitter/X:** 不使用标签。帖子的开头非常重要。
- **LinkedIn:** 开头不要使用表情符号。保持专业性。
- **Instagram:** 以视觉内容为主。图片说明文字应辅助内容，不要重复图片内容。
- **电子邮件:** 标题是吸引读者的关键。

---

### 编辑 —— 内容优化专家

**职责：** 优化草稿，使其适合发布。

**优化流程（共5轮）：**

**第1轮：** 提高清晰度
- 至少减少30%的文字量。
- 删除行话、被动语态和含糊的词语（如“也许”、“可能”、“可以”等）。
- 用具体的动词替换抽象名词。
- 将超过20个字的句子拆分成更短的部分。
- 除非确实有必要，否则删除副词。

**第2轮：** 确保故事连贯性和流畅性
- 开头的吸引人的部分是否能在2句话内表达清楚？
- 各部分之间的过渡是否自然？
- 句子的长度是否合理？

**第3轮：** 确保语言风格一致
- 这种表达方式是否符合预期的品牌语言风格？
- 删除陈词滥调。
- 用具体的词语替换泛泛而谈的表述。

**第4轮：** 质量检查
- 避免使用带有情感操控的语言（如“内疚”、“羞愧”、“恐惧”或虚假的紧迫感）。
- 不要做出没有依据的声明。
- 避免使用可能适用于任何公司的通用表述。

**第5轮：** 技术性润色
- 检查语法、拼写和标点符号。
- 小标题要具有描述性且易于阅读。
- 提供完整的元信息。

**输出格式：**
```markdown
# [Title] — EDITED

[Clean final version]

---
## Edit Report
- Word count: Before [X] → After [Y] ([Z]% reduction)
- Major changes: [list with reasoning]
- Voice match: [assessment]
- Confidence: [ready to publish / needs review on X]
```

---

### 编剧 —— 视频和动画脚本制作人

**职责：** 创作30秒的吸引人的开头、剧集脚本和动画脚本。

**工作流程：**
- **以视觉效果为先** —— 每句话都应该对应一个视觉元素。
- **开头3秒内吸引观众** —— 第一帧和第一句话决定了观众是否会继续观看。
- **每个部分只表达一个主要观点** —— 不要试图包含过多的信息。
**脚本格式：**
```markdown
## [Title] — [Duration] Script

**HOOK (0–3s):**
Visual: [what the viewer sees]
Audio: "[what they hear]"

**BODY (3–[N]s):**
Visual: [description]
Audio: "[dialogue or narration]"

**CLOSE ([N]–[total]s):**
Visual: [closing scene]
Audio: "[CTA or reflective line]"

---
Production notes: [pacing, tone, music direction]
```

### 标题生成器 —— 标题创意专家

**职责：** 为任何内容生成20个以上的标题和吸引人的开头。

**标题生成公式：**

| 公式 | 例子 |
|---------|---------|
| 数字 + 好处 | “7种方法将内容创作时间缩短一半” |
| 问题 | “你是否浪费了80%的内容价值？” |
- 操作指南 | “如何将一篇博客文章转化为一个月的社交媒体内容” |
- 反直觉的观点 | “为什么减少发布频率反而让我们的受众增长了3倍” |
- 具体的结果 | “这个系统能从一篇文章生成60篇内容” |
- 警告 | “在尝试这个方法之前，请先停止创建新内容” |
- 对比前后 | “从一个想法到12种格式，只需一小时” |
- 秘密/未知的信息 | “大多数创作者不知道的内容再利用策略” |

**输出：** 根据预估的点击率生成20个标题，并对前5个标题提供理由。

---

## 内容创作原则（适用于所有代理）

**写作时应遵循的原则：**
- 每篇文章只表达一个主要观点。
- 使用具体的表述方式（例如：“我们将制作时间缩短了60%”，而不是“我们提高了效率”）。
- 用具体的例子来展示效果，而不是空洞的描述。
- 用有趣的内容开头吸引读者。

**绝对不要使用的表述：**
- “深入探讨”、“充分利用”、“利用”、“发挥潜力”、“激动人心的宣布”、“颠覆性的创新”、“在当今快节奏的世界里”、“比以往任何时候都更……”
- 任何可能适用于任何公司的通用表述。

**人类测试原则：** 在最终确定内容之前，问自己：“如果是一个真实的人，他会把这些话直接告诉朋友吗？” 如果答案是否定的，就重新修改。

---

## 分工协作（针对复杂项目）

对于大型内容项目，可以为每个角色分配专门的子代理来协助工作。

```
# Spawn a writer for a long article
sessions_spawn --task "Act as the Writer agent (Content Factory skill). Write a 1,500-word article on [topic] for [audience]. Tone: [voice]. Use prompts/first-draft.md format."

# Spawn the remixer after the article is done
sessions_spawn --task "Act as the Remixer agent (Content Factory skill). Remix this article into: Twitter thread, LinkedIn post, email section, and 5 pull quotes. Source: [article]"
```

---

## 文件结构

```
content-factory/
├── SKILL.md                    ← This file
├── README.md                   ← Human-readable overview
└── prompts/
    ├── first-draft.md          ← Brain dump → structured article
    ├── argument-builder.md     ← Thesis → persuasive essay
    ├── clarity-pass.md         ← Cut 30%, remove jargon
    ├── remix-engine.md         ← One piece → 10 formats
    ├── research-pipeline.md    ← Sources → original article
    ├── headlines.md            ← 20 headlines from formulas
    ├── empathy-rewrite.md      ← Technical → accessible
    ├── story-overlay.md        ← Boring → narrative structure
    ├── polish-pass.md          ← Final edit checklist
    └── voice-cloner.md         ← Match writing style
```

---

*内容工厂 v1.0 — 2026年2月*
*由Carson Jarvis (@CarsonJarvisAI)开发*