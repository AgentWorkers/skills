---
name: workout-logger
description: 记录锻炼情况，跟踪进度，获取锻炼建议以及项目提交（PR）的跟踪信息。
author: clawd-team
version: 1.0.0
triggers:
  - "log workout"
  - "track exercise"
  - "gym session"
  - "what's my PR"
  - "workout history"
---

# 锻炼记录器

通过对话来记录你的健康状况，记录锻炼情况，跟踪个人最佳成绩（PRs），并查看随时间的进步。

## 功能介绍

- 以自然语言记录锻炼内容
- 跟踪个人最佳成绩
- 显示进度图表
- 根据你的锻炼历史推荐合适的锻炼项目
- 你的智能健身伙伴，会记住你所有的锻炼数据。

## 使用方法

**记录锻炼：**
```
"Bench press 185lbs 3x8"
"Ran 5k in 24 minutes"
"Did 30 min yoga"
"Leg day: squats 225x5, lunges 3x12, leg press 400x10"
```

**查看进度：**
```
"What's my bench PR?"
"Show deadlift progress"
"How many times did I work out this month?"
```

**获取建议：**
```
"What should I do for back today?"
"I have 20 minutes, suggest a workout"
"What haven't I trained this week?"
```

**查看历史记录：**
```
"Last chest workout"
"Running history this month"
"Volume for legs last week"
```

## 锻炼类型

- 力量训练（重量 × 次数 × 组数）
- 有氧运动（距离、时间、速度）
- 柔韧性训练（持续时间、类型）
- 体育活动（具体运动、持续时间）

## 最佳成绩（PR）跟踪

- 自动检测以下最佳成绩：
  - 1RM（根据最大重复次数估算）
  - 锻炼量（次数或距离）的最佳成绩
  - 距离/时间记录
  - 连续锻炼成就

## 使用技巧

- 保持锻炼名称的一致性，以便准确跟踪数据
- 说“与上次相同”即可重复之前的锻炼内容
- 询问“恢复状态”以获取休息建议
- 对于不需要使用重物的锻炼，可以使用“自重”作为重量单位
- 随时可以将数据导出为 CSV 格式