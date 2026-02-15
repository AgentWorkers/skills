---
name: reddit
description: 浏览、搜索、发布内容以及管理 Reddit 论坛。仅阅读功能无需身份验证；发布或管理内容则需要先设置 OAuth 访问权限。
metadata: {"clawdbot":{"emoji":"📣","requires":{"bins":["node"]}}}
---

# Reddit

您可以在Reddit上浏览、搜索、发布内容以及管理子版块。仅阅读内容的操作无需认证；而发布或管理内容则需要先设置OAuth权限。

## 设置（用于发布/管理内容）

1. 访问 https://www.reddit.com/prefs/apps
2. 点击“创建另一个应用…”
3. 选择“脚本”类型
4. 将重定向URI设置为 `http://localhost:8080`
5. 记下您的客户端ID（在应用名称下方）和客户端密钥
6. 设置环境变量：
   ```bash
   export REDDIT_CLIENT_ID="your_client_id"
   export REDDIT_CLIENT_SECRET="your_client_secret"
   export REDDIT_USERNAME="your_username"
   export REDDIT_PASSWORD="your_password"
   ```

## 阅读帖子（无需认证）

```bash
# Hot posts from a subreddit
node {baseDir}/scripts/reddit.mjs posts wallstreetbets

# New posts
node {baseDir}/scripts/reddit.mjs posts wallstreetbets --sort new

# Top posts (day/week/month/year/all)
node {baseDir}/scripts/reddit.mjs posts wallstreetbets --sort top --time week

# Limit results
node {baseDir}/scripts/reddit.mjs posts wallstreetbets --limit 5
```

## 搜索帖子

```bash
# Search within a subreddit
node {baseDir}/scripts/reddit.mjs search wallstreetbets "YOLO"

# Search all of Reddit
node {baseDir}/scripts/reddit.mjs search all "stock picks"
```

## 获取帖子的评论

```bash
# By post ID or full URL
node {baseDir}/scripts/reddit.mjs comments POST_ID
node {baseDir}/scripts/reddit.mjs comments "https://reddit.com/r/subreddit/comments/abc123/..."
```

## 发布帖子（需要认证）

```bash
# Text post
node {baseDir}/scripts/reddit.mjs submit yoursubreddit --title "Weekly Discussion" --text "What's on your mind?"

# Link post
node {baseDir}/scripts/reddit.mjs submit yoursubreddit --title "Great article" --url "https://example.com/article"
```

## 回复帖子/评论（需要认证）

```bash
node {baseDir}/scripts/reddit.mjs reply THING_ID "Your reply text here"
```

## 管理帖子（需要认证及管理员权限）

```bash
# Remove a post/comment
node {baseDir}/scripts/reddit.mjs mod remove THING_ID

# Approve a post/comment
node {baseDir}/scripts/reddit.mjs mod approve THING_ID

# Sticky a post
node {baseDir}/scripts/reddit.mjs mod sticky POST_ID

# Unsticky
node {baseDir}/scripts/reddit.mjs mod unsticky POST_ID

# Lock comments
node {baseDir}/scripts/reddit.mjs mod lock POST_ID

# View modqueue
node {baseDir}/scripts/reddit.mjs mod queue yoursubreddit
```

## 注意事项：

- 仅阅读内容的操作使用Reddit的公共JSON API（无需认证）
- 发布或管理内容的操作需要OAuth权限——请先运行`login`命令进行授权
- OAuth令牌存储在`~/.reddit-token.json`文件中（会自动更新）
- 访问限制：OAuth用户每分钟约60次请求；未认证用户每分钟约10次请求