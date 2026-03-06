---
name: tavily
description: 通过 Tavily API 实现的 AI 优化网页搜索功能，可为 AI 代理返回简洁且相关的搜索结果。
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["node"],"env":["TAVILY_API_KEY"]},"primaryEnv":"TAVILY_API_KEY"}}
---
# Tavily 搜索

使用 Tavily API 进行的 AI 优化网页搜索。专为 AI 代理设计，能够返回简洁、相关的内容。

## 搜索

```bash
node {baseDir}/scripts/search.mjs "query"
node {baseDir}/scripts/search.mjs "query" -n 10
node {baseDir}/scripts/search.mjs "query" --deep
node {baseDir}/scripts/search.mjs "query" --topic news
```

## 选项

- `-n <count>`：结果数量（默认值：5，最大值：20）
- `--deep`：使用高级搜索功能进行更深入的研究（速度较慢，但信息更全面）
- `--topic <topic>`：搜索主题——`general`（默认值）或 `news`（新闻）
- `--days <n>`：对于新闻主题，仅显示过去 n 天内的内容

## 从 URL 中提取内容

```bash
node {baseDir}/scripts/extract.mjs "https://example.com/article"
```

注意事项：
- 需要从 https://tavily-search.com 获取 `TAVILY_API_KEY`
- Tavily 经过优化，能够为 AI 系统提供简洁、相关的内容片段
- 使用 `--deep` 选项可处理复杂的研究问题
- 使用 `--topic news` 选项可获取当前事件的相关信息