---
name: unified-web-search
description: 选择最适合的查询来源（Tavily、Web Search Plus、浏览器或本地文件），执行搜索，并返回带有来源信息的排名结果。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
      },
  }
---

# 统一网络搜索技能

该技能能够智能地选择最佳的搜索源，汇总搜索结果，并返回带有来源信息的排名结果。

## 工具 API

### unified_web_search
在多个来源中执行统一搜索。

- **参数：**
  - `query` (字符串，必填)：搜索查询。
  - `sources` (字符串数组，可选)：要搜索的来源列表。默认值为 `['tavily', 'web-search-plus', 'local']`。可选值：`tavily`, `web-search-plus`, `browser`, `local`。
  - `max_results` (整数，可选)：返回的最大结果数量。默认值为 `5`。

**使用方法：**

```bash
node skills/unified-web-search/index.js --query "my search term" --sources '["tavily", "local"]' --max_results 10
```

## 实现方式

该技能从多个来源汇总搜索结果：

- **Tavily**：用于查询网络事实和新闻。
- **Web Search Plus**：用于进行广泛的网络搜索。
- **Browser**：用于有针对性地抓取网站内容（如需要）。
- **Local Files**：用于搜索已索引的本地文档。

搜索结果会根据相关性进行评分和排名，然后附带来源信息一并返回。