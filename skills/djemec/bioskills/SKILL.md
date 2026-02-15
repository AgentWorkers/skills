---
name: bioskills
description: "安装了425项生物信息学技能，涵盖序列分析、RNA-seq（RNA测序）、单细胞分析、变异检测、宏基因组学、结构生物学等56个类别。在配置生物信息学功能时，或当某个生物信息学任务需要尚未安装的专门技能时，可以使用这些工具。"
metadata: {"openclaw":{"requires":{"bins":["git"],"anyBins":["python3","Rscript"]},"os":["darwin","linux"],"emoji":"🧬"}}
---

# bioSkills 安装器

这是一个元技能工具，用于安装 bioinformatics 分析所需的全部 bioSkills 工具集（共 425 项技能，涵盖 62 个类别）。

## 安装方法

运行捆绑的安装脚本，以下载并安装所有 bioSkills 工具：

```bash
bash scripts/install-bioskills.sh
```

或者仅安装特定类别的工具：

```bash
bash scripts/install-bioskills.sh --categories "single-cell,variant-calling,differential-expression"
```

## 安装内容

| 类别组 | 包含的类别 | 技能数量 |
|----------------|-----------|--------|
| 序列与比对 | sequence-io、sequence-manipulation、alignment、alignment-files、database-access | 40 |
| 读取与处理 | read-qc、read-alignment | 11 |
| RNA 测序与表达分析 | differential-expression、rna-quantification、expression-matrix | 14 |
| 单细胞与空间生物学 | single-cell、spatial-transcriptomics | 25 |
| 变异分析 | variant-calling、copy-number、phasing-imputation | 21 |
| 表观基因组学 | chip-seq、atac-seq、methylation-analysis、hi-c-analysis | 25 |
| 微生物组学 | metagenomics、microbiome | 13 |
| 基因组学与组装 | genome-assembly、genome-annotation、genome-intervals、genome-engineering、primer-design | 29 |
| 基因调控与因果关系 | gene-regulatory-networks、causal-genomics、rna-structure | 13 |
| 时间序列与生态基因组学 | temporal-genomics、ecological-genomics | 11 |
| 免疫学与临床基因组学 | immunoinformatics、clinical-databases、tcr-bcr-analysis、epidemiological-genomics | 25 |
| 专业组学技术 | proteomics、metabolomics、alternative-splicing、chemoinformatics、liquid-biopsy | 36 |
| RNA 生物学 | small-rna-seq、epitranscriptomics、clip-seq、ribo-seq | 20 |
| 系统发育与进化生物学 | phylogenetics、population-genetics、comparative-genomics | 16 |
| 结构生物学与系统生物学 | structural-biology、systems-biology | 11 |
| 筛选与细胞分析 | crispr-screens、flow-cytometry、imaging-mass-cytometry | 22 |
| 通路分析与整合 | pathway-analysis、multi-omics-integration、restriction-analysis | 14 |
| 基础设施工具 | data-visualization、machine-learning、workflow-management、reporting、experimental-design、long-read-sequencing | 39 |
| 工作流程 | 从 FASTQ 数据到最终结果的端到端处理流程 | 40 |

## 安装后的使用方式

安装完成后，系统会根据当前任务自动选择并使用相应的 bioSkills 工具。例如：

- “我拥有处理前后的 RNA 测序数据，需要找出差异表达的基因”
- “从这个全基因组测序的 BAM 文件中调用变异信息”
- “对单细胞 RNA 测序数据进行聚类分析并找出标记基因”
- “预测这个蛋白质序列的结构”
- “对这些测序数据执行微生物组分类分析”

## 来源

GitHub: https://github.com/GPTomics/bioSkills

## 相关技能

安装完成后，您将可以使用以下 425 项技能：

- sequence-io、sequence-manipulation、database-access、alignment、alignment-files
- variant-calling、phylogenetics、differential-expression、structural-biology
- single-cell、pathway-analysis、restriction-analysis、methylation-analysis
- chip-seq、metagenomics、long-read-sequencing、read-qc、read-alignment
- rna-quantification、genome-assembly、genome-intervals、data-visualization
- expression-matrix、copy-number、proteomics、flow-cytometry、population-genetics
- multi-omics-integration、spatial-transcriptomics、machine-learning
- workflow-management、microbiome、metabolomics、phasing-imputation
- primer-design、hi-c-analysis、imaging-mass-cytometry、atac-seq
- crispr-screens、reporting、experimental-design、clinical-databases
- tcr-bcr-analysis、small-rna-seq、epitranscriptomics、clip-seq、ribo-seq
- genome-engineering、systems-biology、epidemiological-genomics
- immunoinformatics、comparative-genomics、alternative-splicing
- chemoinformatics、liquid-biopsy、genome-annotation
- gene-regulatory-networks、causal-genomics、rna-structure
- temporal-genomics、ecological-genomics
- workflows