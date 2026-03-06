---
name: data-visualization-studio
description: 从数据集中创建交互式和静态的数据可视化图表。支持生成各种类型的图表（如柱状图、折线图、仪表盘等），并提供多种输出格式（PNG、SVG、HTML、PDF）。
---
# 数据可视化工作室

从原始数据或现有数据集中创建专业的数据可视化图表。

## 使用场景

- 从 CSV、JSON 或数据库数据中生成图表
- 构建用于数据探索的交互式仪表板
- 生成统计图表和视觉分析结果
- 以多种格式（PNG、SVG、HTML、PDF）导出可视化结果
- 创建适合发布的图表和报告

## 快速入门

### 基本图表创建
```python
# Example: Create a simple bar chart
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('data.csv')
plt.bar(data['category'], data['values'])
plt.savefig('chart.png', dpi=300, bbox_inches='tight')
```

### 交互式仪表板
```python
# Example: Create interactive plot with Plotly
import plotly.express as px

df = pd.read_csv('data.csv')
fig = px.scatter(df, x='x_column', y='y_column', color='category')
fig.write_html('dashboard.html')
```

## 支持的库

- **Matplotlib**：静态图表，适合出版的高质量图形
- **Plotly**：交互式可视化效果，支持 Web 仪表板
- **Seaborn**：统计图形工具，提供美观的默认样式
- **Bokeh**：交互式 Web 图表，支持流式数据
- **Altair**：声明式可视化工具，支持 Vega-Lite 插件

## 输出格式

- **PNG/JPEG**：高分辨率的静态图像
- **SVG**：可缩放的矢量图形，适用于 Web 或打印
- **HTML**：嵌入 JavaScript 的交互式网页
- **PDF**：适合发布的文档格式
- **JSON**：用于进一步处理的数据导出格式

## 最佳实践

1. **数据准备**：在可视化之前对数据进行清洗和验证
2. **颜色方案**：使用易于阅读的颜色方案（避免使用红色和绿色）
3. **标签**：务必添加清晰的轴标签和标题
4. **分辨率**：根据使用场景选择合适的 DPI（Web 用 72，打印用 300+）
5. **文件大小**：根据需要优化文件大小以适应 Web 浏览

## 高级功能

- **动画效果**：创建动画过渡效果和时间序列可视化图表
- **地理空间分析**：结合地理数据的地图可视化
- **3D 图表**：三维数据展示
- **自定义样式**：保持与品牌一致的视觉风格
- **实时更新**：从流式数据中实时更新可视化内容

## 参考资料

有关详细示例和高级使用方法，请参阅随附的参考文件：
- `references/chart-types.md`：支持的图表类型完整目录
- `references/styling-guide.md`：自定义和品牌化指南
- `references/performance.md**：针对大型数据集的优化建议