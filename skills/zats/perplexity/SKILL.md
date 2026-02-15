---
name: perplexity
description: 通过 Perplexity API，利用人工智能技术搜索网页并获取带有引用的答案。支持批量查询功能。
homepage: https://docs.perplexity.ai
metadata: {"clawdbot":{"emoji":"🔮","requires":{"bins":["node"],"env":["PERPLEXITY_API_KEY"]},"primaryEnv":"PERPLEXITY_API_KEY"}}
---

# Perplexity 搜索

这是一个基于人工智能的网页搜索工具，能够提供带有引用依据的准确答案。

## 搜索

- 单个查询：
  ```bash
node {baseDir}/scripts/search.mjs "what's happening in AI today"
```

- 多个查询（批量）：
  ```bash
node {baseDir}/scripts/search.mjs "What is Perplexity?" "Latest AI news" "Best coffee in NYC"
```

## 选项

- `--json`：输出原始的 JSON 响应

## 注意事项

- 需要设置 `PERPLEXITY_API_KEY` 环境变量
- 当可用时，搜索结果会包含引用信息
- 批量查询会通过一次 API 调用进行处理