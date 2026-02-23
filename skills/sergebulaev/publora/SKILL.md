---
name: publora
description: **Publora API** — 用于在10个社交媒体平台上（X/Twitter、LinkedIn、Instagram、Threads、TikTok、YouTube、Facebook、Bluesky、Mastodon、Telegram）安排和发布帖子。当用户需要通过Publora在任何社交媒体平台上发布、安排发布时间、起草内容或批量安排多条帖子时，可以使用此功能。
---
# Publora API — 核心功能

Publora 是一个价格合理的 REST API，用于在 10 个平台上安排和发布社交媒体帖子。基础 URL 为：`https://api.publora.com/api/v1`

## 认证

所有请求都需要包含 `x-publora-key` 头部字段。该密钥以 `sk_` 开头。

```bash
curl https://api.publora.com/api/v1/platform-connections \
  -H "x-publora-key: sk_YOUR_KEY"
```

获取您的密钥：[publora.com](https://publora.com) → 设置 → API 密钥 → 生成 API 密钥。
⚠️ 请立即复制密钥——此信息仅显示一次。

## 第 0 步：获取平台 ID

在发布内容之前，**务必先调用此步骤** 以获取有效的平台 ID。

```bash
GET /api/v1/platform-connections
```

```javascript
const res = await fetch('https://api.publora.com/api/v1/platform-connections', {
  headers: { 'x-publora-key': 'sk_YOUR_KEY' }
});
const { connections } = await res.json();
// connections[i].id → use this as platform ID (e.g. "linkedin-ABC123")
```

平台 ID 的格式如下：`twitter-123`、`linkedin-ABC`、`instagram-456`、`threads-789` 等。

## 立即发布

省略 `scheduledTime` 参数即可立即发布内容：

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

## 安排发布

请在请求中包含 `scheduledTime` 参数（格式需符合 ISO 8601 UTC 标准），且时间必须至少在 2 分钟之后：

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

省略 `scheduledTime` 参数——帖子将作为草稿保存，可稍后安排发布时间：

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

## 上传媒体文件（图片和视频）

上传媒体文件的步骤如下：
1. 创建帖子；
2. 获取上传 URL；
3. 将文件上传到 S3 存储服务。

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

视频的最大文件大小为：**512 MB**。

## 平台特定功能

如需了解各平台的特定设置和示例，请安装相应的插件：
- `publora-linkedin`：用于发布 LinkedIn 帖子
- `publora-twitter`：用于发布 X/Twitter 帖子和帖子串（Threads）
- `publora-instagram`：用于发布 Instagram 图片和视频
- `publora-threads`：用于发布 Threads 帖子
- `publora-tiktok`：用于发布 TikTok 视频
- `publora-youtube`：用于发布 YouTube 视频
- `publora-facebook`：用于发布 Facebook 帖子
- `publora-bluesky`：用于发布 Bluesky 帖子
- `publora-mastodon`：用于发布 Mastodon 帖子
- `publora-telegram`：用于发布 Telegram 直播

## 错误代码及含义

| 错误代码 | 含义 |
|------|---------|
| 400 | 请求无效（请检查 `scheduledTime` 的格式及必填字段） |
| 401 | API 密钥无效或缺失 |
| 403 | 免费计划的使用限制已达到（最多只能安排 5 条帖子的发布） |
| 404 | 帖子或资源未找到 |