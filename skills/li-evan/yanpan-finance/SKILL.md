---
name: "a-share-multidim-quant-analysis"
description: "A-Share多维度量化分析MCP服务器：提供券商研究报告、人工智能新闻分析以及股票综合分析服务"
version: "1.3.0"
category: "finance"
tags: ["finance", "stock", "quantitative-analysis", "research-report", "news-analysis", "mcp", "A-share", "China"]
complexity: "beginner"
author: "Li-Evan"
---
# A-Share多维度量化分析

该服务由MCP服务器提供，专为AI代理设计，用于进行A股（中国股票市场）的多维度量化分析。功能包括券商研究报告的查询、AI新闻情感分析以及全面的股票分析。无需任何部署，可直接使用。

## 工具

### `search_research_reports`
- 按公司名称搜索券商研究报告。
- 返回的报告包含标题、来源、内容和日期等详细信息。
- **输入参数**：`company_name`（例如：“比亚迪”），`limit`（默认值：10）
- **覆盖范围**：超过5,000份研究报告，持续更新

### `search_news_analysis`
- 按公司名称和日期范围搜索经过AI分析的新闻。
- 返回原始新闻内容、AI分析结果、情感分析、投资建议及重要性评分。
- **输入参数**：`company_name`，`start_date`（可选），`end_date`（可选），`limit`（默认值：10）
- **覆盖范围**：超过19,000条针对个股和行业的分析新闻

### `get_stock_analysis`
- 根据股票代码获取该股票的最新综合分析报告。
- 报告内容包括技术分析、基本面分析、新闻情感分析、投资建议、风险管理及最终交易决策。
- **输入参数**：`stock_code`（例如：“601900”、“000001”、“300750”）
- **覆盖范围**：超过3,000只股票，超过12,000份分析报告

## 设置

只需将以下代码添加到您的`.mcp.json`文件中：

```json
{
  "mcpServers": {
    "yanpan": {
      "type": "http",
      "url": "http://42.121.167.42:9800/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_API_KEY>"
      }
    }
  }
}
```

无需安装任何软件、使用Docker或维护数据库——只需连接即可使用该服务。

## 获取API密钥

如需获取自己的API密钥，请通过微信联系我们：**ptcg12345**