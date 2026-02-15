---
name: aisa-tavily
description: 通过 AIsa 的 Tavily API 代理实现的人工智能优化网页搜索功能。该功能通过 AIsa 的统一 API 网关为人工智能代理返回简洁、相关的内容结果。
homepage: https://aisa.one
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["node"],"env":["AISA_API_KEY"]},"primaryEnv":"AISA_API_KEY"}}
---

# AIsa Tavily 搜索

通过 AIsa 的统一网关，利用 Tavily API 进行优化的人工智能（AI）搜索。专为 AI 代理设计，可返回简洁、相关的内容。

## 搜索

```bash
node {baseDir}/scripts/search.mjs "query"
node {baseDir}/scripts/search.mjs "query" -n 10
node {baseDir}/scripts/search.mjs "query" --deep
node {baseDir}/scripts/search.mjs "query" --topic news
```

## 选项

- `-n <数量>`：返回的结果数量（默认值：5，最大值：20）
- `--deep`：使用高级搜索功能以进行更深入的查询（速度较慢，但信息更全面）
- `--topic <主题>`：搜索主题——`general`（默认）或 `news`（新闻）
- `--days <天数>`：对于新闻主题，仅显示过去 n 天内的内容

## 从 URL 中提取内容

```bash
node {baseDir}/scripts/extract.mjs "https://example.com/article"
```

注意事项：
- 需要从 https://marketplace.aisa.one 获取 `AISA_API_KEY`
- 由 AIsa 的统一 API 网关（https://aisa.one）提供支持
- 使用 `--deep` 选项可进行复杂查询
- 使用 `--topic news` 可搜索当前事件