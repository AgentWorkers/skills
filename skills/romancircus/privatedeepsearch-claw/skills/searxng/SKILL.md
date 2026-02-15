---
name: searxng
description: 通过本地的 SearXNG 实例实现以隐私保护为首要目标的网页搜索功能。无需使用 Google，可利用 DuckDuckGo、Brave、Qwant、Startpage 等替代搜索引擎进行元搜索。适用于任何网页搜索查询。
homepage: http://localhost:8888
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["curl","jq"]}}}
---

# SearXNG - 私人网络搜索引擎

本地 SearXNG 实例运行在 `http://localhost:8888`，禁用了 Google 和 Bing 的搜索服务。

## 搜索（JSON API）

基本搜索：
```bash
curl -s "http://localhost:8888/search?q=YOUR_QUERY&format=json" | jq -r '.results[:5] | .[] | "[\(.title)](\(.url))\n\(.content)\n"'
```

设置搜索结果数量限制：
```bash
curl -s "http://localhost:8888/search?q=YOUR_QUERY&format=json" | jq -r '.results[:10] | .[] | {title, url, content}'
```

仅获取网址：
```bash
curl -s "http://localhost:8888/search?q=YOUR_QUERY&format=json" | jq -r '.results[:5] | .[].url'
```

## 分类

搜索特定分类：
```bash
# Images
curl -s "http://localhost:8888/search?q=YOUR_QUERY&categories=images&format=json" | jq '.results[:5]'

# Videos
curl -s "http://localhost:8888/search?q=YOUR_QUERY&categories=videos&format=json" | jq '.results[:5]'

# News
curl -s "http://localhost:8888/search?q=YOUR_QUERY&categories=news&format=json" | jq '.results[:5]'

# IT/Tech
curl -s "http://localhost:8888/search?q=YOUR_QUERY&categories=it&format=json" | jq '.results[:5]'

# Science
curl -s "http://localhost:8888/search?q=YOUR_QUERY&categories=science&format=json" | jq '.results[:5]'
```

## 时间筛选

显示最新结果：
```bash
# Last day
curl -s "http://localhost:8888/search?q=YOUR_QUERY&time_range=day&format=json" | jq '.results[:5]'

# Last week
curl -s "http://localhost:8888/search?q=YOUR_QUERY&time_range=week&format=json" | jq '.results[:5]'

# Last month
curl -s "http://localhost:8888/search?q=YOUR_QUERY&time_range=month&format=json" | jq '.results[:5]'

# Last year
curl -s "http://localhost:8888/search?q=YOUR_QUERY&time_range=year&format=json" | jq '.results[:5]'
```

## 语言/地区设置

```bash
# English results
curl -s "http://localhost:8888/search?q=YOUR_QUERY&language=en&format=json" | jq '.results[:5]'

# Specific region (US)
curl -s "http://localhost:8888/search?q=YOUR_QUERY&language=en-US&format=json" | jq '.results[:5]'
```

## 启用的搜索引擎

仅支持尊重用户隐私的搜索引擎（不包含 Google 和 Bing）：
- DuckDuckGo（权重 1.5）
- Brave Search（权重 1.5）
- Startpage（权重 1.2）
- Mojeek（权重 1.0）
- Qwant（权重 1.0）
- Wikipedia（权重 1.5）
- GitHub
- StackOverflow
- Reddit
- arXiv
- Piped/Invidious（YouTube 隐私浏览器）

## 使用技巧

- 对包含空格的查询字符串进行 URL 编码：`q=hello%20world` 或 `q=hello+world`
- 合并多个筛选条件：`categories=news&time_range=week`
- 对于复杂的查询，建议使用网页界面：http://localhost:8888

## 示例用法

- 查找最新的 AI 相关新闻：
```bash
curl -s "http://localhost:8888/search?q=artificial+intelligence+news&categories=news&time_range=week&format=json" | jq -r '.results[:5] | .[] | "## \(.title)\n\(.url)\n\(.content)\n"'
```

- 搜索 GitHub 仓库：
```bash
curl -s "http://localhost:8888/search?q=python+web+scraper&categories=repos&format=json" | jq '.results[:5]'
```