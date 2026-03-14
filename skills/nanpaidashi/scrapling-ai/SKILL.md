---
name: scrapling
description: 使用 Scrapling 工具抓取网站，支持自适应解析、绕过 Cloudflare 以及 MCP（可能是一个特定服务或协议的缩写）。该工具能够处理动态内容、应对反爬虫机制，并提供格式整齐的 HTML 或 JSON 输出结果。
metadata:
  {
    "openclaw":
      {
        "emoji": "🕷️",
        "requires": { "bins": ["scrapling"] },
        "install":
          [
            {
              "id": "pipx",
              "kind": "pipx",
              "package": "scrapling",
              "bins": ["scrapling"],
              "label": "Install Scrapling CLI (pipx)",
            },
            {
              "id": "python3-pip",
              "kind": "pip",
              "package": "scrapling",
              "bins": ["scrapling"],
              "label": "Install Scrapling CLI (pip)",
            },
          ],
      },
  }
---
# 抓取技能

使用 `scrapling` 命令行工具（CLI）来抓取网站，该工具具备自适应解析能力和反爬虫机制。

## 适用场景

✅ **适用于以下情况：**
- 抓取静态或动态网站
- 规避 Cloudflare、验证码或爬虫检测
- 从网页中提取结构化数据（HTML/JSON）
- 处理由 JavaScript 渲染的内容
- 获取不含额外脚本/CSS 的纯净 HTML 内容

## 不适用场景

❌ **不适用以下情况：**
- 简单的 HTTP 请求 → 使用 `web_fetch` 工具
- 需要完整的浏览器自动化操作 → 使用 `browser` 工具
- 基于 API 的数据 → 使用直接的 API 调用
- 本地文件处理 → 使用文件处理工具

## 设置

```bash
# Install CLI
pipx install scrapling
scrapling --version
```

## 常用命令

### 基本抓取操作

```bash
# Get clean HTML
scrapling https://example.com -o html

# Get JSON structure
scrapling https://example.com -o json

# Save to file
scrapling https://example.com -o output.html
```

### 使用请求头/设置超时

```bash
# Custom headers
scrapling https://example.com --headers "User-Agent: Mozilla/5.0"

# Timeout (seconds)
scrapling https://slow-site.com --timeout 30
```

### 提取特定元素

```bash
# XPath extraction
scrapling https://example.com -e "//div[@class='content']" -o html

# CSS selector
scrapling https://example.com -e "div.content" -o html
```

### 输出包含字段的 JSON 数据

```bash
# Extract title, meta description
scrapling https://example.com \
  --fields 'title,meta_description' \
  -o json
```

## MCP 集成

`scrapling` 支持 MCP（模型上下文协议，Model Context Protocol），可用于 AI 代理：

```bash
# Start MCP server
scrapling mcp start
```

然后通过 MCP 配置您的代理以使用 `scraping` 工具。

## 示例

### 抓取新闻文章

```bash
scrapling https://example.com/news/article-123 \
  --fields 'title,author,publish_date,content' \
  -o json
```

### 提取产品信息

```bash
scrapling https://shop.example.com/products \
  -e "//div[@class='product']" \
  -o html
```

### 应对 Cloudflare

```bash
# Scrapling auto-bypasses most protections
scrapling https://protected-site.com -o html
```

## 注意事项

- 默认超时时间为 10 秒
- 自动检测最佳输出格式（html/json/text）
- 根据需要使用无头浏览器处理动态内容
- 遵守速率限制；在请求之间添加延迟

## JSON 输出格式

```json
{
  "title": "Page Title",
  "meta_description": "Description text",
  "content": "<clean HTML>",
  "links": ["http://...", "..."],
  "images": [{"src": "...", "alt": "..."}]
}
```