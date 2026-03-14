---
name: volcano-plot-labeler
description: 使用排斥算法自动标记火山图（volcano plot）中最重要的基因
  algorithm
version: 1.0.0
category: Visual
tags: []
author: AIPOCH
license: MIT
status: Draft
risk_level: Medium
skill_type: Tool/Script
owner: AIPOCH
reviewer: ''
last_updated: '2026-02-06'
---
# Volcano Plot Labeler (ID: 148)

该工具能够自动识别火山图（volcano plot）中最重要的10个基因，并使用排斥算法（repulsion algorithm）为这些基因添加标签，以防止标签重叠。

## 主要功能

- **智能基因筛选**：根据p值和基因表达量的变化倍数（fold change）自动筛选出最重要的10个基因。
- **排斥算法**：通过力导向（force-directed）的定位方式，确保文本标签不会相互重叠。
- **可定制**：支持配置阈值、标签样式和定位选项。
- **多种输出格式**：支持PNG、PDF和SVG格式。

## 安装

```bash
pip install pandas matplotlib numpy scipy
```

## 使用方法

### 基本用法

```python
from volcano_plot_labeler import label_volcano_plot
import pandas as pd

# Load your data
df = pd.read_csv('differential_expression_results.csv')

# Generate labeled volcano plot
fig = label_volcano_plot(
    df,
    log2fc_col='log2FoldChange',
    pvalue_col='padj',
    gene_col='gene_name',
    top_n=10
)
fig.savefig('volcano_plot_labeled.png', dpi=300, bbox_inches='tight')
```

### 高级用法

```python
from volcano_plot_labeler import label_volcano_plot

fig = label_volcano_plot(
    df,
    log2fc_col='log2FoldChange',
    pvalue_col='padj',
    gene_col='gene_name',
    top_n=10,
    pvalue_threshold=0.05,
    log2fc_threshold=1.0,
    figsize=(12, 10),
    repulsion_iterations=100,
    repulsion_force=0.05,
    label_fontsize=10,
    label_color='black',
    arrow_color='gray',
    save_path='output.png'
)
```

### 命令行用法

```bash
python scripts/main.py \
    --input data/deseq2_results.csv \
    --output volcano_labeled.png \
    --log2fc-col log2FoldChange \
    --pvalue-col padj \
    --gene-col gene_name \
    --top-n 10
```

## 输入格式

输入文件应为CSV或TSV格式，包含以下列：
- `log2FoldChange`：基因表达量的对数变化倍数（log2 fold change）
- `padj` 或 `pvalue`：调整后的p值或原始p值
- `gene_name`：基因标识符

## 算法原理

### 基因重要性计算
1. 计算所有基因的 `-log10(pvalue)` 值。
2. 根据综合得分（`|log2FC| * -log10(pvalue)`）对基因进行排序。
3. 选择得分最高的N个基因作为重点标记对象。

### 排斥算法
1. **初始定位**：将标签放置在基因对应的坐标位置。
2. **力场计算**：
   - 计算相邻标签之间的排斥力。
   - 计算标签朝向基因位置的吸引力（即“弹簧力”）。
   - 设定边界力以确保标签保持在图表区域内。
3. **迭代优化**：进行N次迭代，直到标签位置稳定。
4. **绘制箭头**：在标签和基因位置之间绘制连接线。

## 参数设置

| 参数 | 类型 | 默认值 | 说明 |
|-----------|------|---------|-------------|
| `df` | DataFrame | - | 输入数据框 |
| `log2fc_col` | str | 'log2FoldChange' | 对数变化倍数的列名 |
| `pvalue_col` | str | 'padj' | p值的列名 |
| `gene_col` | str | 'gene_name' | 基因名称的列名 |
| `top_n` | int | 10 | 要标记的基因数量 |
| `pvalue_threshold` | float | 0.05 | 用于颜色区分的p值阈值 |
| `log2fc_threshold` | float | 1.0 | 用于颜色区分的对数变化倍数阈值 |
| `repulsion_iterations` | int | 100 | 排斥算法的迭代次数 |
| `repulsion_force` | float | 排斥力的强度 |
| `label_fontsize` | int | 标签的字体大小 |
| `figsize` | tuple | (10, 10) | 图表尺寸 |

## 输出结果

输出为带标签的火山图，包含：
- 用颜色区分的基因点（表示基因的显著性：高/低/不显著）
- 最重要的10个基因的标签及其连接线
- 确保标签之间没有重叠。

## 许可证

MIT许可证

## 风险评估

| 风险指标 | 评估结果 | 风险等级 |
|----------------|------------|-------|
| 代码执行 | 在本地执行Python/R脚本 | 中等风险 |
| 网络访问 | 无外部API调用 | 低风险 |
| 文件系统访问 | 读取输入文件、写入输出文件 | 中等风险 |
| 代码篡改 | 遵循标准提示指南 | 低风险 |
| 数据泄露 | 输出文件保存在工作区 | 低风险 |

## 安全性检查项

- 未使用硬编码的凭证或API密钥。
- 无未经授权的文件系统访问。
- 输出文件不会泄露敏感信息。
- 有防止命令注入的安全机制。
- 输入文件路径经过验证，防止遍历外部目录。
- 输出目录仅限于工作区。
- 脚本在沙箱环境中执行。
- 错误信息经过处理，不会暴露堆栈追踪信息。
- 依赖项已过审计。

## 先决条件

```bash
# Python dependencies
pip install -r requirements.txt
```

## 评估标准

### 成功指标
- 脚本能够成功执行主要功能。
- 输出结果符合质量标准。
- 能够优雅地处理边缘情况。
- 性能表现令人满意。

### 测试用例
1. **基本功能测试**：输入符合预期，输出符合预期。
2. **边缘情况测试**：输入无效时，程序能够优雅地处理错误。
3. **性能测试**：处理大规模数据集时，处理时间在可接受范围内。

## 项目现状

- **当前阶段**：草案阶段。
- **下一次审查日期**：2026-03-06。
- **已知问题**：无。
- **计划中的改进**：
  - 优化性能。
  - 添加更多功能。