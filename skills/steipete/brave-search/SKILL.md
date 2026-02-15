---
name: brave-search
description: 通过 Brave Search API 进行网页搜索和内容提取。可用于搜索文档、事实或任何网页内容。该工具非常轻量级，无需浏览器即可使用。
---

# Brave Search

Brave Search是一款无需浏览器即可进行无头网页搜索和内容提取的工具。

## 设置

首次使用前请运行以下命令：

```bash
cd ~/Projects/agent-scripts/skills/brave-search
npm ci
```

该工具需要以下环境变量：`BRAVE_API_KEY`。

## 搜索

```bash
./search.js "query"                    # Basic search (5 results)
./search.js "query" -n 10              # More results
./search.js "query" --content          # Include page content as markdown
./search.js "query" -n 3 --content     # Combined
```

## 提取页面内容

```bash
./content.js https://example.com/article
```

该工具可以获取指定URL的内容，并将其以Markdown格式提取出来。

## 输出格式

```
--- Result 1 ---
Title: Page Title
Link: https://example.com/page
Snippet: Description from search results
Content: (if --content flag used)
  Markdown content extracted from the page...

--- Result 2 ---
...
```

## 使用场景

- 搜索文档或API参考资料
- 查找事实或最新信息
- 从特定URL获取内容
- 任何不需要交互式浏览的网页搜索任务