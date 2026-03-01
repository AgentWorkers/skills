---
name: rstudio-research-agent
description: 与 R 和 RStudio 环境进行交互，以完成科学研究任务，包括创建项目、运行分析、管理依赖关系以及生成符合出版标准的图表。
---
# RStudio Research Agent

这是一个Claude Code技能，用于自动化基于R的综合研究工作流程。该技能支持用户与R和RStudio环境进行交互，从而实现科学计算、统计分析、生物信息学和数据可视化等功能。

## 概述

该技能帮助研究人员和数据科学家：
- 创建结构化、可复现的R研究项目
- 执行R脚本和RMarkdown分析
- 调试环境和依赖关系问题
- 生成符合出版标准的图表和报告
- 使用`renv`工具管理R包，以确保研究的可复现性

在以下情况下使用该技能：
- 创建具有标准结构的新R项目
- 在现有项目中运行R分析
- 解决R包依赖问题
- 生成统计报告或可视化结果
- 设置可复现的R工作流程

---

## 该技能的功能

激活后，该技能提供以下四个主要功能：

### 1. 创建R研究项目
- 使用标准文件夹结构搭建新的R项目
- 初始化Git仓库（可选）
- 设置`renv`用于包管理
- 生成模板脚本和报告
- 为RStudio创建`.Rproj`文件

### 2. 在现有项目中运行分析
- 执行R脚本和RMarkdown文件
- 处理参数化分析
- 返回结果、表格和图表
- 生成HTML/PDF报告

### 3. 调试环境和依赖关系
- 检查缺失的R包
- 解决库冲突
- 提出环境问题的解决方案
- 验证R版本的兼容性

### 4. 生成符合出版标准的图表
- 使用`ggplot2`等可视化库创建图表
- 导出为PDF/PNG/SVG/TIFF格式
- 遵循特定期刊的格式要求
- 支持多面板复合图表
- 使用对色盲用户友好的颜色方案

---

## 可触发该技能的用户请求示例：
- “为我的基因组数据分析创建一个新的R项目”
- “在我的现有项目中运行`analysis.R`并显示结果”
- “检查是否安装了所有所需的包”
- “根据我的数据集生成带回归线的散点图”
- “为RNA-seq分析设置一个可复现的工作流程”
- “调试我的R环境——某些包无法加载”
- “为这项临床试验数据生成统计报告”

---

## 项目结构

该技能创建的项目遵循以下标准化结构：

```
my-research-project/
├── data/
│   ├── raw/               # Original, immutable data files
│   └── processed/         # Cleaned, transformed data
├── scripts/               # Analysis and processing scripts
├── results/
│   ├── figures/           # Plots and visualizations
│   ├── tables/            # Summary tables
│   └── models/            # Saved model objects (.rds files)
├── reports/               # R Markdown/Quarto documents
├── renv.lock              # Package version lock file
├── .Rproj                 # RStudio project file
└── README.md              # Project documentation
```

---

## 常用工具和包

| 功能 | R包            |
|--------|------------------|
| 数据处理 | tidyverse, data.table      |
| 可视化 | ggplot2, patchwork, scales     |
| 统计分析 | stats, lme4, survival, broom    |
| 生物信息学 | Bioconductor (DESeq2, edgeR, limma)  |
| 报告生成 | rmarkdown, quarto       |
| 可复现性 | renv             |

---

## 示例工作流程

### 创建新项目

**用户需求：** 创建一个用于基因表达分析的新R项目，并初始化Git。

**技能操作：**
1. 创建目录结构（data/, scripts/, results/, reports/）
2. 初始化Git仓库
3. 设置`renv`环境
4. 安装DESeq2、tidyverse、ggplot2
5. 生成分析模板脚本
6. 创建R Markdown报告模板

### 运行分析

**用户需求：** 在现有项目中运行差分表达分析并显示结果。

**技能操作：**
1. 激活项目环境（renv）
2. 执行分析脚本
3. 捕获控制台输出和图表
4. 返回汇总表格和模型统计结果
5. （如需）生成报告

### 调试依赖关系

**用户需求：** 我的R脚本出现“找不到包”的错误。

**技能操作：**
1. 检查R版本和包的路径
2. 扫描脚本中所需的包
3. 与已安装的包进行对比
4. 生成安装命令
5. 检查版本冲突

---

## 注意事项：
- 需要R版本 >= 4.0.0
- 支持RStudio和命令行R环境
- 使用`renv`进行包管理，以确保研究的可复现性
- 所有输出都会保存到文件中（而不仅仅是控制台）
- 遵循R的最佳实践和现代编程规范

---

## 子技能

该技能包含以下子技能：
- **create-project**：搭建新的R研究项目
- **run-analysis**：执行R脚本并生成报告
- **debug-env**：调试R环境和依赖关系
- **generate-plots**：生成符合期刊格式要求的图表

每个子技能都可以独立使用，也可以作为完整工作流程的一部分来调用。