---
name: data-visualization
description: |
  Data visualization with chart selection, color theory, and annotation best practices.
  Covers chart types (bar, line, scatter, heatmap), axes rules, and storytelling with data.
  Use for: charts, graphs, dashboards, reports, presentations, infographics, data stories.
  Triggers: data visualization, chart, graph, data chart, bar chart, line chart,
  scatter plot, data viz, visualization, dashboard chart, infographic data,
  data presentation, chart design, plot, heatmap, pie chart alternative
allowed-tools: Bash(infsh *)
---

# 数据可视化

通过 [inference.sh](https://inference.sh) 命令行工具创建清晰、有效的数据可视化图表。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a chart with Python
infsh app run infsh/python-executor --input '{
  "code": "import matplotlib.pyplot as plt\nimport matplotlib\nmatplotlib.use(\"Agg\")\n\nmonths = [\"Jan\", \"Feb\", \"Mar\", \"Apr\", \"May\", \"Jun\"]\nrevenue = [42, 48, 55, 61, 72, 89]\n\nfig, ax = plt.subplots(figsize=(10, 6))\nax.bar(months, revenue, color=\"#3b82f6\", width=0.6)\nax.set_ylabel(\"Revenue ($K)\")\nax.set_title(\"Monthly Revenue Growth\", fontweight=\"bold\")\nfor i, v in enumerate(revenue):\n    ax.text(i, v + 1, f\"${v}K\", ha=\"center\", fontweight=\"bold\")\nplt.tight_layout()\nplt.savefig(\"revenue.png\", dpi=150)\nprint(\"Saved\")"
}'
```

## 图表选择指南

### 哪种图表适用于哪种数据？

| 数据关系 | 最适合的图表 | 绝对不要使用 |
|------------------|-----------|-----------|
| **随时间变化的数据** | 折线图 | 饼图 |
| **比较不同类别的数据** | 横向柱状图（适用于多个类别） | 折线图 |
| **整体中的部分** | 堆叠柱状图、树状图 | 饼图（虽然有争议，但柱状图通常更清晰） |
| **数据分布** | 直方图、箱线图 | 柱状图 |
| **数据相关性** | 散点图 | 柱状图 |
| **数据排名** | 横向柱状图 | 垂直柱状图、饼图 |
| **地理数据** | 等高线地图 | 柱状图 |
| **随时间变化的组成** | 堆叠面积图 | 多个饼图 |
| **单一指标** | 大数值（关键绩效指标） | 任何图表（可能过于复杂） |
| **数据流程** | 桑基图 | 柱状图 |

### 饼图的局限性

饼图几乎总是错误的选择：

```
❌ Pie chart problems:
   - Hard to compare similar-sized slices
   - Can't show more than 5-6 categories
   - 3D pie charts are always wrong
   - Impossible to read exact values

✅ Use instead:
   - Horizontal bar chart (easy comparison)
   - Stacked bar (part of whole)
   - Treemap (hierarchical parts)
   - Just a table (if precision matters)
```

## 设计规则

### 轴

| 规则 | 原因 |
|------|-----|
| Y轴始终从0开始（柱状图） | 避免误导观众 |
| 折线图可以不从0开始 | 当展示变化趋势而非绝对值时 |
| 为两个轴都添加标签 | 读者不应猜测单位 |
| 删除不必要的网格线 | 减少视觉干扰 |
| 使用水平标签 | 垂直文本难以阅读 |
| 按数值对柱状图进行排序 | 除非有特殊原因，否则不要按字母顺序排序 |

### 颜色

| 原则 | 应用方法 |
|-----------|------------|
| 每个图表最多使用5-7种颜色 | 色彩过多会降低可读性 |
| 突出重点内容 | 其他部分使用灰色，重点部分使用特定颜色 |
| 根据数值大小使用颜色渐变 | 从浅色到深色表示数值从小到大 |
| 根据正负值使用不同的颜色 | 正数为红色，中性为中性色，负数为蓝色 |
| 对于分类数据使用不同的颜色 | 使用不同的色调，但亮度相近 |
| 适合色盲用户 | 避免仅使用红色/绿色——可以添加形状或文字说明 |
| 保持颜色的一致性 | 如果蓝色代表收入，那么在整个图表中都使用蓝色 |

### 好的配色方案

```python
# Sequential (low to high)
sequential = ["#eff6ff", "#bfdbfe", "#60a5fa", "#2563eb", "#1d4ed8"]

# Diverging (negative to positive)
diverging = ["#ef4444", "#f87171", "#d1d5db", "#34d399", "#10b981"]

# Categorical (distinct groups)
categorical = ["#3b82f6", "#f59e0b", "#10b981", "#8b5cf6", "#ef4444"]

# Colorblind-safe
cb_safe = ["#0077BB", "#33BBEE", "#009988", "#EE7733", "#CC3311"]
```

### 文本和标签

| 元素 | 规则 |
|---------|------|
| **标题** | 需要传达的洞察，而不是数据类型。例如：“第二季度收入翻了一番”，而不是“第二季度收入图表” |
| **注释** | 直接在图表上标注关键数据点 |
| **图例** | 尽量避免使用图例——直接在图表线条/柱子上标注 |
| **字体大小** | 演示文稿中至少使用12px或14px以上的字体 |
| **数字格式** | 使用K、M、B等符号表示大数值（例如42K而不是42,000） |
| **数据标签** | 当需要显示精确数值时，为柱子/数据点添加标签 |

## 图表制作技巧

### 折线图（时间序列）

```bash
infsh app run infsh/python-executor --input '{
  "code": "import matplotlib.pyplot as plt\nimport matplotlib\nmatplotlib.use(\"Agg\")\n\nfig, ax = plt.subplots(figsize=(12, 6))\nfig.patch.set_facecolor(\"white\")\n\nmonths = [\"Jan\", \"Feb\", \"Mar\", \"Apr\", \"May\", \"Jun\", \"Jul\", \"Aug\", \"Sep\", \"Oct\", \"Nov\", \"Dec\"]\nthis_year = [120, 135, 148, 162, 178, 195, 210, 228, 245, 268, 290, 320]\nlast_year = [95, 102, 108, 115, 122, 130, 138, 145, 155, 165, 178, 190]\n\nax.plot(months, this_year, color=\"#3b82f6\", linewidth=2.5, marker=\"o\", markersize=6, label=\"2024\")\nax.plot(months, last_year, color=\"#94a3b8\", linewidth=2, linestyle=\"--\", label=\"2023\")\nax.fill_between(range(len(months)), last_year, this_year, alpha=0.1, color=\"#3b82f6\")\n\nax.annotate(\"$320K\", xy=(11, 320), fontsize=14, fontweight=\"bold\", color=\"#3b82f6\")\nax.annotate(\"$190K\", xy=(11, 190), fontsize=12, color=\"#94a3b8\")\n\nax.set_ylabel(\"Revenue ($K)\", fontsize=12)\nax.set_title(\"Revenue grew 68% year-over-year\", fontsize=16, fontweight=\"bold\")\nax.legend(fontsize=12)\nax.spines[\"top\"].set_visible(False)\nax.spines[\"right\"].set_visible(False)\nax.grid(axis=\"y\", alpha=0.3)\nplt.tight_layout()\nplt.savefig(\"line-chart.png\", dpi=150)\nprint(\"Saved\")"
}'
```

### 横向柱状图（比较）

```bash
infsh app run infsh/python-executor --input '{
  "code": "import matplotlib.pyplot as plt\nimport matplotlib\nmatplotlib.use(\"Agg\")\n\nfig, ax = plt.subplots(figsize=(10, 6))\n\ncategories = [\"Email\", \"Social\", \"SEO\", \"Paid Ads\", \"Referral\", \"Direct\"]\nvalues = [12, 18, 35, 22, 8, 5]\ncolors = [\"#94a3b8\"] * len(values)\ncolors[2] = \"#3b82f6\"  # Highlight the winner\n\n# Sort by value\nsorted_pairs = sorted(zip(values, categories, colors))\nvalues, categories, colors = zip(*sorted_pairs)\n\nax.barh(categories, values, color=colors, height=0.6)\nfor i, v in enumerate(values):\n    ax.text(v + 0.5, i, f\"{v}%\", va=\"center\", fontsize=12, fontweight=\"bold\")\n\nax.set_xlabel(\"% of Total Traffic\", fontsize=12)\nax.set_title(\"SEO drives the most traffic\", fontsize=16, fontweight=\"bold\")\nax.spines[\"top\"].set_visible(False)\nax.spines[\"right\"].set_visible(False)\nplt.tight_layout()\nplt.savefig(\"bar-chart.png\", dpi=150)\nprint(\"Saved\")"
}'
```

### 关键绩效指标/大数值展示

```bash
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"display:flex;gap:20px;padding:20px;background:white;font-family:system-ui\"><div style=\"background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:24px;width:200px;text-align:center\"><p style=\"color:#64748b;font-size:14px;margin:0\">Monthly Revenue</p><p style=\"font-size:48px;font-weight:900;margin:8px 0;color:#1e293b\">$89K</p><p style=\"color:#22c55e;font-size:14px;margin:0\">↑ 23% vs last month</p></div><div style=\"background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:24px;width:200px;text-align:center\"><p style=\"color:#64748b;font-size:14px;margin:0\">Active Users</p><p style=\"font-size:48px;font-weight:900;margin:8px 0;color:#1e293b\">12.4K</p><p style=\"color:#22c55e;font-size:14px;margin:0\">↑ 8% vs last month</p></div><div style=\"background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:24px;width:200px;text-align:center\"><p style=\"color:#64748b;font-size:14px;margin:0\">Churn Rate</p><p style=\"font-size:48px;font-weight:900;margin:8px 0;color:#1e293b\">2.1%</p><p style=\"color:#ef4444;font-size:14px;margin:0\">↑ 0.3% vs last month</p></div></div>"
}'
```

### 热力图

```bash
infsh app run infsh/python-executor --input '{
  "code": "import matplotlib.pyplot as plt\nimport numpy as np\nimport matplotlib\nmatplotlib.use(\"Agg\")\n\nfig, ax = plt.subplots(figsize=(10, 6))\n\ndays = [\"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Fri\", \"Sat\", \"Sun\"]\nhours = [\"9AM\", \"10AM\", \"11AM\", \"12PM\", \"1PM\", \"2PM\", \"3PM\", \"4PM\", \"5PM\"]\ndata = np.random.randint(10, 100, size=(len(hours), len(days)))\ndata[2][1] = 95  # Tuesday 11AM peak\ndata[2][3] = 88  # Thursday 11AM\n\nim = ax.imshow(data, cmap=\"Blues\", aspect=\"auto\")\nax.set_xticks(range(len(days)))\nax.set_yticks(range(len(hours)))\nax.set_xticklabels(days, fontsize=12)\nax.set_yticklabels(hours, fontsize=12)\n\nfor i in range(len(hours)):\n    for j in range(len(days)):\n        color = \"white\" if data[i][j] > 60 else \"black\"\n        ax.text(j, i, data[i][j], ha=\"center\", va=\"center\", fontsize=10, color=color)\n\nax.set_title(\"Website Traffic by Day & Hour\", fontsize=16, fontweight=\"bold\")\nplt.colorbar(im, label=\"Visitors\")\nplt.tight_layout()\nplt.savefig(\"heatmap.png\", dpi=150)\nprint(\"Saved\")"
}'
```

## 用数据讲故事

### 叙事结构

| 步骤 | 需要做什么 | 示例 |
|------|-----------|---------|
| 1. **背景** | 说明读者需要了解的信息 | “我们每月跟踪客户获取成本” |
| 2. **问题/变化** | 展示问题或变化 | “第三季度的客户获取成本增加了40%” |
| 3. **解决方案** | 展示洞察或解决方案 | “但客户生命周期价值增加了80%，因此单位经济效益得到了提升” |

### 标题应传达核心洞察

```
❌ Descriptive titles (what the chart shows):
   "Q3 Revenue by Product Line"
   "Monthly Active Users 2024"
   "Customer Satisfaction Survey Results"

✅ Insight titles (what the chart means):
   "Enterprise product drives 70% of revenue growth"
   "User growth accelerated after the free tier launch"
   "Support response time is the #1 satisfaction driver"
```

### 注释技巧

| 技巧 | 适用场景 |
|-----------|------------|
| **突出显示特定数据点** | 强调某个具体的数据点（例如：“峰值：32万”） |
| **参考线** | 显示目标或基准值（例如：“目标：10万”） |
| **阴影区域** | 标记某个时间段（例如：“产品发布窗口”） |
| **箭头+文字** | 引导观众注意趋势变化 |
| **前后对比线** | 显示事件的影响 |

## 暗模式图表

```bash
infsh app run infsh/python-executor --input '{
  "code": "import matplotlib.pyplot as plt\nimport matplotlib\nmatplotlib.use(\"Agg\")\n\n# Dark theme\nplt.rcParams.update({\n    \"figure.facecolor\": \"#0f172a\",\n    \"axes.facecolor\": \"#0f172a\",\n    \"axes.edgecolor\": \"#334155\",\n    \"axes.labelcolor\": \"white\",\n    \"text.color\": \"white\",\n    \"xtick.color\": \"white\",\n    \"ytick.color\": \"white\",\n    \"grid.color\": \"#1e293b\"\n})\n\nfig, ax = plt.subplots(figsize=(12, 6))\nmonths = [\"Jan\", \"Feb\", \"Mar\", \"Apr\", \"May\", \"Jun\"]\nvalues = [45, 52, 58, 72, 85, 98]\n\nax.plot(months, values, color=\"#818cf8\", linewidth=3, marker=\"o\", markersize=8)\nax.fill_between(range(len(months)), values, alpha=0.15, color=\"#818cf8\")\nax.set_title(\"MRR Growth: On track for $100K\", fontsize=18, fontweight=\"bold\")\nax.set_ylabel(\"MRR ($K)\", fontsize=13)\nax.spines[\"top\"].set_visible(False)\nax.spines[\"right\"].set_visible(False)\nax.grid(axis=\"y\", alpha=0.2)\n\nfor i, v in enumerate(values):\n    ax.annotate(f\"${v}K\", (i, v), textcoords=\"offset points\", xytext=(0, 12), ha=\"center\", fontsize=11, fontweight=\"bold\")\n\nplt.tight_layout()\nplt.savefig(\"dark-chart.png\", dpi=150, facecolor=\"#0f172a\")\nprint(\"Saved\")"
}'
```

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 使用饼图 | 难以比较数据，容易产生误导 | 使用柱状图或树状图 |
| Y轴没有从0开始（柱状图） | 会夸大数据差异 | 柱状图的Y轴必须从0开始；折线图可以适当截断 |
| 颜色过多 | 造成视觉干扰 | 最多使用5-7种颜色，只突出重点 |
| 没有标题或标题过于笼统 | 读者无法理解图表的意义 | 标题应明确传达核心洞察 |
| 3D图表 | 会扭曲数据，显得不专业 | 始终使用2D图表 |
| 双Y轴 | 误导观众，难以阅读 | 使用两个独立的图表 |
| 按字母顺序排序柱状图 | 会掩盖数据的真实关系 | 按数值大小排序（从大到小） |
| 轴上没有标签 | 观众无法理解数据 | 必须为轴添加标签 |
| 非必要的装饰元素 | 会分散观众的注意力 | 删除所有不传递信息的元素 |
| 仅使用红色/绿色进行颜色编码 | 色盲用户难以区分颜色 | 可以使用形状、图案或适合色盲用户的配色方案 |

## 相关技能

```bash
npx skills add inferencesh/skills@pitch-deck-visuals
npx skills add inferencesh/skills@technical-blog-writing
npx skills add inferencesh/skills@competitor-teardown
```

浏览所有应用程序：`infsh app list`