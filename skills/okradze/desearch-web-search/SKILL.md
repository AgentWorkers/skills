---
name: desearch-web-search
description: 在网页上搜索，并获取实时显示的、类似搜索引擎结果页（SERP）的搜索结果，包括标题、网址和内容摘要。你可以使用这个功能来进行一般的网页查询，以获取来自互联网上的最新链接和相关信息。
metadata: {"clawdbot":{"emoji":"🌐","homepage":"https://desearch.ai","requires":{"env":["DESEARCH_API_KEY"]}}}
---
# Web Search by Desearch

提供实时网络搜索服务，返回结构化的高质量搜索结果（SERP格式），包括标题、链接和内容摘要。

## 设置

1. 从 [https://console.desearch.ai](https://console.desearch.ai) 获取 API 密钥。
2. 设置环境变量：`export DESEARCH_API_KEY='your-key-here'`

## 使用方法

```bash
# Basic web search
scripts/desearch.py web "latest news on AI"

# Paginated results
scripts/desearch.py web "quantum computing" --start 10
```

## 选项

| 选项 | 说明 |
|--------|-------------|
| `--start` | 分页偏移量（默认值：0）。用于获取下一页的结果。 |

## 示例

### 搜索当前事件
```bash
scripts/desearch.py web "latest AI regulations 2025"
```

### 浏览分页结果
```bash
scripts/desearch.py web "best python libraries" --start 0
scripts/desearch.py web "best python libraries" --start 10
```