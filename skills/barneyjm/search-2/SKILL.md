---
name: search
description: "使用 Tavily 的 LLM 优化搜索 API 在网络上进行搜索。该 API 会返回包含内容片段、评分和元数据的相关结果。当您需要查找任何主题的网页内容而无需编写代码时，可以使用该服务。"
---

# 搜索技能

该功能可在线搜索网页，并返回针对大型语言模型（LLM）使用而优化的相关结果。

## 先决条件

**需要 Tavily API 密钥** - 请在 [https://tavily.com](https://tavily.com) 获取您的密钥。

将密钥添加到 `~/.claude/settings.json` 文件中：
```json
{
  "env": {
    "TAVILY_API_KEY": "tvly-your-api-key-here"
  }
}
```

## 快速入门

### 使用脚本

```bash
./scripts/search.sh '<json>'
```

**示例：**
```bash
# Basic search
./scripts/search.sh '{"query": "python async patterns"}'

# With options
./scripts/search.sh '{"query": "React hooks tutorial", "max_results": 10}'

# Advanced search with filters
./scripts/search.sh '{"query": "AI news", "topic": "news", "time_range": "week", "max_results": 10}'

# Domain-filtered search
./scripts/search.sh '{"query": "machine learning", "include_domains": ["arxiv.org", "github.com"], "search_depth": "advanced"}'
```

### 基本搜索

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

### 高级搜索

```bash
curl --request POST \
  --url https://api.tavily.com/search \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "query": "machine learning best practices",
    "max_results": 10,
    "search_depth": "advanced",
    "include_domains": ["arxiv.org", "github.com"],
    "chunks_per_source": 3
  }'
```

## API 参考

### 端点

```
POST https://api.tavily.com/search
```

### 请求头

| 头部字段 | 值         |
|---------|------------|
| `Authorization` | `Bearer <TAVILY_API_KEY>` |
| `Content-Type` | `application/json` |

### 请求体

| 字段        | 类型          | 默认值       | 说明                |
|------------|--------------|-------------|-------------------|
| `query`     | string        | 必填        | 搜索查询（长度不超过 400 个字符）     |
| `max_results` | integer       | 5           | 最大返回结果数量（0-20）       |
| `search_depth` | string        | `"basic"`       | `ultra-fast`, `fast`, `basic`, `advanced` |
| `topic`     | string        | `"general"`       | `general`, `news`, `finance`     |
| `chunks_per_source` | integer       | 3           | 每个来源返回的片段数量（仅限高级/快速搜索） |
| `time_range` | string        | null          | `day`, `week`, `month`, `year`     |
| `include_domains` | array        | []          | 要包含的域名（最多 300 个）       |
| `exclude_domains` | array        | []          | 要排除的域名（最多 150 个）       |
| `include_answer` | boolean       | false         | 是否包含 AI 生成的结果     |
| `include_raw_content` | boolean       | false         | 是否包含完整页面内容         |
| `include_images` | boolean       | false         | 是否包含图片结果         |

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

| 深度       | 响应延迟      | 相关性      | 内容类型            |
|------------|-------------|-------------|-------------------|
| `ultra-fast`  | 最低          | 最低          | NLP 摘要             |
| `fast`     | 较低          | 较高          | 分段式结果           |
| `basic`     | 中等          | 较高          | NLP 摘要             |
| `advanced`  | 最高          | 最高          | 分段式结果           |

**使用建议：**
- `ultra-fast`：适用于实时聊天、自动完成等场景。
- `fast`：需要分段式结果，但对响应延迟有要求。
- `basic`：通用搜索方式，性能与准确性平衡。
- `advanced`：注重搜索结果的精确性（推荐使用）。

## 示例

### 新闻搜索

```bash
curl --request POST \
  --url https://api.tavily.com/search \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "query": "AI news today",
    "topic": "news",
    "time_range": "day",
    "max_results": 10
  }'
```

### 域名过滤搜索

```bash
curl --request POST \
  --url https://api.tavily.com/search \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "query": "Python async best practices",
    "include_domains": ["docs.python.org", "realpython.com", "github.com"],
    "search_depth": "advanced"
  }'
```

### 带有完整内容的搜索

```bash
curl --request POST \
  --url https://api.tavily.com/search \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "query": "React hooks tutorial",
    "max_results": 3,
    "include_raw_content": true
  }'
```

### 金融领域搜索

```bash
curl --request POST \
  --url https://api.tavily.com/search \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "query": "AAPL earnings Q4 2024",
    "topic": "finance",
    "max_results": 10
  }'
```

## 提示：
- **查询长度不超过 400 个字符**：请注意输入的是搜索内容，而非提示语。
- **将复杂查询拆分为多个子查询**：这样通常能获得更好的搜索结果。
- **使用 `include_domains` 限定搜索范围**：仅获取来自可信来源的信息。
- **使用 `time_range` 筛选最新内容**。
- **根据 `score`（0-1）筛选结果**：分数越高，相关性越高。