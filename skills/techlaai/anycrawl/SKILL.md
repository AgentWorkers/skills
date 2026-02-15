# AnyCrawl 技能

AnyCrawl 提供了与 OpenClaw 的集成接口，支持高效的多线程网页抓取、爬取和搜索功能。

## 设置

### 方法 1：环境变量（推荐）

通过将以下内容添加到 `~/.bashrc` 或 `~/.zshrc` 文件中，使其生效：
```bash
export ANYCRAWL_API_KEY="your-api-key"
```

您可以在 [https://anycrawl.dev](https://anycrawl.dev) 获取 API 密钥。

### 方法 2：OpenClaw 网关配置

```bash
openclaw config.patch --set ANYCRAWL_API_KEY="your-api-key"
```

## 函数

### 1. `anycrawl_scrape`

抓取单个 URL 并将其转换为适合大型语言模型 (LLM) 使用的结构化数据。

**参数：**
- `url` (字符串，必填)：要抓取的 URL
- `engine` (字符串，可选)：抓取引擎（默认值：`"cheerio"`、`"playwright"`、`"puppeteer"`
- `formats` (数组，可选)：输出格式（`["markdown"]`、`["html"]`、`["text"]`、`["json"]`、`["screenshot"]`)
- `timeout` (数字，可选)：超时时间（毫秒，默认值：30000）
- `wait_for` (数字，可选)：提取前的延迟时间（仅适用于浏览器引擎）
- `wait_for_selector` (字符串/对象/数组，可选)：等待匹配的 CSS 选择器
- `include_tags` (数组，可选)：仅包含这些 HTML 标签（例如：`["h1", "p", "article"]`)
- `exclude_tags` (数组，可选)：排除这些 HTML 标签
- `proxy` (字符串，可选)：代理 URL（例如：`"http://proxy:port"`）
- `json_options` (对象，可选)：带有模式的 JSON 提取选项
- `extract_source` (字符串，可选)：输出格式（默认值：`"markdown"` 或 `"html"`）

**示例：**
```javascript
// Basic scrape with default cheerio
anycrawl_scrape({ url: "https://example.com" })

// Scrape SPA with Playwright
anycrawl_scrape({ 
  url: "https://spa-example.com",
  engine: "playwright",
  formats: ["markdown", "screenshot"]
})

// Extract structured JSON
anycrawl_scrape({
  url: "https://product-page.com",
  engine: "cheerio",
  json_options: {
    schema: {
      type: "object",
      properties: {
        product_name: { type: "string" },
        price: { type: "number" },
        description: { type: "string" }
      },
      required: ["product_name", "price"]
    },
    user_prompt: "Extract product details from this page"
  }
})
```

### 2. `anycrawl_search`

在 Google 上进行搜索并返回结构化结果。

**参数：**
- `query` (字符串，必填)：搜索查询
- `engine` (字符串，可选)：搜索引擎（默认值：`"google"`）
- `limit` (数字，可选)：每页的最大结果数（默认值：10）
- `offset` (数字，可选)：跳过的结果数量（默认值：0）
- `pages` (数字，可选)：要检索的页面数（默认值：1，最大值：20）
- `lang` (字符串，可选)：语言设置（例如：`"en"`、`"zh"`、`"vi"`）
- `safe_search` (数字，可选)：安全搜索级别（0：关闭，1：中等，2：高级）
- `scrape_options` (对象，可选)：每个结果的抓取选项

**示例：**
```javascript
// Basic search
anycrawl_search({ query: "OpenAI ChatGPT" })

// Multi-page search in Vietnamese
anycrawl_search({ 
  query: "hướng dẫn Node.js",
  pages: 3,
  lang: "vi"
})

// Search and auto-scrape results
anycrawl_search({
  query: "best AI tools 2026",
  limit: 5,
  scrape_options: {
    engine: "cheerio",
    formats: ["markdown"]
  }
})
```

### 3. `anycrawl_crawl_start`

开始爬取整个网站（异步任务）。

**参数：**
- `url` (字符串，必填)：用于开始爬取的起始 URL
- `engine` (字符串，可选)：抓取引擎（默认值：`"cheerio"`、`"playwright"`、`"puppeteer"`
- `strategy` (字符串，可选)：爬取策略（默认值：`"all"`、`"same-domain"`、`"same-hostname"`、`"same-origin"`）
- `max_depth` (数字，可选)：从起始 URL 开始的最大爬取深度（默认值：10）
- `limit` (数字，可选)：最大爬取页面数（默认值：100）
- `include_paths` (数组，可选)：要包含的路径模式（例如：`["/blog/*"]`)
- `exclude_paths` (数组，可选)：要排除的路径模式（例如：`["/admin/*"]`)
- `scrape_paths` (数组，可选)：仅抓取匹配这些模式的 URL
- `scrape_options` (对象，可选)：每页的抓取选项

**示例：**
```javascript
// Crawl entire website
anycrawl_crawl_start({ 
  url: "https://docs.example.com",
  engine: "cheerio",
  max_depth: 5,
  limit: 50
})

// Crawl only blog posts
anycrawl_crawl_start({
  url: "https://example.com",
  strategy: "same-domain",
  include_paths: ["/blog/*"],
  exclude_paths: ["/blog/tags/*"],
  scrape_options: {
    formats: ["markdown"]
  }
})

// Crawl product pages only
anycrawl_crawl_start({
  url: "https://shop.example.com",
  strategy: "same-domain",
  scrape_paths: ["/products/*"],
  limit: 200
})
```

### 4. `anycrawl_crawl_status`

检查爬取任务的状态。

**参数：**
- `job_id` (字符串，必填)：爬取任务 ID

**示例：**
```javascript
anycrawl_crawl_status({ job_id: "7a2e165d-8f81-4be6-9ef7-23222330a396" })
```

### 5. `anycrawl_crawl_results`

获取爬取结果（分页显示）。

**参数：**
- `job_id` (字符串，必填)：爬取任务 ID
- `skip` (数字，可选)：要跳过的结果数量（默认值：0）

**示例：**
```javascript
// Get first 100 results
anycrawl_crawl_results({ job_id: "xxx", skip: 0 })

// Get next 100 results
anycrawl_crawl_results({ job_id: "xxx", skip: 100 })
```

### 6. `anycrawl_crawl_cancel`

取消正在运行的爬取任务。

**参数：**
- `job_id` (字符串，必填)：爬取任务 ID

### 7. `anycrawl_search_and_scrape`

快速辅助功能：在 Google 上搜索并抓取顶部结果。

**参数：**
- `query` (字符串，必填)：搜索查询
- `max_results` (数字，可选)：要抓取的最大结果数（默认值：3）
- `scrape_engine` (字符串，可选)：用于抓取的引擎（默认值：`"cheerio"`）
- `formats` (数组，可选)：输出格式（默认值：`["markdown"]`)
- `lang` (字符串，可选)：搜索语言

**示例：**
```javascript
anycrawl_search_and_scrape({
  query: "latest AI news",
  max_results: 5,
  formats: ["markdown"]
})
```

## 引擎选择指南

| 引擎 | 适用场景 | 速度 | 是否支持 JavaScript 渲染 |
|--------|----------|-------|--------------|
| `cheerio` | 静态 HTML、新闻、博客 | ⚡ 最快 | ❌ 不支持 |
| `playwright` | 单页应用程序、复杂网站 | 🐢 较慢 | ✅ 支持 |
| `puppeteer` | 特定于 Chrome 的网站、数据收集 | 🐢 较慢 | ✅ 支持 |

## 响应格式

所有响应都遵循以下结构：

```json
{
  "success": true,
  "data": { ... },
  "message": "Optional message"
}
```

错误响应：
```json
{
  "success": false,
  "error": "Error type",
  "message": "Human-readable message"
}
```

## 常见错误代码

- `400` - 请求错误（验证失败）
- `401` - 未经授权（API 密钥无效）
- `402` - 需要支付（信用不足）
- `404` - 未找到
- `429` - 超过速率限制
- `500` - 服务器内部错误

## API 限制

- 爬取请求受您的订阅计划限制
- 爬取任务在 24 小时后过期
- 最大爬取次数受信用额度限制

## 链接

- API 文档：https://docs.anycrawl.dev
- 官网：https://anycrawl.dev
- 测试平台：https://anycrawl.dev/playground