---
name: crawl
description: "**功能说明：**  
可以爬取任意网站，并将页面内容保存为本地 Markdown 文件。适用于需要下载文档、知识库或网页内容以供离线访问或分析的场景。无需编写任何代码——只需提供目标网站的 URL 即可。"
---
# Crawl Skill

该工具用于爬取网站内容，可从多个页面中提取信息。非常适合用于文档生成、知识库构建以及整个网站的内容提取任务。

## 认证

该脚本通过 Tavily MCP 服务器使用 OAuth 进行认证。**无需手动配置**——首次运行时，它会：
1. 检查 `~/.mcp-auth/` 目录中是否存在有效的访问令牌；
2. 如果没有找到令牌，会自动打开浏览器进行 OAuth 认证。

> **注意：** 你必须拥有一个 Tavily 账户。此认证流程仅支持登录，不支持账户创建。如果你还没有账户，请先访问 [tavily.com](https://tavily.com) 注册。

### 替代方案：API 密钥

如果你更喜欢使用 API 密钥，可以在 [https://tavily.com](https://tavily.com) 获取密钥，并将其添加到 `~/.claude/settings.json` 文件中：
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
# 基本爬取
./scripts/crawl.sh '{"url": "https://docs.example.com"}'

# 带有深度限制的爬取
./scripts/crawl.sh '{"url": "https://docs.example.com", "max_depth": 2, "limit": 50}''

# 将结果保存到文件
./scripts/crawl.sh '{"url": "https://docs.example.com", "max_depth": 2}' ./docs

# 带路径过滤的爬取
./scripts/crawl.sh '{"url": "https://example.com", "max_depth": 2, "select_paths": ["/docs/.*", "/api/.*"], "exclude_paths": ["/blog/.*"]}

# 带有指令的爬取（适用于自动化场景）
./scripts/crawl.sh '{"url": "https://docs.example.com", "instructions": "查找 API 文档", "chunks_per_source": 3}'
```

当提供 `output_dir` 参数时，每个爬取到的页面都会被保存为单独的 Markdown 文件。

### 基本爬取示例

```bash
curl --request POST \
  --url https://api.tavily.com/crawl \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "url": "https://docs.example.com",
    "max_depth": 1,
    "limit": 20
  }
```

### 带有指令的爬取示例

```bash
curl --request POST \
  --url https://api.tavily.com/crawl \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "url": "https://docs.example.com",
    "max_depth": 2,
    "instructions": "查找 API 文档和代码示例",
    "chunks_per_source": 3,
    "select_paths": ["/docs/.*", "/api/.*"]
  }
```

## API 参考

### API 端点

```bash
POST https://api.tavily.com/crawl
```

### 请求头

| 头部字段 | 值         |
|---------|-------------|
| `Authorization` | `Bearer <TAVILY_API_KEY>` |
| `Content-Type` | `application/json` |

### 请求体

| 字段        | 类型        | 默认值     | 描述                |
|------------|-------------|-----------|-------------------|
| `url`       | string      | 必填        | 要爬取的根 URL            |
| `max_depth`    | integer      | 1          | 爬取的深度（1-5            |
| `max_breadth`    | integer      | 20          | 每页链接数量            |
| `limit`      | integer      | 50          | 总页面数量限制          |
| `instructions` | string      | 可选        | 用于指导爬取的自然语言指令        |
| `chunks_per_source` | integer      | 3          | 每页显示的片段数量（1-5，需指定指令） |
| `extract_depth` | string      | `"basic"` 或 `advanced` | 提取内容的深度模式        |
| `format`      | string      | `"markdown"` 或 `text`     | 输出格式              |
| `select_paths` | array       | 可选        | 需要包含的路径正则表达式      |
| `exclude_paths` | array       | 可选        | 需要排除的路径正则表达式      |
| `allow_external` | boolean     | true        | 是否包含外部链接            |
| `timeout`     | float       | 150          | 最大等待时间（10-150 秒）        |

### 响应格式

```json
{
  "base_url": "https://docs.example.com",
  "results": [
    {
      "url": "https://docs.example.com/page",
      "raw_content": "# 页面标题\n\n内容..."
    }
  ],
  "response_time": 12.5
}
```

## 爬取深度与性能

| 爬取深度 | 常规页面数量 | 所需时间 |
|---------|-------------|-----------|
| 1        | 10-50        | 几秒钟             |
| 2        | 50-500        | 几分钟             |
| 3        | 500-5000        | 需要数分钟            |

**建议从 `max_depth=1` 开始，根据需要逐步增加深度。**

## 爬取目的

- **用于生成上下文**：**务必使用 `instructions` 和 `chunks_per_source` 参数。这样只会返回相关内容片段，避免上下文信息过于庞大。
- **用于数据收集**：**省略 `chunks_per_source` 参数以获取完整页面内容。**

**示例：**

### 用于生成上下文（推荐）**

当将爬取结果输入到大型语言模型（LLM）时：
```bash
curl --request POST \
  --url https://api.tavily.com/crawl \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "url": "https://docs.example.com",
    "max_depth": 2,
    "instructions": "查找 API 文档和认证指南",
    "chunks_per_source": 3
  }
```

此方式仅返回每页最相关的片段（每个片段最多 500 个字符），适合用于生成上下文。

### 用于特定文档的爬取

```bash
curl --request POST \
  --url https://api.tavily.com/crawl \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "url": "https://example.com",
    "max_depth": 2,
    "instructions": "查找所有关于认证和安全的文档",
    "chunks_per_source": 3,
    "select_paths": ["/docs/.*", "/api/.*"]
  }
```

### 用于数据收集

当需要将内容保存到文件时：
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
  }
```

此方式会返回完整页面内容。可以使用 `output_dir` 参数将结果保存为 Markdown 文件。

## API `map`（用于获取 URL）

当你只需要获取 URL 而不需要内容时，可以使用 `map` 接口：
```bash
curl --request POST \
  --url https://api.tavily.com/map \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "url": "https://docs.example.com",
    "max_depth": 2,
    "instructions": "查找所有 API 文档和指南"
  }
```

**注意：** `map` 接口返回的只是 URL 列表（速度更快）。

## 提示：

- **在自动化场景中始终使用 `chunks_per_source`**，以避免将大量数据输入到大型语言模型时导致信息过载。
- **仅在需要保存完整页面内容时省略 `chunks_per_source` 参数**。
- **初始设置时建议使用较低的深度（如 `max_depth=1`、`limit=20`），然后根据需要逐步增加。
- **使用路径模式来定位所需内容**。
- **在进行全面爬取前，先使用 `map` 接口了解网站结构**。
- **务必设置 `limit` 以防止爬取行为失控。