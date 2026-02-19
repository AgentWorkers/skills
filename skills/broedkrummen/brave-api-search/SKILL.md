---
name: brave-api-search
description: 使用官方的Brave Search API实现实时网络搜索和基于人工智能的答案生成功能。该功能可用于搜索文档、事实、时事新闻或任何网页内容，并能提供带有引用依据的智能回答。需要使用BRAVE_SEARCH_API_KEY和BRAVE_ANSWERS_API_KEY这两个API密钥。
license: MIT
metadata:
  author: Broedkrummen
  version: 2.0.0
---
# Brave API搜索

通过官方的Brave Search API实现实时网页搜索和基于人工智能的答案生成。提供两种工具：

- `brave_search`：返回包含标题、网址、描述以及可选AI摘要的网页搜索结果。
- `brave_answers`：基于实时网页搜索生成的AI答案，其中包含引用来源的文本。

## 设置

将您的Brave API密钥设置为环境变量：

```bash
export BRAVE_SEARCH_API_KEY=your_key_here
export BRAVE_ANSWERS_API_KEY=your_key_here
```

您可以在以下链接获取密钥：https://api-dashboard.search.brave.com

如果您的计划同时支持搜索和AI答案功能，这两个密钥可以相同。

> 注意：此技能明确要求使用`BRAVE_SEARCH_API_KEY`和`BRAVE_ANSWERS_API_KEY`，不能使用通用的`BRAVE_API_KEY`作为替代。

## 何时使用这些工具

**使用`brave_search`的情况：**
- 搜索当前信息、新闻或近期事件。
- 查找文档或技术参考资料。
- 需要带有可点击网址的排名结果以便进一步查看。
- 希望获得搜索结果的AI摘要。

**使用`brave_answers`的情况：**
- 需要包含引用来源的合成答案。
- 需要对多个来源进行综合研究。
- 希望获得带有内联引用的AI生成答案。
- 需要深度搜索功能（多源查询）。

**不适合使用此技能的情况：**
- 问题可以通过上下文或记忆直接回答的情况。
- 不需要外部信息来完成的任务。

## 工具

### brave_search

提供包含标题、网址和描述的排名网页搜索结果。

```
brave_search(query="latest Node.js release", count=5)
brave_search(query="TypeScript generics", extra_snippets=true)
brave_search(query="current weather Copenhagen", freshness="pd")
brave_search(query="React Server Components", summary=true)
```

**参数：**
- `query`（必填）——搜索查询，支持以下操作符：`site:`、`"exact phrase"`、`-exclude`
- `count`——返回的结果数量（1-20个，默认值：10）
- `country`——国家代码（2个字母，默认值：`us`）
- `freshness`——日期过滤：`pd`（24小时）、`pw`（7天）、`pm`（31天）、`py`（1年）
- `extra_snippets`——每个结果最多包含5段额外文本摘录（默认值：false）
- `summary`——获取Brave AI摘要（默认值：false）

**返回值：**包含标题、网址、描述以及可选AI摘要的结果列表。

### brave_answers

基于实时网页搜索生成的AI答案，其中包含引用来源的文本。

```
brave_answers(query="How does React Server Components work?")
brave_answers(query="Compare Postgres vs MySQL for OLAP", enable_research=true)
brave_answers(query="Latest Python release notes", enable_citations=true)
```

**参数：**
- `query`（必填）——要研究的问题或主题。
- `enable_citations`——是否包含内联引用来源（默认值：true）
- `enable_research`——是否启用多源搜索深度搜索模式（默认值：false）
- `country`——搜索的目标国家（默认值：`us`）

**返回值：**包含从搜索结果中提取的引用来源的AI答案，以及相关令牌使用情况。

## 速率限制

| 计划类型 | 每秒查询次数（QPS） | 每月查询次数 |
|------|------------------|----------------------|
| 免费搜索 | 1 | 2,000次 |
| 付费搜索 | 20次 | 每1,000次查询收费5美元 |
| 付费答案 | 2次 | 每1,000次查询收费4美元 |

## API与网络爬虫的区别

此技能使用的是**官方的Brave Search API**，而非网络爬虫。其优势包括：
- 可靠的、结构化的JSON响应。
- 有明确的速率限制提示和适当的错误信息。
- 可访问AI摘要和AI答案相关接口。
- 符合服务条款规定。