---
name: lobster-use
description: |
  Analyze biological data using Lobster AI — single-cell RNA-seq, bulk RNA-seq,
  literature mining, dataset discovery, quality control, and visualization.
  
  USE THIS SKILL WHEN:
  - Analyzing single-cell or bulk RNA-seq data
  - Searching PubMed/GEO for papers or datasets
  - Running quality control on biological data
  - Clustering cells, finding markers, differential expression
  - Creating publication-quality visualizations
  - Working with H5AD, CSV, 10X, GEO/SRA accessions
  
  TRIGGER PHRASES: "analyze cells", "search PubMed", "download GEO", "run QC",
  "cluster", "find markers", "differential expression", "UMAP", "volcano plot",
  "single-cell", "RNA-seq", "bioinformatics"
  
  ASSUMES: Lobster is installed and configured. For setup issues, tell user to
  run `lobster config-test` and fix any errors before proceeding.
---

# Lobster AI 使用指南

Lobster AI 是一个多智能体的生物信息学平台。您可以通过自然语言或斜杠命令与之交互，Lobster 会自动将请求路由到相应的专业智能体。

## 安装

如果尚未安装 Lobster，请指导用户根据其使用的平台执行相应的命令：

### macOS / Linux
```bash
curl -fsSL https://install.lobsterbio.com | bash
```

### Windows (PowerShell)
```powershell
irm https://install.lobsterbio.com/windows | iex
```

### 手动安装（适用于所有平台）
```bash
uv tool install 'lobster-ai[full,anthropic]' && lobster init
# or: pip install 'lobster-ai[full]' && lobster init
```

安装完成后，运行 `lobster init` 命令以配置 API 密钥并选择所需的智能体包。

## 升级
- 使用 `uv tool` 升级：`uv tool upgrade lobster-ai`
- 使用 `pip` 升级：`pip install --upgrade lobster-ai`

## 添加智能体（使用 `uv tool`）

已安装 `uv tool` 的用户可以通过以下命令添加智能体：
`uv tool install lobster-ai --with lobster-transcriptomics --with lobster-proteomics`
运行 `lobster init` 后，系统会指导您完成这一过程并生成相应的命令。

## 快速参考

| 任务 | 参考文档 |
|------|-----------|
| **命令行界面（CLI）命令** | [references/cli-commands.md](references/cli-commands.md) |
| **单细胞分析** | [references/single-cell-workflow.md](references/single-cell-workflow.md) |
| **批量 RNA-seq 分析** | [references/bulk-rnaseq-workflow.md](references/bulk-rnaseq-workflow.md) |
| **文献与数据集** | [references/research-workflow.md](references/research-workflow.md) |
| **可视化** | [references/visualization.md](references/visualization.md) |
| **可用智能体** | [references/agents.md](references/agents.md) |

## 交互方式

### 交互式聊天
```bash
lobster chat                          # Start interactive session
lobster chat --workspace ./myproject  # Custom workspace
lobster chat --reasoning              # Enable detailed reasoning
```

### 单次查询
```bash
lobster query "Your request"
lobster query --session-id latest "Follow-up request"
```

## 核心操作模式

### 自然语言交互（主要方式）
只需描述您的需求即可：
```
"Download GSE109564 and run quality control"
"Cluster the cells and find marker genes"
"Compare hepatocytes vs stellate cells"
```

### 斜杠命令（系统操作）
```
/data                    # Show loaded data info
/files                   # List workspace files
/workspace list          # List available datasets
/workspace load 1        # Load dataset by index
/plots                   # Show generated visualizations
/save                    # Save current session
/status                  # Show system status
/help                    # All commands
```

### 会话连续性
```bash
# Start named session
lobster query --session-id "my_analysis" "Load GSE109564"

# Continue with context
lobster query --session-id latest "Now cluster the cells"
lobster query --session-id latest "Find markers for cluster 3"
```

## 智能体系统

Lobster 会自动将请求路由到相应的专业智能体：

| 智能体 | 负责任务 |
|-------|---------|
| **管理员** | 路由请求、协调各个智能体 |
| **研究智能体** | PubMed 搜索、基因组定位（GEO）、论文提取 |
| **数据专家** | 文件加载、格式转换、数据下载 |
| **转录组学专家** | 单细胞 RNA-seq 分析（scRNA-seq）：数据质量控制（QC）、聚类、特征分析 |
| **差异表达分析专家** | 差异表达分析（DE analysis）、统计测试 |
| **注释专家** | 细胞类型注释、基因集富集 |
| **可视化专家** | 数据可视化（UMAP、热图、火山图等） |
| **蛋白质组学专家** | 质谱分析 |
| **基因组学专家** | VCF 文件处理、全基因组关联研究（GWAS）、变异分析 |
| **机器学习专家** | 数据嵌入、分类分析 |

## 工作空间与输出文件

**默认工作空间**：`.lobster_workspace/`

**输出文件格式**：
| 文件扩展名 | 文件内容 |
|-----------|---------|
| `.h5ad` | 处理后的数据对象 |
| `.html` | 交互式可视化结果 |
| `.png` | 适用于发表的图表 |
| `.csv` | 导出的表格数据 |
| `.json` | 元数据及数据来源信息 |

**输出文件管理**：
```
/files              # List all outputs
/plots              # View visualizations
/open results.html  # Open in browser
/read summary.csv   # Preview file contents
```

## 常见工作流程

```bash
# 1. Start session
lobster chat --workspace ./my_analysis

# 2. Load or download data
"Download GSE109564 from GEO"
# or
/workspace load my_data.h5ad

# 3. Quality control
"Run quality control and show me the metrics"

# 4. Analysis
"Filter low-quality cells, normalize, and cluster"

# 5. Interpretation
"Identify cell types and find marker genes"

# 6. Visualization
"Create UMAP colored by cell type"
/plots

# 7. Export
"Export marker genes to CSV"
/save
```

## 常见问题解决方法

| 问题 | 解决方法 |
|-------|-------|
| Lobster 无响应 | 运行 `lobster config-test` 检查配置 |
| 未加载数据 | 检查 `/data` 目录，使用 `/workspace list` 查看可用数据 |
| 分析失败 | 尝试使用 `--reasoning` 参数重新运行命令 |
| 输出文件缺失 | 检查 `/files` 目录及工作空间目录 |

## 文档资料

在线文档：**docs.omics-os.com**

主要文档章节：
- **命令行界面（CLI）命令**  
- **数据分析工作流程**  
- **单细胞 RNA-seq 分析教程**  
- **智能体相关文档**