---
name: brave-api-search
description: 使用官方的Brave Search API实现实时网页搜索和基于人工智能的答案生成功能。适用于搜索文档、事实、时事新闻或任何网页内容。该功能支持提供带有引用来源的AI生成答案。需要使用BRAVE_SEARCH_API_KEY和BRAVE_ANSWERS_API_KEY进行身份验证。
license: MIT
metadata:
  author: Broedkrummen
  version: 1.0.0
---

# Brave API搜索

通过官方的Brave Search API实现实时网页搜索和基于人工智能的答案生成。提供两种工具：

- `brave_search`：返回包含标题、网址、描述以及可选AI摘要的网页搜索结果。
- `brave_answers`：基于实时网页搜索结果生成的、包含引用来源的AI答案。

## 设置

将您的Brave API密钥设置为环境变量：

```bash
export BRAVE_SEARCH_API_KEY=your_key_here
export BRAVE_ANSWERS_API_KEY=your_key_here
```

您可以在以下链接获取密钥：https://api-dashboard.search.brave.com

如果您的计划同时支持搜索和AI答案功能，这两个密钥可以相同。

## 何时使用这些工具

**使用`brave_search`的情况：**
- 搜索当前信息、新闻或近期事件。
- 查找文档或技术参考资料。
- 需要带有网址的排名结果以便后续处理。
- 希望获取搜索结果的AI摘要。

**使用`brave_answers`的情况：**
- 需要包含引用来源的合成答案。
- 需要对多个来源进行综合研究。
- 希望获得包含引用来源的AI生成答案。
- 需要深度搜索功能（多源查询）。

**不建议使用这些工具的情况：**
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
- `count`——返回的结果数量（1-20个，默认：10个）
- `country`——国家代码（2个字母，默认：`us`）
- `freshness`——日期筛选：`pd`（24小时）、`pw`（7天）、`pm`（31天）、`py`（1年）
- `extra_snippets`——每个结果最多包含5段额外文本摘录（默认：false）
- `summary`——获取Brave AI摘要（默认：false）

**返回值：** 包含标题、网址、描述以及可选AI摘要的结果列表。

### brave_answers

基于实时网页搜索结果生成的AI答案，其中包含引用来源。

```
brave_answers(query="How does React Server Components work?")
brave_answers(query="Compare Postgres vs MySQL for OLAP", enable_research=true)
brave_answers(query="Latest Python release notes", enable_citations=true)
```

**参数：**
- `query`（必填）——要研究的主题或问题
- `enable_citations`——是否包含引用来源（默认：true）
- `enable_research`——是否启用多源搜索深度模式（默认：false）
- `country`——搜索的国家（默认：`us`）

**返回值：** 包含引用来源的AI答案，以及令牌使用情况。

## 使用限制

| 计划类型 | 每秒查询次数（QPS） | 每月限制 |
|------|------------------|----------------------|
| 免费搜索 | 1 | 2,000次 |
| 付费搜索 | 20次 | 每1000次查询收费5美元 |
| 付费答案 | 2次 | 每1000次查询收费4美元 |

## API与网页抓取的区别

此功能使用的是**官方Brave Search API**，而非网页抓取。其优势包括：
- 可靠的、结构化的JSON响应。
- 有明确的速率限制机制和错误提示。
- 可访问AI摘要和AI答案相关的API接口。
- 遵守服务条款。