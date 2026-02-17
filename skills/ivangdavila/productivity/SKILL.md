---
name: Productivity
version: 1.0.1
description: "通过能源管理、时间规划以及设定实际的工作界限来规划、集中精力并完成工作。"
changelog: "Preferences now persist across skill updates"
---
## 自适应学习机制

该学习机制会了解你的工作方式：识别你的工作限制、模式，并根据这些信息来个性化提供帮助。

**核心流程：**
1. **识别** — 通过你提出的问题来了解你的当前处境。
2. **匹配** — 加载相应的情境文件：`situations/{type}.md`。
3. **调整** — 根据你的精力状况、工作限制和环境因素来调整建议。
4. **存储** — 随时间积累你的学习数据（在存储前进行确认）。

---

## 情境检测

根据用户的主要工作情境来加载相应的文件。

| 信号 | 情境 | 对应文件 |
|--------|-----------|------|
| 截止日期、考试、拖延症 | 学生 | `situations/student.md` |
| 日程混乱、任务分配问题 | 高管 | `situations/executive.md` |
| 缺乏条理、客户压力、孤立无援 | 自由职业者 | `situations/freelancer.md` |
| 有孩子、经常被打扰、感到内疚、精疲力竭 | 父母 | `situations/parent.md` |
| 创意枯竭、灵感不稳定 | 创意工作者 | `situations/creative.md` |
| 精疲力竭的症状、长期处于高压状态、悲观情绪 | 精疲力竭者 | `situations/burnout.md` |
| 独立创业者、多任务处理、身兼数职 | 创业者 | `situations/entrepreneur.md` |
| 注意力缺陷多动障碍（ADHD）导致的工作效率问题 | ADHD患者 | `situations/adhd.md` |
| 不同时区、异步工作、工作时间难以控制 | 远程工作者 | `situations/remote.md` |
| 一对一沟通、团队协作、频繁切换任务 | 管理者 | `situations/manager.md` |
*开始时表现良好但随后效率下降* | 习惯养成问题 | `situations/habits.md` |
*总是感觉时间不够用、休息焦虑、过度忙碌导致的问题* | 内疚感/恢复期问题 | `situations/guilt.md` |

多种情境可能会同时存在，应优先处理最主要的情境。

---

## 通用框架

有关适用于各种情境的技巧，请参阅 `frameworks.md`：
- 能量管理（不仅仅是时间管理）
- “足够好”的标准
- 任务启动流程
- 设定工作边界的技巧

---

## 常见误区

请参阅 `traps.md`，了解应避免说或建议的内容。

---

## 生产力档案

用户的偏好信息会保存在 `~/productivity/memory.md` 文件中。首次使用时需要创建该档案：

```markdown
## Energy Patterns
<!-- When focus peaks/crashes. Format: "pattern (level)" -->
<!-- Examples: Peak 9-11am (confirmed), Crashes after lunch (observed) -->

## Constraints
<!-- Hard limits. Format: "constraint (level)" -->
<!-- Examples: Kids pickup 3pm (confirmed), Open office (stated) -->

## What Works
<!-- Effective techniques. Format: "technique (level)" -->
<!-- Examples: Pomodoro (confirmed), Body doubling (pattern) -->

## What Doesn't
<!-- Failed approaches. Format: "approach (level)" -->
<!-- Examples: Morning routines don't stick (confirmed) -->

## Current Situation
<!-- Context. Format: "situation (level)" -->
<!-- Examples: Freelancer, 3 clients (stated), New parent 4mo (confirmed) -->

## Goals
<!-- Objectives. Format: "goal (level)" -->
<!-- Examples: Ship side project (stated), Stop weekend work (exploring) -->
```

*输入格式：`方面：洞察（级别）` — 级别包括：已描述的情况 → 观察到的模式 → 经过确认的信息*

---

*如果文件为空，说明目前还没有收集到任何信息。每个问题都能帮助我们更深入地了解你的工作方式。*