---
name: revenue-operations
description: 分析管道覆盖情况，使用 MAPE（Mean Absolute Percentage Error）跟踪预测准确性，并计算 GTM（Go-to-Market）效率指标，以优化 SaaS 收入。
---
# 收入运营

为SaaS收入团队提供销售管道分析、预测准确性跟踪以及市场推广（GTM）效率评估工具。

## 目录

- [快速入门](#quick-start)
- [工具概述](#tools-overview)
  - [销售管道分析器](#1-pipeline-analyzer)
  - [预测准确性跟踪器](#2-forecast-accuracy-tracker)
  - [GTM效率计算器](#3-gtm-efficiency-calculator)
- [收入运营工作流程](#revenue-operations-workflows)
  - [每周销售管道审查](#weekly-pipeline-review)
  - [预测准确性审查](#forecast-accuracy-review)
  - [GTM效率审计](#gtm-efficiency-audit)
  - [季度业务审查](#quarterly-business-review)
- [参考文档](#reference-documentation)
- [模板](#templates)

---

## 快速入门

```bash
# Analyze pipeline health and coverage
python scripts/pipeline_analyzer.py --input assets/sample_pipeline_data.json --format text

# Track forecast accuracy over multiple periods
python scripts/forecast_accuracy_tracker.py assets/sample_forecast_data.json --format text

# Calculate GTM efficiency metrics
python scripts/gtm_efficiency_calculator.py assets/sample_gtm_data.json --format text
```

---

## 工具概述

### 1. 销售管道分析器

分析销售管道的健康状况，包括覆盖率、阶段转化率、交易处理速度、交易老化风险以及集中度风险。

**输入：** 包含交易、销售配额和阶段配置的JSON文件
**输出：** 覆盖率、转化率、处理速度指标、老化标记、风险评估

**使用方法：**

```bash
# Text report (human-readable)
python scripts/pipeline_analyzer.py --input pipeline.json --format text

# JSON output (for dashboards/integrations)
python scripts/pipeline_analyzer.py --input pipeline.json --format json
```

**计算的关键指标：**
- **销售管道覆盖率** -- 总管道价值 / 销售配额目标（理想值：3-4倍）
- **阶段转化率** -- 各阶段之间的转化率
- **销售处理速度** -- （机会数 × 平均交易额 × 成交率） / 平均销售周期
- **交易老化** -- 标记超出平均周期2倍的交易
- **集中度风险** -- 当超过40%的管道集中在单一交易时发出警告
- **覆盖缺口分析** -- 识别管道不足的季度

**输入格式：**

```json
{
  "quota": 500000,
  "stages": ["Discovery", "Qualification", "Proposal", "Negotiation", "Closed Won"],
  "average_cycle_days": 45,
  "deals": [
    {
      "id": "D001",
      "name": "Acme Corp",
      "stage": "Proposal",
      "value": 85000,
      "age_days": 32,
      "close_date": "2025-03-15",
      "owner": "rep_1"
    }
  ]
}
```

### 2. 预测准确性跟踪器

使用MAPE（平均绝对百分比误差）跟踪预测准确性，检测系统性偏差，分析趋势，并提供分类级别的详细信息。

**输入：** 包含预测周期和可选分类划分的JSON文件
**输出：** MAPE得分、偏差分析、趋势数据、分类明细、准确性评级

**使用方法：**

```bash
# Track forecast accuracy
python scripts/forecast_accuracy_tracker.py forecast_data.json --format text

# JSON output for trend analysis
python scripts/forecast_accuracy_tracker.py forecast_data.json --format json
```

**计算的关键指标：**
- **MAPE** -- 平均绝对百分比误差：(|实际值 - 预测值| / |实际值|) × 100
- **预测偏差** -- 预测过高（正向）或过低（负向）的倾向
- **加权准确性** -- 根据交易金额对MAPE进行加权
- **周期趋势** -- 随时间推移准确性是提高、稳定还是下降
- **分类明细** -- 按销售代表、产品、细分市场或其他自定义维度划分的准确性

**准确性评级：**
| 评级 | MAPE范围 | 解释 |
|--------|-----------|----------------|
| 优秀 | <10% | 预测高度可靠，数据驱动的过程 |
| 良好 | 10-15% | 预测较为准确，仅有轻微差异 |
| 一般 | 15-25% | 需要改进预测流程 |
| 较差 | >25% | 预测方法存在显著问题 |

**输入格式：**

```json
{
  "forecast_periods": [
    {"period": "2025-Q1", "forecast": 480000, "actual": 520000},
    {"period": "2025-Q2", "forecast": 550000, "actual": 510000}
  ],
  "category_breakdowns": {
    "by_rep": [
      {"category": "Rep A", "forecast": 200000, "actual": 210000},
      {"category": "Rep B", "forecast": 280000, "actual": 310000}
    ]
  }
}
```

### 3. GTM效率计算器

计算核心的SaaS GTM效率指标，并提供行业基准和改进建议。

**输入：** 包含收入、成本和客户数据的JSON文件
**输出：** 关键指标（如Magic Number、LTV:CAC、CAC回收期等）以及相应的评级

**使用方法：**

```bash
# Calculate all GTM efficiency metrics
python scripts/gtm_efficiency_calculator.py gtm_data.json --format text

# JSON output for dashboards
python scripts/gtm_efficiency_calculator.py gtm_data.json --format json
```

**计算的关键指标：**

| 指标 | 公式 | 目标值 |
|--------|---------|--------|
| Magic Number | 当期净新收入 / 上期销售与营销支出 | >0.75 |
| LTV:CAC | (平均收入 per customer × 毛利率) / 平均客户获取成本 (CAC) | >3:1 |
| CAC回收期 | CAC / (平均收入 per customer × 毛利率)（以月计） | <18个月 |
| 支出倍数 | 净支出 / 净新收入 | <2倍 |
| 40法则 | 收入增长率 + 现金流量利润率 | >40% |
| 客户留存率 | (起始收入 + 扩展收入 - 收入流失) / 开始收入 | >110% |

**输入格式：**

```json
{
  "revenue": {
    "current_arr": 5000000,
    "prior_arr": 3800000,
    "net_new_arr": 1200000,
    "arpa_monthly": 2500,
    "revenue_growth_pct": 31.6
  },
  "costs": {
    "sales_marketing_spend": 1800000,
    "cac": 18000,
    "gross_margin_pct": 78,
    "total_operating_expense": 6500000,
    "net_burn": 1500000,
    "fcf_margin_pct": 8.4
  },
  "customers": {
    "beginning_arr": 3800000,
    "expansion_arr": 600000,
    "contraction_arr": 100000,
    "churned_arr": 300000,
    "annual_churn_rate_pct": 8
  }
}
```

---

## 收入运营工作流程

### 每周销售管道审查

使用此工作流程进行每周的销售管道检查：

1. **生成管道报告：**
   ```bash
   python scripts/pipeline_analyzer.py --input current_pipeline.json --format text
   ```

2. **审查关键指标：**
   - 管道覆盖率（是否超过销售配额的3倍？）
   - 超过老化阈值的交易（哪些交易需要关注？）
   - 集中度风险（是否过度依赖少数大额交易？）
   - 阶段分布（销售渠道是否健康？）

3. **使用模板记录审查结果：** 使用 `assets/pipeline_review_template.md`

4. **行动事项：** 处理老化交易，重新分配管道资源，弥补覆盖缺口

### 预测准确性审查

每月或每季度进行预测准确性评估和优化：

1. **生成准确性报告：**
   ```bash
   python scripts/forecast_accuracy_tracker.py forecast_history.json --format text
   ```

2. **分析趋势：**
   - MAPE是否呈下降趋势（表示准确性提高？）
   - 哪些销售代表或细分市场的预测误差最大？
   - 是否存在系统性的预测偏差？

3. **使用模板记录审查结果：** 使用 `assets/forecast_report_template.md`

4. **改进措施：** 对预测偏差较大的销售代表进行培训，调整预测方法，优化数据质量

### GTM效率审计

每季度或董事会准备期间进行市场推广效率评估：

1. **计算效率指标：**
   ```bash
   python scripts/gtm_efficiency_calculator.py quarterly_data.json --format text
   ```

2. **与目标进行对比：**
   - Magic Number指标反映GTM支出效率
   - LTV:CAC指标验证单位经济效益
   - CAC回收期指标显示资本效率
   - 40法则平衡增长和盈利能力

3. **使用模板记录审计结果：** 使用 `assets/gtm_dashboard_template.md`

4. **战略决策：** 调整支出分配，优化销售渠道，提升客户留存率

### 季度业务审查

结合这三个工具进行全面的季度业务审查：

1. 运用销售管道分析器评估未来的销售管道状况
2. 运用预测跟踪器评估过去的预测准确性
3. 运用GTM效率计算器评估当前的市场推广效率
4. 将管道健康状况与预测准确性进行对比
5. 使GTM效率指标与增长目标保持一致

---

## 参考文档

| 参考资料 | 说明 |
|-----------|-------------|
| [收入运营指标指南](references/revops-metrics-guide.md) | 完整的指标体系、定义、公式及解释 |
| [销售管道管理框架](references/pipeline-management-framework.md) | 销售管道最佳实践、阶段定义、转化基准 |
| [GTM效率基准](references/gtm-efficiency-benchmarks.md) | 按阶段划分的SaaS行业基准、标准及改进策略 |

---

## 模板

| 模板 | 使用场景 |
|----------|----------|
| [销售管道审查模板](assets/pipeline_review_template.md) | 每周/每月销售管道检查文档 |
| [预测报告模板](assets/forecast_report_template.md) | 预测准确性报告和趋势分析 |
| [GTM效率仪表板模板](assets/gtm_dashboard_template.md) | 供领导层使用的GTM效率仪表板 |
| [示例销售管道数据](assets/sample_pipeline_data.json) | `pipeline_analyzer.py`的示例输入数据 |
| [预期输出](assets/expected_output.json) | `pipeline_analyzer.py`的预期输出结果 |