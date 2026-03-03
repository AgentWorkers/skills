---
name: stripfeed
description: 从任何 URL 获取格式整齐、适合 AI 处理的 Markdown 文本，同时包含标记（tokens）的数量和缓存信息。从网页中去除广告、导航栏、脚本以及其他无关内容。
version: 1.0.0
metadata:
  openclaw:
    requires:
      env: [STRIPFEED_API_KEY]
      bins: [curl]
    primaryEnv: STRIPFEED_API_KEY
    emoji: "📄"
    homepage: https://www.stripfeed.dev
---
# StripFeed

该工具可将任何URL转换为适合大型语言模型（LLM）使用的简洁Markdown格式。它会去除广告、导航栏、脚本以及无关内容，并返回生成的Markdown中的字符数，以便您准确了解所使用的文本量。

## 使用场景

每当您需要读取网页、文章、文档或任何URL内容时，都可以使用StripFeed。与直接获取原始HTML相比，它生成的输出更加整洁，并会提供字符数统计信息。

## 认证

所有请求都需要`STRIPFEED_API_KEY`环境变量。请将其作为Bearer令牌传递：

```
Authorization: Bearer $STRIPFEED_API_KEY
```

您可以在[https://www.stripfeed.dev](https://www.stripfeed.dev)免费获取API密钥（每月200次请求，无需信用卡）。

## 获取单个URL的内容

```bash
curl -s "https://www.stripfeed.dev/api/v1/fetch?url=URL_HERE" \
  -H "Authorization: Bearer $STRIPFEED_API_KEY"
```

该功能会直接以Markdown格式返回处理后的内容（Content-Type: text/markdown）。

### 参数

| 参数          | 是否必填 | 描述                                                                                         |
|---------------|--------|-------------------------------------------------------------------------------------------------------------------------|
| `url`         | 是      | 需要获取的URL（必须是http或https格式）                                                                                         |
| `format`       | 否       | 输出格式：`markdown`（默认）、`json`、`text`、`html`（仅限专业版）                                                                                   |
| `selector`      | 否       | 用于提取特定内容的CSS选择器（例如`article`、`.content`、`#main`）                                                                                   |
| `cache`        | 否       | 设置为`false`可绕过缓存并强制重新获取内容                                                                                   |
| `ttl`         | 否       | 缓存时长（以秒为单位，默认为3600秒，专业版最长86400秒）                                                                                   |
| `max_tokens`    | 否       | 限制输出字符数，以符合您的预算                                                                                         |
| `model`        | 否       | 用于追踪成本的AI模型ID（例如`claude-sonnet-4-6`、`gpt-4o`）                                                                                   |

### JSON格式（推荐用于结构化响应）

如果您需要同时获取元数据，可以使用`format=json`：

```bash
curl -s "https://www.stripfeed.dev/api/v1/fetch?url=URL_HERE&format=json" \
  -H "Authorization: Bearer $STRIPFEED_API_KEY"
```

JSON响应包含以下信息：

```json
{
  "markdown": "# Page Title\n\nClean content...",
  "url": "https://example.com",
  "title": "Page Title",
  "tokens": 1250,
  "originalTokens": 15000,
  "savingsPercent": 91.7,
  "cached": false,
  "fetchMs": 430,
  "format": "json",
  "truncated": false,
  "selector": null,
  "model": null
}
```

### 响应头

所有响应都会包含以下头部信息：

- `X-StripFeed-Tokens`：处理后内容的字符数
- `X-StripFeed-Original-Tokens`：原始HTML的字符数
- `X-StripFeed-Savings-Percent`：节省的字符数百分比
- `X-StripFeed-Cache`：请求是否命中缓存（`HIT`或`MISS`）
- `X-StripFeed-Fetch-Ms`：获取URL所需的时间（如果缓存命中则为0）
- `X-StripFeed-Format`：使用的输出格式

## 批量获取（专业版）

一次请求最多可获取10个URL的内容：

```bash
curl -s -X POST "https://www.stripfeed.dev/api/v1/batch" \
  -H "Authorization: Bearer $STRIPFEED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com", "https://example.org"]}'
```

URL中也可以包含选择器：

```json
{
  "urls": [
    { "url": "https://example.com", "selector": "article" },
    { "url": "https://example.org" }
  ],
  "model": "claude-sonnet-4-6"
}
```

批量请求的响应格式如下：

```json
{
  "results": [
    { "url": "...", "markdown": "...", "tokens": 1250, "status": 200 },
    { "url": "...", "error": "Failed to fetch", "status": 502 }
  ],
  "total": 2,
  "success": 1,
  "failed": 1
}
```

即使某个URL请求失败，也不会影响整个批处理的进度。请检查每个请求的`status`字段以获取错误信息。

## 错误处理

| 状态码        | 含义                                                                                          |
|--------------|-------------------------------------------------------------------------------------------------------------------------|
| 401         | API密钥缺失或无效                                                                                   |
| 403         | 该功能仅限专业版使用                                                                                   |
| 422         | URL、格式或参数无效                                                                                   |
| 429         | 超过请求频率限制或月度配额                                                                                   |
| 502         | 目标URL无法访问或返回错误                                                                                   |
| 504         | 目标URL超时（请求时长限制为9秒）                                                                                   |

## 使用建议

- 默认输出格式为`markdown`，仅包含原始文本。如需获取字符数和元数据，请使用`format=json`。
- 响应内容默认会被缓存1小时。如需实时数据，请设置`cache=false`。
- `max_tokens`参数有助于控制输出字符数，以满足您的需求。
- 使用`selector`仅获取主要内容（例如`selector=article`或`selector=.post-content`），从而忽略侧边栏和页脚信息。
- 免费版：每月200次请求，仅支持Markdown格式。
- 专业版（每月19美元）：支持10万次请求、所有格式、使用选择器以及批量处理功能。