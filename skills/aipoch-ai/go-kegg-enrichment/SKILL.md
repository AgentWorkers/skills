---
name: go-kegg-enrichment
description: >
  对基因列表进行GO（基因本体）和KEGG通路富集分析。  
  触发条件：  
  - 用户提供基因列表（符号或ID）并请求进行富集分析  
  - 用户提及“GO富集”、“KEGG富集”或“通路分析”  
  - 用户希望了解基因集的生物学功能  
  - 用户提供差异表达基因（DEGs）并请求对其进行解释  
  输入：  
  - 基因列表（文件形式或直接输入）  
  - 生物体（人类/小鼠/大鼠）  
  - 背景基因集（可选）  
  输出：  
  - 富集术语  
  - 统计结果  
  - 可视化结果（条形图、点图、富集图）
  \ gene lists.\nTrigger when: \n- User provides a list of genes (symbols or IDs)\
  \ and asks for enrichment analysis\n- User mentions \"GO enrichment\", \"KEGG enrichment\"\
  , \"pathway analysis\"\n- User wants to understand biological functions of gene\
  \ sets\n- User provides differentially expressed genes (DEGs) and asks for interpretation\n\
  - Input: gene list (file or inline), organism (human/mouse/rat), background gene\
  \ set (optional)\n- Output: enriched terms, statistics, visualizations (barplot,\
  \ dotplot, enrichment map)"
version: 1.0.0
category: Bioinfo
tags: []
author: AIPOCH
license: MIT
status: Draft
risk_level: Medium
skill_type: Tool/Script
owner: AIPOCH
reviewer: ''
last_updated: '2026-02-06'
---
# GO/KEGG富集分析

这是一个自动化流程，用于基因本体（GO）和KEGG通路富集分析，并提供结果解释和可视化功能。

## 特点

- **GO富集**：生物过程（BP）、分子功能（MF）、细胞组分（CC）
- **KEGG通路**：具有特定生物体映射的通路富集分析
- **支持多种ID类型**：基因符号、Entrez ID、Ensembl ID、RefSeq
- **统计方法**：超几何检验、Fisher精确检验、GSEA（基因表达显著性分析）支持
- **可视化**：条形图、点图、富集图、cnet图
- **结果解释**：自动生成生物学显著性总结

## 支持的生物体

| 常见名称 | 学名 | KEGG代码 | OrgDB包 |
|-------------|-----------------|-----------|---------------|
| 人类 | Homo sapiens | hsa | org.Hs.eg.db |
| 小鼠 | Mus musculus | mmu | org.Mm.eg.db |
| 大鼠 | Rattus norvegicus | rno | org.Rn.eg.db |
| 斑马鱼 | Danio rerio | dre | org.Dr.eg.db |
| 果蝇 | Drosophila melanogaster | dme | org.Dm.eg.db |
| 酵母 | Saccharomyces cerevisiae | sce | org.Sc.sgd.db |

## 使用方法

### 基本用法

```python
# Run enrichment analysis with gene list
python scripts/main.py --genes gene_list.txt --organism human --output results/
```

### 参数

| 参数 | 描述 | 默认值 | 是否必填 |
|-----------|-------------|---------|----------|
| `--genes` | 基因列表文件路径（每行一个基因） | - | 是 |
| `--organism` | 生物体代码（human/mouse/rat/zebrafish/fly/yeast） | human | 否 |
| `--id-type` | 基因ID类型（符号/entrez/ensembl/refseq） | symbol | 否 |
| `--background` | 背景基因列表文件 | 所有基因 | 否 |
| `--pvalue-cutoff` | 显著性的P值阈值 | 0.05 | 否 |
| `--qvalue-cutoff` | 调整后的P值（q值）阈值 | 0.2 | 否 |
| `--analysis` | 分析类型（go/kegg/all） | all | 否 |
| `--output` | 输出目录 | ./enrichment_results | 否 |
| `--format` | 输出格式（csv/tsv/excel/all） | all | 否 |

### 高级用法

```python
# GO enrichment only with specific ontology
python scripts/main.py \
    --genes deg_upregulated.txt \
    --organism mouse \
    --analysis go \
    --go-ontologies BP,MF \
    --pvalue-cutoff 0.01 \
    --output go_results/

# KEGG enrichment with custom background
python scripts/main.py \
    --genes treatment_genes.txt \
    --background all_expressed_genes.txt \
    --organism human \
    --analysis kegg \
    --qvalue-cutoff 0.05 \
    --output kegg_results/
```

## 输入格式

### 基因列表文件
```
TP53
BRCA1
EGFR
MYC
KRAS
PTEN
```

### 带表达值的数据（用于GSEA）
```
gene,log2FoldChange
TP53,2.5
BRCA1,-1.8
EGFR,3.2
```

## 输出文件

```
output/
├── go_enrichment/
│   ├── GO_BP_results.csv       # Biological Process results
│   ├── GO_MF_results.csv       # Molecular Function results
│   ├── GO_CC_results.csv       # Cellular Component results
│   ├── GO_BP_barplot.pdf       # Visualization
│   ├── GO_MF_dotplot.pdf
│   └── GO_summary.txt          # Interpretation summary
├── kegg_enrichment/
│   ├── KEGG_results.csv        # Pathway results
│   ├── KEGG_barplot.pdf
│   ├── KEGG_dotplot.pdf
│   └── KEGG_pathview/          # Pathway diagrams
└── combined_report.html        # Interactive report
```

## 结果解释

该工具自动生成以下生物学解释内容：

1. **Top Enriched Terms**：按富集比例排序的显著GO术语/通路
2. **Functional Themes**：从富集术语中聚类的生物学主题
3. **Key Genes**：在显著术语中起主导作用的核心基因
4. **Network Relationships**：基因-术语关系可视化
5. **Clinical Relevance**：人类基因的疾病关联

## 技术难度：**高**

⚠️ **AI自主验收状态**：需要人工审核

使用该工具需要以下条件：
- 具备R/Bioconductor环境及clusterProfiler工具
- 多个注释数据库（org.*.eg.db）
- KEGG REST API访问权限
- 复杂的可视化工具依赖

## 依赖项

### 必需的R包
```r
install.packages(c("BiocManager", "ggplot2", "dplyr", "readr"))
BiocManager::install(c(
    "clusterProfiler", 
    "org.Hs.eg.db", "org.Mm.eg.db", "org.Rn.eg.db",
    "enrichplot", "pathview", "DOSE"
))
```

### Python依赖项
```bash
pip install pandas numpy matplotlib seaborn rpy2
```

## 示例工作流程

1. **准备输入数据**：从差异表达基因（DEG）分析中生成基因列表
2. **运行分析**：使用适当的参数执行main.py
3. **审查结果**：检查生成的CSV文件和可视化结果
4. **解读结果**：阅读自动生成的生物学解释摘要

## 参考资料

请参阅`references/`目录，其中包含：
- clusterProfiler文档
- KEGG API指南
- 统计方法说明
- 可视化示例

## 限制

- 需要互联网连接以查询KEGG数据库
- 基因列表过长（>5000个基因）可能需要更多内存
- 部分通路可能不适用于所有生物体
- KEGG API有请求速率限制（每秒最多3次请求）

## 风险评估

| 风险指标 | 评估内容 | 风险等级 |
|----------------|------------|-------|
| 代码执行 | 在本地执行的Python/R脚本 | 中等 |
| 网络访问 | 无外部API调用 | 低 |
| 文件系统访问 | 读取输入文件、写入输出文件 | 中等 |
| 指令篡改 | 有标准的提示和指导 | 低 |
| 数据泄露 | 输出文件保存在工作区 | 低 |

## 安全性检查

- [ ] 无硬编码的凭证或API密钥
- [ ] 无未经授权的文件系统访问
- [ ] 输出文件不包含敏感信息
- [ ] 有防止脚本注入的保护措施
- [ ] 输入文件路径经过验证（防止遍历外部目录）
- [ ] 输出目录限制在工作区内
- [ ] 脚本在沙箱环境中执行
- [ ] 错误信息经过处理（不显示堆栈跟踪）
- [ ] 依赖项经过审核

## 先决条件

```bash
# Python dependencies
pip install -r requirements.txt
```

## 评估标准

### 成功指标
- [ ] 能够成功执行主要功能
- [ ] 输出符合质量标准
- [ ] 良好地处理边缘情况
- [ ] 性能表现可接受

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
  - 新功能的添加