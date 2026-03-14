---
name: dual-disease-transcriptomic-ml-planner
description: Generates complete dual-disease transcriptomic + machine learning research designs from a user-provided disease pair. Use when users want to identify shared DEGs, common hub genes, cross-disease biomarkers, or shared molecular mechanisms between two diseases using public GEO data. Triggers: "shared biomarker study for two diseases", "dual-disease transcriptomic ML paper", "identify common DEGs between disease A and B", "cross-disease hub gene discovery", "shared DEG + PPI + ROC design", "immune infiltration shared biomarker", or "I want to study disease X and Y together". Always outputs four workload configurations (Lite / Standard / Advanced / Publication+) with a recommended primary plan, step-by-step workflow, figure plan, validation strategy, minimal executable version, and publication upgrade path.
license: MIT
skill-author: AIPOCH
---

# 双疾病转录组学机器学习研究规划器

该工具可根据用户提供的疾病对生成完整的双疾病转录组学与机器学习研究设计。系统会输出四种工作配置方案，并推荐一个主要的研究计划。

## 支持的研究类型

| 类型 | 描述 | 示例 |
|-------|-------------|---------|
| **A. 共享差异表达基因（DEG）→ 中心基因** | 差异表达基因重叠 → 蛋白质相互作用（PPI）→ 中心基因共识 | 颅内动脉瘤 + 巨大动脉瘤；糖尿病 + 高血压性肾病 |
| **B. 双疾病共性机制** | 通路层面的共性 | 结合两种疾病的细胞外基质（ECM）、炎症、纤维化机制 |
| **C. PPI + 多算法中心基因优先级排序** | STRING + MCODE + CytoHubba 共识 | 任何具有足够共享差异表达基因的疾病对 |
| **D. 双疾病生物标志物验证** | 发现队列与验证队列中的ROC分析 | 每种疾病至少有两个GEO数据集的疾病对 |
| **E. 免疫浸润 + 共享生物标志物** | CIBERSORT/替代方法 + 基因-免疫细胞相关性分析 | 具有免疫活性的疾病对 |
| **F. 单基因跨疾病深度分析** | 两种疾病中的中心基因基因集富集分析（GSEA） | 具有高AUC值的单一关键中心基因 |
| **G. 以发表为导向的集成设计** | 完整的研究流程：差异表达基因 → 蛋白质相互作用 → ROC → 基因集富集 → 免疫分析 | 适用于高影响力论文的提交 |

## 最低用户输入要求

- 两个疾病或表型
- 如果提供的信息有限，系统会推断出一个合理的默认设计，并明确说明所有假设（规则9）

## 逐步执行流程

### 第1步：确定研究类型

识别：
- 疾病对及生物学主题（血管疾病、自身免疫疾病、纤维化疾病、代谢性疾病、神经退行性疾病、感染性疾病-肿瘤疾病、共病）
- 用户目标：共享生物标志物、共性机制、免疫相关性或发表潜力
- 机器学习在研究中的作用（是核心部分还是辅助工具）
- 是否适合进行免疫分析（参考规则5及下方的组织/工具选择指南）
- 资源限制：仅使用公共数据、每种疾病的数据集数量、时间限制、是否专注于单一基因

### 第2步：生成四种配置方案

系统会生成四种配置方案，并对每种方案进行描述，包括目标、所需数据、主要模块、预期工作量、预期成果图谱、优势与劣势。

| 配置 | 目标 | 时间框架 | 适用场景 |
|--------|------|-----------|----------|
| **基础型** | 共享差异表达基因 + 基础中心基因分析，每种疾病一个数据集 | 2–4周 | 适用于初步研究或撰写框架性论文 |
| **标准型** | 完整研究流程 + 验证分析 + ROC分析 + 单基因深度分析 | 5–9周 | 适用于核心论文的撰写 |
| **高级型** | 标准配置 + 免疫分析 + 基因集富集分析 + 多队列数据验证 | 9–14周 | 适用于竞争性期刊的提交 |
| **发表优化型** | 完整的多层次分析 + 实验建议 + 适用于审稿人评审的详细内容 | 12–20周 | 适用于高影响力论文的提交 |

### 第3步：推荐主要研究方案

根据疾病对的生物学特性、GEO数据的可用性、时间限制及发表目标，选择最合适的配置方案并说明原因。

### 第4步：详细的工作流程

每一步包括：步骤名称、目的、输入内容、方法、关键参数/阈值、预期输出、可能遇到的问题及替代方案。

**数据集与预处理**
- GEO数据集搜索：如果可行，每种疾病分别搜索一个发现队列和一个验证队列（参见[references/geo_search_and_tools.md]）
- 仅限组织类型的数据筛选：排除不适用于该疾病的血液/脑脊液数据；确保两种疾病使用相同类型的组织 |
- **组织选择规则**：选择与疾病病理最相关的组织；对于代谢性疾病，请参考组织/工具选择指南 |
- 平台兼容性检查：合并数据集前确认GPL ID是否匹配或可互操作 |
- 数据标准化；避免强制合并数据 |
- 疾病组与对照组的分组

**数据集层面的容错处理：**
- 如果某种疾病没有GEO数据集：说明不可行，并建议使用最接近的替代表型；降级为仅包含发现分析的基础型方案 |
- 如果每种疾病只有一个数据集：降级为基础型方案；明确说明无法进行验证ROC分析；并提供第二个队列的GEO数据搜索策略

**差异表达基因（DEG）与共享特征分析**
- 使用limma进行差异表达基因分析（logFC > 1–2，adj.p < 0.05）
- 绘制火山图、热图 |
- 绘制共享上调/下调差异表达基因的交集图（维恩图）
- 提供共享基因的汇总表

**差异表达基因交集的容错处理：**
- 如果共享差异表达基因数量为0：不进行蛋白质相互作用（PPI）/中心基因分析；按以下顺序采取补救措施：
  1. 将logFC阈值放宽至0.5（与原始结果一起报告）
  2. 将每种疾病的差异表达基因数量扩展到前500个 |
  3. 改用WGCNA共表达模块分析代替直接差异表达基因交集分析 |
  4. 重新评估疾病对是否具有共同的组织或生物学机制；如果不存在，则建议更换疾病对

**基因富集与共性机制分析**
- 使用GO富集（BP、MF、CC）和KEGG富集（clusterProfiler / DAVID）
- 绘制通路可视化图；总结共性生物学模块

**蛋白质相互作用（PPI）与中心基因优先级排序**
- 使用STRING构建蛋白质相互作用网络（置信度得分 > 0.4）
- 使用Cytoscape进行可视化；使用MCODE识别密集簇 |
- 使用CytoHubba进行多算法排名（至少需要5种算法：度数、MCC、介数、接近度、EPC）
- 根据中心基因的共识结果，筛选出前1/3/10个候选基因

**生物标志物性能评估**
- 进行ROC/AUC分析（pROC）；最低阈值AUC > 0.70 |
- 在发现队列和验证队列中进行ROC分析（适用于标准及以上配置）
- 在多个队列中验证基因表达情况

**ROC分析的容错处理：**
- 如果发现队列的AUC约为0.5：不将其视为生物标志物；将其标记为无信息性；考虑使用3–5个基因的迷你特征集代替单一中心基因 |
- 如果每个组中的基因数量少于30个：明确指出AUC可能存在膨胀风险；使用自助法计算置信区间；避免过度推广

**免疫浸润分析**（根据规则5，仅适用于相关疾病）
- 选择合适的去卷积工具（参见[references/tissue_and_tool_decisions.md]以获取针对不同组织类型的正确工具）
- 比较免疫细胞的比例；分析基因与免疫细胞的相关性（Spearman检验）
- 使用小提琴图、棒状图或热图展示相关性

**单基因深度分析**（适用于标准及以上配置）
- 按中心基因表达情况对样本进行分层 |
- 在两种疾病中进行单基因基因集富集分析；分析跨疾病的通路共性

### 第5步：成果图谱规划

提供完整的图谱列表和表格模板：[references/figure_plan_template.md]

核心图谱包括：工作流程示意图（图1）、差异表达基因火山图+维恩图（图2）、共享差异表达基因热图（图3）、GO/KEGG富集结果（图4）、蛋白质相互作用网络+MCODE排名（图5）、ROC曲线（图6）、免疫浸润相关分析（图7）、单基因基因集富集结果（图8）。表格包括：数据集概述、共享差异表达基因列表、中心基因排名、ROC/AUC总结。

### 第6步：验证与稳健性计划

明确每一步能够证明什么以及不能证明什么：
- **共享表达证据**：差异表达基因的重叠性及阈值的可重复性 |
- **中心基因优先级证据**：蛋白质相互作用网络的拓扑结构及多算法共识（关联关系，而非因果关系） |
- **生物标志物性能证据**：发现队列和验证队列中的ROC分析结果（诊断信号，而非机制证明） |
- **免疫支持证据**：免疫细胞分布的差异及基因-免疫细胞的相关性（仅用于关联分析；规则8） |
- **单基因机制支持证据**：基因集富集分析得出的通路主题（仅用于生成假设；规则7）

### 第7步：风险评估

包含自我评估部分，讨论以下内容：
- 研究设计中最强的部分 |
- 最依赖假设的部分（通常包括：小样本量导致的ROC结果膨胀；不同数据集之间的平台差异） |
- 最可能导致误判的环节（例如：中心基因排名中共享差异表达基因较少；AUC > 0.9但样本量少于50个的情况） |
- 最容易被误解的部分（例如：将免疫去卷积结果误解读为因果关系；将单一中心基因视为机制证明） |
- 审稿人可能提出的批评点：样本量小、缺乏实验验证、平台差异、单一生物标志物的过度解读、免疫去卷积方法的局限性、结直肠癌/感染性疾病的亚型差异 |
- 如果初步结果不理想，制定修订策略（例如：放宽差异表达基因的阈值、更换验证队列、使用迷你特征集）

### 第8步：最小执行版本

仅使用公共数据；每种疾病一个发现数据集；包括差异表达基因分析、维恩图、GO/KEGG结果、STRING分析、MCODE分析、CytoHubba分析结果、发现队列的ROC分析；提供一页的成果解释。建议在推荐方案前确认是否符合时间或数据集的限制。

### 第9步：研究方案升级路径

提供完整的升级方案影响分析表：[references/upgrade_path.md]

主要升级内容包括：每种疾病的验证队列数量（高/低-中等）、多算法中心基因共识（高/低）、跨平台结果的可重复性（高/中等）、免疫浸润分析（中等/中等）、单基因基因集富集（中等/中等）、迷你特征集（3–5个基因）。

## R代码框架指南

在提供R代码示例或研究流程框架时，请遵循以下规则：

1. **示例ID规范**：代码中的所有GEO访问号必须附带注释：`# 示例ID — 运行前请替换为实际的GSE访问号`
2. **零交集检查**：所有研究流程在差异表达基因分析后必须包含可行性检查：
   ```r
   if (length(shared_genes) == 0) {
     stop("No shared DEGs found. Recovery options: (1) relax logFC to 0.5, (2) use top-500 DEGs per disease, (3) switch to WGCNA co-expression module overlap.")
   }
   ```
3. **标准软件包列表**：包括GEOquery、limma、clusterProfiler、org.Hs.eg.db、pROC、igraph、STRINGdb、WGCNA。根据需要调用`BiocManager::install()`函数。
4. **GEO数据集搜索方法**：使用`GEOquery::getGEO("GSEsearch", ...)`或直接访问https://www.ncbi.nlm.nih.gov/geo/进行搜索

**标准R代码模板：**

```r
library(GEOquery); library(limma); library(clusterProfiler); library(pROC)

# Load datasets — EXAMPLE IDs: replace before running
gse_disease1 <- getGEO("GSEXXXXX", GSEMatrix = TRUE)[[1]]  # EXAMPLE ID
gse_disease2 <- getGEO("GSEXXXXX", GSEMatrix = TRUE)[[1]]  # EXAMPLE ID

# DEG analysis (repeat for disease2)
design <- model.matrix(~ group, data = pData(gse_disease1))
fit    <- eBayes(lmFit(exprs(gse_disease1), design))
deg_d1 <- subset(topTable(fit, coef = 2, adjust = "BH", number = Inf),
                 abs(logFC) > 1 & adj.P.Val < 0.05)

# Shared DEG intersection with zero-guard
shared_genes <- intersect(rownames(deg_d1), rownames(deg_d2))
if (length(shared_genes) == 0) {
  stop("No shared DEGs found. Recovery: relax logFC to 0.5 or use top-500 DEGs per disease.")
}

# ROC for top hub gene — EXAMPLE: replace 'HUB_GENE' and labels/scores with real data
roc_obj <- roc(response = labels, predictor = expr_scores)
cat("AUC:", auc(roc_obj), "\n")
if (auc(roc_obj) < 0.70) warning("AUC below 0.70 threshold. Consider mini-signature approach.")
```

## 规则说明

1. **必须输出所有四种配置方案，而不仅仅是其中一个通用方案。**
2. **必须推荐一个主要方案，并给出理由。**
3. **必须区分必要模块和可选模块。**
4. **明确区分共享表达证据、生物标志物性能证据、免疫支持证据和机制支持证据（参见第6步）。**
5. **如果疾病对不适合进行免疫分析，或者该组织类型的免疫去卷积方法不可靠，请不要继续进行相关分析。请参考[references/tissue_and_tool_decisions.md]选择合适的工具。**
6. **对于样本量较少（每个组中基因数量少于30个）或数据集不匹配的情况，不要夸大ROC分析的诊断价值。必须报告自助法计算的置信区间。**
7. **不要将单一中心基因视为机制证明；始终将其标记为“生物标志物候选基因”。**
8. **不要将免疫细胞相关性的结果误解读为因果关系。**
9. **如果用户提供的信息有限，系统会推断出一个合理的默认设计，并明确说明所有假设。**
10. **不要仅提供方法列表或文献综述。**
11. **如果请求内容超出范围（例如：仅涉及单一疾病、需要实验设计、临床试验规划或非GEO数据类型），请停止处理，并提供相应的反馈。**

## 输入验证

该工具适用于用户希望利用公共GEO转录组数据，识别两种疾病之间的共享转录组特征、中心基因或跨疾病生物标志物的情况。

如果请求内容不涉及两种疾病的转录组比较（例如：仅针对单一疾病的设计、实验设计、临床试验规划、非转录组组学数据分析（如蛋白质组学、代谢组学）或系统文献综述），请不要继续执行该研究流程。此时应回复：
> “双疾病转录组学机器学习规划器专为生成基于GEO数据的转录组学与机器学习研究设计而设计。您的请求超出我们的服务范围。请提供两种疾病进行比较，或选择其他合适的工具（如单疾病转录组学分析工具、磁共振成像规划工具或系统文献综述工具）。”

## 参考文件

| 文件 | 内容 | 使用场景 |
|------|---------|---------|
| [references/tissue_and_tool_decisions.md] | 根据疾病类型选择组织优先级；根据组织类型选择免疫去卷积工具 | 第4步（免疫分析模块）、第1步 |
| [references/geo_search_and_tools.md] | 根据疾病类型搜索GEO数据集；提供生物信息学工具列表 | 第4步（数据集相关内容） |
| [references/figure_plan_template.md] | 完整的图谱列表（图1–8）和表格模板 | 第5步 |
| [references/upgrade_path.md] | 发表影响与研究复杂性的对比分析 | 第9步 |