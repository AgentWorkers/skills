---
name: OctenWebSearch
description: 这是一个专为AI代理设计的端到端Web搜索API，能够返回互联网上最相关、实时且高保真的信息。
homepage: https://octen.ai
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["python3"],"env":["OCTEN_API_KEY"]},"primaryEnv":"OCTEN_API_KEY"}}
---
# Octen Web Search

这是一个专为AI代理设计的端到端Web搜索API，能够返回互联网上最相关、实时且高保真的信息。

## 搜索功能

```bash
python3 {baseDir}/scripts/search.py "here is your query"
python3 {baseDir}/scripts/search.py "here is your query" -n 10
python3 {baseDir}/scripts/search.py "here is your query" --start_time "2026-01-01T00:00:00Z"
python3 {baseDir}/scripts/search.py "here is your query" --end_time "2026-01-31T23:59:59Z"
```

## 可选参数

- `-n, --count <count>`：可选。返回的结果数量（最小值：1，最大值：20；如果未提供，则默认为5）
- `--start_time <time>`：可选。用于筛选结果的开始时间（ISO 8601格式，例如："2026-01-01T00:00:00Z"）
- `--end_time <time>`：可选。用于筛选结果的结束时间（ISO 8601格式，例如："2026-01-31T23:59:59Z"）。如果同时提供了`--start_time`和`--end_time`，则`end_time`必须大于`start_time`

## 注意事项
- 需要在环境变量中设置`OCTEN_API_KEY`，该密钥可从[https://octen.ai](https://octen.ai)获取。设置方法如下：`export OCTEN_API_KEY=your-api-key`
- 如果希望根据发布时间筛选结果，请使用`--start_time`和`--end_time`参数。例如，要搜索2026年1月发布的新闻，可以使用`--start_time "2026-01-01T00:00:00Z" --end_time "2026-01-31T23:59:59Z"`。

## 安全性
- `OCTEN_API_KEY`环境变量**仅会被发送到官方的Octen API端点**（`https://api.octen.ai/search`）；
- 任何其他端点或外部服务都不会接收该环境变量；
- API端点在代码中是**硬编码并列入白名单的**，因此无法在运行时进行修改；
- 该技能使用标准的HTTP头部认证方式（`X-Api-Key`），这是API认证的推荐做法；
- 所有的网络请求都通过HTTPS进行，以确保API密钥的安全传输。