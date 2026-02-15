---
name: evolution-state-analyzer
description: 分析内存使用情况的演变图表，以识别停滞模式、重复出现的故障以及性能提升的瓶颈。生成可操作的洞察，为未来的开发周期提供指导。
---
# 进化状态分析器

该技能通过分析 `memory_graph.jsonl` 文件，对进化过程本身进行元分析。

## 功能

- **停滞检测**：识别没有改进的重复循环。
- **基因效能分析**：追踪哪些基因具有最高的成功率。
- **故障原因聚类分析**：将故障原因分组，以确定系统性问题。
- **趋势报告**：可视化随时间变化的进化得分趋势。

## 使用方法

```javascript
const analyzer = require('./index');
const insights = await analyzer.analyzeState();
console.log(JSON.stringify(insights, null, 2));
```

## 示例输出

```json
{
  "total_cycles": 120,
  "success_rate": 0.75,
  "stagnation_detected": true,
  "top_genes": [
    { "id": "gene_repair_v2", "success_rate": 0.95 },
    { "id": "gene_innovate_v1", "success_rate": 0.40 }
  ],
  "recommendations": [
    "Switch to INNOVATE intent (stagnation streak: 5)",
    "Deprecate gene_innovate_v1 (success rate < 0.5)"
  ]
}
```