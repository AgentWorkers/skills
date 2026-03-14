---
name: OctenSearch
description: 由 Octen 提供支持的 LLM（大型语言模型）原生 Web 搜索引擎。平均响应时间小于 80 毫秒，索引更新频率达到分钟级别，能够为 AI 代理提供高度相关且精准的搜索结果。
homepage: https://octen.ai
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["python3"],"env":["OCTEN_API_KEY"]},"primaryEnv":"OCTEN_API_KEY"}, "homepage" : "https://octen.ai", "support" : "support@octen.ai" }
---
# Octen Search

这是一个基于 Octen 的 LLM（大型语言模型）原生 Web 搜索工具，由 Octen 提供的搜索基础设施支持。

## 搜索功能

```bash
python3 {baseDir}/scripts/search.py "here is your query"
python3 {baseDir}/scripts/search.py "here is your query" -n 10
python3 {baseDir}/scripts/search.py "here is your query" --start_time "2026-01-01T00:00:00Z"
python3 {baseDir}/scripts/search.py "here is your query" --end_time "2026-01-31T23:59:59Z"
```

## 选项

- `-n, --count <count>`：可选参数。指定搜索结果的数量（最小值：1，最大值：20；若未提供，则默认为 5）
- `--start_time <time>`：可选参数。用于过滤结果的开始时间（格式为 ISO 8601，例如：“2026-01-01T00:00:00Z”）
- `--end_time <time>`：可选参数。用于过滤结果的结束时间（格式为 ISO 8601，例如：“2026-01-31T23:59:59Z”）。如果同时提供了 `--start_time` 和 `--end_time`，则 `end_time` 必须大于 `start_time`

## 注意事项
- 需要在环境变量中设置 `OCTEN_API_KEY`。您可以从 [https://octen.ai](https://octen.ai) 获取该密钥，然后按照以下方式设置：`export OCTEN_API_KEY=your-api-key`
- 如果您想按发布时间过滤结果，请使用 `--start_time` 和 `--end_time` 参数。例如，要搜索 2026 年 1 月发布的新闻，可以使用 `--start_time "2026-01-01T00:00:00Z" --end_time "2026-01-31T23:59:59Z"`。

## 安全性
- `OCTEN_API_KEY` 环境变量**仅会发送到官方的 Octen API 端点**（`https://api.octen.ai/search`）；
- 任何其他端点或外部服务都不会接收该环境变量；
- API 端点在代码中是**硬编码并列入白名单的**，无法在运行时进行修改；
- 该工具使用标准的 HTTP 请求头认证方式（`X-Api-Key`），这是 API 认证的推荐做法；
- 所有网络请求均通过 HTTPS 进行，以确保 API 密钥的安全传输。