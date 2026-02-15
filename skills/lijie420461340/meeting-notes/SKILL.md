---
name: meeting-notes
description: 将原始的会议记录、文字记录或录音文件转换为结构化、可操作的摘要。
version: 1.0.0
author: Claude Office Skills Contributors
license: MIT
tags: [productivity, meetings, documentation]
---

# 会议记录

## 概述

该工具能够将原始的会议记录、会议记录文本或音频摘要转化为结构清晰、条理分明的文档，其中包含待办事项、决策结果以及关键要点。

**使用场景：**
- 将杂乱的手写笔记整理成简洁的摘要
- 处理会议记录文本
- 提取待办事项及其负责人
- 创建会议纪要以供分发
- 将长时间的讨论内容总结为关键要点

## 使用方法

1. 粘贴您的会议记录、会议记录文本或描述内容
2. 告诉我会议的类型（如站立会议、项目评审、客户电话会议等）
3. 指定所需的格式或模板
4. 我会为您生成包含待办事项的结构化文档

**示例提示：**
- “整理这些会议记录并提取待办事项”
- “根据这份会议记录文本创建正式的会议纪要”
- “总结我们项目评审中的关键决策”
- “将这次头脑风暴会议的内容整理成结构化的文档”

## 会议记录模板

### 标准会议总结

```markdown
# Meeting Summary

**Meeting:** [Title]
**Date:** [Date]
**Attendees:** [Names]
**Duration:** [Time]

## Purpose
[One sentence describing meeting objective]

## Key Discussion Points
1. [Topic 1]
   - [Key point]
   - [Key point]

2. [Topic 2]
   - [Key point]
   - [Key point]

## Decisions Made
- [ ] [Decision 1]
- [ ] [Decision 2]

## Action Items
| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [Task] | [Name] | [Date] | Pending |

## Next Steps
- [Next meeting/milestone]

## Notes
[Any additional context or parking lot items]
```

### 快速站立会议记录

```markdown
# Daily Standup - [Date]

## [Team Member 1]
**Yesterday:** [Completed tasks]
**Today:** [Planned tasks]
**Blockers:** [Issues, if any]

## [Team Member 2]
...

## Team Blockers
- [Blocker requiring escalation]

## Announcements
- [Team-wide updates]
```

### 客户会议记录

```markdown
# Client Meeting Notes

**Client:** [Company Name]
**Date:** [Date]
**Our Team:** [Names]
**Client Team:** [Names]

## Meeting Objective
[Why we met]

## Client Feedback/Requests
1. [Feedback point]
2. [Request]

## Our Commitments
- [What we promised to deliver]
- [Timeline]

## Client Commitments
- [What they will provide]
- [Timeline]

## Follow-up Required
| Item | Owner | Due |
|------|-------|-----|
| [Task] | [Name] | [Date] |

## Next Meeting
[Date/Time/Agenda preview]
```

### 项目评审记录

```markdown
# Project Review: [Project Name]

**Date:** [Date]
**Phase:** [Current phase]
**Status:** 🟢 On Track / 🟡 At Risk / 🔴 Off Track

## Progress Update
- **Completed:** [Milestones achieved]
- **In Progress:** [Current work]
- **Upcoming:** [Next milestones]

## Metrics
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| [KPI] | [Target] | [Actual] | ✅/⚠️/❌ |

## Risks & Issues
| Risk/Issue | Impact | Mitigation | Owner |
|------------|--------|------------|-------|
| [Description] | High/Med/Low | [Plan] | [Name] |

## Decisions Needed
- [Decision requiring escalation]

## Action Items
- [ ] [Task] - @[Owner] - Due: [Date]
```

## 处理指南

### 提取待办事项

寻找表示任务的短语：
- “我们需要...” / “有人应该...” / “你能...” / “你会...”
- “让我们...” / “行动：”
- 名字 + 动词（例如：“John 将负责准备...”）
- 提及任务的截止日期

### 识别决策结果

寻找以下内容：
- “我们决定...” / “决策结果是...”
- “今后，我们将...”
- “同意：” / “确认：”
- 表示共识的表述（“大家都同意...”）

### 确定负责人

- 明确指定的负责人：“Sarah 将负责...”  
- 基于角色的负责人：“设计团队将...”  
- 如果不明确，则默认为会议组织者  
- 标记未分配的待办事项以供后续处理

## 输出格式

```markdown
## Meeting Summary: [Title]

📅 **Date:** [Date]
👥 **Attendees:** [List]

### 📋 Summary
[2-3 sentence overview]

### 💡 Key Points
1. [Point 1]
2. [Point 2]
3. [Point 3]

### ✅ Decisions
- [Decision 1]
- [Decision 2]

### 📌 Action Items
| # | Action | Owner | Due | Priority |
|---|--------|-------|-----|----------|
| 1 | [Task] | [Name] | [Date] | High/Med/Low |

### 🔜 Next Steps
- [Next meeting or milestone]

### 📝 Parking Lot
- [Items to address later]
```

## 自定义选项

请告知您的需求：
- **格式：** 列表形式、表格、散文或正式的会议纪要  
- **详细程度：** 执行摘要、标准格式或详细格式  
- **关注点：** 仅包含待办事项、仅包含决策结果，或包含全部内容  
- **风格：** 随意的团队记录或正式的文档  

## 限制

- 无法参加会议或录制会议  
- 准确性取决于输入笔记的质量  
- 对于含义模糊的代词或缩写可能需要进一步澄清  
- 无法验证承诺或截止日期——在分发前请自行核实  

## 示例

### 示例：将原始笔记转换为结构化摘要

**输入：**
```
product meeting 3/15
talked about launch timeline, sarah thinks we need 2 more weeks
john mentioned the bug in checkout - high priority
decided to push launch to april 1
need to update stakeholders
maria will fix the checkout bug by friday
also discussed new feature requests from customers - will prioritize next sprint
john to send customer feedback summary
```

**输出：**

## 会议总结：产品发布评审

📅 **日期：** 2024年3月15日  
👥 **参会人员：** Sarah、John、Maria  

### 📋 总结  
审查了产品发布的时间表，由于发现了一个关键的检查问题，决定将发布日期推迟两周至4月1日。同时讨论了客户的功能需求，以便后续进行优先级排序。  

### 💡 关键要点  
1. 原定的发布时间表不够充分——还需要额外2周时间  
2. 发现了一个关键的检查问题——必须在发布前修复  
3. 收集了客户的功能需求，以便在下一个冲刺中优先处理  

### ✅ 决策结果  
- 发布日期从3月中旬推迟至 **4月1日**  
- 检查问题是 **最高优先级**  
- 客户的功能需求将在下一个冲刺计划中优先处理  

### 📌 待办事项  
| 编号 | 任务 | 负责人 | 截止日期 | 优先级 |  
|---|--------|-------|-----|----------|  
| 1 | 修复检查问题 | Maria | 3月17日（周五） | 🔴 高优先级 |  
| 2 | 向利益相关者更新新的发布日期 | [未分配] | 尽快 | 🔴 高优先级 |  
| 3 | 发送客户反馈摘要 | John | [待定] | 🟡 中等优先级 |  

### 🔜 下一步行动  
- 跟进修复问题的进度  
- 与利益相关者沟通时间表变更情况  
- 在冲刺计划中优先处理客户的需求