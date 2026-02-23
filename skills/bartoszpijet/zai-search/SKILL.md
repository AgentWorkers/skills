---
name: z.ai-web-search
description: 通过 Z.AI Web Search API 实现的 AI 优化网络搜索功能。该 API 可返回结构化搜索结果（包括标题、URL 和摘要），以便大型语言模型（LLM）进行处理。
homepage: https://docs.z.ai/guides/tools/web-search
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["node"],"env":["ZAI_API_KEY"]},"primaryEnv":"ZAI_API_KEY"}}
---
# Z.AI 网页搜索

使用 Z.AI 网页搜索 API 的 AI 优化网页搜索功能，专为大型语言模型（LLMs）设计——返回包含标题、URL、摘要、网站名称和图标的结构化搜索结果。

## 搜索

```bash
node {baseDir}/scripts/search.mjs "query"
node {baseDir}/scripts/search.mjs "query" -n 15
node {baseDir}/scripts/search.mjs "query" --domain sohu.com
node {baseDir}/scripts/search.mjs "query" --recency oneWeek
node {baseDir}/scripts/search.mjs "query" --days 7
```

## 选项

- `-n <数量>`：返回的结果数量（默认：10，最大：50）
- `--domain <域名>`：将搜索结果限制在指定域名内（例如：`sohu.com`、`www.example.com`）
- `--recency <过滤条件>`：时间范围——`oneDay`（1天）、`oneWeek`（1周）、`oneMonth`（1个月）、`oneYear`（1年）、`noLimit`（无限制）（默认值）
- `--days <n>`：时间范围的简写形式（1→1天，7→1周，30→1个月，365→1年）

## 从 URL 中提取内容

```bash
node {baseDir}/scripts/extract.mjs "https://example.com/article"
```

注意：Z.AI 并不提供专门的提取内容 API。此脚本使用原生的 `fetch` 函数获取网页内容，并去除 HTML 标签以提取基本文本。如需更丰富的内容，请使用搜索结果（其中已包含摘要）。

## 设置

- 在 [Z.AI 平台](https://chat.z.ai) 获取 API 密钥
- 将 `ZAI_API_KEY` 设置到您的环境变量中
- 文档：[网页搜索指南](https://docs.z.ai/guides/tools/web-search)