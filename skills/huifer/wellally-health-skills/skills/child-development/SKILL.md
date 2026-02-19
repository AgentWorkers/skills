---
name: child-development
description: Track and assess child developmental milestones based on ASQ-3 and Denver II standards. Use when user mentions development, milestones, motor skills, language, social skills, or cognitive development.
argument-hint: <operation_type: record/check/milestone/delay/history, e.g.: record gross, check 12 months, milestone all>
allowed-tools: Read, Write
schema: child-development/schema.json
---

# 儿童发育里程碑跟踪功能

本功能基于ASQ-3和Denver II标准，对儿童发育里程碑进行跟踪和评估，以便及时发现发育迟缓的迹象。

## 核心流程

```
User Input → Parse Operation Type → Read Child Information → Calculate Age → Determine Assessment Items → Generate Assessment Report → Save Data
```

## 第1步：解析用户输入

### 操作类型映射

| 输入 | 操作 | 分类 |
|------|--------|--------|
| record | 记录 | 全部（默认）/大运动/精细运动/语言/社交/认知 |
| check | 核验 | - |
| milestone | 里程碑 | 可选：指定分类 |
| delay | 发育迟缓 | - |
| history | 发展历史 | - |

### 发育分类映射

| 输入关键词 | 分类 |
|----------------|--------|
| 大运动 | 大运动技能 |
| 精细运动 | 精细运动技能 |
| 语言 | 语言能力 |
| 社交 | 社交能力 |
| 认知 | 认知能力 |

## 第2步：检查信息完整性

### 必需填写的内容（如缺少请提示用户填写）：
- 儿童姓名（来自data/profile.json文件）
- 出生日期（来自data/profile.json文件）
- 性别（来自data/profile.json文件）
- 早产情况（来自data/profile.json文件）

### 若儿童资料缺失，请提示用户补充：
```
Child profile not found

Please set child basic information first:
/profile child-name Xiaoming
/profile child-birth-date 2020-01-01
/profile child-gender male
```

## 第3步：计算年龄和月龄

```javascript
birthDate = profile.child_birth_date
today = new Date()

ageMonths = (today - birthDate) / (30.44 * 24 * 60 * 60 * 1000)

// Prematurity correction (<37 weeks, correct until 2 years)
if gestational_age < 37 && ageMonths <= 24:
  correctedAgeMonths = ageMonths - (40 - gestational_age) * 4
else:
  correctedAgeMonths = ageMonths
```

## 第4步：生成评估问题

### 根据年龄确定关键发育里程碑

**6个月龄评估示例：**
```
Please assess whether milestones are achieved (yes/no):

Gross Motor (6 months)
  Can sit briefly without support
  Can support self on hands during tummy time
  Can roll from back to tummy

Fine Motor (6 months)
  Can reach for objects
  Can transfer items between hands
  Can pinch with thumb and finger

Language (6 months)
  Can make single syllable sounds (ma/ba etc.)
  Responds to sounds
  Can turn toward sound source

Social (6 months)
  Shows stranger anxiety
  Laughs out loud
  Can express happiness/anger

Cognitive (6 months)
  Looks for dropped objects
  Can distinguish familiar/stranger faces
```

## 第5步：生成评估报告

### 发育评估分级

| 评估结果 | 状态 |
|-------------------|-----------|
| 正常 | 所有分类均符合年龄标准 |
| 可能存在发育迟缓 | 比同龄儿童落后1-2个月 |
| 显著发育迟缓 | 比同龄儿童落后3个月以上 |

### 正常评估报告示例：
```
Developmental Assessment - Normal

Assessment Information:
Child: Xiaoming
Age: 6 months
Corrected age: 6 months
Assessment date: July 1, 2025

Gross Motor Development:
  Sitting alone: Achieved (at 5 months)
  Rolling over: Achieved (at 4 months)
  Tummy time support: Achieved
  Assessment: Normal

Fine Motor:
  Reaching for objects: Achieved
  Transferring between hands: Achieved
  Pincer grasp: Not achieved (normal, ~9 months)
  Assessment: Normal

Comprehensive Assessment:
  Normal development
  All developmental domains within normal range, no significant delays detected.

Recommendations:
  Continue observation and recording
  Provide rich environmental stimulation
  Interact and communicate with child frequently
  Regular developmental assessments
```

## 第6步：保存数据

将数据保存至`data/child-development-tracker.json`文件，包括以下内容：
- `child_profile`：儿童基本信息
- `developmental_tracking.assessments`：评估记录
- `milestone_achievement`：里程碑达成情况统计
- `alerts`：发育预警信息
- `statistics`：统计信息

## 不同年龄段的发育里程碑

### 0-3个月（婴儿早期）
| 年龄 | 大运动 | 精细运动 | 语言 | 社交 |
|-----|-------------|------------|----------|--------|
| 1个月 | 短时间抬头 | 眼睛跟随物体移动 | 发出咿呀声 | 注视人脸 |
| 2个月 | 俯卧时能抬头45度 | 双手合十 | 发笑 | 对人微笑 |
| 3个月 | 俯卧时能抬头90度 | 抓住摇铃 | 对人脸微笑 |

### 4-6个月（婴儿中期）
| 年龄 | 大运动 | 精细运动 | 语言 | 社交 |
|-----|-------------|------------|----------|--------|
| 4个月 | 头部稳定，能够翻身 | 伸手去抓物品 | 发出尖叫 | 大声笑 |
| 5个月 | 在他人帮助下能够坐立 | 能用手指捏取物品 | 被声音吸引 | 识别陌生人 |
| 6个月 | 能短暂坐立 | 能转移物品 | 能说单音节词 | 对陌生人表现出焦虑反应 |

### 发育迟缓的标准

| 分类 | 轻微发育迟缓 | 显著发育迟缓 | 严重发育迟缓 |
|--------|------------|------------------|---------------|
| 大运动 | 比同龄儿童落后1-2个月 | 比同龄儿童落后3-4个月 | 比同龄儿童落后超过4个月 |
| 精细运动 | 比同龄儿童落后1-2个月 | 比同龄儿童落后3-4个月 | 比同龄儿童落后超过4个月 |
| 语言 | 比同龄儿童落后1-2个月 | 比同龄儿童落后3-4个月 | 比同龄儿童落后超过4个月 |
| 社交/认知 | 比同龄儿童落后1-2个月 | 比同龄儿童落后3-4个月 | 比同龄儿童落后超过4个月 |

## 执行说明

1. 从data/profile.json文件中读取儿童信息。
2. 计算儿童的年龄和矫正年龄（如适用）。
3. 根据操作类型执行相应功能。
4. 生成评估报告。
5. 将数据保存至data/child-development-tracker.json文件。

## 医学安全原则

### 安全注意事项：
- 本系统仅用于记录和参考儿童发育里程碑，不能替代专业医学诊断。
- 本系统无法预测儿童未来的发育水平。
- 不能替代专业的发育评估。
- 本系统不提供干预训练计划的建议。

### 系统功能：
- 跟踪儿童发育里程碑
- 筛查发育迟缓
- 发出早期预警
- 记录评估历史

## 重要提示

本系统仅用于记录和参考儿童发育里程碑，**不能替代专业医学诊断**。

儿童的发育存在个体差异；落后1-2个月可能是正常现象。

如果发现明显的发育迟缓或对儿童发育有疑虑，请**及时咨询儿童健康专家或发育行为儿科医生**。