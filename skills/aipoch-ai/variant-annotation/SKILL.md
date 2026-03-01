---
name: variant-annotation
description: >
  从 ClinVar 和 dbSNP 数据库中查询并注释基因变异信息。  
  触发条件包括：  
  - 用户提供变异标识符（rsID、HGVS 表示法或基因组坐标）并询问其临床意义；  
  - 用户提及 “ClinVar”、“dbSNP”、“变异注释”、“致病性” 或 “临床意义”；  
  - 用户想了解某个突变是致病的、良性的还是意义不明确的；  
  - 用户提供需要解读的 VCF 文件或变异数据。  
  输入内容示例：  
  - 变异 ID：rs12345  
  - HGVS 表示法：NM_007294.3:c.5096G>A  
  - 基因组坐标：chr17:43094692:G>A  
  输出内容示例：  
  - 临床意义：  
  - ACMG 分类：  
  - 等位基因频率：  
  - 相关疾病：
  Trigger when:\n- User provides a variant identifier (rsID, HGVS notation, genomic\
  \ coordinates) and asks about clinical significance\n- User mentions \"ClinVar\"\
  , \"dbSNP\", \"variant annotation\", \"pathogenicity\", \"clinical significance\"\
  \n- User wants to know if a mutation is pathogenic, benign, or of uncertain significance\n\
  - User provides VCF content or variant data requiring interpretation\n- Input: variant\
  \ ID (rs12345), HGVS notation (NM_007294.3:c.5096G>A), or genomic coordinates (chr17:43094692:G>A)\n\
  - Output: clinical significance, ACMG classification, allele frequency, disease\
  \ associations"
version: 1.0.0
category: Bioinfo
tags: []
author: AIPOCH
license: MIT
status: Draft
risk_level: High
skill_type: Hybrid (Tool/Script + Network/API)
owner: AIPOCH
reviewer: ''
last_updated: '2026-02-06'
---
# 基因变异注释

本工具能够从ClinVar和dbSNP数据库中查询并解读基因变异的临床意义，并遵循ACMG（美国医学遗传学协会）的指导原则。

## 目的

提供全面的变异注释信息，包括：
- 临床意义分类（致病性、可能致病性、VUS（意义不明确）、可能良性、良性）
- 基于ACMG指导原则的致病性评估
- 人群等位基因频率（gnomAD、ExAC、1000 Genomes）
- 疾病与表型关联
- 功能预测（SIFT、PolyPhen、CADD）

## 支持的输入格式

| 格式 | 例子 | 描述 |
|--------|---------|-------------|
| **rsID** | `rs80357410` | dbSNP参考SNP ID |
| **HGVS cDNA** | `NM_007294.3:c.5096G>A` | 编码区DNA变异 |
| **HGVS Protein** | `NP_009225.1:p.Arg1699Gln` | 蛋白质变异 |
| **HGVS Genomic** | `NC_000017.11:g.43094692G>A` | 基因组坐标 |
| **VCF样式** | `chr17:43094692:G>A` | 染色体:位置:参考序列>替代序列 |
| **Gene:AA** | `BRCA1:R1699Q` | 基因中的氨基酸变异 |

## 使用方法

### Python API

```python
from scripts.main import VariantAnnotator

# Initialize annotator
annotator = VariantAnnotator()

# Query by rsID
result = annotator.query_variant("rs80357410")

# Query by HGVS notation
result = annotator.query_variant("NM_007294.3:c.5096G>A")

# Query by genomic coordinate
result = annotator.query_variant("chr17:43094692:G>A")

# Batch query
results = annotator.batch_query(["rs80357410", "rs28897696", "rs11571658"])
```

### 命令行

```bash
# Single variant query
python scripts/main.py --variant rs80357410

# HGVS notation
python scripts/main.py --variant "NM_007294.3:c.5096G>A"

# Genomic coordinate
python scripts/main.py --variant "chr17:43094692:G>A"

# Batch from file
python scripts/main.py --file variants.txt --output results.json

# With output format
python scripts/main.py --variant rs80357410 --format json
```

## 输出格式

```json
{
  "variant_id": "rs80357410",
  "gene": "BRCA1",
  "chromosome": "17",
  "position": 43094692,
  "ref_allele": "G",
  "alt_allele": "A",
  "hgvs_genomic": "NC_000017.11:g.43094692G>A",
  "hgvs_cdna": "NM_007294.3:c.5096G>A",
  "hgvs_protein": "NP_009225.1:p.Arg1699Gln",
  
  "clinical_significance": {
    "clinvar": "Pathogenic",
    "acmg_classification": "Pathogenic",
    "acmg_criteria": ["PS4", "PM1", "PM2", "PP2", "PP3", "PP5"],
    "acmg_score": 13.0,
    "review_status": "criteria provided, multiple submitters, no conflicts"
  },
  
  "disease_associations": [
    {
      "disease": "Breast-ovarian cancer, familial 1",
      "medgen_id": "C2676676",
      "significance": "Pathogenic"
    }
  ],
  
  "population_frequencies": {
    "gnomAD_genome_all": 0.000008,
    "gnomAD_exome_all": 0.000012,
    "1000G_all": 0.0
  },
  
  "functional_predictions": {
    "sift": "deleterious",
    "polyphen2": "probably_damaging",
    "cadd_score": 24.5,
    "mutation_taster": "disease_causing"
  },
  
  "literature_count": 42,
  "last_evaluated": "2023-12-15",
  
  "interpretation_summary": "This variant (BRCA1 p.Arg1699Gln) is classified as Pathogenic based on ACMG guidelines. It shows strong evidence of pathogenicity including population data (extremely rare), computational predictions (deleterious), and strong clinical significance (established association with hereditary breast-ovarian cancer)."
}
```

## ACMG分类标准

本工具遵循ACMG/AMP指南对基因变异进行解读：

### 致病性证据（评分）

- **PVS1**（8.0）：在已知导致功能丧失（LOF）的基因中出现的变异
- **PS1**（4.0）：与已知致病性变异相同的氨基酸变化
- **PS2**（4.0）：新发突变且具有明确的父系/母系遗传特征
- **PS3**（4.0）：经过充分验证的功能研究显示具有致病性
- **PS4**（4.0）：在患者中的发生率高于对照组
- **PM1**（2.0）：位于关键功能域
- **PM2**（2.0）：在对照组中未检测到（MAF <0.0001）
- **PM3**（2.0）：在携带致病性突变的个体中检测到
- **PM4**（2.0）：导致蛋白质长度变化
- **PM5**（2.0）：与已知致病性变异位于相同位置的新的错义突变
- **PM6**（2.0）：假设为新发突变但未经确认
- **PP1**（1.0）：与疾病存在共分离现象
- **PP2**（1.0）：在低良性率的基因中出现的错义突变
- **PP3**（1.0）：有多个计算证据支持
- **PP4**（1.0）：表型/患者病史与基因变异相匹配
- **PP5**（1.0）：来自可靠来源的报告表明具有致病性

### 良性证据

- **BA1**（-8.0）：在人群中的MAF（等位基因频率）>5%
- **BS1**（-4.0）：MAF高于该疾病的预期值
- **BS2**（-4.0）：在健康成人中观察到
- **BS3**（-4.0）：功能研究未显示致病性
- **BS4**（-4.0）：不存在共分离现象
- **BP1**（-1.0）：在导致截短效应的基因中出现的错义突变
- **BP2**（-1.0）：在携带致病性突变的个体中观察到
- **BP3**（-1.0）：在重复序列中的框内插入/缺失
- **BP4**（-1.0）：有多个计算证据支持其良性
- **BP5**（-1.0）：找到了其他可能的致病原因
- **BP6**（-1.0）：来自可靠来源的报告表明其良性
- **BP7**（-1.0）：同义突变且不影响剪接过程

### 分类阈值

| 分类 | 评分范围 |
|----------------|-------------|
| 致病性 | ≥ 10 |
| 可能致病性 | 6-9 |
| 意义不明确 | 0-5 |
| 可能良性 | -5至-1 |
| 良性 | ≤ -6 |

## 技术难度：**高**

⚠️ **AI自主验收状态**：需要人工审核

本技能要求：
- 集成NCBI E-utilities API（ClinVar、dbSNP）
- 解析和验证HGVS命名规则
- 处理VCF格式数据
- 实施ACMG指导原则
- 集成多种预测算法
- 复杂的数据转换和评分

## 数据来源

| 数据库 | 数据类型 | API/访问方式 |
|----------|-----------|------------|
| **ClinVar** | 临床意义、疾病关联 | NCBI E-utilities |
| **dbSNP** | SNP数据、等位基因频率 | NCBI E-utilities |
| **gnomAD** | 人群频率 | gnomAD API |
| **Ensembl VEP** | 功能预测 | REST API |
| **CADD** | 致害性评分 | REST API |

## 限制

- 需要互联网连接才能查询数据库
- NCBI API的请求速率限制为每秒3次（使用API密钥后可提升至每秒10次）
- 有些变异可能不在ClinVar数据库中（例如无临床数据的VUS变异）
- 复杂变异的HGVS命名规则解析可能会失败
- 并非所有变异都提供人群频率数据
- 功能预测仅基于计算结果

## 参考资料

请参阅`references/`文件夹中的以下资料：
- ACMG指导原则（Richards等人，2015年）
- ClinVar文档
- HGVS命名规则指南
- dbSNP数据字典
- 变异注释示例

## 安全与免责声明

⚠️ **重要提示**：本工具仅用于研究和教育目的。基因变异的解读结果为计算预测，不应作为临床决策的唯一依据。请始终咨询经过认证的遗传咨询师和临床实验室进行诊断。本工具中的ACMG分类结果为算法估算，可能与专家小组的评估结果有所不同。

## 风险评估

| 风险指标 | 评估内容 | 风险等级 |
|----------------|------------|-------|
| 代码执行 | 使用Python脚本 | 高风险 |
| 网络访问 | 外部API调用 | 高风险 |
| 文件系统访问 | 读写数据 | 中等风险 |
| 指令篡改 | 有标准的提示和指导 | 低风险 |
| 数据泄露 | 数据处理过程安全 | 中等风险 |

## 安全检查清单

- [ ] 无硬编码的凭证或API密钥
- [ ] 无未经授权的文件系统访问
- [ ] 输出内容不暴露敏感信息
- [ ] 有防止注入攻击的措施
- [ ] API请求仅使用HTTPS协议
- [ ] 输入内容经过验证
- [ ] 实施了API请求超时和重试机制
- [ ] 输出目录受到限制
- [ ] 脚本在沙箱环境中执行
- [ ] 错误信息经过处理（不暴露内部路径）
- [ ] 依赖项经过审核
- [ ] 未暴露内部服务架构

## 先决条件

```bash
# Python dependencies
pip install -r requirements.txt
```

## 评估标准

### 成功指标
- [ ] 能够成功执行主要功能
- [ ] 输出符合质量标准
- [ ] 能够优雅地处理边缘情况
- [ ] 性能表现可接受

### 测试用例
1. **基本功能**：标准输入 → 预期输出
2. **边缘情况**：无效输入 → 良好的错误处理
3. **性能**：处理大规模数据集时时间合理

## 生命周期状态

- **当前阶段**：草案阶段
- **下一次审查日期**：2026-03-06
- **已知问题**：无
- **计划中的改进**：
  - 性能优化
  - 支持更多功能

## 参数

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `--variant` | str | 必需参数 |  |
| `--file` | str | 必需参数 |  |
| `--output` | str | 必需参数 |  |
| `--format` | str | "json" |  |
| `--api-key` | str | 必需参数 | NCBI API密钥（用于提高请求速率） |
| `--delay` | float | 0.34 |  |