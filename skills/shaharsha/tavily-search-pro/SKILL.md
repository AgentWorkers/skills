---
name: tavily-search-pro
slug: tavily-search-pro
description: >
  Tavily AI search platform with 5 modes: Search (web/news/finance), Extract (URL content),
  Crawl (website crawling), Map (sitemap discovery), and Research (deep research with citations).
  Use for: web search with LLM answers, content extraction, site crawling, deep research.
version: 1.0.0
author: Leo 🦁
tags: [search, tavily, web, news, finance, extract, crawl, research, api]
metadata: {"clawdbot":{"emoji":"🔎","requires":{"env":["TAVILY_API_KEY"]},"primaryEnv":"TAVILY_API_KEY","install":[{"id":"pip","kind":"pip","package":"tavily-python","label":"Install dependencies (pip)"}]}}
allowed-tools: [exec]
---

# Tavily 搜索 🔎

这是一个基于人工智能的网页搜索平台，提供五种搜索模式：搜索（Search）、提取内容（Extract）、爬取网站（Crawl）、生成站点地图（Map）以及深入研究（Research）。

## 必需条件

- 环境变量 `TAVILY_API_KEY` 必须设置。

## 配置

| 环境变量 | 默认值 | 说明 |
| --- | --- | --- |
| `TAVILY_API_KEY` | 未设置 | **必需**。Tavily 的 API 密钥。 |

请在 OpenClaw 的配置文件中设置该密钥：
```json
{
  "env": {
    "TAVILY_API_KEY": "tvly-..."
  }
}
```

## 脚本位置

```bash
python3 skills/tavily/lib/tavily_search.py <command> "query" [options]
```

---

## 命令

### search — 基本网页搜索（默认模式）

提供通用网页搜索功能，支持选择是否包含由大型语言模型（LLM）生成的答案。

```bash
python3 lib/tavily_search.py search "query" [options]
```

**示例：**
```bash
# Basic search
python3 lib/tavily_search.py search "latest AI news"

# With LLM answer
python3 lib/tavily_search.py search "what is quantum computing" --answer

# Advanced depth (better results, 2 credits)
python3 lib/tavily_search.py search "climate change solutions" --depth advanced

# Time-filtered
python3 lib/tavily_search.py search "OpenAI announcements" --time week

# Domain filtering
python3 lib/tavily_search.py search "machine learning" --include-domains arxiv.org,nature.com

# Country boost
python3 lib/tavily_search.py search "tech startups" --country US

# With raw content and images
python3 lib/tavily_search.py search "solar energy" --raw --images -n 10

# JSON output
python3 lib/tavily_search.py search "bitcoin price" --json
```

**输出格式（文本）：**
```
Answer: <LLM-synthesized answer if --answer>

Results:
  1. Result Title
     https://example.com/article
     Content snippet from the page...

  2. Another Result
     https://example.com/other
     Another snippet...
```

---

### news — 新闻搜索

专为新闻文章优化的高效搜索模式。需设置 `topic=news`。

```bash
python3 lib/tavily_search.py news "query" [options]
```

**示例：**
```bash
python3 lib/tavily_search.py news "AI regulation"
python3 lib/tavily_search.py news "Israel tech" --time day --answer
python3 lib/tavily_search.py news "stock market" --time week -n 10
```

---

### finance — 金融搜索

专为金融数据和新闻内容优化的高效搜索模式。需设置 `topic=finance`。

```bash
python3 lib/tavily_search.py finance "query" [options]
```

**示例：**
```bash
python3 lib/tavily_search.py finance "NVIDIA stock analysis"
python3 lib/tavily_search.py finance "cryptocurrency market trends" --time month
python3 lib/tavily_search.py finance "S&P 500 forecast 2026" --answer
```

---

### extract — 从 URL 中提取内容

从一个或多个 URL 中提取可读内容。

**参数：**
- `urls`：需要提取内容的 URL（位置参数）
- `--depth basic|advanced`：提取深度
- `--format markdown|text`：输出格式（默认：markdown）
- `--query "text"`：根据查询内容对提取结果进行重新排序

**示例：**
```bash
# Extract single URL
python3 lib/tavily_search.py extract "https://example.com/article"

# Extract multiple URLs
python3 lib/tavily_search.py extract "https://url1.com" "https://url2.com"

# Advanced extraction with relevance reranking
python3 lib/tavily_search.py extract "https://arxiv.org/paper" --depth advanced --query "transformer architecture"

# Text format output
python3 lib/tavily_search.py extract "https://example.com" --format text
```

**输出格式：**
```
URL: https://example.com/article
─────────────────────────────────
<Extracted content in markdown/text>

URL: https://another.com/page
─────────────────────────────────
<Extracted content>
```

---

### crawl — 爬取网站

从指定根 URL 开始爬取整个网站，并跟随其中的链接。

**参数：**
- `url`：开始爬取的根 URL
- `--depth basic|advanced`：爬取深度
- `--max-depth N`：最大链接深度（默认：2）
- `--max-breadth N`：每层的最大页面数（默认：10）
- `--limit N`：总页面数上限（默认：10）
- `--instructions "text"`：爬取时的自然语言指令
- `--select-paths p1,p2`：仅爬取指定的路径模式
- `--exclude-paths p1,p2`：跳过指定的路径模式
- `--format markdown|text`：输出格式

**示例：**
```bash
# Basic crawl
python3 lib/tavily_search.py crawl "https://docs.example.com"

# Focused crawl with instructions
python3 lib/tavily_search.py crawl "https://docs.python.org" --instructions "Find all asyncio documentation" --limit 20

# Crawl specific paths only
python3 lib/tavily_search.py crawl "https://example.com" --select-paths "/blog,/docs" --max-depth 3
```

**输出格式：**
```
Crawled 5 pages from https://docs.example.com

Page 1: https://docs.example.com/intro
─────────────────────────────────
<Content>

Page 2: https://docs.example.com/guide
─────────────────────────────────
<Content>
```

---

### map — 生成站点地图

发现网站上的所有 URL 并生成站点地图。

**参数：**
- `url`：需要生成地图的根 URL
- `--max-depth N`：爬取深度（默认：2）
- `--max-breadth N`：每层的最大页面数（默认：20）
- `--limit N`：生成的 URL 总数上限（默认：50）

**示例：**
```bash
# Map a site
python3 lib/tavily_search.py map "https://example.com"

# Deep map
python3 lib/tavily_search.py map "https://docs.python.org" --max-depth 3 --limit 100
```

**输出格式：**
```
Sitemap for https://example.com (42 URLs found):

  1. https://example.com/
  2. https://example.com/about
  3. https://example.com/blog
  ...
```

---

### research — 深度研究

针对特定主题进行全面的 AI 研究，并提供引用信息。

**参数：**
- `query`：研究主题
- `--model mini|pro|auto`：研究模型（默认：auto）
  - `mini`：速度更快，成本更低
  - `pro`：研究更全面
  - `auto`：让 Tavily 自动选择模型
- `--json`：输出格式为 JSON（支持结构化数据）

**示例：**
```bash
# Basic research
python3 lib/tavily_search.py research "Impact of AI on healthcare in 2026"

# Pro model for thorough research
python3 lib/tavily_search.py research "Comparison of quantum computing approaches" --model pro

# JSON output
python3 lib/tavily_search.py research "Electric vehicle market analysis" --json
```

**输出格式：**
```
Research: Impact of AI on healthcare in 2026

<Comprehensive research report with citations>

Sources:
  [1] https://source1.com
  [2] https://source2.com
  ...
```

---

## 选项参考

| 选项 | 适用范围 | 说明 | 默认值 |
| --- | --- | --- |
| `--depth basic\|advanced` | search, news, extract | 搜索/提取的深度 | basic |
| `--time day\|week\|month\|year` | search, news, finance | 时间范围过滤 | 无 |
| `-n NUM` | search, news, finance | 最大显示结果数量（0-20） | 5 |
| `--answer` | search, news, finance | 是否包含 LLM 生成的答案 | 否 |
| `--raw` | search, news, finance | 是否包含原始页面内容 | 否 |
| `--images` | search, news, finance | 是否包含图片链接 | 否 |
| `--include-domains d1,d2` | search, news, finance | 仅包含这些域名内的内容 | 无 |
| `--exclude-domains d1,d2` | search, news, finance | 排除这些域名内的内容 | 无 |
| `--country XX` | search, news, finance | 加权显示指定国家的结果 | 无 |
| `--json` | all | 输出格式为 JSON | 否 |
| `--format markdown\|text` | extract, crawl | 内容输出格式 | markdown |
| `--query "text"` | extract | 根据查询内容重新排序结果 | 否 |
| `--model mini\|pro\|auto` | research | 研究模型 | auto |
| `--max-depth N` | crawl, map | 最大爬取深度 | 2 |
| `--max-breadth N` | crawl, map | 每层的最大页面数 | 10/20 |
| `--limit N` | crawl, map | 总页面数/URL 数量上限 | 10/50 |
| `--instructions "text"` | crawl | 爬取时的指令 | 无 |
| `--select-paths p1,p2` | crawl | 仅爬取指定的路径模式 | 无 |
| `--exclude-paths p1,p2` | crawl | 排除指定的路径模式 | 无 |

---

## 错误处理

- **缺少 API 密钥**：显示包含设置说明的错误信息。
- **401 Unauthorized**：API 密钥无效。
- **429 Rate Limit**：达到请求速率限制，请稍后再试。
- **网络错误**：显示详细的错误原因。
- **未找到结果**：显示“未找到结果”的提示信息。
- **超时**：所有 HTTP 请求的默认超时时间为 30 秒。

---

## 服务费用与定价

| 功能 | 基础版 | 高级版 |
| --- | --- | --- |
| 搜索 | 1 个信用点 | 2 个信用点 |
| 提取内容 | 每个 URL 1 个信用点 | 每个 URL 2 个信用点 |
| 爬取网站 | 每页 1 个信用点 | 每页 2 个信用点 |
| 生成站点地图 | 1 个信用点 | 1 个信用点 |
| 深度研究 | 根据模型不同而异 | - |

---

## 安装说明

```bash
bash skills/tavily/install.sh
```