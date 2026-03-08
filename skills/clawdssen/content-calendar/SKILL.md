---
name: content-calendar
version: "1.0.0"
description: >
  **内容规划、调度与跟踪工具：**  
  支持在多种渠道（如新闻通讯、社交媒体、博客文章和视频）中统一规划、安排和跟踪内容发布。能够管理内容发布的各个阶段、发布频率，并充分利用现有资源进行内容再利用。专为那些希望使用系统化工具而非简单电子表格来管理工作的独立创业者及内容创作者设计。
tags: [content, calendar, newsletter, social-media, blog, publishing, scheduling, content-strategy, creator, solopreneur, pipeline, repurposing]
platforms: [openclaw, cursor, windsurf, generic]
category: productivity
author: The Agent Ledger
license: CC-BY-NC-4.0
url: https://github.com/theagentledger/agent-skills
---
# 内容日历  
**由 The Agent Ledger 提供** — [theagentledger.com](https://theagentledger.com)  

您可以轻松规划、安排并跟踪所有渠道的内容发布流程，无需再依赖繁琐的电子表格。该工具为您的团队成员提供了一个结构化的系统，帮助他们从内容构思到最终发布的全过程进行管理，并及时发现进度滞后的项目。  

---

## 该工具的功能  
您的团队成员将能够：  
- 按阶段（构思 → 草稿 → 审核 → 预定发布 → 已发布）来管理内容流程；  
- 监控每个渠道（如新闻通讯、博客、LinkedIn、X 等）的发布频率；  
- 识别需要关注的内容——例如逾期未完成的稿件、计划中的空白环节或闲置的创意；  
- 发现内容复用的机会——即现有内容能否适配新的发布渠道；  
- 每周提供一份内容概要，总结接下来 7 天的发布计划。  

---

## 设置步骤（共 5 步）  
### 第 1 步：创建内容工作区  
在您的团队工作区中创建一个名为 `content/CALENDAR.md` 的文件，并粘贴以下模板：  
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

### 第 2 步：定义您的发布渠道  
根据实际使用的渠道，修改上述的发布频率表格。删除不使用的渠道信息，并补充缺失的渠道。请如实填写发布频率——如果实际每周只发布一次内容，请相应调整。  

### 第 3 步：告知团队成员内容类型  
在 `CALENDAR.md` 的顶部添加说明，列出所有内容类型及其典型的字数或格式要求：  
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
团队成员在查找待处理内容时，会参考这个文件夹结构。  

### 第 5 步：激活该工具  
告知团队成员：  
> “请阅读 ‘内容日历’ 工具并设置好您的内容管理系统。使用 `content/` 目录下的相关文件。”  
或者通过 `HEARTBEAT.md` 文件触发该工具的更新：  
```markdown
## Content Calendar (every Monday)
- Review content/CALENDAR.md
- Flag anything due this week
- Surface 2-3 backlog ideas worth developing
- Check for pieces stuck in Draft >7 days
```  

---

## 内容发布流程  
每篇内容会依次经历以下阶段：  
| 阶段 | 描述 | 通常耗时 |  
|-------|-------------|-----------------|  
| **构思** | 只有标题或概念，尚未开始写作 | 不定期 |  
| **大纲** | 已制定大纲，但未完成草稿 | 1–3 天 |  
| **草稿** | 草稿已完成，但尚未审核 | 1–5 天 |  
| **审核** | 准备进行最终编辑或审批 | 1–2 天 |  
| **预定发布** | 写作完成，设定发布日期 | 完成 |  
| **已发布** | 已上线发布 | 移至存档区 |  

**进度警告**：任何处于“草稿”或“审核”阶段超过 7 天的内容都会在状态报告中被标记出来。  

---

## 每周内容概要格式  
当需要获取内容概要时，团队成员会生成如下格式的报告：  
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
优质的内容具有多重用途。请告知团队成员：查看过去 60 天内发布的所有内容，寻找复用的机会。  
**常见的复用方式包括：**  
- 将新闻通讯文章改编为 LinkedIn 发文（提取核心观点）；  
- 将长篇博客文章拆分为多篇短文；  
- 将视频脚本重新格式化为博客文章；  
- 为新闻通讯添加 SEO 元数据和标题等。  

若需标记可复用的内容，请在 `content/repurpose/queue.md` 文件中添加相应记录：  
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
团队成员可根据需要协助将创意进一步发展为完整的大纲。  

---

## 自定义选项  
### 调整进度警告阈值  
默认设置为 7 天。如需调整，请在 `CALENDAR.md` 中进行修改：  
```markdown
## Settings
- Stall threshold: 5 days
- Overdue warning: 2 days before due date
```  

### 主题分类  
按主题对内容进行分类，以确保内容覆盖均衡：  
```markdown
## Topic Clusters
- Business Systems (40%)
- AI / Automation (30%)
- Personal Productivity (20%)
- Industry News (10%)
```  
如果某个主题在连续 4 周内的发布频率过低，系统会自动发出提醒。  

### 季节性内容标记  
为时效性强的内容添加特殊标记：  
```markdown
| ID | Title | ... | Notes |
|----|-------|-----|-------|
| C012 | Year-end recap | ... | ⏰ SEASONAL: must publish Dec 28-30 |
```  

### 低优先级发布模式  
如果您工作量较大，可告知团队成员：  
> “将内容日历设置为低优先级发布模式。”  
此时系统会优先处理流量最高的渠道，其余内容将被视为非强制性任务。  

---

## 与其他 The Agent Ledger 工具的集成  
| 工具 | 集成方式 |  
|-------|-------------|  
| **每日简报** | 在晨间简报中包含“今日需发布的内容”；  
| **项目跟踪** | 将内容发布情况作为项目进行跟踪（例如：“项目 #5”）；  
| **独立创业者助手** | 在每周业务回顾中检查内容发布进度；  
| **研究助手** | 研究成果直接用于内容创意生成；  
| **收件箱管理** | 收集读者反馈以优化内容质量。  

---

## 常见问题及解决方法  
- **“日历更新不及时”**：  
  添加定期检查机制（建议每周检查一次）。如果您每天发布内容，可改为每日检查。  
- **创意太多，难以优先处理**：  
  参考 `references/advanced-patterns.md` 中的评分标准，根据内容的重要性和难度进行排序。  
- **经常错过发布计划**：  
  审查过去 30 天实际发布的文章数量与计划数量，根据实际情况调整发布频率。  
- **团队成员忘记已发布的内容**：  
  将已发布的内容移至 `content/published/` 目录，并更新 `CALENDAR.md` 的存档信息。定期提醒团队成员更新存档内容。  
- **需要跟踪绩效数据**：  
  该工具主要关注内容发布流程，而非数据分析。请在 `content/published/[slug]-metrics.md` 文件中手动记录相关数据，并据此制定复用策略。  

---

## 触发指令  
您可以通过以下指令激活该工具：  
- “我这周有哪些内容需要发布？”  
- “给我一份内容概要。”  
- “我的内容流程中有哪些项目？”  
- “我有一个新的创意：[创意内容]”  
- “有哪些内容已经逾期未发布？”  
- “上个月的内容有哪些可以复用？”  
- “帮我查看一下内容日历。”  

---

*内容日历——由 The Agent Ledger 提供*  
*欢迎在 [theagentledger.com](https://theagentledger.com) 订阅新工具及每周关于 AI 技术应用的资讯通讯。*  
*许可证：CC-BY-NC-4.0*  

> **免责声明：**  
  本工具由 AI 生成，仅用于提供信息和建议。它不提供专业、财务、法律或技术方面的建议。使用前请仔细阅读所有生成的文件。The Agent Ledger 对使用结果概不负责。使用本工具需自行承担风险。