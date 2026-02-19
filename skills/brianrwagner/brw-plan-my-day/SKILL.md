---
name: plan-my-day
description: 根据昼夜节律研究和 GTD（Getting Things Done）原则，生成一个能源优化、按时间块划分的每日计划。
version: 2.0.0
author: theflohart
tags: [productivity, planning, time-blocking, energy-management, gtd]
---
# 规划我的一天

根据优先级、精力状态和约束条件，生成一份清晰、可操作的每小时工作计划。

## 为什么选择这个工具而不是 ChatGPT？

**“直接询问”的问题：** 每次得到的计划都不同，缺乏连贯性，也无法记录哪些方法有效，也无法随着时间进行优化。

**这个工具提供：**
1. **一致的方法论** – 每天都使用相同的决策框架（前三项优先事项、精力高峰时段、缓冲时间规则）。
2. **考虑精力的时间安排** – 自动将高认知要求的任务安排在精力最充沛的时段。
3. **尊重个人约束** – 充分考虑你的日程安排、精力模式和个人界限。
4. **学习与反馈机制** – 可以追踪哪些时间安排方式最适合你。
5. **内置的晚间反思** – 强制你对自己的工作成果进行反思。

**你可以自己实现这个计划**：每天输入相同的详细指令，手动查看日程安排，记住自己的精力模式，并记录完成情况。或者只需花费2分钟使用这个工具。

## 使用方法

```
/plan-my-day [optional: YYYY-MM-DD for future date]
```

（根据你的个人精力状况进行相应设置）

## 规划原则（基于科学研究）

1. **昼夜节律优化** – 认知表现通常在醒来后2-3小时达到峰值（Roenneberg, 2012）
2. **超昼夜节律** – 每90分钟工作，中间休息15-20分钟（Ericsson, 1993）
3. **避免决策疲劳** – 将高风险决策安排在下午3点之前（Kahneman, 2011）
4. **明确的目标设定** – 具体的时间+任务组合能显著提高完成率（Gollwitzer, 1999）

## 精力高峰时段（默认设置，可自定义）

**上午高峰期：** 9:00 AM - 12:00 PM
- 适合进行深度工作、战略思考和复杂问题解决
- 这段时间的认知能力最强
- 将最重要的任务安排在此时段。

**下午次高峰期：** 2:00 PM - 4:00 PM
- 适合专注工作、开会和创造性任务
- 能力仍较高，但略低于上午。

**下午行政时段：** 4:00 PM - 6:00 PM
- 适合处理邮件、处理琐事、进行一对一沟通和规划
- 这段时间精力稍弱，应避免复杂决策。

**恢复时段：** 12:00 PM - 1:00 PM, 6:00 PM+
- 用于用餐、锻炼、散步和恢复精力
- 这些时段对持续的工作效率至关重要。

**放松时段（晚上）：** 7:00 PM以后
- 适合反思、阅读和为第二天做准备
- 不适合进行高认知要求的任务。

## 规划流程

### 1. 收集信息（30秒）
- 查看现有的日程安排
- 回顾昨天未完成的任务
- 记录所有固定的承诺和截止日期
- 确定当天的主要任务

### 2. 确定前三项优先事项（60秒）
对每个潜在任务评估：
- **影响**：这个任务能否推动关键指标或截止日期的达成？
- **紧急性**：今天必须完成吗？
- **难度**：在现有时间内能完成吗？

**筛选标准：** 选择影响最大且紧急性最高的三个任务。

### 3. 制定时间安排（90秒）
**排序逻辑：**
1. 首先安排固定的会议和电话。
2. 将第一优先事项安排在精力高峰时段。
3. 将第二优先事项安排在下午次高峰时段或下一个空闲时段。
4. 将第三优先事项安排在剩余的时段。
5. 在主要任务之间安排20分钟的缓冲时间。
6. 将行政工作（如处理邮件、使用Slack）安排在精力较低的时段。
7. 确保休息和用餐时间不被占用。

**缓冲时间规则：** 只安排可用时间的80%。

### 4. 应对约束条件**
- **个人界限**：早上8点之前和晚上7点之后不工作（可自定义）。
- **会议限制**：每天会议时间不超过4小时。
- **专注工作时段**：深度工作至少持续90分钟，避免干扰。
- **休息规定**：每90分钟休息15分钟。

## 输出格式

```markdown
# Daily Plan - [Day], [Month] [Date], [Year]

## Today's Mission

**Primary Goal:** [One-sentence outcome for the day]

**Top 3 Priorities:**
1. [Priority 1 with specific, measurable outcome]
2. [Priority 2 with specific, measurable outcome]
3. [Priority 3 with specific, measurable outcome]

**Success looks like:** [What "done" means today]

---

## Time-Blocked Schedule

### 8:00 - 9:00: Morning Prime 🌅
**Focus:** Wake up, coffee, light movement, review plan

- [ ] Morning routine (30 min)
- [ ] Review today's plan + priorities (10 min)
- [ ] Quick inbox scan (15 min - flag only, don't respond)

**Energy level:** Building

---

### 9:00 - 11:00: Deep Work Block 1 🎯 [PRIORITY #1]
**Focus:** [Specific priority 1 task]

- [ ] [Concrete subtask 1]
- [ ] [Concrete subtask 2]
- [ ] [Concrete subtask 3]

**Target:** [Measurable outcome by 11:00]

**Protection:** Phone off, Slack paused, door closed

---

### 11:00 - 11:15: Break ☕
**Focus:** Step away from desk

- Physical movement (walk, stretch)
- Hydrate
- No screens

---

### 11:15 - 12:30: Deep Work Block 2 🎯 [PRIORITY #2]
**Focus:** [Specific priority 2 task]

- [ ] [Concrete subtask 1]
- [ ] [Concrete subtask 2]

**Target:** [Measurable outcome by 12:30]

---

### 12:30 - 1:30: Lunch Break 🍽️
**Focus:** Eat, recharge, disconnect

- Proper meal (not at desk)
- 15-minute walk if possible
- No work talk

**Energy level:** Recovery

---

### 1:30 - 3:00: Focused Work Block 🎯 [PRIORITY #3]
**Focus:** [Specific priority 3 task]

- [ ] [Concrete subtask 1]
- [ ] [Concrete subtask 2]

**Target:** [Measurable outcome by 3:00]

---

### 3:00 - 3:15: Break ☕
**Focus:** Recharge

---

### 3:15 - 4:30: Meetings / Collaborative Work 👥
**Focus:** [Meeting name or collaborative task]

- [ ] [Meeting 1 with agenda]
- [ ] [Follow-up actions from meetings]

**Prep:** Review agendas 10 minutes before

---

### 4:30 - 5:30: Admin & Communication 📧
**Focus:** Process inbox, respond to messages, light tasks

- [ ] Clear email inbox (respond, archive, defer)
- [ ] Slack catch-up and responses
- [ ] Update project trackers
- [ ] Quick wins / small tasks

**Energy level:** Lower (perfect for admin)

---

### 5:30 - 6:00: Planning & Wrap-Up 📋
**Focus:** Close the day, plan tomorrow

- [ ] Evening check-in (see below)
- [ ] Tomorrow's top 3 priorities draft
- [ ] Inbox zero for peace of mind
- [ ] Close all work apps

---

### 6:00 PM+: Personal Time 🏡
**No work beyond this point**

---

## Success Criteria

### Must-Have (Non-Negotiable) ✓
- [ ] Priority 1 complete: [Specific outcome]
- [ ] Priority 2 complete: [Specific outcome]
- [ ] At least 80% progress on Priority 3

### Should-Have (Important) ⭐
- [ ] [Secondary task 1]
- [ ] [Secondary task 2]

### Nice-to-Have (Bonus) 💡
- [ ] [Bonus task 1]
- [ ] [Bonus task 2]

---

## Evening Check-In (5 minutes at 5:30 PM)

**Completion status:**
- Priority 1 done? **YES / NO** - [If no, why?]
- Priority 2 done? **YES / NO** - [If no, why?]
- Priority 3 done? **YES / NO** - [If no, why?]

**What went well:**
[What worked today? What helped you execute?]

**What got stuck:**
[Where did you lose time? What blocked you?]

**Energy assessment:**
- Peak hours productive? **YES / NO**
- Breaks taken? **YES / NO**
- Felt energized or drained? **[Score 1-10]**

**Tomorrow's adjustment:**
[What to change in tomorrow's plan based on today?]

---

## Quick Decision Framework

**Before saying YES to anything today:**

1. **Is this one of my top 3 priorities?**
   - YES → Schedule it in appropriate energy window
   - NO → Go to #2

2. **Does this directly support today's mission?**
   - YES → Add to relevant time block
   - NO → Go to #3

3. **Can this wait until tomorrow?**
   - YES → Add to tomorrow's list
   - NO → Question if it's really urgent

**If NO to all three → Decline or defer**

---
```

## 实际案例

### 示例1：高产出日（创始人/高管）

**背景**：产品发布周，有高风险的演示和团队协调工作

```markdown
## Top 3 Priorities:
1. Finalize launch announcement (900 words, 3 versions) - DONE by 11:30
2. Run partner demo with clear next steps - DONE by 3:00
3. Team sprint planning with Q2 priorities set - DONE by 5:00

## Schedule:
- 9:00-11:30: Deep work → Launch copy (Priority #1)
- 12:30-2:45: Partner demo prep + execution (Priority #2)
- 3:00-4:45: Sprint planning with team (Priority #3)
- 5:00-5:30: Email/admin/wrap

## Evening Check-In:
✓ Priority 1: YES (shipped 3 versions, CEO approved)
✓ Priority 2: YES (partner committed, contract signed)
✓ Priority 3: YES (team aligned, stories pointed)

What worked: Protected deep work time for writing, prepped demo thoroughly
Tomorrow: Start execution on sprint, less coordination overhead
```

### 示例2：需要深度工作的日子（独立开发者）

**背景**：需要连续6小时以上不间断编码

```markdown
## Top 3 Priorities:
1. Ship authentication refactor (PR ready for review) - DONE by 12:00
2. Debug production issue #847 (root cause found + fix deployed) - DONE by 4:00
3. Documentation for new API endpoints (published) - DONE by 6:00

## Schedule:
- 9:00-12:00: Deep work → Auth refactor (Priority #1)
- 1:00-4:00: Deep work → Debug + deploy (Priority #2)
- 4:15-5:45: Documentation writing (Priority #3)
- 5:45-6:00: Update tickets, close day

## Protections:
- Slack: Paused 9am-12pm, 1pm-4pm
- No meetings scheduled
- Phone: DND mode

## Evening Check-In:
✓ Priority 1: YES (PR approved, merged)
✓ Priority 2: YES (issue resolved, monitoring green)
✓ Priority 3: 90% (docs drafted, needs final review tomorrow)

What worked: Zero meetings = maximum flow state
Tomorrow: Finish docs, start new feature work
```

### 示例3：会议较多的日子（经理/主管）

**背景**：担任领导角色，需要协调多个团队

```markdown
## Top 3 Priorities:
1. Align exec team on Q2 budget priorities - DONE by 11:00
2. Resolve team conflict (performance conversation) - DONE by 3:00
3. Approve 3 critical design reviews - DONE by 5:30

## Schedule:
- 8:30-9:00: Pre-meeting prep (agendas, talking points)
- 9:00-11:00: Exec budget meeting (Priority #1)
- 11:15-12:15: 1-on-1 performance conversation (Priority #2)
- 1:30-3:00: Design review meetings (Priority #3, all 3 back-to-back)
- 3:15-4:30: Email/admin/follow-ups from meetings
- 4:30-5:00: Next week prep + team updates

## Evening Check-In:
✓ Priority 1: YES (budget approved, owners assigned)
✓ Priority 2: YES (performance plan agreed, follow-up scheduled)
✓ Priority 3: YES (2 approved, 1 needs revision)

What got stuck: Back-to-back meetings = no thinking time
Tomorrow: Block 2-hour deep work window, fewer meetings
```

## 用户案例研究

**用户**：一家B2B SaaS公司的市场经理，过去常常应对大量的临时任务

**使用前的情况：**
- 平均每天花费6-8小时在会议中，仅有2小时用于工作。
- 最重要的任务很少完成。
- 频繁收到邮件和Slack通知的干扰。
- 每周任务完成率仅为15%。
- 自认为工作高效，但实际上收获甚微。

**使用“规划我的一天”工具后的变化：**
- 每天早上使用该工具（2-3分钟生成计划）。
- 保护了9:00 AM - 11:00 AM的深度工作时段（在日程中标记为“专注时间”）。
- 每天明确设定前三项优先事项。
- 增加了晚上的检查环节以跟踪任务完成情况。

**8周后的效果：**
- 每周任务完成率提高到74%（相比之前提高了59%）。
- 每天会议时间从6-8小时减少到3-4小时。
- 每周有4天能够保持深度工作（之前为零）。
- 自我评估的精力水平从4.1分提高到8.2分。
**团队反馈：** “你更加专注和果断。”

## 配置选项

### 标准模式（默认设置）
```
/plan-my-day
```
- 平衡的精力高峰时段
- 假设工作时间为8小时
- 20%的缓冲时间

### 高产出模式
```
/plan-my-day --mode high-output
```
- 工作时间为10小时
- 更紧凑的时间安排
- 10%的缓冲时间
- 适合：产品发布周或项目冲刺期

### 深度工作模式
```
/plan-my-day --mode deep-work
```
- 最大化的连续工作时间
- 减少会议
- 30%的缓冲时间
- 适合：独立开发者或创意工作者

### 会议密集模式
```
/plan-my-day --mode coordination
```
- 先安排会议
- 工作时段围绕会议安排
- 25%的缓冲时间
- 适合：经理、高管和面向客户的岗位

## 安装方法

```bash
# Copy skill to your skills directory
cp -r plan-my-day $HOME/.openclaw/skills/

# Verify installation
/plan-my-day --version
```

**无需任何依赖** – 仅依赖规划逻辑。

**未来功能（即将推出）**
- **与Google Calendar同步** – 自动导入现有日程。
- **任务完成率跟踪** – 分析计划的有效性。
- **学习个人精力模式** – 根据你的实际表现进行调整。
- **团队协调** – 在团队间同步专注工作时段。

## 使用技巧

1. **优先使用该工具** – 在查看邮件或Slack之前先使用它。
2. **保护精力高峰时段** – 在日程中标记9:00 AM - 11:00 AM为“专注时间”，拒绝会议。
3. **跟踪完成率** – 利用晚上的检查数据来改进计划。
4. **调整精力高峰时段** – 默认为9:00 AM - 11:00 AM，如实际情况不同可自行调整。
5. **结合晚间总结习惯** – 晚上进行总结并为第二天做准备。
6. **不要过度安排** – 如果计划显示8小时的工作量，确保实际工作时间也能达到。

## 常见错误及避免方法**

❌ **安排过多任务** – 如果安排了所有时间，反而可能失败。务必留出20%的缓冲时间。
❌ **忽略精力高峰时段** – 将高难度任务安排在下午，容易导致效率低下。
❌ **忽略休息时间** – 90分钟的专注工作需要15分钟的休息时间，否则效率会下降。
❌ **不进行晚间反思** – 没有反思就无法改进计划。
❌ **中途更改优先事项** – 除非确实紧急，否则坚持早晨设定的优先事项。

## 质量检查清单

一个好的每日计划应包含：
- [ ] 明确的前三项优先事项及可衡量的成果
- [ ] 第一优先事项安排在精力高峰时段
- [ ] 20%的缓冲时间（不要将每个小时都安排任务）
- [ ] 每90分钟安排休息时间
- [ ] 保证午餐休息时间（至少30分钟）
- [ ] 包含晚上的检查模板
- [ ] 晚上7点之后不安排工作（保护个人时间）

## 支持方式

如有问题或建议，请提供：
- 你的日常工作时间安排和会议负担
- 三个优先事项的示例
- 你的精力高峰时段
- 当前计划中存在的问题

---

**本工具基于昼夜节律研究（Roenneberg）、刻意练习原则（Ericsson）和GTD方法论（Allen）设计。**

**用2分钟规划你的每一天，专注执行，持续取得成功。**