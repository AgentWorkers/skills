---
name: "Water Tracker"
description: "它会自动学习你的补水习惯，通过日常对话中的提及来记录你的饮水量，而无需进行精确的测量。"
version: "1.0.1"
changelog: "Preferences now persist across skill updates"
---
## 自适应补水追踪

此功能会随着用户补水习惯的变化而不断优化。它会根据用户实际的补水情况以及影响补水效果的因素进行自我调整。

**使用规则：**
- 从任何来源（对话、饮食记录、运动记录等）收集与补水相关的信息。
- 首次提到补水相关内容时，询问用户常用的饮水容器容量（例如：“你通常使用多大容量的杯子或瓶子？”）。
- 对于模糊的记录（如“午餐时喝了水”），会通过上下文进行推测。
- 如果记录确实不明确，最多提一个问题进行澄清，之后会记住用户的回答。
- 绝不会因为用户忘记喝水而催促他们，也不会强制设定具体的饮水量目标（毫升或盎司）。
- 如果用户记录了摄入了苏打水、果汁或咖啡，只需记录下来，无需评价或提醒。
- 当天气炎热、用户进行运动或喝了咖啡时，会默默地提示他们需要增加饮水量。
- 如果用户表示头痛或疲劳，会温和地询问：“今天的饮水量如何？”
- 随着时间的推移，系统会逐渐了解用户的饮食规律、晨间习惯和工作习惯。
- 用户的常用饮水容器容量信息存储在 `containers.md` 文件中，饮水习惯则记录在 `patterns.md` 文件中。

---

## 记忆存储

用户的偏好信息会保存在 `~/water/memory.md` 文件中。

请使用以下代码块来创建并维护这个文件：

```markdown
## Sources
<!-- Where hydration data comes from. Format: "source: what" -->
<!-- Examples: conversation: meal mentions, fitness: post-workout -->

## Containers
<!-- Learned container sizes. Format: "container: size" -->
<!-- Examples: usual glass: 300ml, gym bottle: 750ml, restaurant: 250ml -->

## Schedule
<!-- Detected hydration patterns. Format: "pattern" -->
<!-- Examples: always with lunch, coffee then water AM, evening tea -->

## Correlations
<!-- What affects their hydration. Format: "factor: effect" -->
<!-- Examples: gym days: +500ml, hot weather: extra glass, coffee: follows with water -->

## Preferences
<!-- How they want hydration tracked. Format: "preference" -->
<!-- Examples: no reminders, just log silently, weekly summary only -->

## Flags
<!-- Signs of low hydration to watch. Format: "signal" -->
<!-- Examples: headache, fatigue, dark urine mentioned, skipped water at lunch -->
```

*如果某个部分为空，说明目前还没有相关数据。请继续观察并补充信息。*