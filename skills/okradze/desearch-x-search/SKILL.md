---
name: desearch-x-search
description: 实时搜索 X（Twitter）平台上的内容。可以通过关键词、用户名或标签来查找帖子。可以获取用户的动态时间线、回复内容，以及转发这些帖子的用户信息；也可以通过帖子的 ID 或 URL 来获取具体帖子的详细信息。支持高级过滤功能，如日期范围、语言设置、互动阈值（如点赞/评论数）和媒体类型（如图片、视频等）。
metadata: {"clawdbot":{"emoji":"𝕏","homepage":"https://desearch.ai","requires":{"env":["DESEARCH_API_KEY"]}}}
---
# X（Twitter）搜索工具（Desearch）

实时搜索和监控X/Twitter内容。支持搜索帖子、追踪用户、查看时间线、回复以及转发者，并提供强大的过滤功能。

## 设置

1. 从 [https://console.desearch.ai](https://console.desearch.ai) 获取API密钥。
2. 设置环境变量：`export DESEARCH_API_KEY='your-key-here'`

## 使用方法

```bash
# Search X posts by keyword
scripts/desearch.py x "Bittensor TAO" --sort Latest --count 10

# Search with filters
scripts/desearch.py x "AI news" --user elonmusk --start-date 2025-01-01
scripts/desearch.py x "crypto" --min-likes 100 --verified --lang en

# Get a specific post by ID
scripts/desearch.py x_post 1892527552029499853

# Fetch multiple posts by URL
scripts/desearch.py x_urls "https://x.com/user/status/123" "https://x.com/user/status/456"

# Search posts by a specific user
scripts/desearch.py x_user elonmusk --query "AI" --count 10

# Get a user's timeline
scripts/desearch.py x_timeline elonmusk --count 20

# Get retweeters of a post
scripts/desearch.py x_retweeters 1982770537081532854

# Get a user's replies
scripts/desearch.py x_replies elonmusk --count 10

# Get replies to a specific post
scripts/desearch.py x_post_replies 1234567890 --count 10
```

## 命令

| 命令 | 描述 |
|---------|-------------|
| `x` | 使用高级过滤器（日期、互动次数、媒体类型）搜索X平台上的帖子 |
| `x_post` | 根据ID检索单条帖子 |
| `x_urls` | 根据URL获取多条帖子 |
| `x_user` | 根据特定用户名搜索帖子 |
| `x_timeline` | 查看用户的最新时间线帖子 |
| `x_retweeters` | 获取转发某条帖子的用户 |
| `x_replies` | 查看用户的回复 |
| `x_post_replies` | 查看特定帖子的回复 |

## 选项

| 选项 | 描述 | 适用命令 |
|--------|-------------|------------|
| `--count`, `-n` | 结果数量（默认：10，最大：100） | 大多数命令 |
| `--sort` | 排序方式：`Top` 或 `Latest` | `x` |
| `--user`, `-u` | 按X平台用户名过滤 | `x` |
| `--start-date` | 开始日期（UTC格式，YYYY-MM-DD） | `x` |
| `--end-date` | 结束日期（UTC格式，YYYY-MM-DD） | `x` |
| `--lang` | 语言代码（例如：`en`, `es`, `fr`） | `x` |
| `--verified` | 过滤已认证用户 | `x` |
| `--blue-verified` | 过滤带有蓝色认证标志的用户 | `x` |
| `--is-quote` | 仅显示带引号的推文 | `x` |
| `--is-video` | 仅显示包含视频的推文 | `x` |
| `--is-image` | 仅显示包含图片的推文 | `x` |
| `--min-retweets` | 最小转发次数 | `x` |
| `--min-replies` | 最小回复次数 | `x` |
| `--min-likes` | 最小点赞次数 | `x` |
| `--query`, `-q` | 额外搜索查询条件 | `x_user`, `x_replies`, `x_post_replies` |
| `--cursor` | 分页游标 | `x_retweeters` |

## 示例

### 查找某个话题的热门讨论
```bash
scripts/desearch.py x "Bittensor" --sort Latest --count 20 --min-likes 5
```

### 监控用户的动态
```bash
scripts/desearch.py x_timeline elonmusk --count 20
```