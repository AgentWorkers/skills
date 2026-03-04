---
name: x-poster
description: 使用 OpenTweet API 在 X（Twitter）上发布内容。您可以创建推文、安排发布时间、发布多条推文（即“线程”）、上传媒体文件、查看分析数据，并自主管理您在 X 上的内容。
version: 1.1.2
homepage: https://opentweet.io/features/openclaw-twitter-posting
user-invocable: true
metadata: {"openclaw":{"requires":{"env":["OPENTWEET_API_KEY"]},"primaryEnv":"OPENTWEET_API_KEY"}}
---
# OpenTweet X 发布器

您可以使用 OpenTweet REST API 在 X（Twitter）上发布内容。所有请求都会发送到 `https://opentweet.io`，并需要使用用户的 API 密钥。

## 认证

每个请求都必须包含以下头部信息：
```
Authorization: Bearer $OPENTWEET_API_KEY
Content-Type: application/json
```

对于文件上传，请使用 `Content-Type: multipart/form-data`。

## 开始使用前

**务必先验证连接是否正常：**
```
GET https://opentweet.io/api/v1/me
```
该请求会返回订阅状态、每日发帖限制以及剩余发帖数量。在安排或发布内容之前，请确保 `subscription.has_access` 为 `true` 且 `limits_remaining_posts_today` 大于 0。

## 发帖管理

### 创建推文
```
POST https://opentweet.io/api/v1/posts
Body: { "text": "Your tweet text" }
```
可选地添加 `"scheduled_date": "2026-03-01T10:00:00Z"` 以安排发帖时间（需要激活订阅，日期必须在未来）。

### 立即创建并发布（一步完成）
```
POST https://opentweet.io/api/v1/posts
Body: { "text": "Hello from the API!", "publish_now": true }
```
该请求会同时创建推文并立即在 X 上发布。不能与 `scheduled_date` 选项或批量发帖结合使用。成功时，响应中会包含 `status: "posted"`、`x_post_id` 和 `url`（实际的 X 推文链接）。

### 带有媒体的推文
```
POST https://opentweet.io/api/v1/posts
Body: {
  "text": "Check out this screenshot!",
  "media_urls": ["https://url-from-upload-endpoint"]
}
```
首先通过 `POST /api/v1/upload` 上传媒体文件，然后将返回的 URL 传递给 `media_urls`。

### 创建话题帖
```
POST https://opentweet.io/api/v1/posts
Body: {
  "text": "First tweet of the thread",
  "is_thread": true,
  "thread_tweets": ["Second tweet", "Third tweet"]
}
```

### 带有每条推文媒体的话题帖
```
POST https://opentweet.io/api/v1/posts
Body: {
  "text": "Thread intro with image",
  "is_thread": true,
  "thread_tweets": ["Second tweet", "Third tweet"],
  "media_urls": ["https://intro-image-url"],
  "thread_media": [["https://img-for-tweet-2"], []]
}
```
`thread_media` 是一个数组数组。每个内部数组包含对应推文的媒体 URL。对于没有媒体的推文，使用 `[]` 表示。

### 在 X 社区中发布内容
```
POST https://opentweet.io/api/v1/posts
Body: {
  "text": "Shared with the community!",
  "community_id": "1234567890",
  "share_with_followers": true
}
```

### 批量创建（最多 50 条推文）
```
POST https://opentweet.io/api/v1/posts
Body: {
  "posts": [
    { "text": "Tweet 1", "scheduled_date": "2026-03-01T10:00:00Z" },
    { "text": "Tweet 2", "scheduled_date": "2026-03-01T14:00:00Z" }
  ]
}
```

### 安排发帖时间
```
POST https://opentweet.io/api/v1/posts/{id}/schedule
Body: { "scheduled_date": "2026-03-01T10:00:00Z" }
```
日期必须在未来，并使用 ISO 8601 格式。

### 立即发布
```
POST https://opentweet.io/api/v1/posts/{id}/publish
```
不需要输入推文正文。内容会立即在 X 上发布。响应中会包含 `status: "posted"`、`x_post_id` 和 `url`（实际的 X 推文链接）。

### 批量安排发布（最多 50 条推文）
```
POST https://opentweet.io/api/v1/posts/batch-schedule
Body: {
  "schedules": [
    { "post_id": "id1", "scheduled_date": "2026-03-02T09:00:00Z" },
    { "post_id": "id2", "scheduled_date": "2026-03-03T14:00:00Z" }
  ],
  "community_id": "optional-community-id",
  "share_with_followers": true
}
```

### 列出所有推文
```
GET https://opentweet.io/api/v1/posts?status=scheduled&page=1&limit=20
```
状态选项：`scheduled`、`posted`、`draft`、`failed`

### 获取推文信息
```
GET https://opentweet.io/api/v1/posts/{id}
```

### 更新推文信息
```
PUT https://opentweet.io/api/v1/posts/{id}
Body: { "text": "Updated text", "media_urls": ["https://..."], "scheduled_date": "2026-03-01T10:00:00Z" }
```
所有字段均为可选。已发布的推文无法更新。将 `scheduled_date` 设置为 `null` 可以取消安排（将其恢复为草稿状态）。

### 删除推文
```
DELETE https://opentweet.io/api/v1/posts/{id}
```

## 媒体上传

### 上传图片或视频
```
POST https://opentweet.io/api/v1/upload
Content-Type: multipart/form-data
Body: file=@your-image.png
```
返回结果：`{ "url": "https://..." }`

支持的格式：JPG、PNG、GIF、WebP（最大 5MB）、MP4、MOV（最大 20MB）。

**工作流程**：先上传媒体文件，然后在创建或更新推文时使用返回的 URL。

## 分析

### 账户概览
```
GET https://opentweet.io/api/v1/analytics/overview
```
返回发布统计信息（总推文数、发布频率、活跃天数、平均每周推文数、最活跃的小时/天数、话题帖数量、媒体使用情况），以及发布 streak（当前和最长 streak）、趋势数据（本周与上周、本月与上月对比）、类别分布和最近活动（过去 7 天和 30 天的每日数据）。

### 推文互动指标（仅限高级计划）
```
GET https://opentweet.io/api/v1/analytics/tweets?period=30
```
返回每条推文的互动数据：点赞数、转发数、回复数、引用数、展示次数、书签数以及互动率。还包括表现最佳的/最差的推文、内容类型统计、互动时间线以及最佳发布时间。时间范围：7-365 天或“全部”。

### 关注者增长
```
GET https://opentweet.io/api/v1/analytics/followers?days=30
```
返回随时间变化的关注者数量、当前关注者数量、净增长量和增长百分比。时间范围：7-365 天或“全部”。

### 最佳发布时间
```
GET https://opentweet.io/api/v1/analytics/best-times
```
分析您的发布模式以找到最佳发布时间。至少需要发布 3 条推文才能使用此功能。

### 增长速度和预测
```
GET https://opentweet.io/api/v1/analytics/growth
```
返回每日/每周/每月的增长率、增长加速度、达到关注者里程碑的预计时间，以及发布活动与增长之间的相关性。

## 常见工作流程

**首先：验证连接是否正常：**
1. `GET /api/v1/me` — 检查 `authenticated` 是否为 `true`，`subscription.has_access` 是否为 `true`。

**立即发布推文（两步完成）：**
1. `GET /api/v1/me` — 检查 `limits.can_post` 是否为 `true`
2. 创建推文：`POST /api/v1/posts` 并输入文本内容
3. 发布推文：`POST /api/v1/posts/{id}/publish`

**立即发布推文（一步完成）：**
1. `GET /api/v1/me` — 检查 `limits.can_post` 是否为 `true`
2. `POST /api/v1/posts` 并输入 `{"text": "...", "publish_now": true}`

**带图片的推文：**
1. `GET /api/v1/me` — 检查发帖限制
2. 上传图片：`POST /api/v1/upload` 并获取返回的 URL
3. 创建推文：`POST /api/v1/posts` 并输入 `{"text": "...", "media_urls": ["<url>"]`
4. 发布推文：`POST /api/v1/posts/{id}/publish`

**安排推文时间：**
1. `GET /api/v1/me` — 检查 `limits_remaining_posts_today` 是否大于 0
2. 一次性创建并安排推文：`POST /api/v1/posts` 并输入文本内容和 `scheduled_date`

**安排一周的内容：**
1. `GET /api/v1/me` — 检查剩余的发布限制
2. 批量创建推文：`POST /api/v1/posts` 并输入包含 `scheduled_date` 的推文数组

**创建带媒体的话题帖：**
1. 为每张图片分别上传：`POST /api/v1/upload`
2. 创建推文：`POST /api/v1/posts` 并输入 `is_thread`、`thread_tweets`、`media_urls`（第一条推文）和 `thread_media`（后续推文）

**批量安排草稿：**
1. 创建草稿：`POST /api/v1/posts` 并输入推文数组
2. 批量安排：`POST /api/v1/posts/batch-schedule` 并输入推文 ID 和安排时间

**发布前查看分析数据：**
1. `GET /api/v1/analytics/best-times` — 查找最佳发布时间
2. `GET /api/v1/analytics/overview` — 查看发布趋势
3. 根据建议的最佳时间安排推文

## 重要规则
- 在安排或发布内容之前，务必先调用 `GET /api/v1/me` 以检查发帖限制。
- 重要提示：始终解析并使用 API 返回的 JSON 数据。切勿伪造或假设响应值。
- 推文 ID 总是 24 个字符的 MongoDB ObjectId（例如 "507f1f77bcf86cd799439011"），不能使用简短字符串。
- 所有推文响应中都会包含 `status` 字段：`draft`、`scheduled`、`posted` 或 `failed`。
- 已发布的推文会包含 `url` 字段，其中包含实际的 X 推文链接。请始终使用该链接，切勿自行构建链接。
- 要确认推文已发布，请检查 `status` 是否为 `posted` 且 `url` 是否存在。
- 每条推文的长度限制为 280 个字符。
- 每次请求最多可发布 50 条推文。
- 请求速率限制：普通用户每分钟 60 次，高级用户每分钟 1,000 次；每日 300 次，高级用户每分钟 1,000 次。
- 日期必须使用 ISO 8601 格式且必须在未来。
- 安排或发布内容需要激活订阅（创建草稿无需订阅）。
- 在 `POST /api/v1/posts` 中包含 `scheduled_date` 需要订阅。
- 在创建推文之前请上传媒体文件——使用返回的 URL 设置 `media_urls` 或 `thread_media`。
- 媒体文件大小限制：图片（JPG、PNG、GIF、WebP）最大 5MB，视频（MP4、MOV）最大 20MB。
- 推文互动分析功能需要高级计划（高级计划用户才能使用，否则会返回 403 错误代码）。
- 403 错误表示未订阅；429 错误表示达到每日发帖限制。
- 检查响应状态码：201 表示创建成功，200 表示成功，4xx 表示客户端错误，5xx 表示服务器错误。

## 完整 API 文档
更多详细信息请访问：https://opentweet.io/api/v1/docs