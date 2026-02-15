---
name: arc-creator
description: 根据 nfdi4plants ARC 规范，创建并填充带注释的研究上下文（Annotated Research Contexts, ARCs）。该工具可用于创建新的 ARC、添加研究/检测/工作流程/运行记录、注释 ISA 元数据、将研究数据组织到 ARC 结构中，或将 ARC 推送到 DataHUB。它以交互式方式引导用户完成所有必需和可选的元数据字段的填写。
---

# ARC 创建器

根据 nfdi4plants ARC 规范 v3.0.0 创建 FAIR 数字对象。

## 先决条件

- 已安装 `git` 和 `git-lfs`
- ARC Commander CLI 已安装在 `~/bin/arc`（可选，但推荐）
- 如需与 DataHUB 同步：需要 git.nfdi4plants.org 或 datahub.hhu.de 的个人访问令牌

## 交互式 ARC 创建流程

按顺序引导用户完成以下步骤。通过对话形式提出问题，不要一次性列出所有问题。每条消息中最多提 2-4 个相关问题。

### 第 1 阶段：调查设置

询问用户：
1. **调查标识符**（简短、使用小写字母和连字符组成，例如 `cold-stress-arabidopsis`）
2. **标题**（调查的简明名称）
3. **描述**（研究目标的文字说明）
4. **本地存储 ARC 的位置**（建议存储在 `/home/uranus/arc-projects/<identifier>/`）

然后运行 `scripts/create_arc.sh <path> <identifier>` 并设置调查元数据：
```bash
arc investigation update -i "<id>" --title "<title>" --description "<desc>"
```

### 第 2 阶段：研究

对于每项研究，询问：
1. **研究标识符**（例如 `plant-growth`）
2. **标题和描述**
3. **实验对象**（针对“Characteristic [Organism]”）
4. **生长条件**（温度、光照、培养基等）
5. **来源材料**（投入的材料——种子、细胞系等）
6. **样本材料**（产生的材料——叶片、根系、提取物等）
7. **实验方案**——用户是否有相关的实验方案文档？
8. **实验变量**——正在测试哪些实验因素？（例如温度、基因型、处理方式）

使用以下命令创建相关文件：
```bash
arc study init --studyidentifier "<id>"
arc study update --studyidentifier "<id>" --title "<title>" --description "<desc>"
```

将实验方案文件复制到 `studies/<id>/protocols/`。
将资源文件复制到 `studies/<id>/resources/`。

### 第 3 阶段：检测

对于每个检测项目，询问：
1. **检测标识符**（例如 `proteomics-ms`、`rnaseq`、`sugar-measurement`）
2. **检测类型**（例如蛋白质表达分析、转录组分析、代谢物分析）
3. **技术类型**（例如质谱分析、核苷酸测序、平板读取器）
4. **技术平台**（例如 Illumina NovaSeq、Bruker timsTOF）
5. **数据文件**——原始数据文件存放位置？（将保存在 `assays/<id>/dataset/`）
6. **处理后的数据**——是否有处理后的输出文件？
7. **实验方案**——是否有特定于该检测的实验方案？
8. **执行者**——谁执行了该检测？（姓名、所属机构、角色）

使用以下命令创建相关文件：
```bash
arc assay init -a "<id>" --measurementtype "<type>" --technologytype "<tech>"
```

将数据文件复制到 `assays/<id>/dataset/`，实验方案文件复制到 `assays/<id>/protocols/`。

### 第 4 阶段：工作流程（可选）

询问是否有计算分析步骤。对于每个计算分析步骤，询问：
1. **工作流程标识符**（例如 `deseq2-analysis`、`heatmap-generation`）
2. **工作流程描述**
3. **代码文件**（脚本、笔记本等）
4. **依赖项**（Python 包、R 库、Docker 镜像）

将代码文件放入 `workflows/<id>/`。
注意：虽然规范要求必须创建 `workflow.cwl` 文件，但实际上通常会在后续步骤中生成。请告知用户这一点。

### 第 5 阶段：实验运行（可选）

询问是否有实验结果。对于每个实验结果，询问：
1. **实验运行标识符**
2. **生成该结果的流程名称**
3. **输出文件**（图表、表格、处理后的数据）

将输出文件保存在 `runs/<id>/`。

### 第 6 阶段：联系人及出版物

询问：
1. **调查联系人**（姓名、电子邮件、所属机构、角色——至少包括项目负责人）
2. **出版物**（如果有——DOI、PubMed ID、标题、作者）

使用以下命令添加相关信息：
```bash
arc investigation person register --lastname "<last>" --firstname "<first>" --email "<email>" --affiliation "<aff>"
```

### 第 7 阶段：Git 提交及 DataHUB 同步

1. 配置 Git 用户信息：
```bash
git config user.name "<name>"
git config user.email "<email>"
```

2. 提交更改：
```bash
git add -A
git commit -m "Initial ARC: <investigation title>"
```

3. 询问用户是否希望将数据推送到 DataHUB。如果需要：
   - 询问目标服务器（git.nfdi4plants.org、datahub.hhu.de 等）
   - 创建远程仓库（通过浏览器或 API）
   - 设置远程仓库并执行推送操作

## ISA 元数据参考

有关 ISA-XLSX 字段、注释表列和本体参考的详细信息，请参阅 `references/arc-spec.md`。

## 重要提示

- **检测数据是不可修改的**——在初次上传后，切勿修改 `assays/<id>/dataset/` 中的文件
- **研究部分描述实验材料，检测部分描述实验过程**
- **工作流程是代码实现，实验结果是分析结果**
- 对于大于 100 MB 的文件，使用 `git lfs track "*.fastq.gz" "*.bam" "*.raw"` 进行版本控制
- **不要将 ARC 文件存储在 OneDrive/Dropbox 上**——Git 与云存储同步可能会导致数据冲突
- ARC Commander CLI 的使用方法：`arc <subcommand> --help`