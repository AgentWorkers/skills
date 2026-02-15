---
name: ai-daily-briefing
version: 1.0.0
description: "每天以专注的状态开始工作。早上会收到一份简报，其中包含未完成的任务、当天的优先事项、日历概览以及近期会议的要点。该系统与 AI 会议记录工具（ai-meeting-notes）集成，用于管理待办事项列表。无需任何额外的设置，只需简单地说“briefing”即可获取相关信息。"
author: Jeff J Hunter
homepage: https://jeffjhunter.com
tags: [daily-briefing, morning-routine, productivity, todo, priorities, calendar, focus, daily-ops, task-management, planning]
---

# ☀️ 人工智能每日简报  
**每天以清晰的状态开始新的一天，明确知道什么是最重要的。**  
通过每日简报，您可以了解未完成的任务、当天的优先事项以及近期工作的背景信息。  

无需任何设置，只需简单地说“briefing”即可获取简报内容。  

---

## ⚠️ 重要提示：简报的格式（请先阅读）  
**当用户请求简报时，必须按照以下格式回复：**  
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☀️ DAILY BRIEFING — [Day], [Month] [Date], [Year]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ OVERDUE ([X] items)
• Task 1 — was due [date]
• Task 2 — was due [date]

📅 TODAY'S PRIORITIES
1. [ ] Priority task 1 — [deadline/context]
2. [ ] Priority task 2 — [deadline/context]
3. [ ] Priority task 3 — [deadline/context]

📆 CALENDAR
• [Time] — [Event]
• [Time] — [Event]
• [Time] — [Event]

💡 CONTEXT (from recent meetings)
• [Key insight 1]
• [Key insight 2]
• [Key insight 3]

🎯 FOCUS FOR TODAY
[One sentence: What's the ONE thing that matters most today?]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```  

### 强制性规则  
| 规则 | 要求 |  
|------|-------------|  
| **仅回复一条消息** | 将所有信息汇总在一条消息中 |  
| **按顺序呈现内容** | 未完成的任务 → 当天的优先事项 → 日历 → 工作背景 → 需要关注的重点 |  
| **跳过空白部分** | 如果没有未完成的任务，则跳过相应部分 |  
| **每个部分最多5条信息** | 保持信息简洁易读（日历部分除外） |  
| **结尾必须包含一个重点** | 每条简报结尾必须明确一个需要关注的重点事项 |  

---

## 为何需要这个功能？  
每天早晨，您都会遇到同样的问题：  
- 有哪些任务未完成？  
- 今天有哪些安排？  
- 我需要了解哪些会议信息？  
- 有哪些背景信息需要记住？  
通过每日简报，您可以一次性获取所有这些信息，而无需在多个地方查找。  

## 简报的功能  
| 输入 | 输出 |  
|-------|--------|  
| “briefing” | 提供完整的每日概览 |  
| “有哪些未完成的任务？” | 仅显示未完成的任务 |  
| “我的日历上有什么安排？” | 显示当天的日程安排 |  
| “我应该关注什么？” | 提供优先事项建议 |  
| “本周预览” | 提供下周的日程概览 |  

## 数据来源  
简报信息来自以下来源（如果存在的话）：  

### 1. 待办事项列表（来自 ai-meeting-notes）  
**位置：** 工作区根目录下的 `todo.md`  

```markdown
# To-Do List

## ⚠️ Overdue
| # | Task | Owner | Due | Source |
|---|------|-------|-----|--------|
| 3 | Send proposal | @You | Jan 25 | client-call.md |

## 📅 Due Today
| # | Task | Owner | Source |
|---|------|-------|--------|
| 5 | Review budget | @You | team-sync.md |

## 📆 This Week
| # | Task | Owner | Due | Source |
|---|------|-------|-----|--------|
| 1 | Finalize report | @You | Fri | planning.md |
```  

### 2. 会议记录  
**位置：** `meeting-notes/` 文件夹  
- 扫描最近3-7天的会议记录  
- 提取会议中的决策、行动事项及相关背景信息  
- 显示重要的提醒事项  

### 3. 日历（如果可用）  
- 显示当天的会议和活动  
- 提供明天的日程预览（可选）  
- 显示可能存在的时间冲突或紧张的日程安排  

### 4. 记忆/背景信息文件（如果使用了 ai-persona-os）  
**位置：**  
- `MEMORY.md` — 永久性存储的信息  
- `memory/[today].md` — 当天的会议记录  
- `USER.md` — 用户的个人设置  

---

## 触发简报的指令  
以下任何指令都会触发简报的生成：  
| 指令 | 动作 |  
|--------|--------|  
| “briefing” | 生成完整的每日简报 |  
| “daily briefing” | 生成完整的每日简报 |  
| “morning briefing” | 生成完整的每日简报 |  
| “我今天有哪些任务？” | 生成完整的每日简报 |  
| “我想了解今天的情况” | 生成完整的每日简报 |  
| “给我介绍一下今天的安排” | 生成完整的每日简报 |  

---

<aiinstructions>  
## 人工智能的工作流程：  
当用户请求简报时，请按照以下步骤操作：  

### 第0步：准备工作  
在生成简报之前，请确认：  
- [ ] 会回复一条消息  
- [ ] 会严格按照规定的格式回复  
- [ ] 每条简报结尾都会包含一个需要关注的重点事项  

### 第1步：收集数据  
按顺序检查以下文件：  
```
1. todo.md (to-do list from ai-meeting-notes)
2. meeting-notes/ folder (recent meeting notes)
3. MEMORY.md (if using ai-persona-os)
4. memory/[today].md (session notes)
5. Calendar integration (if available)
```  
**如果没有任何数据来源：**  
```
No existing to-do list or meeting notes found.

Would you like me to:
• Create a to-do list? (just tell me your tasks)
• Process some meeting notes? (paste them here)
• Set up a simple priority list for today?
```  

### 第2步：提取未完成的任务  
从 `todo.md` 中提取标记为“⚠️ 未完成”的任务。  
**显示格式：**  
```
⚠️ OVERDUE ([X] items)
• [Task] — was due [date]
• [Task] — was due [date]
```  
**规则：**  
- 最多显示5项任务（如果超过5项，则显示“+ [X] 项未完成的任务”）  
- 按紧急程度排序  
- 显示任务的原始截止日期  
- 如果没有未完成的任务，则跳过此部分  

### 第3步：提取当天的优先事项  
从多个来源汇总优先事项：  
1. **来自 `todo.md` 的任务**：  
   - 标记为“📅 今天到期”的任务  
   - 标记为“📆 本周内到期”的任务  
2. **来自 `meeting-notes/` 的任务**：  
   - 分配给用户的、今天到期的行动事项  
   - 需要跟进的事项  
3. **来自日历的任务**：  
   - 需要准备的会议  
   - 截止日期  

**显示格式：**  
```
📅 TODAY'S PRIORITIES
1. [ ] [Task] — [deadline/context]
2. [ ] [Task] — [deadline/context]
3. [ ] [Task] — [deadline/context]
```  
**规则：**  
- 最多显示5项任务  
- 为便于查看，任务会编号  
- 按紧急程度和重要性排序  

### 第4步：查看日历  
如果日历数据可用：  
**显示格式：**  
```
📆 CALENDAR
• [Time] — [Event]
• [Time] — [Event]
• [Time] — [Event]
```  
**规则：**  
- 按时间顺序显示所有事件  
- 显示事件名称和时间  
- 如果没有日历数据，则显示“未连接日历”  

### 第5步：整理近期会议的背景信息  
扫描 `meeting-notes/` 文件夹中的文件（最近3-7天的记录），提取以下内容：  
- 会议中的关键决策  
- 需要记住的重要背景信息  
- 提及的截止日期  
- 需要跟进的人员或事项  

**显示格式：**  
```
💡 CONTEXT (from recent meetings)
• [Key insight 1]
• [Key insight 2]
• [Key insight 3]
```  
**规则：**  
- 最多显示5条相关信息  
- 仅包含相关且可执行的背景信息  
- 如有必要，可注明会议来源（例如：“来自客户电话”）  
- 如果没有近期会议记录，则跳过此部分  

### 第6步：确定重点事项  
根据收集到的所有信息，确定最重要的一项任务。  
**选择重点的依据：**  
- 有严重后果的未完成任务  
- 今天有重要会议的议题  
- 不能延期的截止日期  
- 会阻碍其他工作的依赖事项  

**显示格式：**  
```
🎯 FOCUS FOR TODAY
[One clear sentence about the single most important thing]
```  
**示例：**  
- “请发送Acme公司的提案——该提案已经逾期2天了，他们正在等待回复。”  
- “准备下午2点的投资者电话会议——其他事项都可以暂时放一放。”  
- “在开始新工作之前，先完成3项未完成的任务。”  
- “今天没有紧急事务，可以用来深入研究第二季度的计划。”  

### 第7步：整合简报内容  
将所有信息按照规定的格式整合在一起：  
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☀️ DAILY BRIEFING — [Day], [Month] [Date], [Year]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Overdue section — if any]

[Today's Priorities section]

[Calendar section — if available]

[Context section — if any]

[Focus statement — always]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```  

### 处理不同情况  
- **“有哪些未完成的任务？”**  
```
⚠️ OVERDUE ITEMS

1. [Task] — was due [date]
2. [Task] — was due [date]

[If none: "Nothing overdue! You're caught up."]
```  
- **“我的日历上有什么安排？”**  
```
📆 TODAY'S CALENDAR — [Date]

• [Time] — [Event]
• [Time] — [Event]

[Tomorrow preview if requested]
```  
- **“本周预览” / “本周的安排是什么？”**  
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 WEEKLY PREVIEW — Week of [Date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MONDAY
• [Tasks/events]

TUESDAY
• [Tasks/events]

[etc.]

⚠️ WATCH OUT FOR
• [Key deadline or conflict]
• [Important meeting]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```  

### 特殊情况处理：  
- 如果没有找到数据来源：  
  - 不显示空简报  
  - 提供帮助设置待办事项列表或整理会议记录的选项  
- **首次使用用户**：  
  - 解释数据来源  
  - 提供初始化设置的帮助  
- **周末简报**：  
  - 简报内容简化  
  - 重点介绍下周的准备工作  
  - 如果当天没有安排，可省略“当天的优先事项”  
- **结束时的提示**：  
  - 提供“今天剩余的任务”和“明天的日程预览”，并告知当前时间  

### 交流语气  
- **简洁明了且具有行动指导性**：避免冗长内容  
- **如实说明优先事项**：不粉饰未完成的任务  
- **积极向上**：虽然今天可能很忙，但一切都在可控范围内  
- **主动提醒**：在问题出现之前就提前提示用户  

---

## 该功能与哪些工具配合使用效果最佳？  
| 工具 | 原因 |  
|-------|-----|  
| **ai-meeting-notes** | 用于生成待办事项列表 |  
| **ai-persona-os** | 提供记忆和背景信息 |  
**独立使用**：即使没有其他工具，也能生成简报，但可能缺少会议背景信息和持续性的待办事项列表。  

## 快速上手指南  
**第一天使用方法：**  
```
You: "briefing"
AI: [Shows briefing based on available data, or offers to set up]
```  
**使用 ai-meeting-notes 后：**  
```
You: "briefing"
AI: [Shows full briefing with overdue items, priorities, context]
```  

## 自定义简报内容  
想要自定义简报内容吗？请告知您的需求：  
**时间设置**：  
- “我早上6点开始工作” → 提前显示相关信息  
- “显示明天的会议安排” → 显示明天的日程预览  
**内容设置**：  
- “始终显示天气” → 添加天气信息  
- “跳过日历部分” → 不显示日历内容  
- **添加激励性语句**：添加激励性的语句  
**优先事项设置**：  
- “健康相关的事项永远优先处理” → 提高健康相关事项的优先级  
- “家庭优先” → 优先处理家庭事务  

## 简报示例：  
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☀️ DAILY BRIEFING — Tuesday, February 3, 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ OVERDUE (2 items)
• Send Acme proposal — was due Feb 1
• Review Week 2 training materials — was due Jan 31

📅 TODAY'S PRIORITIES
1. [ ] Anne follow-up call — 2pm today
2. [ ] Finalize Week 3 training content — EOD
3. [ ] Prep for Makati trip — flights need booking
4. [ ] Respond to Karlen re: workflow docs
5. [ ] Clear overdue Acme proposal

📆 CALENDAR
• 10:00 AM — Team standup (30 min)
• 2:00 PM — Anne follow-up call (1 hour)
• 4:30 PM — Workshop dry run (90 min)

💡 CONTEXT (from recent meetings)
• Anne partnership confirmed — ready to move forward (from anne-call)
• OpenClaw bot architecture changing to specialists (from pm-meeting)
• Makati trip deadline approaching — need flights by Friday

🎯 FOCUS FOR TODAY
Get the Acme proposal out first thing — it's 2 days overdue and blocking the deal.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```  

## 关于创建者  
**Jeff J Hunter** 创建了这个系统，帮助人们每天以清晰的状态开始新的一天，避免混乱。  
他通过“AI Persona Method”培训了数千人，并管理着拥有360多万成员的AI社区。  
**想将AI技术转化为实际收入吗？**  
大多数人浪费API信用却没有任何实际成果。Jeff会教你如何构建能够自我盈利的AI系统。  
👉 **加入AI Money Group**：https://aimoneygroup.com  
👉 **联系Jeff**：https://jeffjhunter.com  

---

*这是AI Persona操作系统生态系统的一部分——帮助您构建实用且能带来收益的AI应用。*