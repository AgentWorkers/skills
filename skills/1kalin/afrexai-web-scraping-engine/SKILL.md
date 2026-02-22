---
name: Web Scraping & Data Extraction Engine
description: 完整的网页抓取方法论——包括法律合规性、架构设计、反检测机制、数据管道以及生产环境下的运营管理。适用于构建网页抓取工具、提取网页数据、监控竞争对手信息或大规模自动化数据收集的场景。
---
# 网页抓取与数据提取引擎

## 快速健康检查（先运行此检查）

对你的抓取操作进行评分（每项2分）：

| 指标 | 合规 | 不合规 |
|--------|---------|-----------|
| 合法性 | 检查了robots.txt文件，阅读了服务条款 | 盲目抓取数据 |
| 架构 | 工具与网站复杂度相匹配 | 对于静态HTML使用Puppeteer |
| 防检测措施 | 旋转代理IP、设置延迟、使用多种代理指纹 | 使用单一IP地址，无延迟 |
| 数据质量 | 有数据验证和去重流程 | 仅保存原始数据，未进行清洗 |
| 错误处理 | 有重试逻辑和断路器 | 在遇到403错误时直接崩溃 |
| 监控 | 跟踪成功率并设置警报 | 无法监控抓取情况 |
| 存储 | 数据结构化、去重、有版本控制 | 保存为扁平文件，存在重复数据 |
| 安排抓取 | 频率合适，避开高峰时段 | 在工作时间频繁抓取 |

**总分：/16** → 12分以上：可投入生产使用 | 8-11分：需要改进 | 8分以下：停止当前方案并重新设计 |

---

## 第1阶段：法律与伦理基础

### 抓取前的合规性检查清单

```yaml
compliance_brief:
  target_domain: ""
  date_assessed: ""
  
  robots_txt:
    checked: false
    target_paths_allowed: false
    crawl_delay_specified: ""
    ai_bot_rules: ""  # Many sites now block AI crawlers specifically
    
  terms_of_service:
    reviewed: false
    scraping_mentioned: false
    scraping_prohibited: false
    api_available: false
    api_sufficient: false
    
  data_classification:
    type: ""  # public-factual | public-personal | behind-auth | copyrighted
    contains_pii: false
    pii_types: []  # name, email, phone, address, photo
    gdpr_applies: false  # EU residents' data
    ccpa_applies: false  # California residents' data
    
  legal_risk: ""  # low | medium | high | do-not-scrape
  decision: ""  # proceed | use-api | request-permission | abandon
  justification: ""
```

### 法律环境快速参考

| 情况 | 风险等级 | 关键案例 |
|----------|-----------|--------------|
| 公开数据，无需登录，robots.txt允许抓取 | 低风险 | hiQ诉LinkedIn案（2022年） |
| 公开数据，robots.txt禁止抓取 | 中等风险 | Meta诉Bright Data案（2024年） |
| 数据需要登录才能获取 | 高风险 | Van Buren诉US案（2021年），CFAA法规 |
| 未经同意收集个人数据 | 高风险 | GDPR第6条，CCPA第1798.100条 |
| 重新发布受版权保护的内容 | 高风险 | 版权法第106条 |
| 价格/产品比较 | 低风险 | eBay诉Bidder's Edge案（合理使用原则） |
| 学术/研究用途 | 低至中等风险 | 视具体司法管辖区而定 |
| 规避反爬虫措施 | 高风险 | CFAA法规视为“超出授权范围”

### 决策规则

1. **是否有API可用且能满足你的需求？** → 始终优先使用API。
2. **robots.txt是否禁止抓取？** → 除非获得书面许可，否则必须遵守。
3. **数据需要登录才能获取？** → 未经明确授权不得抓取。
4. **数据是否包含个人身份信息（PII）？** → 在收集前必须遵守GDPR/CCPA法规。
5. **内容是否受版权保护？** → 仅提取事实或数据点，不得获取完整内容。
6. **网站是否明确禁止抓取？** → 请求许可或寻找其他数据来源。

### 2025年及以后的AI爬虫注意事项

许多网站现在专门阻止AI相关的爬虫：

```
# Common AI bot blocks in robots.txt
User-agent: GPTBot
User-agent: ChatGPT-User
User-agent: Google-Extended
User-agent: CCBot
User-agent: anthropic-ai
User-agent: ClaudeBot
User-agent: Bytespider
User-agent: PerplexityBot
```

**规则**：如果数据用于AI训练，请检查是否存在以下禁止条款。

---

## 第2阶段：架构选择

### 工具选择矩阵

| 工具/方法 | 适用场景 | 速度 | 对JavaScript的支持 | 复杂度 | 成本 |
|---------------|----------|-------|------------|------------|------|
| HTTP客户端（requests/axios） | 静态HTML、API | ⚡⚡⚡ | ❌ | 低 | 免费 |
| Beautiful Soup / Cheerio | 静态HTML解析 | ⚡⚡⚡ | ❌ | 低 | 免费 |
| Scrapy | 大规模结构化抓取 | ⚡⚡⚡ | 需安装插件 | 中等 | 免费 |
| Playwright / Puppeteer | 支持JavaScript渲染的网站、单页应用（SPA）、交互式网站 | ⚡ | ✅ | 中等 | 免费 |
| Selenium | 传统浏览器自动化工具 | ⚡ | ✅ | 高成本 | 免费 |
| Crawlee | 混合型抓取工具（HTTP + 浏览器备用方案） | ⚡⚡ | ✅ | 中等 | 免费 |
| Firecrawl / ScrapingBee | 提供反爬虫解决方案 | ⚡⚡ | ✅ | 低成本 | 付费 |
| Bright Data / Oxylabs | 企业级工具，支持代理和浏览器自动化 | ⚡⚡ | ✅ | 低成本 | 付费 |

### 架构决策树

```
Is the content in the initial HTML source?
├── YES → Is the site structure consistent?
│   ├── YES → Static scraper (requests + BeautifulSoup/Cheerio)
│   └── NO → Scrapy with custom parsers
└── NO → Does the page require user interaction?
    ├── YES → Playwright/Puppeteer with interaction scripts
    └── NO → Playwright in non-interactive mode
        └── At scale (>10K pages)? → Crawlee (hybrid mode)
            └── Heavy anti-bot? → Managed service (Firecrawl/ScrapingBee)
```

### 架构简要说明（YAML格式）

```yaml
scraping_project:
  name: ""
  objective: ""  # What data, why, how often
  
  targets:
    - domain: ""
      pages_estimated: 0
      rendering: "static" | "javascript" | "spa"
      anti_bot: "none" | "basic" | "cloudflare" | "advanced"
      rate_limit: ""  # requests per second safe limit
      
  tool_selected: ""
  justification: ""
  
  data_schema:
    fields: []
    output_format: ""  # json | csv | database
    
  schedule:
    frequency: ""  # once | hourly | daily | weekly
    preferred_time: ""  # off-peak for target timezone
    
  infrastructure:
    proxy_needed: false
    proxy_type: ""  # residential | datacenter | mobile
    storage: ""
    monitoring: ""
```

---

## 第3阶段：请求工程

### HTTP请求最佳实践

```python
# Python example — production request pattern
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()

# Retry strategy
retry = Retry(
    total=3,
    backoff_factor=1,      # 1s, 2s, 4s
    status_forcelist=[429, 500, 502, 503, 504],
    respect_retry_after_header=True
)
session.mount("https://", HTTPAdapter(max_retries=retry))

# Realistic headers
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Cache-Control": "no-cache",
})
```

### 请求头轮换策略

为了防止被识别，请轮换以下请求头：

| 请求头 | 轮换池大小 | 备注 |
|--------|-------------------|-------|
| User-Agent | 20-50个真实的浏览器User-Agent | 根据操作系统分布选择 |
| Accept-Language | 5-10种语言组合 | 根据代理服务器地理位置选择 |
| Sec-Ch-Ua | 与User-Agent匹配 | 例如Chrome/Edge/Brave浏览器 |
| Referer | 每次请求随机变化 | 可根据上一页或搜索引擎设置 |
| ...

### 速率限制规则

| 网站类型 | 安全延迟时间 | 过激的延迟时间（风险较高） |
|-----------|-----------|-------------------|
| 小型企业网站 | 5-10秒 | 2-3秒 |
| 中型网站 | 2-5秒 | 1-2秒 |
| 大型平台（如Amazon） | 3-5秒 | 1秒 |
| API接口 | 遵循API文档规定 | 绝不超出规定 |
| robots.txt规定的抓取延迟 | 必须严格遵守 | 绝不低于规定的延迟时间 |

**规则：**
1. 始终遵守robots.txt文件中的`Crawl-delay`设置。
2. 添加随机延迟（±30%）以避免被识别。
3. 在工作时间对小型网站降低抓取速度。
4. 重视`Retry-After`头部的设置——它们具有实际意义。
5. 如果遇到429错误，应指数级增加延迟时间（每次翻倍）。

---

## 第4阶段：解析与数据提取

### CSS选择器策略（优先顺序）

1. **数据属性**：`[data-product-id]`, `[data-price]`（最稳定）
2. **语义ID**：`#product-title`, `#price`（相对稳定）
3. **ARIA属性**：`[aria-label="Price"]`（提高可访问性）
4. **语义HTML元素**：`article`, `main`, `nav`（结构化元素）
5. **类名**：`.product-card`（可能因页面设计变更而改变）
6. **XPath定位**：`//div[3]/span[2]`（最后手段）

### 数据提取模式

**优先提取结构化数据**——在编写CSS选择器之前，请先确认数据结构：

```python
# 1. Check JSON-LD (best source — structured, clean)
import json
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, 'html.parser')
for script in soup.find_all('script', type='application/ld+json'):
    data = json.loads(script.string)
    # Often contains: Product, Article, Organization, etc.

# 2. Check Open Graph meta tags
og_title = soup.find('meta', property='og:title')
og_price = soup.find('meta', property='product:price:amount')

# 3. Check microdata
items = soup.find_all(itemtype=True)

# 4. Fall back to CSS selectors only if above are empty
```

### 表格数据提取方法：

```python
import pandas as pd

# Quick table extraction
tables = pd.read_html(html)  # Returns list of DataFrames

# For complex tables with merged cells
def extract_table(soup, selector):
    table = soup.select_one(selector)
    headers = [th.get_text(strip=True) for th in table.select('thead th')]
    rows = []
    for tr in table.select('tbody tr'):
        cells = [td.get_text(strip=True) for td in tr.select('td')]
        rows.append(dict(zip(headers, cells)))
    return rows
```

### 分页处理：

```python
# Pattern 1: Next button
while True:
    # ... scrape current page ...
    next_link = soup.select_one('a.next-page, [rel="next"], .pagination .next a')
    if not next_link or not next_link.get('href'):
        break
    url = urljoin(base_url, next_link['href'])
    
# Pattern 2: API pagination (infinite scroll sites)
page = 1
while True:
    resp = session.get(f"{api_url}?page={page}&limit=50")
    data = resp.json()
    if not data.get('results'):
        break
    # ... process results ...
    page += 1

# Pattern 3: Cursor-based
cursor = None
while True:
    params = {"limit": 50}
    if cursor:
        params["cursor"] = cursor
    resp = session.get(api_url, params=params)
    data = resp.json()
    # ... process ...
    cursor = data.get('next_cursor')
    if not cursor:
        break
```

### JavaScript渲染的内容处理

```python
# Playwright pattern for JS-rendered pages
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 ...",
    )
    page = context.new_page()
    
    # Block unnecessary resources (speed + stealth)
    page.route("**/*.{png,jpg,jpeg,gif,svg,woff,woff2}", 
               lambda route: route.abort())
    
    page.goto(url, wait_until="networkidle")
    
    # Wait for specific content (better than arbitrary sleep)
    page.wait_for_selector('[data-product-id]', timeout=10000)
    
    # Extract after JS rendering
    content = page.content()
    # ... parse with BeautifulSoup/Cheerio ...
    
    browser.close()
```

---

## 第5阶段：反检测与隐蔽策略

### 网站常用的检测方法及应对措施

| 检测方法 | 应对策略 |
|--------|-----------------|------------|
| IP地址识别 | 使用黑名单或数据中心范围过滤代理IP |
| 请求频率 | 对同一IP的请求进行限制并添加延迟 |
| TLS指纹识别 | 使用真实的浏览器或curl工具模拟请求 |
| 浏览器特征识别 | 使用Playwright工具并配置隐蔽功能 |
| JavaScript挑战 | 使用Cloudflare的Turnstile或hCaptcha |
| Cookie/会话管理 | 确保Cookie存在且会话信息完整 |
| 浏览行为检测 | 模拟自然浏览行为 |
| 鼠标/键盘操作检测 | 避免发送交互信号 |
| 请求头一致性 | 确保请求头与User-Agent匹配 |

### 代理策略

```yaml
proxy_strategy:
  # Tier 1: Free/Datacenter (for non-protected sites)
  basic:
    type: "datacenter"
    cost: "$1-5/GB"
    success_rate: "60-80%"
    use_for: "APIs, small sites, no anti-bot"
    
  # Tier 2: Residential (for most protected sites)
  standard:
    type: "residential"
    cost: "$5-15/GB"
    success_rate: "90-95%"
    use_for: "Cloudflare, major platforms"
    rotation: "per-request or sticky 10min"
    
  # Tier 3: Mobile/ISP (for maximum stealth)
  premium:
    type: "mobile"
    cost: "$15-30/GB"
    success_rate: "95-99%"
    use_for: "Aggressive anti-bot, social media"
    
  rules:
    - Start with cheapest tier, escalate only on blocks
    - Match proxy geo to target audience geo
    - Rotate on 403/429, not every request
    - Use sticky sessions for multi-page scrapes
    - Monitor proxy health — remove slow/blocked IPs
```

### Playwright的隐蔽配置

```python
# Essential stealth for Playwright
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=[
            '--disable-blink-features=AutomationControlled',
            '--disable-features=IsolateOrigins,site-per-process',
        ]
    )
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="en-US",
        timezone_id="America/New_York",
        geolocation={"latitude": 40.7128, "longitude": -74.0060},
        permissions=["geolocation"],
    )
    
    # Remove automation indicators
    page = context.new_page()
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
    """)
```

### 如何绕过Cloudflare的反爬虫机制

```
Cloudflare detected?
├── JS Challenge only → Playwright with stealth + residential proxy
├── Turnstile CAPTCHA → Managed service (ScrapingBee/Bright Data)
├── Under Attack Mode → Wait, try later, or managed service
└── WAF blocking → Different approach needed
    ├── Check for API endpoints (network tab)
    ├── Check for mobile app API
    └── Consider if data is available elsewhere
```

---

## 第6阶段：数据管道与数据质量

### 数据验证规则

```python
# Validation pattern — validate BEFORE storing
from dataclasses import dataclass, field
from typing import Optional
import re
from datetime import datetime

@dataclass
class ScrapedProduct:
    url: str
    title: str
    price: Optional[float]
    currency: str = "USD"
    scraped_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def validate(self) -> list[str]:
        errors = []
        if not self.url.startswith('http'):
            errors.append("Invalid URL")
        if not self.title or len(self.title) < 3:
            errors.append("Title too short or missing")
        if self.price is not None and self.price < 0:
            errors.append("Negative price")
        if self.price is not None and self.price > 1_000_000:
            errors.append("Price suspiciously high — verify")
        if self.currency not in ("USD", "EUR", "GBP", "BTC"):
            errors.append(f"Unknown currency: {self.currency}")
        return errors
```

### 数据去重策略

| 方法 | 适用场景 | 实现方式 |
|--------|------------|----------------|
| 基于URL的去重 | 对于每个URL唯一的页面 | 对URL进行哈希处理 |
| 内容哈希 | 对于内容相同但URL不同的页面 | 使用MD5/SHA256对关键字段进行哈希 |
| 模糊匹配 | 对于内容相似的页面 | 使用Jaccard相似度大于0.85 |
| 综合键值对 | 对于多个字段都不同的页面 | 使用域名+产品ID+变体进行哈希 |

```python
import hashlib

def dedup_key(item: dict, fields: list[str]) -> str:
    """Generate dedup key from selected fields."""
    values = "|".join(str(item.get(f, "")) for f in fields)
    return hashlib.sha256(values.encode()).hexdigest()

# Usage
seen = set()
for item in scraped_items:
    key = dedup_key(item, ["url", "product_id"])
    if key not in seen:
        seen.add(key)
        clean_items.append(item)
```

### 数据清洗流程

```
Raw HTML → Parse → Extract → Validate → Clean → Deduplicate → Store
                                ↓
                          Quarantine (failed validation)
```

**常见的数据清洗操作：**

| 问题 | 解决方案 |
|---------|----------|
| HTML实体（如`&`） | 使用`html.unescape()`函数去除 |
| 多余空格 | 使用`" ".join(text.split())`去除 |
| Unicode编码问题 | 使用`unicodedata.normalize('NFKD', text)`处理 |
| 文本中的价格（如“$49.99”） | 使用正则表达式`r'[\$£€]?([\d,]+\.?\d*)'`提取 |
| 不同日期格式 | 使用`dateutil.parser.parse()`并设置`dayfirst`参数 |
| 相对URL | 使用`urllib.parse.urljoin(base, relative)`处理 |
| 编码问题 | 使用`chardet.detect()`进行编码检测 |

---

## 第7阶段：存储与导出

### 存储策略选择

| 数据量 | 抓取频率 | 数据查询需求 | 推荐存储方式 |
|--------|-----------|-------------|----------------|
| <10K条记录 | 一次性抓取 | 无需特殊存储 | JSON/CSV文件 |
| <10K条记录 | 频繁抓取 | 使用简单查询 | SQLite |
| 10K-1M条记录 | 频繁抓取 | 需进行复杂查询 | PostgreSQL |
| 1M条以上记录 | 持续抓取 | 用于数据分析 | 使用PostgreSQL并设置分区 |
| 仅追加日志 | 持续抓取 | 适用于时间序列数据 | ClickHouse / TimescaleDB |

### SQLite存储示例（最常用）

```python
import sqlite3
import json
from datetime import datetime

def init_db(path="scraper_data.db"):
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            url TEXT UNIQUE,
            data JSON NOT NULL,
            scraped_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT,
            checksum TEXT
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_url ON items(url)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_scraped ON items(scraped_at)")
    return conn

def upsert(conn, url, data, checksum):
    conn.execute("""
        INSERT INTO items (url, data, checksum) VALUES (?, ?, ?)
        ON CONFLICT(url) DO UPDATE SET
            data = excluded.data,
            updated_at = datetime('now'),
            checksum = excluded.checksum
        WHERE items.checksum != excluded.checksum
    """, (url, json.dumps(data), checksum))
    conn.commit()
```

### 数据导出格式

```python
# CSV export
import csv
def to_csv(items, path, fields):
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(items)

# JSON Lines (best for large datasets — streaming)
def to_jsonl(items, path):
    with open(path, 'w') as f:
        for item in items:
            f.write(json.dumps(item) + '\n')

# Incremental export (only new/changed since last export)
def export_since(conn, last_export_time):
    cursor = conn.execute(
        "SELECT data FROM items WHERE scraped_at > ? OR updated_at > ?",
        (last_export_time, last_export_time)
    )
    return [json.loads(row[0]) for row in cursor]
```

---

## 第8阶段：错误处理与系统弹性

### 错误分类与应对措施

| HTTP状态码 | 含义 | 处理方式 |
|-----------|---------|--------|
| 200 | 成功 | 正常处理 |
| 301/302 | 重定向 | 遵循重定向规则（最多尝试5次） |
| 403 | 被禁止/被封锁 | 旋转代理IP，降低抓取频率 |
| 404 | 未找到 | 记录错误，跳过该请求，标记URL为无效 |
| 429 | 被限制访问 | 遵循重试规则，每次尝试间隔时间加倍 |
| 500-504 | 服务器错误 | 重试3次 |
| 连接超时 | 网络问题 | 更换代理IP |
| SSL错误 | 证书问题 | 记录错误，进一步排查 |

### 断路器机制

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=300):
        self.failures = 0
        self.threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.last_failure = 0
        self.state = "closed"  # closed | open | half-open
    
    def record_failure(self):
        self.failures += 1
        self.last_failure = time.time()
        if self.failures >= self.threshold:
            self.state = "open"
            # Alert: "Circuit open — too many failures"
    
    def record_success(self):
        self.failures = 0
        self.state = "closed"
    
    def can_proceed(self):
        if self.state == "closed":
            return True
        if self.state == "open":
            if time.time() - self.last_failure > self.reset_timeout:
                self.state = "half-open"
                return True  # Try one request
            return False
        return True  # half-open: allow attempt
```

### 检查点与恢复机制

```python
import json
from pathlib import Path

class Checkpointer:
    def __init__(self, path="checkpoint.json"):
        self.path = Path(path)
        self.state = self._load()
    
    def _load(self):
        if self.path.exists():
            return json.loads(self.path.read_text())
        return {"completed_urls": [], "last_page": 0, "cursor": None}
    
    def save(self):
        self.path.write_text(json.dumps(self.state))
    
    def is_done(self, url):
        return url in self.state["completed_urls"]
    
    def mark_done(self, url):
        self.state["completed_urls"].append(url)
        if len(self.state["completed_urls"]) % 50 == 0:
            self.save()  # Periodic save
```

---

## 第9阶段：监控与运营维护

### 爬虫健康状况监控仪表盘

```yaml
dashboard:
  real_time:
    - metric: "requests_per_minute"
      alert_if: "> 60 for small sites"
    - metric: "success_rate"
      alert_if: "< 90%"
    - metric: "avg_response_time_ms"
      alert_if: "> 5000"
    - metric: "blocked_rate"
      alert_if: "> 10%"
      
  per_run:
    - metric: "pages_scraped"
    - metric: "items_extracted"
    - metric: "items_validated"
    - metric: "items_deduplicated"
    - metric: "new_items"
    - metric: "updated_items"
    - metric: "errors_by_type"
    - metric: "run_duration"
    - metric: "proxy_cost"
    
  weekly:
    - metric: "data_freshness"
      description: "% of records updated in last 7 days"
    - metric: "site_structure_changes"
      description: "Selectors that stopped matching"
    - metric: "total_cost"
      description: "Proxy + compute + storage"
```

### 系统故障检测

当网站重新设计或选择器失效时，需及时发现：

```python
def health_check(results: list[dict], expected_fields: list[str]) -> dict:
    """Check if scraper is still extracting correctly."""
    total = len(results)
    if total == 0:
        return {"status": "CRITICAL", "message": "Zero results — likely broken"}
    
    field_coverage = {}
    for field in expected_fields:
        filled = sum(1 for r in results if r.get(field))
        coverage = filled / total
        field_coverage[field] = coverage
        
    issues = []
    for field, coverage in field_coverage.items():
        if coverage < 0.5:
            issues.append(f"{field}: {coverage:.0%} fill rate (expected >50%)")
    
    if issues:
        return {"status": "WARNING", "issues": issues}
    return {"status": "OK", "field_coverage": field_coverage}
```

### 运营手册

**每日操作：**
- 检查每个目标域名的成功率 |
- 查看错误日志，寻找新的问题模式 |
- 验证数据更新情况

**每周操作：**
- 比较抓取数量与基准值（下降超过20%需调查）
- 监控代理使用情况 |
- 随机检查10条记录的准确性

**每月操作：**
- 完整验证选择器的有效性 |
- 检查合规性（如robots.txt文件更新、服务条款变更）
- 优化成本 |
- 从抓取队列中移除无效的URL

---

## 第10阶段：常见抓取场景

### 场景1：电子商务价格监控

```yaml
use_case: "Track competitor prices daily"
tool: "requests + BeautifulSoup"
schedule: "Daily at 03:00 UTC (off-peak)"
targets: ["competitor-a.com/products", "competitor-b.com/api"]
data:
  - product_id
  - product_name
  - price
  - currency
  - in_stock
  - scraped_at
storage: "SQLite with price history"
alerts: "Price change > 10% → notify"
```

### 场景2：招聘信息聚合

```yaml
use_case: "Aggregate job listings from multiple boards"
tool: "Scrapy with per-site spiders"
schedule: "Every 6 hours"
targets: ["board-a.com", "board-b.com", "board-c.com"]
data:
  - title
  - company
  - location
  - salary_range
  - posted_date
  - url
  - source
dedup: "Hash(title + company + location)"
storage: "PostgreSQL"
```

### 场景3：新闻与内容监控

```yaml
use_case: "Monitor industry news mentions"
tool: "requests + RSS feeds (preferred) + web fallback"
schedule: "Every 30 minutes"
approach:
  1: "RSS/Atom feeds (fastest, cleanest)"
  2: "Google News RSS for topic"
  3: "Direct scraping if no feed"
data:
  - headline
  - source
  - url
  - published_at
  - snippet
  - sentiment
alerts: "Keyword match → immediate notification"
```

### 场景4：社交媒体情报收集

```yaml
use_case: "Track brand mentions and sentiment"
tool: "Official APIs (always) + web search fallback"
rules:
  - NEVER scrape social platforms directly — use APIs
  - Twitter/X: Official API ($100/mo basic)
  - Reddit: Official API (free tier available)
  - LinkedIn: No scraping (aggressive legal action)
  - Instagram: Official API only (Meta Business)
fallback: "Brave/Google search for public mentions"
```

### 场景5：房地产信息抓取

```yaml
use_case: "Track property listings and prices"
tool: "Playwright (most listing sites are JS-heavy)"
schedule: "Daily"
challenges:
  - Heavy JavaScript rendering
  - Anti-bot measures (Cloudflare common)
  - Frequent layout changes
  - Map-based results
approach: "API endpoint discovery via network tab first"
```

---

## 第11阶段：扩展策略

### 并发抓取架构

```
Single machine (small scale):
├── asyncio + aiohttp (Python) → 50-200 concurrent requests
├── Worker pool (ThreadPoolExecutor) → 10-50 threads
└── Scrapy reactor → Built-in concurrency

Multi-machine (large scale):
├── URL queue: Redis / RabbitMQ / SQS
├── Workers: Multiple Scrapy/custom workers
├── Results: Shared PostgreSQL / S3
└── Coordinator: Celery / custom scheduler
```

### 成本优化方法

| 方法 | 影响 | 实施方式 |
|-------|--------|-----|
| 使用HTTP客户端而非浏览器 | 成本降低10-50倍 | 始终优先使用HTTP客户端 |
| 避免加载图片/CSS/字体 | 节省60-80%的带宽 | 使用DNS缓存 |
| 压缩响应数据 | 节省50-70%的带宽 | 在请求头中设置`Accept-Encoding: gzip, br` |
| 智能调度 | 避免重复抓取 | 在需要时才进行抓取 |
| 选择合适的代理类型 | 根据网站类型选择合适的代理 | 对于简单网站，避免使用住宅区代理 |

---

## 第12阶段：高级抓取技巧

### API发现（网络请求分析）

在构建抓取工具之前，检查网站是否提供隐藏的API接口：

1. 打开开发工具 → 网络选项卡
2. 过滤XHR/Fetch类型的请求 |
3. 浏览网站，点击“加载更多”按钮，过滤和排序数据 |
4. 寻找JSON格式的响应数据 |
| 大多数单页应用（SPA）通过REST/GraphQL API提供数据 |

**常见的隐藏API接口示例：**
- `/api/v1/products?page=1&limit=20`
- `/graphql`接口（带查询参数）
- `/wp-json/wp/v2/posts`（WordPress的API）

### 无头浏览器优化

```python
# Minimize browser resource usage
context = browser.new_context(
    viewport={"width": 1280, "height": 720},
    java_script_enabled=True,  # Only if needed
    has_touch=False,
    is_mobile=False,
)

# Block resource types you don't need
page.route("**/*", lambda route: (
    route.abort() if route.request.resource_type in 
    ["image", "stylesheet", "font", "media"] 
    else route.continue_()
))
```

### 在需要登录的网站进行抓取

```python
# When authorized to scrape behind login
# ALWAYS use session-based auth, never store passwords in code

# Pattern: Login once, reuse session
session = requests.Session()
login_resp = session.post("https://example.com/login", data={
    "username": os.environ["SCRAPE_USER"],
    "password": os.environ["SCRAPE_PASS"],
})
assert login_resp.ok, "Login failed"

# Session cookies are now stored — use for subsequent requests
data_resp = session.get("https://example.com/api/data")
```

### 避免重复抓取

### 数据质量评分标准（0-100分）

| 评估维度 | 权重 | 评估内容 |
|-----------|--------|---------------|
| 合法性 | 20% | 是否遵守法律法规、处理个人身份信息、保留审计记录 |
| 数据质量 | 20% | 数据验证、准确性、完整性、更新频率 |
| 系统弹性 | 15% | 错误处理能力、重试机制、断路器设置 |
| 防检测措施 | 15% | 代理IP轮换、使用多种代理、设置合理的延迟 |
| 架构 | 10% | 选择合适的工具、代码整洁度、模块化设计 |
| 监控能力 | 10% | 成功率、故障检测能力、警报机制 |
| 性能 | 5% | 抓取速度、成本效率、资源使用情况 |
| 文档编写 | 5% | 操作手册的完整性、数据结构文档、合规性评估 |

**评分标准：** 90分以上：优秀 | 75-89分：良好 | 60-74分：需要改进 | 60分以下：需要重新设计 |

---

## 10个常见错误

| 缺误编号 | 错误内容 | 解决方法 |
|---|---------|-----|
| 1 | 不检查robots.txt文件 | 必须首先检查robots.txt文件，这是法律保障 |
| 2 | 不设置延迟 | 所有延迟时间都设置为固定值，添加30%的随机延迟 |
| 3 | 不进行数据验证 | 在存储前必须验证所有数据 |
| 4 | 对静态HTML使用浏览器 | 使用HTTP客户端通常更快更便宜 |
| 5 | 使用单一IP地址抓取 | 任何需要频繁抓取的数据源都应使用代理IP轮换 |
| 6 | 不检测系统故障 | 需要监控抓取次数和数据填充率 |
| 7 | 仅保存原始HTML | 应立即提取数据并进行结构化处理 |
| 8 | 未设置检查点/恢复机制 | 长时间运行的抓取任务必须能够恢复 |
| 9 | 忽略结构化数据 | 使用JSON-LD或microdata格式比CSS选择器更有效 |
| 10 | 在有API的情况下仍使用传统抓取方式 | 必须先检查是否存在API接口 |

---

## 5个特殊情况

1. **单页应用（React/Vue/Angular）**：必须使用浏览器渲染或查找隐藏的API接口。优先选择API接口，因为它们更快更可靠。
2. **无限滚动页面**：拦截加载更多内容的XHR/fetch请求。只有在必要时才模拟滚动行为。API接口通常支持`page`或`offset`参数。
3. **遇到CAPTCHAs**：如果遇到CAPTCHAs，说明抓取行为过于激进。首先尝试降低抓取频率；如果CAPTCHAs无法绕过，可以考虑使用专业服务（如2Captcha或Anti-Captcha）或重新设计抓取策略。
4. **动态类名**：对于使用CSS模块或Tailwind框架的网站，应使用数据属性、ARIA标签或文本选择器。`[dataTestId="price"]`在页面重新设计后仍然有效，而`.sc-bdVTJa`可能失效。
5. **多语言网站**：通过`html[lang]`属性识别语言。设置`Accept-Language`头部以获取所需语言。注意URL结构的变化（如`/en/`, `/de/`, 子域名）。

---

## 常用命令与咨询

1. **“我能否抓取这个网站？”** → 运行合规性检查（robots.txt文件、服务条款、数据类型）
2. **“应该使用什么工具抓取这个网站？”** → 分析网站渲染方式、反爬虫机制，推荐合适的工具 |
3. **“为这个网站开发抓取工具”** → 提供完整的架构设计和代码示例 |
4. **“我的抓取工具被屏蔽了”** | 提供反检测问题的诊断建议和代理设置建议 |
5. **“从这个网站提取数据”** | 首先检查结构化数据，再使用CSS选择器 |
6. **“如何监控这个网站的变化？”** | 提供页面分页机制的实现方法和警报设置建议 |
7. **“如何大规模抓取这些页面？”** | 提供并发抓取的架构设计和成本估算 |
8. **“如何清洗和存储抓取的数据？” | 提供数据清洗和存储的建议 |
9. **“我的抓取工具运行正常吗？” | 运行健康检查并检测系统故障 |
10. **“如何找到这个网站的API接口？” | 提供网络请求分析方法和常见API接口的查找技巧 |

---

## 其他帮助信息

1. 如需检查某个网站是否允许抓取，请运行合规性检查。
2. 为了提高抓取效率，建议优先使用HTTP客户端，并避免加载图片和CSS/字体文件。
3. 对于需要登录的网站，务必使用适当的代理策略。
4. 定期检查数据质量和准确性，并设置合理的延迟策略。
5. 为了提高系统的弹性，需要设置错误处理机制和断路器。
6. 为了确保数据质量，必须对数据进行验证和去重。
7. 为了方便存储和查询，建议使用结构化的数据格式和合适的数据库。
8. 定期监控抓取系统的运行状态，并及时处理故障。
9. 根据网站的特点选择合适的抓取策略和工具。
10. 遵循最佳实践，可以避免很多常见问题并提高抓取效率。