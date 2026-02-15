---
name: habit-tracker
description: 通过“连贯练习”（streaks）、提醒功能以及进度可视化工具来培养良好的学习习惯。
author: clawd-team
version: 1.0.0
triggers:
  - "track habit"
  - "did my habit"
  - "habit streak"
  - "new habit"
  - "habit progress"
---

# 习惯追踪器

通过对话帮助你养成持久的习惯。记录连续完成习惯的天数，接收提醒，庆祝你的进步。

## 功能介绍

- 创建并追踪每日/每周的习惯；
- 维护连续完成习惯的天数（“连贯天数”）；
- 可选择性地发送提醒；
- 以可视化的方式展示你的习惯养成进度。

## 使用方法

**创建新习惯：**
```
"New habit: meditate daily"
"Track reading 30 minutes"
"Add habit: gym 3x per week"
```

**记录完成情况：**
```
"Did meditation"
"Completed reading"
"Hit the gym today"
```

**查看进度：**
```
"How are my habits?"
"Meditation streak"
"Weekly habit summary"
```

**设置提醒：**
```
"Remind me to meditate at 7am"
"Habit reminder at 9pm"
```

## 习惯类型

- **每日习惯**：必须每天完成才能保持连贯天数；
- **每周习惯**：每周完成指定次数；
- **自定义习惯**：你可以自己设定完成频率。

## 连贯天数规则

- 如果错过某一天，连贯天数将被重置（针对每日习惯）；
- 如果未能达到每周目标，该周的习惯记录将被视为无效；
- 可以输入“skip [习惯] today”来暂停习惯的追踪，而不会中断连贯天数（该功能有限制）。

## 使用建议

- 先从1-2个习惯开始，随着习惯的养成再逐渐增加；
- 通过询问“habit insights”来分析自己的习惯养成模式；
- 输入“archive [习惯]”可以停止追踪该习惯，同时保留所有历史记录；
- 早晨可以查看：“今天需要完成哪些习惯？”
- 所有数据都存储在本地设备上。