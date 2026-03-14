---
name: protocol-deviation-classifier
description: >
  **功能：**  
  根据 GCP/ICH E6 标准自动对临床试验中的方案偏差进行分类，评估这些偏差对受试者安全、数据完整性和试验科学有效性的影响。  
  **触发条件：**  
  当需要对方案偏差进行分类评估时，输入偏差事件描述或偏差类型。  
  **使用场景：**  
  临床试验质量管理、偏差影响评估、监管文件准备、审核准备。
  or "minor deviation".

  Function: Automatically classify protocol deviations in clinical trials based on
  GCP/ICH E6 standards,

  assessing the impact on subject safety, data integrity, and trial scientific validity.

  Trigger: When classification assessment of protocol deviations is needed, input
  deviation event description or deviation type.

  Use cases: Clinical trial quality management, deviation impact assessment, regulatory
  submission preparation, audit preparation.

  '
version: 1.0.0
category: Pharma
tags:
- clinical-trials
- gcp
- compliance
- deviation
- quality
- ich-e6
- ctm
author: AIPOCH
license: MIT
status: Draft
risk_level: Medium
skill_type: Tool/Script
owner: AIPOCH
reviewer: ''
last_updated: '2026-02-06'
---
# 协议偏差分类器

这是一个基于GCP（Good Clinical Practice）和ICH E6指南的临床试验协议偏差分类工具，能够自动判断偏差属于“重大偏差”还是“轻微偏差”。

## 主要功能

- **自动分类**：根据偏差描述自动判断偏差的严重程度。
- **风险评估**：评估偏差对受试者安全、数据完整性和科学有效性的影响。
- **法规依据**：分类标准符合GCP、ICH E6以及FDA/EMA的指南要求。
- **报告生成**：生成符合监管要求的偏差分类报告。
- **中文支持**：完全支持中文临床试验场景。

## 偏差分类标准

### 重大/关键偏差

可能影响试验数据完整性、受试者安全或试验科学有效性的偏差：

| 类别 | 例子 |
|------|------|
| 知情同意 | 未经受试者同意进行研究程序，使用过期或错误的知情同意书 |
| 入组/排除标准 | 接纳不符合入组标准的受试者，或接纳符合排除标准的受试者 |
| 研究产品 | 过量给药，使用禁忌药物，给药途径错误，随机化错误 |
| 安全性 | 未按照协议要求进行安全性监测，遗漏严重不良事件（SAE）/疑似严重不良事件（SUSAR）报告，报告延迟 |
| 盲法设置 | 未经授权的人员解盲，未记录紧急解盲程序 |
| 数据完整性 | 伪造数据，系统性遗漏关键数据 |
| 禁止的操作 | 违反试验协议的关键操作程序，未进行关键疗效评估 |

### 轻微偏差

不太可能影响试验数据完整性、受试者安全或试验科学有效性的偏差：

| 类别 | 例子 |
|------|------|
| 访问时间 | 访问时间略有超出规定范围（例如，几天内），非关键访问的延迟 |
| 样本采集 | 非关键样本采集的时间轻微偏差，样本处理略有延迟 |
| 问卷填写 | 生活质量问卷/日记卡提交延迟几天 |
| 数据记录 | 非关键数据记录的延迟，拼写/格式错误 |
| 程序执行 | 二次程序执行顺序的调整，遗漏了非关键评估（例如身高测量） |
| 文档记录 | 来源文件签名延迟，遗漏了次要文件（例如非关键检查报告） |

## 使用方法

### Python API

```python
from scripts.main import DeviationClassifier

# Initialize classifier
classifier = DeviationClassifier()

# Classify single deviation
result = classifier.classify(
    description="Subject visit delayed by 2 days",
    deviation_type="Visit Window"
)
print(result.classification)  # "Minor Deviation"
print(result.confidence)      # 0.92
print(result.rationale)       # Classification rationale explanation

# Batch classification
deviations = [
    {"description": "Blood sample collected without informed consent", "type": "Informed Consent"},
    {"description": "Quality of life questionnaire submitted 3 days late", "type": "Data Collection"}
]
batch_results = classifier.classify_batch(deviations)

# Generate report
report = classifier.generate_report(batch_results)
```

### 命令行界面（CLI）使用方法

```bash
# Classify single deviation
python scripts/main.py classify --description "Subject visit delayed by 2 days" --type "Visit Window"

# Batch classification from file
python scripts/main.py batch --input deviations.json --output report.json

# Interactive classification
python scripts/main.py interactive

# Assess deviation impact
python scripts/main.py assess \
  --description "Subject accidentally took double dose of investigational drug" \
  --safety-impact high \
  --data-impact medium \
  --scientific-impact medium
```

### 输入格式

**JSON输入文件格式：**

```json
[
  {
    "id": "DEV-001",
    "description": "Subject visit delayed by 2 days",
    "type": "Visit Window",
    "occurrence_date": "2024-01-15",
    "severity_factors": {
      "safety_impact": "none",
      "data_impact": "low",
      "scientific_impact": "low"
    }
  },
  {
    "id": "DEV-002",
    "description": "Blood collection performed without informed consent",
    "type": "Informed Consent",
    "severity_factors": {
      "safety_impact": "high",
      "data_impact": "high",
      "scientific_impact": "high"
    }
  }
]
```

### 输出格式

**分类结果：**

```json
{
  "id": "DEV-001",
  "classification": "Minor Deviation",
  "classification_en": "Minor Deviation",
  "confidence": 0.92,
  "rationale": "Visit time window slightly delayed (2 days), does not affect subject safety, data integrity, or trial scientific validity.",
  "risk_factors": {
    "safety_risk": "none",
    "data_integrity_risk": "low",
    "scientific_validity_risk": "none"
  },
  "regulatory_basis": [
    "ICH E6(R2) Section 4.5",
    "GCP Section 6.4.4"
  ],
  "recommended_actions": [
    "Document in file",
    "Track trends"
  ]
}
```

## 分类算法

分类依据以下评估维度：

1. **受试者安全影响**：
   - 无：无影响
   - 低：轻微影响
   - 中等：中等影响
   - 高：严重影响

2. **数据完整性影响**：
   - 无：无影响
   - 低：对非关键数据有轻微影响
   - 中等：对关键数据有部分影响
   - 高：对关键数据造成严重损害

3. **试验科学有效性影响**：
   - 无：无影响
   - 低：对统计功效有轻微影响
   - 中等：可能影响主要终点
   - 高：严重影响试验结论

**分类规则**：
- 任何维度为“高” → 重大偏差
- 安全维度为“中等”且数据/科学维度中任意一个为“中等以上” → 重大偏差
- 其他情况 → 轻微偏差

## 法规依据

- ICH E6(R2) 良好临床实践指南
- ICH E6(R3) 良好临床实践指南（草案）
- FDA 21 CFR Part 312（IND法规）
- FDA针对行业的指导：临床试验监管
- EMA关于基于风险的质量管理指南
- NMPA药物临床试验良好临床实践指南

## 依赖项

- Python 3.8及以上版本
- 无第三方依赖项（纯Python标准库实现）

## 注意事项

1. 该工具提供分类建议，最终决定需由临床质量保证人员确认。
2. 严重/关键偏差必须立即报告给申办方和伦理委员会。
3. 建议定期审查偏差趋势并实施纠正和预防措施（CAPA）。
4. 分类标准可能因监管机构、试验类型和协议要求而有所不同。

## 风险评估

| 风险指标 | 评估内容 | 风险等级 |
|----------------|------------|-------|
| 代码执行 | 在本地执行的Python/R脚本 | 中等 |
| 网络访问 | 无外部API调用 | 低 |
| 文件系统访问 | 读取输入文件，写入输出文件 | 中等 |
| 指令篡改 | 遵循标准提示指南 | 低 |
| 数据泄露 | 输出文件保存在工作区 | 低 |

## 安全性检查清单

- [ ] 无硬编码的凭证或API密钥
- [ ] 无未经授权的文件系统访问
- [ ] 输出不暴露敏感信息
- [ ] 有防止注入攻击的措施
- [ ] 输入文件路径经过验证（防止路径遍历）
- [ ] 输出目录限制在工作区内
- [ ] 脚本在沙箱环境中执行
- [ ] 错误信息经过处理（不暴露堆栈跟踪）
- [ ] 依赖项经过审核

## 先决条件

```bash
# Python dependencies
pip install -r requirements.txt
```

## 评估标准

### 成功指标
- [ ] 成功执行主要功能
- [ ] 输出符合质量标准
- [ ] 良好处理边缘情况
- [ ] 性能可接受

### 测试用例
1. **基本功能**：标准输入 → 预期输出
2. **边缘情况**：无效输入 → 良好的错误处理
3. **性能**：处理大型数据集时性能可接受

## 生命周期状态

- **当前阶段**：草案阶段
- **下一次审查日期**：2026-03-06
- **已知问题**：无
- **计划中的改进**：
  - 性能优化
  - 增加更多功能支持