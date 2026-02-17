---
name: "Sleep"
description: "它会自动学习你的睡眠模式，通过可穿戴设备收集数据、分析你的日常对话以及观察你的睡眠习惯来了解你的睡眠规律。"
version: "1.0.1"
changelog: "Preferences now persist across skill updates"
---
## 自适应睡眠追踪功能

该功能会随着用户睡眠习惯的了解以及影响睡眠因素的变化而不断进化。

**规则：**
- 从任何来源（可穿戴设备、对话内容、用户的自发评论等）收集与睡眠相关的信息。
- 判断用户是希望主动获取睡眠状态更新，还是仅希望被被动观察。
- 在收集到连续3次以上一致的睡眠数据后，分析睡眠模式。
- 绝不在不合适的时机（如深夜或用户忙碌时）询问用户的睡眠情况。
- 有关数据整合的详细信息，请参考 `sources.md`；有关检测到的睡眠节律信息，请参考 `patterns.md`。

---

## 记忆存储

用户的睡眠数据会保存在以下路径：`~/sleep/memory.md`

**格式：**
```markdown
# Sleep Memory

## Sources
<!-- Where sleep data comes from. Format: "source: reliability" -->
<!-- Examples: apple-health: synced daily, conversation: mentions fatigue -->

## Schedule
<!-- Detected sleep patterns. Format: "pattern" -->
<!-- Examples: weekday ~23:30-07:00, weekend +1.5h later -->

## Correlations
<!-- What affects their sleep. Format: "factor: effect" -->
<!-- Examples: coffee after 15:00: -1h, exercise: +quality -->

## Preferences
<!-- How they want sleep tracked. Format: "preference" -->
<!-- Examples: no morning check-ins, weekly summary only -->

## Flags
<!-- Signs of poor sleep to watch for. Format: "signal" -->
<!-- Examples: "tired", "couldn't sleep", double coffee -->
```

*如果某个部分为空，说明目前还没有相关数据。请通过观察用户的对话内容来补充数据。*