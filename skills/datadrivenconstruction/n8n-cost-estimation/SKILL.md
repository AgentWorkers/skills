---
slug: "n8n-cost-estimation"
display_name: "N8N Cost Estimation"
description: "构建一个 n8n 管道，用于从 Revit/IFC 文件中自动进行成本估算。该流程将利用 DDC CWICR 数据库和 LLM（大型语言模型）进行分类处理。"
---

# 自动化成本估算流程

## 商业案例

### 问题描述
传统的成本估算流程需要：
- 手动在价格数据库中查找工作项信息
- 耗时的元素分类工作
- 对定价标准的专业知识要求较高
- 需要重复输入数据

### 解决方案
一个免费的开源n8n流程，利用人工智能（LLM）和包含55,000多个工作项的向量数据库，将CAD（Revit 2015-2026）文件转换为完整的成本和时间估算结果。

### 商业价值

| 传统流程 | 自动化流程 |
|-----------------|----------------------|
| BIM经理手动导出数据 | 流程自动对元素进行分类 |
| 初级估算师查询数据库 | 向量搜索可在几毫秒内找到匹配项 |
| 高级估算师绘制组件图 | LLM识别数量参数 |
| 工头计算工时 | DDC CWICR数据库中包含标准规范 |
| 项目经理汇总成本 | 流程输出分阶段的成本明细 |

**处理速度**：每个元素组大约需要3-10秒

## 技术实现

### 流程架构
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Revit/IFC   │───>│ CAD2DATA    │───>│ Structured  │
│ File        │    │ Converter   │    │ Excel/CSV   │
└─────────────┘    └─────────────┘    └─────────────┘
                                             │
                                             ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Cost Report │<───│ Price Match │<───│ LLM Class.  │
│ HTML/Excel  │    │ DDC CWICR   │    │ + QTO       │
└─────────────┘    └─────────────┘    └─────────────┘
```

### n8n流程步骤

#### 1. 文件转换节点
```javascript
// Execute CAD converter
const filePath = $input.first().json.file_path;
const outputDir = filePath.replace(/\.[^.]+$/, '');

const command = `RvtExporter.exe "${filePath}" complete bbox`;

// Returns: { xlsx_path, dae_path }
```

#### 2. 加载元素
```javascript
// Read converted Excel into n8n
const xlsx = $node["Read Binary Files"].json;
const elements = xlsx.sheets["Elements"];

// Group by category for processing
const grouped = elements.reduce((acc, el) => {
  const cat = el.Category;
  if (!acc[cat]) acc[cat] = [];
  acc[cat].push(el);
  return acc;
}, {});

return Object.entries(grouped).map(([category, items]) => ({
  json: {category, items, count: items.length}
}));
```

#### 3. LLM分类
```javascript
// Prompt for Claude/GPT classification
const prompt = `
You are a construction estimator. Given these BIM elements:
Category: ${$input.first().json.category}
Sample elements: ${JSON.stringify($input.first().json.items.slice(0,5))}

1. Identify the construction work type
2. List relevant quantity parameters (Volume, Area, Length, Count)
3. Suggest standard work items from construction norms

Return as JSON:
{
  "work_type": "...",
  "quantity_params": ["Volume", "Area"],
  "suggested_items": ["Concrete foundation", "Formwork"]
}
`;
```

#### 4. 在DDC CWICR中进行向量搜索
```javascript
// Search DDC CWICR database for matching work items
const qdrantClient = require('@qdrant/js-client-rest');

const searchResults = await qdrantClient.search('ddc_cwicr_en', {
  vector: await getEmbedding($input.first().json.work_description),
  limit: 10,
  score_threshold: 0.7
});

return searchResults.map(r => ({
  json: {
    work_code: r.payload.work_item_code,
    description: r.payload.description,
    unit: r.payload.unit,
    unit_price: r.payload.unit_price,
    similarity: r.score
  }
}));
```

#### 5. 计算成本
```javascript
// Match quantities to prices
const elements = $node["Load Elements"].json;
const prices = $node["Vector Search"].json;

let totalCost = 0;
const breakdown = [];

for (const el of elements.items) {
  const matchedPrice = prices.find(p => p.similarity > 0.8);
  if (matchedPrice) {
    const quantity = el.Volume || el.Area || 1;
    const cost = quantity * matchedPrice.unit_price;
    totalCost += cost;

    breakdown.push({
      element: el.Name,
      quantity: quantity,
      unit: matchedPrice.unit,
      unit_price: matchedPrice.unit_price,
      total: cost
    });
  }
}

return [{json: {totalCost, breakdown}}];
```

#### 6. 生成报告
```javascript
// Create HTML report
const data = $input.first().json;

const html = `
<!DOCTYPE html>
<html>
<head>
  <title>Cost Estimate Report</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background-color: #4CAF50; color: white; }
    .total { font-size: 1.5em; font-weight: bold; }
  </style>
</head>
<body>
  <h1>Cost Estimate Report</h1>
  <p class="total">Total: $${data.totalCost.toLocaleString()}</p>
  <table>
    <tr><th>Element</th><th>Quantity</th><th>Unit</th><th>Price</th><th>Total</th></tr>
    ${data.breakdown.map(row => `
      <tr>
        <td>${row.element}</td>
        <td>${row.quantity.toFixed(2)}</td>
        <td>${row.unit}</td>
        <td>$${row.unit_price.toFixed(2)}</td>
        <td>$${row.total.toFixed(2)}</td>
      </tr>
    `).join('')}
  </table>
</body>
</html>
`;

return [{json: {html, filename: 'estimate_report.html'}}];
```

## 实际应用结果
以示例项目（rac_basic_sample.rvt）为例：
- 处理时间：使用ChatGPT约30分钟
- 分析的元素数量：500多个
- 自动分类准确率：95%
- 需要手动审核的情况：5%的边缘案例

## 来自社区的关键观点
> “我的个人看法是：那些忽视工作流程自动化和AI工具的专业人士，在建筑行业超越他们之前，大概还有5年的时间。这些工具是免费且开源的，数据也是公开的。唯一的问题是谁能先学会使用它们。”

## 先决条件
- n8n（本地或托管版本）
- DDC CAD转换工具
- DDC CWICR数据库
- OpenAI/Anthropic API密钥
- Qdrant向量数据库

## 资源
- **GitHub**：cad2data流程仓库
- **数据库**：OpenConstructionEstimate-DDC-CWICR
- **社区**：n8n Workflows for Construction（Telegram频道）