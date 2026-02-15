---
name: querit-search
description: >-
  Web search via Querit.ai API. Use when you need to search the web for
  documentation, current events, facts, or any web content. Returns
  structured results with titles, URLs, and snippets.
metadata: {"openclaw":{"emoji":"🔎","requires":{"env":["QUERIT_API_KEY"]},"primaryEnv":"QUERIT_API_KEY","install":[{"id":"node","kind":"node","label":"Install npm dependencies"}]}}
---

# Querit 搜索

通过 Querit.ai API 进行网页搜索和内容提取，无需使用浏览器。

## 设置

所需环境变量：`QUERIT_API_KEY` — 可在 https://querit.ai 获取免费密钥（每月 1,000 次查询）。

## 搜索

```bash
node {baseDir}/search.js "query"                          # 5 results (default)
node {baseDir}/search.js "query" -n 10                    # more results (max 100)
node {baseDir}/search.js "query" --lang english            # language filter
node {baseDir}/search.js "query" --country "united states" # country filter
node {baseDir}/search.js "query" --date w1                 # past week (d1/w1/m1/y1)
node {baseDir}/search.js "query" --site-include github.com # only this domain
node {baseDir}/search.js "query" --site-exclude reddit.com # exclude domain
node {baseDir}/search.js "query" --content                 # also extract page content
node {baseDir}/search.js "query" --json                    # raw JSON output
```

可以组合使用不同的搜索标志（flags）：

```bash
node {baseDir}/search.js "react hooks" -n 3 --lang english --site-include reactjs.org --content
```

## 提取页面内容

```bash
node {baseDir}/content.js https://example.com/article
```

该功能用于获取指定 URL 的主要内容，并将其以 Markdown 格式提取出来。

## 输出格式

### 搜索结果（默认格式）

```
1. Page Title
   https://example.com/page
   Site: example.com
   Age: 3 days ago
   Description snippet from search results

2. Another Page
   ...
```

### 使用 `--content` 选项

在搜索结果列表之后，每个页面的提取内容会以 Markdown 格式显示：

```
### 1. Page Title
URL: https://example.com/page

# Extracted heading
Extracted body content in markdown...

---
```

### 使用 `--json` 选项

输出结果以原始 JSON 数组的形式，包含以下字段：`url`、`title`、`snippet`、`page_age`、`page_time`。

## 使用场景

- 搜索文档、API 参考资料或教程
- 查找事实、时事新闻或最新信息
- 从特定网站中提取内容（使用 `--site-include` 选项）
- 获取并阅读网页内容（使用 `--content` 或 `content.js` 选项）
- 任何不需要交互式浏览的网页搜索任务

## 限制

- 每次查询的字符数限制为 72 个（超出限制时会自动截断并显示警告）
- 每次查询最多返回 100 个结果
- 每个网站过滤条件最多支持 20 个域名
- 免费 tier：每月 1,000 次查询，QPS（每秒请求数）为 1
- 支持的语言：英语、日语、韩语、德语、法语、西班牙语、葡萄牙语