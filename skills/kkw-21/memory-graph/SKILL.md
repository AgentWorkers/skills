# 内存图谱（Memory Graph）

将内存集群以交互式知识图谱的形式进行可视化展示和导航。能够将使用 Luhmann 编码存储的数据转换为可探索的节点-链接图，支持集群高亮显示、文本说明以及实时更新功能。

## 使用方法

```bash
memory-graph render <graph-id>     # Generate graph visualization
memory-graph explore <graph-id>    # Interactive exploration mode
memory-graph export <graph-id>     # Export as SVG/PNG/JSON
```

## 主要功能：

- 具有集群识别能力的布局系统，可自动对数据进行分析并分组；
- 为每个内存集群生成相应的文本说明；
- 支持发现不同用户之间的数据关联；
- 提供适用于 Web 视窗的输出格式，便于集成到应用程序中。