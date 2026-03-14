---
name: time-masheen
description: THE_TIME_MASHEEN — full-spectrum web intelligence combining live scraping, historical time travel, and interactive browser automation. Use when: (1) scraping or crawling any live website (static, JS-heavy, or rendering-protected), (2) going back in time to retrieve archived or historical versions of any page via the Wayback Machine, (3) comparing what a site looks like now vs. what it looked like in any previous year, (4) automating browser interactions (login, click, fill forms) on web apps that can't be passively scraped, (5) extracting data from login-gated or paywalled pages, or (6) any task requiring live scraping + historical research + browser interaction in combination. Triggers on: "scrape this", "crawl", "wayback", "archive", "what did this site look like", "compare current vs historical", "browser automation", "extract data from", "log in and scrape", "go back in time on".
---

# THE_TIME_MASHEEN

> *介入。回溯过去。抓取数据。自动化处理所需信息。*

这是一个三层网络智能框架，你可以选择其中一层，或者将所有三层结合使用。

| 层次 | 工具 | 功能 |
|-------|------|-----|
| **实时数据抓取** | Scrapling | 从任何实时URL中提取内容 |
| **历史数据抓取** | Wayback Machine CDX API | 回溯到指定的历史快照 |
| **交互式操作** | playwright-cli | 模拟真实浏览器行为——登录、点击、滚动页面、填写表单 |

---

## 决策树

```
Need web data?
│
├─ Historical / "what did it look like before"?
│    └─ Wayback CDX API → scrape snapshot via Scrapling or web_fetch
│
├─ Need to click / log in / fill forms first?
│    └─ playwright-cli → authenticate → hand off to Scrapling
│
└─ Just current content?
     ├─ Static / simple       → scrapling get
     ├─ JS-heavy / React      → scrapling fetch --network-idle
     └─ Heavily protected sites → scrapling stealthy-fetch --solve-cloudflare
```

---

## 第一层——实时数据抓取（Scraping）

### 执行流程（始终从顶层开始）

```bash
# 1. Static sites, blogs, docs
scrapling extract get "https://example.com" output.md

# 2. JS-heavy / React / Next.js / dynamic content
scrapling extract fetch "https://example.com" output.md --network-idle --wait 3000

# 3. Cloudflare / rendering-protected
scrapling extract stealthy-fetch "https://example.com" output.md --solve-cloudflare
```

### 提取特定内容（节省处理时间）
```bash
scrapling extract fetch "https://example.com" output.md --css-selector "main article"
scrapling extract get "https://example.com" output.md --css-selector ".pricing-table"
```

**规则：**
- 读取数据后务必清理临时文件
- 使用`.md`格式输出可读文本，仅使用`.html`格式进行结构解析
- 使用`--css-selector`来避免处理庞大的HTML内容

更多关于CLI参数、爬虫框架和Python API的详细信息，请参阅`references/scrapling.md`。

---

## 第二层——时间旅行（Wayback Machine）

### 查找URL的所有历史快照
```bash
curl -s "https://web.archive.org/cdx/search/cdx?url=example.com&output=json&fl=timestamp,statuscode&filter=statuscode:200&limit=20"
```

### 每年保存一个快照（用于版本跟踪）
```bash
curl -s "https://web.archive.org/cdx/search/cdx?url=example.com&output=json&collapse=timestamp:4&fl=timestamp,statuscode&filter=statuscode:200"
```

### 抓取特定时间点的数据
```bash
# Scrapling for clean extraction:
scrapling extract get "https://web.archive.org/web/20230601000000/https://example.com/" archive.md

# Or read via web_fetch:
# web_fetch: https://web.archive.org/web/20230601000000/https://example.com/
```

### 检查URL是否已被存档
```bash
curl -s "https://archive.org/wayback/available?url=example.com" | python3 -m json.tool
```

更多关于CDX API和`ia` CLI的使用方法，请参阅`references/wayback.md`。

---

## 第三层——交互式自动化（playwright-cli）

当页面需要登录、点击或动态交互才能获取内容时，使用此工具。

```bash
# Open browser
playwright-cli open https://app.example.com

# Snapshot to get element refs
playwright-cli snapshot

# Interact
playwright-cli click e12
playwright-cli fill e5 "username@example.com"
playwright-cli press Tab
playwright-cli fill e6 "password"
playwright-cli press Enter

# Capture state
playwright-cli screenshot
playwright-cli eval "document.title"

# Close
playwright-cli close
```

### 执行流程：先认证再批量抓取数据
```bash
# 1. playwright-cli open → log in → navigate to target
# 2. playwright-cli screenshot  # verify you're authenticated
# 3. scrapling extract get <url> output.md  # scrape while session is active
```

---

## 结合所有三层功能

### 实时数据与历史数据的对比（价格变化、内容更新、竞争情报）
```bash
# 1. Scrape current state
scrapling extract get "https://competitor.com/pricing" current.md

# 2. Find yearly snapshots
curl -s "https://web.archive.org/cdx/search/cdx?url=competitor.com/pricing&output=json&collapse=timestamp:4&fl=timestamp&filter=statuscode:200"

# 3. Scrape archived version from any year
scrapling extract get "https://web.archive.org/web/20230101000000/https://competitor.com/pricing" archive.md

# 4. Diff
diff archive.md current.md
```

### 需要登录的网站——完整数据抓取
```bash
# playwright handles auth → Scrapling does the bulk lift
playwright-cli open https://example.com/login
playwright-cli fill e5 "your@email.com"
playwright-cli fill e6 "password"
playwright-cli press Enter
playwright-cli screenshot  # verify you're in
scrapling extract get "https://example.com/members/content" output.md
```

---

## 安全性

此功能会打开真实的浏览器会话，并可以抓取需要登录保护的页面。使用前请注意以下事项：

- **你控制着浏览器。**`playwright-cli`会在你的机器上运行浏览器，它会根据你的指令访问指定URL并操作页面元素。
- **所有数据仅保存在本地。**自动化过程中使用的所有会话状态仅存在于你的机器上，且仅用于你启动的抓取任务。
- **仅用于你可以访问的网站。**该工具仅用于合法的网络研究，如竞争情报收集、内容监控或访问你拥有账户的网站。它不能用于未经授权的访问。
- **运行前请仔细检查命令。**与所有自动化工具一样，在执行前请确保你了解其工作原理。

---

### CLI扩展性——适配任何软件

当你需要为任何桌面或Web应用程序提供完整的CLI接口时：
```bash
# Install once in Claude Code
/plugin marketplace add HKUDS/CLI-Anything
/plugin install cli-anything

# Build a complete CLI for any software (7-phase pipeline)
/cli-anything:cli-anything ./target-app

# Iteratively refine
/cli-anything:refine ./target-app "focus on data export workflows"
```