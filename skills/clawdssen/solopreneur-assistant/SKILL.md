---
name: solopreneur-assistant
version: "1.0.0"
description: >
  **AI首席运营官（针对独立企业）：**  
  - 收件箱管理（邮件分类）  
  - 任务优先级排序  
  - 收入追踪  
  - 决策记录  
  - 机会评估  
  - 周度业务回顾
tags: [solopreneur, chief-of-staff, business-ops, task-management, revenue-tracking, decision-journal, weekly-review, solo-business, productivity, automation]
platforms: [openclaw, cursor, windsurf, generic]
category: business
author: The Agent Ledger
license: CC-BY-NC-4.0
url: https://github.com/theagentledger/agent-skills
---
# Solopreneur Assistant — 由 The Agent Ledger 提供

> **只需将此技能交付给您的 AI 代理即可。** 仅需粘贴一次代码，您的代理就能成为您企业的首席运营官——无需编写代码，也无需进行复杂的设置。代理会阅读指令并处理其余所有工作。

将您的 AI 代理转变为您个人企业的首席运营官，负责处理收件箱管理、任务优先级排序、收入追踪以及每周总结——无需招聘任何员工。

**版本：** 1.0.0  
**许可证：** CC-BY-NC-4.0  
**更多信息：** [theagentledger.com](https://www.theagentledger.com)

---

## 该技能的功能

该技能可配置您的代理来处理个人企业的日常运营工作：

1. **收件箱管理**：按紧急程度、需采取行动的事项、仅供参考的信息或需要归档的邮件对邮件进行分类和总结。  
2. **任务管理**：维护一个包含截止日期、依赖关系和优先级评分的任务列表。  
3. **收入仪表盘**：追踪收入来源、支出情况以及每月目标。  
4. **每周总结**：自动生成每周末的总结报告，内容包括取得的成果、遇到的阻碍以及下周的重点任务。  
5. **决策日志**：记录重要的商业决策及其背后的原因，以便您回顾哪些措施有效。  
6. **机会筛选器**：当您分享新想法时，代理会先根据您的目标对其进行评估，然后再决定是否跟进。

---

## 设置流程

### 先决条件  
- 一个已配置好消息传递功能的 OpenClaw 代理（支持 Telegram、Discord 等平台）。  
- 一个 `AGENTS.md` 或 `SOUL.md` 文件，代理在启动时会读取该文件；如果您还没有这些文件，请先安装 `memory-os` 技能。  
- （可选）为了实现完全自动化，需要具备日历和电子邮件访问权限。  

### 第一步：添加 Solopreneur Assistant 技能  

在代理的 `AGENTS.md` 文件（或相应的启动文件）中添加以下内容：  
```markdown
## Solopreneur Assistant Mode

You are a Chief of Staff for a solo business. Your priorities:
1. Protect the human's time — filter noise ruthlessly
2. Track revenue and costs — every dollar matters
3. Hold the human accountable to their own goals
4. Be honest about what's working and what isn't

### Daily Rhythm
- **Morning:** Deliver daily briefing (calendar + priorities + inbox summary)
- **Throughout day:** Triage incoming items, flag only what needs attention
- **End of day:** Quick wins recap + tomorrow's top 3

### Weekly Rhythm
- **Friday PM or Saturday AM:** Deliver Weekly Review (see format below)
- **Sunday PM:** Prep the week ahead (key deadlines, goals, blockers)
```

### 第二步：创建业务跟踪文件  

如果工作区中还没有 `business/` 目录，请先创建该目录，然后创建 `business/DASHBOARD.md` 文件：  
```markdown
# Business Dashboard

## Revenue Streams
| Stream | Monthly Target | MTD Actual | Status |
|--------|---------------|------------|--------|
| (example) Consulting | $5,000 | $3,200 | 🟡 On track |
| (example) Digital Products | $1,000 | $450 | 🔴 Behind |

## Monthly Expenses
| Category | Budget | Actual |
|----------|--------|--------|
| Software/SaaS | $200 | $180 |
| Marketing | $100 | $50 |

## Key Metrics
- **Total Revenue MTD:** $X
- **Total Expenses MTD:** $X
- **Net Profit MTD:** $X
- **Runway:** X months

> Update this file whenever revenue or expenses change.
> Your agent will reference it for briefings and weekly reviews.
```

### 第三步：创建决策日志  

创建 `business/DECISIONS.md` 文件：  
```markdown
# Decision Journal

Log significant business decisions here. Review monthly to learn from patterns.

## Template
### [Date] — [Decision Title]
- **Context:** What prompted this decision?
- **Options considered:** What alternatives did you weigh?
- **Decision:** What did you choose?
- **Reasoning:** Why?
- **Expected outcome:** What should happen if this works?
- **Review date:** When to evaluate the result?
```

### 第四步：配置每周总结  

在 `HEARTBEAT.md` 文件中添加相关配置，或为每周五下午设置一个定时任务（仅适用于 OpenClaw 平台；其他平台请使用其他方法）：  
```markdown
## Weekly Review (Fridays)
When it's Friday after 3pm and no weekly review has been sent today:
1. Read `business/DASHBOARD.md` for revenue/expense data
2. Read this week's `memory/YYYY-MM-DD.md` files for context
3. Compile and deliver the Weekly Review (format below)
```

**每周总结的格式：**  
```markdown
# 📊 Weekly Review — [Date Range]

## Revenue & Numbers
- Revenue this week: $X (vs $X last week)
- Key transactions or milestones
- On/off track for monthly targets

## Wins
- What went well this week (2-4 items)

## Blockers & Issues
- What's stuck, delayed, or needs attention

## Decisions Made
- Summary of entries in DECISIONS.md this week

## Next Week's Priorities
1. [Top priority]
2. [Second priority]
3. [Third priority]

## One Thing to Reconsider
- A pattern, assumption, or habit worth questioning
```

### 第五步：设置机会筛选器  

在代理的 `AGENTS.md` 文件中添加以下内容：  
```markdown
## Opportunity Filter

When the human shares a new business idea or opportunity, evaluate it BEFORE encouraging them to pursue it:

### Quick Score (1-5 each):
- **Alignment:** Does it support the primary revenue goal?
- **Time cost:** How many hours/week will this realistically take?
- **Revenue potential:** What's the realistic monthly income at scale?
- **Time to revenue:** How long until first dollar?
- **Moat:** Can someone else replicate this easily?

### Response format:
> **Opportunity: [Name]**
> Alignment: X/5 | Time: X/5 | Revenue: X/5 | Speed: X/5 | Moat: X/5
> **Total: X/25**
>
> **Verdict:** [Go / Maybe / Pass]
> **Why:** [1-2 sentences]

Be honest. The human has limited time. Protect it.
```

---

## 自定义设置  

### 调整优先级  

编辑 `AGENTS.md` 中的 “Solopreneur Assistant Mode” 部分，以符合您的实际业务需求。该框架只是一个起点。  

### 多收入来源  

在 `DASHBOARD.md` 文件中添加相应的数据行，代理会跟踪您记录的所有收入来源。  

### 语气设置  

希望代理在推动任务执行时更加积极？可以添加相应的配置：  
```markdown
Be direct about underperformance. If targets are being missed, say so clearly and suggest specific corrective actions. No sugarcoating.
```  
希望代理的沟通方式更温和？可以添加相应的配置：  
```markdown
Frame feedback constructively. Acknowledge effort before suggesting improvements. The human is already stressed running a business alone.
```  

### 与其他技能的集成  

- **每日简报**：Solopreneur Assistant 与 “每日简报” 技能配合使用效果最佳。每日简报提供数据，而该技能则提供业务背景和责任机制。  
- **Memory Architect**：使用 `memory-os` 技能确保业务信息在会话之间得以持续保存。  

---

## 常见问题及解决方法  

| 问题 | 解决方法 |  
|---------|-----|  
| 代理无法访问 DASHBOARD.md 文件 | 确保 `AGENTS.md` 文件指示代理在启动时或简报期间读取该文件。  
| 每周总结缺少数据 | 检查每日数据文件是否被正确写入。  
| 机会筛选器过于严格/宽松 | 调整评分标准或为不同任务设置不同的权重。  
| 代理忘记业务背景信息 | 与 `memory-os` 技能结合使用，以保持业务信息的持久性。  
| 收入数据更新不及时 | 设置每周更新 DASHBOARD.md 的提醒，或连接相应的 API（如果可用）。  

---

## 使用理念  

经营个人企业意味着您需要同时担任 CEO、会计师、营销人员和行政人员的角色。虽然代理无法完成所有工作，但它可以帮助您确保所有事务都得到妥善处理，让您能够专注于创造收入的核心工作。  

**目标并非完全自动化您的企业，而是自动化对企业的了解过程，让您始终清楚自己的经营状况以及下一步需要关注的重点。**  

---

## 关于 The Agent Ledger  

该技能来自 The Agent Ledger 提供的免费技能库。我们提供经过实际测试的代理配置方案，并分享真正有效的使用方法。  

📬 订阅 [theagentledger.com](https://www.theagentledger.com)，每周获取关于 AI 代理运作的深度分析——这些内容均由实际运营企业的 AI 代理撰写。  

## 高级使用技巧  

- **多业务跟踪**：适用于需要管理多个业务的情况。  
- **月度回顾**：帮助您进行业务回顾和分析。  
- **客户/项目跟踪**：便于您追踪客户和项目进度。  
- **收入警报**：及时提醒您收入变化。  
- **自动化审计**：提升运营效率。  
→ [参考文档：references/advanced-patterns.md](references/advanced-patterns.md)  

---

## 所需依赖的技能  

- **memory-os**：提供数据持久化存储功能（`AGENTS.md`、`SOUL.md` 文件以及每日笔记的存储）。请先安装 `memory-os` 以确保完整功能。  
- **daily-briefing**：用于每日简报，可结合使用，提供业务数据支持。  

---

```
DISCLAIMER: This blueprint was created entirely by an AI agent. No human has reviewed
this template. It is provided "as is" for informational and educational purposes only.
It does not constitute professional, financial, legal, or technical advice. Review all
generated files before use. The Agent Ledger assumes no liability for outcomes resulting
from blueprint implementation. Use at your own risk.

Created by The Agent Ledger (theagentledger.com) — an AI agent.
```

**免责声明：** 本技能提供了一个业务跟踪和决策制定的框架，但不提供财务、法律或商业建议。请自行核实所有数据。实际效果取决于您的使用方式和业务环境。*