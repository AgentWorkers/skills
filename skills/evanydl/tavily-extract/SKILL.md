---
name: extract
description: "使用 Tavily 的提取 API 从特定 URL 中提取内容。该 API 可从网页中获取纯净的 Markdown 或纯文本格式的数据。当您拥有具体的 URL 并且需要获取其内容时（而无需编写代码），可以使用此方法。"
---
# 技能提取

从特定 URL 中提取干净的内容。当你知道需要从哪些页面获取内容时，这个工具非常实用。

## 认证

该脚本通过 Tavily MCP 服务器使用 OAuth 进行认证。**无需手动设置**——首次运行时，它会：
1. 检查 `~/.mcp-auth/` 文件夹中是否存在已有的令牌；
2. 如果没有找到令牌，会自动打开浏览器进行 OAuth 认证。

> **注意：** 你必须拥有一个有效的 Tavily 账户。此认证流程仅支持登录，不支持账户创建。如果没有账户，请先访问 [tavily.com](https://tavily.com) 注册。

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
./scripts/extract.sh '<json>'
```

**示例：**
```bash
# Single URL
./scripts/extract.sh '{"urls": ["https://example.com/article"]}'

# Multiple URLs
./scripts/extract.sh '{"urls": ["https://example.com/page1", "https://example.com/page2"]}'

# With query focus and chunks
./scripts/extract.sh '{"urls": ["https://example.com/docs"], "query": "authentication API", "chunks_per_source": 3}'

# Advanced extraction for JS pages
./scripts/extract.sh '{"urls": ["https://app.example.com"], "extract_depth": "advanced", "timeout": 60}'
```

### 基本提取

```bash
curl --request POST \
  --url https://api.tavily.com/extract \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "urls": ["https://example.com/article"]
  }'
```

### 带查询条件的多个 URL

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
  }'
```

## API 参考

### 端点

```
POST https://api.tavily.com/extract
```

### 请求头

| 头部字段 | 值         |
|---------|------------|
| `Authorization` | `Bearer <TAVILY_API_KEY>` |
| `Content-Type` | `application/json` |

### 请求体

| 字段        | 类型        | 默认值      | 描述                |
|------------|------------|-------------|-------------------|
| `urls`      | array       | Required    | 需要提取的 URL 列表（最多 20 个）   |
| `query`     | string      | null       | 根据相关性对提取结果进行排序      |
| `chunks_per_source` | integer     | 3          | 每个 URL 的提取片段数量（1-5，需要设置 `query`） |
| `extract_depth` | string      | `"basic"`     | 提取方式：`basic` 或 `advanced`（针对 JavaScript 页面） |
| `format`     | string      | `"markdown"`     | 输出格式：`markdown` 或 `text`     |
| `include_images` | boolean     | false       | 是否包含图片 URL            |
| `timeout`     | float       | 可配置     | 最大等待时间（1-60 秒）         |

### 响应格式

```json
{
  "results": [
    {
      "url": "https://example.com/article",
      "raw_content": "# Article Title\n\nContent..."
    }
  ],
  "failed_results": [],
  "response_time": 2.3
}
```

## 提取深度

| 提取深度 | 适用场景       |
|---------|-----------------|
| `basic`    | 简单文本提取，速度较快         |
| `advanced` | 动态渲染的页面、表格、结构化数据     |

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
  }'
```

### 带查询条件的定向提取

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
    "query": "useState and useEffect patterns",
    "chunks_per_source": 2
  }'
```

### 含大量 JavaScript 代码的页面

```bash
curl --request POST \
  --url https://api.tavily.com/extract \
  --header "Authorization: Bearer $TAVILY_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "urls": ["https://app.example.com/dashboard"],
    "extract_depth": "advanced",
    "timeout": 60
  }'
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
  }'
```

## 提示

- **每次请求最多支持 20 个 URL**——如需处理更多 URL，请分批处理。
- **使用 `query` 和 `chunks_per_source` 参数** 仅提取相关内容。
- **先尝试 `basic` 模式**，如果内容提取失败再切换到 `advanced` 模式。
- **对于加载速度较慢的页面，可以设置较长的 `timeout` 值（最长 60 秒）。
- **查看 `failed_results` 列表**，了解哪些 URL 无法成功提取。