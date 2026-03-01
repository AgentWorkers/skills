---
name: create-r-project
description: 创建一个新的R研究项目，该项目应具备标准的文件夹结构、Git初始化配置、renv包管理工具以及模板脚本。
---
# 创建 R 研究项目

这是一个专门用于构建具有可复现结构和最佳实践的新 R 研究项目的子技能。

## 概述

该子技能会创建一个完整的、适用于科学 research、统计分析、生物信息学和数据可视化的 R 项目结构。

当用户需要以下操作时，请使用此子技能：
- 从零开始创建一个新的 R 项目
- 设置可复现的研究工作流程
- 初始化 Git 以进行版本控制
- 生成分析模板脚本

---

## 该子技能的功能

调用此子技能后，它将执行以下操作：

1. **创建目录结构**
   - `data/raw/`：原始的、不可修改的数据文件
   - `data/processed/`：清洗过的数据
   - `scripts/`：分析和处理脚本
   - `results/figures/`：图表和可视化结果
   - `results/tables/`：汇总表格
   - `results/models/`：保存的模型对象（.rds 文件）
   - `reports/`：R Markdown/Quarto 文档

2. **初始化版本控制**
   - 创建包含 R 相关规则的 `.gitignore` 文件
   - （如果需要）初始化 Git 仓库
   - 提交初始项目结构

3. **设置包管理**
   - 初始化 `renv` 以创建可复现的 R 环境
   - 创建 `renv.lock` 文件
   - 生成 `.Rprofile` 文件以实现 `renv` 的自动激活

4. **创建 RStudio 项目**
   - 生成用于 RStudio 集成的 `.Rproj` 文件
   - 配置项目选项

5. **生成模板文件**
   - 分析脚本模板（`scripts/01_analysis.R`）
   - R Markdown 报告模板（`reports/report.Rmd`）
   - 包含项目文档的 `README.md` 文件
   - 适用于 R 项目的 `.gitignore` 文件

---

## 用户示例请求

- “创建一个用于基因组分析的新 R 项目”
- “使用 Git 设置一个 R 研究项目”
- “为差异表达分析初始化一个 R 项目”
- “创建一个用于统计建模的 R 工作流程”

---

## 生成的模板

### 分析脚本（`scripts/01_analysis.R`）

```r
# Load libraries
library(tidyverse)
# Add required packages

# Load data
raw_data <- read_csv("data/raw/input.csv")

# Process data
processed_data <- raw_data %>%
  # Add processing steps
  mutate()

# Save processed data
write_csv(processed_data, "data/processed/cleaned.csv")

# Analysis
results <- processed_data %>%
  # Add analysis code
  summarize()

# Save results
write_csv(results, "results/tables/results.csv")

# Generate plots
g <- ggplot(processed_data, aes()) +
  geom_point() +
  theme_minimal()

ggsave("results/figures/plot1.pdf", g, width = 6, height = 4)
```

### R Markdown 报告（`reports/report.Rmd`）

```markdown
---
title: "Analysis Report"
output: html_document
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
library(tidyverse)
```

## Methods

Describe your analysis methods here.

## Results

```{r results}
# 加载并显示结果
results <- read_csv("results/tables/results.csv")
results
```

## Figures

```{r figures}
# 显示生成的图表
knitr::includegraphics("results/figures/plot1.pdf")
```
```

---

## 参数

| 参数 | 描述 | 默认值 |
|-----------|-------------|---------|
| `project_name` | 项目目录的名称 | 必填 |
| `init-git` | 是否初始化 Git 仓库 | `false` |
| `create_rproj` | 是否创建 RStudio 项目文件 | `true` |
| `init_renv` | 是否初始化 `renv` 环境 | `true` |
| `project_type` | 项目类型（通用、生物信息学、统计） | `general` |

---

## 注意事项

- 项目遵循标准的 R 研究项目规范
- `renv.lock` 确保包版本的稳定性
- `.gitignore` 文件排除敏感数据和编译后的文件
- 所有脚本使用相对路径以提高可移植性

---

## 相关子技能

- **run-analysis**：在创建的项目中执行分析
- **debug-env**：设置和排查 R 环境的问题