---
name: perplexity
description: 通过 Perplexity API，利用人工智能技术搜索网页并获取带有引用的详细答案。支持批量查询功能。
homepage: https://openrouter.ai/
metadata: {"clawdbot":{"emoji":"🔮","requires":{"bins":["node"],"env":["OPENROUTER_API_KEY"]},"primaryEnv":"OPENROUTER_API_KEY"}}
---
# Perplexity Search

这是一个基于人工智能的网页搜索工具，能够提供带有引用信息的准确答案。

## 搜索方式

- 单个查询：
    ```bash
node {baseDir}/scripts/search.mjs "what's happening in AI today"
```

- 多个查询（批量）：
    ```bash
node {baseDir}/scripts/search.mjs "What is Perplexity?" "Latest AI news" "Best coffee in NYC"
```

## 选项

- `--json`：以原始 JSON 格式输出搜索结果

## 注意事项

- 需要设置 `OPENROUTER_API_KEY` 环境变量
- 搜索结果中会包含可用的引用信息
- 批量查询会在一次 API 调用中完成处理