---
name: goal-tracker
version: "1.0.0"
description: 面向个体创业者的OKR（目标与关键成果）式目标跟踪系统：包括季度目标设定、每周进度检查、进度评分机制，以及一个人工智能辅助工具，该工具能在问题恶化为失败之前及时发出预警。
tags: [goals, okr, accountability, quarterly-review, weekly-checkin, progress-tracking, solopreneur, habits, milestones, focus]
platforms: [openclaw, cursor, windsurf, generic]
category: productivity
author: The Agent Ledger
license: CC-BY-NC-4.0
url: https://github.com/theagentledger/agent-skills
---
# 目标追踪器

设定那些不会被遗忘的目标，并让一个智能助手在您偏离目标时提醒您。

**作者：The Agent Ledger** — [theagentledger.com](https://theagentledger.com)

---

## 问题所在

大多数目标管理工具的问题都出在同一个地方：您在一月份设定目标，十二月份进行回顾，却发现在二月份自己已经偏离了目标，却浑然不知。解决办法不是使用更完善的模板，而是一个每周都会检查目标并在问题恶化之前发出警报的智能助手。

这个工具能让您的助手成为您的责任伙伴——一种基于数据、坦诚相待的责任监督方式。

---

## 设置步骤

### 第一步：创建目标目录

```bash
mkdir -p goals/
```

### 第二步：创建季度目标文件

创建 `goals/GOALS.md` 文件：

```markdown
# Goals

**Current Quarter:** Q[N] [YEAR]
**Quarter Dates:** [Start] → [End]
**Last Updated:** [date]

---

## 🎯 This Quarter's Goals

### Goal 1: [Name]

**Why it matters:** [One sentence — the real reason, not the polished reason]
**Success looks like:** [Specific, observable outcome]
**Deadline:** [date or end of quarter]
**Status:** 🟢 On Track | 🟡 At Risk | 🔴 Off Track | ✅ Done | ⏸ Paused

**Key Results:**
- [ ] KR1: [measurable outcome] — current: [X] / target: [Y]
- [ ] KR2: [measurable outcome] — current: [X] / target: [Y]
- [ ] KR3: [measurable outcome] — current: [X] / target: [Y]

**Weekly Progress:**
| Week | Progress | Blocker | Score |
|------|----------|---------|-------|
| Wk1  |          |         |       |

---

### Goal 2: [Name]
<!-- Repeat structure above -->

---

## 📋 Goal Backlog

Goals you want to pursue — not this quarter, but tracked so they don't get lost.

| Goal | Why | Estimated Quarter |
|------|-----|-------------------|
|      |     |                   |

---

## ✅ Completed Goals

| Goal | Quarter | Outcome |
|------|---------|---------|
|      |         |         |
```

### 第三步：向助手说明您的目标

只需用自然语言告诉助手您的目标：

> “我希望在三月末实现每月5000美元的收入。我的关键成果是：在3月10日前发布产品，获得50位付费客户，并撰写8期新闻通讯。”

助手会按照上述格式将这些目标整理到 `goals/GOALS.md` 文件中。

---

## 每周检查

助手每周（或根据预设触发条件）会进行一次结构化的检查：

### 触发条件

- “每周目标检查”
- “我的目标进展如何？”
- “目标更新” + 进展情况说明
- 通过心跳信号或cron任务自动触发（详见高级设置）

### 检查流程

助手会：
1. **读取 `goals/GOALS.md` 文件** — 获取当前季度的目标和关键成果（KRs）
2. **提出3个针对性问题**：
   - 本周在每个目标上取得了哪些进展？
   - 是否出现了新的阻碍因素或假设发生了变化？
   - 是否有目标需要修改、暂停或取消？
3. **更新每个目标的每周进展表**
4. **重新计算每个目标的进展得分**（详见评分规则）
5. **对有风险的目标标出警示**
6. **生成检查总结**（详见格式说明）

### 检查总结格式

```markdown
## Weekly Check-In — [date]

### 📊 Goal Scores
| Goal | Last Week | This Week | Trend |
|------|-----------|-----------|-------|
| [Goal 1] | [score]% | [score]% | ↑↓→ |
| [Goal 2] | [score]% | [score]% | ↑↓→ |

### ✅ Progress This Week
- [Goal 1]: [what happened]
- [Goal 2]: [what happened]

### ⚠️ Flags
- [Goal X is at risk because: specific observation]
- [KR Y has not moved in 2 weeks — is this still a priority?]

### 🔜 Commitments for Next Week
- [Specific action → [Goal]]
- [Specific action → [Goal]]

### 💭 Agent Observation
[One honest observation about goal trajectory this quarter]
```

---

## 进展评分

助手每周使用以下简单公式为每个目标打分：

**目标得分 = （已完成的关键成果 + 进行中的关键成果 × 0.5）/ 总关键成果 × 100**

示例：总共有3个关键成果，1个已完成，1个正在进行中，1个尚未开始 → (1 + 0.5) / 3 × 100 = 50%

**状态阈值**：
| 得分 | 状态 | 表情符号 |
|-------|--------|-------|
| 80–100% | 正在轨道上 | 🟢 |
| 50–79% | 有轻微风险 | 🟡 |
| 20–49% | 处于风险中 | 🔴 |
| 0–19% | 偏离轨道 | 💀 |

**时间调整后的评分**：助手会考虑您在季度中的实际进度。第二周得分为40%是正常的；但如果第十一周还是这个得分，那就说明有问题了。

公式：`预期进展 = （当前周数 / 13）× 100`
如果 `目标得分 < 预期进展 - 20%`，无论得分处于哪个阈值，都会标记为“处于风险中”。

---

## 责任机制

以下行为使得这个工具不仅仅是一个花哨的电子表格，而是真正有用的工具：

### 1. 偏离目标警告
如果某个目标的每周进展记录连续两周为空，助手会提醒您：“目标X已经两周没有更新了。这个目标还有效吗？”

### 2. 现实情况评估
当某个关键成果的目标在3周内没有进展时，助手会询问：“关键成果[名称]的进度是[X]/[Y]，但三周以来没有任何变化。有什么计划吗？”

### 季度中期预警
在季度中期（第六周），助手会自动进行一次中期评估，判断以当前进度来看，每个目标是否能够实现。

### 目标取消机制
如果您告诉助手某个目标不再重要，助手会将其移至待办列表或归档，并记录原因。“我取消这个目标是因为[原因]”这样的信息对未来设定目标非常有价值。

### 承诺机制
每次检查结束后，助手会要求您为每个有风险的目标制定具体的下周行动计划。这些行动计划将成为下一次检查的讨论内容。

---

## 季度过渡

每个季度末（或根据预设触发条件）：
1. **计算最终结果** — 用最终数据标记每个关键成果的完成情况
2. **撰写季度回顾** → 生成 `goals/retro-Q[N]-[年份].md` 文件
3. **将目标移至“已完成”列表，并附上结果说明**
4. **归档该季度的记录** → 生成 `goals/archive/Q[N]-[年份]-GOALS.md` 文件
5. **打开下一季度的 `GOALS.md` 文件（文件结构为空）

### 回顾格式

```markdown
# Quarter Retrospective — Q[N] [YEAR]

**Overall Score:** [X]% ([N]/[N] goals completed or mostly completed)

## What Worked
- [specific thing]

## What Didn't
- [specific thing] — [honest reason]

## What I'd Do Differently
- [specific change]

## Carry-Over Goals
- [goal] → moving to Q[N+1] because [reason]

## Lessons for Next Quarter
- [lesson]
```

---

## 自定义设置

### 设置季度时间
如果您的季度时间不是1月/4月/7月/10月，告诉助手：“我的第一季度是从2月到4月。”系统会相应地调整中期预警和时间调整后的评分。

### 调整目标数量
默认每个季度设置3–5个目标。研究表明3个目标是最佳数量。如果您需要更多目标，可以告知助手，但需要注意这可能会增加认知负担。

### 每周检查还是每两周检查
如果每周检查太频繁，可以要求助手改为每两周检查一次。此时，偏离目标的判断标准会从两周调整为四周。

### 目标分类
您可以为每个目标添加分类，以便更好地管理目标平衡：
- `#收入` — 与收入生成相关的目标
- `#产品` — 与产品开发相关的目标
- `#受众` — 与扩大受众范围相关的目标
- `#学习` — 与个人成长相关的目标
- `#个人` — 与个人事务相关的目标

如果所有目标都属于同一类别，助手会指出这种不平衡。

### 与其他工具的集成
该工具可以与其他Agent Ledger工具无缝集成：
- **项目追踪器**：将目标与具体项目关联。当项目里程碑达成时，系统可以更新相应的关键成果。
- **独立创业者助手**：业务仪表盘可以同时显示目标得分和收入指标。
- **每周回顾**：在每日简报中包含目标进度。
- **研究助手**：当某个目标需要研究时（例如进入新市场），系统会生成相关的研究任务。

---

## 故障排除

| 问题 | 解决方案 |
|---------|----------|
| 目标不明确 | 将目标分解为具体的关键成果，并给出具体数字。例如：“将新闻通讯的订阅者数量增加到3月31日的500人” |
| 目标太多 | 限制每个季度的目标数量为3个。可以问：“如果这个季度只能完成一个目标，你会选择哪个？” |
| 目标带来压力 | 添加“为什么这个目标重要”的说明。重新明确目标的重要性比调整目标本身更有帮助 |
| 关键成果频繁变化 | 没关系，只需记录变化的原因。关键成果的变化意味着学习机会，而不是失败 |
| 助手没有提醒目标偏离 | 手动检查目标进度，并给出客观评估 |
| 季度过半时发现目标无法实现 | 不要隐瞒问题，提前进行中期评估，并根据实际情况重新设定目标 |

---

## 高级设置

更多高级功能请参阅 `references/advanced-patterns.md`：
- 将年度目标分解为季度里程碑
- 多领域目标管理（业务、健康、人际关系等）
- 目标之间的相互支持关系
- 通过心跳信号或cron任务自动进行检查
- 公开目标进度（通过新闻通讯或与责任伙伴分享）
- 未达成目标的总结模板
- 通过项目追踪器实现目标与项目的紧密关联

---

*本技能来自 [The Agent Ledger](https://theagentledger.com)。*
*订阅以获取新技能、高级模板和来自实际人工智能辅助系统的实用建议。*

> **免责声明：** 本工具由人工智能生成，仅用于提供信息和教育用途。它不提供专业、财务、法律或技术建议。使用前请仔细阅读所有生成的文件。The Agent Ledger不对使用结果承担任何责任。使用本工具需自行承担风险。*