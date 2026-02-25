---
name: scrapling
description: "使用 Scrapling 进行网络爬取：这是一个基于 Python 的框架，具备反机器人策略（如 Cloudflare Turnstile、指纹欺骗）、自适应元素定位、隐身无头浏览器功能以及完整的 CSS/XPath 数据提取能力。当 `web_fetch` 失败时（例如遇到 Cloudflare 防护或需要解析 JavaScript 渲染的页面），或者需要从网站中提取结构化数据（如价格、文章内容、列表等）时，该工具非常适用。Scrapling 支持 HTTP 请求、隐身模式以及完整浏览器模式。来源：github.com/D4Vinci/Scrapling（PyPI：scrapling）。请仅在被允许爬取的网站上使用该工具。"
license: MIT
metadata:
  source: https://github.com/D4Vinci/Scrapling
  pypi: https://pypi.org/project/scrapling/
---
# 抓取技能

**来源:** https://github.com/D4Vinci/Scrapling（开源项目，采用类似MIT的许可证）  
**PyPI:** `scrapling` — 首次使用前请先安装（详见下文）

> ⚠️ 仅允许抓取您有权限访问的网站。请遵守`robots.txt`文件和网站的服务条款。严禁使用隐秘模式绕过付费墙或未经授权访问受限内容。

## 安装（只需安装一次，运行前需获得用户许可）

```bash
pip install scrapling[all]
patchright install chromium  # required for stealth/dynamic modes
```

- `scrapling[all]` 会安装 `patchright`（Playwright 的一个隐秘版本，作为 PyPI 包提供）、`curl_cffi`、MCP 服务器依赖库以及 IPython shell。
- `patchright install chromium` 会通过 `patchright` 自带的安装程序下载 Chromium（约 100 MB，安装机制与 `playwright install chromium` 相同）。
- 运行前请务必获得用户许可——该命令会安装约 200 MB 的依赖库和浏览器二进制文件。

## 脚本

`scripts/scrape.py` — 用于三种数据获取模式的命令行工具（CLI）封装。

```bash
# Basic fetch (text output)
python3 ~/skills/scrapling/scripts/scrape.py <url> -q

# CSS selector extraction
python3 ~/skills/scrapling/scripts/scrape.py <url> --selector ".class" -q

# Stealth mode (Cloudflare bypass) — only on sites you're authorized to access
python3 ~/skills/scrapling/scripts/scrape.py <url> --mode stealth -q

# JSON output
python3 ~/skills/scrapling/scripts/scrape.py <url> --selector "h2" --json -q
```

## 数据获取模式

- **http**（默认模式）：使用浏览器进行快速数据获取，并通过伪造 TLS 信息来规避某些网站的限制。适用于大多数网站。
- **stealth**：使用无头版 Chrome 浏览器，并具备反检测功能，适用于 Cloudflare 或反爬虫策略的网站。
- **dynamic**：使用完整的 Playwright 浏览器，适用于包含大量 JavaScript 和单页应用程序（SPA）的网站。

## 各模式的适用场景

- 如果遇到 403/429 错误或 Cloudflare 的限制，请使用 `--mode stealth`。
- 如果页面内容需要执行 JavaScript 代码，请使用 `--mode dynamic`。
- 对于普通网站且仅需要文本或数据，建议使用 `--mode http`（默认模式）。

## Python 内联使用

如需在命令行之外编写自定义逻辑，可以直接在 Python 代码中实现。请参考 `references/patterns.md` 以了解以下内容：
- 自适应抓取（`auto_save` / `adaptive`：将元素信息保存到本地以便后续使用）
- 会话/cookie 管理
- 异步操作
- XPath 查询、相似元素查找、属性提取

## 注意事项

- **MCP 服务器**（`scrapling mcp`）：用于支持基于人工智能的抓取功能。仅在确实需要且可信任的情况下启动该服务器——它会启动一个本地 HTTP 服务器。
- `auto_save=True`：将元素信息保存到磁盘，以便后续进行自适应抓取。该设置会在工作目录中创建相应的本地状态文件。
- `stealth` 和 `dynamic` 模式均使用无头版 Chromium 浏览器，因此无需使用 `xvfb-run` 命令。
- 对于大规模爬取任务，请参考 Scrapling 的官方文档以使用 Spider API。