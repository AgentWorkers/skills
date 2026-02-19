---
name: web-pilot
description: 无需使用 API 密钥即可搜索网页并阅读页面内容。适用于需要通过 DuckDuckGo、Brave 或 Google 进行多页搜索的场景；可以从 URL 中提取可读文本；支持使用带有标签页、点击功能、截图和文本搜索功能的浏览器进行交互式浏览；还可以下载文件或 PDF 文件，并关闭 cookie 相关的提示信息。该工具基于 Playwright 和 Chromium 技术开发，支持 JSON、Markdown 和文本格式的输出结果。
---
# Web Pilot

该工具包含四个脚本，无需使用任何API密钥。所有输出默认为JSON格式。

**依赖库：** `requests`, `beautifulsoup4`, `playwright`（需安装Chromium浏览器）。
**可选依赖库：** `pdfplumber` 或 `PyPDF2`（用于提取PDF文件中的文本）。

安装方法：`pip install requests beautifulsoup4 playwright && playwright install chromium`

## 1. 在网页上搜索

```bash
python3 scripts/google_search.py "query" --pages N --engine ENGINE
```

- `--engine` — 可选参数，支持 `duckduckgo`、`brave` 或 `google` 作为搜索引擎；
- 返回结果格式为 `[{title, url, snippet}, ...]`。

## 2. 阅读网页内容（仅读取一次）

```bash
python3 scripts/read_page.py "https://url" [--max-chars N] [--visible] [--format json|markdown|text] [--no-dismiss]
```

- `--format` — 可选参数，支持 `json`、`markdown` 或 `text` 三种输出格式；
- 可自动关闭网页中的cookie同意提示框（使用 `--no-dismiss` 选项可忽略此功能）。

## 3. 持久化的浏览器会话

```bash
python3 scripts/browser_session.py open "https://url"              # Open + extract
python3 scripts/browser_session.py navigate "https://other"        # Go to new URL
python3 scripts/browser_session.py extract [--format FMT]          # Re-read page
python3 scripts/browser_session.py screenshot [path] [--full]      # Save screenshot
python3 scripts/browser_session.py click "Submit"                  # Click by text/selector
python3 scripts/browser_session.py search "keyword"                # Search text in page
python3 scripts/browser_session.py tab new "https://url"           # Open new tab
python3 scripts/browser_session.py tab list                        # List all tabs
python3 scripts/browser_session.py tab switch 1                    # Switch to tab index
python3 scripts/browser_session.py tab close [index]               # Close tab
python3 scripts/browser_session.py dismiss-cookies                 # Manually dismiss cookies
python3 scripts/browser_session.py close                           # Close browser
```

- 浏览器会话在页面打开或切换时自动处理cookie同意提示；
- 支持多个标签页的独立操作（打开、切换、关闭）；
- 搜索结果会附带行号；
- 提取内容时支持JSON、Markdown或文本格式的输出。

## 4. 下载文件

```bash
python3 scripts/download_file.py "https://example.com/doc.pdf" [--output DIR] [--filename NAME]
```

- 会根据URL或HTTP头部信息自动确定文件名；
- 如果安装了 `pdfplumber` 或 `PyPDF2`，则可以提取PDF文件中的文本；
- 返回结果格式为 `{"status", "path", "filename", "size_bytes", "content_type", "extracted_text"}`。