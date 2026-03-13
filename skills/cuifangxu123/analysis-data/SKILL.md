---
name: data-analysis
description: >
  数据分析技能提供三大核心功能：数据分析、数据解读和数据可视化。
  **使用场景**：
  (1) 数据分析 - 统计分析、数据过滤、数据聚合、数值计算（例如：“计算总销售额”、“筛选数据量超过100条的记录”）
  (2) 数据解读 - 趋势分析、模式识别、报告生成（例如：“分析销售趋势”、“解读数据变化”
  (3) 数据可视化 - 图表生成、数据显示（例如：“绘制条形图”、“生成饼状图”）
  **相关关键词**：分析数据、统计分析、计算、解读趋势、生成图表、可视化、数据绘制
  **前提条件**：需要设置环境变量 CHARTGEN_API_KEY（请从 chartgen.ai 获取该密钥）
metadata:
  openclaw:
    requires:
      env:
        - CHARTGEN_API_KEY
---
# ChartGen 数据分析

基于 ChartGen API 的数据分析技能，支持基于自然语言的数据分析、解释和可视化。

## 概述

该技能通过自然语言交互实现无需代码的数据分析。它支持 Text2SQL、Text2Data 和 Text2Code 分析功能。只需提供 Excel/CSV 文件或 JSON 数据，即可自动执行数据查询、数据解释和数据可视化（ChatBI）。

该技能能够通过对话式查询智能解析时间、指标和分析维度，然后生成数据 SQL 查询，创建交互式 BI 图表和结构化分析报告。该技能针对标准化的垂直数据集进行了优化，由企业级分析引擎提供支持，确保结果的可靠性。

**API 服务**：该技能使用托管在 [chartgen.ai](https://chartgen.ai) 的 ChartGen API 服务。所有数据都会被发送到 `https://chartgen.ai/api/platform_api/` 进行处理。

---

## 快速入门

### 1. 申请 API 密钥

您可以在 [chartgen.ai](https://chartgen.ai) 上轻松创建和管理您的 API 密钥。首先，您需要注册一个账户。

**步骤：**
1. 访问 [chartgen.ai](https://chartgen.ai) 并注册账户
2. 进入 API 管理控制台
3. 创建一个新的 API 并设置信用额度
4. 复制 API 密钥以供使用

### 2. 配置环境变量

```bash
export CHARTGEN_API_KEY="your-api-key-here"
```

### 3. 运行脚本

```bash
# Data Analysis
python scripts/data_analysis.py --query "Calculate total sales by region" --file sales.xlsx

# Data Interpretation
python scripts/data_interpretation.py --query "Analyze sales trends" --file sales.xlsx

# Data Visualization
python scripts/data_visualization.py --query "Draw a bar chart of sales by region" --file sales.xlsx
```

---

## 信用规则

- 调用单个工具消耗 20 个信用点
- 免费账户每月可免费使用 200 个信用点
- 信用点用完后，您可以在 [chartgen.ai 的计费页面](https://chartgen.ai/billing) 购买更多信用点或升级账户

---

## 脚本参考

| 脚本 | 功能 | 使用场景 |
|--------|----------|----------|
| `data_analysis.py` | 数据分析 | 统计分析、过滤、聚合、计算 |
| `data_interpretation.py` | 数据解释 | 趋势分析、模式发现、报告生成 |
| `data_visualization.py` | 数据可视化 | 图表生成、数据显示 |

---

## 参数

### 常见参数

| 参数 | 是否必填 | 描述 |
|-----------|----------|-------------|
| `--query` | ✅ | 自然语言查询语句 |
| `--file` | ❌ | 本地文件路径（.xlsx/.xls/.csv），与 --json 互斥 |
| `--json` | ❌ | JSON 数据（字符串或文件路径），与 --file 互斥 |

### 可视化特定参数

| 参数 | 描述 |
|-----------|-------------|
| `--output, -o` | 输出 HTML 文件路径（默认为 /tmp/openclaw/charts/） |

---

## 数据格式

### 文件格式

支持 `.xlsx`、`.xls`、`.csv` 格式的 Excel 和 CSV 文件。

注意：只需提供 --file 或 --json 中的一个。如果同时提供了两个参数，--file 优先生效。文件类型支持行-指标-列格式和列-指标-行格式的数据文件。

### JSON 格式

JSON 数据应为数组格式，其中每个元素表示一行数据：

```json
[
  {"name": "Product A", "sales": 1000, "region": "East"},
  {"name": "Product B", "sales": 1500, "region": "North"},
  {"name": "Product C", "sales": 800, "region": "South"}
]
```

或者通过文件传递数据：

```bash
python scripts/data_analysis.py --query "Analyze the data" --json data.json
```

---

## 使用示例

### 数据分析

```bash
# Statistical calculation
python scripts/data_analysis.py --query "Calculate total and average sales by region" --file sales.xlsx

# Data filtering
python scripts/data_analysis.py --query "Filter products with sales greater than 1000" --file sales.xlsx

# Sorting
python scripts/data_analysis.py --query "Sort by sales in descending order" --file sales.xlsx
```

### 数据解释

```bash
# Trend analysis
python scripts/data_interpretation.py --query "Analyze monthly sales trends" --file monthly_sales.xlsx

# Anomaly detection
python scripts/data_interpretation.py --query "Find and explain anomalies in the data" --file data.xlsx

# Comprehensive interpretation
python scripts/data_interpretation.py --query "Provide a comprehensive analysis of this data with key insights" --file report.xlsx
```

### 数据可视化

```bash
# Bar chart
python scripts/data_visualization.py --query "Draw a bar chart of sales by product" --file sales.xlsx

# Line chart
python scripts/data_visualization.py --query "Draw a line chart of sales trends" --file trends.xlsx

# Pie chart
python scripts/data_visualization.py --query "Draw a pie chart of sales by region" --file sales.xlsx

# Save to specific path
python scripts/data_visualization.py --query "Draw a scatter plot" --file data.xlsx -o /path/to/chart.html
```

---

## 输出描述

### 数据分析与数据解释

返回 Markdown 格式的文本结果，包括分析结论、数据表格等。

### 数据可视化

1. **控制台输出**：ECharts 配置 JSON
2. **HTML 文件**：可以在浏览器中打开以查看图表

---

## 错误处理

常见错误及解决方法：

| 错误信息 | 原因 | 解决方案 |
|---------------|-------|----------|
| `CHARTGEN_API_KEY 未设置` | 环境变量未设置 | `export CHARTGEN_API_KEY="your-key"` |
| **API 请求超时** | 请求超时 | 检查网络连接并重试 |
| **文件未找到** | 文件不存在 | 检查文件路径是否正确 |
| **信用点不足** | 信用点不足 | 充值或联系管理员 |

---

## 技术细节

- **API 基本 URL**：`https://chartgen.ai/api/platform_api/`
- **认证**：请求头 `Authorization: <api-key>`
- **请求格式**：JSON
- **超时时间**：60 秒
- **必需的环境变量**：`CHARTGEN_API_KEY`

有关实现细节，请参阅 `scripts/chartgen_api.py`。

---

## 隐私声明

**发送到远程 API 的数据**：该技能会读取您提供的数据文件（CSV/XLSX/JSON），对其进行 Base64 编码，然后发送到 `https://chartgen.ai/api/platform_api/` 进行分析和图表生成。您的数据将会离开您的设备。

**建议**：
- 不要上传敏感或受监管的数据
- 使用具有有限权限/信用点的专用 API 密钥
- 在使用前请查阅 [chartgen.ai](https://chartgen.ai) 的隐私政策