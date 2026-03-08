---
name: meeting-assistant
version: "1.0.0"
url: https://github.com/theagentledger/agent-skills
description: >
  **AI会议助手：专为自由职业者和专业人士设计**  
  该工具能够根据您的笔记和背景信息自动生成会议前的简要资料，实时记录会议中的重要内容，并为相关责任人生成包含任务清单和截止日期的总结报告。  
  它可与项目跟踪系统、邮件分类工具、客户关系管理工具以及自由职业者辅助工具无缝集成，帮助您更高效地管理会议和日常事务。
tags: [meetings, notes, action-items, productivity, solopreneur, crm, project-management]
platforms: [openclaw, cursor, windsurf, generic]
category: productivity
author: The Agent Ledger
license: CC-BY-NC-4.0
---
# 会议助手  
**由 [The Agent Ledger](https://theagentledger.com) 提供**  

*永远不要忘记会议中做出的决定，也千万不要错过任何后续行动。在参加会议前，一定要做好充分的准备。*  

---

## 该技能的功能  

该技能能将您的代理转变为会议管理的得力助手，帮助您：  
- **在会议前** 通过结构化的会议简报（包括会议背景、目标、讨论要点及待解决的问题）为您做好充分准备；  
- **在会议期间或会议结束后** 立即将会议内容以清晰、易于阅读的格式记录下来；  
- **提取** 会议中的行动项，包括负责人员、截止日期和优先级；  
- **整理** 会议记录，以便日后能够方便地查找和引用相关决策；  
- **进行后续跟进**，提醒您未完成的行动项以及逾期的承诺。  

该技能适用于各种类型的会议：客户电话会议、团队例会、投资者沟通、供应商谈判、一对一会议以及战略讨论会等。  

---

## 设置步骤（共4步）  

### 第1步：将技能添加到 `AGENTS.md` 文件中  

将以下代码段添加到您的 `AGENTS.md` 文件中：  
```markdown
## Meeting Assistant (Agent Ledger Skill)

You have a meeting management system. For all meeting-related requests:

**Pre-meeting:** When I say "prep for [meeting name]" or "meeting brief", generate a structured brief.
**During/after:** When I say "meeting notes" or "capture notes", create a structured meeting record.
**Action items:** When I say "action items" or "follow-ups", extract and list all commitments.
**Review:** When I say "meeting review" or "open actions", surface unresolved items from recent meetings.

State file: meetings/meeting-log.md (create if missing)
Active actions file: meetings/open-actions.md (create if missing)
Meeting archive: meetings/YYYY-MM/ (organize by month)

Capture format: Brief → Notes → Actions → Filed. Never skip the action item step.
```  

### 第2步：创建会议文件夹  

您的代理会自动创建相应的会议文件。文件夹结构如下：  
```
meetings/
  meeting-log.md          ← index of all meetings (title, date, type, key decision)
  open-actions.md         ← running list of unresolved action items across all meetings
  YYYY-MM/
    YYYY-MM-DD-meeting-name.md   ← individual meeting records
```  

### 第3步：初始化状态文件  

请您的代理执行以下命令：  
> “初始化我的会议助手。按照标准格式创建 `meetings/meeting-log.md` 和 `meetings/open-actions.md` 文件。”  

系统将生成：  
- `meetings/meeting-log.md`：  
```markdown
# Meeting Log

| Date | Meeting | Type | Key Decision | File |
|------|---------|------|--------------|------|
| (populated automatically) |
```  
- `meetings/open-actions.md`：  
```markdown
# Open Action Items

Last reviewed: YYYY-MM-DD

| # | Action | Owner | Due | Meeting | Status |
|---|--------|-------|-----|---------|--------|
| (populated automatically) |
```  

### 第4步：首次使用该技能  

尝试输入如下命令：  
*“为与 [公司名称] 的30分钟销售沟通会议准备会议简报。他们对我们提供的 [产品/服务] 感兴趣，我们之前已经有过一次交流。”*  

---

## 使用方式  

### 会议前准备简报  

**触发命令**：`Prep brief for [会议名称]` 或 `meeting brief: [会议详情]`  
**需要包含的信息**：会议名称、参会人员、会议时长、会议目的以及任何相关的背景信息。  
**示例**：  
> “为与 Acme Corp. 的每周例会准备简报，会议时长30分钟，内容为第一季度项目进展更新。上次会议中我们确定了新的时间表。”  

**输出格式**：  
```markdown
## Meeting Brief — Acme Corp Weekly Check-in
**Date/Time:** [to confirm]
**Duration:** 30 min
**Attendees:** [you] + Acme Corp contact(s)
**Meeting Type:** Client check-in

### Context
[Summary of relationship, project background, last touchpoint]

### Goals for This Meeting
1. [Primary goal]
2. [Secondary goal]

### Talking Points
- [Key update to share]
- [Decision that needs resolution]
- [Question to ask]

### Open Items from Last Meeting
- [ ] [Unresolved action from prior call]

### Questions to Ask
- [Question 1]
- [Question 2]

### Watch For
- [Potential concern or signal to notice]
```  

### 记录会议内容  

**触发命令**：`Meeting notes: [粘贴或口述会议内容]` 或 `Capture this meeting: [会议详情]`  
**示例**：  
> “会议记录：与 Acme 公司的通话，时长45分钟，Sarah 和 Tom 参加了会议。他们批准了修订后的项目范围。Tom 对三月的截止日期表示担忧，建议增加一周的缓冲时间。我们同意将交付日期推迟到3月14日。Sarah 将在周五下班前发送更新后的合同，而我将在周三之前发送修订后的项目计划。”  

**输出格式**：  
```markdown
## Meeting Notes — Acme Corp Weekly Check-in
**Date:** YYYY-MM-DD
**Duration:** 45 min
**Attendees:** [You], Sarah (Acme), Tom (Acme)
**Meeting Type:** Client check-in

### Summary
[2-3 sentence recap of what happened and what was decided]

### Key Decisions
- [Decision 1]
- [Decision 2]

### Discussion Notes
- [Topic 1]: [What was said]
- [Topic 2]: [What was said]

### Action Items
| # | Action | Owner | Due | Priority |
|---|--------|-------|-----|----------|
| 1 | Send updated contract | Sarah (Acme) | EOD Fri | High |
| 2 | Send revised project plan | You | Wed | High |

### Open Questions
- [Unresolved question from meeting]

### Next Meeting
[Date/topic if scheduled, or "TBD"]
```  

### 仅提取行动项  

**触发命令**：`Pull action items from [会议记录或描述]`  
**适用场景**：当您仅有原始会议记录，需要提取并整理行动项时使用。  
**输出格式**：  
```markdown
## Action Items — [Meeting Name] (YYYY-MM-DD)

**Your actions:**
- [ ] [Action] — due [date]
- [ ] [Action] — due [date]

**Others' actions (to follow up on):**
- [ ] [Name]: [Action] — due [date]

**Added to open-actions.md:** ✅
```  

### 每周行动项回顾  

**触发命令**：`Meeting review` 或 `open actions` 或 `what’s overdue?`  
**功能**：扫描 `meetings/open-actions.md` 文件，标记逾期的行动项，并提醒您本周需要完成的承诺。  
**输出格式**：  
```markdown
## Open Actions Review — Week of YYYY-MM-DD

### 🔴 Overdue
- [ ] [Action] | Owner: [name] | Was due: [date] | From: [meeting]

### 🟡 Due This Week
- [ ] [Action] | Owner: [name] | Due: [date] | From: [meeting]

### ✅ Completed Since Last Review
- [x] [Action] | Closed: [date]

### 📋 On Deck (Next 2 Weeks)
- [ ] [Action] | Owner: [name] | Due: [date]

---
Total open: [N] | Overdue: [N] | Due this week: [N]
```  

### 完成行动项  

**触发命令**：`Close action [#] from [会议名称]` 或 `mark done: [行动项描述]`  
**功能**：在 `open-actions.md` 文件中标记行动项为已完成，并更新相应的会议记录。  

### 会议类型示例  

| 会议类型 | 准备深度 | 会议记录详细程度 | 行动重点 |  
|------|------------|--------------|--------------|  
| 发现/销售会议 | 深度 | 中等 | 确定下一步行动方向 |  
| 客户例会 | 中等 | 全面记录 | 记录承诺和截止日期 |  
| 战略讨论会 | 深度 | 全面记录 | 会议决策及负责人信息 |  
| 团队例会 | 简略记录 | 主要记录会议中的障碍因素 |  
| 供应商/合作伙伴会议 | 中等 | 全面记录 | 合同内容及交付物信息 |  
| 一对一会议 | 中等 | 全面记录 | 促进个人成长及明确责任分配 |  
| 董事会/投资者会议 | 深度 | 全面记录 | 会议决策及关键绩效指标 |  

---

## 文件命名规则  

会议文件的命名格式为：`YYYY-MM-DD-[会议名称].md`  
示例：  
- `2026-03-07-acme-weekly.md`  
- `2026-03-10-discovery-rivercity.md`  
- `2026-03-12-team-standup.md`  
当您输入 “file this meeting” 时，代理会自动完成文件命名。  

---

## 与其他 Agent Ledger 技能的集成  

| 技能 | 集成方式 |  
|-------|-----------------|  
| **client-relationship-manager** | 会议结束后自动更新客户关系管理系统（CRM）数据；将客户历史信息整合到会议简报中 |  
| **project-tracker** | 将会议中的行动项与项目里程碑关联；标记可能影响项目的决策 |  
| **inbox-triage** | 根据会议内容对邮件进行分类处理；根据行动项生成跟进邮件 |  
| **solopreneur-assistant** | 将会议频率和承诺事项纳入每周优先级审查 |  
| **goal-tracker** | 更新战略会议的相关目标进展；将会议决策记录在目标跟踪系统中 |  
| **decision-log** | 重要会议决策会自动被记录在决策日志中以供后续参考 |  

### 综合工作流程示例（CRM + 会议助手）  

> “为与 Riverside Design 的沟通会议准备简报。首先查看他们的 CRM 记录。”  
代理会：  
1. 从 `crm/crm-records.md` 中获取 Riverside Design 的客户信息；  
2. 查看之前的交流记录；  
3. 根据交流历史生成会议简报；  
4. 会议结束后：更新 CRM 中的交流记录；如果符合条件，提升交易阶段。  

---

## 自定义设置  

### 调整会议简报的详细程度  

在 `AGENTS.md` 文件中，您可以自定义会议简报的详细程度：  
```markdown
## Meeting Brief Depth
- Discovery/Sales calls: Full brief (context, goals, BANT, qualification signals)
- Client check-ins: Standard brief (context, goals, open items)
- Internal calls: Light brief (agenda + open actions only)
- Ad-hoc calls: Minimal (goals + open questions only)
```  

### 自动归档文件  

您可以设置文件在多少天后自动归档：  
```markdown
## Meeting Archive Rule
After 30 days, meeting files in meetings/ can be moved to meetings/archive/YYYY-MM/
Keep open-actions.md current regardless of file age.
```  

### 设置默认会议时区  

您可以指定会议的默认时区：  
```markdown
## Meeting Timezone
Default timezone for all meetings: [Your timezone]
Always include timezone when noting scheduled follow-ups.
```  

### 设置定期会议模板  

对于每周固定的会议，您可以创建相应的模板：  
```markdown
## Recurring Meetings
- Weekly client call (Mondays, [Client Name]): standard check-in, always 30 min
- Friday retrospective (Fridays, internal): wins/blockers/next week priorities
```  

---

## 常见问题及解决方法  

| 问题 | 可能原因 | 解决方法 |  
|---------|--------------|-----|  
| 会议简报过于简单 | 提供的信息不足 | 请包含参会人员姓名、会议历史及当前项目进度 |  
| 未提取到行动项 | 会议记录不够正式 | 请在记录完成后单独执行 “提取行动项” 命令 |  
| `open-actions.md` 文件过于混乱 | 有些行动项未被标记为已完成 | 每周执行一次 “会议回顾” 功能，并明确标记已完成的行动项 |  
| 代理无法获取 CRM 数据 | 未正确配置技能之间的关联 | 请在 `AGENTS.md` 中明确指示 “在准备会议简报前查看 CRM 数据” |  
| 会议文件格式错误 | 使用了默认的简报模板 | 请指定会议类型（如 “发现会议简报” 或 “一对一会议准备”） |  

---

## 隐私说明  

所有会议记录和行动项均 **仅存储在您的工作空间内**，不会被共享或传输到外部。会议记录可能包含敏感的商业信息，请妥善保管 `meetings/` 文件夹。  
代理 **绝不会** 自动向任何人发送会议记录或行动项。所有对外发送的沟通内容（如跟进邮件或 Slack 消息）都需要您的明确指令。  

*“会议助手” 是由 [The Agent Ledger](https://theagentledger.com) 提供的免费技能，该平台专注于开发实用的 AI 系统。*  
*欢迎访问 [theagentledger.com](https://theagentledger.com) 获取更多技能、使用指南及高级实施方案。*  
*许可协议：[CC-BY-NC-4.0](https://creativecommons.org/licenses/by-nc/4.0/)*  

> **免责声明**：本技能由 AI 生成，仅用于提供信息和建议用途，不构成专业、财务或法律建议。使用前请仔细核对所有生成的文件。The Agent Ledger 对使用结果概不负责。使用本技能需自行承担风险。*