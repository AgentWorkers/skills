---
name: Meetings
description: 构建一个个人会议系统，用于记录会议内容、准备会议议程，并确保不会错过任何后续跟进事项。
metadata: {"clawdbot":{"emoji":"🤝","os":["linux","darwin","win32"]}}
---

## 核心功能  
- 用户分享会议记录或音频时，系统会提取关键信息和待办事项。  
- 如果用户有即将召开的会议，系统会协助其准备相关资料。  
- 系统会主动提醒用户关于会议及待处理的后续事项。  
- 系统会自动创建一个名为 `~/meetings/` 的工作文件夹来存储会议相关文件。  

## 文件结构  
```
~/meetings/
├── upcoming/
│   └── 2024-02-15-client-review.md
├── past/
│   └── 2024/
├── recurring/
│   └── weekly-standup.md
├── people/
│   └── sarah-chen.md
└── follow-ups.md
```  

## 会议结束后  
用户粘贴会议记录或描述会议内容时：  
```markdown
# 2024-02-11-product-sync.md
## Meeting
Product Sync with Engineering

## Date
February 11, 2024, 2:00 PM

## Attendees
Sarah, Mike, Lisa

## Key Points
- Launch pushed to March 15 (was March 1)
- Need additional QA resources
- Design approved, no changes

## Decisions Made
- Hire contractor for QA
- Keep current feature scope

## Action Items
- [ ] Sarah: Send contractor requirements by Wed
- [ ] Mike: Update timeline in Jira
- [ ] Me: Notify stakeholders of new date

## Open Questions
- Budget approval for contractor?

## Next Meeting
Feb 18, same time
```  

## 快速记录  
无论是通过语音还是简短的文字记录：  
“刚刚完成了产品同步工作。发布计划推迟到3月15日。Sarah负责与外包测试人员对接。我需要通知相关利益方。”  
系统会自动将这些信息整理成结构化的格式，提取待办事项，并标记需要跟进的事项。  

## 会议前准备  
在会议安排之前，系统会提醒用户以下内容：  
```markdown
# Prep: Client Review (Tomorrow 10am)
## Context
- Last met: Jan 15
- Project: Website redesign
- Status: Phase 2, 60% complete

## From Last Meeting
- They wanted mobile mockups — did we deliver?
- Budget concern raised — was it resolved?

## Open Action Items
- [ ] Send revised timeline (was due last week)

## Their Recent Activity
- Sarah emailed about invoice Tuesday

## Suggested Agenda
1. Phase 2 progress update
2. Mobile mockups review
3. Timeline discussion
4. Budget clarification
```  

## 待办事项跟踪  
```markdown
# follow-ups.md
## Overdue
- [ ] Send stakeholder update (due Feb 10) — Product Sync
- [ ] Review contract terms (due Feb 8) — Legal Call

## Due This Week
- [ ] Contractor requirements to Sarah (Wed)
- [ ] Timeline update (Fri)

## Waiting On Others
- Mike: Jira update
- Lisa: Design assets
```  

## 定期会议  
```markdown
# recurring/weekly-standup.md
## Meeting
Weekly Team Standup

## Schedule
Mondays 9:00 AM

## Usual Attendees
Full product team

## Running Notes
### Feb 11
- Sprint on track
- John out next week

### Feb 4
- Delayed by design review
- Added Lisa to project
```  

## 人员信息  
```markdown
# people/sarah-chen.md
## Role
VP Product, Acme Corp

## Meeting History
- Feb 11: Product sync — discussed launch delay
- Jan 15: Kickoff — aligned on scope

## Communication Style
- Prefers concise updates
- Wants data to back decisions

## Notes
- Reports to CEO directly
- Budget authority up to $50k
```  

## 主动提醒  
- “2小时后与Sarah有会议——请准备好相关资料。”  
- “上周有3项待办事项已经逾期。”  
- “你答应过Mike今天会给他一个更新。”  
- “30分钟后有定期会议。”  

## 需要提取的信息  
- 会议中做出的决策  
- 待办事项（涉及的人员、内容、截止时间）  
- 未解决的问题  
- 重要的讨论要点  
- 下次会议的日期  

## 需要展示的信息  
- 会议前的准备资料  
- 过期和即将进行的待办事项  
- 与会人员的背景信息  
- 你之前所做的承诺  

## 持续改进  
- 初始阶段：会议结束后立即记录会议内容。  
- 跟踪待办事项和后续事项。  
- 为重要会议添加准备资料。  
- 逐步完善关于与会人员的背景信息。  

## 不应做的事情  
- 不要让待办事项被遗忘。  
- 在没有了解会议背景的情况下参加会议。  
- 忘记自己所做的承诺。  
- 忽略定期会议的安排。