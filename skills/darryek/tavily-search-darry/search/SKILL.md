---
name: search
description: "使用 Tavily 的 LLM 优化搜索 API 在网络上进行搜索。该 API 会返回包含内容片段、评分和元数据的相关结果。当您需要查找任何主题的网页内容而无需编写代码时，可以使用它。"
---
# 搜索技能

该脚本可在线搜索相关信息，并优化搜索结果以适应大型语言模型（LLM）的使用需求。

## 认证

该脚本通过 Tavily MCP 服务器使用 OAuth 进行认证。**无需手动配置**——首次运行时，它会：
1. 检查 `~/.mcp-auth/` 文件是否存在有效的令牌；
2. 如果未找到令牌，会自动打开浏览器进行 OAuth 认证。

> **注意：** 您必须拥有一个有效的 Tavily 账户。此认证流程仅支持登录，不支持账户创建。如果您还没有账户，请先访问 [tavily.com](https://tavily.com) 注册。

### 替代方案：API 密钥

如果您更喜欢使用 API 密钥，可以在 [https://tavily.com](https://tavily.com) 获取密钥，并将其添加到 `~/.claude/settings.json` 文件中：
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
# 基本搜索
./scripts/search.sh '{"query": "python async patterns"}'

# 带参数的搜索
./scripts/search.sh '{"query": "React hooks tutorial", "max_results": 10}'

# 带过滤条件的高级搜索
./scripts/search.sh '{"query": "AI news", "time_range": "week", "max_results": 10}'
```

### 基本搜索示例（使用 curl 命令）

```bash
curl --request POST \
  --url https://api.tavily.com/search \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "query": "latest developments in quantum computing",
    "max_results": 5
  }
```

### 高级搜索示例（使用 curl 命令）

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
  }
```

## API 参考

### 端点

```json
POST https://api.tavily.com/search
```

### 请求头

| 头部字段 | 值 |
|---------|-------|
| `Authorization` | `Bearer <TAVILY_API_KEY>` |
| `Content-Type` | `application/json` |
```

### 请求体

| 字段 | 类型 | 默认值 | 说明 |
|---------|------|---------|-------------|
| `query` | string | 必填 | 搜索查询（长度不超过 400 个字符） |
| `max_results` | integer | 10 | 最大返回结果数量（0-20） |
| `search_depth` | string | `"basic"` | `ultra-fast`, `fast`, `basic`, `advanced` | 搜索深度 |
| `topic` | string | `"general"` | 仅搜索通用主题 |
| `time_range` | string | null | `day`, `week`, `month`, `year` | 时间范围 |
| `start_date` | string | null | 从指定日期之后的结果（格式：YYYY-MM-DD） |
| `end_date` | string | null | 从指定日期之前的结果（格式：YYYY-MM-DD） |
| `include_domains` | array | [] | 包含的域名（最多 300 个） |
| `exclude_domains` | array | [] | 排除的域名（最多 150 个） |
| `country` | string | null | 仅针对特定国家优化搜索结果（仅适用于通用主题） |
| `include_raw_content` | boolean | false | 是否包含页面原始内容 |
| `include_images` | boolean | false | 是否包含图片结果 |
| `include_image_descriptions` | boolean | false | 是否包含图片的描述 |
| `include_favicon` | boolean | false | 是否包含每个结果的图标链接 |

## 响应格式

```json
{
  "query": "latest developments in quantum computing",
  "results": [
    {
      "title": "页面标题",
      "url": "https://example.com/page",
      "content": "提取的文本片段...",
      "score": 0.85
    }
  ],
  "response_time": 1.2
}
```

## 搜索深度

| 深度 | 响应延迟 | 相关性 | 内容类型 |
|---------|---------|-----------|--------------|
| `ultra-fast` | 最低 | 最低 | NLP 摘要 |
| `fast` | 较低 | 较好 | 部分内容 |
| `basic` | 中等 | 较高 | NLP 摘要 |
| `advanced` | 最高 | 最高 | 完整内容 |

**使用建议：**
- `ultra-fast`：适用于实时聊天、自动完成等场景 |
- `fast`：需要部分内容但延迟要求较低 |
- `basic`：通用搜索，平衡性能和准确性 |
- `advanced`：需要高精度搜索结果（默认推荐）

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
  }
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
  }
```

## 提示：
- **搜索查询长度应控制在 400 个字符以内**。
- **将复杂查询拆分为多个子查询**，通常能获得更好的搜索结果。
- **使用 `include_domains` 限定搜索范围，仅获取来自可信来源的信息**。
- **使用 `time_range` 限定搜索时间范围**，以获取最新信息。
- **根据 `score`（0-1）筛选结果，获取相关性最高的搜索结果。