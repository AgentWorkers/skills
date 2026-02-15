# KPI 追踪技能

该技能用于跟踪、分析并报告任何业务的关键绩效指标（KPI）。

## 功能介绍

激活此技能后，它可以帮助您：
- 定义并分类 KPI（例如收入、运营、市场营销、客户成功等）
- 设置目标及阈值（分为绿色、黄色、红色三个等级）
- 以 Markdown 格式生成每周/每月的 KPI 报告
- 标记偏离目标的 KPI 并提示其根本原因
- 将历史数据存储在简单的 JSON 文件中，以便进行趋势分析

## 使用方法

您可以告诉机器人：“跟踪这些 KPI”，或“生成一份 KPI 报告”，或“哪些指标偏离了目标？”

### 设置

在工作区中创建 `kpi-config.json` 文件：

```json
{
  "kpis": [
    {
      "name": "Monthly Recurring Revenue",
      "category": "revenue",
      "unit": "$",
      "target": 50000,
      "redBelow": 35000,
      "yellowBelow": 45000
    },
    {
      "name": "Customer Churn Rate",
      "category": "customer",
      "unit": "%",
      "target": 3,
      "redAbove": 7,
      "yellowAbove": 5
    }
  ]
}
```

### 记录数据

例如：您可以说：“本周的 MRR 记录为 42,000 美元”。

机器人会将相关数据存储到 `kpi-data.json` 文件中：

```json
{
  "entries": [
    { "kpi": "Monthly Recurring Revenue", "value": 42000, "date": "2026-02-13", "note": "Post-launch week" }
  ]
}
```

### 生成报告

您可以说：“生成 KPI 报告”，机器人会生成一份格式化的报告：

```
📊 KPI Report — Week of Feb 10, 2026

🟢 Monthly Recurring Revenue: $48,200 (target: $50,000) — 96.4%
🔴 Customer Churn Rate: 8.1% (target: 3%) — needs attention
🟡 Lead Conversion Rate: 11% (target: 15%) — trending up from 9%

⚠️ Action needed on 1 red, 1 yellow KPI
```

### 趋势分析

您可以说：“显示 MRR 的趋势”，机器人会读取历史数据并总结其变化趋势、发展速度以及按照当前进度是否能够达成目标。

## 机器人的行为规范：

1. 从 `kpi-config.json` 文件中读取 KPI 的定义
2. 读写 `kpi-data.json` 文件以获取历史数据
3. 当被要求生成报告时，计算每个 KPI 的当前状态，并用颜色进行可视化展示
4. 如果某个 KPI 的数值处于红色警告状态，机器人会主动建议需要调查的问题
5. 在记录数据时，机器人会验证数值的合理性（例如，流失率不可能为负数）

## 文件位置：

- 配置文件：`kpi-config.json`（位于工作区根目录或自定义路径）
- 数据文件：`kpi-data.json`（与配置文件位于同一目录）
- 报告文件：按需生成，可选择性保存到 `reports/kpi-YYYY-MM-DD.md` 文件夹中

## 使用技巧

建议将此技能与定时任务（cron job）结合使用，以自动生成每周的 KPI 报告。如需更深入的业务洞察或预设的行业 KPI 模板，可以查看 [AfrexAI Context Packs](https://afrexai-cto.github.io/context-packs/)——这些模板为 10 多个行业提供了现成的 KPI 监控方案。