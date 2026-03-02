---
name: bailian-web-search
description: 通过 Bailian（Alibaba ModelStdio）API 实现的 AI 优化网页搜索功能。该功能可为大型语言模型（LLMs）提供多源、简洁的网页搜索结果。
homepage: https://bailian.console.aliyun.com/cn-beijing?tab=app#/mcp-market/detail/WebSearch
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["bash","curl","jq"],"env":["DASHSCOPE_API_KEY"]},"primaryEnv":"DASHSCOPE_API_KEY"}}
---
# Bailian Web Search

这是一个基于Bailian WebSearch(Enable_search) API的、经过AI优化的网络搜索服务。专为AI代理设计，能够返回清晰、相关的内容。

## 搜索功能

```bash
{baseDir}/scripts/mcp-websearch.sh "query"
{baseDir}/scripts/mcp-websearch.sh  "query"  10
```

## 可用选项

- `<count>`：搜索结果的数量（默认值：5，最大值：20）
- `<query>`：用户输入的搜索关键词