---
name: "financial-analyst"
description: 执行财务比率分析、DCF（Discounted Cash Flow，折现现金流）估值、预算差异分析以及滚动预测的构建，以支持战略决策。适用于分析财务报表、构建估值模型、评估预算差异或制定财务预测与展望。当用户提及财务建模、现金流分析、公司估值、财务预测或电子表格分析时，该工具同样适用。
---
# 财务分析师技能

## 概述

这是一个可用于实际财务分析的工具包，提供比率分析、DCF估值、预算差异分析和滚动预测功能。它专为财务建模、预测与预算编制、管理报告、业务绩效分析以及投资分析而设计。

## 五阶段工作流程

### 第一阶段：范围界定
- 明确分析目标和相关方需求
- 确定数据来源和时间范围
- 设定重要性阈值和准确性标准
- 选择合适的分析框架

### 第二阶段：数据分析和建模
- 收集并验证财务数据（资产负债表、利润表、现金流量表）
- 在进行比率计算之前，**验证输入数据的完整性**（检查缺失字段、空值或不合理数值）
- 计算五大类财务比率（盈利能力、流动性、杠杆率、效率、估值）
- 使用加权平均资本成本（WACC）和终值计算方法构建DCF模型；**将DCF模型的输出与合理范围进行对比**（例如，与可比公司进行比较）
- 构建预算差异分析，并对差异进行正面/负面分类
- 基于驱动因素进行预测，并进行情景建模

### 第三阶段：洞察生成
- 解释比率趋势，并与行业标准进行对比
- 识别重大差异及其根本原因
- 通过敏感性分析评估估值范围
- 评估预测情景（基准情景/乐观情景/悲观情景），以支持决策制定

### 第四阶段：报告编制
- 生成包含关键发现的高管摘要
- 按部门和类别生成详细的差异报告
- 提供包含敏感性分析的DCF估值报告
- 呈现包含趋势分析的滚动预测结果

### 第五阶段：后续跟进
- 监控预测的准确性（目标：收入±5%，费用±3%）
- 确保报告按时交付（目标：100%按时完成）
- 随着实际数据的获取，更新模型
- 根据差异分析结果调整假设

## 工具

### 1. 比率计算器 (`scripts/ratio_calculator.py`)

从财务报表数据中计算并解释财务比率。

**比率类别：**
- **盈利能力：**净资产收益率（ROE）、总资产收益率（ROA）、毛利率、营业利润率、净利润率
- **流动性：**流动比率、速动比率、现金比率
- **杠杆率：**债务与权益比率、利息保障倍数、债务服务覆盖率（DSCR）
- **效率：**资产周转率、存货周转率、应收账款周转率、应收账款周转天数（DSO）
- **估值：**市盈率（P/E）、市净率（P/B）、市销率（P/S）、企业价值与息税折旧摊销前利润比率（EV/EBITDA）、PEG比率

```bash
python scripts/ratio_calculator.py sample_financial_data.json
python scripts/ratio_calculator.py sample_financial_data.json --format json
python scripts/ratio_calculator.py sample_financial_data.json --category profitability
```

### 2. DCF估值 (`scripts/dcf_valuation.py`

使用DCF方法对企业价值和股权价值进行估值，并进行敏感性分析。

**特点：**
- 通过资本资产定价模型（CAPM）计算WACC
- 预测收入和自由现金流（默认为5年）
- 采用永续增长法和退出倍数法计算终值
- 求出企业价值和股权价值
- 进行双向敏感性分析（折现率与增长率）

```bash
python scripts/dcf_valuation.py valuation_data.json
python scripts/dcf_valuation.py valuation_data.json --format json
python scripts/dcf_valuation.py valuation_data.json --projection-years 7
```

### 3. 预算差异分析器 (`scripts/budget_variance_analyzer.py`

分析实际数据与预算数据以及上一年的表现，并进行重要性筛选。

**特点：**
- 计算金额和百分比差异
- 设置重要性阈值（默认为10%或5万美元）
- 根据收入/费用情况对差异进行正面/负面分类
- 按部门和类别进行数据分解
- 生成高管摘要

```bash
python scripts/budget_variance_analyzer.py budget_data.json
python scripts/budget_variance_analyzer.py budget_data.json --format json
python scripts/budget_variance_analyzer.py budget_data.json --threshold-pct 5 --threshold-amt 25000
```

### 4. 预测构建器 (`scripts/forecast_builder.py`

基于驱动因素进行收入预测，并进行滚动现金流预测和情景建模。

**特点：**
- 基于驱动因素的收入预测模型
- 13周的滚动现金流预测
- 情景建模（基准情景/乐观情景/悲观情景）
- 使用简单线性回归进行趋势分析（基于标准库）

```bash
python scripts/forecast_builder.py forecast_data.json
python scripts/forecast_builder.py forecast_data.json --format json
python scripts/forecast_builder.py forecast_data.json --scenarios base,bull,bear
```

## 知识库

| 参考资料 | 用途 |
|-----------|---------|
| `references/financial-ratios-guide.md` | 比率公式、解释及行业标准 |
| `references/valuation-methodology.md` | DCF估值方法、WACC、终值计算方法 |
| `references/forecasting-best-practices.md` | 基于驱动因素的预测方法、滚动预测及预测准确性 |
| `references/industry-adaptations.md` | 不同行业（SaaS、零售、制造业、金融服务、医疗保健）的特定指标和注意事项 |

## 模板

| 模板 | 用途 |
|----------|---------|
| `assets/variance_report_template.md` | 预算差异报告模板 |
| `assets/dcf_analysis_template.md` | DCF估值分析模板 |
| `assets/forecast_report_template.md` | 收入预测报告模板 |

## 关键指标与目标

| 指标 | 目标 |
|--------|--------|
| 预测准确性（收入） | ±5% |
| 预测准确性（费用） | ±3% |
| 报告交付 | 100%按时完成 |
| 模型文档 | 所有假设均完整记录 |
| 差异解释 | 100%的重要差异均得到解释 |

## 输入数据格式

所有脚本均支持JSON格式的输入文件。请参阅 `assets/sample_financial_data.json` 以获取涵盖所有工具的完整输入格式说明。

## 依赖库

**无** - 所有脚本仅使用Python的标准库（`math`、`statistics`、`json`、`argparse`、`datetime`）。无需使用numpy、pandas或scipy。