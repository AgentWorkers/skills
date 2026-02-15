---
name: letterboxd-watchlist
description: 将公开 Letterboxd 用户的观看列表抓取为 CSV 或 JSONL 格式的电影标题和电影 URL 列表，无需登录。此功能适用于用户请求导出、抓取或复制其观看列表的情况，也可用于构建“观看下一部”（watch-next）的观影推荐列表。
---

# Letterboxd 观看列表抓取工具

使用随附的脚本来抓取 Letterboxd 的公共观看列表（无需身份验证）。  
如果用户未提供用户名，请务必向用户询问。

## 脚本

- `scripts/scrape_watchlist.py`

### 基本用法

```bash
uv run scripts/scrape_watchlist.py <username> --out watchlist.csv
```

### 强化模式（推荐）

```bash
uv run scripts/scrape_watchlist.py <username> --out watchlist.jsonl --delay-ms 300 --timeout 30 --retries 2
```

### 输出格式

- `--out *.csv` → 输出格式为 `title,link`
- `--out *.jsonl` → 每行输出一个 JSON 对象：`{"title": "…", "link": "…"}`

## 注意事项

- Letterboxd 的用户名不区分大小写，但必须完全匹配。
- 该脚本会抓取分页的页面：`/watchlist/page/<n>/`。
- 停止条件：当遇到第一页中没有 `data-target-link="/film/..."` 标签的条目时停止抓取。
- 脚本会验证用户名格式（`[A-Za-z0-9_-]+`），并支持重试和超时机制。
- 默认的爬取延迟为每页 250 毫秒，以减少临时错误的发生。
- 本脚本采用尽力而为的 HTML 抓取方式；如果 Letterboxd 修改了页面标记，请相应调整脚本中的正则表达式。

## 使用范围

- 本工具仅用于抓取 Letterboxd 的公共观看列表，并将结果输出为 CSV 或 JSONL 格式。
- 除非用户明确要求，否则不得读取本地文件夹、扫描图书馆数据或执行其他无关操作。