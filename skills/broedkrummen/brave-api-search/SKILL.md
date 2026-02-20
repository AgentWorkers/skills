---
name: brave-api-search
description: 使用官方的Brave Search API实现实时网络搜索和基于人工智能的答案生成功能。适用于搜索文档、事实、时事信息或任何网页内容。该功能支持提供带有引用的、基于人工智能的答案。需要使用BRAVE_SEARCH_API_KEY和BRAVE_ANSWERS_API_KEY进行授权。
license: MIT
metadata:
  author: Broedkrummen
  version: 2.1.1
---
# Brave API搜索

通过官方的Brave Search API实现实时网络搜索和基于人工智能的答案生成。提供两种工具：

- `brave_search`：返回包含标题、URL、描述以及可选AI摘要的网络搜索结果。
- `brave_answers`：基于实时网络搜索生成的AI答案，其中包含内联引用。

## 设置

建议将您的Brave API密钥配置在本地`.env`文件中：

```bash
# .env (do not commit)
BRAVE_SEARCH_API_KEY=your_key_here
BRAVE_ANSWERS_API_KEY=your_key_here
```

如需在shell会话中临时使用这些密钥，可按以下步骤操作：

在[https://api-dashboard.search.brave.com](https://api-dashboard.search.brave.com)获取API密钥。如果您的计划同时支持搜索和AI答案功能，这两个密钥可以相同。

> 注意：此技能必须使用`BRAVE_SEARCH_API_KEY`和`BRAVE_ANSWERS_API_KEY`这两个密钥，不能使用通用的`BRAVE_API_KEY`作为替代。

## 适用场景

- **使用`brave_search`的情况：**
  - 搜索当前信息、新闻或近期事件。
  - 查找文档或技术参考资料。
  - 需要带有可点击URL的排名结果以便进一步查看。
  - 希望获取搜索结果的AI摘要。

- **使用`brave_answers`的情况：**
  - 需要包含引用来源的合成答案。
  - 需要对多个来源进行综合研究。
  - 希望获得带有内联引用的AI生成答案。
  - 需要开启深度搜索模式（多源信息整合）。

- **不适用的情况：**
  - 问题可以通过上下文或记忆直接回答的情况。
  - 不需要外部信息来完成的任务。

## 工具介绍

### brave_search

提供包含标题、URL和描述的排名搜索结果。

**参数：**
- `query`（必填）：搜索查询，支持以下操作符：`site:`、`"exact phrase"`、`-exclude`。
- `count`：返回的结果数量（1-20条，默认值：10条）。
- `country`：国家代码（2个字母，默认值：`us`）。
- `freshness`：日期筛选条件（`pd`：24小时；`pw`：7天；`pm`：31天；`py`：1年）。
- `extra_snippets`：每条结果是否包含最多5段额外文本摘录（默认值：`false`）。
- `summary`：是否获取Brave AI生成的摘要（默认值：`false`）。

**返回值：** 包含标题、URL、描述以及可选AI摘要的结果列表。

### brave_answers

基于实时网络搜索生成的AI答案，其中包含内联引用。

**参数：**
- `query`（必填）：要查询的问题或主题。
- `enable_citations`：是否包含内联引用来源（默认值：`true`）。
- `enable_research`：是否启用深度搜索模式（默认值：`false`）。
- `country`：搜索的目标国家（默认值：`us`）。

**返回值：** 包含从网络搜索结果中提取的引用来源的AI生成答案，以及相关令牌使用情况。

## 定价与限制

Brave的定价基于信用额度，具体价格可能随时调整。请勿假设存在固定的免费请求次数。

当前公开信息（在生产使用前请在Brave控制台文档中确认）：
- 可能提供每月试用信用额度（例如：每月5美元）。
- 搜索和答案功能的信用消耗方式不同。
- 答案生成可能还会产生基于令牌的费用。
- QPS（每秒请求数）限制取决于您的套餐等级。

请随时在以下链接查看您的使用限制和消耗情况：
- [https://api-dashboard.search.brave.com](https://api-dashboard.search.brave.com)
- [https://brave.com/search/api/](https://brave.com/search/api/)

## 安全性与打包说明

- 该技能仅调用`https://api.search.brave.com/res/v1`下的官方Brave API接口。
- 必须设置两个环境变量：`BRAVE_SEARCH_API_KEY`和`BRAVE_ANSWERS_API_KEY`（请将它们保存在`.env`文件中，不要直接写在命令或聊天中）。
- 该技能不会请求持久性系统权限，也不会修改系统配置。
- 该技能基于两个本地Node.js脚本实现，无需外部安装或下载。

## API与网络爬虫的区别

该技能使用的是**官方的Brave Search API**，而非网络爬虫。其优势包括：
- 可靠的、结构化的JSON响应格式。
- 支持速率限制机制和详细的错误信息。
- 可访问AI摘要和AI答案生成功能。
- 遵守服务条款规定。