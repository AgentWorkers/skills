---
name: copd
description: COPD management - lung function monitoring (FEV1), symptom assessment (CAT, mMRC), exacerbation tracking, and vaccination records
argument-hint: <operation_type+info, e.g.: fev1 1.8 65%, cat score 18, mmrc 2, exacerbation moderate>
allowed-tools: Read, Write
schema: copd/schema.json
---

# 慢性阻塞性肺疾病（COPD）管理技能

慢性阻塞性肺疾病（COPD）的长期管理包括肺功能监测、症状评估以及急性加重的预防。

## 核心流程

```
User Input -> Identify Operation Type -> Extract Parameter Info -> Check Completeness -> [Need Supplement] Ask User
                                                      |
                                                   [Information Complete]
                                                      |
                                              Generate JSON -> Save Data -> Output Confirmation
```

## 第1步：解析用户输入

### 操作类型识别

| 输入关键词 | 操作类型 | 描述 |
|----------------|----------------|-------------|
| fev1, 肺功能 | 肺功能测试记录 |
| cat | 症状评估 | CAT评分 |
| mmrc | mMRC评分 | mMRC呼吸困难评分 |
| 症状 | 症状记录 | 症状记录 |
| 急性加重 | 急性加重记录 | 急性加重记录 |
| 药物 | 药物管理 | 药物管理 |
| 疫苗 | 疫苗接种记录 | 疫苗接种记录 |
| 状态 | 控制状态 | 查看控制状态 |
| 评估 | GOLD分级评估 | GOLD分级评估 |

### 肺功能相关关键词映射

| 输入关键词 | 对应字段 | 例子 |
|----------------|-------|--------|
| fev1, fev | fev1 | 1.8（升） |
| 预测值, 百分比 | fev1_percent_predicted | 65% |
| fvc | fvc | 3.2（升） |
| 比率 | fev1_fvc_ratio | 0.56 |

### 症状类型相关关键词

| 输入关键词 | 症状类型 | ------------------- |
| 呼吸困难 | dyspnea |          |
| 咳嗽 | cough |          |
| 痰液 | sputum |          |
| 喘息 | wheeze |          |

### 痰液颜色相关关键词

| 输入关键词 | 痰液颜色 | ------------------- |
| 白色 | white |          |
| 清澈 | clear |          |
| 黄色 | yellow |          |
| 浓绿色 | green |          |
| 脓性 | purulent |          |

### 痰液量相关关键词

| 输入关键词 | 痰液量 | ------------------- |
| 少量 | scanty |          |
| 中等 | moderate |          |
| 大量 | abundant |          |

### 急性加重的严重程度

| 输入关键词 | 严重程度 | ------------------- |
| 轻微 | mild |          |
| 中度 | moderate |          |
| 重度 | severe |          |

### 急性加重的诱因

| 输入关键词 | 诱因 | ------------------- |
| 病毒感染 | viral_infection |          |
| 细菌感染 | bacterial_infection |          |
| 空气污染 | air_pollution |          |
| 天气变化 | weather_change |          |

## 第2步：检查信息完整性

### 必需的肺功能记录：
- FEV1值（升）

### 必需的CAT评分：
- 总分（0-40分）

### 必需的mMRC评分：
- 评分等级（0-4级）

### 必需的症状记录：
- 症状类型
- 严重程度或描述

### 必需的急性加重记录：
- 严重程度（轻微/中度/重度）

## 第3步：（如有需要）进行交互式提示

### 情景A：肺功能数值不完整
```
Please provide complete lung function data:
- FEV1 value (L)
- FEV1 percent predicted (%)
- FVC value (L) [optional]
- FEV1/FVC ratio [optional]
```

### 情景B：CAT评分缺失
```
Please perform CAT scoring (each item 0-5 points):
1. Cough
2. Sputum
3. Chest tightness
4. Shortness of breath climbing stairs
5. Limitation in housework activities
6. Confidence in outdoor activities
7. Sleep quality
8. Energy level

Or enter total score directly (0-40 points)
```

### 情景C：mMRC评分缺失
```
Please select mMRC grade (0-4):
Grade 0 - Only shortness of breath during strenuous exercise
Grade 1 - Shortness of breath when walking fast or climbing incline
Grade 2 - Walk slower than peers or need to stop to catch breath
Grade 3 - Need to stop after 100m or few minutes
Grade 4 - Severe shortness of breath, cannot leave home
```

## 第4步：生成JSON数据

### 肺功能记录
```json
{
  "date": "2025-06-10",
  "post_bronchodilator": {
    "fev1": 1.8,
    "fev1_percent_predicted": 65,
    "fvc": 3.2,
    "fev1_fvc_ratio": 0.56
  },
  "gold_grade": "Grade 2",
  "interpretation": "Moderate airflow limitation"
}
```

### CAT评分记录
```json
{
  "date": "2025-06-20",
  "total_score": 18,
  "max_score": 40,
  "interpretation": "Moderate symptom impact",
  "impact_level": "Medium",
  "items": {
    "cough": 2,
    "sputum": 2,
    "chest_tightness": 2,
    "breathlessness_climbing": 3,
    "activity_limitation": 2,
    "confidence_outdoors": 2,
    "sleep": 3,
    "energy": 2
  }
}
```

### 急性加重记录
```json
{
  "id": "exace_20250215000000001",
  "date": "2025-02-15",
  "severity": "moderate",
  "triggers": ["viral_infection"],
  "symptoms": ["increased_dyspnea", "purulent_sputum"],
  "treatment": ["antibiotics", "prednisone"],
  "hospitalized": false,
  "recovery_days": 10
}
```

完整的数据库模式定义请参见 [schema.json](schema.json)。

## 第5步：保存数据

1. 读取 `data/copd-tracker.json` 文件
2. 根据操作类型更新相应的数据
3. 更新统计信息
4. 将更新后的数据写回文件

## 执行说明

```
1. Identify operation type (fev1/cat/mmrc/symptom/exacerbation/medication/vaccine/status/assessment)
2. Extract parameter information
3. Check required field completeness
4. If missing, ask user to supplement
5. Generate JSON compliant with schema.json
6. Save to data/copd-tracker.json
7. Output confirmation and medical recommendations
```

## 示例交互

### 示例1：肺功能记录
```
User: fev1 1.8 65%

AI: Lung function test result recorded
FEV1: 1.8 L (65% predicted)
GOLD Grade: Grade 2 (moderate)
Interpretation: Moderate airflow limitation

Recommendation: Regular lung function recheck, at least once a year
```

### 示例2：CAT评分
```
User: cat score 18

AI: CAT score recorded
Total score: 18/40
Impact: Moderate impact
Grade: Medium

Symptom control needs improvement, consult doctor for treatment adjustment
```

### 示例3：急性加重记录
```
User: exacerbation moderate viral_infection

AI: Exacerbation event recorded
Date: 2025-06-20
Severity: Moderate
Trigger: Viral infection

This is the 1st exacerbation this year

If symptoms continue to worsen for more than 3 days, seek medical attention
```

### 示例4：查看控制状态
```
User: copd status

AI: COPD Control Status Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GOLD Grade: Grade 2 (moderate)
Symptom assessment: CAT 18 (moderate impact)
Lung function: FEV1 1.8L (65%)

Exacerbations: 1 this year (last: 2025-02-15)
Medication: Tiotropium 18μg qd
Vaccination: Flu vaccine (2024-10), Pneumonia vaccine (2023-05)

Control Evaluation: Symptom control suboptimal, recommend optimizing treatment
```

更多示例请参见 [examples.md](examples.md)。

## 医疗安全边界

### 不可执行的内容：
- 提供具体的药物剂量调整建议
- 直接开具或推荐特定药物
- 取代医生的诊断和治疗决策
- 预测疾病预后或肺功能下降的速度

### 可执行的内容：
- 提供肺功能监测记录和趋势分析
- 提供症状评分和评估（CAT、mMRC）
- 提供急性加重记录和诱因追踪
- 提供药物提醒和疫苗接种提醒
- 提供生活方式建议和就医提醒

### 紧急医疗指征：
- 呼吸困难显著加重（休息后未见缓解）
- 嘴唇或指甲呈现紫色（发绀）
- 意识混乱、嗜睡或昏迷
- 胸痛，怀疑心肌梗死或气胸