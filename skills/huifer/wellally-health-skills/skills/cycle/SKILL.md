---
name: cycle
description: Track menstrual cycle, PMS symptoms, ovulation prediction, and women's health insights
argument-hint: <operation_type+description, e.g.: start period started today, log heavy flow today, predict conception mode>
allowed-tools: Read, Write
schema: cycle/schema.json
---

# 月经周期追踪功能

帮助用户追踪月经周期、经前综合症（PMS）症状、预测排卵时间，并提供个性化的健康建议。

## 核心流程

```
User Input → Parse Operation Type → Execute Operation → Generate/Update Data → Save → Output Result
```

## 支持的操作

| 操作 | 描述 | 示例 |
|-----------|-------------|---------|
| 开始 | 记录月经开始时间 | /cycle start 今天开始记录月经周期 |
| 结束 | 记录月经结束时间 | /cycle end 今天月经结束 |
| 记录 | 日常日志 | /cycle log 今天经量较多，伴有腹痛 |
| 预测 | 排卵预测 | /cycle predict 预测受孕可能性 |
| 查看历史记录 | 查看周期记录 | /cycle history 查看过去6个月的记录 |
| 分析 | 分析周期规律 | /cycle analyze 分析周期数据 |
| 状态 | 当前周期状态 | /cycle status 查看当前周期状态 |
| 设置 | 配置参数 | /cycle settings 设置周期长度（例如：28天） |

## 第一步：解析用户输入

### 操作类型识别

| 输入关键词 | 对应操作 |
|----------------|-----------|
| start | 开始记录周期 |
| end | 结束记录周期 |
| log | 记录每日情况 | |
| predict | 预测排卵时间 | |
| history | 查看历史记录 | |
| analyze | 分析周期数据 | |
| status | 查看周期状态 | |
| settings | 修改设置 | |

### 日期识别

| 输入 | 日期格式 |
|------|-------------|
| today | 当前日期 | |
| YYYY-MM-DD | 指定日期 | |
| Month DD | 今年某月的某一天 | |
| Day X | 当前周期的某一天 | |

### 经期强度识别

| 关键词 | 强度 | 分值 |
|----------|-----------|-------|
| very_heavy | 非常严重 | 5 |
| heavy | 严重 | 4 |
| medium | 中等 | 3 |
| light | 轻微 | 2 |
| spotting | 出血量极少 | 1 |

### 症状识别

**疼痛**：腹痛、腰痛、头痛、乳房胀痛、关节疼痛
**消化系统**：腹胀、腹泻、便秘、恶心、食欲变化
**情绪**：情绪波动、易怒、焦虑、情绪低落、烦躁
**精力**：疲劳、疲倦、缺乏精力、嗜睡

### 情绪状态识别

**积极**：快乐、愉快、平静、正常
**消极**：情绪低落、焦虑、易怒、烦躁、抑郁
**中性**：情绪平稳、正常

### 精力水平识别

**高**：精力充沛、活跃、状态良好
**中等**：正常、状态一般
**低**：疲劳、疲倦、精疲力尽

## 第二步：检查信息完整性

### 开始记录周期的操作要求：
- 无（使用默认日期：今天）

### 开始记录周期的操作验证：
- 日期不能在未来
- 如果当前已有正在进行的周期，系统会提示用户先结束当前周期

### 结束记录周期的操作要求：
- 无（使用默认日期：今天）
- 必须有正在进行的周期
- 结束日期必须晚于开始日期

### 记录每日情况的操作要求：
- 需提供日志描述

### 记录每日情况的操作建议：
- 提供日期（可选，默认为今天）
- 经期流量描述
- 任何出现的症状

## 第三步：根据需要提供交互式提示

### 情况A：在周期结束前重新开始记录
```
Unfinished cycle detected

Current cycle: Started 2025-11-28
Tip: Please use /cycle end to end current cycle first
```

### 情况B：尝试结束记录但当前没有活跃的周期
```
No active cycle

Recent cycle: 2025-11-30 - 2025-12-04
Tip: Please use /cycle start to begin a new cycle
```

### 情况C：日志记录内容不足
```
Please provide more log information, such as:
• Flow: heavy, medium, light
• Symptoms: abdominal pain, lower back pain, headache, etc.
• Mood: normal, low, anxious
```

## 第四步：生成JSON数据

### 周期数据结构
```json
{
  "cycle_id": "cycle_20251228",
  "period_start": "2025-12-28",
  "period_end": null,
  "cycle_length": null,
  "period_length": null,
  "flow_pattern": {
    "day_1": "heavy",
    "day_2": "medium"
  },
  "pms_symptoms": {
    "start_date": null,
    "symptoms": {}
  },
  "daily_logs": [],
  "ovulation_date": null,
  "predictions": {},
  "notes": "",
  "created_at": "2025-12-28T08:00:00.000Z",
  "completed": false
}
```

### 日常日志数据结构
```json
{
  "id": "log_20251228001",
  "date": "2025-12-28",
  "cycle_day": 1,
  "phase": "menstrual",
  "flow": {
    "intensity": "heavy",
    "description": "Heavy flow"
  },
  "symptoms": ["abdominal pain", "lower back pain"],
  "mood": "low",
  "energy_level": "low",
  "medication_taken": [],
  "notes": "",
  "created_at": "2025-12-28T20:00:00.000Z"
}
```

完整的数据结构定义请参见 [schema.json](schema.json)。

## 第五步：保存数据

1. 读取 `data/cycle-tracker.json` 文件
2. 更新相关数据
3. 将更新后的数据写回文件
4. 如果有详细的记录，将其保存到 `data/周期记录/YYYY-MM/YYYY-MM-DD_周期记录.json` 文件中

## 执行说明
```
1. Parse user input and determine operation type
2. Execute corresponding logic based on operation type
3. Validate input data and state
4. Generate JSON compliant with schema.json
5. Save to data/cycle-tracker.json
6. Output operation result and summary to user
```

## 示例交互

### 示例1：开始记录周期
```
User: /cycle start period started today

System:
Cycle record created

Cycle Information:
Period start: 2025-12-28

Prediction Information:
Expected next period: 2026-01-25
Expected ovulation date: 2026-01-11
Fertile window: January 6 - January 12

Current Status:
Cycle day: 1
Phase: Menstrual phase

Data saved to: data/周期记录/2025-12/2025-12-28_周期记录.json
```

### 示例2：记录每日情况
```
User: /cycle log heavy flow today abdominal pain

System:
Daily log recorded

Log Information:
Date: 2025-12-28
Cycle day: 1
Phase: Menstrual phase

Flow: Heavy (level 4)
Symptoms: Abdominal pain
Mood: Normal
Energy: Medium

Cycle Progress:
Day 1/5 of current cycle (estimated)
Days to ovulation: 13
Days to next period: 27

Data saved to: data/周期记录/2025-12/2025-12-28_周期记录.json
```

### 示例3：预测排卵时间
```
User: /cycle predict conception mode

System:
Ovulation Prediction (Conception Mode)

Based on last 6 cycles:
Average cycle length: 28.5 days
Cycle regularity: 92% (very regular)

Ovulation Prediction:
Expected ovulation date: January 11, 2026

Detailed Fertile Schedule:
January 6 (Fertile day 1): 10% conception probability
January 7 (Fertile day 2): 15% conception probability
January 8 (Fertile day 3): 20% conception probability
January 9 (Fertile day 4): 25% conception probability
January 10 (Fertile day 5): 30% conception probability
January 11 (Ovulation day): 35% conception probability
January 12 (Fertile day 7): 15% conception probability

Best conception window: January 9 - January 11

Conception Advice:
• Start folic acid supplementation 3 months early (400-800μg/day)
• Maintain moderately frequent intercourse during fertile period
• Lie down for 15-30 minutes after intercourse
• Maintain healthy weight and regular sleep schedule
```

更多使用示例请参见 [examples.md](examples.md)。