---
name: bio-orchestrator
description: 元代理（Meta-agent）负责将生物信息学请求路由到相应的子技能（sub-skills）。它负责文件类型检测、分析计划制定、报告生成以及结果的可重复性导出（reproducibility export）等任务。
version: 0.1.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env: []
      config: []
    always: false
    emoji: "🧬"
    homepage: https://github.com/manuelcorpas/ClawBio
    os: [macos, linux]
    install:
      - kind: uv
        package: biopython
        bins: []
      - kind: uv
        package: pandas
        bins: []
---
# Bio Orchestrator

Bio Orchestrator 是一个用于生物信息学分析的元代理（meta-agent）。它的职责包括：

1. **理解用户的生物学问题**，并确定需要调用哪些专门的生物信息学工具（技能）。
2. **检测输入文件的类型**（如 VCF、FASTQ、BAM、CSV、PDB、h5ad），并将文件路由到相应的工具进行处理。
3. **在需要多个步骤的分析任务中**，规划这些步骤的顺序（例如：“先注释变异，再评估多样性”）。
4. **生成结构化的 Markdown 报告**，其中包含分析方法、结果、图表和参考文献。
5. **提供可复现性的分析环境**（包括conda环境配置、命令日志和数据校验信息）。

## 路由表

| 输入文件类型 | 路由目标 | 触发示例 |
|-------------|----------|------------------|
| VCF 文件或变异数据 | equity-scorer, vcf-annotator | “分析我的 VCF 文件中的变异多样性”，“注释变异” |
| FASTQ/BAM 文件 | seq-wrangler | “对我的测序数据进行处理”，“将数据比对到 GRCh38 基因组” |
| PDB 文件或蛋白质结构查询 | struct-predictor | “预测 BRCA1 蛋白的结构”，“与 AlphaFold 结果进行比较” |
| h5ad/Seurat 数据 | scrna-orchestrator | “对单细胞数据进行聚类分析”，“寻找标记基因” |
| 文献查询 | lit-synthesizer | “查找关于 X 的相关论文”，“总结 Y 领域的最新研究” |
| 祖先/群体信息 CSV 文件 | equity-scorer | “评估群体多样性”，“生成 HEIM 分析报告” |
| 请求生成可复现性分析环境 | repro-enforcer | “将分析过程导出为 Nextflow 工作流”，“创建可复现性容器” |

## 决策流程

收到生物信息学分析请求后，Bio Orchestrator 会执行以下步骤：

1. **识别文件类型**：检查文件的扩展名和头部信息，确认文件是否存在及其格式。
2. **匹配相应的工具**：根据上述路由表将文件路由到相应的工具。如果类型不明确，会请求用户进一步确认。
3. **检查依赖关系**：在调用工具之前，确保所需的软件已安装（例如 `which samtools`）。
4. **规划分析流程**：对于多步骤的分析任务，先制定详细的计划并获取用户确认。
5. **执行分析**：按顺序运行相应的工具，并在工具之间传递分析结果。
6. **生成报告**：生成包含以下内容的 Markdown 报告：
   - 分析方法（使用的工具、版本和参数）
   - 分析结果（表格、图表、关键发现）
   - 可复现性信息（用于重新执行的命令、conda 环境配置、数据校验信息）
7. **记录操作日志**：将所有操作记录到工作目录下的 `analysis_log.md` 文件中。

## 文件类型检测

```python
EXTENSION_MAP = {
    ".vcf": "equity-scorer",
    ".vcf.gz": "equity-scorer",
    ".fastq": "seq-wrangler",
    ".fastq.gz": "seq-wrangler",
    ".fq": "seq-wrangler",
    ".fq.gz": "seq-wrangler",
    ".bam": "seq-wrangler",
    ".cram": "seq-wrangler",
    ".pdb": "struct-predictor",
    ".cif": "struct-predictor",
    ".h5ad": "scrna-orchestrator",
    ".rds": "scrna-orchestrator",
    ".csv": "equity-scorer",  # default for tabular; inspect headers
    ".tsv": "equity-scorer",
}
```

## 报告模板

所有分析生成的报告都遵循以下结构：

```markdown
# Analysis Report: [Title]

**Date**: [ISO date]
**Skill(s) used**: [list]
**Input files**: [list with checksums]

## Methods
[Tool versions, parameters, reference genomes used]

## Results
[Tables, figures, key findings]

## Reproducibility
[Commands to re-run this exact analysis]
[Conda environment export]
[Data checksums (SHA-256)]

## References
[Software citations in BibTeX]
```

## 多工具协同处理示例

用户请求：“先注释 sample.vcf 文件中的变异，然后评估群体的多样性。”

**分析流程**：
1. 使用 vcf-annotator 工具对 sample.vcf 文件中的变异进行注释，并添加祖先信息。
2. 使用 equity-scorer 工具从注释后的 VCF 文件中计算群体多样性指标。
3. Bio Orchestrator 将这些结果整合到统一的报告中。

## 安全规则

- **未经用户明确许可，严禁将基因组数据上传到外部服务**。
- **在读取或写入文件之前，务必验证文件路径**。除非用户明确允许，否则禁止操作工作目录之外的文件。
- **详细记录所有操作**：记录每个执行的命令、读取/写入的文件以及使用的工具版本。
- **设置安全检查机制**：在执行任何可能破坏数据的操作（如覆盖文件、删除中间文件）之前，必须先征得用户同意。

## 常见查询示例：

- “这个文件是什么类型的？[文件路径]”
- “分析我的 1000 Genomes VCF 文件中的变异多样性”
- “对这些 FASTQ 文件进行全面的质量控制处理，并将数据比对到 hg38 基因组”
- “查找关于镰状细胞病中 CRISPR 基因编辑的最新研究论文”
- “预测这个蛋白质序列（MKWVTFISLLFLFSSAYS...）的结构”
- “将我的分析过程设置为可复现的 Nextflow 工作流”