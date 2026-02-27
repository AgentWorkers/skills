---
name: brave-api-search
description: 实时网络搜索、自动建议功能以及基于人工智能的答案生成，均通过官方的Brave Search API实现。可用于搜索文档、事实、时事新闻或任何网页内容。该功能支持提供带有引用依据的AI生成答案，并具备查询词自动建议功能。使用该服务需要BRAVE_SEARCH_API_KEY和BRAVE_ANSWERS_API_KEY这两个API密钥。
license: MIT
metadata:
  author: Broedkrummen
  version: 3.0.0
---
# Brave API搜索

通过Brave官方搜索API实现实时网页搜索、自动建议以及基于AI的答案功能。提供以下三个工具：

- `brave_search`：返回包含标题、URL、描述以及可选AI摘要的网页搜索结果。
- `brave_suggest`：在用户输入查询时提供自动建议功能，支持丰富的元数据。
- `brave_answers`：基于实时网页搜索结果生成的AI答案，其中包含内联引用。

## 设置

建议将Brave API密钥配置在本地`.env`文件中：

```bash
# .env (do not commit)
BRAVE_SEARCH_API_KEY=your_key_here
BRAVE_ANSWERS_API_KEY=your_key_here
```

如果需要，也可以在shell会话中导出这些密钥。

您可以在以下链接获取API密钥：https://api-dashboard.search.brave.com

如果您的计划同时支持搜索和AI答案功能，这两个密钥可以相同。

> 注意：`brave_search`和`brave_suggest`使用`BRAVE_SEARCH_API_KEY`；`brave_answers`需要`BRAVE_ANSWERS_API_KEY`。

> 请注意：此技能必须使用`BRAVE_SEARCH_API_KEY`和`BRAVE_ANSWERS_API_KEY`，不能使用通用的`BRAVE_API_KEY`作为替代。

## 适用场景

**使用`brave_search`的场景：**
- 搜索当前信息、新闻或近期事件。
- 查找文档或技术参考资料。
- 需要带有URL的排名结果以便后续处理。
- 希望获取搜索结果的AI摘要。

**使用`brave_suggest`的场景：**
- 为搜索界面提供自动完成功能。
- 帮助用户更快地构建更准确的查询。
- 在用户输入时提供查询建议。
- 希望建议中包含丰富的元数据（如标题、描述、图片）。

**使用`brave_answers`的场景：**
- 需要包含引用来源的合成答案。
- 需要对多个来源进行深入研究。
- 希望获得基于AI的答案，并且答案中包含内联引用。
- 需要深度搜索功能（多源查询）。

**不适用的场景：**
- 问题可以通过上下文或记忆直接回答的情况。
- 不需要外部信息来完成的任务。

## 工具

### brave_search

提供包含标题、URL和描述的排名网页搜索结果。

```
brave_search(query="latest Node.js release", count=5)
brave_search(query="TypeScript generics", extra_snippets=true)
brave_search(query="current weather Copenhagen", freshness="pd")
brave_search(query="React Server Components", summary=true)
```

**参数：**
- `query`（必填）：搜索查询，支持以下操作符：`site:`、`"exact phrase"`、`-exclude`。
- `count`：返回的结果数量（1-20个，默认值：10个）。
- `country`：2位字母的国家代码（默认值：`us`）。
- `freshness`：日期过滤选项：`pd`（24小时）、`pw`（7天）、`pm`（31天）、`py`（1年）。
- `extra_snippets`：每个结果是否包含最多5段额外文本摘录（默认值：`false`）。
- `summary`：是否获取Brave AI摘要（默认值：`false`）。

**返回值：** 包含标题、URL、描述以及可选AI摘要的结果列表。

### brave_suggest

在用户输入查询时提供智能的自动建议功能。

```
brave_suggest(query="hello")
brave_suggest(query="pyt", count=5, country="US")
brave_suggest(query="einstein", rich=true)
```

**参数：**
- `query`（必填）：用于生成建议的查询部分内容。
- `count`：建议的数量（1-10个，默认值：5个）。
- `country`：2位字母的国家代码（默认值：`US`）。
- `rich`：是否包含丰富的元数据（如标题、描述、图片）（默认值：`false`，需付费计划）。

**最佳实践：**
- 实现防抖机制（150-300毫秒），以避免用户在输入时频繁调用API。
- 异步加载建议内容，以免阻塞用户界面。

### brave_answers

基于实时网页搜索生成的AI答案，其中包含内联引用。

```
brave_answers(query="How does React Server Components work?")
brave_answers(query="Compare Postgres vs MySQL for OLAP", enable_research=true)
brave_answers(query="Latest Python release notes", enable_citations=true)
```

**参数：**
- `query`（必填）：要研究的主题或问题。
- `enable_citations`：是否包含内联引用来源（默认值：`true`）。
- `enable_research`：是否启用多源深度搜索模式（默认值：`false`）。
- `country`：搜索的目标国家（默认值：`us`）。

**返回值：** 包含从搜索结果中提取的引用来源的AI答案，以及相关令牌使用情况。

## 价格与限制

Brave的服务费用基于信用额度，可能会有所变动。请不要假设请求次数是固定的。

当前公开的信息（在生产使用前请在Brave控制台/文档中核实）：
- 可能提供每月试用信用额度（例如：每月5美元的信用额度）。
- 搜索和答案功能消耗的信用额度不同。
- 丰富的建议功能需要付费的自动建议计划。
- 答案生成可能会产生基于令牌的费用。
- QPS（每秒请求数）限制取决于您的订阅计划。

请随时在以下链接查看您的使用限制和消耗情况：
- https://api-dashboard.search.brave.com
- https://brave.com/search/api/

## 安全性与打包说明

- 该技能仅调用`https://api.search.brave.com/res/v1`下的Brave官方API端点。
- 它需要两个环境变量：`BRAVE_SEARCH_API_KEY`和`BRAVE_ANSWERS_API_KEY`（请将它们保存在`.env`文件中，不要直接写在命令或聊天中）。
- 该技能不会请求持久性系统权限，也不会修改系统配置。
- 该技能基于源代码实现（包含三个本地Node脚本），无需外部安装或下载。

## API与网页抓取的区别

该技能使用的是**Brave官方搜索API**，而非网页抓取。其优势包括：
- 可靠的、结构化的JSON响应。
- 支持速率限制和适当的错误信息。
- 可访问AI摘要、AI答案和自动建议功能。
- 遵守服务条款。