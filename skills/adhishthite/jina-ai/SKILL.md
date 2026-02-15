---
name: jina
description: 通过 Jina AI API 进行网页阅读和搜索。可以从 URL（r.jina.ai）获取格式清晰的 Markdown 内容，执行网页搜索（s.jina.ai），或进行深度的多步骤研究（DeepSearch）。
homepage: "https://github.com/adhishthite/jina-ai-skill"
metadata:
  {
    "clawdbot":
      {
        "emoji": "🔍",
        "requires": { "env": ["JINA_API_KEY"] },
        "primaryEnv": "JINA_API_KEY",
        "files": ["scripts/*"],
      },
  }
---

# Jina AI — 阅读器、搜索与深度搜索

Jina AI 提供网页阅读和搜索功能。使用此功能需要设置 `JINA_API_KEY` 环境变量。

> **信任与隐私：** 使用此功能时，URL 和查询数据会传输到 Jina AI（jina.ai）。只有在您信任 Jina 并愿意共享数据的情况下，才请安装此功能。

> **模型调用：** 该功能可以由模型自动调用，无需用户手动触发（这是集成功能的默认行为）。如果您希望仅通过手动操作来调用该功能，请在 OpenClaw 的技能设置中禁用模型调用。

**获取您的 API 密钥：** https://jina.ai/ → 仪表板 → API 密钥

## 外部端点

此功能仅向以下外部端点发送 HTTP 请求：

| 端点 | URL 模式 | 功能 |
|----------|-------------|---------|
| **阅读器 API** | `https://r.jina.ai/{url}` | 将 URL 内容发送给 Jina 并转换为 Markdown 格式 |
| **搜索 API** | `https://s.jina.ai/{query}` | 向 Jina 发送搜索查询以获取网页搜索结果 |
| **深度搜索 API** | `https://deepsearch.jina.ai/v1/chat/completions` | 向 Jina 发送研究问题以进行多步骤分析 |

此功能不会进行其他外部网络调用。

## 安全与隐私

- **身份验证：** 仅将您的 `JINA_API_KEY` 通过 `Authorization` 头部发送到 Jina 的服务器 |
- **发送的数据：** 您提供的 URL 和搜索查询会被发送到 Jina 的服务器进行处理 |
- **本地文件：** 该功能不会读取或传输任何本地文件 |
- **本地存储：** 除标准输出外，不会在本地存储任何数据 |
- **环境访问：** 脚本仅访问 `JINA_API_KEY` 环境变量；不会读取其他环境变量 |
- **Cookies：** 默认情况下不会转发 Cookies；对于已认证的内容，可以使用 `X-Set-Cookie` 头部进行设置，但这是可选的 |

## 端点

| 端点 | 基本 URL | 功能 |
|----------|----------|---------|
| **阅读器** | `https://r.jina.ai/{url}` | 将任何 URL 转换为干净的 Markdown 格式 |
| **搜索** | `https://s.jina.ai/{query}` | 使用大型语言模型（LLM）生成的结果进行网页搜索 |
| **深度搜索** | `https://deepsearch.jina.ai/v1/chat/completions` | 多步骤研究辅助工具 |

所有端点都支持 `Authorization: Bearer $JINA_API_KEY` 的身份验证。

---

## 阅读器 API (`r.jina.ai`)

用于获取任何 URL 并返回适合大型语言模型（LLM）处理的干净内容。支持网页、PDF 文件以及包含大量 JavaScript 代码的网站。

### 基本用法

```bash
# Plain text output
curl -s "https://r.jina.ai/https://example.com" \
  -H "Authorization: Bearer $JINA_API_KEY" \
  -H "Accept: text/plain"

# JSON output (includes url, title, content, timestamp)
curl -s "https://r.jina.ai/https://example.com" \
  -H "Authorization: Bearer $JINA_API_KEY" \
  -H "Accept: application/json"
```

或者使用辅助脚本：`scripts/jina-reader.sh <url> [--json]`

### 参数（通过头部或查询参数）

#### 内容控制

| 头部字段 | 查询参数 | 可能的值 | 默认值 | 说明 |
|--------|-------------|--------|---------|-------------|
| `X-Respond-With` | `respondWith` | `content`, `markdown`, `html`, `text`, `screenshot`, `pageshot`, `vlm`, `readerlm-v2` | 输出格式 |
| `X-Retain-Images` | `retainImages` | `none`, `all`, `alt`, `all_p`, `alt_p` | 图片处理方式 |
| `X-Retain-Links` | `retainLinks` | `none`, `all`, `text`, `gpt-oss` | 链接处理方式 |
| `X-With-Generated-Alt` | `withGeneratedAlt` | `true`/`false` | 是否自动生成图片标题 |
| `X-With-Links-Summary` | `withLinksSummary` | `true` | 是否添加链接部分 |
| `X-With-Images-Summary` | `withImagesSummary` | `true`/`false` | 是否添加图片部分 |
| `X-Token-Budget` | `tokenBudget` | 数字 | 响应的最大令牌数量 |

#### CSS 选择器

| 头部字段 | 查询参数 | 说明 |
|--------|-------------|-------------|
| `X-Target-Selector` | `targetSelector` | 仅提取匹配的元素 |
| `X-Wait-For-Selector` | `waitForSelector` | 在提取前等待指定元素加载完成 |
| `X-Remove-Selector` | `removeSelector` | 在提取前移除指定元素 |

#### 浏览器与网络设置

| 头部字段 | 查询参数 | 说明 |
|--------|-------------|-------------|
| `X-Timeout` | `timeout` | 页面加载超时时间（1-180 秒） |
| `X-Respond-Timing` | `respondTiming` | 确定页面何时“准备好”（例如通过 `html` 或 `network-idle` 等条件） |
| `X-No-Cache` | `noCache` | 忽略缓存内容 |
| `X-Proxy` | `proxy` | 代理服务器的国家代码或 `auto`（自动选择代理） |
| `X-Set-Cookie` | `setCookies` | 为已认证的内容转发 Cookies |

### 常见使用模式

```bash
# Extract main content, remove navigation elements
curl -s "https://r.jina.ai/https://example.com/article" \
  -H "Authorization: Bearer $JINA_API_KEY" \
  -H "X-Retain-Images: none" \
  -H "X-Remove-Selector: nav, footer, .sidebar, .ads" \
  -H "Accept: text/plain"

# Extract specific section
curl -s "https://r.jina.ai/https://example.com" \
  -H "Authorization: Bearer $JINA_API_KEY" \
  -H "X-Target-Selector: article.main-content"

# Parse a PDF
curl -s "https://r.jina.ai/https://example.com/paper.pdf" \
  -H "Authorization: Bearer $JINA_API_KEY" \
  -H "Accept: text/plain"

# Wait for dynamic content
curl -s "https://r.jina.ai/https://spa-app.com" \
  -H "Authorization: Bearer $JINA_API_KEY" \
  -H "X-Wait-For-Selector: .loaded-content" \
  -H "X-Respond-Timing: network-idle"
```

---

## 搜索 API (`s.jina.ai`)

提供适合大型语言模型（LLM）处理的网页搜索结果，包含完整页面内容。

### 基本用法

```bash
# Plain text
curl -s "https://s.jina.ai/your+search+query" \
  -H "Authorization: Bearer $JINA_API_KEY" \
  -H "Accept: text/plain"

# JSON
curl -s "https://s.jina.ai/your+search+query" \
  -H "Authorization: Bearer $JINA_API_KEY" \
  -H "Accept: application/json"
```

或者使用辅助脚本：`scripts/jina-search.sh "<query>" [--json]`

### 搜索参数

| 参数 | 可能的值 | 说明 |
|-------|--------|-------------|
| `site` | 域名 | 限制搜索范围到特定网站 |
| `type` | `web`, `images`, `news` | 搜索类型 |
| `num` / `count` | 0-20 | 结果数量 |
| `gl` | 国家代码 | 地理位置（例如 `us`, `in`） |
| `filetype` | 文件扩展名 | 按文件类型过滤 |
| `intitle` | 字符串 | 必须出现在页面标题中 |

所有阅读器相关的参数也适用于搜索结果。

### 常见使用模式

```bash
# Site-scoped search
curl -s "https://s.jina.ai/OpenAI+GPT-5?site=reddit.com" \
  -H "Authorization: Bearer $JINA_API_KEY" \
  -H "Accept: text/plain"

# News search
curl -s "https://s.jina.ai/latest+AI+news?type=news&num=5" \
  -H "Authorization: Bearer $JINA_API_KEY" \
  -H "Accept: application/json"

# Search for PDFs
curl -s "https://s.jina.ai/machine+learning+survey?filetype=pdf&num=5" \
  -H "Authorization: Bearer $JINA_API_KEY"
```

---

## 深度搜索

结合搜索、阅读和推理的多步骤研究工具。兼容 OpenAI 的聊天式问答 API。

```bash
curl -s "https://deepsearch.jina.ai/v1/chat/completions" \
  -H "Authorization: Bearer $JINA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "jina-deepsearch-v1",
    "messages": [{"role": "user", "content": "Your research question here"}],
    "stream": false
  }'
```

或者使用辅助脚本：`scripts/jina-deepsearch.sh "<question>"`

适用于需要多个来源和推理过程的复杂研究任务。

---

## 辅助脚本

| 脚本 | 功能 |
|--------|---------|
| `scripts/jina-reader.sh` | 将任何 URL 读取为 Markdown 格式 |
| `scripts/jina-search.sh` | 执行网页搜索 |
| `scripts/jina-deepsearch.sh` | 进行多步骤深度研究 |
| `scripts/jina-reader.py` | 使用 Python 编写的阅读器脚本（仅依赖标准库） |

---

## 使用限制

- **免费（无 API 密钥）：** 每分钟 20 次请求 |
- **使用 API 密钥：** 提供更高的请求限制，并采用基于令牌的计费方式

## API 文档

- 阅读器 API：https://jina.ai/reader |
- 搜索 API：https://s.jina.ai/docs |
- OpenAPI 规范：https://r.jina.ai/openapi.json | https://s.jina.ai/openapi.json

## 使用场景

| 需求 | 使用功能 |
|------|-----|
| 将 URL 转换为 Markdown | **阅读器** — 适用于包含大量 JavaScript 代码的网站 |
| 进行网页搜索 | **搜索** — 生成适合大型语言模型的结果 |
| 多源复杂研究 | **深度搜索** |
| 从 URL 解析 PDF 文件 | **阅读器** — 直接提供 PDF URL |
| 截取页面截图 | **阅读器** 并使用 `X-Respond-With: screenshot` 参数 |
| 提取结构化数据 | **阅读器** 并使用 `jsonSchema` 参数 |

---

## 注意事项：