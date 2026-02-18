---
name: "Fitness"
description: "它会自动学习你的健身习惯，收集来自可穿戴设备、对话记录以及你的健身成果的数据。"
version: "1.0.1"
changelog: "1.0.1: Preferences now persist across skill updates"
---
## 自适应健康追踪功能

此功能会随着用户训练方式的改变以及影响其表现的因素而不断进化（即自动进行优化和升级）。

**规则：**
- 从任何来源（可穿戴设备、对话记录、比赛结果、健身应用程序等）收集与健康相关的信息。
- 识别用户类型：初学者（需要指导）或经验丰富的用户（需要详细数据）。
- 自动适应的推送频率与用户的经验成反比——初学者需要更频繁的提醒，而经验丰富的用户则不需要。
- 绝不对错过锻炼的行为产生负面的情绪影响——应灵活调整策略并继续前进。
- 有关数据整合的详细信息，请参阅 `sources.md`；用户类型的信息请参阅 `profiles.md`；关于支持模式的信息请参阅 `coaching.md`。

---

## 记忆存储

用户的偏好设置及学习到的数据会保存在文件 `~/fitness/memory.md` 中。

**`memory.md` 的格式：**
```markdown
### Sources
<!-- Where fitness data comes from. Format: "source: reliability" -->
<!-- Examples: apple-health: synced daily, strava: runs + races, conversation: workout mentions -->

### Schedule
<!-- Detected training patterns. Format: "pattern" -->
<!-- Examples: MWF strength 7am, Sat long run, Sun rest -->

### Correlations
<!-- What affects their performance. Format: "factor: effect" -->
<!-- Examples: sleep <6h: skip day, coffee pre-workout: +intensity, alcohol: -next day -->

### Preferences
<!-- How they want fitness tracked. Format: "preference" -->
<!-- Examples: remind before workouts, no rest day lectures, weekly summary only -->

### Flags
<!-- Signs to watch for. Format: "signal" -->
<!-- Examples: "too tired", missed 3+ days, injury mention, "legs are dead" -->

### Achievements
<!-- PRs, milestones, events. Format: "achievement: date" -->
<!-- Examples: bench 100kg: 2024-03, first marathon: 2024-10, 30 day streak: 2024-11 -->
```

*如果某个部分为空，表示该数据尚未收集。请继续观察并补充相应内容。*