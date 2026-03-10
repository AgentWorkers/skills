---
name: crawl
description: "**功能说明：**  
可以爬取任意网站，并将网页内容保存为本地 Markdown 文件。适用于需要下载文档、知识库或网页内容以供离线访问或分析的场景。无需编写任何代码——只需提供目标网站的 URL 即可。"
---
# Crawl Skill

该工具用于爬取网站内容，可以从多个页面中提取信息。非常适合用于文档生成、知识库构建以及整个网站的内容提取。

## 认证

该脚本通过 Tavily MCP 服务器使用 OAuth 进行认证。**无需手动配置**——首次运行时，它会：
1. 检查 `~/.mcp-auth/` 目录中是否存在有效的 OAuth 令牌；
2. 如果没有找到令牌，会自动在浏览器中启动 OAuth 认证流程。

> **注意：** 必须拥有 Tavily 账户。此认证流程仅支持登录，不支持账户创建。如果还没有账户，请先访问 [tavily.com](https://tavily.com) 注册。

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
./scripts/crawl.sh '<json>' [output_dir]
```

**示例：**
```bash
# Basic crawl
./scripts/crawl.sh '{"url": "https://docs.example.com"}'

# Deeper crawl with limits
./scripts/crawl.sh '{"url": "https://docs.example.com", "max_depth": 2, "limit": 50}'

# Save to files
./scripts/crawl.sh '{"url": "https://docs.example.com", "max_depth": 2}' ./docs

# Focused crawl with path filters
./scripts/crawl.sh '{"url": "https://example.com", "max_depth": 2, "select_paths": ["/docs/.*", "/api/.*"], "exclude_paths": ["/blog/.*"]}'

# With semantic instructions (for agentic use)
./scripts/crawl.sh '{"url": "https://docs.example.com", "instructions": "Find API documentation", "chunks_per_source": 3}'
```

当提供了 `output_dir` 参数时，每个爬取到的页面都会被保存为独立的 Markdown 文件。

### 基本爬取

```bash
curl --request POST \
  --url https://api.tavily.com/crawl \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "url": "https://docs.example.com",
    "max_depth": 1,
    "limit": 20
  }'
```

### 带有指令的定向爬取

```bash
curl --request POST \
  --url https://api.tavily.com/crawl \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "url": "https://docs.example.com",
    "max_depth": 2,
    "instructions": "Find API documentation and code examples",
    "chunks_per_source": 3,
    "select_paths": ["/docs/.*", "/api/.*"]
  }'
```

## API 参考

### 端点

```
POST https://api.tavily.com/crawl
```

### 请求头

| 头部字段 | 值         |
|---------|-------------|
| `Authorization` | `Bearer <TAVILY_API_KEY>` |
| `Content-Type` | `application/json` |

### 请求体

| 字段        | 类型        | 默认值     | 说明                |
|------------|------------|-----------|-------------------|
| `url`       | string      | Required    | 要开始爬取的根 URL          |
| `max_depth`    | integer     | 1         | 爬取的深度（1-5层）         |
| `max_breadth`    | integer     | 20         | 每页显示的链接数量         |
| `limit`      | integer     | 50         | 总页面数量上限           |
| `instructions` | string      | null       | 爬取时的定向指令（自然语言）       |
| `chunks_per_source` | integer     | 3         | 每页显示的片段数量（1-5个，需设置指令） |
| `extract_depth` | string      | `"basic"`     | 爬取深度模式（`basic` 或 `advanced`） |
| `format`      | string      | `"markdown"`     | 输出格式（`markdown` 或 `text`）     |
| `select_paths` | array      | null       | 需要包含的 URL 正则表达式     |
| `exclude_paths` | array      | null       | 需要排除的 URL 正则表达式     |
| `allow_external` | boolean     | true       | 是否允许包含外部链接         |
| `timeout`     | float       | 150        | 最大等待时间（10-150 秒）       |

### 响应格式

```json
{
  "base_url": "https://docs.example.com",
  "results": [
    {
      "url": "https://docs.example.com/page",
      "raw_content": "# Page Title\n\nContent..."
    }
  ],
  "response_time": 12.5
}
```

## 爬取深度与性能

| 爬取深度 | 典型页面数量 | 所需时间       |
|---------|------------|------------------|
| 1        | 10-50       | 几秒钟             |
| 2        | 50-500       | 几分钟             |
| 3        | 500-5000       | 需要几分钟           |

建议从 `max_depth=1` 开始，根据实际需求逐步增加深度。

## 爬取目的：获取上下文信息 vs 收集数据

- **用于生成上下文信息（将结果输入到大型语言模型中）**：务必同时使用 `instructions` 和 `chunks_per_source` 参数。这样可以仅返回相关内容片段，避免信息量过大导致上下文混乱。
- **用于数据收集（将内容保存到文件中）**：省略 `chunks_per_source` 参数以获取完整页面内容。

## 示例

### 用于生成上下文信息（推荐）

当需要将爬取结果输入到大型语言模型（LLM）中时，请使用此方式：
```bash
curl --request POST \
  --url https://api.tavily.com/crawl \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "url": "https://docs.example.com",
    "max_depth": 2,
    "instructions": "Find API documentation and authentication guides",
    "chunks_per_source": 3
  }'
```

这种方式仅返回每页最相关的信息片段（每个片段最多 500 个字符），有助于保持上下文的清晰度。

### 用于生成特定类型的内容（如技术文档）：

```bash
curl --request POST \
  --url https://api.tavily.com/crawl \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "url": "https://example.com",
    "max_depth": 2,
    "instructions": "Find all documentation about authentication and security",
    "chunks_per_source": 3,
    "select_paths": ["/docs/.*", "/api/.*"]
  }'
```

### 用于数据收集（保存完整页面内容）

当需要将内容保存到文件中以供后续处理时，请使用此方式：
```bash
curl --request POST \
  --url https://api.tavily.com/crawl \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "url": "https://example.com/blog",
    "max_depth": 2,
    "max_breadth": 50,
    "select_paths": ["/blog/.*"],
    "exclude_paths": ["/blog/tag/.*", "/blog/category/.*"]
  }'
```

这种方式会返回完整页面内容。使用 `output_dir` 参数可以将结果保存为 Markdown 文件。

## 获取网站结构（Map API）

当只需要获取 URL 而不需要内容时，可以使用 `map` API：
```bash
curl --request POST \
  --url https://api.tavily.com/map \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "url": "https://docs.example.com",
    "max_depth": 2,
    "instructions": "Find all API docs and guides"
  }'
```

这种方式仅返回 URL，速度更快：
```json
{
  "base_url": "https://docs.example.com",
  "results": [
    "https://docs.example.com/api/auth",
    "https://docs.example.com/guides/quickstart"
  ]
}
```

## 提示：

- **在自动化处理中始终使用 `chunks_per_source` 参数**：这可以防止将大量信息一次性输入到大型语言模型中导致上下文混乱。
- **仅在数据收集时省略 `chunks_per_source` 参数**：此时需要保存完整页面内容。
- **初始设置应保守一些（例如 `max_depth=1`、`limit=20`），然后根据需要逐步增加参数值。
- **使用路径模式`` 来定位感兴趣的部分**。
- **在进行全面爬取之前，先使用 `map` API 了解网站结构**。
- **务必设置 `limit` 参数**，以防止爬取过程失控。