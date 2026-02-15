---
name: bioskills
description: "安装了412项生物信息学技能，涵盖序列分析、RNA-seq（RNA测序）、单细胞分析、变异检测、宏基因组学、结构生物学等54个类别。在配置生物信息学功能时，或在需要尚未安装的专门技能来处理生物信息学任务时，可以使用这些技能。"
metadata: {"openclaw":{"requires":{"anyBins":["python3","Rscript"]},"os":["darwin","linux"],"emoji":"🧬"}}
---

# bioSkills 安装器

这是一个元技能工具，用于安装完整的 bioSkills 组件（包含 60 个类别下的 412 项生物信息学分析技能）。

## 安装方法

运行捆绑的安装脚本以下载并安装所有 bioSkills 组件：

```bash
bash scripts/install-bioskills.sh
```

或者仅安装特定的类别：

```bash
bash scripts/install-bioskills.sh --categories "single-cell,variant-calling,differential-expression"
```

## 安装内容

| 类别组 | 包含的类别 | 技能             |
|----------------|------------------|-------------------|
| 序列与比对       | sequence-io, sequence-manipulation, alignment, alignment-files, database-access | 40             |
| 读取处理       | read-qc, read-alignment        | 11                |
| RNA 测序与表达分析   | differential-expression, rna-quantification, expression-matrix | 14                |
| 单细胞与空间生物学   | single-cell, spatial-transcriptomics     | 25                |
| 变异分析       | variant-calling, copy-number, phasing-imputation | 21                |
| 表观基因组学     | chip-seq, atac-seq, methylation-analysis, hi-c-analysis | 25                |
| 微生物组学       | metagenomics, microbiome        | 13                |
| 基因组学与组装     | genome-assembly, genome-annotation, genome-intervals, genome-engineering | 29                |
| 调控机制与因果关系   | gene-regulatory-networks, causal-genomics, rna-structure | 13                |
| 免疫学与临床医学   | immunoinformatics, clinical-databases, tcr-bcr-analysis, epidemiological-genomics | 25                |
| 特化组学技术     | proteomics, metabolomics, alternative-splicing, chemoinformatics | 36                |
| RNA 生物学       | small-rna-seq, epitranscriptomics, clip-seq, ribo-seq    | 20                |
| 系统发育与进化     | phylogenetics, population-genetics, comparative-genomics | 16                |
| 结构生物学与系统生物学 | structural-biology, systems-biology    | 11                |
| 筛选与细胞分析     | crispr-screens, flow-cytometry, imaging-mass-cytometry | 22                |
| 通路分析与整合     | pathway-analysis, multi-omics-integration, restriction-analysis | 14                |
| 基础设施       | data-visualization, machine-learning, workflow-management, reporting | 39                |
| 工作流程       | End-to-end pipelines (FASTQ 到结果)     | 38                |

## 安装后的使用方式

安装完成后，相关技能会根据当前的任务自动被触发。例如：

- “我有处理前后的 RNA 测序数据，请找出差异表达的基因”
- “从这个全基因组测序的 BAM 文件中调用变异信息”
- “对单细胞 RNA 测序数据进行聚类分析并找出标记基因”
- “预测这个蛋白质序列的结构”
- “对这些高通量测序数据执行微生物组分类分析”

## 来源

GitHub: https://github.com/GPTomics/bioSkills

## 相关技能

安装完成后，您将可以使用以下 412 项技能：

- sequence-io
- sequence-manipulation
- database-access
- alignment
- alignment-files
- variant-calling
- phylogenetics
- differential-expression
- structural-biology
- single-cell
- pathway-analysis
- restriction-analysis
- methylation-analysis
- chip-seq
- metagenomics
- long-read-sequencing
- read-qc
- read-alignment
- rna-quantification
- genome-assembly
- genome-intervals
- data-visualization
- expression-matrix
- copy-number
- proteomics
- flow-cytometry
- population-genetics
- multi-omics-integration
- spatial-transcriptomics
- machine-learning
- workflow-management
- microbiome
- metabolomics
- phasing-imputation
- primer-design
- hi-c-analysis
- imaging-mass-cytometry
- atac-seq
- crispr-screens
- reporting
- experimental-design
- clinical-databases
- tcr-bcr-analysis
- small-rna-seq
- epitranscriptomics
- clip-seq
- ribo-seq
- genome-engineering
- systems-biology
- epidemiological-genomics
- immunoinformatics
- comparative-genomics
- alternative-splicing
- chemoinformatics
- liquid-biopsy
- genome-annotation
- gene-regulatory-networks
- causal-genomics
- rna-structure
- workflows