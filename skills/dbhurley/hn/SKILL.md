---
name: hn
description: 浏览 Hacker News：查看热门新闻、最新文章、精选内容、用户提问、相关展示、招聘信息以及带有评论的新闻详情。
homepage: https://news.ycombinator.com
metadata: {"clawdis":{"emoji":"📰","requires":{"bins":["curl"]}}}
---

# Hacker News

您可以通过命令行阅读 Hacker News 的内容。

## 命令

### 热门新闻
```bash
uv run {baseDir}/scripts/hn.py top          # Top 10 stories
uv run {baseDir}/scripts/hn.py top -n 20    # Top 20 stories
```

### 其他信息源
```bash
uv run {baseDir}/scripts/hn.py new          # Newest stories
uv run {baseDir}/scripts/hn.py best         # Best stories
uv run {baseDir}/scripts/hn.py ask          # Ask HN
uv run {baseDir}/scripts/hn.py show         # Show HN
uv run {baseDir}/scripts/hn.py jobs         # Jobs
```

### 新闻详情
```bash
uv run {baseDir}/scripts/hn.py story <id>              # Story with top comments
uv run {baseDir}/scripts/hn.py story <id> --comments 20 # More comments
```

### 搜索
```bash
uv run {baseDir}/scripts/hn.py search "AI agents"      # Search stories
uv run {baseDir}/scripts/hn.py search "Claude" -n 5    # Limit results
```

## API

使用官方的 [Hacker News API](https://github.com/HackerNews/API)（无需认证）。