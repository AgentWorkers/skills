---
name: content-calendar
version: "1.0.0"
description: 规划、安排并跟踪多渠道的内容发布——包括新闻通讯、社交媒体、博客文章和视频。管理系统中的各个阶段、发布节奏以及内容再利用的时机。专为那些需要一套高效管理系统而非仅仅依赖电子表格的独立创业者及内容创作者设计。
tags: [content, calendar, newsletter, social-media, blog, publishing, scheduling, content-strategy, creator, solopreneur, pipeline, repurposing]
platforms: [openclaw, cursor, windsurf, generic]
category: productivity
author: The Agent Ledger
license: CC-BY-NC-4.0
url: https://github.com/theagentledger/agent-skills
---
# 内容日历

**由 The Agent Ledger 提供** — [theagentledger.com](https://theagentledger.com)

无需使用复杂的电子表格，即可规划、安排并跟踪您在各个渠道上的内容发布流程。此工具为代理人提供了一个结构化的系统，帮助管理从内容构思到最终发布的整个过程，并及时发现进度滞后的部分。

---

## 该工具的功能

您的代理人将能够：
- 按阶段（构思 → 草稿 → 审核 → 安排发布 → 已发布）来组织内容发布流程；
- 跟踪每个渠道（新闻通讯、博客、LinkedIn、X 等）的发布频率；
- 识别需要关注的内容——如逾期未完成的项目、计划中的空白环节或闲置的创意；
- 发现内容复用的机会——即现有内容可以适配到新渠道的情况；
- 每周提供一份内容概要，总结接下来 7 天的发布计划。

---

## 设置步骤（共 5 步）

### 第 1 步：创建内容工作区

在您的代理人工作区内创建一个名为 `content/CALENDAR.md` 的文件，并粘贴以下模板：

```markdown
# Content Calendar

_Last updated: [date]_

## Active Pipeline

| ID | Title | Type | Channel | Stage | Due Date | Notes |
|----|-------|------|---------|-------|----------|-------|
| C001 | | | | Idea | | |

## Publishing Cadence

| Channel | Frequency | Day/Time | Status |
|---------|-----------|----------|--------|
| Newsletter | Weekly | Thursday | Active |
| Blog | Bi-weekly | Monday | Active |
| LinkedIn | 3x/week | Mon/Wed/Fri | Active |
| X/Twitter | Daily | 9am | Active |

## Content Backlog (Unscheduled Ideas)

- [ ] [idea title] — [brief description]

## Published Archive

_Completed pieces move here after publishing._
```

### 第 2 步：定义您的渠道

根据实际使用的渠道，修改上述的发布频率表格。删除不使用的渠道信息，并补充缺失的渠道。如实填写发布频率——如果您实际上每周只发布一次内容，请相应地调整表格。

### 第 3 步：向代理人说明内容类型

在 `CALENDAR.md` 的顶部添加说明，列出您的内容类型及其典型的字数或格式要求：

```markdown
## Content Types
- **Newsletter** — ~800 words, personal tone, one main idea + links
- **Blog Post** — 1,200–2,000 words, SEO-focused, structured headers
- **LinkedIn Post** — 150–300 words, story format, one insight
- **X Thread** — 5–10 tweets, hook + value + CTA
- **YouTube Script** — 800–1,500 words, conversational
```

### 第 4 步：创建内容文件夹结构

```
content/
├── CALENDAR.md          ← pipeline overview (this file)
├── ideas/               ← rough idea notes
├── drafts/              ← in-progress pieces
├── published/           ← archive of completed work
└── repurpose/           ← repurposing queue
```

代理人在查找需要处理的内容时，会参考这个文件夹结构。

### 第 5 步：激活该工具

告诉代理人：
> “请阅读 ‘内容日历’ 工具并设置我的内容管理系统。使用 `content/` 目录下的文件。”

或者通过 `HEARTBEAT.md` 文件触发该工具的运行：

```markdown
## Content Calendar (every Monday)
- Review content/CALENDAR.md
- Flag anything due this week
- Surface 2-3 backlog ideas worth developing
- Check for pieces stuck in Draft >7 days
```

---

## 内容发布流程阶段

每份内容会依次经历以下阶段：

| 阶段 | 描述 | 典型耗时 |
|-------|-------------|-----------------|
| **构思** | 只有标题或概念，尚未开始编写 | 时间不定 |
| **大纲** | 已有结构，但尚未完成草稿 | 1–3 天 |
| **草稿** | 草稿已完成，但尚未审核 | 1–5 天 |
| **审核** | 准备进行最终编辑或审批 | 1–2 天 |
| **安排发布** | 内容已编写完毕，设定发布日期 | 完成 |
| **已发布** | 已上线——移至存档区 | 存档 |

**进度延迟标志**：任何处于“草稿”或“审核”阶段超过 7 天的内容都会在状态报告中被标记出来。

---

## 每周内容概要格式

当被要求提供内容概要时，代理人将生成如下格式的报告：

```
CONTENT BRIEF — Week of [date]

PUBLISHING THIS WEEK
━━━━━━━━━━━━━━━━━━━
• [Day] — [Channel]: [Title] (Stage: Scheduled ✅)
• [Day] — [Channel]: [Title] (Stage: Draft — needs ~2h to finish ⚠️)

OVERDUE / AT RISK
━━━━━━━━━━━━━━━━
• [Title] — [Channel] — was due [date], stuck in [Stage] for [X] days
  → Recommended action: [complete / reschedule / cut]

SCHEDULE GAPS
━━━━━━━━━━━━
• [Channel] has no content scheduled for [date range]
  → Backlog options: [list 2-3 relevant ideas]

REPURPOSE OPPORTUNITIES
━━━━━━━━━━━━━━━━━━━━━━
• "[Title]" (published [date]) → could become [format] for [channel]

NEXT WEEK PREVIEW
━━━━━━━━━━━━━━━━
• [Channel]: [Title] (Stage: Outline — on track)
• [Channel]: [TBD — needs idea]

RECOMMENDED ACTION TODAY
━━━━━━━━━━━━━━━━━━━━━━━
1. [Most urgent thing]
2. [Second thing]
3. [Third thing]
```

---

## 内容复用机制

优秀的 content 具有多重用途。请指示代理人查看过去 60 天内发布的所有内容，寻找复用的机会：

**常见的复用方式：**
- 新闻通讯文章 → LinkedIn 发布（提取核心观点）
- 博文 → X 平台帖子（拆分为 5–8 个要点）
- 长篇博客 → 短篇博客（分段发布）
- 视频脚本 → 博文（进行轻微格式调整）
- 新闻通讯 → 博文（添加 SEO 元数据和标题）

若需要标记可复用的内容，请在 `content/repurpose/queue.md` 文件中添加相应记录：

```markdown
| Original | Original Channel | Repurpose As | Target Channel | Status |
|----------|-----------------|--------------|----------------|--------|
| [Title] | Newsletter | Thread | X/Twitter | Todo |
```

---

## 内容创意收集

将初步的创意以纯文本形式保存到 `content/ideas/` 目录中。命名规则如下：

```
[topic-slug].md
```

**最低可行创意记录示例：**

```markdown
# [Idea Title]

**Angle:** [One sentence on the specific take]
**Channel:** [Best fit channel]
**Why now:** [Why this is relevant/timely]
**Hook:** [Draft hook if you have one]
**Related:** [Links to existing content it connects to]
```

代理人可以根据需要协助将创意发展成详细的大纲。

---

## 自定义选项

### 调整进度延迟阈值
默认值为 7 天。如需调整，请在 `CALENDAR.md` 中进行修改：

```markdown
## Settings
- Stall threshold: 5 days
- Overdue warning: 2 days before due date
```

### 主题分类
按主题对内容进行分类，以确保覆盖范围均衡：
```markdown
## Topic Clusters
- Business Systems (40%)
- AI / Automation (30%)
- Personal Productivity (20%)
- Industry News (10%)
```
代理人会监控某个主题在 4 周内的发布频率是否不足。

### 季节性内容标记
为时效性强的内容添加特殊标记：
```markdown
| ID | Title | ... | Notes |
|----|-------|-----|-------|
| C012 | Year-end recap | ... | ⏰ SEASONAL: must publish Dec 28-30 |
```

### 采用最低可行发布频率模式
如果您工作量较大，可指示代理人：
> “将内容日历设置为最低可行发布频率。”

系统将优先处理流量最高的渠道，并将其他渠道的内容标记为非必选项。

---

## 与其他 The Agent Ledger 工具的集成

| 工具 | 集成方式 |
|-------|-------------|
| **每日简报** | 在晨间简报中包含“今日需发布的内容” |
| **项目跟踪** | 将内容发布情况作为项目进行跟踪（例如：“项目 #5”） |
| **独立创业者助手** | 在每周业务回顾中审查内容发布情况 |
| **研究助手** | 研究成果直接用于内容创意的生成 |
| **收件箱分类** | 收集读者回复/反馈，以优化内容质量 |

---

## 常见问题解决方法

**“我的日历更新不及时”**
添加定期检查机制。对于大多数创作者来说，每周检查一次即可。如果您每天发布内容，则改为每天检查。

**“创意太多，无法优先处理”**
参考 `references/advanced-patterns.md` 中的评分标准，根据创意的难度和影响力对其进行排序。

**“总是错过发布计划”**
进行发布频率审核：统计过去 30 天实际发布的文章数量与计划发布的文章数量。根据实际情况调整发布频率表格，而非理想目标。

**“代理人总是忘记我已发布的内容”**
将已发布的文章移至 `content/published/` 目录，并更新 `CALENDAR.md` 中的存档部分。定期提醒代理人：“请更新内容存档文件。”

**“我想查看绩效数据”**
该工具主要跟踪发布流程，而非分析数据。如需绩效数据，请在 `content/published/[slug]-metrics.md` 文件中手动记录相关指标，并在内容复用决策时参考这些数据。

---

## 触发方式

当您说出以下指令时，该工具会自动启动：
- “我这周有哪些内容需要发布？”
- “给我一份内容概要”
- “我的内容发布流程是什么？”
- “我有一个新的内容创意：[创意内容]”
- “有哪些内容已经逾期未发布？”
- “我可以复用上个月的内容吗？”
- “查看我的内容日历”

---

*内容日历——由 The Agent Ledger 提供*
*欢迎在 [theagentledger.com](https://theagentledger.com) 订阅新工具及关于构建 AI 驱动系统的每周通讯。*
*许可协议：CC-BY-NC-4.0*