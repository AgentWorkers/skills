---
name: openbio
description: >
  OpenBio API for biological data access and computational biology tools.
  Use when: (1) Querying biological databases (PDB, UniProt, ChEMBL, etc.),
  (2) Searching scientific literature (PubMed, bioRxiv, arXiv),
  (3) Running structure prediction (Boltz, Chai, ProteinMPNN),
  (4) Performing pathway/enrichment analysis,
  (5) Designing molecular biology experiments (primers, cloning),
  (6) Analyzing variants and clinical data.
metadata:
  tags: [biology, protein, genomics, chemistry, bioinformatics, drug-discovery]
---

## 安装

```bash
bunx skills add https://github.com/openbio-ai/skills --skill openbio
```

## 认证

**必需**：设置 `OPENBIO_API_KEY` 环境变量。

```bash
export OPENBIO_API_KEY=your_key_here
```

**基础 URL**：`https://openbio-api.fly.dev/`

## 快速入门

```bash
# List available tools
curl -X GET "https://openbio-api.fly.dev/api/v1/tools" \
  -H "X-API-Key: $OPENBIO_API_KEY"

# Get tool schema (always do this first!)
curl -X GET "https://openbio-api.fly.dev/api/v1/tools/{tool_name}" \
  -H "X-API-Key: $OPENBIO_API_KEY"

# Invoke tool
curl -X POST "https://openbio-api.fly.dev/api/v1/tools" \
  -H "X-API-Key: $OPENBIO_API_KEY" \
  -F "tool_name=search_pubmed" \
  -F 'params={"query": "CRISPR", "max_results": 5}'
```

## 工具选择指南

```
What do you need?
│
├─ Protein/structure data?
│   └─ Read rules/protein-structure.md
│       → PDB, AlphaFold, UniProt tools
│
├─ Literature search?
│   └─ Read rules/literature.md
│       → PubMed, arXiv, bioRxiv, OpenAlex
│
├─ Genomics/variants?
│   └─ Read rules/genomics.md
│       → Ensembl, GWAS, VEP, GEO
│
├─ Small molecule analysis?
│   └─ Read rules/cheminformatics.md
│       → RDKit, PubChem, ChEMBL
│
├─ Cloning/PCR/assembly?
│   └─ Read rules/molecular-biology.md
│       → Primers, restriction, Gibson, Golden Gate
│
├─ Structure prediction/design?
│   └─ Read rules/structure-prediction.md
│       → Boltz, Chai, ProteinMPNN, LigandMPNN
│
├─ Pathway analysis?
│   └─ Read rules/pathway-analysis.md
│       → KEGG, Reactome, STRING
│
└─ Clinical/drug data?
    └─ Read rules/clinical-data.md
        → ClinicalTrials, ClinVar, FDA, Open Targets
```

## 重要规则

### 1. 必须先查看工具的接口规范（schema）
```bash
# Before invoking ANY tool:
curl -X GET "https://openbio-api.fly.dev/api/v1/tools/{tool_name}" \
  -H "X-API-Key: $OPENBIO_API_KEY"
```
参数名称可能有所不同（例如，使用 `pdb_ids` 而不是 `pdb_id`）。请务必查看接口规范以避免错误。

### 2. 长时间运行的任务（如 `submit_*` 系列工具）
预测工具会返回一个 `job_id`。需要定期检查任务是否已完成：
```bash
# Check status
curl -X GET "https://openbio-api.fly.dev/api/v1/jobs/{job_id}/status" \
  -H "X-API-Key: $OPENBIO_API_KEY"

# Get results with download URLs
curl -X GET "https://openbio-api.fly.dev/api/v1/jobs/{job_id}" \
  -H "X-API-Key: $OPENBIO_API_KEY"
```

### 3. 数据质量标准
不要仅仅获取数据，还要对其进行解读：
- **AlphaFold pLDDT**：得分 > 70 表示结构较为稳定；得分 < 50 表示结构不稳定
- **结合位点的实验分辨率**：需小于 2.5 Å
- **GWAS p 值**：小于 5×10⁻⁸ 表示具有统计学意义
- **Tanimoto 相似度**：大于 0.7 表示化合物结构相似

详细的质量标准请参阅相应的规则文件。

## 规则文件
这些文件包含了特定领域的专业知识：
| 文件名 | 涉及的工具 |
|------|---------------|
| [rules/api.md](rules/api.md) | 核心接口、任务管理 |
| [rules/protein-structure.md](rules/protein-structure.md) | PDB、PDBe、AlphaFold、UniProt |
| [rules/literature.md](rules/literature.md) | PubMed、arXiv、bioRxiv、OpenAlex |
| [rules/genomics.md](rules/genomics.md) | Ensembl、ENA、Gene、GWAS、GEO |
| [rules/cheminformatics.md](rules/cheminformatics.md) | RDKit、PubChem、ChEMBL |
| [rules/molecular-biology.md](rules/molecular-biology.md) | 引物设计、PCR、DNA切割、基因组组装 |
| [rules/structure-prediction.md](rules/structure-prediction.md) | Boltz、Chai、ProteinMPNN 等 |
| [rules/pathway-analysis.md](rules/pathway-analysis.md) | KEGG、Reactome、STRING |
| [rules/clinical-data.md](rules/clinical-data.md) | ClinicalTrials、ClinVar、FDA |

## 工具分类统计

| 分类 | 工具数量 | 示例 |
|----------|-------|----------|
| 蛋白质结构 | 23 | fetch_pdb_metadata、get_alphafold_prediction |
| 文献检索 | 14 | search_pubmed、arxiv_search、biorxiv_search_keywords |
| 基因组学 | 27 | lookup_gene、vep_predict、search_gwas_associations_by_trait |
| 化学信息学 | 20 多个 | calculate_molecular_properties、chembl_similarity_search |
| 分子生物学 | 15 | design_primers、restriction_digest、assemble_gibson |
| 结构预测 | 15 多个 | submit_boltz_prediction、submit_proteinmpnn_prediction |
| 通路分析 | 24 | analyze_gene_list、get_string_network |
| 临床数据 | 22 | search_clinical_trials、search_clinvar |

## 常见错误

1. **未查看工具的接口规范** → 导致参数使用错误
2. **忽略数据质量指标** → 使用不可靠的数据
3. **选择错误的工具** → 请参考规则文件中的工具选择指南
4. **未定期检查任务进度** → 从而错过预测结果

---

**提示**：如有疑问，可以尝试使用以下接口查询工具信息：`GET /api/v1/tools/search?q=your_query`