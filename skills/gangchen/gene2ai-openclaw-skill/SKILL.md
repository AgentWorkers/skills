---
name: gene2ai
description: 这是一个专为AI代理设计的个人健康数据管理平台。您可以通过自然语言对话来查询基因组相关信息（如健康风险、药物反应、CYP450代谢酶状态、HLA等位基因类型、APOE基因型、营养状况、身体特征以及祖先信息），上传医疗文件以供AI进行分析，记录每日健康数据，并探索基因组信息与实验室检测结果之间的关联。
version: 3.0.0
metadata:
  openclaw:
    requires:
      env:
        - GENE2AI_API_KEY
    primaryEnv: GENE2AI_API_KEY
    emoji: "🧬"
    homepage: https://gene2.ai/guide
---
# Gene2AI — 为您的人工智能助手提供健康数据

您可以通过Gene2AI平台访问用户的个人健康数据，这些数据包括：

- **基因组数据**：来自23andMe、AncestryDNA、WeGene等平台的原始基因检测文件中的324多个指标——涵盖273个基因的933个SNP，分为9个类别；
- **健康文档**：实验室报告、体检结果、医疗记录和影像报告——这些数据已被人工智能解析为结构化指标；
- **用户自报的指标**：血压、血糖、体重、心率等日常测量数据；
- **交叉参考**：实验室指标与基因组标记之间的双向链接（例如，LDL-C与胆固醇基因之间的关联）。

## 何时使用此技能

当用户需要以下信息时，请使用此技能：

### 基因组数据查询
- 询问他们的**遗传健康风险**（例如：“我是否有患2型糖尿病的风险？”、“阿尔茨海默病的风险如何？”）；
- 询问**药物反应**或药物基因组学信息（例如：“我如何代谢咖啡因？”、“我对华法林敏感吗？”）；
- 询问**CYP450代谢酶的状态**（例如：“我的CYP2D6状态是什么？”、“我是快速代谢者吗？”）；
- 询问**HLA等位基因**（例如：“我携带HLA-B*57:01吗？”、“我有药物过敏的风险吗？”）；
- 询问**APOE基因型**（例如：“我的APOE状态是什么？”、“我有ε4等位基因吗？”）；
- 询问**营养和营养基因组学信息**（例如：“我需要更多的维生素D吗？”、“我乳糖不耐受吗？”）；
- 询问**身体特征**（例如：“我的DNA显示我的肌肉类型是什么？”）；
- 希望根据他们的基因获得**个性化建议**；
- 提到他们的**DNA**、**基因**、**SNP**或**基因变异**。

### 健康数据管理
- 发送与健康相关的文档（实验室报告、体检结果、医疗记录、处方、影像报告）；
- 请求上传、保存或记录健康数据；
- 口头报告健康指标（血压、血糖、体重、心率等）；
- 询问他们的健康数据状态或摘要；
- 例如：“帮我保存这份体检报告”、“将这个上传到我的健康数据库”、“记录一下我的血压”。

### 交叉参考查询
- 询问实验室结果与基因之间的关联（例如：“我的LDL很高——我有遗传风险因素吗？”）；
- 希望获得结合基因组和实验室数据的全面风险概览；
- 请求进行全面的健康评估。

## 配置

用户的Gene2AI API密钥作为环境变量`GENE2AI_API_KEY`提供。

API密钥是**按个人资料划分的**——每个密钥仅关联一个特定的健康资料（例如，“自我”、“母亲”、“父亲”）。使用此密钥时，所有数据查询将自动返回仅与该资料相关的数据。这样可以防止意外地混合不同家庭成员的健康数据。

> **重要提示：**每个密钥仅适用于一个资料。如果用户为多个家庭成员管理健康数据，应为每个资料生成一个单独的密钥。可以使用`?profileId=`查询参数来覆盖密钥的默认资料。

如果`GENE2AI_API_KEY`未设置，请指导用户：
1. 访问https://gene2.ai并登录（或创建账户）；
2. 转到**API密钥**页面（https://gene2.ai/api-keys）；
3. 点击**生成新密钥**并选择该密钥应访问的健康资料；
4. 复制生成的令牌并在OpenClaw中进行配置：

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

### 健康资料（推荐的首次调用）

```bash
curl -s "https://gene2.ai/api/v1/health-data/profile" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

返回一个**简洁的、仅包含结论的健康资料**（约2-4KB）。这是任何代理会话的首选调用。响应内容包括：
- **APOE基因型**结论（例如，“APOE ε3/ε4——风险增加”）；
- 每个基因的**CYP450代谢酶状态**（例如，“CYP2D6：正常代谢者”以及受影响的药物）；
- **HLA携带者状态**（仅显示阳性等位基因）；
- **较高的健康风险**（疾病名称+风险等级+简要说明，不包含原始SNP）；
- **药物敏感性**（药物+敏感性等级）；
- **营养标志**（基于基因变异的营养问题）；
- **异常的实验室/体检指标**（仅显示最新值：名称、数值、单位、标志）；
- **医疗发现**——所有检查结果（CT、超声、X光、MRI、心电图、体格检查、功能测试等），按类别分组，包括正常和异常结果，保留原始语言；
- **医疗发现摘要**——每个类别的总数和异常数量；
- **建议关注的重点领域**（通过交叉参考基因组+临床+影像数据自动生成）。

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

> **此资料设计为可缓存并在多次会话中重复使用。**它不包含原始的基因数据（没有rs-IDs、基因型或SNP详细信息），因此适合代理内存和跨会话引用。医疗发现包括所有检查结果（正常和异常），按类别分组，并在每个类别内按日期排序（最新结果优先）。`finding`字段保留了医疗报告的原始语言（中文或英文）。当用户需要具体的基因详细信息时，可以使用以下端点进行深入查询。

### 摘要概览

```bash
curl -s "https://gene2.ai/api/v1/health-data/summary" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

返回总文档数量、总记录数以及按类别和基因组子类别的分类。

### 完整记录（可过滤）

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

**查询参数：**
| 参数 | 值 | 描述 |
|-----------|--------|-------------|
| `category` | `genomic`、`lab_result`、`checkup`、`self_reported`、`medical_record`、`imaging` | 按数据类别过滤 |
| `subcategory` | `health_risk`、`drug_response`、`trait`、`nutrition`、`ancestry`、`apoe`、`hla`、`cyp450` | 按基因组子类别过滤 |
| `format` | `grouped` | 按类别→子类别层次结构组织记录 |

### 增量更改（用于同步）

```bash
curl -s "https://gene2.ai/api/v1/health-data/delta?since_version={version_number}" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

---

## 第2部分：基因组数据类别

基因组数据分为9个子类别。使用`?category=genomic`查询时，每条记录都包含一个`data`字段，其中包含已解析的结构化对象（无需手动解析`valueText` JSON）。

### health_risk（193个标记）

按疾病/基因分组的疾病风险评估（CFTR、LDLR、阿尔茨海默病、CAD、T2D等）

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

**风险等级**：`低`、`平均`、`略高`、`高`、`非常高`

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

CYP450代谢酶表型分析，附带CPIC星形等位基因定义和特定药物的建议。

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

**代谢酶状态**：**超快速代谢者`、`正常代谢者`、`中间代谢者`、**缓慢代谢者`

### hla（9个等位基因）

通过标签SNP推断的HLA等位基因分型，用于免疫相关疾病和药物过敏。

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

基于人群特定变异分析的区域祖先百分比。

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

### 综合风险仪表盘

```bash
curl -s "https://gene2.ai/api/v1/health-data/risk-overview" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

返回一个结合基因组和实验室数据的综合风险仪表盘：

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

返回与该实验室指标相关的基因组记录，以便进行交叉参考（例如：“您的LDL很高，并且您具有与家族性高胆固醇相关的LDLR基因变异”）。

### 实验室-基因组摘要

```bash
curl -s "https://gene2.ai/api/v1/health-data/lab-genomic-summary" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

返回所有实验室指标及其相关的基因组记录数量，用于构建交叉参考仪表盘。

---

## 第4部分：按Job ID查询基因组数据（旧版本）

为了向后兼容，您也可以通过Job ID查询基因组数据：

```bash
curl -s -X GET "https://gene2.ai/api/v1/genomics/${GENE2AI_JOB_ID}" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

如果`GENE2AI_JOB_ID`未设置，请询问用户的Job ID（可在https://gene2.ai/my-jobs页面查看）。

> **注意**：/health-data/full?category=genomic端点（第1部分）是首选，因为它返回了丰富且已解析的数据，并支持过滤/分组。

---

## 第5部分：上传健康文档

当用户发送看似健康文档的文件（图像或PDF）时：

### 第1步：与用户确认

在上传之前务必确认：“我将把这个文件上传到您的Gene2AI健康数据库进行人工智能分析。系统会自动提取所有健康指标。继续吗？”

### 第2步：确定文档类别

- `lab_result` — 血液检测、尿液检测、生化检测；
- `checkup` — 年度体检报告；
- `medical_record` — 医生访问记录、诊断结果；
- `imaging` — X光、CT、MRI、超声报告。

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

- **如果状态为“completed”**：显示提取的指标数量，突出显示任何异常发现（`abnormalFlag` = “high”、“low”、“critical_high”、“critical_low”或“abnormal”），并列出检测机构和文档类型；
- **如果状态为“parsing”**：告诉用户解析仍在进行中。他们可以在https://gene2.ai/health-data查看，或稍后再次请求；
- **如果状态为“failed”**：报告`parseError`消息，并建议直接在https://gene2.ai/health-data上传文件。

---

## 第6部分：提交结构化健康指标

当用户口头报告健康指标时（例如：“我的血压是125/82”，“血糖5.8”，“体重72kg”）：

### 常见指标及参考范围

| 指标 | 中文 | 单位 | 参考范围 |
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

- `normal` — 在参考范围内；
- `high` — 超出参考范围；
- `low` — 低于参考范围；
- `critical_high` — 危险地高于（例如，SBP > 180）；
- `critical_low` — 危险地低于（例如，血糖 < 2.8）。

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
| 401 | `missing_token` | 未设置Authorization头——检查`GENE2AI_API_KEY`是否已设置 |
| 401 | `invalid_token` | API密钥格式错误或无效 |
| 403 | `token_expired` | API密钥已过期（30天限制）——用户需要在https://gene2.ai/api-keys重新生成 |
| 403 | `key_revoked` | API密钥已被手动吊销 |
| 403 | `job_id_mismatch` | 密钥未授权用于此Job ID（密钥仅限特定作业） |
| 404 | `job_not_found` | Job ID不存在 |
| 404 | `data_not_available` | 分析尚未完成 |

如果收到`token_expired`或`key_revoked`错误，请指导用户访问https://gene2.ai/api-keys生成新的API密钥。

---

## 建议的代理查询策略

### 数据层级

Gene2AI将健康数据分为三个层级，以便代理高效使用：

| 层级 | 端点 | 大小 | 包含内容 | 持久性 |
|------|----------|------|----------|-------------|
| **层级1：健康资料** | `/health-data/profile` | 约2-4KB | 仅包含结论（风险等级、代谢酶状态、异常标志） | **可在会话间缓存和重复使用** |
| **层级2：详细记录** | `/health-data/full`、`/health-data/risk-overview` | 约50-500KB | 具体基因型、SNP、实验室值、交叉参考 | 仅用于当前会话，不持久保存 |
| **层级3：原始数据** | 仅限于网站（gene2.ai） | MB+ | 原始基因文件、完整分析JSON | 从不进入代理上下文 |

### 建议的流程

1. **从健康资料开始**：调用 `/health-data/profile` 获取简洁的概览。这对于大多数健康相关决策（饮食、锻炼、一般健康问题）已经足够。**将此资料缓存到代理内存**中，以便在会话间使用。
2. **仅在需要时深入查询**：当用户提出具体问题时（例如，“我的CYP2D6基因型到底是什么？”、“显示我的APOE SNP”），调用 `/health-data/full?category=genomic&subcategory=cyp450` 获取详细记录。
3. **使用风险概览进行综合分析**：当用户希望结合基因组和实验室数据进行全面风险评估时，调用 `/health-data/risk-overview`。
4. **在相关时进行交叉参考**：在讨论实验室结果时，检查 `/health-data/genomic-links/{code}`，查看是否有相关的基因因素（例如，LDL高 → 检查LDLR变异）。
5. **使用分组格式进行汇总**：`/health-data/full?format=grouped` 按类别和子类别组织所有数据，非常适合构建全面的健康摘要。

### 数据处理指南

- **层级1（健康资料）**：可以安全地缓存、记忆并在会话间引用。不包含可用于重建DNA信息的原始基因数据。包含所有医疗发现（CT、超声、X光、心电图、体格检查等），按类别分组为结论级别文本。
- **层级2（详细记录）**：仅用于当前会话。包含更敏感的特定基因型和实验室值。
- 如果不确定使用哪个层级，**从层级1开始**。健康资料的`suggestedFocusAreas`字段将指导您进一步调查的方向。
- `medicalFindings`对象按类型（影像、体格检查、功能测试、临床笔记）分组所有检查结果。每个发现包括`examType`（CT/超声/X光/心电图等）、`bodyPart`、`finding`（原始语言）、`conclusion`（正常/轻微/严重）和`date`。每个类别内的发现按日期排序，最新结果优先。

---

## 呈现健康数据的指南

1. **始终包含免责声明**：基因数据提供风险估计，而非诊断。实验室结果应由医疗专业人员解读。始终提醒用户咨询医生以获取医疗建议。
2. **清晰解释风险等级**：“风险增加”并不意味着确定性。基因只是众多因素之一（生活方式、环境、家族史等）。
3. **提供可操作的建议**：在分享药物基因组学数据时，建议用户在与医生讨论后再做出药物调整。
4. **尊重敏感性**：健康和祖先数据可能具有情感敏感性。谨慎并带有背景地呈现发现结果。
5. **交叉参考数据**：为了提供全面的建议，将基因组见解与实验室结果和用户自报的指标结合起来。例如，将基因维生素D代谢数据与实际血液检测水平结合起来，可以提供更完整的建议。
6. **引用具体变异**：在讨论基因组发现时，提及rsID（例如，rs7903146），以便用户可以验证或进一步研究。
7. **突出显示异常值**：在呈现实验室结果时，明确标注任何超出范围的值，并提供其含义的背景信息。
8. **上传前务必询问**：健康数据敏感——未经用户明确确认，切勿上传文件。
9. **不要提供医疗建议**：在报告异常值时，提供背景信息，但始终建议咨询医疗专业人员。
10. **数据分层**：使用健康资料（/health-data/profile）作为默认数据来源。仅在用户提出需要基因型级别或实验室值级别详细信息的具体问题时才获取详细记录。健康资料设计为可在会话间缓存；详细记录应视为临时数据。