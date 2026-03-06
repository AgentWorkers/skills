---
name: extract
description: "使用 Tavily 的提取 API 从特定 URL 中提取内容。该 API 可从网页中获取干净的 Markdown 或纯文本格式的数据。当你拥有具体的 URL 并且需要获取其内容（而无需编写代码）时，可以使用此方法。"
---
# 技能提取工具

该工具可以从指定的 URL 中提取干净的内容，非常适合已知需要提取内容的页面情况。

## 认证

该脚本通过 Tavily MCP 服务器使用 OAuth 进行认证。**无需手动设置**——首次运行时，它会：
1. 检查 `~/.mcp-auth/` 目录中是否存在有效的令牌；
2. 如果没有找到令牌，会自动打开浏览器进行 OAuth 认证。

> **注意：** 必须拥有 Tavily 账户。此认证流程仅支持登录，不支持账户创建。如果没有账户，请先访问 [tavily.com](https://tavily.com) 注册。

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
./scripts/extract.sh '<json>'
```

**示例：**
```bash
# 单个 URL
./scripts/extract.sh '{"urls": ["https://example.com/article"]}'
```

# 多个 URL
```bash
./scripts/extract.sh '{"urls": ["https://example.com/page1", "https://example.com/page2"]}'
```

# 带有查询条件和数据分块的提取
```bash
./scripts/extract.sh '{"urls": ["https://example.com/docs"], "query": "authentication API", "chunks_per_source": 3}'
```

# 针对 JavaScript 页面的高级提取
```bash
./scripts/extract.sh '{"urls": ["https://app.example.com"], "extract_depth": "advanced", "timeout": 60}'
```

### 基本提取方式

```bash
curl --request POST \
  --url https://api.tavily.com/extract \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "urls": ["https://example.com/article"]
  }
```

### 带有查询条件的多个 URL

```bash
curl --request POST \
  --url https://api.tavily.com/extract \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "urls": [
      "https://example.com/ml-healthcare",
      "https://example.com/ai-diagnostics"
    ],
    "query": "AI diagnostic tools accuracy",
    "chunks_per_source": 3
  }
```

## API 参考

### 端点

```json
POST https://api.tavily.com/extract
```

### 请求头

| 头部字段 | 值         |
|---------|-------------|
| `Authorization` | `Bearer <TAVILY_API_KEY>` |
| `Content-Type` | `application/json` |
```

### 请求体

| 字段      | 类型        | 默认值    | 描述                                      |
|-----------|------------|---------|-------------------------------------------|
| `urls`     | array       | Required   | 要提取的 URL 列表（最多 20 个）                         |
| `query`     | string       | null      | 根据相关性对提取内容进行排序                         |
| `chunks_per_source` | integer     | 3        | 每个 URL 的数据块数量（1-5，需要设置查询条件）                |
| `extract_depth` | string       | `"basic"`     | `basic` 或 `advanced`（针对 JavaScript 页面）                |
| `format`     | string       | `"markdown"`     | 输出格式（`markdown` 或 `text`）                   |
| `include_images` | boolean     | false       | 是否包含图片 URL                              |
| `timeout`     | float       | 1-60 秒     | 最大等待时间                               |

## 响应格式

```json
{
  "results": [
    {
      "url": "https://example.com/article",
      "raw_content": "# 文章标题\n\n内容..."
    }
  ],
  "failed_results": [],
  "response_time": 2.3
}
```

## 提取深度

| 深度        | 使用场景      |
|------------|-------------|
| `basic`     | 简单文本提取，速度更快     |
| `advanced`    | 动态渲染的页面、表格、结构化数据           |

## 示例

### 单个 URL 的提取

```bash
curl --request POST \
  --url https://api.tavily.com/extract \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "urls": ["https://docs.python.org/3/tutorial/classes.html"],
    "extract_depth": "basic"
  }
```

### 带有查询条件的提取

```bash
curl --request POST \
  --url https://api.tavily.com/extract \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "urls": [
      "https://example.com/react-hooks",
      "https://example.com/react-state"
    ],
    "query": "useState 和 useEffect 的使用模式",
    "chunks_per_source": 2
  }
```

### 针对 JavaScript 内容丰富的页面的提取

```bash
curl --request POST \
  --url https://api.tavily.com/extract \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "urls": ["https://app.example.com/dashboard"],
    "extract_depth": "advanced",
    "timeout": 60
  }
```

### 批量提取

```bash
curl --request POST \
  --url https://api.tavily.com/extract \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "urls": [
      "https://example.com/page1",
      "https://example.com/page2",
      "https://example.com/page3",
      "https://example.com/page4",
      "https://example.com/page5"
    ],
    "extract_depth": "basic"
  }
```

## 提示

- **每次请求最多支持 20 个 URL**——如需处理更多 URL，请分批提交。
- **使用 `query` 和 `chunks_per_source` 参数来仅提取相关内容**。
- **先尝试使用 `basic` 模式**；如果提取失败，再切换到 `advanced` 模式。
- **对于加载速度较慢的页面，可设置较长的 `timeout`（最长 60 秒）。
- **查看 `failed_results` 列表，了解哪些 URL 无法被成功提取。