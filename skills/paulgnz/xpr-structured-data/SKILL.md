---
name: structured-data
description: CSV解析、JSON转CSV转换以及SVG图表生成
---

## 结构化数据

您拥有处理结构化数据以及生成可视化内容的工具：

**CSV处理：**
- `parse_csv` — 将CSV文本解析为JSON对象数组
  - 自动检测分隔符（逗号、制表符、分号、竖线）
  - 支持包含嵌入逗号和新行的字段
  - 返回`data`（完整数组）、`columns`（列信息）、`row_count`（行数）以及`preview`（前5行数据）
  - 可通过`limit`参数处理大型数据集，仅获取前N行数据

- `json_to_csv` — 将JSON对象数组转换为CSV文本
  - 会自动为包含分隔符、换行符或引号的字段添加引号
  - 可通过`columns`参数选择或重新排序特定列
  - 嵌套对象会通过`JSON.stringify`进行序列化

**图表：**
- `generate_chart` — 根据数据生成SVG图表
  - 图表类型：条形图（bar）、折线图（line）、饼图（pie）
  - 单系列数据格式：`{ labels: ["A", "B"], values: [10, 20] }`
  - 多系列数据格式：`{ labels: ["Q1", "Q2"], series: [{ name: "2024", values: [10, 20] }, { name: "2025", values: [15, 25] }] }`
  - 返回`svg`（原始SVG代码）和`data_uri`（用于嵌入Markdown的Base64编码格式）
  - 在Markdown中嵌入图表的格式：`![图表](data:image/svg+xml;base64,...)`

**最佳实践：**
- 使用`parse_csv`将CSV数据转换为JSON格式以便进一步处理
- 使用`json_to_csv`将处理后的数据转换回CSV格式以便输出
- 使用`generate_chart`生成可视化图表用于报告展示
- 结合`execute_js`（代码沙箱功能）进行复杂的数据转换
- 结合`store_deliverable`将生成的图表和处理后的数据保存为工作成果
- 通过`data_uri`将图表嵌入PDF文档中