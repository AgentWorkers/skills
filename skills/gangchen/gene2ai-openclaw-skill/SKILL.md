---
name: gene2ai
description: 您可以从 Gene2AI 查询您的个人基因组数据。系统会提供结构化的 JSON 数据，涵盖健康风险、药物反应、营养状况、遗传特征以及祖先信息等，这些数据将为您的个性化健康管理提供支持（基于人工智能的个性化服务）。
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - GENE2AI_API_KEY
        - GENE2AI_JOB_ID
    primaryEnv: GENE2AI_API_KEY
    emoji: "🧬"
    homepage: https://gene2.ai/guide
---
# Gene2AI — 为AI代理提供的基因组数据

您可以通过Gene2AI API访问用户的个人基因组数据。这些数据已从原始的基因检测文件（如23andMe、AncestryDNA等）中处理成结构化、AI可读取的JSON格式，涵盖了健康风险、药物反应、营养状况、身体特征和祖先信息。

## 何时使用此技能

当用户询问以下内容时，请使用此技能：

- **遗传健康风险**（例如：“我有患2型糖尿病的风险吗？”）
- **药物反应**或药物基因组学（例如：“我如何代谢咖啡因？”、“我对华法林敏感吗？”）
- **营养**和营养基因组学（例如：“我需要补充更多的维生素D吗？”、“我是否乳糖不耐受？”）
- **身体特征**（例如：“我的DNA显示我的肌肉类型是什么？”）
- **祖先构成**或单倍群信息
- 基于用户基因信息的个性化健康、健身、饮食或健康建议
- 任何与用户的**DNA**、**基因**、**SNP**或**基因变异**相关的问题

## 如何查询API

向Gene2AI API发送GET请求：

```bash
curl -X GET "https://gene2.ai/api/v1/genomics/${GENE2AI_JOB_ID}" \
  -H "Authorization: Bearer ${GENE2AI_API_KEY}"
```

环境变量`GENE2AI_API_KEY`和`GENE2AI_JOB_ID`由用户提供。如果这些变量未设置，请让用户执行以下操作：
1. 访问https://gene2.ai并上传他们的基因数据文件
2. 分析完成后，前往https://gene2.ai/api-keys生成API密钥
3. 设置环境变量：
   ```
   GENE2AI_API_KEY=<their API key>
   GENE2AI_JOB_ID=<their job ID from the results page>
   ```

## 响应格式

API返回一个JSON对象，其中包含以下顶级类别：

| 类别 | 描述 | 示例字段 |
|---|---|---|
| `health_risks` | 基于基因变异的疾病风险评估 | condition（疾病状况）、risk_level（风险等级）、rsid（SNP标识符）、genotype（基因型） |
| `pharmacogenomics` | 药物反应预测和代谢状态 | drug（药物）、gene（基因）、metabolizer_status（代谢状态）、recommendation（建议） |
| `traits` | 身体和行为特征预测 | trait（特征）、result（结果）、confidence（置信度）、rsid（SNP标识符） |
| `nutrigenomics` | 与营养相关的基因信息 | nutrient（营养素）、gene（基因）、status（状态） |
| `ancestry` | 祖先构成和单倍群数据 | region（地区）、percentage（占比）、haplogroup（单倍群） |
| `metadata` | 分析元数据 | source（数据来源）、total_variants（总变异数）、analyzed_at（分析时间） |

### 示例响应结构

```json
{
  "health_risks": [
    {
      "condition": "Type 2 Diabetes",
      "risk_level": "elevated",
      "rsid": "rs7903146",
      "genotype": "CT"
    }
  ],
  "pharmacogenomics": [
    {
      "drug": "Caffeine",
      "gene": "CYP1A2",
      "metabolizer_status": "fast",
      "recommendation": "Normal caffeine tolerance"
    }
  ],
  "traits": [
    {
      "trait": "Lactose Tolerance",
      "result": "Likely tolerant",
      "confidence": "high",
      "rsid": "rs4988235"
    }
  ],
  "nutrigenomics": [
    {
      "nutrient": "Vitamin D",
      "gene": "VDR",
      "status": "May need supplementation"
    }
  ],
  "ancestry": [
    {
      "region": "East Asian",
      "percentage": 45.2,
      "haplogroup": "D4"
    }
  ],
  "metadata": {
    "source": "23andme",
    "total_variants": 650000,
    "analyzed_at": "2026-03-01T12:00:00Z"
  }
}
```

## 错误处理

| HTTP 状态码 | 错误代码 | 含义 |
|---|---|---|
| 401 | `missing_token` | 未设置授权头——请检查`GENE2AI_API_KEY`是否已设置 |
| 401 | `invalid_token` | API密钥格式错误或无效 |
| 403 | `token_expired` | API密钥已过期（有效期为30天）——用户需要前往https://gene2.ai/api-keys生成新的密钥 |
| 403 | `key_revoked` | API密钥已被手动吊销 |
| 403 | `job_id_mismatch` | 该密钥未授权用于此作业ID |
| 404 | `job_not_found` | 作业ID不存在 |
| 404 | `data_not_available` | 分析尚未完成——请用户稍后查看状态 |

如果收到`token_expired`或`key_revoked`错误，请指导用户访问https://gene2.ai/api-keys生成新的API密钥。

## 展示基因组数据的指南

在向用户展示基因组信息时，请遵循以下指南：

1. **始终包含免责声明**：基因数据提供的是风险估计，并非诊断结果。务必提醒用户咨询医疗专业人员以做出医疗决策。
2. **清晰解释风险等级**：“风险升高”并不意味着必然会发生。说明基因只是众多因素之一（还包括生活方式、环境、家族史等）。
3. **提供可操作的建议**：在分享药物基因组学数据时，建议用户在与医生讨论后再调整用药方案。
4. **尊重用户的敏感性**：祖先和健康风险数据可能涉及敏感信息。请谨慎并结合背景信息呈现结果。
5. **跨类别综合建议**：为了提供全面的建议，需结合不同类别的信息。例如，将维生素D代谢的营养基因组学数据与健康风险数据结合起来，可以给出更完整的建议。
6. **引用具体的基因变异**：在讨论某个发现时，提及rsID（例如rs7903146），以便用户可以验证或进一步研究。