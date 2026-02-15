---
name: reddit
description: "通过 web scraping 技术从 old.reddit.com 读取和搜索 Reddit 帖子。当 Clawdbot 需要浏览 Reddit 内容时（例如：阅读子版块的帖子、搜索特定主题、监控特定社区），可以使用此功能。该功能仅提供只读访问权限，不允许用户发布帖子或评论。"
---

# Reddit Skill 📰

使用公开的 JSON API 读取和搜索 Reddit 帖子。无需 API 密钥。

## 快速入门

```bash
# Read top posts from a subreddit
python3 /root/clawd/skills/reddit/scripts/reddit_scraper.py --subreddit LocalLLaMA --limit 5

# Search for posts
python3 /root/clawd/skills/reddit/scripts/reddit_scraper.py --search "clawdbot" --limit 5

# Read newest posts
python3 /root/clawd/skills/reddit/scripts/reddit_scraper.py --subreddit ClaudeAI --sort nuevos --limit 5
```

## 选项

| 选项 | 缩写 | 描述 | 默认值 |
|--------|-------|-------------|---------|
| `--subreddit` | `-s` | 子版块名称（不含 `r/`） | - |
| `--search` | `-q` | 搜索查询 | - |
| `--sort` | - | 排序方式：热门、最新、顶部、受欢迎、新帖、上升趋势 | `top` |
| `--time` | `-t` | 时间筛选：小时、天、周、月、年、全部 | `day` |
| `--limit` | `-n` | 帖子数量（最多 100 条） | `25` |
| `--json` | `-j` | 以 JSON 格式输出 | `false` |
| `--verbose` | `-v` | 显示帖子预览文本 | `false` |

## 示例

### 读取子版块帖子
```bash
# Top posts of the day (default)
python3 /root/clawd/skills/reddit/scripts/reddit_scraper.py --subreddit programming

# Hot posts
python3 /root/clawd/skills/reddit/scripts/reddit_scraper.py --subreddit programming --sort hot

# New posts
python3 /root/clawd/skills/reddit/scripts/reddit_scraper.py --subreddit programming --sort nuevos

# Top posts of the week
python3 /root/clawd/skills/reddit/scripts/reddit_scraper.py --subreddit programming --sort top --time week
```

### 搜索帖子
```bash
# Search all of Reddit
python3 /root/clawd/skills/reddit/scripts/reddit_scraper.py --search "machine learning"

# Search within a subreddit
python3 /root/clawd/skills/reddit/scripts/reddit_scraper.py --subreddit selfhosted --search "docker"

# Search with time filter
python3 /root/clawd/skills/reddit/scripts/reddit_scraper.py --search "AI news" --time week
```

### JSON 输出
```bash
# Get raw JSON data for processing
python3 /root/clawd/skills/reddit/scripts/reddit_scraper.py --subreddit technology --limit 3 --json
```

## 输出字段（JSON）

- `title`：帖子标题
- `author`：作者用户名
- `score`：净点赞数
- `num_comments`：评论数量
- `url`：帖子链接
- `permalink`：Reddit 讨论页面链接
- `subreddit`：子版块名称
- `created_utc`：Unix 时间戳
- `selftext`：帖子正文（前 200 个字符）
- `upvote_ratio`：点赞百分比（0-1）

## 限制

- **仅限读取**：无法发布、评论或投票
- **请求限制**：如果请求过多，Reddit 可能会限制请求频率
- **无身份验证**：部分内容可能受到访问限制

## 技术细节

有关实现细节，请参阅 [TECHNICAL.md](references/TECHNICAL.md)。