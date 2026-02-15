---
name: lofy-fitness
description: Lofy AI助手的健身管理功能包括：  
- 通过自然语言记录锻炼情况；  
- 跟踪饮食摄入量，并提供卡路里和蛋白质的估算数据；  
- 使用Epley公式检测健身进展（如体重变化）；  
- 根据每周目标生成健身提醒；  
- 提供健身进度报告。  

这些功能适用于记录锻炼内容、饮食情况、监测健身进展，或生成每周健身总结。
---

# 健身追踪器 — 锻炼与健康管理工具

该工具用于记录用户的锻炼情况、饮食记录、个人最佳成绩（PRs）以及健身习惯的持续性。通过自然的对话方式，帮助用户保持自律和诚实。

## 数据文件：`data/fitness.json`

```json
{
  "profile": { "goal": "", "weight_log": [], "start_date": null },
  "workouts": [],
  "meals": [],
  "prs": {},
  "weekly_summary": [],
  "current_week": { "workout_count": 0, "target": 0, "workouts": [] }
}
```

### 锻炼记录格式
```json
{
  "date": "2026-02-07",
  "type": "strength",
  "muscle_groups": ["chest", "triceps"],
  "exercises": [
    { "name": "Bench Press", "sets": [{"weight": 185, "reps": 5}] }
  ],
  "duration_min": 60,
  "notes": ""
}
```

### 饮食记录格式
```json
{
  "date": "2026-02-07",
  "meal": "lunch",
  "description": "Chicken bowl with rice",
  "estimated_calories": 650,
  "estimated_protein_g": 45,
  "time": "12:30"
}
```

## 自然语言解析

### 锻炼内容解析：
- "bench 185x5 185x4" → 卧推，2组：185次/组，每组5次
- "tricep pushdowns 50x12 x3" → 三头肌弯举，3组，每组50次
- "went for a 5k run, 28 minutes" → 有氧运动，跑步，5公里，28分钟
- "did legs" （未提供具体细节） → 记录锻炼的肌肉群，并标注“未提供详细信息”，但仍计入锻炼记录

### 饮食记录解析：
- "had chipotle for lunch" → 估计热量约650卡，蛋白质约40克
- "protein shake after gym" → 估计热量约200卡，蛋白质约30克
- "skipped breakfast" → 记录该行为；如果连续3天以上出现这种情况，可适当提醒用户

### 个人最佳成绩（PR）检测：
解析锻炼记录后，将每次锻炼的结果与存储的PR进行比较：
- Epley 1RM（最大重复次数）的计算公式：重量 × (1 + 每组重复次数 / 30)
- 如果新的1RM超过存储的PR，则更新记录并给予鼓励
- 仅对达到个人最佳成绩的锻炼进行庆祝，而非每次锻炼都记录

## 使用说明：
1. 在回复关于健身相关的问题之前，请务必先查看`data/fitness.json`文件。
2. 每次完成锻炼后，立即更新`data/fitness.json`文件中的数据。
3. 回复内容应简洁明了，包括确认信息及一条评论。
4. 提醒逻辑：每天最多发送一次健身提醒，仅当用户未达到每周目标时才会发送。
5. 重点关注锻炼的持续性，而非锻炼强度；坚持锻炼比追求高强度更重要。
6. 如果用户提及受伤或感到疼痛，建议其休息，切勿强迫自己继续锻炼。
7. 每周生成报告，通过数据展示用户的健身趋势（是否有所进步、处于平台期还是有所下降）。