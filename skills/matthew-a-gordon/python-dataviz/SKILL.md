---
name: python-dataviz
description: 使用 Python（matplotlib、seaborn、plotly）进行专业的数据可视化。可以创建符合出版标准的静态图表、统计可视化结果以及交互式图形。适用于从数据生成图表、制作包含数据组件的信息图，或生成科学/统计可视化内容。支持导出为 PNG/SVG（静态格式）和 HTML（交互式格式）。
---
# Python数据可视化

使用Python领先的库来创建专业的图表、图形和统计可视化效果。

## 库及其使用场景

**matplotlib** - 静态图表，适合出版物质量，具有完全的控制能力
- 条形图、折线图、散点图、饼图、直方图、热力图
- 多面板图形、子图
- 自定义样式、注释
- 导出格式：PNG、SVG、PDF

**seaborn** - 统计可视化工具，提供美观的默认样式
- 分布图（小提琴图、箱线图、KDE图、直方图）
- 分类图（条形图、计数图、群集图）
- 关系图（散点图、折线图、回归图）
- 矩阵图（热力图、聚类图）
- 基于matplotlib构建，可无缝集成

**plotly** - 交互式图表，适合网页展示
- 鼠标悬停提示、缩放、平移功能
- 3D图表、动画效果
- 可通过Dash框架构建仪表板
- 导出格式：HTML、PNG（需要kaleido库）

## 快速入门

### 设置环境

```bash
cd skills/python-dataviz
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

### 创建图表

```python
import matplotlib.pyplot as plt
import numpy as np

# Data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(x, y, linewidth=2, color='#667eea')
plt.title('Sine Wave', fontsize=16, fontweight='bold')
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.grid(alpha=0.3)
plt.tight_layout()

# Export
plt.savefig('output.png', dpi=300, bbox_inches='tight')
plt.savefig('output.svg', bbox_inches='tight')
```

## 图表选择指南

**分布/统计图表：**
- 直方图 → `plt.hist()` 或 `sns.histplot()`
- 箱线图 → `sns.boxplot()`
- 小提琴图 → `sns.violinplot()`
- KDE图 → `sns.kdeplot()`

**比较图表：**
- 条形图 → `plt.bar()` 或 `sns.barplot()`
- 分组条形图 → `sns.barplot(hue=...)`
- 水平条形图 → `plt.barh()` 或 `sns.barplot(orient='h')`

**关系图表：**
- 散点图 → `plt.scatter()` 或 `sns.scatterplot()`
- 折线图 → `plt.plot()` 或 `sns.lineplot()`
- 回归图 → `sns.regplot()` 或 `sns.lmplot()`

**热力图：**
- 相关系数矩阵 → `sns.heatmap(df.corr())`
- 二维数据 → `plt.imshow()` 或 `sns.heatmap()`

**交互式图表：**
- 任何使用plotly绘制的图表 → `plotly.express` 或 `plotly.graph_objects`
- 详情请参阅 references/plotly-examples.md

## 最佳实践

### 1. 图表大小与DPI设置
```python
plt.figure(figsize=(10, 6))  # Width x Height in inches
plt.savefig('output.png', dpi=300)  # Publication: 300 dpi, Web: 72-150 dpi
```

### 2. 颜色调色板选择
```python
# Seaborn palettes (works with matplotlib too)
import seaborn as sns
sns.set_palette("husl")  # Colorful
sns.set_palette("muted")  # Soft
sns.set_palette("deep")  # Bold

# Custom colors
colors = ['#667eea', '#764ba2', '#f6ad55', '#4299e1']
```

### 3. 图表样式设置
```python
# Use seaborn styles even for matplotlib
import seaborn as sns
sns.set_theme()  # Better defaults
sns.set_style("whitegrid")  # Options: whitegrid, darkgrid, white, dark, ticks

# Or matplotlib styles
plt.style.use('ggplot')  # Options: ggplot, seaborn, bmh, fivethirtyeight
```

### 4. 多个子图的使用
```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes[0, 0].plot(x, y1)
axes[0, 1].plot(x, y2)
# etc.
plt.tight_layout()  # Prevent label overlap
```

### 5. 图表导出格式
```python
# PNG for sharing/embedding (raster)
plt.savefig('chart.png', dpi=300, bbox_inches='tight', transparent=False)

# SVG for editing/scaling (vector)
plt.savefig('chart.svg', bbox_inches='tight')

# For plotly (interactive)
import plotly.express as px
fig = px.scatter(df, x='col1', y='col2')
fig.write_html('chart.html')
```

## 高级主题

详细指南请参阅相关参考资料：

- **颜色理论与调色板**：references/colors.md
- **统计图表**：references/statistical.md
- **Plotly交互式图表**：references/plotly-examples.md
- **多面板布局**：references/layouts.md

## 示例脚本

请查看 scripts/ 目录中的示例脚本：

- `scripts/bar_chart.py` - 条形图和分组条形图
- `scripts/line_chart.py` - 多序列折线图
- `scripts/scatter_plot.py` - 带有回归分析的散点图
- `scripts/heatmap.py` - 相关系数热力图
- `scripts/distribution.py` - 直方图、KDE图、小提琴图
- `scripts/interactive.py` - Plotly交互式图表

## 常见问题解决方法

### “找不到matplotlib模块”
```bash
cd skills/python-dataviz
source .venv/bin/activate
pip install -r requirements.txt
```

### 图表为空
- 确保 `plt.savefig()` 在所有绘图命令之后执行
- 开发过程中使用 `plt.show()` 进行交互式查看

### 图表标签被截断
```python
plt.tight_layout()  # Add before plt.savefig()
# Or
plt.savefig('output.png', bbox_inches='tight')
```

### 图表分辨率较低
```python
plt.savefig('output.png', dpi=300)  # Not 72 or 100
```

## 开发环境

该技能包含一个包含所有依赖项的虚拟环境（venv）。使用前请务必激活该环境：

```bash
cd /home/matt/.openclaw/workspace/skills/python-dataviz
source .venv/bin/activate
```

依赖项：matplotlib, seaborn, plotly, pandas, numpy, kaleido（用于Plotly静态导出）