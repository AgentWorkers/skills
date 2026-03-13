---
name: search
description: "使用 Tavily 的搜索 API 在网络上进行搜索。该 API 会返回相关且准确的结果，包括内容片段、评分以及元数据。当用户需要搜索网页、查找资料来源、寻找链接或研究某个主题时，可以使用此 API。"
---
# 搜索技能

该功能用于在网络上搜索信息，并返回适合大型语言模型（LLM）使用的相关结果。

## 要求

请将您的 API 密钥设置为环境变量：

```bash
export TAVILY_API_KEY=tvly-...
```

您可以在 [tavily.com](https://tavily.com) 获取 API 密钥。

## 快速入门

该脚本接受一个名为 `--json` 的参数，该参数表示 Tavily API 的原始请求体。这个 JSON 数据与 [Tavily 搜索 API](https://docs.tavily.com/documentation/api-reference/endpoint/search) 的接口完全匹配。

```bash
./scripts/search.sh --json '{"query": "python async patterns"}'
```

**示例：**

```bash
# Quick lookup
./scripts/search.sh --json '{"query": "OpenAI latest funding round"}'

# More results
./scripts/search.sh --json '{"query": "Stripe documentation", "max_results": 10}'

# Recent news only
./scripts/search.sh --json '{"query": "Landscape of electric vehicles 2026", "time_range": "week", "max_results": 10}'

# Scoped to specific sources
./scripts/search.sh --json '{"query": "NVIDIA stock analysis", "search_depth": "advanced"}'
```

### 相等的 curl 命令

该脚本实际上只是对 Tavily API 请求的封装：

```bash
curl --request POST \
  --url https://api.tavily.com/search \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "query": "latest developments in quantum computing",
    "max_results": 5
  }'
```

## API 参考

### 端点

```
POST https://api.tavily.com/search
```

### 请求头

| 请求头 | 值         |
|--------|-------------|
| `Authorization` | `Bearer <TAVILY_API_KEY>` |
| `Content-Type` | `application/json` |

### 请求体

| 字段        | 类型        | 默认值     | 描述                |
|------------|------------|-----------|-------------------|
| `query`     | string       | Required    | 搜索查询（长度不超过 400 个字符）     |
| `max_results` | integer     | 10        | 最大返回结果数量（0-20）       |
| `search_depth` | string       | `"basic"`     | 搜索深度（`basic` 或 `advanced`）    |
| `time_range` | string       | null       | 时间范围（`day`, `week`, `month`, `year`）  |
| `start_date` | string       | null       | 开始日期（格式：`YYYY-MM-DD`）     |
| `end_date` | string       | null       | 结束日期（格式：`YYYY-MM-DD`）     |
| `include_domains` | array       | []        | 包含的域名            |
| `exclude_domains` | array       | []        | 排除的域名            |
| `country`     | string       | null       | 仅返回特定国家的结果（仅适用于通用主题） |
| `include_raw_content` | boolean     | false       | 是否包含页面原始内容         |
| `include_images` | boolean     | false       | 是否包含图片结果           |
| `include_image_descriptions` | boolean     | false       | 是否包含图片描述           |
| `include_favicon` | boolean     | false       | 是否包含每个结果的图标链接         |

### 响应格式

```json
{
  "query": "latest developments in quantum computing",
  "results": [
    {
      "title": "Page Title",
      "url": "https://example.com/page",
      "content": "Extracted text snippet...",
      "score": 0.85
    }
  ],
  "response_time": 1.2
}
```

## 搜索深度

| 搜索深度 | 响应延迟 | 相关性 | 内容类型            |
|---------|-----------|-----------|----------------------|
| `basic`    | 中等       | 高        | NLP 摘要             |
| `advanced` | 较高       | 最高       | 分块显示的结果内容        |

**使用建议：**
- `basic`：通用搜索，适合大多数场景。
- `advanced`：适用于需要高精确度的搜索（推荐使用）。

## 提示：
- **查询长度请控制在 400 个字符以内**：请注意，这里指的是搜索查询的内容，而不是提示语。
- **将复杂的查询拆分为多个子查询**：这样通常能获得更好的搜索结果。
- **使用 `include_domains` 选项来限定搜索范围，仅获取来自可信来源的结果。**
- **通过 `time_range` 限定时间范围，以获取最新的信息。**