---
name: lobster-use
description: >
  使用Lobster AI执行生物信息学分析，支持单细胞RNA测序（single-cell RNA-seq）、批量RNA测序（bulk RNA-seq）、基因组学（VCF/GWAS）、蛋白质组学（质谱/亲和力分析）、代谢组学（LC-MS/GC-MS/NMR）以及机器学习（特征选择、生存分析）等任务。此外，该工具还具备文献搜索、数据集发现和数据可视化功能。适用于处理生物数据、组学分析或生物信息学相关任务。支持的文件格式包括H5AD、CSV、VCF、PLINK、10X以及mzML；数据源支持GEO/SRA/PRIDE/MetaboLights等平台。
  **常用命令/短语：**  
  - 分析细胞数据：`analyze cells`  
  - 在PubMed中搜索文献：`search PubMed`  
  - 下载GEO数据：`download GEO`  
  - 运行质量控制（QC）：`run QC`  
  - 数据聚类：`cluster`  
  - 寻找基因标记：`find markers`  
  - 差异表达分析：`differential expression`  
  - 绘制UMAP图谱：`UMAP`  
  - 单细胞分析：`single-cell`  
  - RNA测序：`RNA-seq`  
  - 基因组关联研究（GWAS）：`GWAS`  
  - 蛋白质组学分析：`proteomics`  
  - 质谱分析：`mass spec`  
  - 代谢组学分析：`metabolomics`  
  - 使用MetaboLights平台：`MetaboLights`  
  - 数据可视化：`visualization`  
  **使用前提：**  
  - 确保已安装并正确配置Lobster软件。如遇到配置问题，请用户运行`lobster config-test`命令检查并修复错误后再继续使用。
required_binaries:
  - lobster
  - python3
primary_credential: LLM_PROVIDER_API_KEY
required_env_vars:
  - name: ANTHROPIC_API_KEY
    required: one_of_provider
    description: Anthropic Claude API key
  - name: GOOGLE_API_KEY
    required: one_of_provider
    description: Google Gemini API key
  - name: OPENAI_API_KEY
    required: one_of_provider
    description: OpenAI API key
  - name: OPENROUTER_API_KEY
    required: one_of_provider
    description: OpenRouter API key (600+ models)
  - name: AWS_ACCESS_KEY_ID
    required: one_of_provider
    description: AWS Bedrock access key (must be paired with AWS_SECRET_ACCESS_KEY)
  - name: AWS_SECRET_ACCESS_KEY
    required: one_of_provider
    description: AWS Bedrock secret key (must be paired with AWS_ACCESS_KEY_ID)
  - name: AZURE_AI_ENDPOINT
    required: one_of_provider
    description: Azure AI endpoint URL (must be paired with AZURE_AI_CREDENTIAL)
  - name: AZURE_AI_CREDENTIAL
    required: one_of_provider
    description: Azure AI API credential (must be paired with AZURE_AI_ENDPOINT)
  - name: NCBI_API_KEY
    required: false
    description: NCBI API key for faster PubMed/GEO access (recommended)
credential_note: |
  Exactly ONE LLM provider is required (not all). Choose one provider and set
  only that provider's env var(s). Paired credentials (AWS, Azure) must both be set.
declared_writes:
  - .lobster_workspace/                        # Workspace data, session state, outputs
  - .lobster_workspace/.env                    # Provider credential (workspace-scoped, mode 0600)
  - .lobster_workspace/provider_config.json    # Provider selection config
  - ~/.config/lobster/credentials.env          # ONLY if --global flag is used (not default)
  - ~/.config/lobster/providers.json           # ONLY if --global flag is used (not default)
network_access:
  - docs.omics-os.com                          # On-demand documentation fetches
  - LLM provider API endpoint                  # Whichever single provider is configured
  - eutils.ncbi.nlm.nih.gov                   # PubMed/GEO search (Research Agent only)
  - ftp.ncbi.nlm.nih.gov                      # GEO/SRA dataset downloads (Data Expert only)
  - www.ebi.ac.uk                              # PRIDE/MetaboLights (Research Agent only)
source:
  github: https://github.com/the-omics-os/lobster
  pypi: https://pypi.org/project/lobster-ai/
always: false
---
# Lobster AI 使用指南

Lobster AI 是一个多代理的生物信息学平台。用户可以使用自然语言描述分析需求，Lobster 会自动将请求路由到 10 个软件包中的 22 个专业代理。

## 系统要求

- **二进制文件**：`lobster` 命令行工具（`pip install lobster-ai`），Python 3.12 或更高版本
- **凭证**：需要设置一个 LLM（大型语言模型）提供商的密钥作为环境变量（并非所有代理都需要）：
  - `ANTHROPIC_API_KEY` | `GOOGLE_API_KEY` | `OPENAI_API_KEY` | `OPENROUTER_API_KEY`
  - `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY`（适用于 Bedrock 平台）
  - `AZURE.AI_ENDPOINT` + `AZURE.AI_CREDENTIAL`（适用于 Azure 平台）
  - Ollama：无需密钥（使用本地模型）
- **可选**：`NCBI_API_KEY` 可用于更快地查询 PubMed 和 GEO 数据
- **输出路径**：数据文件保存在 `.lobster_workspace/` 目录下，凭证信息保存在 `.env` 文件中（权限设置为 0600）
- **全局配置**：可以通过 `--global` 标志进行配置（默认不使用），配置文件位于 `~/.config/lobster/` 目录下
- **网络连接**：需要连接到 LLM 提供商的 API 以及公共生物数据库（如 GEO、SRA、PRIDE、MetaboLights）

## 文档查找

Lobster AI 的文档网站（`docs.omics-os.com`）提供了适合 LLM 阅读的原始 Markdown 格式文档：

| 路由 | 用途 |
|-------|-----|
| `/llms.txt` | 所有页面的索引（包含标题、URL 和描述） |
| `/llms-full.txt` | 所有免费页面的完整内容 |
| `/raw/docs/{slug}.md` | 特定页面的原始 Markdown 文件 |

**工作流程**：首先获取 `/llms.txt` 文件以获取页面的路径，然后通过 `/raw/docs/{slug}.md` 获取具体页面的内容。
示例：`https://docs.omics-os.com/raw/docs/tutorials/single-cell-rnaseq.md`

## 两种使用模式

Lobster AI 支持以下两种使用模式：

**编排模式**：代理通过 `lobster query --json --session-id` 命令进行编程式调用，解析输出结果并执行多步骤分析。详情请参阅 [agent-patterns.md](references/agent-patterns.md)。

**指导模式**：代理会指导用户如何在 Lobster 的聊天界面或命令行中输入指令。请参考下面的路由表来确定需要获取的文档页面。

## 快速入门

```bash
# Install (PyPI -- preferred)
pip install 'lobster-ai[full]'
# or: uv tool install 'lobster-ai[full]'

# Configure (uses env var -- never pass raw keys on command line)
lobster init --non-interactive --anthropic-key "$ANTHROPIC_API_KEY" --profile production

# Run analysis (always pass -w and --session-id together)
lobster query -w ./my_analysis --session-id "proj" --json "Download GSE109564 and run QC"

# Inspect workspace (no tokens burned, ~300ms)
lobster command data --json -w ./my_analysis
```

**来源**：[github.com/the-omics-os/lobster](https://github.com/the-omics-os/lobster)  
**PyPI**：[pypi.org/project/lobster-ai](https://pypi.org/project/lobster-ai/)

## 路由表

| 操作需求 | 对应文档路径 | 参考文档 |
|---|---|---|
| **安装与配置** | `getting-started/installation` | -- |
| **配置选项** | `getting-started/configuration` | -- |
| **使用命令行工具** | `guides/cli-commands` | [cli-reference.md](references/cli-reference.md) |
| **编程式编排** | -- | [agent-patterns.md](references/agent-patterns.md) |
| **分析单细胞 RNA 测序数据** | `tutorials/single-cell-rnaseq` | -- |
| **分析批量 RNA 测序数据** | `tutorials/bulk-rnaseq` | -- |
| **分析蛋白质组学数据** | `tutorials/proteomics` | -- |
| **了解数据格式** | `guides/data-formats` | -- |
| **搜索文献/数据集** | `agents/research` | -- |
| **分析基因组学数据** | `agents/genomics` | -- |
| **分析代谢组学数据** | `case-studies/metabolomics` | -- |
| **机器学习/特征选择** | `agents/ml` | -- |
| **药物发现** | `agents/drug-discovery` | -- |
| **结果可视化** | `agents/visualization` | -- |
| **故障排除** | `support/troubleshooting` | -- |
| **查看案例研究** | `case-studies/{domain}` | -- |
| **查看所有代理功能** | `agents` | -- |
| **扩展 Lobster 功能（开发模式）** | -- | 使用 `lobster-dev` 技能 |

**获取文档页面的示例**：`https://docs.omics-os.com/raw/docs/{slug}.md`

## 重要规则

1. **多步骤分析时必须使用 `--session-id`** —— 这样数据会在多次请求中保持一致
2. **使用 `lobster command --json` 命令检查工作空间状态** —— 这样不会消耗令牌，耗时约 300 毫秒
3. **只有“Research Agent”具有网络访问权限** —— 其他代理都在处理已加载的数据
4. **分析前必须进行质量控制** —— 必须先评估数据质量
5. **编程解析输出时使用 `--json` 标志** |
6. **运行分析步骤前请确认数据已加载**（使用 `lobster command data --json`）
7. **默认工作空间为 `.lobster_workspace/` —— 可通过 `-w <path>` 进行自定义 |
8. **文档内容按需从 `docs.omics-os.com/raw/docs/{slug}.md` 获取** —— 不要自行猜测工作流程

## 代理概述

Lobster AI 包含 22 个代理，分别属于 10 个不同的软件包。Lobster 会根据用户的自然语言请求自动选择合适的代理进行处理：

| 代理 | 所属软件包 | 负责的任务 |
|---|---|---|
| **Supervisor** | lobster-ai | 路由请求、协调各个代理的工作 |
| **Research Agent** | lobster-research | 查询 PubMed、GEO、SRA、PRIDE、MetaboLights 等数据库 |
| **Data Expert** | lobster-research | 文件加载、下载、格式转换（离线操作） |
| **Transcriptomics Expert** | lobster-transcriptomics | 单细胞 RNA 测序和批量 RNA 测序的数据处理（包括质量控制、聚类分析） |
| **Annotation Expert** | lobster-transcriptomics | 细胞类型注释、基因集富集分析 |
| **DE Analysis Expert** | lobster-transcriptomics | 差异表达分析、假批量数据分析（GSEA） |
| **Proteomics Expert** | lobster-proteomics | 蛋白质组学分析（包括质量控制、标准化、批量校正） |
| **Proteomics DE Expert** | lobster-proteomics | 蛋白质差异表达分析、通路富集、STRING PPI 分析 |
| **Biomarker Discovery** | lobster-proteomics | 生物标志物筛选、嵌套方差分析、核心蛋白识别 |
| **Metabolomics Expert** | lobster-metabolomics | 质谱数据分析（LC-MS/GC-MS/NMR）、数据标准化、PCA/PLS-DA 分析、注释 |
| **Genomics Expert** | lobster-genomics | VCF/PLINK 文件处理、基因组关联分析（GWAS）、变异注释 |
| **Variant Analysis Expert** | lobster-genomics | VEP 注释、ClinVar 分析、临床优先级评估 |
| **ML Expert** | lobster-ml | 机器学习预处理、特征选择、数据导出 |
| **Feature Selection Expert** | lobster-ml | 特征稳定性分析、LASSO 算法、方差过滤 |
| **Survival Analysis Expert** | lobster-ml | Cox 模型、Kaplan-Meier 分析、风险分层 |
| **Drug Discovery Expert** | lobster-drug-discovery | 药物靶点验证、化合物特性分析 |
| **Cheminformatics Expert** | lobster-drug-discovery | 分子描述符分析、化合物相似性比较 |
| **Clinical Dev Expert** | lobster-drug-discovery | 临床试验设计、终点分析、安全性评估 |
| **Pharmacogenomics Expert** | lobster-drug-discovery | 药物-基因相互作用分析 |
| **Visualization Expert** | lobster-visualization | 数据可视化（UMAP、热图、火山图等） |
| **Metadata Assistant** | lobster-metadata | 数据元信息管理、元数据标准化 |
| **Protein Structure Viz** | lobster-structural-viz | PDB 数据获取、PyMOL 可视化工具、RMSD 计算 |

**每个代理的详细文档**：`https://docs.omics-os.com/raw/docs/agents/{domain}.md`