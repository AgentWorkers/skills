---
name: exa-web-search-free
description: 通过 Exa MCP 进行免费的人工智能搜索：可以在线搜索新闻/信息，通过代码搜索从 GitHub/StackOverflow 获取文档/示例，还可以对公司进行调研以获取商业情报。无需使用 API 密钥。
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["mcporter"]}}}
---

# Exa Web Search（免费）

提供针对网页、代码及公司信息的神经网络搜索功能，无需API密钥。

## 设置

请确认`mcporter`已正确配置：
```bash
mcporter list exa
```

如果未列出配置选项，请执行以下操作：
```bash
mcporter config add exa https://mcp.exa.ai/mcp
```

## 核心工具

### web_search_exa
用于搜索网页上的最新信息、新闻或相关数据。

**参数：**
- `query` - 搜索查询
- `numResults`（可选，默认值：8）
- `type`（可选） - `"auto"`、`"fast"` 或 `"deep"`

### get_code_context_exa
从GitHub和Stack Overflow中查找代码示例和文档。

**参数：**
- `query` - 代码或API的搜索查询
- `tokensNum`（可选，默认值：5000） - 搜索范围：1000-50000个结果

### company_research_exa
用于查询公司的业务信息和新闻。

**参数：**
- `companyName` - 公司名称
- `numResults`（可选，默认值：5）

## 高级工具（可选）

通过更新配置URL，可启用以下额外工具：
- `web_search_advanced_exa` - 域名/日期筛选功能
- `deep_search_exa` - 查询扩展功能
- `crawling_exa` - 全文提取功能
- `people_search_exa` - 专业人士资料查询
- `deep_researcher_start/check` - 人工智能研究辅助工具

**启用所有工具：**
```bash
mcporter config add exa-full "https://mcp.exa.ai/mcp?tools=web_search_exa,web_search_advanced_exa,get_code_context_exa,deep_search_exa,crawling_exa,company_research_exa,people_search_exa,deep_researcher_start,deep_researcher_check"

# Then use:
mcporter call 'exa-full.deep_search_exa(query: "AI safety research")'
```

## 使用提示：

- 网页搜索：使用`type: "fast"`可快速查找信息，使用`type: "deep"`可进行深入研究
- 代码搜索：设置`tokensNum`为1000-2000可获取更精确的结果，设置为5000+可获取更全面的信息
- 详情请参阅[examples.md](references/examples.md)中的使用示例

## 资源

- [GitHub](https://github.com/exa-labs/exa-mcp-server)
- [npm](https://www.npmjs.com/package/exa-mcp-server)
- [文档](https://exa.ai/docs)