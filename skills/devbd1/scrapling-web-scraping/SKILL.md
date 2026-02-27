---
name: scrapling
description: 使用Scrapling进行高级网络爬虫开发——针对MCP（MCP-native）平台提供的提取、爬取及反爬虫处理方案。通过mcporter（MCP）工具进行执行；本文档涵盖了相关策略、实用技巧及最佳实践。
---
# 网页抓取——MCP原生指南

> **指南层 + MCP集成**  
> 使用此技能来制定抓取策略和模式。执行抓取任务时，通过`mcporter`调用Scrapling的MCP服务器。

## 快速入门（MCP）

### 1. 安装支持MCP的Scrapling工具  
```bash
pip install scrapling[mcp]
# Or for full features:
pip install scrapling[mcp,playwright]
python -m playwright install chromium
```

### 2. 将Scrapling添加到OpenClaw的MCP配置中  
```json
{
  "mcpServers": {
    "scrapling": {
      "command": "python",
      "args": ["-m", "scrapling.mcp"]
    }
  }
}
```

### 3. 通过mcporter进行调用  
```
mcporter call scrapling fetch_page --url "https://example.com"
```

## 执行与指导  
| 任务 | 工具 | 示例 |
|------|------|---------|
| 获取页面内容 | **mcporter** | `mcporter call scrapling fetch_page --url URL` |
| 使用CSS提取数据 | **mcporter** | `mcporter call scrapling css_select --selector ".title::text"` |
| 应该使用哪种抓取工具？ | **本技能** | 请参阅下方的“抓取工具选择指南” |
| 如何应对机器人攻击？ | **本技能** | 请参阅“反机器人攻击策略” |
| 复杂的爬取模式？ | **本技能** | 请参阅“爬虫使用技巧” |

## 抓取工具选择指南  
```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   Fetcher       │────▶│ DynamicFetcher   │────▶│ StealthyFetcher  │
│   (HTTP)        │     │ (Browser/JS)     │     │ (Anti-bot)       │
└─────────────────┘     └──────────────────┘     └──────────────────┘
     Fastest              JS-rendered               Cloudflare, 
     Static pages         SPAs, React/Vue          Turnstile, etc.
```

### 决策树  
1. **静态HTML页面？** → 使用`Fetcher`（速度比其他工具快10-100倍）  
2. **需要执行JavaScript代码？** → 使用`DynamicFetcher`  
3. **被网站阻止？** → 使用`StealthyFetcher`  
4. **需要处理复杂的会话状态？** → 使用相应的会话管理工具  

### MCP抓取模式  
- `fetch_page` — HTTP请求工具  
- `fetch_dynamic` — 基于浏览器的抓取工具（使用Playwright）  
- `fetch_stealthy` — 防止机器人攻击的抓取模式  

## 反机器人攻击策略  
### 第1级：常规HTTP请求  
```python
# MCP call: fetch_page with options
{
  "url": "https://example.com",
  "headers": {"User-Agent": "..."},
  "delay": 2.0
}
```

### 第2级：会话状态管理  
```python
# Use sessions for cookie/state across requests
FetcherSession(impersonate="chrome")  # TLS fingerprint spoofing
```

### 第3级：隐秘抓取模式  
```python
# MCP: fetch_stealthy
StealthyFetcher.fetch(
    url,
    headless=True,
    solve_cloudflare=True,  # Auto-solve Turnstile
    network_idle=True
)
```

### 第4级：代理轮换  
详情请参阅`references/proxy-rotation.md`  

## 自适应抓取（提高稳定性）  
Scrapling可以通过使用自适应选择器来应对网站重新设计：  
```python
# First run — save fingerprints
products = page.css('.product', auto_save=True)

# Later runs — auto-relocate if DOM changed
products = page.css('.product', adaptive=True)
```

**MCP使用方法：**  
```
mcporter call scrapling css_select \\
  --selector ".product" \\
  --adaptive true \\
  --auto-save true
```

## 爬虫框架（用于大规模爬取）  
何时使用爬虫：  
- ✅ **使用爬虫**：当需要抓取10页以上的内容、需要并发处理、支持任务恢复或需要使用代理轮换时  
- ✅ **直接使用HTTP请求**：当只需抓取1-5页内容、提取速度较快且流程简单时  

### 基本爬虫使用技巧  
```python
from scrapling.spiders import Spider, Response

class ProductSpider(Spider):
    name = "products"
    start_urls = ["https://example.com/products"]
    concurrent_requests = 10
    download_delay = 1.0
    
    async def parse(self, response: Response):
        for product in response.css('.product'):
            yield {
                "name": product.css('h2::text').get(),
                "price": product.css('.price::text').get(),
                "url": response.url
            }
        
        # Follow pagination
        next_page = response.css('.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page)

# Run with resume capability
result = ProductSpider(crawldir="./crawl_data").start()
result.items.to_jsonl("products.jsonl")
```

### 高级技巧：多会话爬虫  
```python
from scrapling.spiders import Spider, Request, Response
from scrapling.fetchers import FetcherSession, AsyncStealthySession

class MultiSessionSpider(Spider):
    name = "multi"
    start_urls = ["https://example.com/"]
    
    def configure_sessions(self, manager):
        manager.add("fast", FetcherSession(impersonate="chrome"))
        manager.add("stealth", AsyncStealthySession(headless=True), lazy=True)
    
    async def parse(self, response: Response):
        for link in response.css('a::attr(href)').getall():
            if "/protected/" in link:
                yield Request(link, sid="stealth")
            else:
                yield Request(link, sid="fast")
```

### 爬虫功能  
- **暂停/恢复**：`crawldir`参数用于保存抓取进度  
- **流式处理**：`async for item in spider.stream()`实现实时数据处理  
- **自动重试**：可配置对被阻止请求的重试策略  
- **数据导出**：内置的`to_json()`、`to_jsonl()`函数可用于数据导出  

## 命令行接口（CLI）与交互式Shell  
### 终端命令提取（无需编写代码）  
```bash
# Extract to markdown
scrapling extract get 'https://example.com' content.md

# Extract specific element
scrapling extract get 'https://example.com' content.txt \\
  --css-selector '.article' \\
  --impersonate 'chrome'

# Stealth mode
scrapling extract stealthy-fetch 'https://protected.com' content.md \\
  --no-headless \\
  --solve-cloudflare
```

### 交互式Shell  
```bash
scrapling shell

# Inside shell:
>>> page = Fetcher.get('https://example.com')
>>> page.css('h1::text').get()
>>> page.find_all('div', class_='item')
```

## 解析器API（超越CSS/XPath）  
### BeautifulSoup风格的解析方法  
```python
# Find by attributes
page.find_all('div', {'class': 'product', 'data-id': True})
page.find_all('div', class_='product', id=re.compile(r'item-\\d+'))

# Text search
page.find_by_text('Add to Cart', tag='button')
page.find_by_regex(r'\\$\\d+\\.\\d{2}')

# Navigation
first = page.css('.product')[0]
parent = first.parent
siblings = first.next_siblings
children = first.children

# Similarity
similar = first.find_similar()  # Find visually/structurally similar elements
below = first.below_elements()  # Elements below in DOM
```

### 自动生成的选择器  
```python
# Get robust selector for any element
element = page.css('.product')[0]
selector = element.auto_css_selector()  # Returns stable CSS path
xpath = element.auto_xpath()
```

## 代理轮换  
```python
from scrapling.spiders import ProxyRotator

# Cyclic rotation
rotator = ProxyRotator([
    "http://proxy1:8080",
    "http://proxy2:8080",
    "http://user:pass@proxy3:8080"
], strategy="cyclic")

# Use with any session
with FetcherSession(proxy=rotator.next()) as session:
    page = session.get('https://example.com')
```

## 常见抓取技巧  
### 分页处理  
```python
# Page numbers
for page_num in range(1, 11):
    url = f"https://example.com/products?page={page_num}"
    ...

# Next button
while next_page := response.css('.next a::attr(href)').get():
    yield response.follow(next_page)

# Infinite scroll (DynamicFetcher)
with DynamicSession() as session:
    page = session.fetch(url)
    page.scroll_to_bottom()
    items = page.css('.item').getall()
```

### 登录会话管理  
```python
with StealthySession(headless=False) as session:
    # Login
    login_page = session.fetch('https://example.com/login')
    login_page.fill('input[name="username"]', 'user')
    login_page.fill('input[name="password"]', 'pass')
    login_page.click('button[type="submit"]')
    
    # Now session has cookies
    protected_page = session.fetch('https://example.com/dashboard')
```

### Next.js数据提取  
```python
# Extract JSON from __NEXT_DATA__
import json
import re

next_data = json.loads(
    re.search(
        r'__NEXT_DATA__" type="application/json">(.*?)</script>',
        page.html_content,
        re.S
    ).group(1)
)
props = next_data['props']['pageProps']
```

## 输出格式  
```python
# JSON (pretty)
result.items.to_json('output.json')

# JSONL (streaming, one per line)
result.items.to_jsonl('output.jsonl')

# Python objects
for item in result.items:
    print(item['title'])
```

## 性能优化建议  
1. **尽可能使用HTTP请求工具** — 速度比浏览器快10-100倍  
2. **模拟浏览器行为** — 使用`impersonate='chrome'`来规避TLS指纹识别  
3. **支持HTTP/3协议** — 使用`FetcherSession(http3=True)`  
4. **限制资源消耗** — 在`Dynamic/Stealthy`模式下设置`disable_resources=True`  
5. **连接池** — 在多个请求中重用会话资源  

## 必须遵守的规则  
- 仅抓取您被授权访问的内容  
- 遵守网站的robots.txt文件和服务条款（ToS）  
- 在大规模爬取时设置延迟（`download_delay`）  
- 未经许可不得绕过付费墙或身份验证机制  
- 绝对不要抓取个人或敏感信息  

## 参考资料  
- `references/mcp-setup.md` — MCP配置详细指南  
- `references/anti-bot.md` — 反机器人攻击策略  
- `references/proxy-rotation.md` — 代理设置与轮换方法  
- `references/spider-recipes.md` — 高级爬取技巧  
- `references/api-reference.md` — API快速参考  
- `references/links.md` — 官方文档链接  

## 示例脚本  
- `scripts/scrapling_scrape.py` — 用于一次性快速抓取数据  
- `scripts/scrapling_smoke_test.py` — 用于测试网络连接和检测机器人攻击的脚本