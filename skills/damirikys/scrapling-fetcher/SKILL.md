---
name: scrapling
description: >
  使用 **Scrapling** 这个 Python 框架进行网页抓取。该框架具备反爬虫机制（可绕过 Cloudflare 的 Turnstile 防护机制、伪造用户指纹），能够智能追踪网页中的元素，使用隐秘的无头浏览器进行抓取，并能完整提取 CSS 和 XPath 数据。适用于以下场景：  
  - 当 `web_fetch` 方法失败时（例如遇到 Cloudflare 的限制、需要处理由 JavaScript 动态生成的页面或需要突破付费墙的情况）；  
  - 从网站中提取结构化数据（如商品价格、文章内容、列表信息）；  
  - 构建能够适应网站重新设计的爬虫程序。  
  Scrapling 支持 HTTP 请求、隐秘抓取模式以及完整的浏览器模拟功能。
---
# 抓取技能

Scrapling 已在系统级别安装（`pip install scrapling[all]`）。Chromium 可用于无头浏览器模式。

## 脚本

`scripts/scrape.py` — 为三种获取模式提供的 CLI 包装器。

```bash
# Basic fetch (text output)
python3 ~/skills/scrapling/scripts/scrape.py <url>

# CSS selector
python3 ~/skills/scrapling/scripts/scrape.py <url> --selector ".class" 

# Stealth mode (Cloudflare bypass)
python3 ~/skills/scrapling/scripts/scrape.py <url> --mode stealth

# JSON output
python3 ~/skills/scrapling/scripts/scrape.py <url> --selector "h2" --json

# Quiet (suppress INFO logs)
python3 ~/skills/scrapling/scripts/scrape.py <url> -q
```

## 获取模式

- **http**（默认）— 使用浏览器 TLS 指纹欺骗的快速 HTTP 方式，适用于大多数网站。
- **stealth**— 使用具有反检测功能的无头 Chrome 浏览器，适用于 Cloudflare 或反爬虫场景。
- **dynamic**— 使用 Playwright 完整浏览器框架，适用于需要处理大量 JavaScript 和单页应用程序（SPA）的网站。

## 如何选择合适的模式

- 如果 `web_fetch` 方法返回 403/429 错误或遇到 Cloudflare 挑战，请使用 `--mode stealth`。
- 如果页面内容需要执行 JavaScript，请使用 `--mode dynamic`。
- 如果只是需要获取普通网站的文本或数据，请使用 `--mode http`（默认模式）。

## Python 内联使用

对于 CLI 无法处理的自定义逻辑，可以直接在 Python 代码中编写。请参考 `references/patterns.md` 以了解以下内容：
- 自适应抓取（能够应对网站重新设计）
- 会话/cookie 处理
- 异步操作
- XPath 查询、相似内容查找、属性提取
- MCP 服务器配置

## 注意事项

- `stealth` 和 `dynamic` 模式需要显示页面内容，因此会使用无头 Chromium 浏览器（无需使用 `xvfb-run`）。
- 当首次执行抓取时，如果设置 `auto_save=True`，系统会保存元素指纹以供后续自适应抓取使用。
- 对于大规模爬取，请使用 Spider API（详见 Scrapling 文档）。