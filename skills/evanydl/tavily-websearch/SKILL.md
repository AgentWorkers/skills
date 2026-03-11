---
name: search
description: "使用 Tavily 的 LLM 优化搜索 API 在网络上进行搜索。该 API 会返回包含内容片段、评分和元数据的相关结果。当您需要查找任何主题的网络内容而无需编写代码时，可以使用它。"
---
# 搜索技能

该脚本可在线搜索并获取针对大型语言模型（LLM）使用而优化的相关结果。

## 认证

该脚本通过 Tavily MCP 服务器使用 OAuth 进行认证。**无需手动设置**——首次运行时，它会：
1. 检查 `~/.mcp-auth/` 文件夹中是否存在有效的令牌。
2. 如果未找到令牌，会自动打开浏览器进行 OAuth 认证。

> **注意：** 您必须拥有一个有效的 Tavily 账户。此 OAuth 流程仅支持登录，不支持账户创建。如果您还没有账户，请先访问 [tavily.com](https://tavily.com) 注册。

### 替代方案：API 密钥

如果您更喜欢使用 API 密钥，可以在 [https://tavily.com](https://tavily.com) 获取一个密钥，并将其添加到 `~/.claude/settings.json` 文件中：
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
./scripts/search.sh '{"query": "AI news", "time_range": "week", "max_results": 10}'

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
    "include_domains": ["arxiv.org", "github.com"]
  }'
```

## API 参考

### 端点

```
POST https://api.tavily.com/search
```

### 请求头

| 请求头 | 值         |
|--------|------------|
| `Authorization` | `Bearer <TAVILY_API_KEY>` |
| `Content-Type` | `application/json` |

### 请求体

| 字段    | 类型       | 默认值    | 描述         |
|---------|-----------|------------|
| `query`    | string     | 必填      | 搜索查询（长度不超过 400 个字符） |
| `max_results` | integer   | 10        | 最大返回结果数量（0-20） |
| `search_depth` | string     | `"basic"`     | 搜索深度（`ultra-fast`, `fast`, `basic`, `advanced`） |
| `topic`    | string     | `"general"`     | 搜索主题（仅限通用主题） |
| `time_range` | string     | null       | 时间范围（`day`, `week`, `month`, `year`） |
| `start_date` | string     | null       | 返回日期（格式：`YYYY-MM-DD`） |
| `end_date` | string     | null       | 开始日期（格式：`YYYY-MM-DD`） |
| `include_domains` | array     | []        | 包含的域名（最多 300 个） |
| `exclude_domains` | array     | []        | 排除的域名（最多 150 个） |
| `country`    | string     | null       | 仅从指定国家获取结果（仅限通用主题） |
| `include_raw_content` | boolean   | false       | 是否包含页面原始内容 |
| `include_images` | boolean   | false       | 是否包含图片结果 |
| `include_image_descriptions` | boolean   | false       | 是否包含图片描述 |
| `include_favicon` | boolean   | false       | 是否包含每个结果的图标链接 |

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

| 搜索深度 | 响应延迟 | 相关性 | 内容类型       |
|---------|-----------|------------|--------------|
| `ultra-fast` | 最低       | 最低       | NLP 摘要       |
| `fast`    | 较低       | 较高       | 分段式内容     |
| `basic`    | 中等       | 较高       | NLP 摘要       |
| `advanced` | 最高       | 最高       | 分段式内容     |

**使用建议：**
- `ultra-fast`：适用于实时聊天、自动完成输入等场景。
- `fast`：需要分段式结果但响应延迟要求较低。
- `basic`：通用搜索，性能平衡。
- `advanced`：追求高搜索精度（默认推荐）。

## 示例

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

### 包含完整内容的搜索

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

## 提示：
- **请确保搜索查询长度不超过 400 个字符**。
- **将复杂的查询拆分为多个子查询**，这样通常能获得更好的搜索结果。
- **使用 `include_domains` 仅搜索来自可信来源的内容**。
- **使用 `time_range` 限定搜索时间范围**。
- **通过 `score`（0-1）筛选相关性最高的搜索结果**。