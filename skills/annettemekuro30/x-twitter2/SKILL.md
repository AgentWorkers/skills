---
name: twitter-openclaw
description: 与 Twitter/X 互动：阅读推文、进行搜索、发布推文、点赞、转发推文以及管理你的时间线。
user-invocable: true
metadata: {"openclaw":{"emoji":"🐦‍⬛","skillKey":"twitter-openclaw","primaryEnv":"TWITTER_BEARER_TOKEN","requires":{"bins":["twclaw"],"env":["TWITTER_BEARER_TOKEN"]},"install":[{"id":"npm","kind":"node","package":"twclaw","bins":["twclaw"],"label":"Install twclaw (npm)"}]}}
---

# twitter-openclaw 🐦‍⬛

这是一个用于与Twitter/X上的帖子、时间线以及用户进行交互的工具，通过OpenClaw实现。

## 认证

需要设置一个Twitter API承载令牌（`TWITTER_BEARER_TOKEN`）。

可选地，可以设置`TWITTER_API_KEY`和`TWITTER_API_SECRET`以执行写入操作（如发布、点赞、转发）。

运行`twclaw auth-check`来验证凭据。

## 命令

### 读取

```bash
twclaw read <tweet-url-or-id>          # Read a single tweet with full metadata
twclaw thread <tweet-url-or-id>        # Read full conversation thread
twclaw replies <tweet-url-or-id> -n 20 # List replies to a tweet
twclaw user <@handle>                  # Show user profile info
twclaw user-tweets <@handle> -n 20     # User's recent tweets
```

### 时间线

```bash
twclaw home -n 20                      # Home timeline
twclaw mentions -n 10                  # Your mentions
twclaw likes <@handle> -n 10           # User's liked tweets
```

### 搜索

```bash
twclaw search "query" -n 10            # Search tweets
twclaw search "from:elonmusk AI" -n 5  # Search with operators
twclaw search "#trending" --recent     # Recent tweets only
twclaw search "query" --popular        # Popular tweets only
```

### 热门话题

```bash
twclaw trending                        # Trending topics worldwide
twclaw trending --woeid 23424977       # Trending in specific location
```

### 发布

```bash
twclaw tweet "hello world"                          # Post a tweet
twclaw reply <tweet-url-or-id> "great thread!"      # Reply to a tweet
twclaw quote <tweet-url-or-id> "interesting take"   # Quote tweet
twclaw tweet "look at this" --media image.png        # Tweet with media
```

### 互动

```bash
twclaw like <tweet-url-or-id>          # Like a tweet
twclaw unlike <tweet-url-or-id>        # Unlike a tweet
twclaw retweet <tweet-url-or-id>       # Retweet
twclaw unretweet <tweet-url-or-id>     # Undo retweet
twclaw bookmark <tweet-url-or-id>      # Bookmark a tweet
twclaw unbookmark <tweet-url-or-id>    # Remove bookmark
```

### 关注

```bash
twclaw follow <@handle>                # Follow user
twclaw unfollow <@handle>              # Unfollow user
twclaw followers <@handle> -n 20       # List followers
twclaw following <@handle> -n 20       # List following
```

### 列表

```bash
twclaw lists                           # Your lists
twclaw list-timeline <list-id> -n 20   # Tweets from a list
twclaw list-add <list-id> <@handle>    # Add user to list
twclaw list-remove <list-id> <@handle> # Remove user from list
```

## 输出选项

```bash
--json          # JSON output
--plain         # Plain text, no formatting
--no-color      # Disable ANSI colors
-n <count>      # Number of results (default: 10)
--cursor <val>  # Pagination cursor for next page
--all           # Fetch all pages (use with caution)
```

## OpenClaw使用指南

- 读取推文时，务必显示作者、用户名、推文内容、时间戳以及互动次数。
- 对于话题帖，应按时间顺序显示推文。
- 搜索结果时，用关键指标进行简洁总结。
- 在发布、点赞或转发之前，请先确认用户的意愿。
- 请遵守Twitter的速率限制，避免批量操作。
- 如需程序化处理输出结果，请使用`--json`选项。

## 故障排除

### 401 Unauthorized（未经授权）
请检查`TWITTER_BEARER_TOKEN`是否已设置且有效。

### 429 Rate Limited（速率限制）
请稍后重试。Twitter API对每个15分钟的时间窗口有严格的速率限制。

---

**简而言之**：可以使用此工具在Twitter/X上阅读、搜索、发布内容并进行互动。执行写入操作前，请务必先确认用户的同意。