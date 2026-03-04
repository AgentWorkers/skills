---
name: late
description: 通过命令行界面（CLI）在13个平台上安排和管理社交媒体帖子
version: 0.1.0
homepage: https://docs.getlate.dev
tags: [social-media, scheduling, instagram, tiktok, twitter, linkedin, facebook, threads, youtube, bluesky, pinterest, reddit, snapchat, telegram]
metadata:
  env:
    - LATE_API_KEY (required) - Your Late API key from https://getlate.dev/settings/api
    - LATE_API_URL (optional) - Defaults to https://getlate.dev/api
---
# Late CLI

该工具允许您通过终端或AI代理，在13个社交媒体平台上（Instagram、TikTok、X/Twitter、LinkedIn、Facebook、Threads、YouTube、Bluesky、Pinterest、Reddit、Snapchat、Telegram、Google Business）安排并发布帖子。

## 设置

```bash
npm install -g late
late auth:set --key "sk-your-api-key"
late auth:check  # verify it works
```

或者直接设置环境变量：`export LATE_API_KEY="sk-your-api-key"`

## 核心工作流程

安排帖子的典型步骤如下：

```bash
# 1. See your profiles
late profiles:list

# 2. See connected social accounts
late accounts:list

# 3. Schedule a post
late posts:create --text "Hello world!" --accounts <accountId1>,<accountId2> --scheduledAt "2025-01-15T10:00:00Z"

# 4. Check post status
late posts:list --status scheduled

# 5. View analytics (requires analytics add-on)
late analytics:posts --profileId <profileId>
```

## 输出格式

所有命令默认以JSON格式输出（适用于AI代理和管道传输）。若需要格式化输出，请添加`--pretty`参数。

错误信息始终以以下格式返回：`{"error": true, "message": "...", "status": 401}`

## 命令参考

### 认证

```bash
# Save API key
late auth:set --key "sk-your-api-key"

# Optionally set custom API URL
late auth:set --key "sk-..." --url "https://custom.api.url/api/v1"

# Verify key works
late auth:check
```

### 账户信息（个人资料）

```bash
# List all profiles
late profiles:list

# Create a profile
late profiles:create --name "My Brand"

# Get profile details
late profiles:get <profileId>

# Update profile
late profiles:update <profileId> --name "New Name"

# Delete profile (must have no connected accounts)
late profiles:delete <profileId>
```

### 账户（社交媒体连接）

```bash
# List all connected accounts
late accounts:list

# Filter by profile or platform
late accounts:list --profileId <id> --platform instagram

# Get single account
late accounts:get <accountId>

# Check health of all accounts (rate limits, token expiry)
late accounts:health
```

### 发布帖子

```bash
# Publish immediately
late posts:create --text "Hello!" --accounts <id1>,<id2>

# Schedule for later
late posts:create --text "Scheduled post" --accounts <id> --scheduledAt "2025-06-01T14:00:00Z"

# Save as draft
late posts:create --text "Draft idea" --accounts <id> --draft

# With media
late posts:create --text "Check this out" --accounts <id> --media "https://example.com/image.jpg"

# With title (YouTube, Reddit)
late posts:create --text "Description" --accounts <id> --title "My Video Title"

# List posts with filters
late posts:list --status published --page 1 --limit 20
late posts:list --profileId <id> --from "2025-01-01" --to "2025-01-31"
late posts:list --search "product launch"

# Get post details
late posts:get <postId>

# Delete a post
late posts:delete <postId>

# Retry a failed post
late posts:retry <postId>
```

### 分析数据（需安装分析插件）

```bash
# Post analytics
late analytics:posts --profileId <id>
late analytics:posts --postId <postId>
late analytics:posts --platform instagram --sortBy engagement

# Daily metrics
late analytics:daily --accountId <id> --from "2025-01-01" --to "2025-01-31"

# Best posting times
late analytics:best-time --accountId <id>
```

### 媒体文件上传

```bash
# Upload a file (returns URL for use in posts:create --media)
late media:upload ./photo.jpg
late media:upload ./video.mp4
```

## 平台特定示例

### Instagram Reel（Instagram短视频）

```bash
late media:upload ./reel.mp4
# Use the returned URL:
late posts:create --text "New reel!" --accounts <instagramAccountId> --media "<returned-url>"
```

### 多平台同时发布帖子

```bash
late posts:create \
  --text "Big announcement!" \
  --accounts <instagramId>,<twitterId>,<linkedinId> \
  --media "https://example.com/image.jpg" \
  --scheduledAt "2025-06-01T09:00:00Z" \
  --timezone "America/New_York"
```

### Threads与Twitter同时发布

```bash
late posts:create --text "Thoughts on AI agents..." --accounts <threadsId>,<twitterId>
```

## 支持的平台

Instagram、TikTok、X（Twitter）、LinkedIn、Facebook、Threads、YouTube、Bluesky、Pinterest、Reddit、Snapchat、Telegram、Google Business Profile。

## 错误处理

常见错误及其含义：
- `401` - API密钥无效或缺失
- `402` - 某项功能需要付费插件（例如分析数据）
- `403` - 计划使用次数达到上限或权限不足
- `404` - 资源未找到
- `429` - 账户被限制使用（处于冷却期）

## 对AI代理的建议

- 在创建帖子之前，务必先使用`late accounts:list`获取有效的账户ID。
- 发布帖子前，使用`late accounts:health`检查账户是否被限制使用。
- 可以使用`late posts:get`根据`late posts:create`返回的ID来查看帖子的发布状态。
- 对于包含多张图片的帖子，先使用`late media:upload`上传每张图片，然后将所有图片的URL用逗号分隔后传递给`--media`参数。
- 为确保帖子能够可靠地发布，请至少提前5分钟进行安排。