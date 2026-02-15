---
name: plan-my-day
description: 生成一个节能且按时间块划分的每日计划
version: 1.0.0
author: theflohart
tags: [productivity, planning, time-blocking, energy-management]
---

# 规划我的一天

根据当前的优先事项和精力状态，生成一份清晰、可执行的每小时工作计划。

## 使用方法

```
/plan-my-day [optional: YYYY-MM-DD for future date]
```

## 规划原则

1. **早晨准备**：将第一个小时用于起床后的个人仪式（如梳洗、锻炼等），而非处理任务。
2. **根据精力安排任务**：根据任务的难度和自己的精力水平来安排它们。
3. **时间块划分**：为每项工作分配特定的时间段。
4. **确定三大重点**：明确当天最重要的三项任务。

## 精力状态（可根据个人节奏调整）

- **高效时段**：早晨（适合处理难度较大的任务）
- **次高峰时段**：下午（适合专注的工作和会议）
- **休息时段**：用于锻炼、用餐和休息
- **放松时段**：晚上（适合处理较轻松的任务或进行规划）

## 规划步骤

1. **收集信息**：
   - 查看现有的每日笔记
   - 回顾当前的优先事项
   - 确认已确定的日程安排（如会议、电话等）
   - 查看昨天的待办事项

2. **确定三大优先事项**：
   - 今天必须完成的任务有哪些？
   - 哪项任务对实现目标影响最大？
   - 哪项任务有截止日期？

3. **制定时间安排**：
   - 将优先事项安排在精力最充沛的时段
   - 安排好固定的日程安排
   - 在不同任务之间留出缓冲时间
   - 确保安排休息和恢复时间

4. **考虑限制因素**：
   - 遵守已有的预约
   保护个人时间
   确保安排用餐时间
   避免过度安排任务

## 输出格式

```markdown
# Daily Plan - [Day], [Month] [Date], [Year]

## Today's Mission

**Primary Goal:** [One-sentence goal for the day]

**Top 3 Priorities:**
1. [Priority 1 with specific outcome]
2. [Priority 2 with specific outcome]
3. [Priority 3 with specific outcome]

---

## Time-Blocked Schedule

### [TIME] - [TIME]: [Block Name]
**Focus:** [Primary focus for this block]

- [ ] [Specific task 1]
- [ ] [Specific task 2]
- [ ] [Specific task 3]

**Target:** [Measurable outcome]

---

[Continue for each time block...]

---

## Success Criteria

### Must-Have (Non-Negotiable)
- [ ] [Critical task 1]
- [ ] [Critical task 2]
- [ ] [Critical task 3]

### Should-Have (Important)
- [ ] [Important task 1]
- [ ] [Important task 2]

### Nice-to-Have (Bonus)
- [ ] [Bonus task 1]

---

## Evening Check-In

- [ ] Priority 1 done? **YES / NO**
- [ ] Priority 2 done? **YES / NO**
- [ ] Priority 3 done? **YES / NO**

**What went well:**

**What got stuck:**

**Tomorrow's priority adjustment:**
```

## 决策框架

在开始任何事情之前，请先问自己：
1. 这项任务是否属于我的三大优先事项之一？
2. 完成这项任务能否帮助我实现当天的目标？
3. 这项任务能否推迟到明天再做？

**如果三个问题的答案都是“否”，那就不要做这件事。**

## 提示：

- 不要安排满100%的时间——预留20%的缓冲时间。
- 将最困难的任务安排在精力最充沛的时段。
- 将相似的任务组合在一起处理（批量处理）。
- 安排好休息时间，不要只是期待休息。
- 如有需要，可在中午时调整计划。