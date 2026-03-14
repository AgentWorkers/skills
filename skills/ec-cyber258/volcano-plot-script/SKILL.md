---
name: volcano-plot-script
description: 根据差异表达基因（DEG）分析结果，生成用于绘制火山图的 R/Python 代码。当用户需要可视化基因表达数据、p 值与倍数变化值的散点图，或生成可用于生物信息学分析的出版级图表时，可触发该代码的运行。
version: 1.0.0
category: Bioinfo
tags: [volcano-plot, bioinformatics, deg-analysis, r, python, visualization]
author: AIPOCH
license: MIT
status: Draft
risk_level: Medium
skill_type: Tool/Script
owner: AIPOCH
reviewer: 
last_updated: 2026-02-06
---
# 火山图脚本生成器

这是一项用于根据差异基因表达分析结果生成适合发表的火山图（volcano plot）的技能。

## 概述

火山图能够直观地展示基因表达数据中的统计显著性（p值）与变化幅度（倍数变化）之间的关系。该技能可以生成可定制的R或Python脚本，用于生成高质量、适合发表的图表。

## 使用场景

- 可视化RNA-seq差异表达分析（DEG）的结果
- 识别显著上调和下调的基因
- 突出显示感兴趣的基因（标记基因或通路）
- 为学术论文生成符合发表标准的图表
- 比较多种实验条件

## 输入要求

- 必需的输入数据格式：
  - 基因标识符（基因符号或ENSEMBL ID）
  - 对数2倍数变化值（log2 fold change）
  - 调整后的或原始的p值
  - 可选：基因注释、通路信息

## 输出结果

- 适合发表的火山图（格式：PNG/PDF/SVG）
- 可定制的R或Python脚本
- 可选：标记有显著性的基因列表

## 使用方法

```python
# Example: Run the volcano plot generator
python scripts/main.py --input deg_results.csv --output volcano_plot.png
```

## 参数

| 参数 | 描述 | 默认值 |
|---------|------------|---------|
| `--input` | DEG分析结果的CSV/TSV文件路径 | 必需 |
| `--output` | 输出图文件的路径 | volcano_plot.png |
| `--log2fc-col` | 对数2倍数变化的列名 | log2FoldChange |
| `--pvalue-col` | p值的列名 | padj |
| `--gene-col` | 基因ID的列名 | gene |
| `--log2fc-thresh` | 显著性的对数2倍数变化阈值 | 1.0 |
| `--pvalue-thresh` | p值的阈值 | 0.05 |
| `--label-genes` | 包含基因标签的文件路径 | 无 |
| `--top-n` | 要标记的显著基因数量 | 10 |
| `--color-up` | 上调基因的颜色 | #E74C3C |
| `--color-down` | 下调基因的颜色 | #3498DB |
| `--color-ns` | 非显著基因的颜色 | #95A5A6 |

## 技术难度

**中等** - 需要掌握以下知识：
- 差异表达分析（DEG）的概念（倍数变化、p值、FDR）
- 数据可视化原理
- Matplotlib/ggplot2绘图库的使用

## 依赖库

### Python
- pandas
- matplotlib
- seaborn
- numpy

### R
- ggplot2
- dplyr
- ggrepel（用于基因标签的定位）

## 参考资料

- [示例数据集和模板](references/)
- 火山图可视化的最佳实践
- 适合不同人群的配色方案

## 作者

该技能由生物信息学可视化工具自动生成。

## 风险评估

| 风险指标 | 评估结果 | 风险等级 |
|---------|------------|---------|
| 代码执行 | 在本地执行Python/R脚本 | 中等 |
| 网络访问 | 无外部API调用 | 低 |
| 文件系统访问 | 读取输入文件、写入输出文件 | 中等 |
- 指令篡改 | 遵循标准提示指南 | 低 |
| 数据泄露 | 输出文件保存在工作区 | 低 |

## 安全性检查

- 无硬编码的凭证或API密钥
- 输入文件路径经过验证（避免遍历上级目录）
- 输出目录限制在工作区内
- 脚本在沙箱环境中执行
- 错误信息经过处理（不暴露堆栈跟踪）
- 依赖库已审核（pandas、matplotlib、seaborn、numpy）

## 先决条件

```bash
# Python dependencies
pip install -r requirements.txt

# R dependencies (if using R)
install.packages(c("ggplot2", "dplyr", "ggrepel"))
```

## 评估标准

### 成功指标
- 成功生成可执行的Python/R脚本
- 输出图符合发表标准
- 根据阈值正确识别显著基因
- 能够优雅地处理缺失或格式错误的数据
- 配色方案对色盲用户友好

### 测试用例
1. **基本差异表达可视化**：输入标准的DESeq2结果 → 生成有效的火山图
2. **自定义阈值**：调整对数2倍数变化和p值阈值 → 正确分类基因
3. **基因标注**：指定要标注的基因 → 标签显示正确
4. **大数据集**：输入20,000多个基因 → 性能表现良好
5. **数据格式错误**：输入包含缺失值 → 能够优雅地处理错误

## 生命周期状态

- **当前阶段**：草案阶段
- **下一次审查日期**：2026-03-06
- **已知问题**：无
- **计划中的改进**：
  - 添加交互式图表功能（使用Plotly）
  - 支持多组比较
  - 与通路富集工具集成