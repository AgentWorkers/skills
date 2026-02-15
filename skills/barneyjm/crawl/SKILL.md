---
name: crawl
description: "**功能描述：**  
可以爬取任意网站，并将网页内容保存为本地 Markdown 文件。适用于需要下载文档、知识库或网页内容以供离线访问或分析的场景。无需编写任何代码——只需提供网站的 URL 即可。"
---

# Crawl Skill

该技能用于爬取网站内容，可以从多个页面中提取信息。非常适合用于文档生成、知识库构建以及整个网站的数据提取。

## 先决条件

**需要 Tavily API 密钥** - 请在 [https://tavily.com](https://tavily.com) 获取您的 API 密钥。

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

当提供了 `output_dir` 时，每个爬取到的页面都会被保存为单独的 Markdown 文件。

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
|---------|------------|
| `Authorization` | `Bearer <TAVILY_API_KEY>` |
| `Content-Type` | `application/json` |

### 请求体

| 字段        | 类型         | 默认值       | 说明         |
|------------|-------------|-------------|
| `url`       | string       | 必填        | 开始爬取的根 URL     |
| `max_depth`    | integer      | 1           | 爬取的深度（1-5层）   |
| `max_breadth`    | integer      | 20           | 每页链接数量     |
| `limit`      | integer      | 总页面数量上限   |
| `instructions` | string       | 可选        | 爬取方向的自然语言指令 |
| `chunks_per_source` | integer      | 3           | 每页的数据块数量   |
| `extract_depth` | string       | `"basic"`      | 爬取深度模式（basic/advanced） |
| `format`     | string       | `"markdown"`      | 输出格式（markdown/text） |
| `select_paths` | array       | 可选        | 需要包含的路径正则表达式 |
| `exclude_paths` | array       | 可选        | 需要排除的路径正则表达式 |
| `allow_external` | boolean      | true         | 是否允许包含外部链接   |
| `timeout`     | float        | 150          | 最大等待时间（10-150 秒） |

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

| 爬取深度 | 典型页面数量 | 所需时间     |
|---------|-------------|-------------|
| 1        | 10-50        | 几秒钟       |
| 2        | 50-500        | 几分钟       |
| 3        | 500-5000       | 需要很多分钟     |

**建议从 `max_depth=1` 开始，根据需要逐步增加深度。**

## 爬取目的：获取上下文信息 vs 收集数据

**用于生成上下文（将结果输入到大型语言模型中）：** 必须使用 `instructions` 和 `chunks_per_source` 参数。这样只会返回相关的数据块，而不会返回整个页面，从而避免上下文信息过载。

**用于数据收集（保存到文件中）：** 可以省略 `chunks_per_source` 参数以获取完整页面内容。

## 示例

### 用于生成上下文：代理式研究（推荐）

当将爬取结果输入到大型语言模型（LLM）中时使用此方法：

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

每次页面只返回最相关的部分内容（每段最多 500 个字符），适合用于生成上下文而不会造成信息过载。

### 用于生成上下文：针对性技术文档

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

### 用于数据收集：完整页面存档

当需要将内容保存到文件中以供后续处理时使用此方法：

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

返回完整页面内容，可以使用 `output_dir` 参数将结果保存为 Markdown 文件。

## Map API（URL 发现）

如果您只需要获取 URL 而不需要内容，可以使用 `map` 而不是 `crawl`：

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

**注意：** `map` 方法比 `crawl` 方法更快，因为它只返回 URL。

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

- **在代理式工作流程中始终使用 `chunks_per_source` 参数**，以避免将大量数据输入到大型语言模型中导致信息过载。
- **仅在数据收集时省略 `chunks_per_source` 参数**，以保存完整页面内容。
- **开始时设置较低的深度和页面数量（例如 `max_depth=1`，`limit=20`），然后根据需要逐步增加。
- **使用路径模式`select_paths` 和 `exclude_paths` 来定位所需或排除不需要的内容。**
- **在进行全面爬取之前，先使用 `map` 方法了解网站结构。**
- **始终设置 `limit` 参数**，以防止爬取行为失控。