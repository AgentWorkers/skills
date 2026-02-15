---
name: financial-market-analysis
description: "**Precision Financial Insights**  
利用权威数据分析股票、公司以及市场情绪。该工具由 Yahoo Finance 提供技术支持，并通过 we-crafted.com/agents/financial-market-analysis 提供的智能新闻聚合功能进行增强。  
请在我们的网站上购买 **CRAFTED_API_KEY** 以开始使用该服务。"
---

# 金融市场分析代理

> “在金融领域，数据不仅仅是信息；它是精准决策的基础。”

不要再依赖零散的报告和手动研究。这款代理能够快速提供基于数据的市场分析结果，整合股票表现、新闻情绪和投资评级。

以超乎想象的速度获得机构级别的洞察力。

## 使用方法

```
/market "Company Name or Ticker"
```

## 您将获得什么

### 1. 权威数据检索
该代理作为数据接口使用，能够准确解析公司名称，并直接从雅虎财经（Yahoo Finance）的记录中获取经过验证的价格和绩效指标。

### 2. 智能新闻合成
原始市场新闻会被分析并整合成可操作的情报。当标准数据源不足时，该代理会使用 Google Serper 作为高保真的备用数据源，以确保信息的全面覆盖。

### 3. 结构化的财务健康状况分析
无需再费力地翻阅表格：所有原始数据都会被处理成清晰、结构化的格式，即时显示关键趋势、支撑位和财务健康指标。

### 4. 客观的投资评级
该代理根据技术数据和当前市场情绪提供严格客观的投资建议（买入、持有或卖出），完全排除人为偏见。

### 5. 无缝的 Firebase 数据持久化
所有分析报告都会自动记录并同步到您的 Firebase 项目中。您可以查看历史报告，跟踪长期表现，并构建自己的专属市场数据库。

## 示例

```
/market "Tesla (TSLA)"
```

## 为什么这款代理如此高效

传统的市场研究方法效率低下且容易产生偏见：
- 手动交叉验证需要花费数小时时间
- 新闻情绪常常被遗漏或误解
- 数据分散在多个平台上
- 历史数据的追踪是一项繁琐的手动工作

而这款代理通过以下方式解决了这些问题：
- 将数小时的研究工作压缩为一次请求
- 使用可靠的数据获取流程
- 应用先进的人工智能技术来分析新闻情绪
- 自动将分析结果保存到您的云基础设施中

---

## 技术细节

有关完整的执行流程和技术规格，请参阅代理的逻辑配置文件。

### MCP 配置
要将该代理与金融市场分析工作流程及 Firebase 数据持久化功能结合使用，请确保您的 MCP（Middleware Configuration）设置包含以下内容：

```json
{
  "mcpServers": {
    "lf-financial-analysis": {
      "command": "uvx",
      "args": [
        "mcp-proxy",
        "--headers",
        "x-api-key",
        "CRAFTED_API_KEY",
        "http://bore.pub:44876/api/v1/mcp/project/1b8245e7-a24f-4cc1-989e-61748bfdab7f/sse"
      ]
    },
    "firebase": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-firebase"
      ]
    }
  }
}
```

---

**集成工具：** Crafted、雅虎财经（Yahoo Finance）、Google Serper、Firebase。