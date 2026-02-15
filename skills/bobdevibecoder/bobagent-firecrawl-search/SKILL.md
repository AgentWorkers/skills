---
name: firecrawl
description: 通过 Firecrawl API 进行网页搜索和数据抓取。当您需要搜索网页、抓取网站内容（包括那些包含大量 JavaScript 代码的页面）、遍历整个网站，或从网页中提取结构化数据时，可以使用该 API。使用该功能前，请确保已设置 `FIRECRAWL_API_KEY` 环境变量。
---

# Firecrawl

通过 Firecrawl API 进行网络搜索和数据抓取。

## 先决条件

请在您的环境变量或 `.env` 文件中设置 `FIRECRAWL_API_KEY`：
```bash
export FIRECRAWL_API_KEY=fc-xxxxxxxxxx
```

## 快速入门

### 在网页上搜索
```bash
firecrawl_search "your search query" --limit 10
```

### 抓取单个页面
```bash
firecrawl_scrape "https://example.com"
```

### 遍历整个网站
```bash
firecrawl_crawl "https://example.com" --max-pages 50
```

## API 参考

详细 API 文档和高级选项请参阅 [references/api.md](references/api.md)。

## 脚本

- `scripts/search.py` - 使用 Firecrawl 在网页上搜索
- `scripts/scrape.py` - 抓取单个 URL 的内容
- `scripts/crawl.py` - 遍历整个网站并抓取数据