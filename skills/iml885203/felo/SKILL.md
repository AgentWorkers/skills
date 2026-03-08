---
name: felo
description: "通过 Felo API 进行 AI 合成的网络搜索功能：能够将 15 至 40 个来源的信息汇总成结构化的摘要。适用场景包括：  
(1) 需要综合多个来源信息来研究某个主题时；  
(2) 收集 Reddit、GitHub、X（Twitter）等平台上的社区趋势数据时；  
(3) 需要对多个来源进行交叉分析的市场新闻研究时；  
(4) 输入诸如“帮我查一下”、“搜索一下”、“研究一下”、“什么在流行”等指令时。  
**不适用场景**：  
- 单一网站的查询（请使用 `web_fetch` 功能）；  
- 需要精确时间戳的紧急查询（请使用 `web_search` 功能）；  
- 快速的、仅需 1 秒内完成的结果查询。"
---
# Felo AI 搜索

当您需要以下功能时，可以使用 Felo AI 进行全面的人工智能摘要式网络搜索：
- 将多个来源的信息整合为结构化的见解
- 获取带有上下文信息的热门话题（社区趋势分析）
- 需要跨来源综合分析的研究问题

**请勿用于：**
- 需要精确时间戳的时效性查询
- 单一来源的查找（请使用 `web_fetch`）
- 对速度要求极高的场景（Felo 的搜索速度约为 15 秒，而 `web_search` 为约 1 秒）

## 认证

API 密钥的位置：`~/.config/felo/api_key`

```bash
cat ~/.config/felo/api_key
# Returns: fk-Kfcl9cKqX18y3d93qAk06dK3f0dHowiycT6OqcSkMqfQjDal
```

## 基本用法

```bash
curl -s -X POST https://openapi.felo.ai/v2/chat \
  -H "Authorization: Bearer $(cat ~/.config/felo/api_key)" \
  -H "Content-Type: application/json" \
  -d '{"query": "Your search query here (1-2000 chars)"}' | jq .
```

## 响应结构

```json
{
  "status": "ok",
  "data": {
    "answer": "AI-generated summary...",
    "query_analysis": {
      "queries": ["optimized", "search", "terms"]
    },
    "resources": [
      {
        "link": "https://...",
        "title": "Source title",
        "snippet": "Relevant excerpt"
      }
    ]
  }
}
```

**关键字段：**
- `data.answer` — 由 AI 生成的综合答案（用于摘要）
- `data.resources` — 来源链接（通常包含 15-40 个来源）

## 常见用法模式

### 社区趋势分析（定时任务）

```bash
# Query: Broad topic + time constraint + source diversity
curl -s -X POST https://openapi.felo.ai/v2/chat \
  -H "Authorization: Bearer $(cat ~/.config/felo/api_key)" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the top 5 trending topics in the OpenClaw AI agent community this week? Include specific discussions from Reddit, GitHub, X (Twitter), forums, and blogs. Provide source links."
  }' > /tmp/felo_result.json

# Extract structured output
ANSWER=$(jq -r '.data.answer' /tmp/felo_result.json)
SOURCES=$(jq -r '.data.resources[0:10] | .[] | "- [\(.title)](\(.link))"' /tmp/felo_result.json)
SOURCE_COUNT=$(jq '.data.resources | length' /tmp/felo_result.json)
```

### 交互式研究

```bash
# For one-off queries
felo_query() {
  local query="$1"
  curl -s -X POST https://openapi.felo.ai/v2/chat \
    -H "Authorization: Bearer $(cat ~/.config/felo/api_key)" \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"$query\"}" | jq -r '.data.answer'
}

felo_query "Compare memory-lancedb-pro vs mem0 for AI agent long-term memory"
```

## 速率限制

- 默认值：每个 API 密钥每分钟 100 次请求
- 响应头：`X-RateLimit-*`
- 对 429 错误采用指数级退避策略进行处理

## 错误处理

常见错误：
- `INVALID_API_KEY`（401）—— 请检查 `~/.config/felo/api_key`
- `QUERY_TOO_LONG`（400）—— 查询长度超过 2000 个字符
- `RATE_LIMIT_EXCEEDED`（429）—— 请求过多，请稍后再试

## 何时使用 Felo 与 web_search

| 使用场景 | 工具 | 原因 |
|----------|------|--------|
| 分析多个来源的社区趋势 | **Felo** | 采用人工智能合成，覆盖范围更广 |
| 搜索特定网站（例如 `site:reddit.com`） | **web_search** | 可使用精确的网站定位操作符 |
| 需要时间戳的查询（例如“1 天前”） | **web_search** | Felo 不支持时间戳功能 |
- 需要跨来源分析的研究 | **Felo** | 提供人工智能生成的见解 |
- 对速度要求极高的查询 | **web_search** | 搜索速度更快（约 1 秒 vs Felo 的 15 秒）

## 注意事项

- Felo 会返回 15-40 个来源的信息，但不包含时间戳
- 查询中可以包含时间提示（如“本周”、“最近”），但结果不保证经过时间过滤
- Felo 最适合用于**趋势检测**和**主题综合分析**，不适用于**对时间敏感的监控**