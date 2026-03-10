---
name: "revenue-operations"
description: 分析销售流程的健康状况、收入预测的准确性以及市场推广（Go-to-Market, GTM）的效率指标，以优化SaaS业务的收入。适用于分析销售流程的覆盖范围、预测收入、评估市场推广绩效、审查销售指标、进行销售流程分析、使用MAPE工具跟踪预测准确性、计算市场推广效率，或衡量SaaS团队的销售效率及单位经济效益等场景。
---
# 收入运营

为SaaS收入团队提供管道分析、预测准确性跟踪以及GTM（市场推广）效率测量工具。

> **输出格式：** 所有脚本均支持 `--format text`（人类可读格式）和 `--format json`（用于仪表盘或集成）。

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

### 1. 管道分析器（Pipeline Analyzer）

分析销售管道的健康状况，包括覆盖比率、阶段转化率、交易速度、老化风险和集中风险。

**输入：** 包含交易、配额和阶段配置的JSON文件
**输出：** 覆盖比率、转化率、速度指标、老化标志、风险评估

**使用方法：**

```bash
python scripts/pipeline_analyzer.py --input pipeline.json --format text
```

**计算的关键指标：**
- **管道覆盖比率** -- 总管道价值 / 配额目标（理想值：3-4倍）
- **阶段转化率** -- 阶段间的转化率
- **销售速度** -- （机会数 × 平均交易额 × 中标率） / 平均销售周期
- **交易老化** -- 标记超过平均周期时间2倍的交易
- **集中风险** -- 当超过40%的管道集中在少数几笔交易时发出警告
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

### 2. 预测准确性跟踪器（Forecast Accuracy Tracker）

使用MAPE（平均绝对百分比误差）跟踪预测准确性，检测系统性偏差，分析趋势，并提供分类级细分。

**输入：** 包含预测周期和可选分类细分的JSON文件
**输出：** MAPE得分、偏差分析、趋势、分类细分、准确性评级

**使用方法：**

```bash
python scripts/forecast_accuracy_tracker.py forecast_data.json --format text
```

**计算的关键指标：**
- **MAPE** -- (|实际值 - 预测值| / |实际值|) × 100
- **预测偏差** -- 预测过高（正向）或预测过低（负向）的趋势
- **加权准确性** -- 根据交易金额对MAPE进行加权
- **周期趋势** -- 随时间推移准确性是提高、稳定还是下降
- **分类细分** -- 按销售代表、产品、细分市场或其他自定义维度划分的准确性

**准确性评级：**
| 评级 | MAPE范围 | 解释 |
|--------|-----------|----------------|
| 优秀 | <10% | 预测高度准确，数据驱动的过程 |
| 良好 | 10-15% | 预测可靠，偏差较小 |
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

### 3. GTM效率计算器（GTM Efficiency Calculator）

计算核心SaaS GTM效率指标，并提供行业基准和改进建议。

**输入：** 包含收入、成本和客户数据的JSON文件
**输出：** 关键指标（如Magic Number、LTV:CAC、CAC回收期、Burn Multiple、Rule of 40等）及其评级

**使用方法：**

```bash
python scripts/gtm_efficiency_calculator.py gtm_data.json --format text
```

**计算的关键指标：**

| 指标 | 公式 | 目标值 |
|--------|---------|--------|
| Magic Number | 当期净新收入（Net New ARR） / 上期销售和营销支出（S&M Spend） | >0.75 |
| LTV:CAC | (平均每次交易收入ARPA × 毛利率) / 平均客户获取成本CAC | >3:1 |
| CAC回收期 | CAC / (ARPA × 毛利率)（月数） | <18个月 |
| Burn Multiple | 净支出 / 净新收入 | <2倍 |
| Rule of 40 | 收入增长率百分比 + 自由现金流利润率 | >40% |
| 净客户留存率 | (初始收入 + 扩展收入 - 收缩收入 - 客户流失率) / 初始收入 | >110% |

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

### 每周管道审查

使用此工作流程进行每周的管道检查：

1. **验证输入数据：** 确认管道导出数据是最新的，并且所有必需字段（阶段、价值、关闭日期、负责人）都已填写完整。
2. **生成管道报告：**
   ```bash
   python scripts/pipeline_analyzer.py --input current_pipeline.json --format text
   ```

3. **将输出总数与CRM源系统进行交叉核对**，以确保数据完整性。
4. **审查关键指标：**
   - 管道覆盖比率（是否超过配额的3倍？）
   - 超过阈值的老化交易（哪些交易需要干预？）
   - 集中风险（是否过度依赖少数几笔大额交易？）
   - 阶段分布（销售漏斗是否健康？）
5. **使用模板记录结果：** 使用 `assets/pipeline_review_template.md`
6. **行动事项：** 处理老化交易，重新分配管道资源，填补覆盖缺口。

### 预测准确性审查

每月或每季度进行一次，以评估和改进预测流程：

1. **验证输入数据：** 确保所有预测周期都有对应的实际数据，并且没有遗漏的周期。
2. **生成准确性报告：**
   ```bash
   python scripts/forecast_accuracy_tracker.py forecast_history.json --format text
   ```

3. **将实际数据与CRM中的已成交记录进行交叉核对**，再得出结论。
4. **分析趋势：**
   - MAPE是否呈下降趋势（表示预测准确性在提高？）
   - 哪些销售代表或细分市场的预测误差最大？
   - 是否存在系统性的预测偏差？
5. **使用模板记录结果：** 使用 `assets/forecast_report_template.md`
6. **改进措施：** 对预测偏差较大的销售代表进行培训，调整预测方法，提高数据质量。

### GTM效率审计

每季度或在进行董事会准备时进行，以评估市场推广效率：

1. **验证输入数据：** 确认收入、成本和客户数据与财务记录一致。
2. **计算效率指标：**
   ```bash
   python scripts/gtm_efficiency_calculator.py quarterly_data.json --format text
   ```

3. **将计算出的收入和支出总数与财务系统进行交叉核对**，然后再分享结果。
4. **与目标进行对比：**
   - Magic Number（>0.75）
   - LTV:CAC（>3:1）
   - CAC回收期（<18个月）
   - Rule of 40（>40%）
5. **使用模板记录结果：** 使用 `assets/gtm_dashboard_template.md`
6. **战略决策：** 调整支出分配，优化销售渠道，提高客户留存率。

### 季度业务回顾

结合这三个工具进行全面的季度业务回顾（QBR）分析：

1. 运行管道分析器，了解未来的销售潜力。
2. 运行预测跟踪器，评估过去的预测准确性。
3. 运行GTM效率计算器，获取效率基准。
4. 将管道健康状况与预测准确性进行对比。
5. 使GTM效率指标与增长目标保持一致。

---

## 参考文档

| 参考文档 | 说明 |
|-----------|-------------|
| [收入运营指标指南](references/revops-metrics-guide.md) | 完整的指标体系、定义、公式和解释 |
| [管道管理框架](references/pipeline-management-framework.md) | 管道管理最佳实践、阶段定义、转化率基准 |
| [GTM效率基准](references/gtm-efficiency-benchmarks.md) | 按阶段划分的SaaS基准、行业标准、改进策略 |

---

## 模板

| 模板 | 使用场景 |
|----------|----------|
| [管道审查模板](assets/pipeline_review_template.md) | 每周/每月的管道检查文档 |
| [预测报告模板](assets/forecast_report_template.md) | 预测准确性报告和趋势分析 |
| [GTM仪表盘模板](assets/gtm_dashboard_template.md) | 供领导层使用的GTM效率仪表盘 |
| [示例管道数据](assets/sample_pipeline_data.json) | `pipeline_analyzer.py`的示例输入数据 |
| [预期输出](assets/expected_output.json) | `pipeline_analyzer.py`的预期输出结果 |