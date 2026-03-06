---
name: warehouse-chart-reports
description: 从 SQLite/CSV 数据生成仓库分析图表、表格图像以及可用于报告的可视化素材。当用户需要仓库图表、产品表格图像、库存状况饼图、收入/利润数据图表、缺失产品的可视化展示，或是用于 PDF 或幻灯片报告的图片资源时，可使用该功能。
---
# 仓库图表报告

使用此技能可以生成用于仓库演示的清晰图表/报告图像。

## 运行完整的仓库可视化工具包（推荐）

执行：

```bash
python skills/warehouse-chart-reports/scripts/run_warehouse_reports.py \
  --db demo/warehouse_agent/warehouse_demo.db \
  --out demo/warehouse_agent/outputs
```

这将生成以下文件：
- `stock_status_pie.png`（库存状况饼图）
- `revenue_by_category.png`（按类别划分的收入图表）
- `daily_profit_30d.png`（过去30天的每日利润图表）
- `product_table_top40.png`（排名前40的产品表格）
- `missing_products.csv`（缺失产品的列表）
- `kpi_summary.txt`（关键绩效指标摘要）

## 仅生成产品表格图像

执行：

```bash
python skills/warehouse-chart-reports/scripts/product_table_image.py \
  --db demo/warehouse_agent/warehouse_demo.db \
  --out demo/warehouse_agent/outputs/product_table_top40.png \
  --limit 40
```

## 注意事项：

- 如果系统上没有matplotlib，建议使用virtualenv环境来安装Python相关库。
- 保持图表样式简洁易读，以便用于PDF嵌入。
- 如果当天的销售时间戳数据较少，可以使用过去30天的利润图表来观察销售趋势。