---
name: child-sleep
description: Track child sleep patterns, manage sleep schedules, and identify sleep problems. Use when user mentions child sleep, bedtime, waking up, nap, or sleep issues.
argument-hint: <operation_type: record/schedule/problem/analysis/routine/history, e.g.: record 9pm sleep 7am wake, schedule, problem difficulty falling asleep, analysis, routine>
allowed-tools: Read, Write
schema: child-sleep/schema.json
---

# 儿童睡眠管理功能

本功能支持儿童睡眠记录、睡眠计划管理以及睡眠问题的识别，并提供针对不同年龄段的睡眠时长参考和作息建议。

## 核心流程

```
User Input → Identify Operation Type → Read Child Information → Determine Sleep Standards by Age → Generate Assessment Report → Save Data
```

## 第一步：解析用户输入

### 操作类型映射

| 输入 | 操作 | 说明 |
|------|--------|-------------|
| record | 记录睡眠数据 | 录制孩子的睡眠情况 |
| schedule | 安排睡眠计划 | 设置孩子的睡眠时间表 |
| problem | 识别睡眠问题 | 检测是否存在睡眠问题 |
| analysis | 分析睡眠质量 | 对孩子的睡眠状况进行分析 |
| routine | 提出作息建议 | 根据分析结果提供作息建议 |
| history | 查看历史记录 | 查看孩子的睡眠历史数据 |

### 时间信息识别

| 输入格式 | 解析结果 |
|---------------|---------------|
| 21:00 sleep, bedtime 21:00 | 睡眠时间：21:00 |
| 7:00 wake, wake 7:00 | 觉醒时间：07:00 |
| woke 1 time, wakeup 1 | 夜间醒来次数：1次 |

## 第二步：检查信息完整性

### 必需的信息：
- 睡眠时间（可从输入中获取或使用默认值）
- 觉醒时间（可从输入中获取或使用默认值）

### 可选信息：
- 夜间醒来次数
- 入睡时间
- 睡眠质量描述

## 第三步：根据年龄确定睡眠标准

| 年龄 | 推荐总睡眠时间 | 夜间睡眠时间 | 白天小睡时间 | 小睡次数 |
|-----|-------------------------|-------------|--------------|-----------|
| 0-3个月 | 14-17小时 | 8-10小时 | 6-7小时 | 3-4次 |
| 4-12个月 | 12-16小时 | 9-12小时 | 3-4小时 | 2-3次 |
| 1-2岁 | 11-14小时 | 10-12小时 | 1.5-3小时 | 1-2次 |
| 3-5岁 | 10-13小时 | 10-12小时 | 0-2小时 | 0次 |
| 6-12岁 | 9-12小时 | 9-12小时 | 0次 | 0次 |
| 13-18岁 | 8-10小时 | 8-10小时 | 0次 | 0次 |

## 第四步：生成评估报告

### 睡眠质量评估

| 评估项目 | 标准 |
|----------------|----------|
| 睡眠时长 | 在推荐范围内为正常 |
| 入睡时间 | 在30分钟内入睡为正常 |
| 夜间醒来次数 | 1次以内为正常（1岁以下儿童可能更多） |
| 睡眠质量 | 睡眠质量良好，有助于正常发育 |

### 睡眠质量正常示例：
```
Sleep record saved

Sleep Information:
Child: Xiaoming
Age: 2 years 5 months
Sleep date: Night of January 13, 2025

Bedtime: 21:00
Asleep time: 21:30
Wake time: 07:00
Total sleep duration: 9.5 hours

Night Status:
  Night wakeups: 1 time
  Wake duration: ~10 minutes
  Falling asleep: Self-soothing
  Sleep quality: Good

Sleep Assessment:
  Sleep duration normal (recommended 10-12 hours)
  Appropriate bedtime
  Normal night wakeups
  Good sleep quality

Daytime Naps:
  Nap count: 1 time
  Nap duration: ~2 hours
  Total sleep (including naps): ~11.5 hours

Schedule Recommendations:
  Continue current schedule
  Establish consistent bedtime routine
  Create good sleep environment

Data saved
```

### 睡眠不足示例：
```
Sleep Insufficient Alert

Sleep Information:
Child: Xiaoming
Age: 2 years 5 months
Sleep date: Night of January 13, 2025

Bedtime: 22:00
Asleep time: 23:00
Wake time: 06:30
Total sleep duration: 7.5 hours

Sleep Assessment:
  Insufficient sleep duration (recommended 10-12 hours)
  Late bedtime
  Difficulty falling asleep
  Frequent night wakeups

Possible Impact:
  Poor daytime energy
  Irritability
  Decreased appetite
  Lowered immunity

Improvement Recommendations:

Adjust Schedule
  Start bedtime routine 30 minutes early
  Fixed bedtime (20:30-21:00)

Optimize Bedtime Routine
  Stop screen time 1 hour before
  Quiet activities (picture books, warm bath)
  Fixed routine order

Improve Sleep Environment
  Room temperature 20-22°C
  Keep dark and quiet
  Comfortable bedding

If sleep deprivation persists:
  Consult pediatrician to rule out sleep disorders etc.

Data saved
```

## 第五步：保存数据

将数据保存到 `data/child-sleep-tracker.json` 文件中，内容包括：
- `child_profile`：儿童的基本信息
- `sleep_records`：睡眠记录
- `sleep_schedule`：睡眠时间表
- `bedtime_routine`：睡前作息习惯
- `sleep_problems`：睡眠问题记录
- `statistics`：睡眠统计信息

## 常见睡眠问题及应对建议

### 入睡困难
- 表现：睡前30分钟以上仍无法入睡
- 可能原因：作息不规律、过度疲劳、睡眠环境不佳
- 建议：制定固定的作息时间表，提前开始睡前准备

### 夜间频繁醒来
- 表现：每晚醒来2次以上
- 可能原因：饥饿、不适、习惯性醒来
- 建议：查明原因，逐步减少夜间醒来的次数

### 过早起床
- 表现：早上6点前醒来且无法再次入睡
- 可能原因：睡眠环境或作息安排不当
- 建议：调整入睡时间，遮挡早晨的光线

### 拒绝小睡
- 表现：白天不愿意小睡
- 可能原因：处于发育阶段、精力旺盛
- 建议：创造安静的睡眠环境，不要强迫孩子小睡

### 夜惊/噩梦
- 表现：夜间惊恐地哭泣
- 可能原因：处于发育阶段、过度疲劳
- 建议：安抚孩子，不要唤醒他们

## 2-3岁儿童的睡前作息建议

### 睡前1小时（20:00）
- 停止使用电子设备
- 停止剧烈活动
- 转换到安静的环境

### 睡前30分钟（20:30）
- 收拾玩具
- 上厕所、喝水
- 准备洗澡

### 洗澡时间（20:40）
- 洗温水澡（10-15分钟）
- 穿上睡衣/尿布

### 睡前活动（21:00）
- 读睡前故事书（2-3本）
- 轻声说话/唱歌
- 举行简单的睡前仪式

### 睡觉时间（21:15-21:30）
- 上床睡觉，盖好被子
- 给予最后的安慰
- 说晚安，然后离开房间

## 执行步骤

1. 读取 `data/profile.json` 文件中的儿童信息
2. 根据年龄确定睡眠标准
3. 分析睡眠数据或生成相应的建议
4. 将结果保存到 `data/child-sleep-tracker.json` 文件中

## 医学安全注意事项

- 本系统仅用于睡眠记录和提供参考建议，**不能替代专业医学诊断**。
- 如出现以下情况，请咨询儿科医生：
- 打鼾并伴有呼吸暂停
- 夜间频繁惊恐地哭泣
- 白天过度嗜睡
- 睡眠中行为异常
- 长期严重失眠