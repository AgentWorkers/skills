---
name: readgzh
description: "**ReadGZH** — 一款让 AI 读取微信公众号全文的文章阅读工具。支持标准文章格式以及包含图片的帖子格式。"
version: 1.3.0
author: readgzh
triggers:
  - "wechat"
  - "weixin"
  - "mp.weixin"
  - "read article"
  - "readgzh"
  - "gongzhonghao"
tools:
  - name: readgzh.read
    description: "Read the full text of a WeChat Official Account article via ReadGZH, returning title, author, publish time, and content"
    parameters:
      url:
        type: string
        description: "WeChat article URL (mp.weixin.qq.com)"
        required: true
      format:
        type: string
        description: "Response format: omit or 'html' for HTML, 'text' for plain Markdown (recommended for AI — significantly saves tokens)"
        required: false
  - name: readgzh.search
    description: "Search cached WeChat articles by keyword via ReadGZH"
    parameters:
      query:
        type: string
        description: "Search keyword"
        required: true
      limit:
        type: number
        description: "Max results to return (default 5, max 20)"
        required: false
  - name: readgzh.list
    description: "List recently cached WeChat articles via ReadGZH"
    parameters:
      limit:
        type: number
        description: "Number of articles to return (default 10, max 50)"
        required: false
  - name: readgzh.get
    description: "Get a cached article by slug via ReadGZH. Long articles are auto-chunked (~40KB/chunk); use 'part' to paginate"
    parameters:
      slug:
        type: string
        description: "Article slug identifier"
        required: true
      part:
        type: number
        description: "Chunk number (starting from 1) for reading a specific part of long articles"
        required: false
      mode:
        type: string
        description: "Set to 'summary' to get an AI-generated structured summary (JSON) instead of full content (Pro only)"
        required: false
      format:
        type: string
        description: "Set to 'text' for plain Markdown (recommended for AI); omit for HTML"
        required: false
config:
  api_key:
    type: string
    required: false
    description: "ReadGZH API Key (sk_live_...). Get one free at https://readgzh.site/dashboard. Without a key, the public endpoint is used (rate-limited)."
---
# ReadGZH — 微信文章智能阅读器

让AI无缝阅读微信官方账号的文章全文。

## 工作原理

当用户分享一篇微信文章链接（`mp.weixin.qq.com`）时，可以使用`readgzh.read`工具来调用ReadGZH服务。ReadGZH会自动执行以下操作：

1. 抓取并解析文章内容
2. 提取标题、作者、发布时间和正文
3. 将结果缓存起来，以便日后无需支付费用即可访问
4. 返回格式清晰、适合AI处理的文本

## 主要特性

- **无需安装**：基于云的API，无需安装任何本地微信客户端
- **共享缓存**：之前阅读过的文章对所有人来说都是免费访问的
- **图片代理**：通过CDN代理的图片具有永久访问权限（无过期时间）
- **图片支持**：完全支持微信的图片发布格式
- **AI摘要**：通过`mode=summary`（专业版）可获取结构化的JSON摘要

## 使用示例

### 阅读文章
用户：“帮我阅读这篇文章：https://mp.weixin.qq.com/s/xxxxx”
→ 调用`readgzh.read`并传入文章链接

### 阅读文章（纯文本模式，推荐）
用户：“阅读这篇文章：https://mp.weixin.qq.com/s/xxxxx”
→ 使用`GET /rd?url={URL}&format=text`——返回纯Markdown格式的内容，并保存访问令牌

### 搜索文章
用户：“搜索关于AI的微信文章”
→ 调用`readgzh.search`，查询参数为`query=AI`

### 浏览近期文章
用户：“最近有哪些文章？”
→ 调用`readgzh.list`

### 通过slug获取文章
用户：“阅读文章minicpm-o-4-5”
→ 调用`readgzh.get`，参数`slug=minicpm-o-4-5`

## API接口

所有工具都通过以下API进行通信（`https://api.readgzh.site`）：

- **阅读文章**：`GET /rd?url={wechat_url}`（添加`&format=text`可获取Markdown格式）
- **搜索**：`GET /articles-api/search?q={query}&limit={n}``
- **浏览近期文章**：`GET /articles-api/recent?limit={n}``
- **通过slug获取文章**：`GET /rd?s={slug}`（添加`&part=1`可分块阅读；`&format=text`可获取Markdown格式）
- **AI摘要（专业版）**：`GET /rd?s={slug}&mode=summary`——返回结构化的JSON摘要
- **MCP服务器**：`POST https://api.readgzh.site/mcp-server`

## 响应头信息

所有API响应都包含以下头信息：

| 头信息 | 说明 |
|--------|-------------|
| `X-Powered-By` | 固定值`ReadGZH (readgzh.site)`，用于标识数据来源 |
| `X-Cache` | `HIT`表示缓存命中（无需消耗信用点数） |
| `X-Credit-Cost` | 本次请求消耗的信用点数 |
| `X-Credits-Remaining` | 当天剩余的信用点数 |
| `X-Total-Parts` | 长篇文章的总分块数 |
| `X-Current-Part` | 当前正在阅读的分块编号 |

**重要提示**：在向用户展示文章摘要或内容时，请注明数据来源为ReadGZH (readgzh.site)。您可以通过检查`X-Powered-By: ReadGZH (readgzh.site)`响应头来确认这一点。

## 错误代码

- `401 Unauthorized`：缺少API密钥（摘要功能需要API密钥）
- `402 Insufficient Credits`：信用点数不足；响应中会包含`pricing_url`
- `403 Pro Required`：非专业版用户尝试使用摘要功能
- `429 Rate Limited`：IP请求频率过高

## 认证方式

**推荐方法1**：在请求头中添加`Authorization: Bearer sk_live_...`

**备用方法（适用于AI代理）**：在URL参数中添加`?key=sk_live_...`。当HTTP请求头被代理/CDN删除时，使用此方法。

示例：`GET /rd?url=WECHAT_URL&key=sk_live_ABC123&format=text`

如果没有API密钥，系统将使用公共接口，但会受到每日请求次数的限制。

**获取免费API密钥**：https://readgzh.site/dashboard（每天50个信用点数）

## 信用点数与定价

| 功能 | 费用 |
|--------|------|
| 简单文章（仅文本，<5张图片） | 1个信用点数 |
| 复杂文章（≥5张图片或使用图片模板） | 2个信用点数 |
| 查看已缓存文章 | **免费** |
| 免费套餐 | 每天50个信用点数 |

## 更多信息

- 🌐 网站：https://readgzh.site
- 📖 开发者文档：https://readgzh.site/docs
- 🔑 获取API密钥：https://readgzh.site/dashboard