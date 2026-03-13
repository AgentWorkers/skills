---
name: gene2ai
description: 这是专为AI代理设计的个人健康数据管理平台。您可以查询基因组相关信息、上传医疗文件、记录日常健康指标、查看基因组数据与实验室检测结果的关联信息、接收个性化的每日健康报告，并在日常对话中获得与您的基因和临床数据相关的健康建议——所有这些功能都基于您真实的基因和临床数据来实现。
version: 3.3.1
metadata:
  openclaw:
    requires:
      env:
        - GENE2AI_API_KEY
    primaryEnv: GENE2AI_API_KEY
    emoji: "🧬"
    homepage: https://gene2.ai/guide
---
# Gene2AI — 为您的健康数据提供AI建议

您可以通过Gene2AI平台访问用户的个人健康数据，这些数据包括：

- **基因组数据**：来自23andMe、AncestryDNA、WeGene等原始基因检测文件的324多个指标——涵盖9个类别中的273个基因的933个SNP
- **健康文档**：实验室报告、体检结果、医疗记录和影像报告——由AI解析为结构化的指标
- **用户自报的指标**：血压、血糖、体重、心率等日常测量数据
- **交叉参考**：实验室指标与基因组标记之间的双向链接（例如，LDL-C与胆固醇基因）

## 何时使用此技能

在用户以下情况下使用此技能：

### 基因组数据查询
- 询问他们的**遗传健康风险**（例如：“我有患2型糖尿病的风险吗？”、“阿尔茨海默病的风险呢？”）
- 询问**药物反应**或药物基因组学（例如：“我如何代谢咖啡因？”、“我对华法林敏感吗？”）
- 询问**CYP450代谢器状态**（例如：“我的CYP2D6状态如何？”、“我是代谢缓慢的吗？”）
- 询问**HLA等位基因**（例如：“我携带HLA-B*57:01吗？”、“我有药物过敏的风险吗？”）
- 询问**APOE基因型**（例如：“我的APOE状态如何？”、“我有ε4等位基因吗？”）
- 询问**营养**和营养基因组学（例如：“我需要更多的维生素D吗？”、“我乳糖不耐受吗？”）
- 询问**身体特征**（例如：“我的DNA显示我的肌肉类型是什么？”）
- 询问**祖先构成**
- 希望根据他们的基因获得**个性化建议**
- 提到他们的**DNA**、**基因**、**SNP**或**基因变异**

### 健康数据管理
- 发送健康相关文档（实验室报告、体检结果、医疗记录、处方、影像报告）
- 询问上传、保存或记录健康数据
- 口头报告健康指标（血压、血糖、体重、心率等）
- 询问他们的健康数据状态或摘要
- 说诸如“帮我保存这份体检报告”、“把这个上传到我的健康档案”或“记录一下我的血压”之类的话

### 交叉参考查询
- 询问实验室指标与基因组标记之间的关联（例如：“我的LDL很高——我有遗传风险因素吗？”）
- 希望获得结合基因组和实验室数据的全面风险概览
- 询问全面的健康评估

### 上下文相关的健康建议（被动式——始终开启）

- 对话涉及**药物、补充剂或药品**时——在回应前检查CYP450代谢器状态和药物敏感性
- 对话涉及**饮食、营养或食物选择**时——检查营养标志和相关基因标记
- 对话涉及**锻炼、健身或运动**时——检查特征标记（肌肉类型、耐力风险）
- 对话涉及**旅行、海拔或气候**时——检查相关的基因适应
- 对话涉及**睡眠、疲劳或能量**时——检查咖啡因代谢和昼夜节律标记
- 对话涉及**压力或心理健康**时——检查相关的风险标记
- 对话涉及**家庭计划或怀孕**时——检查携带者状态标记
- 对话涉及**医疗预约或检测结果**时——与基因组数据交叉参考

> **工作原理**：当对话自然涉及健康相关话题时，您可以引用用户的健康档案来提供个性化建议。**首次使用时**，请询问用户的许可：“我可以访问您的Gene2AI健康档案——在讨论健康话题时，您希望我参考您的遗传和临床数据吗？”用户确认后，在同一会话中的未来健康相关对话中，您可以主动引用他们的档案，无需再次询问。如果用户拒绝，只有在用户明确请求时才使用Gene2AI数据。

### 每日健康简报（主动式——定期）

- 用户请求设置每日健康检查或简报
- 定期的cron作业会触发每日简报（见下文第7部分）
- 用户通过每日指标回应健康检查

## 配置

用户的Gene2AI API密钥作为环境变量`GENE2AI_API_KEY`提供。

API密钥是**按档案划分的**——每个密钥绑定到特定的健康档案（例如，“Self”、“Mom”、“Dad”）。使用此密钥时，所有数据查询将自动返回仅属于该档案的数据。这可以防止意外混合家庭成员的健康数据。

> **重要提示**：每个密钥仅适用于一个档案。如果用户为多个家庭成员管理健康数据，应为每个档案生成单独的密钥。`?profileId=`查询参数可以覆盖密钥的默认档案，用于高级用例。

如果`GENE2AI_API_KEY`未设置，请指导用户：
1. 访问https://gene2.ai并登录（或创建账户）
2. 前往**API Keys**页面（https://gene2.ai/api-keys）
3. 点击**Generate New Key**并选择此密钥应访问的健康档案
4. 复制生成的令牌并在OpenClaw中配置它：

```json
{
  "skills": {
    "entries": {
      "gene2ai": {
        "enabled": true,
        "apiKey": "<paste-your-token-here>"
      }
    }
  }
}
```

---

## 第1部分：查询健康数据

### 健康档案（推荐的首次调用）

```bash
curl -s "https://gene2.ai/api/v1/health-data/profile" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

返回一个**简洁的、仅包含结论的健康档案**（约2-4KB）。这是任何代理会话的首次推荐调用。响应包含：
- **APOE基因型**结论（例如，“APOE ε3/ε4 — 风险增加”）
- 每个基因的**CYP450代谢器状态**（例如，“CYP2D6：正常代谢器”）及其影响的药物
- **HLA携带者状态**（仅显示阳性等位基因）
- **升高的健康风险**（状况 + 风险级别 + 简短说明，不包含原始SNP）
- **药物敏感性**（药物 + 敏感性级别）
- **营养标志**（来自基因变异的营养问题）
- **异常的实验室/体检指标**（仅显示最新值：名称、值、单位、标志）
- **医疗发现**——所有检查结果（CT、超声波、X光、MRI、ECG、体检、功能测试等），按类别分组，包括正常和异常发现，保留原始语言
- **医疗发现摘要**——每个类别的总数和异常数量
- **建议关注的重点领域**（通过交叉参考基因组 + 临床 + 影像数据自动生成）

```json
{
  "_format": "gene2ai-health-profile-v1",
  "_description": "Compact health profile from Gene2AI. Contains interpretive conclusions only.",
  "dataCoverage": { "genomicMarkers": 324, "labIndicators": 247, "medicalFindings": 18, ... },
  "genomicHighlights": {
    "apoe": "APOE ε3/ε4 — Increased (1 copy of ε4)",
    "cyp450": [{ "gene": "CYP2D6", "status": "Normal Metabolizer", "affectedDrugs": [] }],
    "elevatedRisks": [{ "condition": "Alzheimer's Disease", "risk": "elevated", "note": "..." }],
    "drugSensitivities": [{ "drug": "Warfarin", "sensitivity": "increased", "note": "..." }],
    "nutritionFlags": [{ "nutrient": "Vitamin D", "note": "..." }]
  },
  "abnormalIndicators": [{ "name": "LDL Cholesterol", "value": 3.8, "unit": "mmol/L", "flag": "high" }],
  "medicalFindings": {
    "imaging": [
      { "type": "imaging", "examType": "CT", "bodyPart": "Liver", "finding": "肝脏密度减低", "conclusion": "Mild fatty liver", "severity": "mild", "clinicalSignificance": "Common finding", "recommendation": "Lifestyle modification", "date": "2026-01-15" },
      { "type": "imaging", "examType": "Ultrasound", "bodyPart": "Thyroid", "finding": "右叶小结节", "conclusion": "Thyroid nodule, likely benign", "severity": "mild", "recommendation": "Follow-up in 12 months", "date": "2026-01-15" }
    ],
    "physical_exam": [
      { "type": "physical_exam", "examType": "General", "bodyPart": "Heart", "finding": "心律齐，无杂音", "conclusion": "Normal cardiac exam", "severity": "normal", "date": "2026-01-15" }
    ],
    "functional_test": [
      { "type": "functional_test", "examType": "ECG", "bodyPart": "Heart", "finding": "窦性心律", "conclusion": "Normal ECG", "severity": "normal", "date": "2026-01-15" }
    ]
  },
  "medicalFindingsSummary": {
    "total": 18, "abnormal": 4,
    "byCategory": {
      "imaging": { "total": 8, "abnormal": 3 },
      "physical_exam": { "total": 6, "abnormal": 0 },
      "functional_test": { "total": 4, "abnormal": 1 }
    }
  },
  "suggestedFocusAreas": ["Alzheimer's risk management (APOE ε4 carrier)", ...]
}
```

> **此档案设计为可缓存并在对话中重复使用。**它不包含原始基因数据（没有rs-IDs、基因型或SNP详细信息），因此适合代理内存和跨会话引用。医疗发现包括所有检查结果（正常和异常），按类别分组，并按日期排序（最新优先）。`finding`字段保留了医疗报告的原始语言（中文或英文）。当用户需要具体的基因详细信息时，可以使用以下端点进行深入查询。

### 摘要概述

```bash
curl -s "https://gene2.ai/api/v1/health-data/summary" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

返回总文档数、总记录数以及按类别和基因组子类别的细分。

### 完整记录（带过滤）

```bash
# All records
curl -s "https://gene2.ai/api/v1/health-data/full" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"

# Filter by category
curl -s "https://gene2.ai/api/v1/health-data/full?category=genomic" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"

# Filter by subcategory (genomic only)
curl -s "https://gene2.ai/api/v1/health-data/full?category=genomic&subcategory=cyp450" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"

# Grouped format (organized by category → subcategory)
curl -s "https://gene2.ai/api/v1/health-data/full?category=genomic&format=grouped" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

**查询参数**：

| 参数 | 值 | 描述 |
|-----------|--------|-------------|
| `category` | `genomic`、`lab_result`、`checkup`、`self_reported`、`medical_record`、`imaging` | 按数据类别过滤 |
| `subcategory` | `health_risk`、`drug_response`、`trait`、`nutrition`、`ancestry`、`apoe`、`hla`、`cyp450` | 按基因组子类别过滤 |
| `format` | `grouped` | 按类别 → 子类别层次结构组织记录 |

### 增量变化（用于同步）

```bash
curl -s "https://gene2.ai/api/v1/health-data/delta?since_version={version_number}" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

---

## 第2部分：基因组数据类别

基因组数据分为9个子类别。使用`?category=genomic`查询时，每条记录都包含一个`data`字段，其中包含解析后的结构化对象（无需手动解析`valueText` JSON）。

### health_risk（193个标记）

按状况/基因分组的疾病风险评估（CFTR、LDLR、阿尔茨海默病、CAD、T2D等）

```json
{
  "indicatorName": "Alzheimer's Disease",
  "indicatorCode": "alzheimers_disease_rs429358",
  "subcategory": "health_risk",
  "valueText": "{...}",
  "data": {
    "condition": "Alzheimer's Disease",
    "risk": "elevated",
    "confidence": "high",
    "description": "Variant associated with increased risk",
    "snps": ["rs429358"],
    "genotype": "CT",
    "populationNote": "Found in ~15% of European populations"
  }
}
```

**风险级别**：`low`、`average`、`slightly_elevated`、`elevated`、`high`

### drug_response（61个标记）

针对华法林、氯吡格雷、SSRIs、可待因、他莫昔芬等的药物基因组学预测（PharmGKB + CPIC）

```json
{
  "indicatorName": "Warfarin Sensitivity",
  "subcategory": "drug_response",
  "data": {
    "drug": "Warfarin",
    "gene": "VKORC1",
    "sensitivity": "increased",
    "recommendation": "Consider lower initial dose",
    "confidence": "high",
    "snps": ["rs9923231"]
  }
}
```

### cyp450（3个基因：CYP2C19、CYP2D6、CYP2C9）

CYP450代谢器表型分析，附带CPIC星形等位基因定义和特定药物建议。

```json
{
  "indicatorName": "CYP2D6",
  "subcategory": "cyp450",
  "data": {
    "metabolizerStatus": "Normal Metabolizer",
    "activityScore": "2.0",
    "allele1": "*1",
    "allele2": "*2",
    "drugRecommendations": [
      {
        "drug": "Codeine",
        "recommendation": "Use label-recommended age- or weight-specific dosing",
        "evidence": "Strong (CPIC)"
      },
      {
        "drug": "Tamoxifen",
        "recommendation": "Use tamoxifen at standard dosing",
        "evidence": "Strong (CPIC)"
      }
    ],
    "limitations": "Star allele calling based on common variants only",
    "methodology": "CPIC star allele definitions"
  }
}
```

**代谢器状态**：`Ultrarapid Metabolizer`、`Normal Metabolizer`、`Intermediate Metabolizer`、`Poor Metabolizer`

### hla（9个等位基因）

通过标签SNP推断的HLA等位基因分型，用于免疫相关状况和药物过敏。

```json
{
  "indicatorName": "HLA-B*57:01",
  "subcategory": "hla",
  "data": {
    "allele": "HLA-B*57:01",
    "carrierStatus": "Negative",
    "associations": [
      {
        "drug": "Abacavir",
        "name": "Abacavir Hypersensitivity",
        "evidence": "Strong (CPIC)",
        "recommendation": "Standard abacavir use is appropriate"
      }
    ]
  }
}
```

### apoe（1条记录）

APOE基因分型——ε2/ε3/ε4等位基因，用于评估阿尔茨海默病和心血管风险。

```json
{
  "indicatorName": "APOE Genotype",
  "subcategory": "apoe",
  "data": {
    "alleles": ["ε3", "ε4"],
    "alzheimerRisk": "Increased (1 copy of ε4)",
    "cardiovascularNote": "ε4 associated with higher LDL cholesterol levels",
    "snps": {
      "rs429358": { "genotype": "CT", "chromosome": "19" },
      "rs7412": { "genotype": "CC", "chromosome": "19" }
    }
  }
}
```

### trait（21个标记）

基因特征预测：头发颜色、皮肤色素沉着、咖啡因代谢、酒精耐受性、肌肉纤维类型。

### nutrition（32个标记）

营养基因组学：基于基因变异的维生素D、叶酸/MTHFR、B12、Omega-3、铁、钙的需求。

### ancestry（4个区域）

来自特定人群变异分析的区域祖先百分比。

```json
{
  "indicatorName": "East Asian",
  "subcategory": "ancestry",
  "data": {
    "region": "East Asian",
    "percentage": 95.2
  }
}
```

---

## 第3部分：风险概览与交叉参考

### 风险概览（综合仪表板）

```bash
curl -s "https://gene2.ai/api/v1/health-data/risk-overview" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

返回一个结合基因组和实验室数据的综合风险仪表板：

```json
{
  "genomic": {
    "totalIndicators": 324,
    "elevatedRisks": [
      {
        "indicatorName": "Alzheimer's Disease",
        "subcategory": "health_risk",
        "risk": "elevated",
        "snps": ["rs429358"],
        "genotype": "CT"
      }
    ],
    "subcategoryCounts": {
      "health_risk": 193,
      "drug_response": 61,
      "nutrition": 32,
      "trait": 21,
      "hla": 9,
      "ancestry": 4,
      "cyp450": 3,
      "apoe": 1
    }
  },
  "lab": {
    "totalIndicators": 247,
    "abnormalIndicators": [
      {
        "indicatorName": "LDL Cholesterol",
        "indicatorCode": "LDL-C",
        "valueNumeric": 3.8,
        "valueUnit": "mmol/L",
        "abnormalFlag": "high",
        "refRangeHigh": 3.4
      }
    ]
  },
  "crossReferences": [
    {
      "labIndicator": {
        "code": "LDL-C",
        "name": "LDL Cholesterol",
        "latestValue": 3.8,
        "unit": "mmol/L",
        "abnormalFlag": "high"
      },
      "relatedGenomicCount": 12,
      "conditions": ["Familial Hypercholesterolemia", "Coronary Artery Disease"]
    }
  ]
}
```

### 实验室指标的基因组链接

```bash
# Find genomic markers related to LDL cholesterol
curl -s "https://gene2.ai/api/v1/health-data/genomic-links/LDL-C" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

**支持的指标代码**：TC、TG、LDL-C、HDL-C、SBP、DBP、FBG、HbA1c、BMI、UA、TSH、FT3、FT4、ALT、AST、GGT、ALP、TBIL、SCr、BUN、WBC、HGB、PLT、CRP

返回与该实验室指标相关的基因组记录，以便进行交叉参考（例如，“您的LDL很高，并且您在LDLR中有与家族性高胆固醇相关的基因变异”）。

### 实验室-基因组摘要

```bash
curl -s "https://gene2.ai/api/v1/health-data/lab-genomic-summary" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

返回所有实验室指标及其相关的基因组记录数量，用于构建交叉参考仪表板。

---

## 第4部分：按作业ID查询基因组数据（旧版本）

为了向后兼容，您也可以通过作业ID查询基因组数据：

```bash
curl -s -X GET "https://gene2.ai/api/v1/genomics/${GENE2AI_JOB_ID}" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

如果`GENE2AI_JOB_ID`未设置，请询问用户的作业ID（在https://gene2.ai/my-jobs页面上可见）。

> **注意**： `/health-data/full?category=genomic`端点（第1部分）是首选，因为它返回了丰富且已解析的数据，并支持过滤/分组。

---

## 第5部分：上传健康文档

当用户发送文件（图像或PDF）且看起来是健康文档时：

### 第1步：与用户确认

在上传之前始终请求确认：“我将把这个上传到您的Gene2AI健康数据档案进行AI分析。系统将自动提取所有健康指标。继续吗？”

### 第2步：确定文档类别

- `lab_result` — 血液测试、尿液测试、生化面板
- `checkup` — 年度体检报告
- `medical_record` — 医生访问笔记、诊断结果
- `imaging` — X光、CT、MRI、超声波报告

### 第3步：上传文件

```bash
curl -s -X POST "https://gene2.ai/api/v1/health-data/upload" \
  -H "Authorization: Bearer $GENE2AI_API_KEY" \
  -F "file=@{filepath}" \
  -F "source=openclaw" \
  -F "category={detected_category}" \
  -F "documentDate={date_if_known_YYYY-MM-DD}" \
  -F "title={brief_description}"
```

响应将包含一个文档ID和状态“parsing”。保存文档ID。

### 第4步：检查解析状态

等待15秒，然后检查：

```bash
curl -s "https://gene2.ai/api/v1/health-data/doc/{doc_id}" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

### 第5步：报告结果

- **如果状态是“completed”**：显示提取的指标数量，突出显示任何异常发现（`abnormalFlag` = “high”、“low”、“critical_high”、“critical_low”或“abnormal”），并列出检测到的机构和文档类型。
- **如果状态是“parsing”**：告诉用户解析仍在进行中。他们可以在https://gene2.ai/health-data稍后查看，或者让您稍后再检查。
- **如果状态是“failed”**：报告`parseError`消息，并建议直接在https://gene2.ai/health-data上传。

---

## 第6部分：提交结构化健康指标

当用户口头报告健康指标时（例如，“我的血压是125/82”，“血糖5.8”，“体重72kg”）：

### 常见指标和参考范围

| 指标 | 中文 | 单位 | 正常范围 |
|-----------|---------|------|-------------|
| 收缩压 | 收缩压 | mmHg | 90-140 |
| 舒张压 | 舒张压 | mmHg | 60-90 |
| 心率 | 心率 | bpm | 60-100 |
| 空腹血糖 | 空腹血糖 | mmol/L | 3.9-6.1 |
| 体温 | 体温 | °C | 36.1-37.2 |
| 体重 | 体重 | kg | — |
| 身高 | 身高 | cm | — |
| BMI | 体质指数 | kg/m² | 18.5-24.9 |
| 血氧饱和度 | 血氧饱和度 | % | 95-100 |

### 确定异常Flag

- `"normal"` — 在参考范围内
- `"high"` — 高于参考范围
- `"low"` — 低于参考范围
- `"critical_high"` — 危险地高（例如，SBP > 180）
- `"critical_low"` — 危险地低（例如，血糖 < 2.8）

### 提交数据

```bash
curl -s -X POST "https://gene2.ai/api/v1/health-data/records" \
  -H "Authorization: Bearer $GENE2AI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "self_reported",
    "title": "{brief_description}",
    "documentDate": "{today_YYYY-MM-DD}",
    "source": "openclaw",
    "records": [
      {
        "indicatorName": "{english_name}",
        "indicatorNameZh": "{chinese_name}",
        "valueNumeric": {numeric_value},
        "valueUnit": "{unit}",
        "refRangeLow": {low_bound_or_null},
        "refRangeHigh": {high_bound_or_null},
        "abnormalFlag": "{flag}"
      }
    ]
  }'
```

向用户确认数据已保存，并提及任何异常值。

---

## 错误处理

| HTTP状态 | 错误代码 | 含义 |
|---|---|---|
| 401 | `missing_token` | 未设置授权头——检查`GENE2AI_API_KEY`是否已设置 |
| 401 | `invalid_token` | API密钥格式错误或无效 |
| 403 | `token_expired` | API密钥已过期（30天限制）——用户需要在https://gene2.ai/api-keys重新生成 |
| 403 | `key_revoked` | API密钥已被手动撤销 |
| 403 | `job_id_mismatch` | 密钥未授权用于此作业ID（密钥仅限作业使用） |
| 404 | `job_not_found` | 作业ID不存在 |
| 404 | `data_not_available` | 分析尚未完成 |

如果收到`token_expired`或`key_revoked`错误，请指导用户访问https://gene2.ai/api-keys生成新的API密钥。

---

## 建议的代理查询策略

### 数据层级

Gene2AI将健康数据分为三个层级，以便代理高效使用：

| 层级 | 端点 | 大小 | 包含内容 | 持久性 |
|------|----------|------|----------|-------------|
| **层级1：健康档案** | `/health-data/profile` | ~2-4KB | 仅包含结论（风险级别、代谢器状态、异常标志） | **跨会话缓存和重复使用** |
| **层级2：详细记录** | `/health-data/full`、`/health-data/risk-overview` | ~50-500KB | 特定基因型、SNP、实验室值、交叉参考 | 每次会话使用，不持久 |
| **层级3：原始数据** | 仅限网站（gene2.ai） | MB+ | 原始基因文件、完整分析JSON | 从不进入代理上下文 |

### 建议的流程

1. **从健康档案开始**：调用 `/health-data/profile`以获取简洁的概览。这对于大多数健康相关决策（饮食、锻炼、一般健康问题）已经足够。**在代理内存中缓存此档案**以供跨会话参考。
2. **仅在需要时深入查询**：当用户提出具体问题时（例如，“我的CYP2D6基因型到底是什么？”、“显示我的APOE SNP”），调用 `/health-data/full?category=genomic&subcategory=cyp450`以获取详细记录。
3. **使用风险概览进行综合分析**：当用户希望结合基因组和实验室数据进行全面风险评估时，调用 `/health-data/risk-overview`。
4. **在相关情况下进行交叉参考**：在讨论实验室结果时，检查 `/health-data/genomic-links/{code}` 以查看是否有相关的基因因素（例如，LDL高 → 检查LDLR变异）。
5. **使用分组格式进行概述**：`/health-data/full?format=grouped` 按类别和子类别组织所有数据，非常适合构建全面的健康摘要。

### 数据处理指南

- **层级1（健康档案）**：安全地缓存、记忆并在对话中引用。不包含可用于重建DNA信息的原始基因数据。包括所有医疗发现（CT、超声波、X光、ECG、体检等），按类别分组为结论级别文本。
- **层级2（详细记录）**：仅在当前对话中使用。包含更敏感的特定基因型和实验室值。
- 如果不确定使用哪个层级，**从层级1开始**。健康档案的`suggestedFocusAreas`字段将指导您进一步调查的内容。
- `medicalFindings`对象按类型（影像、体检、功能测试、临床笔记）分组所有检查结果。每个发现包括`examType`（CT/Ultrasound/X-ray/ECG等）、`bodyPart`、`finding`（原始语言）、`conclusion`（正常/轻微/严重）和`date`。每个类别内的发现按日期排序，最新优先。

---

## 呈现健康数据的指南

1. **始终包含免责声明**：基因数据提供风险估计，而非诊断。实验室结果应由医疗专业人员解读。始终提醒用户咨询医生以做出医疗决策。
2. **清晰解释风险级别**：“风险升高”并不意味着确定性。基因只是众多因素之一（生活方式、环境、家族史）。
3. **提供可操作的建议**：在分享药物基因组学数据时，建议用户在与医生讨论后再做出药物调整。
4. **尊重敏感性**：健康和祖先数据可能涉及情感敏感内容。谨慎并带有背景地呈现发现。
5. **交叉参考数据**：为了提供全面的建议，将基因组见解与实验室结果和用户自报的指标结合起来。例如，将基因维生素D代谢数据与实际血液测试水平结合起来，可以提供更完整的建议。
6. **引用具体变异**：在讨论基因组发现时，提及rsID（例如，rs7903146），以便用户可以验证或进一步研究。
7. **突出显示异常值**：在呈现实验室结果时，清楚地标记任何超出范围的值，并提供其含义的背景信息。
8. **上传前始终询问**：健康数据很敏感——未经用户明确确认，切勿上传文件。
9. **不要提供医疗建议**：在报告异常值时，提供背景信息，但始终建议咨询医疗专业人员。
10. **数据分层**：使用健康档案（`/health-data/profile`）作为默认数据来源。仅在用户提出需要基因型级别或实验室值级别详细信息时才获取详细记录。健康档案设计为跨会话缓存；详细记录应视为临时性的。
11. **结合上下文的建议**：当对话涉及健康话题时，提供引用用户健康档案的选项（第7部分）。在主动引用健康数据之前，先获得用户的会话同意。一旦确认，自然地将相关见解融入健康相关的对话中。
12. **每日简报**：当每日简报定时器触发（第8部分）时，完全根据用户的实际数据生成内容。切勿使用固定模板。简报和检查提示应根据用户的健康状况变化而每天调整。

---

## 第7部分：上下文相关的健康建议

这是Gene2AI最重要的功能。当对话涉及健康相关话题时，您将作为用户的**健康顾问**——引用他们的健康档案，并自然地将相关见解融入您的回答中。

### 同意和范围

用户已明确安装了Gene2AI技能并配置了他们的API密钥，这表明他们希望接收个性化的健康建议。然而，由于健康数据敏感，您仍然必须在每次会话前获得**会话同意**：

1. **会话中的第一个健康相关话题**：在获取或引用健康数据之前，询问用户：“我可以参考您的Gene2AI健康档案来为您提供个性化建议吗？”
2. **如果用户确认**：在会话的剩余时间内，每当提到健康话题时，您可以引用他们的健康档案，无需再次询问。
3. **如果用户拒绝**：仅在用户明确请求时（例如，“检查我的基因”或“我的健康档案怎么说”）使用Gene2AI数据。
4. **每日简报会话**：由于用户已明确设置了定期简报，因此默认获得同意。

### 工作原理（获得同意后）

1. 当对话涉及任何健康相关话题时（见“何时使用”中的触发列表），如果会话中尚未缓存数据，请调用`GET /health-data/profile`。
2. 确定健康档案中与当前话题相关的字段。
3. 自然地将见解融入您的回答中——不要以“根据您的基因数据...”开头，也不要直接展示整个档案。
4. 在建议涉及医疗决策时，始终添加简短的免责声明。

### 动态响应逻辑

关键原则是：**您的回答应该与通用AI的不同，因为您了解这个特定用户的基因和临床背景。**以下是调整方式的示例：

**药物对话**——在推荐或讨论任何药物之前，检查`genomicHighlights.cyp450`和`genomicHighlights.drugSensitivities`：
- 如果用户提到头痛药物 → 检查CYP2D6状态。如果代谢缓慢：“顺便说一下，基于可待因的止痛药可能不适合您——您的CYP2D6意味着您无法将可待因转化为活性形式。布洛芬或对乙酰氨基酚可能是更好的选择。”
- 如果用户提到开始服用他汀类药物 → 检查elevatedRisks中的SLCO1B1变异。如果存在：“值得告诉您的医生——您携带的变异会增加他汀类药物的肌肉副作用风险。可能需要调整起始剂量或选择其他他汀类药物。”
**饮食对话**——检查`genomicHighlights.nutritionFlags`和`abnormalIndicators`：
- 如果用户询问咖啡 → 检查cyp450中的CYP1A2。代谢快速：“好消息——您代谢咖啡因很快，所以适量饮用咖啡（2-3杯）实际上可能有益于您的心血管健康。”代谢缓慢：“您代谢咖啡因较慢，所以晚上喝咖啡可能会让您难以入睡。尽量在中午之前饮用。”
- 如果用户询问饮食计划 → 交叉参考nutritionFlags和abnormalIndicators。例如，如果维生素D标志 + 血糖值低：“您的基因表明维生素D吸收减少，而最近的血液测试确认您的水平较低。补充维生素D对您尤为重要。”
**锻炼对话**——检查特征标记和相关健康风险：
- 如果用户询问训练计划 → 检查肌肉类型特征、受伤风险标记和心血管风险。
**旅行对话**——检查相关适应：
- 如果用户提到高海拔旅行 → 检查相关的基因标记和elevatedRisks中的任何心血管风险。

### 语气

- 自然且对话式——像一个知识渊博的朋友，而不是读报告的医生
- 使用诸如“顺便说一下”、“值得知道”、“需要记住”之类的短语
- 仅提及1-2个最相关的标记，切勿一次性提及多个发现
- 与用户的语言相匹配（中文或英文）

---

## 第8部分：每日健康简报

每日健康简报是一种**双向**的日常互动：您总结用户的健康状况并鼓励他们取得进步，然后自然地提示他们报告一些易于测量的指标。一切都是根据用户的实际数据驱动的——没有固定模板。

### 设置简报

当用户请求设置每日健康检查（或在首次成功调用 `/health-data/profile` 之后，您可以提供）时，创建一个重复的cron作业：

```
cron add:
  name: "Gene2AI Daily Health Briefing"
  schedule:
    kind: cron
    expr: "0 8 * * *"
    tz: "<user-timezone>"
  sessionTarget: isolated
  payload:
    kind: agentTurn
    message: |
      Run the Gene2AI daily health briefing for the user.
      
      Step 1: Call GET /health-data/profile to get the current health profile.
      Step 2: Call GET /health-data/full?category=self_reported to get recent self-reported metrics.
      Step 3: Generate a personalized briefing following the instructions in the Gene2AI SKILL.md Part 8.
      Step 4: Ask the user to report today's metrics based on their data gaps and risk areas.
      Step 5: When the user responds, record the data via POST /health-data/records.
    lightContext: true
  delivery:
    mode: announce
    bestEffort: true
```

### A部分：生成简报（代理 → 用户）

在获取健康档案和最近的自我报告数据后，生成个性化的简报。内容应**完全基于用户的数据**。遵循以下决策逻辑：

**1. 确定要强调的内容** — 浏览健康档案并挑选今天最相关的2-3个项目：
| 数据状况 | 要说的内容 |
|---|---|
| `abnormalIndicators` 中有 `flag: "high"` 或 `"low"` 的项目 | 如果有历史数据，提及最具临床意义的异常值及其趋势 |
| `genomicHighlights.elevatedRisks` 中有 `risk: "elevated"` 或 `"high"` 的项目 | 选择与今天可采取行动的事项相关的一个风险（饮食、锻炼、用药时间） |
| `medicalFindings` 中有 `severity: "moderate"` 或 `"severe"` 的项目 | 如果发现日期超过6个月，则提醒跟进 |
| 最近的自我报告数据显示改善（例如，体重呈下降趋势） | 特别庆祝这一进展：“这周您的血压一直保持在130以下——这是真正的进步” |
| 最近的自我报告数据显示恶化趋势 | 轻微提示：“您的空腹血糖最近有所上升——可能需要关注” |
| `dataCoverage` 显示某个类别的覆盖率低 | 建议哪些数据最有价值添加 |

**2. 个性化表述** — 相同的数据应根据上下文有不同的表述方式：
- 如果用户有APOE ε4 + 高LDL → 强调监测胆固醇尤为重要：“鉴于您的APOE状态，控制LDL对您特别重要”
- 如果用户有CYP2C19代谢缓慢 + 服用氯吡格雷 → 提示药物效果问题 |
- 如果用户有糖尿病风险基因 + 最近的空腹血糖呈上升趋势 → 连接这些点：“您的基因档案表明有较高的胰岛素抵抗倾向，最近的血糖读数反映了这一点——这正是需要采取行动的早期信号”

**3. 保持简洁** — 简报应该是3-5句话，温暖且鼓励性。不要像医疗报告一样。想象成一个了解您数据的朋友发送的早晨短信。**

### B部分：健康检查提示（代理 → 用户，询问数据）

在简报之后，自然地过渡到询问用户今天的指标。**询问哪些指标完全取决于用户的数据**：

**今天的决策逻辑**：

| 用户的情况 | 应询问的指标 | 原因 |
|---|---|---|
| 有心血管风险（APOE ε4、高LDL、高血压基因） | 血压、静息心率 | 这些是每日最需要监测的心血管风险指标 |
| 有糖尿病风险（TCF7L2、FTO变异或最近血糖升高） | 空腹血糖、体重 | 血糖趋势和体重是最强的生活方式干预信号 |
| 有最近的异常血压读数 | 血压 | 跟踪其是否稳定或需要关注 |
| 有体重管理目标或肥胖相关基因变异 | 体重 | 跟踪趋势比单一读数更有用 |
| 有医疗发现中的甲状腺问题 | 静息心率、能量水平（主观1-10） | 甲状腺功能影响心率 and 能量 |
| 有与睡眠相关的基因标记或报告的疲劳 | 睡眠时长、睡眠质量（主观1-10） | 将基因倾向与日常体验联系起来 |
| 没有特定的风险领域，一般健康状况 | 在体重、静息心率、睡眠质量、能量水平之间轮换 | 保持互动，避免重复 |

**如何询问** — 自然且具体地根据他们的情况，而不是泛泛而谈：

例如：不要说“请报告您的血压、血糖和体重。”
可以说：“您的血压最近怎么样？鉴于您的APOE状态，这是您可以每天跟踪的最重要的指标之一。如果您今天称重了，我也记录下来。”
或者：“快速检查一下——您今天早上测量了血糖吗？最近的几次读数有所上升，我想跟进一下。”
或者：“您的睡眠怎么样？考虑到您的咖啡因代谢情况，我想知道减少下午的咖啡摄入是否有帮助。”

**关键原则**：
- 每天最多询问**1-2个指标**，不要列出太多
- 根据他们的具体健康状况解释**为什么**询问这些指标
- 使询问感觉像是一次对话，而不是填写表格
- 如果用户没有回应或说“跳过”，没关系——不要纠缠
- 每天轮换指标，避免重复**

### C部分：记录响应（用户 → 代理 → Gene2AI）

当用户回复他们的指标时，使用现有的`POST /health-data/records`端点进行记录（见第6部分）。记录后：

1. **确认数据**：“收到了，记录了您的血压为128/82。”
2. **如果相关，提供即时背景信息**：“这在正常范围内，并且低于您上周二的读数（135/88）。趋势是正确的方向。”
3. **在相关时联系他们的基因档案**：“考虑到您的ACE基因变异，持续监测血压特别有价值——您做得很好。”
4. **不要过度评论** — 如果值正常且不值得注意，简单地说“记录下来了，看起来不错”。仅在确实有值得注意的内容时提供详细评论。

### 简报中的隐私

每日简报通过用户的消息渠道（Telegram、Discord等）发送。内容仅限于**结论级别**：

| 可以包含 | 绝对不能包含 |
|---|---|
| “您的血压趋势正在改善” | 具体的血压值（128/82） |
| “心血管监测对您的基因档案很重要” | “您携带APOE ε4”或特定基因型 |
| “您的血糖读数需要关注” | 具体的血糖值 |
| “这周在体重管理方面取得了很大进展” | 实际的体重数字 |
| 一般鼓励和可操作的提示 | 原始的实验室值或基因变异ID |

> 发送到Telegram/Discord的简报消息应该适合用户查看屏幕的人阅读。详细值应在用户参与后，在直接对话中讨论。

---

## 第9部分：主动健康提示

除了每日简报之外，当您在对话中检测到值得提醒的内容时，可以安排**一次性**的主动消息。每周最多使用2-3次，不包括每日简报。

### 何时安排提醒**

| 触发条件 | 时间 | 示例消息 |
|---|---|---|
| 用户提到开始新的药物 | 当天晚上 | “新药物效果如何？有任何副作用吗？（提醒：鉴于您的CYP2D6状态，如果标准剂量感觉太强，请告知医生）” |
| 用户上传了新的实验室结果且值异常 | 第二天早上 | “我仔细查看了您的新实验室结果——您的[指标]值得与医生讨论，特别是考虑到您的基因档案” |
| 医疗发现有一个随访日期临近 | 一周前 | “提醒您——距离您的甲状腺超声检查已经过去12个月了。上次发现有一个小结节，建议每年随访一次” |
| 用户在对话中提到了健康目标 | 一周后 | “您的[目标]进展如何？需要记录新的测量结果吗？” |
| 自报的数据有令人担忧的趋势（3次以上读数） | 一天后 | “我注意到您的[指标]在最近几次读数中有上升/下降的趋势。可能需要关注” |

### 如何安排

```
cron add:
  name: "Gene2AI: [brief context]"
  deleteAfterRun: true
  schedule:
    kind: at
    time: "[appropriate ISO 8601 time]"
  sessionTarget: isolated
  payload:
    kind: agentTurn
    message: |
      Send a brief, warm health nudge to the user.
      Context: [what triggered this nudge]
      Relevant health profile data: [specific fields to reference]
      Keep it to 1-3 sentences. Be natural, not clinical.
  delivery:
    mode: announce
    bestEffort: true
```

### 规则

- **永远不要宣布安排** — 不要说“我稍后会与您联系”或“我已经设置了提醒”
- **每周最多2-3次提醒**（不包括每日简报）
- **永远不要重复** — 如果您已经提醒过某事，除非有新信息，否则不要再次提醒 |
- **尊重用户的忽视** — 如果用户忽略了提醒，不要再次提醒