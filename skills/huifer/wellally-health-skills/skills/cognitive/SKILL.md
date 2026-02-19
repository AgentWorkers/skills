---
name: cognitive
description: Cognitive function assessment tracking for elderly - MMSE/MoCA tests, cognitive domain evaluation, ADL/IADL assessment, and risk monitoring
argument-hint: <operation_type+info, e.g.: mmse score 27, moca 24, domain memory mild_impairment, adl independent>
allowed-tools: Read, Write
schema: cognitive/schema.json
---

# 认知功能评估技能

该技能用于管理老年人的认知功能评估，包括MMSE（简易精神状态检查）、MoCA（蒙特利尔认知评估）测试、认知领域评估以及日常生活能力（ADL）评估。

## 核心流程

```
User Input -> Identify Operation Type -> Extract Parameter Info -> Check Completeness -> [Need Supplement] Ask User
                                                      |
                                                   [Information Complete]
                                                      |
                                              Generate JSON -> Save Data -> Output Confirmation
```

## 第一步：解析用户输入

### 操作类型识别

| 输入关键词 | 操作类型 | 描述 |
|----------------|----------------|-------------|
| mmse | mmse_test | 进行MMSE测试 |
| moca | moca_test | 进行MoCA测试 |
| domain | cognitive_domain | 进行认知领域评估 |
| adl | adl_assessment | 进行日常生活能力评估 |
| iadl | iadl_assessment | 进行工具性日常生活能力评估 |
| status | cognitive_status | 查看认知状态 |
| trend | trend_analysis | 查看认知功能变化趋势 |
| risk | risk_assessment | 进行认知功能风险评估 |

### 认知领域关键词映射

| 输入关键词 | 领域名称 | |
|----------------|--------------|
| memory | 记忆 |
| executive | 执行功能 |
| language | 语言能力 |
| visuospatial | 视空间能力 |

### 功能状态关键词映射

| 输入关键词 | 状态值 | |
| normal | 正常 |
| mild | 轻度损伤 |
| moderate | 中度损伤 |
| severe | 重度损伤 |
| independent | 独立 |
| needs_assistance | 需要协助 |
| dependent | 需要他人照顾 |
| supervision_needed | 需要监督 |

### 日常生活能力（ADL）相关关键词

| 输入关键词 | 项目名称 | |
| bathing | 洗澡 |
| dressing | 穿衣 |
| toileting | 如厕 |
| transferring | 移动 |
| continence | 大小便控制 |
| feeding | 进食 |

### 工具性日常生活能力（IADL）相关关键词

| 输入关键词 | 项目名称 | |
| shopping | 购物 |
| cooking | 烹饪 |
| managing_medications | 用药管理 |
| using_telephone | 使用电话 |
| managing_finances | 财务管理 |
| housekeeping | 家务管理 |
| transportation | 交通出行 |
| laundry | 洗衣 |

## 第二步：检查信息完整性

### MMSE测试所需信息：
- 总分（0-30分）

### MoCA测试所需信息：
- 总分（0-30分）
- 教育水平（可选，用于分数调整）

### 认知领域评估所需信息：
- 评估领域（记忆/执行功能/语言能力/视空间能力）
- 功能状态（正常/轻度损伤/中度损伤/重度损伤）

### 日常生活能力/工具性日常生活能力评估所需信息：
- 项目名称
- 功能状态

## 第三步：（如有需要）进行交互式提示

### 情景A：缺少MMSE/MoCA测试结果
```
Please provide test total score (0-30 points)
```

### 情景B：缺少认知领域评估信息
```
Please specify the cognitive domain to assess:
- memory (memory)
- executive (executive function)
- language (language ability)
- visuospatial (visuospatial ability)

What is the function status?
- normal (normal)
- mild_impairment (mild impairment)
- moderate_impairment (moderate impairment)
- severe_impairment (severe impairment)
```

### 情景C：缺少日常生活能力/工具性日常生活能力评估项目信息
```
Please provide specific activity items and function status
```

## 第四步：生成JSON格式的数据

### MMSE测试记录
```json
{
  "test_type": "mmse",
  "date": "2025-06-20",
  "total_score": 27,
  "max_score": 30,
  "interpretation": "Normal",
  "items": {
    "orientation": 10,
    "registration": 3,
    "attention": 5,
    "recall": 3,
    "language": 6
  }
}
```

### MoCA测试记录
```json
{
  "test_type": "moca",
  "date": "2025-06-20",
  "total_score": 24,
  "adjusted_score": 25,
  "education_years": 12,
  "max_score": 30,
  "interpretation": "Mild Cognitive Impairment"
}
```

### 认知领域评估记录
```json
{
  "domain": "memory",
  "status": "mild_impairment",
  "assessment_date": "2025-06-20",
  "notes": "Short-term memory impaired, long-term memory preserved"
}
```

### 日常生活能力评估记录
```json
{
  "activity": "bathing",
  "status": "independent",
  "assessment_date": "2025-06-20"
}
```

完整的架构定义请参见[schema.json](schema.json)。

## 第五步：保存数据

1. 读取`data/cognitive-assessment.json`文件
2. 根据操作类型更新相应数据
3. 更新统计信息
4. 将更新后的数据写回文件

## 执行说明

```
1. Identify operation type (mmse/moca/domain/adl/iadl/status/trend/risk)
2. Extract parameter information (scores, cognitive domains, function status, etc.)
3. Check required field completeness
4. If missing, ask user to supplement
5. Generate JSON compliant with schema.json
6. Save to data/cognitive-assessment.json
7. Output confirmation and interpretation results
```

## 示例交互

### 示例1：进行MMSE测试
```
User: mmse score 27

AI: MMSE test result recorded
Total score: 27/30
Interpretation: Normal
Next assessment: 2026-06-20
```

### 示例2：进行认知领域评估
```
User: domain memory mild_impairment

AI: Cognitive domain assessment recorded
Cognitive domain: Memory (memory)
Status: Mild impairment (mild_impairment)

Currently impaired cognitive domain: Memory
```

### 示例3：进行日常生活能力评估
```
User: adl independent

AI: ADL assessment result recorded
All 6 basic activities: Independent
Dependency level: No dependency
```

### 示例4：查看认知状态
```
User: cognitive status

AI: Cognitive Function Status Report
━━━━━━━━━━━━━━━━━━━━━━━━
Latest MMSE: 27/30 (Normal) - 2025-06-20
Latest MoCA: 24/30 (Mild impairment) - 2025-06-15

Cognitive domain status:
- Memory: Mild impairment
- Executive function: Normal
- Language: Normal
- Visuospatial: Normal

Daily function:
- ADL: Independent
- IADL: Needs assistance (2 items)
```

更多示例请参见[examples.md](examples.md)。

## 医疗安全边界

### 不可执行的内容：
- 诊断认知障碍或痴呆症
- 替代神经科医生/老年病专家的专业评估
- 提供具体的药物治疗方案

### 可执行的内容：
- 进行认知功能筛查（MMSE/MoCA）
- 跟踪认知功能下降趋势
- 进行日常生活能力（ADL/IADL）评估
- 进行认知领域功能评估
- 提供风险预警和就医建议

### 医疗建议：
- 如果出现以下情况，请及时就医：
- MMSE评分 ≤ 26分
- MoCA评分 ≤ 25分
- 多个认知领域受损
- 日常生活能力/工具性日常生活能力下降
- 认知功能迅速下降