---
name: zhipu-search
description: |
  Zhipu AI Web Search Tool - Provides flexible search engine capabilities.
  
  Use when:
  - Need to search web information for latest data
  - Need specific search engines (Sogou, Quark, Zhipu Search)
  - Need to filter search results by time range or domain
  - Need to control result count and detail level
  
  Supported search engines: search_std (basic), search_pro (advanced), search_pro_sogou (Sogou), search_pro_quark (Quark)
  Supported parameters: search intent recognition, result count, time filter, domain filter, content size control
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["ZHIPU_API_KEY"] },
      },
  }
---

# Zhipu 搜索

通过 Zhipu AI API 进行网页搜索，支持多种搜索引擎和灵活的参数配置。

## 快速入门

### 基本搜索

```python
# Use default parameters
search_query = "OpenClaw latest version"
search_engine = "search_std"
```

### 高级搜索（完整参数）

```python
search_query = "AI development trends"      # Required, max 70 chars
search_engine = "search_pro"                # Required: search_std/search_pro/search_pro_sogou/search_pro_quark
search_intent = true                        # Optional, default false, enable search intent recognition
count = 20                                  # Optional, default 10, range 1-50
search_domain_filter = "example.com"        # Optional, whitelist domain filter
search_recency_filter = "oneWeek"           # Optional: oneDay/oneWeek/oneMonth/oneYear/noLimit
content_size = "high"                       # Optional: medium/high, control content detail level
request_id = "unique-request-id"            # Optional, unique request identifier
user_id = "user-123456"                     # Optional, end user ID (6-128 chars)
```

## 使用方法

### 方法 1：直接调用脚本（推荐）

```bash
python scripts/zhipu_search.py \
  --query "search content" \
  --engine search_pro \
  --count 10
```

### 方法 2：使用 OpenClaw 工具

系统会根据需求自动选择合适的参数。

## API 参数参考

| 参数 | 类型 | 是否必填 | 默认值 | 描述 |
|---------|--------|---------|--------------|-------------------------|
| search_query | string | ✅ | - | 搜索内容，建议长度不超过 70 个字符 |
| search_engine | enum | ✅ | - | 可选值：search_std、search_pro、search_pro_sogou、search_pro_quark |
| search(intent | boolean | - | false | 是否启用搜索意图识别 |
| count | integer | - | 10 | 结果数量（1-50 条） |
| search_domain_filter | string | - | - | 白名单域名过滤 |
| search_recency_filter | enum | - | 可选值：oneDay/oneWeek/oneMonth/oneYear/noLimit | 结果更新频率 |
| content_size | enum | - | - | 可选值：medium/high | 控制内容长度 |
| request_id | string | - | - | 唯一请求标识符 |
| user_id | string | - | - | 用户 ID（6-128 个字符） |

## 搜索引擎选择指南

| 工具 | 适用场景 |
|--------|-------------------|
| search_std | 基本搜索，常规问答 |
| search_pro | 高级搜索，需要更精确的结果 |
| search_pro_sogou | 搜狗搜索，适用于中国国内内容 |
| search_pro_quark | Quark 搜索，适用于特定场景 |

## 响应结构

```json
{
  "id": "task-id",
  "created": 1704067200,
  "request_id": "request-id",
  "search_intent": [
    {
      "query": "original query",
      "intent": "SEARCH_ALL",
      "keywords": "rewritten keywords"
    }
  ],
  "search_result": [
    {
      "title": "title",
      "content": "content summary",
      "link": "result link",
      "media": "site name",
      "icon": "site icon",
      "refer": "reference number",
      "publish_date": "publish date"
    }
  ]
}
```

## 环境要求

- 必须配置环境变量 `ZHIPU_API_KEY` |
- 需要 Python 3.7 或更高版本 |
- 需要 `requests` 库

## 注意事项

1. `search_query` 的长度应控制在 70 个字符以内 |
2. `search_pro_sogou` 的结果数量默认为 10 条；可选值：20、30、40、50 条 |
3. 如果提供了 `user_id`，其长度必须在 6-128 个字符之间 |
4. 启用搜索意图识别会增加响应时间，但能提高结果的相关性