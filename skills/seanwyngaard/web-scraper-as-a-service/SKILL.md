---
name: web-scraper-as-a-service
description: 构建适用于客户端的网页爬虫，能够生成结构清晰、数据格式统一的结果。适用于为客户开发爬虫工具、从网站中提取数据，或交付完整的爬虫项目。
argument-hint: "[target-url-or-brief]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebFetch, WebSearch
---

# 作为服务的网页爬虫

我们将爬虫任务从简单的请求转化为可交付的完整项目。我们负责生成爬虫脚本、运行爬虫、清洗数据，并将所有结果打包交付给客户。

## 使用方法

```
/web-scraper-as-a-service "Scrape all products from example-store.com — need name, price, description, images. CSV output."
/web-scraper-as-a-service https://example.com --fields "title,price,rating,url" --format csv
/web-scraper-as-a-service brief.txt
```

## 爬虫生成流程

### 第一步：分析目标网站

在编写任何代码之前，请执行以下操作：

1. **获取目标网站的URL**，以了解页面结构。
2. **识别以下信息**：
   - 该网站是由服务器生成的静态HTML页面，还是由客户端生成的JavaScript/单页应用程序（SPA）？
   - 网站采取了哪些反爬虫措施？（如Cloudflare、验证码、请求速率限制等）
   - 分页方式（URL参数、无限滚动、加载更多按钮等）
   - 数据结构（产品卡片、表格行、列表项等）
   - 预计的数据量（总页数/项目数量）
3. **选择合适的工具**：
   - 如果网站使用静态HTML：使用Python + `requests` + `BeautifulSoup`
   - 如果网站使用JavaScript生成内容：使用Python + `playwright`
   - 如果网站提供API：直接调用API（检查API请求的格式）

### 第二步：构建爬虫脚本

在`scraper/`目录下生成一个完整的Python脚本：

```
scraper/
  scrape.py           # Main scraper script
  requirements.txt    # Dependencies
  config.json         # Target URLs, fields, settings
  README.md           # Setup and usage instructions for client
```

`scrape.py`脚本必须包含以下内容：

```python
# Required features in every scraper:

# 1. Configuration
import json
config = json.load(open('config.json'))

# 2. Rate limiting (ALWAYS — be respectful)
import time
DELAY_BETWEEN_REQUESTS = 2  # seconds, adjustable in config

# 3. Retry logic
MAX_RETRIES = 3
RETRY_DELAY = 5

# 4. User-Agent rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
    # ... at least 5 user agents
]

# 5. Progress tracking
print(f"Scraping page {current}/{total} — {items_collected} items collected")

# 6. Error handling
# - Log errors but don't crash on individual page failures
# - Save progress incrementally (don't lose data on crash)
# - Write errors to error_log.txt

# 7. Output
# - Save data incrementally (append to file, don't hold in memory)
# - Support CSV and JSON output
# - Clean and normalize data before saving

# 8. Resume capability
# - Track last successfully scraped page/URL
# - Can resume from where it left off if interrupted
```

### 第三步：数据清洗

爬取数据后，对数据进行清洗：

1. **去除重复数据**（根据唯一标识符或复合键进行去重）
2. **规范文本格式**（去除多余的空白字符，修复编码问题，保持大小写一致）
3. **验证数据**（确保必填字段不为空，价格为数字类型，URL格式正确）
4. **统一数据格式**（日期格式化为ISO 8601，货币单位统一）
5. **生成数据质量报告**：
   ```
   Data Quality Report
   ───────────────────
   Total records: 2,487
   Duplicates removed: 13
   Empty fields filled: 0
   Fields with issues: price (3 records had non-numeric values — cleaned)
   Completeness: 99.5%
   ```

### 第四步：生成客户可交付的成果文件

生成一个完整的交付文件包：

```
delivery/
  data.csv                    # Clean data in requested format
  data.json                   # JSON alternative
  data-quality-report.md      # Quality metrics
  scraper-documentation.md    # How the scraper works
  README.md                   # Quick start guide
```

`scraper-documentation.md`文件应包含以下内容：
- 爬取了哪些数据以及来源
- 收集到的记录数量
- 数据字段及其说明
- 重新运行爬虫的方法
- 已知的限制因素
- 爬取日期

### 第五步：将结果呈现给客户

向客户展示以下信息：
1. **总结**：从Y个页面中爬取了X条记录，数据质量为Z%
2. **样本数据**：输出的前5条记录
3. **文件存放位置**：交付文件的保存路径
4. **给客户的注意事项**：关于数据的相关说明

## 爬虫模板

根据目标网站类型，使用相应的模板：

### 电子商务产品爬虫
字段：名称、价格、原价、折扣、描述、图片、类别、商品编号（sku）、评分、评论数量、库存状态、网址

### 房地产列表
字段：地址、价格、卧室数量、浴室数量、建筑面积（平方英尺）、地块面积、房源类型、代理信息、描述、图片、网址

### 招聘信息
字段：职位名称、公司名称、工作地点、薪资范围、职位类型、职位描述、任职要求、发布日期、网址

### 商业/机构列表
字段：企业名称、地址、电话号码、官方网站、所属类别、评分、评论数量、营业时间、企业描述

### 新闻/博客文章
字段：标题、作者、发布日期、文章内容、标签、网址、图片

## 伦理爬虫准则

1. **始终遵守robots.txt文件**——在爬取前先查看该文件。
2. **遵守请求速率限制**——每次请求之间至少等待2秒。
3. **正确设置User-Agent**——使用真实但合理的User-Agent字符串。
4. **不要爬取个人隐私信息**（如电子邮件、电话号码），除非客户明确授权且这些信息是公开可获取的。
5. **缓存爬取结果**——避免不必要的重复请求。
6. **阅读服务条款**——如果网站的服务条款禁止爬取，请告知客户。