---
name: firecrawl
description: >
  **Firecrawl API集成（支持管理式身份验证）**  
  该API支持抓取、爬取、映射以及搜索网页内容。  
  当用户需要从网站中提取数据、遍历整个网站、映射URL或进行网页搜索时，可使用此功能。  
  对于其他第三方应用程序，请使用`api-gateway`技能（https://clawhub.ai/byungkyu/api-gateway）。
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---
# Firecrawl

使用管理认证方式访问 Firecrawl API。该 API 可用于抓取网页、爬取整个网站、映射网站 URL 以及进行全文搜索。

## 快速入门

```bash
# Scrape a webpage
python <<'EOF'
import urllib.request, os, json
data = json.dumps({"url": "https://example.com", "formats": ["markdown"]}).encode()
req = urllib.request.Request('https://gateway.maton.ai/firecrawl/v2/scrape', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基础 URL

```
https://gateway.maton.ai/firecrawl/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Firecrawl API 端点路径。该网关会将请求代理到 `api.firecrawl.dev`，并自动插入您的 API 密钥。

## 认证

所有请求都需要在 `Authorization` 头部包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的 Firecrawl 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=firecrawl&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'firecrawl'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接信息

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "connection": {
    "connection_id": "b5449045-2dcd-4e99-816f-65f80511affb",
    "status": "ACTIVE",
    "creation_time": "2026-03-11T09:49:09.917114Z",
    "last_updated_time": "2026-03-11T09:49:27.616143Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "firecrawl",
    "metadata": {},
    "method": "API_KEY"
  }
}
```

### 删除连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 指定连接

如果您有多个 Firecrawl 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({"url": "https://example.com"}).encode()
req = urllib.request.Request('https://gateway.maton.ai/firecrawl/v2/scrape', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', 'b5449045-2dcd-4e99-816f-65f80511affb')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略该头部，网关将使用默认的（最旧的）活动连接。

## API 参考

### 抓取网页内容

```bash
POST /firecrawl/v2/scrape
```

从单个网页中提取内容。

**必填参数：**
- `url` (string): 要抓取的网页 URL

**可选参数：**
- `formats` (array): 输出格式 - "markdown", "html", "json", "screenshot", "links"（默认：["markdown"]）
- `onlyMainContent` (boolean): 仅提取主要内容，排除页眉/页脚（默认：true）
- `includeTags` (array): 要包含的 HTML 标签
- `excludeTags` (array): 要排除的 HTML 标签
- `waitFor` (integer): 抓取前的等待时间（毫秒）（默认：0）
- `timeout` (integer): 请求超时时间（毫秒）（默认：30000，最大：300000）
- `mobile` (boolean): 模拟移动设备（默认：false）
- `actions` (array): 抓取前要执行的浏览器操作
- `headers` (object): 自定义 HTTP 头部信息
- `blockAds` (boolean): 阻止广告和 cookie 广告（默认：true）

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "url": "https://docs.firecrawl.dev",
    "formats": ["markdown", "html"],
    "onlyMainContent": True,
    "waitFor": 1000
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/firecrawl/v2/scrape', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "success": true,
  "data": {
    "markdown": "# Example Domain\n\nThis domain is for use in documentation...",
    "metadata": {
      "title": "Example Domain",
      "language": "en",
      "sourceURL": "https://example.com",
      "url": "https://example.com/",
      "statusCode": 200,
      "contentType": "text/html",
      "creditsUsed": 1
    }
  }
}
```

### 开始爬取网站

```bash
POST /firecrawl/v2/crawl
```

开始爬取整个网站。返回一个爬取 ID 以便后续查询状态。

**必填参数：**
- `url` (string): 开始爬取的基准 URL

**可选参数：**
- `limit` (integer): 最大爬取页数（默认：10000）
- `maxDepth` (integer): 最大爬取深度
- `includePaths` (array): 要包含的 URL 的正则表达式模式
- `excludePaths` (array): 要排除的 URL 的正则表达式模式
- `allowSubdomains` (boolean): 允许爬取子域名
- `allowExternalLinks` (boolean): 跟随外部链接
- `scrapeOptions` (object): 每页抓取的选项（格式、是否仅提取主要内容等）
- `webhook` (string): 完成通知的 Webhook URL

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "url": "https://example.com",
    "limit": 10,
    "scrapeOptions": {
        "formats": ["markdown"]
    }
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/firecrawl/v2/crawl', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "success": true,
  "id": "019cdc53-0acf-76ec-a80c-3ead753b2730",
  "url": "https://api.firecrawl.dev/v1/crawl/019cdc53-0acf-76ec-a80c-3ead753b2730"
}
```

### 查询爬取状态

```bash
GET /firecrawl/v2/crawl/{id}
```

获取爬取作业的状态和结果。

**路径参数：**
- `id` (string): 爬取作业 ID

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
crawl_id = "019cdc53-0acf-76ec-a80c-3ead753b2730"
req = urllib.request.Request(f'https://gateway.maton.ai/firecrawl/v2/crawl/{crawl_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "success": true,
  "status": "completed",
  "completed": 2,
  "total": 2,
  "creditsUsed": 2,
  "expiresAt": "2026-03-12T09:56:00.000Z",
  "data": [
    {
      "markdown": "# Example Domain\n\nThis domain is for use in documentation...",
      "metadata": {
        "title": "Example Domain",
        "sourceURL": "https://example.com",
        "statusCode": 200
      }
    }
  ]
}
```

**状态值：**
- `scraping` - 爬取进行中
- `completed` - 爬取成功
- `failed` - 爬取失败

### 取消爬取作业

```bash
DELETE /firecrawl/v2/crawl/{id}
```

取消正在进行的爬取作业。

**路径参数：**
- `id` (string): 爬取作业 ID

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
crawl_id = "019cdc53-0acf-76ec-a80c-3ead753b2730"
req = urllib.request.Request(f'https://gateway.maton.ai/firecrawl/v2/crawl/{crawl_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "success": true,
  "status": "cancelled"
}
```

### 映射网站 URL

```bash
POST /firecrawl/v2/map
```

获取网站的所有 URL，但不提取内容。

**必填参数：**
- `url` (string): 起始 URL

**可选参数：**
- `search` (string): 按相关性排序结果的查询条件
- `limit` (integer): 返回的最大链接数（默认：5000，最大：100000）
- `includeSubdomains` (boolean): 是否包含子域名（默认：true）
- `sitemap` (string): 网站地图处理方式 - "skip", "include", "only"（默认："include")
- `ignoreQueryParameters` (boolean): 排除带有查询参数的 URL（默认：true）
- `timeout` (integer): 超时时间（毫秒）

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "url": "https://docs.firecrawl.dev",
    "limit": 100,
    "includeSubdomains": False
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/firecrawl/v2/map', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "success": true,
  "links": [
    "https://docs.firecrawl.dev",
    "https://docs.firecrawl.dev/api-reference",
    "https://docs.firecrawl.dev/introduction"
  ]
}
```

### 进行全文搜索

```bash
POST /firecrawl/v2/search
```

搜索网页并获取每个结果的全文内容。

**必填参数：**
- `query` (string): 搜索查询（最多 500 个字符）

**可选参数：**
- `limit` (integer): 结果数量（默认：5，最大：100）
- `sources` (array): 搜索类型 - "web", "images", "news"（默认：["web"]）
- `country` (string): ISO 国家代码（默认："US")
- `location` (string): 地理定位（例如："Germany")
- `tbs` (string): 时间过滤 - "qdr:d"（天）、"qdr:w"（周）、"qdr:m"（月）、"qdr:y"（年）
- `timeout` (integer): 超时时间（毫秒）（默认：60000）
- `scrapeOptions` (object): 内容提取的选项

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "query": "web scraping best practices",
    "limit": 5,
    "scrapeOptions": {
        "formats": ["markdown"]
    }
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/firecrawl/v2/search', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "success": true,
  "data": [
    {
      "url": "https://example.com/article",
      "title": "Web Scraping Best Practices",
      "description": "Learn the best practices for web scraping...",
      "markdown": "# Web Scraping Best Practices\n\n..."
    }
  ],
  "creditsUsed": 5
}
```

### 批量抓取网页

```bash
POST /firecrawl/v2/batch/scrape
```

一次性抓取多个 URL。

**必填参数：**
- `urls` (array): 要抓取的 URL 列表

**可选参数：**
- `formats` (array): 输出格式（默认：["markdown"]）
- `onlyMainContent` (boolean): 仅提取主要内容（默认：true）
- `webhook` (string): 完成通知的 Webhook URL

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "urls": ["https://example.com", "https://example.org"],
    "formats": ["markdown"]
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/firecrawl/v2/batch/scrape', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "success": true,
  "id": "019cdc59-56b9-7096-a9f9-95fcc92a3a75",
  "url": "https://api.firecrawl.dev/v1/batch/scrape/019cdc59-56b9-7096-a9f9-95fcc92a3a75"
}
```

### 查看批量抓取作业的状态

```bash
GET /firecrawl/v2/batch/scrape/{id}
```

获取批量抓取作业的状态和结果。

**路径参数：**
- `id` (string): 批量抓取作业 ID

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
batch_id = "019cdc59-56b9-7096-a9f9-95fcc92a3a75"
req = urllib.request.Request(f'https://gateway.maton.ai/firecrawl/v2/batch/scrape/{batch_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "success": true,
  "status": "completed",
  "completed": 2,
  "total": 2,
  "creditsUsed": 2,
  "expiresAt": "2026-03-12T10:02:54.000Z",
  "data": [
    {
      "markdown": "# Example Domain\n\n...",
      "metadata": {
        "title": "Example Domain",
        "sourceURL": "https://example.com",
        "statusCode": 200
      }
    }
  ]
}
```

### 取消批量抓取作业

```bash
DELETE /firecrawl/v2/batch/scrape/{id}
```

取消正在进行的批量抓取作业。

**路径参数：**
- `id` (string): 批量抓取作业 ID

### 查看批量抓取作业的错误

```bash
GET /firecrawl/v2/batch/scrape/{id}/errors
```

获取批量抓取作业的错误信息。

**路径参数：**
- `id` (string): 批量抓取作业 ID

**响应：**
```json
{
  "errors": [],
  "robotsBlocked": []
}
```

### 查看单个爬取作业的错误

```bash
GET /firecrawl/v2/crawl/{id}/errors
```

获取单个爬取作业的错误信息。

**路径参数：**
- `id` (string): 爬取作业 ID

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
crawl_id = "019cdc53-0acf-76ec-a80c-3ead753b2730"
req = urllib.request.Request(f'https://gateway.maton.ai/firecrawl/v2/crawl/{crawl_id}/errors')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "errors": [],
  "robotsBlocked": []
}
```

### 查看所有活动的爬取作业

```bash
GET /firecrawl/v2/crawl/active
```

获取所有活动的爬取作业。

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/firecrawl/v2/crawl/active')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "success": true,
  "crawls": []
}
```

### 提取结构化数据

```bash
POST /firecrawl/v2/extract
```

使用 AI 从 URL 中提取结构化数据。

**必填参数：**
- `urls` (array): 要提取数据的 URL 列表
- `prompt` (string): 提取内容的自然语言描述

**可选参数：**
- `schema` (object): 结构化输出的 JSON 模式
- `scrapeOptions` (object): 抓取选项

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "urls": ["https://example.com"],
    "prompt": "Extract the main heading and description"
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/firecrawl/v2/extract', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "success": true,
  "id": "019cdc59-977b-774b-b584-af2af45c055b",
  "urlTrace": []
}
```

### 查看提取作业的状态

```bash
GET /firecrawl/v2/extract/{id}
```

获取提取作业的状态和结果。

**路径参数：**
- `id` (string): 提取作业 ID

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
extract_id = "019cdc59-977b-774b-b584-af2af45c055b"
req = urllib.request.Request(f'https://gateway.maton.ai/firecrawl/v2/extract/{extract_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "success": true,
  "data": [
    {
      "heading": "Example Domain",
      "description": "This domain is for use in documentation..."
    }
  ],
  "status": "completed",
  "expiresAt": "2026-03-11T16:03:05.000Z"
}
```

### 创建浏览器会话

```bash
POST /firecrawl/v2/browser
```

创建一个交互式浏览器会话，以便通过 CDP 进行手动控制。

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({}).encode()
req = urllib.request.Request('https://gateway.maton.ai/firecrawl/v2/browser', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "success": true,
  "id": "019cdc5d-5c9d-732e-a7bd-f095a96a2bb1",
  "cdpUrl": "wss://browser.firecrawl.dev/cdp/...",
  "liveViewUrl": "https://liveview.firecrawl.dev/...",
  "interactiveLiveViewUrl": "https://liveview.firecrawl.dev/...",
  "expiresAt": "2026-03-11T10:17:12.409Z"
}
```

### 列出浏览器会话

```bash
GET /firecrawl/v2/browser
```

列出所有活动的浏览器会话。

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/firecrawl/v2/browser')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "success": true,
  "sessions": [
    {
      "id": "019cdc5d-5c9d-732e-a7bd-f095a96a2bb1",
      "status": "active",
      "cdpUrl": "wss://browser.firecrawl.dev/cdp/...",
      "liveViewUrl": "https://liveview.firecrawl.dev/..."
    }
  ]
}
```

### 删除浏览器会话

```bash
DELETE /firecrawl/v2/browser/{id}
```

删除浏览器会话。

**路径参数：**
- `id` (string): 浏览器会话 ID

### 启动 AI 代理

```bash
POST /firecrawl/v2/agent
```

启动一个 AI 代理以自动导航和提取数据。

**必填参数：**
- `prompt` (string): 要提取的数据描述（最多 10,000 个字符）

**可选参数：**
- `urls` (array): 代理要访问的 URL 列表
- `schema` (object): 结构化输出的 JSON 模式
- `maxCredits` (integer): 消耗限额（默认：2500）
- `strictConstrainToURLs` (boolean): 仅访问提供的 URL
- `model` (string): "spark-1-mini"（默认，成本较低）或 "spark-1-pro"（精度较高）

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "prompt": "Find the pricing information",
    "urls": ["https://example.com"],
    "model": "spark-1-mini"
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/firecrawl/v2/agent', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "success": true,
  "id": "019cdc5d-a2d4-728c-9c91-e9eae475568f"
}
```

### 查看代理作业的状态

```bash
GET /firecrawl/v2/agent/{id}
```

获取代理作业的状态和结果。

**路径参数：**
- `id` (string): 代理作业 ID

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
agent_id = "019cdc5d-a2d4-728c-9c91-e9eae475568f"
req = urllib.request.Request(f'https://gateway.maton.ai/firecrawl/v2/agent/{agent_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "success": true,
  "status": "completed",
  "model": "spark-1-pro",
  "data": {...},
  "expiresAt": "2026-03-12T10:07:30.055Z"
}
```

### 取消代理作业

```bash
DELETE /firecrawl/v2/agent/{id}
```

取消正在进行的代理作业。

**路径参数：**
- `id` (string): 代理作业 ID

## 浏览器操作

使用 `actions` 参数在抓取前与页面交互：

**可用操作：**
- `wait` - 等待指定的毫秒数
- `click` - 根据 CSS 选择器点击元素
- `write` - 在输入框中输入文本
- `scroll` - 滚动页面
- `screenshot` - 生成截图
- `execute` - 运行自定义 JavaScript 代码

## 代码示例

### JavaScript 示例

```javascript
const response = await fetch('https://gateway.maton.ai/firecrawl/v2/scrape', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`
  },
  body: JSON.stringify({
    url: 'https://example.com',
    formats: ['markdown']
  })
});
const data = await response.json();
console.log(data.data.markdown);
```

### Python 示例

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/firecrawl/v2/scrape',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={
        'url': 'https://example.com',
        'formats': ['markdown']
    }
)
data = response.json()
print(data['data']['markdown'])
```

## 注意事项：

- 抓取操作每页消耗 1 个信用点（基本代理）。
- 针对反爬虫网站的增强代理可能会消耗最多 5 个信用点。
- 爬取结果在 24 小时后失效。
- 最大超时时间为 300,000 毫秒（5 分钟）。
- 使用 `onlyMainContent: true` 可获得更干净的结果（不包括导航/页脚内容）。
- 重要提示：当将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境中可能无法正确解析环境变量 `$MATON_API_KEY`。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 缺少 Firecrawl 连接或参数无效 |
| 401 | Maton API 密钥无效或缺失 |
| 402 | 需要支付（Firecrawl 信用点已耗尽） |
| 409 | 冲突（例如，爬取作业已完成） |
| 429 | 超过请求频率限制 |
| 4xx/5xx | 来自 Firecrawl API 的传递错误 |

### 故障排除：API 密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证 API 密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用名称无效

1. 确保您的 URL 路径以 `firecrawl` 开头。例如：
- 正确：`https://gateway.maton.ai/firecrawl/v2/scrape`
- 错误：`https://gateway.maton.ai/v2/scrape`

## 资源

- [Firecrawl API 文档](https://docs.firecrawl.dev/api-reference/v2-introduction)
- [Firecrawl 仪表板](https://firecrawl.dev)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)