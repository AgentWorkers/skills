---
name: web-multi-search
description: 使用 `async-search-scraper` 同时搜索多个搜索引擎（Bing、Yahoo、Startpage、Aol、Ask），并遍历各个搜索引擎的结果页面。
metadata:
  clawdis:
    emoji: "🔍"
    primaryEnv: python
    requires:
      bins:
        - python3
        - pip
    install:
      - python3 -m pip install -r requirements.txt
      - python3 -m pip install git+https://github.com/soxoj/async-search-scraper.git --no-deps
---

# 网页多引擎搜索

使用 [async-search-scraper](https://github.com/soxoj/async-search-scraper) 可以同时从 **多个搜索引擎** 中搜索网页。该工具能够从 Bing、Yahoo、Startpage、Aol 和 Ask 等网站收集搜索结果，并遍历多个搜索结果页面。

## 设置

```bash
cd skills/web-multi-search
python3 -m pip install -r requirements.txt
python3 -m pip install git+https://github.com/soxoj/async-search-scraper.git --no-deps
```

> **注意：** 该库需要从 GitHub 的 URL 安装，而非通过 PyPI 安装。必须使用 `--no-deps` 参数，因为该库会自动安装 `bs4` 库（但实际上所需的依赖库已包含在 `requirements.txt` 文件中）。

### Linux (apt) 的备用安装方式
如果 `pip` 无法使用，可以安装相应的系统软件包：

```bash
sudo apt-get update
sudo apt-get install -y python3-requests python3-aiohttp python3-aiohttp-socks python3-bs4
```

## 使用方法

运行搜索脚本并输入查询内容：

```bash
python3 web_multi_search.py "your search query"
```

### 参数选项

| 参数 | 默认值 | 说明 |
|------|---------|-------------|
| `--pages` | `3` | 每个搜索引擎返回的结果页面数 |
| `--engines` | `all` | 所有可用搜索引擎（以逗号分隔的列表：`bing,yahoo,startpage,aol,ask`） |
| `--proxy` | `none` | HTTP/SOCKS 代理地址 |
| `--timeout` | `10` | HTTP 请求的超时时间（秒） |
| `--output` | `json` | 输出格式：`json`、`csv` 或 `text` |
| `--unique-urls` | `off` | 按 URL 去重搜索结果 |
| `--unique-domains` | `off` | 按域名去重搜索结果 |

### 使用示例

```bash
# Basic search, 3 pages per engine, JSON output
python3 web_multi_search.py "python async tutorial"

# Search only Bing and Yahoo, 5 pages each
python3 web_multi_search.py "machine learning" --engines bing,yahoo --pages 5

# Unique URLs only, CSV output
python3 web_multi_search.py "OpenClaw skills" --unique-urls --output csv

# Use a proxy
python3 web_multi_search.py "privacy tools" --proxy socks5://127.0.0.1:9050
```

### 输出格式

默认的输出格式为 JSON，返回一个包含搜索结果的对象数组：

```json
[
  {
    "engine": "Bing",
    "host": "example.com",
    "link": "https://example.com/page",
    "title": "Page Title",
    "text": "Snippet of the page content..."
  }
]
```

### 如何使用该工具

当需要从网页中获取信息时：
1. 运行脚本并输入用户的查询内容。
2. 解析 JSON 输出内容，提取相关的链接和文本片段。
3. 利用这些结果来回答用户的问题，或进一步获取特定页面以供深入阅读。

```bash
# Quick search and capture output
RESULTS=$(python3 /path/to/skills/web-multi-search/web_multi_search.py "query here" 2>/dev/null)
echo "$RESULTS" | python3 -c "import json,sys; data=json.load(sys.stdin); [print(r['link'], r['title']) for r in data[:10]]"
```

## 支持的搜索引擎

| 搜索引擎 | 支持情况 |
|--------|--------|
| Bing | 可用 |
| Yahoo | 可用 |
| Startpage | 可用 |
| Aol | 可用 |
| Ask | 可用 |
| Google | 不支持（需要 JavaScript） |
| DuckDuckGo | 不支持（有验证码） |
| Dogpile | 不支持（返回 HTTP 403 错误） |
| Mojeek | 不支持（返回 HTTP 403 错误） |
| Qwant | 不支持（返回 HTTP 403 错误） |
| Torch | 需要使用 TOR 代理 |

## 常见问题解决方法

- **导入错误**：确保使用 `--no-deps` 参数从 GitHub 安装库。
- **搜索结果为空或被屏蔽**：某些搜索引擎可能设置了访问限制。可以增加请求间隔或减少请求的页面数量。
- **Torch 搜索引擎**：仅支持通过 `socks5://127.0.0.1:9050` 运行的 TOR 代理。