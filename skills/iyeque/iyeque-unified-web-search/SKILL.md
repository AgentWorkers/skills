---
name: unified-web-search
description: 选择最适合的查询来源（Tavily、Web Search Plus、浏览器或本地文件），执行搜索，并返回带有来源信息的排名结果。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["node"], "env": ["TAVILY_API_KEY"] },
        "version": "1.1.0",
      },
  }
---
# 统一网络搜索技能

该技能能够智能地选择最佳的搜索源，汇总搜索结果，并以包含来源信息的形式返回排序后的答案。

## 安全性

所有搜索查询都会经过验证和清理：
- 最大查询长度：500个字符
- 禁用Shell元字符以防止命令注入
- 本地文件搜索仅限于工作区目录内

## 工具API

### unified_web_search
在多个来源中执行统一搜索。

- **参数：**
  - `query`（字符串，必填）：搜索查询（仅支持字母数字、空格和基本标点符号）
  - `sources`（字符串数组，可选）：要搜索的来源列表。默认值为`['tavily', 'web-search-plus', 'local']`。可选值：`tavily`、`web-search-plus`、`browser`、`local`。
  - `max_results`（整数，可选）：返回的最大结果数量。默认值为5。

**使用方法：**

```bash
# Search all sources
node skills/unified-web-search/index.js --query "my search term" --max_results 10

# Search specific sources
node skills/unified-web-search/index.js --query "AI developments" --sources '["tavily", "local"]' --max_results 10

# Search local files only
node skills/unified-web-search/index.js --query "meeting notes" --sources '["local"]'
```

## 实现方式

该技能从多个来源汇总搜索结果：
- **Tavily**：基于人工智能的优化网络搜索服务，具有相关性评分功能（需要`TAVILY_API_KEY`）
- **Web Search Plus**：更广泛的网络搜索覆盖范围（未来会集成该功能）
- **Browser**：针对特定网站的爬取（未来会集成该功能）
- **Local Files**：在工作区目录中搜索匹配的文件名

搜索结果会根据相关性进行评分和排序，然后以JSON格式返回，并附带来源信息。

## 输出格式

```json
[
  {
    "source": "tavily",
    "title": "Article Title",
    "url": "https://example.com/article",
    "score": 0.95,
    "content": "Brief excerpt from the article..."
  },
  {
    "source": "local",
    "title": "/path/to/file.txt",
    "snippet": "Found query in filename: file.txt",
    "score": 0.5
  }
]
```

## 环境变量

- `TAVILY_API_KEY`：使用Tavily搜索功能所必需的密钥。请在https://app.tavily.com获取您的密钥

## 错误处理

- 如果查询缺失或为空，则返回错误信息
- 如果查询包含不允许的字符，则返回错误信息
- 能够优雅地处理API故障（继续使用其他来源进行搜索）
- 如果未设置`TAVILY_API_KEY`，则会发出警告

## 示例

```bash
$ node skills/unified-web-search/index.js --query "climate change" --max_results 3
[
  {
    "source": "tavily",
    "title": "IPCC Climate Report 2024",
    "url": "https://ipcc.ch/report",
    "score": 0.92,
    "content": "The latest IPCC report shows..."
  },
  {
    "source": "tavily",
    "title": "Climate Action Tracker",
    "url": "https://climateactiontracker.org",
    "score": 0.87,
    "content": "Tracking government climate commitments..."
  },
  {
    "source": "local",
    "title": "/home/user/.openclaw/workspace/memory/climate-notes.md",
    "snippet": "Found query in filename: climate-notes.md",
    "score": 0.5
  }
]
```