---
name: hackernews
description: 浏览和搜索 Hacker News。获取热门故事、新发布的故事、最佳故事、用户提问（Ask HN）的内容，以及职位招聘信息。查看故事详情、用户评论和用户资料。通过 Algolia 工具对故事和评论进行搜索。查找“谁在招聘？”的相关帖子。您可以利用该工具进行各种与 Hacker News 相关的查询，例如：“Hacker News 上的热门话题是什么？”，“在 Hacker News 上搜索‘AI’相关的内容”，“显示故事 X 的评论”，“谁在招聘？”，“最新的用户提问（Ask HN）帖子”。
---

# Hacker News

这是一个用于Hacker News API的命令行工具（CLI），无需进行身份验证。

## 命令行使用方法

运行 `scripts/hn.sh <command>`。所有命令都支持使用 `--json` 选项来获取原始JSON格式的输出。

### 浏览新闻文章

```bash
# Top/trending stories (default 10)
scripts/hn.sh top
scripts/hn.sh top --limit 20

# Other lists
scripts/hn.sh new --limit 5     # newest
scripts/hn.sh best --limit 10   # highest rated
scripts/hn.sh ask                # Ask HN
scripts/hn.sh show               # Show HN
scripts/hn.sh jobs               # job postings
```

### 查看文章详情及评论

```bash
# Full item details (story, comment, job, poll)
scripts/hn.sh item 12345678

# Top comments on a story
scripts/hn.sh comments 12345678
scripts/hn.sh comments 12345678 --limit 10 --depth 2
```

### 查看用户资料

```bash
scripts/hn.sh user dang
```

### 搜索

```bash
# Basic search
scripts/hn.sh search "rust programming"

# With filters
scripts/hn.sh search "LLM" --type story --sort date --period week --limit 5
scripts/hn.sh search "hiring remote" --type comment --period month
```

### 查看招聘信息

```bash
# Latest "Who is hiring?" job postings
scripts/hn.sh whoishiring
scripts/hn.sh whoishiring --limit 20
```

## 常见使用场景

| 用户需求 | 命令 |
|---|---|
| “Hacker News上有什么热门内容？” | `scripts/hn.sh top` |
| “最新的‘Ask HN’帖子” | `scripts/hn.sh ask` |
| “在Hacker News上搜索‘X’” | `scripts/hn.sh search "X"` |
| “显示文章Y的评论” | `scripts/hn.sh comments Y` |
| “谁在招聘？” | `scripts/hn.sh whoishiring` |
| “介绍一下Hacker News用户Z” | `scripts/hn.sh user Z` |

## 注意事项

- 为了提高效率，新闻文章的列表会采用并行获取的方式加载。
- 评论和用户简介中的HTML内容会自动转换为纯文本。
- 时间戳会以相对时间格式显示（例如：“2小时前”、“3天前”）。
- 有关API的详细信息，请参阅 [references/api.md](references/api.md)。