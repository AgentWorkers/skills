---
name: bird-twitter
description: 使用 `bird` 库实现的 Twitter/X 命令行界面（CLI）封装工具：可以发布推文、回复评论、查看推文、进行搜索以及管理你的时间线。这是一个基于 GraphQL 的高效 X CLI 工具。
version: 1.0.0
author: cyzi
tags: [twitter, x, tweet, social, timeline, search]
metadata: {"openclaw":{"emoji":"🐦","skillKey":"bird-twitter","primaryEnv":"AUTH_TOKEN","requires":{"bins":["bird"],"env":["AUTH_TOKEN","CT0"]}}}
---
# Bird Twitter Skill 🐦

这是一个基于 `bird` 工具的快速 Twitter/X 命令行接口（CLI）封装，支持通过 Twitter 的 GraphQL API 发布推文、回复推文、阅读推文、搜索推文以及管理个人时间线。

## 所需的环境变量

```bash
export AUTH_TOKEN=<your_twitter_auth_token>
export CT0=<your_twitter_ct0_cookie>
```

### 如何获取令牌

1. 在浏览器中登录 Twitter/X。
2. 打开开发者工具（按 F12 键）。
3. 转到“应用/存储”（Application/Storage）→“Cookies”（Cookies）→“twitter.com”。
4. 复制以下内容：
   - `auth_token` → `AUTH_TOKEN`
   - `ct0` → `CT0`

## 快速使用方法

```bash
# Check login status
bird whoami

# Check credential availability
bird check

# Post a tweet
bird tweet "Hello from bird-twitter skill!"

# Reply to a tweet
bird reply <tweet-id-or-url> "Great thread!"

# Read a tweet
bird read <tweet-id-or-url>

# Read with JSON output
bird read <tweet-id-or-url> --json

# Search tweets
bird search "query"

# Get home timeline
bird home

# Get mentions
bird mentions

# Get liked tweets
bird likes

# Follow a user
bird follow <username>

# Get user's tweets
bird user-tweets <handle>

# Get trending topics
bird news
bird trending
```

## 命令

### 发布推文

| 命令 | 描述 |
|---------|-------------|
| `bird tweet <文本>` | 发布新推文 |
| `bird reply <链接> <文本>` | 回复一条推文 |
| `bird tweet <文本> --media <路径>` | 发布带有媒体内容的推文（最多支持 4 张图片或 1 个视频） |

### 阅读推文

| 命令 | 描述 |
|---------|-------------|
| `bird read <链接>` | 阅读/获取一条推文 |
| `bird thread <链接>` | 显示完整的推文对话线程 |
| `bird replies <链接>` | 列出对某条推文的回复 |
| `bird user-tweets <用户名>` | 获取用户的全部推文 |

### 管理时间线

| 命令 | 描述 |
|---------|-------------|
| `bird home` | 主页时间线（“为你推荐”的推文） |
| `bird mentions` | 提及你的推文 |
| `bird likes` | 你喜欢的推文 |
| `bird bookmarks` | 你收藏的推文 |

### 搜索与发现

| 命令 | 描述 |
|---------|-------------|
| `bird search <查询>` | 搜索推文 |
| `bird news` | 来自“探索”（Explore）板块的 AI 策略推荐的新闻 |
| `bird trending` | 热门话题 |

### 账户管理

| 命令 | 描述 |
|---------|-------------|
| `bird whoami` | 显示当前登录的账户信息 |
| `bird check` | 检查凭证是否有效 |
| `bird follow <用户名>` | 关注用户 |
| `bird unfollow <用户名>` | 取消关注用户 |
| `bird followers` | 查看你的关注者 |
| `bird following` | 查看你关注的用户 |
| `bird lists` | 查看你的 Twitter 列表 |

## 输出选项

| 选项 | 描述 |
|--------|-------------|
| `--json` | 输出为 JSON 格式 |
| `--json-full` | 包含原始的 API 响应内容 |
| `--plain` | 纯文本输出（不含表情符号和颜色） |
| `--no-emoji` | 禁用表情符号 |
| `--no-color` | 禁用 ANSI 颜色显示 |
| `--timeout <毫秒>` | 请求超时时间 |

## 配置文件

配置信息从以下文件读取：
- `~/.config/bird/config.json5`
- `./.birdrc.json5`

支持的配置参数：
- `chromeProfile` | Chrome 浏览器的配置文件路径 |
- `firefoxProfile` | Firefox 浏览器的配置文件路径 |
- `cookieTimeoutMs` | cookie 提取的超时时间（以毫秒为单位） |
- `timeoutMs` | 请求的总超时时间（以毫秒为单位） |
- `quoteDepth` | 引用推文的最大深度

## 环境变量

| 变量 | 描述 |
|----------|-------------|
| `AUTH_TOKEN` | **必填** | Twitter 的认证令牌（auth_token） |
| `CT0` | **必填** | Twitter 的 ct0 令牌 |
| `NO_COLOR` | 禁用颜色显示 |
| `BIRD_TIMEOUT_MS` | 默认的超时时间（以毫秒为单位） |
| `BIRD COOKIE_TIMEOUT_MS` | 从 cookie 中提取令牌的超时时间（以毫秒为单位） |
| `BIRD_QUOTE_DEPTH` | 引用推文的最大深度 |

## 示例

```bash
# Check who's logged in
bird whoami

# Post a simple tweet
bird tweet "Hello world from OpenClaw!"

# Post with an image
bird tweet "Check this out!" --media ./image.png

# Reply to a tweet
bird reply 1234567890123456789 "Thanks for sharing!"

# Search for tweets about AI
bird search "artificial intelligence" --json

# Get your home timeline
bird home -n 20

# Read a tweet thread
bird thread https://x.com/user/status/1234567890

# Get trending topics
bird trending
```

## 故障排除

### 401 未授权错误
请确认 `AUTH_TOKEN` 和 `CT0` 已设置且有效。运行 `bird check` 命令进行验证。

### 令牌过期
Twitter 令牌会定期过期，请从浏览器 cookie 中重新复制令牌。

### 请求频率限制
Twitter 的 GraphQL API 有请求频率限制。请稍等几分钟后再尝试。

---

**总结**：使用 `bird` 工具，您可以快速地执行 Twitter/X 相关的操作，包括发布推文、回复推文、搜索推文以及管理个人时间线！只需设置 `AUTH_TOKEN` 和 `CT0` 令牌即可开始使用。