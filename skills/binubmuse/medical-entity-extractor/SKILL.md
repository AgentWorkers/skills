---
name: medical-entity-extractor
description: 从患者信息中提取医疗实体（症状、药物、实验室检测结果、诊断结果）。
license: MIT
metadata:
  author: "NAPSTER AI"
  maintainer: "NAPSTER AI"
  openclaw:
    requires:
      bins: []
---
# 医疗实体提取器

该工具能够从非结构化的患者信息中提取结构化的医疗数据。

## 功能概述

1. **症状提取**：识别症状的名称、严重程度、持续时间以及病情的发展趋势。
2. **药物信息提取**：查找药物的名称、剂量、服用频率以及可能的副作用。
3. **实验室检测结果提取**：解析实验室检测结果、生命体征和各项测量数据。
4. **诊断信息提取**：识别患者所患的疾病或病症。
5. **时间信息提取**：记录症状开始的时间以及持续的时间长度。
6. **待处理事项**：识别患者提出的请求（如预约就诊、续药、咨询问题等）。

## 输入格式

```json
[
  {
    "id": "msg-123",
    "priority_score": 78,
    "priority_bucket": "P1",
    "subject": "Medication side effects",
    "from": "patient@example.com",
    "date": "2026-02-27T10:30:00Z",
    "body": "I've been feeling dizzy since starting the new blood pressure medication (Lisinopril 10mg) three days ago. My BP this morning was 145/92."
  }
]
```

## 输出格式

```json
[
  {
    "id": "msg-123",
    "entities": {
      "symptoms": [
        {
          "name": "dizziness",
          "severity": "moderate",
          "duration": "3 days",
          "onset": "since starting new medication"
        }
      ],
      "medications": [
        {
          "name": "Lisinopril",
          "dosage": "10mg",
          "frequency": null,
          "context": "new medication"
        }
      ],
      "lab_values": [
        {
          "type": "blood_pressure",
          "value": "145/92",
          "unit": "mmHg",
          "timestamp": "this morning"
        }
      ],
      "diagnoses": [
        {
          "name": "hypertension",
          "context": "implied by blood pressure medication"
        }
      ],
      "action_items": [
        {
          "type": "medication_review",
          "reason": "possible side effect (dizziness)"
        }
      ]
    },
    "summary": "Patient reports dizziness after starting Lisinopril 10mg 3 days ago. BP elevated at 145/92. Possible medication side effect requiring review."
  }
]
```

## 实体类型

### 症状
- 症状名称、严重程度（轻微/中度/严重）、持续时间、发病时间、病情发展情况（好转/稳定/恶化）

### 药物
- 药物名称、剂量、服用频率、给药途径、用药状态（新用药/正在使用/已停药）

### 实验室检测结果
- 检测项目类型（血压、血糖、胆固醇等）、检测数值、单位、时间戳、正常范围

### 诊断结果
- 诊断名称、诊断情况（确诊/疑似/排除）

### 生命体征
- 体温、心率、呼吸频率、血氧饱和度、血压

### 待处理事项
- 事项类型（预约就诊、续药、咨询问题）、紧急程度、处理原因

## 医学术语处理能力

该工具能够识别以下内容：
- 常见的医学缩写（如 BP、HR、RR、O2 sat 等）
- 药物的品牌名称和通用名称
- 医学术语的通俗表达（例如 “sugar” 对应 “糖尿病”，“heart attack” 对应 “心肌梗塞”）
- 表示时间范围的短语（如 “since yesterday”（从昨天开始）、“for the past week”（过去一周）

## 集成方式

该工具可通过 OpenClaw 命令行界面（CLI）进行调用：
```bash
openclaw skill run medical-entity-extractor --input '[{"id":"msg-1","priority_score":78,...}]' --json
```

或通过编程方式实现：
```typescript
const result = await execFileAsync('openclaw', [
  'skill', 'run', 'medical-entity-extractor',
  '--input', JSON.stringify(scoredMessages),
  '--json'
]);
```

**推荐模型**：Claude Sonnet 4.5（模型路径：`openclaw models set anthropic/claude-sonnet-4-5`）

## 隐私与安全保障

- 所有数据处理均在本地通过 OpenClaw 完成
- 除用于大型语言模型（LLM）处理的 Claude API 外，不会向任何外部服务传输数据
- 提取的医疗实体信息仅保存在用户本地环境中。