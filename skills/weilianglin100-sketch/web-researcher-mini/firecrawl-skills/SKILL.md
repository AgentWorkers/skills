---
name: firecrawl-cli
description: |
  Firecrawl CLI for web scraping, crawling, and search. Scrape single pages or entire websites, map site URLs, and search the web with full content extraction. Returns clean markdown optimized for LLM context. Use for research, documentation extraction, competitive intelligence, and content monitoring.
---

# Firecrawl CLI

使用 `firecrawl` CLI 可以抓取并搜索网页。Firecrawl 会返回适合大型语言模型（LLM）使用环境的优化后的 Markdown 格式数据，处理 JavaScript 的渲染逻辑，绕过常见的网页阻塞因素，并提供结构化的数据。

## 安装

检查状态、认证信息以及请求速率限制：

```bash
firecrawl --status
```

安装完成后，输出以下信息：

```
  🔥 firecrawl cli v1.0.2

  ● Authenticated via FIRECRAWL_API_KEY
  Concurrency: 0/100 jobs (parallel scrape limit)
  Credits: 500,000 remaining
```

- **并发任务数**：允许的最大并行任务数量。请在接近但不要超过此限制的情况下运行多个任务。
- **剩余 API 信用额度**：每次抓取操作都会消耗一定的信用额度。

如果尚未安装，请执行：`npm install -g firecrawl-cli`

如果用户未登录，请务必参考 [rules/install.md](rules/install.md) 中的安装说明以获取更多信息。

## 认证

如果未进行认证，请执行以下命令：

```bash
firecrawl login --browser
```

`--browser` 标志会自动打开浏览器进行认证，而无需用户手动操作。

## 文件组织结构

在工作目录中创建一个 `.firecrawl/` 文件夹（如果该文件夹尚不存在），用于存储抓取结果。如果 `.gitignore` 文件中尚未包含 `.firecrawl/` 文件，请将其添加到该文件中。在保存数据时，请始终使用 `-o` 选项，以避免数据占用过多磁盘空间：

```bash
# Search the web (most common operation)
firecrawl search "your query" -o .firecrawl/search-{query}.json

# Search with scraping enabled
firecrawl search "your query" --scrape -o .firecrawl/search-{query}-scraped.json

# Scrape a page
firecrawl scrape https://example.com -o .firecrawl/{site}-{path}.md
```

## 示例用法

```
.firecrawl/search-react_server_components.json
.firecrawl/search-ai_news-scraped.json
.firecrawl/docs.github.com-actions-overview.md
.firecrawl/firecrawl.dev.md
```

## 命令说明

### Search（搜索） - 可选择进行数据抓取的网页搜索

```bash
# Basic search (human-readable output)
firecrawl search "your query" -o .firecrawl/search-query.txt

# JSON output (recommended for parsing)
firecrawl search "your query" -o .firecrawl/search-query.json --json

# Limit results
firecrawl search "AI news" --limit 10 -o .firecrawl/search-ai-news.json --json

# Search specific sources
firecrawl search "tech startups" --sources news -o .firecrawl/search-news.json --json
firecrawl search "landscapes" --sources images -o .firecrawl/search-images.json --json
firecrawl search "machine learning" --sources web,news,images -o .firecrawl/search-ml.json --json

# Filter by category (GitHub repos, research papers, PDFs)
firecrawl search "web scraping python" --categories github -o .firecrawl/search-github.json --json
firecrawl search "transformer architecture" --categories research -o .firecrawl/search-research.json --json

# Time-based search
firecrawl search "AI announcements" --tbs qdr:d -o .firecrawl/search-today.json --json  # Past day
firecrawl search "tech news" --tbs qdr:w -o .firecrawl/search-week.json --json          # Past week

# Location-based search
firecrawl search "restaurants" --location "San Francisco,California,United States" -o .firecrawl/search-sf.json --json
firecrawl search "local news" --country DE -o .firecrawl/search-germany.json --json

# Search AND scrape content from results
firecrawl search "firecrawl tutorials" --scrape -o .firecrawl/search-scraped.json --json
firecrawl search "API docs" --scrape --scrape-formats markdown,links -o .firecrawl/search-docs.json --json
```

**搜索选项：**

| 选项 | 描述 |
|--------|-------------|
| `--limit <n>` | 最大搜索结果数量（默认值：5，最大值：100） |
| `--sources <sources>` | 以逗号分隔的来源类型：web（网页）、images（图片）、news（新闻）（默认值：web） |
| `--categories <categories>` | 以逗号分隔的类别类型：github（GitHub 文档）、research（研究资料）、pdf（PDF 文档） |
| `--tbs <value>` | 时间过滤选项：qdr:h（小时）、qdr:d（天）、qdr:w（周）、qdr:m（月）、qdr:y（年） |
| `--location <location>` | 地理定位选项（例如：“Germany”） |
| `--country <code>` | ISO 国家代码（默认值：US） |
| `--scrape` | 启用搜索结果的抓取功能 |
| `--scrape-formats <formats>` | 当 `--scrape` 选项被启用时，指定抓取数据的格式（默认值：markdown） |
| `-o, --output <path>` | 将搜索结果保存到指定文件 |

### Scrape（抓取） - 提取单页内容

```bash
# Basic scrape (markdown output)
firecrawl scrape https://example.com -o .firecrawl/example.md

# Get raw HTML
firecrawl scrape https://example.com --html -o .firecrawl/example.html

# Multiple formats (JSON output)
firecrawl scrape https://example.com --format markdown,links -o .firecrawl/example.json

# Main content only (removes nav, footer, ads)
firecrawl scrape https://example.com --only-main-content -o .firecrawl/example.md

# Wait for JS to render
firecrawl scrape https://spa-app.com --wait-for 3000 -o .firecrawl/spa.md

# Extract links only
firecrawl scrape https://example.com --format links -o .firecrawl/links.json

# Include/exclude specific HTML tags
firecrawl scrape https://example.com --include-tags article,main -o .firecrawl/article.md
firecrawl scrape https://example.com --exclude-tags nav,aside,.ad -o .firecrawl/clean.md
```

**抓取选项：**

| 选项 | 描述 |
|--------|-------------|
| `-f, --format <formats>` | 输出格式：markdown、html、rawHtml、links、screenshots、json |
| `-H, --html` | `--format html` 的简写形式 |
| `--only-main-content` | 仅提取页面主要内容 |
| `--wait-for <ms>` | 在抓取页面内容前等待指定的时间（用于处理 JavaScript 动画等） |
| `--include-tags <tags>` | 仅包含指定的 HTML 标签 |
| `--exclude-tags <tags>` | 排除指定的 HTML 标签 |
| `-o, --output <path>` | 将抓取结果保存到指定文件 |

### Crawl（爬取） - 全面爬取整个网站

```bash
# Start a crawl (returns job ID)
firecrawl crawl https://example.com

# Wait for crawl to complete
firecrawl crawl https://example.com --wait

# With progress indicator
firecrawl crawl https://example.com --wait --progress

# Check crawl status
firecrawl crawl <job-id>

# Limit pages
firecrawl crawl https://example.com --limit 100 --max-depth 3

# Crawl blog section only
firecrawl crawl https://example.com --include-paths /blog,/posts

# Exclude admin pages
firecrawl crawl https://example.com --exclude-paths /admin,/login

# Crawl with rate limiting
firecrawl crawl https://example.com --delay 1000 --max-concurrency 2

# Save results
firecrawl crawl https://example.com --wait -o crawl-results.json --pretty
```

**爬取选项：**

| 选项 | 描述 |
|--------|-------------|
| `--wait` | 等待爬取任务完成 |
| `--progress` | 在爬取过程中显示进度信息 |
| `--limit <n>` | 最大爬取页数 |
| `--max-depth <n>` | 最大爬取深度 |
| `--include-paths <paths>` | 仅爬取指定的路径 |
| `--exclude-paths <paths>` | 跳过指定的路径 |
| `--delay <ms>` | 请求之间的延迟时间 |
| `--max-concurrency <n>` | 最大并发请求数量 |

### Map（映射） - 发现网站上的所有 URL

```bash
# List all URLs (one per line)
firecrawl map https://example.com -o .firecrawl/urls.txt

# Output as JSON
firecrawl map https://example.com --json -o .firecrawl/urls.json

# Search for specific URLs
firecrawl map https://example.com --search "blog" -o .firecrawl/blog-urls.txt

# Limit results
firecrawl map https://example.com --limit 500 -o .firecrawl/urls.txt

# Include subdomains
firecrawl map https://example.com --include-subdomains -o .firecrawl/all-urls.txt
```

**映射选项：**

| 选项 | 描述 |
|--------|-------------|
| `--limit <n>` | 最大要发现的 URL 数量 |
| `--search <query>` | 根据搜索查询筛选 URL |
| `--sitemap <mode>` | 是否包含子域名、跳过子域名或仅包含主域名 |
| `--json` | 以 JSON 格式输出结果 |
| `-o, --output <path>` | 将结果保存到指定文件 |

## 信用额度使用

```bash
# Show credit usage
firecrawl credit-usage

# Output as JSON
firecrawl credit-usage --json --pretty
```

## 查看抓取文件

除非特别需要，否则切勿一次性读取整个 `firecrawl` 的输出文件（这些文件可能包含数千行数据）。建议使用 `grep`、`head` 命令或分批读取文件内容：

```bash
# Check file size and preview structure
wc -l .firecrawl/file.md && head -50 .firecrawl/file.md

# Use grep to find specific content
grep -n "keyword" .firecrawl/file.md
grep -A 10 "## Section" .firecrawl/file.md
```

## 并行处理

可以使用 `&` 符号和 `wait` 命令并行执行多个抓取任务：

```bash
# Parallel scraping (fast)
firecrawl scrape https://site1.com -o .firecrawl/1.md &
firecrawl scrape https://site2.com -o .firecrawl/2.md &
firecrawl scrape https://site3.com -o .firecrawl/3.md &
wait
```

对于大量 URL，可以使用 `xargs` 命令结合 `-P` 选项实现并行处理：

```bash
cat urls.txt | xargs -P 10 -I {} sh -c 'firecrawl scrape "{}" -o ".firecrawl/$(echo {} | md5).md"'
```

## 与其他工具的结合使用

```bash
# Extract URLs from search results
jq -r '.data.web[].url' .firecrawl/search-query.json

# Get titles from search results
jq -r '.data.web[] | "\(.title): \(.url)"' .firecrawl/search-query.json

# Count URLs from map
firecrawl map https://example.com | wc -l
```