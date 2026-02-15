---
name: tavily
description: 通过 Tavily API 实现的 AI 优化网页搜索功能：为 AI 代理返回简洁、相关的搜索结果。
homepage: https://tavily.com
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["node"],"env":["TAVILY_API_KEY"]},"primaryEnv":"TAVILY_API_KEY"}}
---

# Tavily 搜索

这是一个使用 Tavily API 优化的 AI 搜索工具，专为 AI 代理设计，能够返回简洁、相关的内容。

## 搜索

```bash
node {baseDir}/scripts/search.mjs "query"
node {baseDir}/scripts/search.mjs "query" -n 10
node {baseDir}/scripts/search.mjs "query" --deep
node {baseDir}/scripts/search.mjs "query" --topic news
```

## 选项

- `-n <count>`：返回的结果数量（默认值：5，最大值：20）
- `--deep`：使用高级搜索功能进行更深入的搜索（速度较慢，但信息更全面）
- `--topic <topic>`：搜索主题（默认值为 `general` 或 `news`）
- `--days <n>`：针对新闻主题，仅搜索过去 n 天内的内容

## 从 URL 中提取内容

```bash
node {baseDir}/scripts/extract.mjs "https://example.com/article"
```

注意事项：
- 需要从 https://tavily.com 获取 `TAVILY_API_KEY`。
- Tavily 已针对 AI 系统进行了优化，能够返回简洁、相关的信息片段。
- 对于复杂的研究问题，可以使用 `--deep` 选项。
- 若需搜索当前事件，请使用 `--topic news` 选项。