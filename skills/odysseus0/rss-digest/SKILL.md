---
name: rss-digest
description: "使用 `feed CLI` 功能生成代理型 RSS 摘要。该工具负责获取 RSS 源、对内容进行分类筛选，并汇总其中的高质量文章。适用场景包括：  
(1) 阅读 RSS 源或快速了解最新新闻；  
(2) 用户请求获取近期文章的汇总或摘要；  
(3) 用户询问当天有哪些新内容或有趣的文章；  
(4) 用户提到相关 RSS 源、RSS 或博客时。"
metadata: {"openclaw": {"emoji": "📡", "requires": {"bins": ["feed"]}, "install": [{"kind": "brew", "formula": "odysseus0/tap/feed", "bins": ["feed"], "label": "Install via Homebrew"}, {"kind": "go", "package": "github.com/odysseus0/feed/cmd/feed@latest", "bins": ["feed"], "label": "Install via Go"}]}}
---

# RSS 摘要

该工具会从 RSS 源中筛选出值得阅读的内容。需要使用 `feed` 命令行工具（可通过 `brew install odysseus0/tap/feed` 安装）。

## 工作流程

0. **初始化**：运行 `feed get stats`。如果没有 RSS 源，可以导入预设的源列表：`feed import https://github.com/odysseus0/feed/raw/main/hn-popular-blogs-2025.opml`（包含 92 个精选的科技博客）。系统会询问用户是否希望添加自己的 RSS 源。
1. **获取最新内容**：使用 `feed fetch` 命令获取最新的文章条目。
2. **扫描**：使用 `feed get entries --limit 50` 命令获取最近的未读文章（包括标题、来源和发布日期）。
3. **筛选**：从中挑选出 5-10 篇具有较高价值的文章。优先考虑与人工智能、系统工程、开发工具相关的内容，以及那些引人注目或观点独特的文章。
4. **阅读**：使用 `feed get entry <id>` 命令查看每篇文章的完整内容（以 Markdown 格式显示）。
5. **总结**：为每篇文章生成摘要，包括标题、来源以及简短的 2-3 句说明其重要性的内容。如果内容可以按主题分类，可以进行分类展示。

## 命令

```
feed fetch                              # pull latest from all feeds
feed get entries --limit N              # list unread entries (table)
feed get entries --feed <id> --limit N  # filter by feed
feed get entry <id>                     # read full post (Markdown)
feed search "<query>"                   # full-text search
feed update entries --read <id> ...     # batch mark read
feed get feeds                          # list feeds with unread counts
feed get stats                          # database stats
```

## 注意事项

- 默认输出格式为表格形式，便于快速浏览；如需以 JSON 格式查看内容，请使用 `-o json` 选项。
- `feed get entry <id>` 命令会返回文章的 Markdown 内容。
- 如果文章数量过多，可以使用 `--feed <feed_id>` 选项来过滤特定来源的文章。