---
name: child-mental
description: Child mental health screening, mood tracking, behavior assessment, anxiety and ADHD screening. Use when user mentions child emotions, behavior, attention, mood swings, or mental concerns.
argument-hint: <operation_type: record/mood/behavior/anxiety/adhd/report/history, e.g.: record happy mood, mood happy, behavior, anxiety, adhd>
allowed-tools: Read, Write
schema: child-mental/schema.json
---

# 儿童心理健康评估技能

该技能用于儿童的心理健康评估、情绪追踪以及行为问题的筛查，提供关于焦虑、注意力等方面的初步评估。

## 核心流程

```
User Input → Identify Operation Type → Read Child Information → Determine Assessment Items by Age → Generate Assessment Report → Save Data
```

## 第一步：解析用户输入

### 操作类型映射

| 输入 | 操作 | 说明 |
|------|--------|-------------|
| record | 记录 | 录入全面评估信息 |
| mood | 情绪 | 追踪情绪变化 |
| behavior | 行为 | 评估行为表现 |
| anxiety | 焦虑 | 筛查焦虑状况 |
| adhd | ADHD | 筛查注意力缺陷多动障碍（ADHD） |
| report | 生成报告 | 生成综合评估报告 |
| history | 历史记录 | 查看过往评估数据 |

### 情绪关键词映射

| 输入 | 情绪 |
|------|------|
| happy | 开心的 |
| calm | 平静的 |
| sad | 悲伤的 |
| angry | 生气的 |
| excited | 兴奋的 |
| anxious | 焦虑的 |

## 第二步：检查信息完整性

### 必需输入（缺失时提示输入）：
- 儿童姓名（来自 data/profile.json 文件）
- 出生日期（来自 data/profile.json 文件）
- 性别（来自 data/profile.json 文件）

## 第三步：根据年龄确定评估项目

| 年龄 | 评估重点 |
|-----|------------------|
| 0-3岁 | 情绪反应、依恋关系、行为模式 |
| 3-6岁 | 情绪表达、社交行为、注意力 |
| 6-12岁 | 情绪调节、学习行为、同伴关系 |
| 12-18岁 | 情绪管理、自我意识、应对压力 |

## 第四步：生成评估报告

### 情绪状态评估

| 总体情绪 | 状态 |
|--------------|------------|
| 稳定 | 情绪反应正常，自我调节能力良好 |
| 波动较大 | 情绪变化频繁，难以预测 |
| 不稳定 | 难以自我安抚，经常哭泣 |

### 行为评估分级

| 评估结果 | 状态 |
|-------------------|-----------|
| 正常 | 所有行为领域均符合年龄特征 |
| 轻微问题 | 1-2个领域存在轻微困难 |
| 严重问题 | 多个领域存在显著困难 |

### 正常评估报告示例：
```
Mental health assessment saved

Assessment Information:
Child: Xiaoming
Age: 2 years 5 months
Assessment date: January 14, 2025

Mood State:
  Overall mood: Stable
  Emotional expression: Rich and appropriate
  Emotional regulation: Good

Behavior Assessment:
  Overall behavior: Normal
  Activity level: Moderate
  Attention: Good
  Compliance: Good
  Aggressive behavior: None

Comprehensive Assessment:
  Normal mental development

Recommendations:
  Continue providing loving environment
  More companionship and interaction
  Establish regular daily routine

Data saved
```

## 第五步：保存数据

将数据保存到 `data/child-mental-tracker.json` 文件中，内容包括：
- `child_profile`：儿童基本信息
- `assessments`：评估记录
- `mood_tracking`：情绪追踪数据
- `behavior_tracking`：行为追踪数据
- `statistics`：统计信息

## 焦虑筛查项目

### 分离焦虑
- 与父母分离时哭泣
- 害怕父母不会回来
- 拒绝上学
- 离开家时出现身体不适症状

### 社交焦虑
- 害怕陌生环境
- 不愿意与他人互动
- 害怕被注视
- 避免社交场合

### 广泛性焦虑
- 过度担忧
- 肌肉紧张
- 睡眠困难
- 容易疲劳

## ADHD 筛查评分标准

| 总分 | 评估结果 |
|-------------|------------|
| <20分 | 不太可能是 ADHD |
| 20-30分 | 可能患有 ADHD，建议进一步评估 |
| >30分 | 高度怀疑患有 ADHD，建议专业评估 |

## 不同年龄段的心理健康重点

### 0-3岁（婴儿期）
- 评估重点：依恋关系、情绪反应、行为模式
- 常见问题：分离焦虑、睡眠问题、喂养问题

### 3-6岁（学龄前）
- 评估重点：情绪表达、社交行为、自我照顾能力
- 常见问题：攻击性行为、恐惧症、语言问题

### 6-12岁（学龄期）
- 评估重点：学习行为、同伴关系、自我意识
- 常见问题：学习困难、ADHD、焦虑

### 12-18岁（青春期）
- 评估重点：情绪管理、自我认同、应对压力
- 常见问题：抑郁、焦虑、行为问题

## 执行说明

1. 读取 `data/profile.json` 文件中的儿童信息
2. 根据年龄和操作类型确定评估项目
3. 生成评估报告
4. 将数据保存到 `data/child-mental-tracker.json` 文件中

## 医疗安全原则

### 安全界限
- 本系统仅用于心理健康记录和筛查参考，不提供精神障碍诊断
- 不推荐使用任何精神药物
- 不提供心理治疗服务
- 不处理危机情况

### 系统功能
- 进行心理健康评估记录
- 提供症状筛查参考
- 追踪情绪变化趋势
- 提供医疗咨询建议

## 重要提示

本系统仅用于心理健康记录和筛查参考，**不能替代专业心理评估和诊断**。

如出现以下情况，请**立即寻求专业帮助**：
- 有伤害自己或他人的想法或行为
- 极端情绪爆发
- 完全不遵守操作说明
- 完全脱离社交环境
- 睡眠或食欲发生严重变化
- 出现幻觉或妄想

如遇紧急情况，请**立即拨打 120 或前往最近的医院**。