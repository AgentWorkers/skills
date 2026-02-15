---
name: decodo-scraper
description: 使用 Decodo Scraper OpenClaw 技能在 Google 上搜索或抓取网页内容。
homepage: https://decodo.com
credentials:
  - DECODO_AUTH_TOKEN
env:
  required:
    - DECODO_AUTH_TOKEN
---

# Decodo Scraper OpenClaw 技能

使用此技能可以通过 [Decodo Web Scraping API](https://help.decodo.com/docs/web-scraping-api-google-search) 在 Google 上进行搜索或抓取任何 URL。`Search` 命令会返回一个 JSON 格式的结果数组；`Scrape URL` 命令则会返回该网页的纯 Markdown 内容。

**身份验证：** 需要在您的环境变量中设置 `DECODO_AUTH_TOKEN`（从 Decodo 仪表板 → Scraping APIs 获取的基本认证令牌），或者将其保存在仓库根目录下的 `.env` 文件中。

**错误处理：** 如果操作失败，脚本会将错误信息以 JSON 格式写入标准错误流（stderr），并以代码 1 退出。

---

## 工具

### 1. 在 Google 上搜索

使用此工具可以查找 URL、答案或结构化的搜索结果（包括自然搜索结果、AI 概述、相关问题等）。

**命令：**
```bash
python tools/scrape.py --target google_search --query "your search query"
```

**示例：**
```bash
python tools/scrape.py --target google_search --query "best laptops 2025"
python tools/scrape.py --target google_search --query "python requests tutorial"
```

**可选参数：** `--geo us` 或 `--locale en` 可用于指定地理位置或语言。

---

### 2. 抓取网页内容

使用此工具可以获取特定网页的内容。默认情况下，API 会以 Markdown 格式返回内容，这种格式更便于大型语言模型（LLMs）处理，同时也能减少所需的 API 请求次数。

**命令：**
```bash
python tools/scrape.py --target universal --url "https://example.com"
```

**示例：**
```bash
python tools/scrape.py --target universal --url "https://example.com"
python tools/scrape.py --target universal --url "https://news.ycombinator.com/"
```

---

## 总结

| 功能        | 目标            | 参数        | 示例命令                |
|-------------|----------------|------------|----------------------|
| 搜索        | `google_search`     | `--query`    | `python tools/scrape.py --target google_search --query "laptop"` |
| 抓取网页内容 | `universal`     | `--url`     | `python tools/scrape.py --target universal --url "https://example.com"` |

**输出：**  
- `Search`：搜索结果以 JSON 格式输出到标准输出（stdout）。  
- `Scrape URL`：网页内容以 Markdown 格式输出到标准输出（stdout）。