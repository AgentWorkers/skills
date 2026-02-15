---
name: postiz
description: |
  Schedule and manage social media posts via Postiz API (self-hosted or cloud).
  Direct API integration — no n8n dependency.
  Supports X/Twitter, LinkedIn, Bluesky with platform-specific character limits.
  Includes deduplication, scheduling, media upload, and thread creation.

  WHAT IT CAN DO:
  - Schedule posts to 28+ channels (X, LinkedIn, Bluesky, Reddit, Instagram, Facebook, Threads, YouTube, TikTok, Pinterest, Mastodon, and more)
  - Multi-platform posting in a single API call with platform-adapted content
  - X/Twitter thread creation for longer content
  - Media upload (file and URL)
  - Find next available posting slot per channel
  - List, query, update, and delete scheduled posts
  - Deduplication workflow (check existing before posting)
  - Platform-specific character limits and content tone guidance
  - Post state management (QUEUE, PUBLISHED, ERROR, DRAFT)
  - Helper script for quick posting with auto-validation

  USE WHEN: scheduling social media posts, creating multi-platform content, managing a posting calendar, uploading media for social posts, checking post status, creating X/Twitter threads, or automating social media workflows.
---

# Postiz 社交媒体调度器

支持直接通过 API 发布社交媒体内容，无需使用 n8n 工作流程。

## 设置

### 所需的环境变量

```bash
# Core configuration
export POSTIZ_URL="https://your-postiz-instance.com"
export POSTIZ_EMAIL="your@email.com"
export POSTIZ_PASSWORD="your-password"

# Integration IDs (get from Postiz dashboard → Integrations)
export POSTIZ_X_ID="your-x-integration-id"
export POSTIZ_LINKEDIN_ID="your-linkedin-integration-id"
export POSTIZ_BLUESKY_ID="your-bluesky-integration-id"
```

要获取您的集成 ID，请按照以下步骤操作：
1. 登录 Postiz 控制面板
2. 转到 **集成** 或 **渠道** 面板
3. 每个已连接的账户都会显示一个 ID（或者使用 API：`GET /api/integrations/list`）

## 平台限制

| 平台 | 字符限制 | 说明 |
|----------|-----------------|-------|
| X/Twitter | **280** | 链接算作 23 个字符（使用 t.co 简短链接） |
| LinkedIn | **3,000** | 预览中仅显示前 140 个字符 |
| Bluesky | **300** | 目标受众为技术或开发者群体 |

## 平台内容指南

### X/Twitter（280 个字符）
- 内容简短精炼
- 最多使用 1-2 个标签
- 长内容请分多条推文发布

### LinkedIn（3,000 个字符）
- 保持专业的语气
- 可以使用更长的内容
- 标签放在内容末尾（建议使用 3-5 个）
- 预览中仅显示前 140 个字符——请确保这些字符对用户有吸引力！

### Bluesky（300 个字符）
- 与 X 类似，但允许稍长的内容
- 不支持官方标签（请谨慎使用）
- 目标受众为技术或开发者群体

## 认证

```bash
# Login and save cookie (required before any API call)
curl -s -c /tmp/postiz-cookies.txt \
  "$POSTIZ_URL/api/auth/login" \
  -H 'Content-Type: application/json' \
  -d "{\"email\":\"$POSTIZ_EMAIL\",\"password\":\"$POSTIZ_PASSWORD\",\"provider\":\"LOCAL\"}"
```

Cookie 会定期过期。如果遇到 401 错误，请重新登录。

## 查找下一个可用时间槽

```bash
curl -s -b /tmp/postiz-cookies.txt \
  "$POSTIZ_URL/api/posts/find-slot/$POSTIZ_X_ID"
```

该功能可返回指定渠道的下一个可用发布时间，便于自动调度以避免冲突。

## 从 URL 上传媒体文件

```bash
curl -s -b /tmp/postiz-cookies.txt \
  "$POSTIZ_URL/api/media/upload-from-url" \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://example.com/image.png"}'
```

## 创建帖子

### 单一平台发布计划

```bash
curl -s -b /tmp/postiz-cookies.txt \
  "$POSTIZ_URL/api/posts" \
  -H 'Content-Type: application/json' \
  -d "{
    \"type\": \"schedule\",
    \"date\": \"2026-02-05T15:00:00Z\",
    \"posts\": [{
      \"integration\": {\"id\": \"$POSTIZ_X_ID\"},
      \"value\": [{\"content\": \"Your tweet here (max 280 chars)\", \"image\": []}],
      \"settings\": {\"__type\": \"x\"}
    }]
  }"
```

### 多平台发布（内容适配）

```bash
curl -s -b /tmp/postiz-cookies.txt \
  "$POSTIZ_URL/api/posts" \
  -H 'Content-Type: application/json' \
  -d "{
    \"type\": \"schedule\",
    \"date\": \"2026-02-05T15:00:00Z\",
    \"posts\": [
      {
        \"integration\": {\"id\": \"$POSTIZ_X_ID\"},
        \"value\": [{\"content\": \"Short X version (280 chars max)\", \"image\": []}],
        \"settings\": {\"__type\": \"x\"}
      },
      {
        \"integration\": {\"id\": \"$POSTIZ_LINKEDIN_ID\"},
        \"value\": [{\"content\": \"Longer LinkedIn version with more context and professional tone. Can be up to 3000 characters.\", \"image\": []}],
        \"settings\": {\"__type\": \"linkedin\"}
      },
      {
        \"integration\": {\"id\": \"$POSTIZ_BLUESKY_ID\"},
        \"value\": [{\"content\": \"Bluesky version (300 chars max)\", \"image\": []}],
        \"settings\": {\"__type\": \"bluesky\"}
      }
    ]
  }"
```

### 发布类型
- `schedule` — 在指定日期/时间自动发布
- `draft` — 保存以供审核（不会自动发布）
- `now` — 立即发布

## 列出和查询帖子

### 按日期范围获取帖子（必选！）

```bash
curl -s -b /tmp/postiz-cookies.txt \
  "$POSTIZ_URL/api/posts?startDate=2026-02-01T00:00:00Z&endDate=2026-02-08T00:00:00Z" \
  | jq '.posts[] | {id, state, publishDate, platform: .integration.providerIdentifier, content: .content[0:60]}'
```

### 发布前检查重复内容

```bash
# Get recent posts and check content similarity
curl -s -b /tmp/postiz-cookies.txt \
  "$POSTIZ_URL/api/posts?startDate=2026-02-01T00:00:00Z&endDate=2026-02-08T00:00:00Z" \
  | jq -r '.posts[] | "\(.integration.providerIdentifier): \(.content[0:80])"'
```

## 帖子状态

| 状态 | 说明 |
|-------|-------------|
| `QUEUE` | 已安排，等待发布 |
| `PUBLISHED` | 发布成功 |
| `ERROR` | 发布失败 |
| `DRAFT` | 保存但未安排发布 |

## 媒体上传

### 上传图片

```bash
# Upload returns {id, path}
curl -s -b /tmp/postiz-cookies.txt \
  "$POSTIZ_URL/api/media/upload-simple" \
  -F 'file=@/path/to/image.png'
```

### 在帖子中使用媒体文件

```json
"value": [{
  "content": "Post with image",
  "image": [{"id": "MEDIA_ID", "path": "/uploads/..."}]
}]
```

## Twitter/X 的多条推文

对于较长的内容，可以在 X 上创建多条推文：

```json
"value": [
  {"content": "Tweet 1/3: Introduction to the topic...", "image": []},
  {"content": "Tweet 2/3: The main point explained...", "image": []},
  {"content": "Tweet 3/3: Conclusion and call to action.", "image": []}
]
```

## 管理帖子

### 删除帖子

```bash
curl -s -b /tmp/postiz-cookies.txt -X DELETE \
  "$POSTIZ_URL/api/posts/POST_ID"
```

### 更新发布计划

```bash
curl -s -b /tmp/postiz-cookies.txt -X PUT \
  "$POSTIZ_URL/api/posts/POST_ID/date" \
  -H 'Content-Type: application/json' \
  -d '{"date": "2026-02-06T10:00:00Z"}'
```

## 最佳实践

### 避免重复
- 在创建新帖子前，请务必查询现有帖子
- 在内容中使用唯一的标识符（如日期、具体引用）
- 检查帖子的 `QUEUE` 和 `PUBLISHED` 状态

### 发布计划
- 每个平台之间的发布间隔至少为 2-4 小时
- 最佳发布时间：上午 9 点、中午 12 点、下午 5 点（根据受众时区）
- 避免同时在所有平台上发布相同的内容

### 内容适配
- 不要直接截断内容！请为每个平台重新编写：
  - **X**：包含吸引人的开头、关键信息以及行动号召（CTA）
  - **LinkedIn**：提供背景信息、价值主张以及引导用户互动的问题
  - **Bluesky**：使用轻松、适合技术受众的语言风格

## 辅助脚本

### 向多个平台发布帖子

```bash
# Single platform
uv run scripts/post.py \
  --platform x \
  --content "Your tweet here" \
  --schedule "2026-02-05T15:00:00Z"

# Multi-platform with different content
uv run scripts/post.py \
  --x "Short X version" \
  --linkedin "Longer LinkedIn version with more detail" \
  --bluesky "Bluesky version" \
  --schedule "2026-02-05T15:00:00Z"

# Post immediately
uv run scripts/post.py \
  --platform x \
  --content "Posting now!" \
  --now

# Validate without posting
uv run scripts/post.py \
  --x "Test content" \
  --validate
```

### 检查重复内容

```bash
# Check last 30 days
uv run scripts/check_duplicates.py

# Check last 7 days
uv run scripts/check_duplicates.py --days 7

# Check if specific content would be duplicate
uv run scripts/check_duplicates.py --content "Your proposed post content"
```

## 故障排除

### 401 未授权错误
重新运行登录命令以刷新 Cookie。

### 帖子无法发布
1. 确认帖子状态为 `QUEUE` 而非 `DRAFT`
2. 确认发布日期在未来
3. 检查集成是否仍在 UI 中正常连接

### 帖子重复
在创建新帖子前，请务必检查现有内容。API 不会自动检测重复内容。

### 缺少环境变量
脚本会提示您缺少哪些环境变量，请在 shell 或 `.env` 文件中设置它们：
```bash
export POSTIZ_URL="https://your-postiz.example.com"
export POSTIZ_EMAIL="your@email.com"
export POSTIZ_PASSWORD="your-password"
export POSTIZ_X_ID="your-integration-id"
```