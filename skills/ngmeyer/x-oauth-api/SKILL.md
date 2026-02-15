---
name: x-oauth-api
description: 使用官方的 OAuth 1.0a API 将内容发布到 X（Twitter）上。该 API 支持免费 tier（基础功能）。
metadata:
  { "openclaw": { "requires": { "env": ["X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_TOKEN_SECRET"] } } }
---

# X OAuth API 技能

使用官方的 X API 和 OAuth 1.0a 认证方式，向 X（原名 Twitter）发布内容。

## 概述

该技能提供了直接访问 X API v2 的功能，可用于发布推文、管理话题以及监控提及信息。无需使用代理或第三方服务，直接使用您的 X API 凭据即可进行操作。

**适用场景：**
- 用户请求“在 X 上发布内容”、“发这条推文”或“在 Twitter 上发布”
- 需要创建话题或媒体帖子
- 希望查看提及信息或回复评论

## 快速入门

### 1. 配置 X API 凭据

请将以下环境变量（来自您的 X 开发者账户）保存到系统中：
```
X_API_KEY              # Consumer Key (API Key)
X_API_SECRET           # Consumer Secret
X_ACCESS_TOKEN         # Access Token
X_ACCESS_TOKEN_SECRET  # Access Token Secret
X_USER_ID              # Optional: Your numeric user ID (speeds up mentions)
```

### 免费 tier 与付费 tier

**免费 tier 支持的功能：**
- ✅ 发布推文和话题
- ✅ 删除推文
- ✅ 查看账户信息（`x me`）

**需要 Basic+ tier 才能使用的功能：**
- 🔒 搜索推文
- 🔒 获取提及信息
- 🔒 上传媒体文件

### 2. 基本用法

```bash
# Post a simple tweet
x post "Hello from X API"

# Post a thread
x thread "First tweet" "Second tweet" "Third tweet"

# Check mentions
x mentions --limit 10

# Search recent tweets
x search "AI agents" --limit 5
```

## 命令

### `x post <text>`
发布一条推文。

**可选参数：**
- `--reply-to <tweet-id>` - 回复特定的推文
- `--quote <tweet-id>` - 引用某条推文
- `--media <file>` - 附加图片/视频

**示例：**
```bash
x post "Check this out" --media image.jpg
```

### `x thread <tweet1> <tweet2> ...`
发布一个包含多条推文的话题。

**示例：**
```bash
x thread \
  "Thread about AI" \
  "Here's what I learned" \
  "Most important takeaway"
```

### `x mentions [options]`
获取您账户的最近提及信息。

**可选参数：**
- `--limit <n>` - 提及信息的数量（默认：10，最大：100）
- `--since <tweet-id>` - 仅获取该 ID 之后的提及信息
- `--format json` - 以 JSON 格式输出

**注意：** 需要 `X_USER_ID` 环境变量；否则系统会自动获取该信息（但速度较慢）。

### `x search <query> [options]`
搜索最近的推文。

**可选参数：**
- `--limit <n>` - 搜索结果的数量（默认：10，最大：100）
- `--format json` - 以 JSON 格式输出

### `x delete <tweet-id>`
删除一条推文。

### `x me`
显示当前账户的信息（名称、用户名、关注者数量、用户 ID）。

## API 使用频率限制

X API v2 对每个端点都设置了使用频率限制：

| 端点 | 使用频率限制 | 限制时间窗口 |
|----------|-------|--------|
| POST /2/tweets | 200 次/15 分钟（免费 tier） |
| GET /2/tweets/search/recent | 100 次/15 分钟（免费 tier） |
| GET /2/users/:id/mentions | 100 次/15 分钟（免费 tier） |

不同使用等级的频率限制可能有所不同。详情请参阅 [X API 文档](https://developer.twitter.com/en/docs/twitter-api/rate-limits)。

## 认证

OAuth 1.0a 的认证过程是透明的。只需通过环境变量提供您的凭据，该技能会自动为所有请求添加认证信息。

## 示例

### 带附件发布推文
```bash
x post "Check out this screenshot" --media screenshot.png
```

### 回复推文
```bash
x post "Great point!" --reply-to 1234567890123456789
```

### 创建一个包含三条推文的话题
```bash
x thread \
  "Just launched x-oauth-api skill" \
  "It lets you post to X directly from your agent" \
  "No proxies, direct OAuth 1.0a authentication"
```

### 搜索并回复推文
```bash
# Find interesting tweets
x search "agent framework"

# Reply to one
x post "Have you tried this?" --reply-to 1234567890123456789
```

## 故障排除

**出现 “Unauthorized” 错误**
- 确保 X API 凭据正确
- 验证环境变量中是否已设置正确的凭据
- 确保您的应用程序在 X 开发者门户中具有写入权限

**出现 “Rate limit exceeded” 错误**
- 等待 15 分钟后重试
- 减少请求频率
- 查看 [X 开发者门户](https://developer.twitter.com/en/portal/dashboard) 上的频率限制信息

**出现 “This endpoint requires a paid X API tier” 错误**
- 搜索和获取提及信息需要 Basic+ 级别的权限
- 免费 tier 仅支持发布、删除和查看账户信息
- 可在 [https://developer.twitter.com/en/portal/products] 升级账户等级

**推文无法发布**
- 确保推文内容长度不超过 280 个字符（使用 X Premium 服务时长度限制为 4000 个字符）
- 检查是否存在特殊的格式问题
- 查看 [api.twitterstat.us](https://api.twitterstat.us/) 上的 API 状态

## 所需条件**

- 拥有具备 API 访问权限的 X 开发者账户
- 配置了 OAuth 1.0a 凭据
- 能够访问 api.twitter.com

## 成本

免费。基本使用功能是免费的。请在 X 开发者门户中查看您的应用程序的使用频率限制。

## 技术支持

如有关于 X API 的问题，请参阅：[https://developer.twitter.com/en/docs/twitter-api]