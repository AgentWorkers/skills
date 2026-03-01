---
name: survival-analysis-km
description: 生成Kaplan-Meier生存曲线，计算生存统计量（对数秩检验、中位生存时间），并估算临床和生物学生存数据分析中的风险比。当用户请求生存分析、Kaplan-Meier图、事件发生时间分析，或在生物医学背景下询问生存统计信息时，该功能会被触发。
  (log-rank test, median survival time), and estimates hazard ratios for clinical
  and biological survival data analysis. Triggered when user requests survival analysis,
  Kaplan-Meier plots, time-to-event analysis, or asks about survival statistics in
  biomedical contexts.
version: 1.0.0
category: Bioinfo
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
# 生存分析（Kaplan-Meier）

Kaplan-Meier生存分析工具，适用于临床和生物学研究。可生成适用于发表的生存曲线，并提供相应的统计测试结果。

## 主要功能

- **Kaplan-Meier曲线生成**：生成包含置信区间的生存曲线（符合学术发表标准）
- **统计测试**：对数秩检验（Log-rank test）、Wilcoxon检验、Peto-Peto检验
- **风险比（Hazard Ratios）**：Cox比例风险回归分析，附带95%置信区间
- **汇总统计**：中位生存时间、受限平均生存时间（Restricted Mean Survival Time, RMST）
- **多组分析**：支持2个及以上的比较组
- **风险表**：可选择在图表下方显示风险表

## 使用方法

### Python脚本示例

```bash
python scripts/main.py --input data.csv --time time_col --event event_col --group group_col --output results/
```

### 参数说明

| 参数          | 说明                | 是否必填       |
|--------------|-------------------|-------------|
| `--input`       | 输入CSV文件路径          | 是           |
| `--time`       | 表示生存时间的列名         | 是           |
| `--event`       | 表示事件发生情况的列名（1=事件发生，0=数据被删失）| 是           |
| `--group`       | 分组变量对应的列名         | 可选         |
| `--output`      | 结果输出目录           | 是           |
| `--conf-level`     | 置信水平（默认：0.95）         | 可选         |
| `--risk-table`    | 是否在图表中显示风险表       | 可选         |

### 输入格式

输入CSV文件应包含以下列：
- **Time**：数值型列，表示事件发生或数据被删失的时间
- **Event**：二进制列（1=事件发生，0=数据被删失）
- **Group**：分类列，用于数据分组

### 输出文件

- `km_curve.png`：Kaplan-Meier生存曲线图
- `km_curve.pdf`：适用于发表的矢量格式文件
- `survival_stats.csv`：统计汇总数据（中位生存时间、置信区间）
- `hazard_ratios.csv`：Cox回归结果（风险比及95%置信区间）
- `logrank_test.csv`：成对比较的p值
- `report.txt`：人类可读的总结报告

## 技术细节

### 统计方法

1. **Kaplan-Meier估计器**：非参数的最大似然法估计生存函数
   - 使用乘积极限法（Product-limit method）计算生存函数Ŝ(t)：Ŝ(t) = Π(tᵢ≤t) (1 - dᵢ/nᵢ)
   - 使用Greenwood公式估计方差

2. **对数秩检验（Log-Rank Test）**：最常用的生存曲线比较方法
   - 原假设：各组间生存曲线无差异
   - 按每个时间点的风险人数进行加权计算

3. **Cox比例风险模型（Cox Proportional Hazards）**：半参数回归模型
   - 模型表达式：h(t|X) = h₀(t) × exp(β₁X₁ + β₂X₂ + ...)
   - 通过Schoenfeld残差检验比例风险假设是否成立

### 所需依赖库

- `lifelines`：核心生存分析库
- `matplotlib`, `seaborn`：用于数据可视化
- `pandas`, `numpy`：数据处理库
- `scipy`：提供统计测试功能

### 技术难度：高 ⚠️

该工具涉及高级统计建模。建议由生物统计学家审核结果，特别是在以下情况下：
- 比例风险假设不成立时
- 样本量较小（每组少于30个样本）
- 数据删失率较高（超过50%）
- 存在时间变化的协变量

## 参考文献

相关资料请参见`references/`文件夹：
- Kaplan EL, Meier P (1958)：原始论文
- Cox DR (1972)：Cox回归模型论文
- 用于测试的样本数据集
- 临床报告指南（ATN, CONSORT）

## 参数设置

| 参数          | 类型                | 默认值          | 说明                          |
|--------------|-------------------|-----------------------------|
| `--input`       | str                | 输入CSV文件路径                |                              |
| `--time`       | str                | 表示生存时间的列名                |                              |
| `--event`       | str                | 表示事件发生情况的列名                |                              |
| `--group`       | str                | 分组变量对应的列名                |                              |
| `--output`      | str                | 结果输出目录                      |                              |
| `--conf-level`     | float                | 置信水平（0.95）                     |                              |
| `--risk-table`    | str                | 是否在图表中显示风险表                |                              |
| `--figsize`     | str                | 图表尺寸（例如：'10'）                 |                              |
| `--dpi`       | int                | 图像分辨率（例如：300）                 |                              |

## 示例输出

- 显示带有95%置信区间的生存曲线
- 中位生存时间：实验组A为28.4个月（95%置信区间：24.1-32.7个月），安慰剂组为18.2个月（95%置信区间：15.3-21.1个月）
- 对数秩检验p值：0.0023
- 风险比：0.62（95%置信区间：0.45-0.85），p值：0.003

## 风险评估

| 风险指标       | 评估内容                | 风险等级        |
|--------------|-------------------|---------------------------|
| 代码执行       | 在本地执行Python/R脚本       | 中等风险                    |
| 网络访问       | 无外部API调用             | 低风险                        |
| 文件系统访问     | 读取输入文件、写入输出文件       | 中等风险                        |
| 指令篡改       | 遵循标准提示指南             | 低风险                        |
| 数据泄露       | 输出文件保存在工作区             | 低风险                        |

## 安全性检查

- 无硬编码的凭证或API密钥
- 无未经授权的文件系统访问
- 输出内容不包含敏感信息
- 有防止命令注入的安全措施
- 输入文件路径经过验证
- 输出目录限制在工作区内
- 脚本在沙箱环境中执行
- 错误信息经过处理（不暴露堆栈追踪）
- 所有依赖库均经过审核

## 先决条件

### 评估标准

- 脚本能够成功执行主要功能
- 输出结果符合质量标准
- 能够优雅地处理边缘情况
- 性能表现可接受

### 测试用例

- **基本功能测试**：输入有效数据 → 输出符合预期结果
- **边缘情况测试**：输入无效数据 → 脚本能正确处理错误
- **性能测试**：处理大型数据集时性能表现良好

## 开发现状

- **当前阶段**：草案阶段
- **下一次审查日期**：2026-03-06
- **已知问题**：无
- **计划改进**：
  - 优化性能
  - 添加新功能支持