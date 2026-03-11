---
name: "campaign-analytics"
description: 该工具通过多触点归因（multi-touch attribution）、漏斗转化分析（funnel conversion analysis）以及投资回报率（ROI）计算来分析营销活动的表现，从而帮助优化营销策略。适用于分析营销活动、广告效果、归因模型、转化率，以及计算跨渠道的营销投资回报率（ROI）、广告投资回报率（ROAS）、每次点击成本（CPA）等关键营销指标。
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  domain: campaign-analytics
  updated: 2026-02-06
  python-tools: attribution_analyzer.py, funnel_analyzer.py, campaign_roi_calculator.py
  tech-stack: marketing-analytics, attribution-modeling
---
# 活动分析

提供生产级活动性能分析，包括多触点归因建模、漏斗转化分析和投资回报率（ROI）计算。三个Python命令行工具（CLI）仅使用标准库即可实现确定性、可重复的分析结果——无需外部依赖、无需API调用、无需机器学习模型。

---

## 输入要求

所有脚本都接受一个JSON文件作为参数输入。请参阅`assets/sample_campaign_data.json`以获取完整示例。

### 归因分析器

```json
{
  "journeys": [
    {
      "journey_id": "j1",
      "touchpoints": [
        {"channel": "organic_search", "timestamp": "2025-10-01T10:00:00", "interaction": "click"},
        {"channel": "email", "timestamp": "2025-10-05T14:30:00", "interaction": "open"},
        {"channel": "paid_search", "timestamp": "2025-10-08T09:15:00", "interaction": "click"}
      ],
      "converted": true,
      "revenue": 500.00
    }
  ]
}
```

### 漏斗分析器

```json
{
  "funnel": {
    "stages": ["Awareness", "Interest", "Consideration", "Intent", "Purchase"],
    "counts": [10000, 5200, 2800, 1400, 420]
  }
}
```

### 活动ROI计算器

```json
{
  "campaigns": [
    {
      "name": "Spring Email Campaign",
      "channel": "email",
      "spend": 5000.00,
      "revenue": 25000.00,
      "impressions": 50000,
      "clicks": 2500,
      "leads": 300,
      "customers": 45
    }
  ]
}
```

### 输入验证

在运行脚本之前，请验证JSON文件是否有效，并且符合预期的结构。常见错误包括：
- **缺少所需键**（例如`journeys`、`funnel.stages`、`campaigns`）→ 脚本会抛出`KeyError`错误并终止执行
- 漏斗数据中的数组长度不匹配（`stages`和`counts`的长度必须相同）→ 抛出`ValueError`错误
- ROI数据中的货币值非数字 → 抛出`TypeError`错误

在将JSON文件传递给任何脚本之前，可以使用`python -m json.tool your_file.json`来验证其语法是否正确。

---

## 输出格式

所有脚本都支持通过`--format`标志选择两种输出格式：
- `--format text`（默认）：适合人类阅读的表格和摘要，便于审查
- `--format json`：适合机器读取的JSON格式，便于集成到自动化流程中

---

## 典型分析工作流程

为了全面评估活动效果，请按顺序运行这三个脚本：

```bash
# Step 1 — Attribution: understand which channels drive conversions
python scripts/attribution_analyzer.py campaign_data.json --model time-decay

# Step 2 — Funnel: identify where prospects drop off on the path to conversion
python scripts/funnel_analyzer.py funnel_data.json

# Step 3 — ROI: calculate profitability and benchmark against industry standards
python scripts/campaign_roi_calculator.py campaign_data.json
```

利用归因分析结果确定表现最佳的渠道，然后针对这些渠道的细分人群进行漏斗分析，最后验证ROI指标，以便优先调整预算分配。

---

## 使用方法

### 归因分析

```bash
# Run all 5 attribution models
python scripts/attribution_analyzer.py campaign_data.json

# Run a specific model
python scripts/attribution_analyzer.py campaign_data.json --model time-decay

# JSON output for pipeline integration
python scripts/attribution_analyzer.py campaign_data.json --format json

# Custom time-decay half-life (default: 7 days)
python scripts/attribution_analyzer.py campaign_data.json --model time-decay --half-life 14
```

### 漏斗分析

```bash
# Basic funnel analysis
python scripts/funnel_analyzer.py funnel_data.json

# JSON output
python scripts/funnel_analyzer.py funnel_data.json --format json
```

### 活动ROI计算

```bash
# Calculate ROI metrics for all campaigns
python scripts/campaign_roi_calculator.py campaign_data.json

# JSON output
python scripts/campaign_roi_calculator.py campaign_data.json --format json
```

---

## 脚本说明

### 1. attribution_analyzer.py

实现五种行业标准的归因模型，用于将转化功劳分配给不同的营销渠道：
| 模型 | 描述 | 适用场景 |
|-------|-------------|----------|
| 首次触点 | 将100%的功劳归于首次互动 | 品牌 awareness 活动 |
| 最后触点 | 将100%的功劳归于最后一次互动 | 直接响应活动 |
| 线性 | 所有触点平均分配功劳 | 平衡的多渠道评估 |
| 时间衰减 | 更多功劳归于最近的触点 | 销售周期较短的活动 |
| 位置-based | 40/20/40的比例分配（首次/中间/最后一次） | 全渠道营销 |

### 2. funnel_analyzer.py

分析转化漏斗，以识别瓶颈和优化机会：
- 各阶段的转化率和流失率
- 自动识别瓶颈（绝对值和相对值最大的环节）
- 整体漏斗转化率
- 当提供多个细分人群时，可以进行对比分析

### 3. campaign_roi_calculator.py

计算全面的ROI指标，并提供行业基准数据：
- **ROI**：投资回报率
- **ROAS**：广告支出回报率
- **CPA**：每次获取客户的成本
- **CPL**：每次转化的成本
- **CAC**：客户获取成本
- **CTR**：点击率
- **CVR**：转化率（转化为客户的数量）
- 标记表现不佳的活动，以便与行业基准进行对比

---

## 参考指南

| 名称 | 位置 | 用途 |
|-------|----------|---------|
| 归因模型指南 | `references/attribution-models-guide.md` | 详细介绍五种归因模型，包括计算公式、优缺点及选择标准 |
| 活动指标基准 | `references/campaign-metrics-benchmarks.md` | 按渠道和行业提供CTR、CPC、CPM、CPA、ROAS等指标的行业基准 |
| 漏斗优化框架 | `references/funnel-optimization-framework.md` | 分阶段优化策略、常见瓶颈及最佳实践 |

---

## 最佳实践

1. **使用多种归因模型**——至少比较三种模型，以全面评估各渠道的价值；单一模型无法提供完整的信息。
2. **设置合适的回顾窗口**——根据平均销售周期长度来设定时间衰减周期。
3. **对漏斗数据进行细分**——比较不同细分人群（渠道、群体、地理位置）以识别影响效果的因素。
4. **首先与自身历史数据对比**——行业基准可以提供参考，但历史数据是最重要的对比依据。
5. **定期进行ROI分析**——活跃活动每周分析一次，战略性评估每月进行一次。
6. **包含所有成本**——在计算ROI时，不仅要考虑媒体支出，还要考虑创意、工具和人力成本。
7. **严格记录A/B测试结果**——使用提供的模板确保统计结果的准确性和决策依据的清晰性。

---

## 限制条件

- **不提供统计显著性测试**——脚本仅提供描述性指标；p值计算需要外部工具。
- **仅使用标准库**——不支持高级统计库。适用于大多数规模的活动，但不适合数据量超过10万条记录的情况。
- **离线分析**——脚本分析静态的JSON数据；不支持实时数据连接或API集成。
- **单一货币**——所有货币值均假设为同一货币单位；不支持货币转换。
- **简化的时间衰减模型**——基于可配置的衰减周期采用指数衰减公式；未考虑工作日/周末或季节性因素。
- **不支持跨设备追踪**——归因分析基于提供的原始数据；跨设备用户身份的识别需要在前端处理。

## 相关技能

- **数据分析与追踪**：负责设置追踪系统（而非数据分析本身）。
- **A/B测试设置**：设计实验以验证分析结果。
- **营销运营**：负责将分析结果传递给相应的执行团队。
- **付费广告**：根据分析结果优化广告支出。