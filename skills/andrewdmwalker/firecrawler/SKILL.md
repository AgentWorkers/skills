---
name: firecrawl
description: 使用 Firecrawl API 进行网页抓取和爬取。可以将网页内容以 Markdown 格式获取，截取屏幕截图，提取结构化数据，搜索网页内容，以及爬取文档网站。当用户需要抓取某个 URL 的内容、获取当前网页信息、截取屏幕截图、从页面中提取特定数据，或为某个框架/库爬取相关文档时，可以使用该工具。
version: 1.0.0
author: captmarbles
---

# Firecrawl Web Skill

使用 [Firecrawl](https://firecrawl.dev) 进行网页抓取、搜索和爬取操作。

## 设置

1. 从 [firecrawl.dev/app/api-keys](https://www.firecrawl.dev/app/api-keys) 获取您的 API 密钥。
2. 设置环境变量：
   ```bash
   export FIRECRAWL_API_KEY=fc-your-key-here
   ```
3. 安装 SDK：
   ```bash
   pip3 install firecrawl
   ```

## 使用方法

所有命令均使用该技能目录中的 `fc.py` 脚本。

### 获取页面内容（Markdown 格式）

获取任意 URL 并将其转换为干净的 Markdown 格式。支持处理由 JavaScript 渲染的内容。

```bash
python3 fc.py markdown "https://example.com"
python3 fc.py markdown "https://example.com" --main-only  # skip nav/footer
```

### 截取屏幕截图

获取任意 URL 的完整页面截图。

```bash
python3 fc.py screenshot "https://example.com" -o screenshot.png
```

### 提取结构化数据

根据 JSON 模式从页面中提取特定字段。

**模式示例**（`schema.json`）：
```json
{
  "type": "object",
  "properties": {
    "title": { "type": "string" },
    "price": { "type": "number" },
    "features": { "type": "array", "items": { "type": "string" } }
  }
}
```

### 网页搜索

在网页上搜索并获取搜索结果（可能需要付费高级会员）。

```bash
python3 fc.py search "Python 3.13 new features" --limit 5
```

### 爬取文档

爬取整个文档网站。非常适合学习新的开发框架。

```bash
python3 fc.py crawl "https://docs.example.com" --limit 30
python3 fc.py crawl "https://docs.example.com" --limit 50 --output ./docs
```

**注意：** 每页抓取操作消耗 1 个信用点。请设置合理的使用限制。

### 映射网站 URL

在开始抓取之前，先获取网站上的所有 URL。

```bash
python3 fc.py map "https://example.com" --limit 100
python3 fc.py map "https://example.com" --search "api"
```

## 示例命令

- *"抓取 https://blog.example.com/post 并对其进行总结"*
- *"截取 stripe.com 的屏幕截图"*
- *"从该产品页面中提取名称、价格和功能信息"*
- *"爬取 Astro 的文档，以便帮助我构建网站"*
- *"映射 docs.stripe.com 上的所有 URL"*

## 价格

免费 tier 包含 500 个信用点。1 个信用点等于 1 个页面的抓取、1 张截图或 1 次搜索查询。