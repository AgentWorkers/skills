---
name: publora
description: **Publora API** — 用于在11个平台上（X/Twitter、LinkedIn、Instagram、Threads、TikTok、YouTube、Facebook、Bluesky、Mastodon、Telegram、Pinterest）安排和发布社交媒体帖子。当用户需要发布、安排发布时间、草拟帖子、批量安排发布、管理工作空间用户、配置Webhook或通过Publora获取LinkedIn分析数据时，可以使用此功能。
---
# Publora API — 核心功能

Publora 是一个价格合理的 REST API，用于在 11 个平台上安排和发布社交媒体帖子。基础 URL 为：`https://api.publora.com/api/v1`

## 认证

所有请求都需要包含 `x-publora-key` 头部字段。该密钥以 `sk_` 开头。

```bash
curl https://api.publora.com/api/v1/platform-connections \
  -H "x-publora-key: sk_YOUR_KEY"
```

获取您的密钥：[publora.com](https://publora.com) → 设置 → API 密钥 → 生成 API 密钥。
⚠️ 请立即复制密钥——此信息仅显示一次。

## 第 0 步：获取平台 ID

在发布帖子之前，请务必先调用此接口以获取有效的平台 ID。

```javascript
const res = await fetch('https://api.publora.com/api/v1/platform-connections', {
  headers: { 'x-publora-key': 'sk_YOUR_KEY' }
});
const { connections } = await res.json();
// connections[i].platformId → e.g. "linkedin-ABC123", "twitter-456"
// Also returns: tokenStatus, tokenExpiresIn, lastSuccessfulPost, lastError
```

平台 ID 的格式如下：`twitter-123`、`linkedin-ABC`、`instagram-456`、`threads-789` 等。

## 立即发布

省略 `scheduledTime` 参数即可立即发布帖子：

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Your post content here',
    platforms: ['twitter-123', 'linkedin-ABC']
  })
});
```

## 安排帖子发布

请在请求中包含 ISO 8601 UTC 格式的 `scheduledTime` 参数——时间必须在未来：

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Scheduled post content',
    platforms: ['twitter-123', 'linkedin-ABC'],
    scheduledTime: '2026-03-16T10:00:00.000Z'
  })
});
// Response: { postGroupId: "pg_abc123", scheduledTime: "..." }
```

## 保存为草稿

省略 `scheduledTime` 参数——帖子将作为草稿保存，稍后可以安排发布：

```javascript
// Create draft
const { postGroupId } = await createPost({ content, platforms });

// Schedule later
await fetch(`https://api.publora.com/api/v1/update-post/${postGroupId}`, {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({ status: 'scheduled', scheduledTime: '2026-03-16T10:00:00.000Z' })
});
```

## 列出帖子

您可以过滤、分页和排序已安排或已发布的帖子：

```javascript
// GET /api/v1/list-posts
// Query params: status, platform, fromDate, toDate, page, limit, sortBy, sortOrder
const res = await fetch(
  'https://api.publora.com/api/v1/list-posts?status=scheduled&platform=twitter&page=1&limit=20',
  { headers: { 'x-publora-key': 'sk_YOUR_KEY' } }
);
const { posts, pagination } = await res.json();
// pagination: { page, limit, totalItems, totalPages, hasNextPage, hasPrevPage }
```

有效的帖子状态包括：`draft`（草稿）、`scheduled`（已安排）、`published`（已发布）、`failed`（发布失败）和 `partially_published`（部分发布）。

## 获取/删除帖子

```bash
# Get post details
GET /api/v1/get-post/:postGroupId

# Delete post (also removes media from storage)
DELETE /api/v1/delete-post/:postGroupId
```

## 查看帖子日志

用于调试发布失败或部分发布的帖子：

```javascript
const res = await fetch(
  `https://api.publora.com/api/v1/post-logs/${postGroupId}`,
  { headers: { 'x-publora-key': 'sk_YOUR_KEY' } }
);
const { logs } = await res.json();
```

## 测试连接

在发布帖子之前，请验证与各平台的连接是否正常：

```javascript
const res = await fetch(
  'https://api.publora.com/api/v1/test-connection/linkedin-ABC123',
  { method: 'POST', headers: { 'x-publora-key': 'sk_YOUR_KEY' } }
);
// Returns: { status: "ok"|"error", message, permissions, tokenExpiresIn }
```

## 批量安排发布（一周的内容）

```python
from datetime import datetime, timedelta, timezone
import requests

HEADERS = { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' }
base_date = datetime(2026, 3, 16, 10, 0, 0, tzinfo=timezone.utc)

posts = ['Monday post', 'Tuesday post', 'Wednesday post', 'Thursday post', 'Friday post']

for i, content in enumerate(posts):
    scheduled_time = base_date + timedelta(days=i)
    requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
        'content': content,
        'platforms': ['twitter-123', 'linkedin-ABC'],
        'scheduledTime': scheduled_time.isoformat()
    })
```

## 媒体上传

所有媒体文件（图片和视频）的上传流程分为三个步骤：
- **步骤 1**：`POST /api/v1/create-post` → 获取 `postGroupId`
- **步骤 2**：`POST /api/v1/get-upload-url` → 获取 `uploadUrl`
- **步骤 3**：使用 `uploadUrl` 和文件数据（上传到 S3 时无需身份验证）

```python
import requests

HEADERS = { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' }

# Step 1: Create post
post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'Check this out!',
    'platforms': ['instagram-456'],
    'scheduledTime': '2026-03-15T14:30:00.000Z'
}).json()
post_group_id = post['postGroupId']

# Step 2: Get pre-signed upload URL
upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
    'fileName': 'photo.jpg',
    'contentType': 'image/jpeg',
    'type': 'image',  # or 'video'
    'postGroupId': post_group_id
}).json()

# Step 3: Upload directly to S3 (no auth header needed)
with open('./photo.jpg', 'rb') as f:
    requests.put(upload['uploadUrl'], headers={'Content-Type': 'image/jpeg'}, data=f)
```

对于轮播图，需要使用相同的 `postGroupId` 调用 `get-upload-url` 多次。

## 跨平台多线程发布

X/Twitter 和 Threads 支持自动多线程发布。不同内容的段落请使用 `---` 分隔，并单独写在一行上：

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'First tweet in the thread.\n\n---\n\nSecond tweet continues.\n\n---\n\nFinal tweet wraps up.',
    platforms: ['twitter-123', 'threads-789']
  })
});
```

> ⚠️ **注意事项**：由于 Threads 应用的重新连接问题，目前 Threads 不支持多线程嵌套帖子（内容会自动拆分为独立的回复）。单条帖子和轮播图的功能仍然正常。如需更新信息，请联系 support@publora.com。

## LinkedIn 分析

```javascript
// Post statistics
await fetch('https://api.publora.com/api/v1/linkedin-post-statistics', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    postedId: 'urn:li:share:7123456789',
    platformId: 'linkedin-ABC123',
    queryTypes: 'ALL'  // or: IMPRESSION, MEMBERS_REACHED, RESHARE, REACTION, COMMENT
  })
});

// Profile summary (followers + aggregated stats)
await fetch('https://api.publora.com/api/v1/linkedin-profile-summary', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({ platformId: 'linkedin-ABC123' })
});
```

可用的分析接口包括：
| 接口 | 描述 |
|--------|---------|
| `POST /linkedin-post-statistics` | 获取帖子的浏览量、互动量和分享次数 |
| `POST /linkedin-account-statistics` | 获取账户的汇总数据 |
| `POST /linkedin-followers` | 获取关注者数量及增长情况 |
| `POST /linkedin-profile-summary` | 获取账户概览 |
| `POST /linkedin-create-reaction` | 对帖子做出反应 |
| `DELETE /linkedin-delete-reaction` | 删除对帖子的反应 |

## Webhook

当帖子发布、发布失败或令牌过期时，您可以接收实时通知：

```javascript
// Create a webhook
await fetch('https://api.publora.com/api/v1/webhooks', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    name: 'My webhook',
    url: 'https://myapp.com/webhooks/publora',
    events: ['post.published', 'post.failed', 'token.expiring']
  })
});
// Returns: { webhook: { _id, name, url, events, secret, isActive } }
// Save the `secret` — it's only shown once. Use it to verify webhook signatures.
```

有效的事件类型包括：`post.scheduled`、`post.published`、`post.failed` 和 `token.expiring`

| 接口 | 方法 | 描述 |
|--------|--------|-------------|
| `/webhooks` | GET | 列出所有 Webhook |
| `/webhooks` | POST | 创建新的 Webhook |
| `/webhooks/:id` | PATCH | 更新 Webhook 设置 |
| `/webhooks/:id` | DELETE | 删除 Webhook |
| `/webhooks/:id/regenerate-secret` | POST | 重新生成 Webhook 密钥 |

每个账户最多可以设置 10 个 Webhook。

## 工作区 API（B2B）

您可以通过工作区账户管理多个用户。如需启用工作区 API 功能，请联系 serge@publora.com。

```javascript
// Create a managed user
const user = await fetch('https://api.publora.com/api/v1/workspace/users', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_CORP_KEY' },
  body: JSON.stringify({ email: 'client@example.com', displayName: 'Acme Corp' })
}).then(r => r.json());

// Generate connection URL for user to connect their social accounts
const { connectionUrl } = await fetch(
  `https://api.publora.com/api/v1/workspace/users/${user.id}/connection-url`,
  { method: 'POST', headers: { 'x-publora-key': 'sk_CORP_KEY' } }
).then(r => r.json());

// Post on behalf of managed user
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-publora-key': 'sk_CORP_KEY',
    'x-publora-user-id': user.id  // ← key header for acting on behalf of a user
  },
  body: JSON.stringify({ content: 'Post for Acme Corp!', platforms: ['linkedin-XYZ'] })
});
```

工作区相关的接口包括：
| 接口 | 方法 | 描述 |
|--------|--------|-------------|
| `/workspace/users` | GET | 列出受管理的用户 |
| `/workspace/users` | POST | 创建受管理的用户 |
| `/workspace/users/:userId` | DELETE | 删除受管理的用户 |
| `/workspace/users/:userId/api-key` | POST | 为每个用户生成 API 密钥 |
| `/workspace/users/:userId/connection-url` | POST | 生成每个用户的 OAuth 连接链接 |

每个受管理的用户每天最多可以发布 100 条帖子（`dailyPostsLeft`）。请勿在客户端暴露您的工作区 API 密钥——请使用为每个用户生成的 API 密钥。

## 平台限制快速参考（API）

> ⚠️ API 的限制通常比原生应用程序更严格。在开发时请务必考虑这些限制。

| 平台 | 字符限制 | 最大图片数量 | 最大视频文件大小 | 只能上传文本？ |
|--------|-----------|-----------|-----------|------------|
| Twitter/X | 280（高级账户为 25K） | 4 张图片，每张最大 5MB | 可上传 2 分钟内的视频，文件最大 512MB | ✅ |
| LinkedIn | 3,000 | 20 张图片，每张最大 5MB | 可上传时长 30 分钟内的视频，文件最大 500MB | ✅ |
| Instagram | 2,200 | 最多 10 张图片（仅支持 JPEG 格式），每张最大 8MB | 可上传时长 90 秒内的视频，文件最大 300MB | ❌ |
| Threads | 500 | 20 张图片，每张最大 8MB | 可上传时长 5 分钟内的视频，文件最大 500MB | ✅ |
| TikTok | 2,200 | 仅支持视频上传 | 可上传时长 10 分钟内的视频，文件最大 4GB | ❌ |
| YouTube | 5,000 条描述信息 | 仅支持视频上传 | 可上传时长 12 小时的视频，文件最大 256GB | ❌ |
| Facebook | 63,206 | 最多 10 张图片，每张最大 10MB | 可上传时长 45 分钟内的视频，文件最大 2GB | ✅ |
| Bluesky | 300 | 4 张图片，每张最大 1MB | 可上传时长 3 分钟内的视频，文件最大 100MB | ✅ |
| Mastodon | 500 | 4 张图片，每张最大 16MB | 可上传时长约 99 分钟内的视频 | ✅ |
| Telegram | 4,096 张图片（含 1,024 条说明文字），每张图片最大 10MB | 可上传时长 50 分钟内的视频（通过 Bot API） | ✅ |

有关完整的限制详情，请参阅 [Publora API 文档](https://github.com/publora/publora-api-docs) 中的 `docs/guides/platform-limits.md`。

## 平台特定功能

针对不同平台，提供了相应的设置、限制和示例：
- `publora-linkedin`：用于管理 LinkedIn 的帖子、分析数据和互动操作
- `publora-twitter`：用于管理 X/Twitter 的帖子和轮播图
- `publora-instagram`：用于管理 Instagram 的图片、Reels 和轮播图
- `publora-threads`：用于管理 Threads 的帖子
- `publora-tiktok`：用于管理 TikTok 的视频
- `publora-youtube`：用于管理 YouTube 的视频
- `publora-facebook`：用于管理 Facebook 页面的帖子
- `publora-bluesky`：用于管理 Bluesky 的帖子
- `publora-mastodon`：用于管理 Mastodon 的帖子
- `publora-telegram`：用于管理 Telegram 的频道

## 帖子状态

- `draft`：尚未安排发布
- `scheduled`：等待发布
- `published`：已成功发布
- `failed`：发布失败（请查看 `/post-logs`）
- `partially_published`：部分平台上的发布操作失败

## 错误代码及含义

| 错误代码 | 含义 |
|--------|---------|
| 400 | 请求无效（请检查 `scheduledTime` 的格式及必填字段） |
| 401 | API 密钥无效或缺失 |
| 403 | 达到平台使用限制或未启用工作区 API |
| 404 | 未找到帖子或资源 |
| 429 | 超过了平台的使用频率限制 |