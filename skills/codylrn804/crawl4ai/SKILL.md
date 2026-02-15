---
name: crawl4ai
description: 这是一个基于人工智能（AI）的网页抓取框架，用于从网站中提取结构化数据。当 Codex 需要使用 AI 技术来爬取、解析网页内容、提取数据，或者处理动态内容以及复杂的 HTML 结构时，可以选用该框架。
---

# Crawl4ai

## 概述

Crawl4ai 是一个基于人工智能的网页抓取框架，旨在高效地从网站中提取结构化数据。它结合了传统的 HTML 解析技术和人工智能，能够处理动态内容，智能地提取文本，并从复杂的网页中清洗和整理数据。

## 适用场景

当 Codex 需要执行以下操作时，可以使用 Crawl4ai：
- 从网页中提取结构化数据（如产品信息、文章内容、表单数据、表格数据等）
- 抓取包含动态内容或复杂 JavaScript 代码的网站
- 清理并规范从不同 HTML 结构中提取的数据
- 与返回 HTML 数据的 API 或 Web 服务进行交互
- 直接抓取数据以规避 CORS（跨源资源共享）限制
- 可靠地大规模处理网页内容

**常用指令：**
- “从这个网站中提取数据”
- “从 [URL] 页面中抓取 [特定类型的数据]”
- “解析这个 HTML 文件”
- “从 [URL] 获取数据”
- “从 [网站] 中提取结构化信息”
- “从 [网站] 抓取 [数据类型]”

## 快速入门

### 基本用法

```python
from crawl4ai import AsyncWebCrawler, BrowserMode

async def scrape_page(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            browser_mode=BrowserMode.LATEST,
            headless=True
        )
        return result.markdown, result.clean_html
```

### 提取结构化数据

```python
from crawl4ai import AsyncWebCrawler, JsonModeScreener
import json

async def extract_products(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            screenshot=True,
            javascript=True,
            bypass_cache=True
        )
        # Extract product data
        products = []
        for item in result.extracted_content:
            if item['type'] == 'product':
                products.append({
                    'name': item['name'],
                    'price': item['price'],
                    'url': item['url']
                })
        return products
```

## 常见任务

### 网页抓取基础

**场景：** 用户希望从网站中抓取所有文章的标题。

```python
from crawl4ai import AsyncWebCrawler

async def scrape_articles(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            javascript=True,
            verbose=True
        )
        # Extract article titles from HTML
        articles = result.extracted_content if result.extracted_content else []
        titles = [item.get('name', item.get('text', '')) for item in articles]
        return titles
```

**指令示例：** “从这个网站中抓取文章标题” 或 “从 [URL] 获取所有文章标题”

### 动态内容处理

**场景：** 网站通过 JavaScript 加载数据。

```python
from crawl4ai import AsyncWebCrawler

async def scrape_dynamic_site(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            javascript=True,  # Wait for JS execution
            wait_for="body",   # Wait for specific element
            delay=1.5,         # Wait time after load
            headless=True
        )
        return result.markdown
```

**指令示例：** “抓取这个动态更新的网站” 或 “这个页面需要通过 JavaScript 来加载数据”

### 结构化数据提取

**场景：** 提取特定的字段（如价格、描述等）。

```python
from crawl4ai import AsyncWebCrawler

async def extract_product_details(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            screenshot=True,
            js_code="""
                const products = document.querySelectorAll('.product');
                return Array.from(products).map(p => ({
                    name: p.querySelector('.name')?.textContent,
                    price: p.querySelector('.price')?.textContent,
                    url: p.querySelector('a')?.href
                }));
            """
        )
        return result.extracted_content
```

**指令示例：** “从这个页面中提取产品详情” 或 “从 [URL] 获取价格和名称”

### HTML 清理与解析

**场景：** 清理杂乱的 HTML 代码并提取纯净的文本。

```python
from crawl4ai import AsyncWebCrawler

async def clean_and_parse(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            remove_tags=['script', 'style', 'nav', 'footer', 'header'],
            only_main_content=True
        )
        # Clean and return markdown
        clean_text = result.clean_html
        return clean_text
```

**指令示例：** “清理这个 HTML 文件” 或 “从这个页面中提取主要内容”

## 高级功能

### 自定义 JavaScript 注入

```python
async def custom_scrape(url, custom_js):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            js_code=custom_js,
            js_only=True  # Only execute JS, don't download resources
        )
        return result.extracted_content
```

### 会话管理

```python
from crawl4ai import AsyncWebCrawler

async def multi_page_scrape(base_url, urls):
    async with AsyncWebCrawler() as crawler:
        results = []
        for url in urls:
            result = await crawler.arun(
                url=url,
                session_id=f"session_{url}",
                bypass_cache=True
            )
            results.append({
                'url': url,
                'content': result.markdown,
                'status': result.success
            })
        return results
```

## 最佳实践

1. **始终检查网站是否允许抓取** – 遵守 robots.txt 文件和服务条款
2. **设置适当的延迟** – 在请求之间添加延迟，以避免服务器负担过重
3. **优雅地处理错误** – 实现重试机制和错误处理
4. **有选择地提取数据** – 只提取所需的数据，避免下载整个页面
5. **可靠地存储数据** – 将提取的数据保存为结构化格式（如 JSON、CSV）
6. **清理 URL** – 处理重定向和格式错误的 URL

## 错误处理

```python
async def robust_scrape(url):
    try:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
                url=url,
                timeout=30000  # 30 seconds timeout
            )
            if result.success:
                return result.markdown, result.extracted_content
            else:
                print(f"Scraping failed: {result.error_message}")
                return None, None
    except Exception as e:
        print(f"Scraping error: {str(e)}")
        return None, None
```

## 输出格式

Crawl4ai 支持多种输出格式：
- **Markdown**：简洁易读的文本（`result.markdown`）
- **清洗后的 HTML**：结构化且格式整齐的 HTML（`result.clean_html`）
- **提取的内容**：结构化的 JSON 数据（`result.extracted_content`）
- **截图**：页面的可视化展示（`result.screenshot`）
- **链接**：页面上所有的链接（`result-links`）

## 资源

### 脚本/
- 用于常见抓取操作的 Python 脚本：
  - `scrape_single_page.py`：基本抓取工具
  - `scrape_multiple_pages.py`：分页批量抓取
  - `extract_from_html.py`：HTML 解析辅助工具
  - `clean_html.py`：HTML 清理工具

### 参考资料/
- **文档和示例：**
  - `api_reference.md`：完整的 API 文档
  - `examples.md`：常见用例和最佳实践
  - `error_handling.md`：故障排除指南