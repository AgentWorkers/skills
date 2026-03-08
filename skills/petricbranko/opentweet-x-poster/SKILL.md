---
name: x-poster
description: 使用 OpenTweet API 在 X（Twitter）上发布内容。您可以创建推文、安排发布时间、发布多条推文（即“线程”）、上传媒体文件、查看分析数据，并自主管理您的 X 账户内容。
version: 1.1.3
homepage: https://opentweet.io/features/openclaw-twitter-posting
user-invocable: true
metadata: {"openclaw":{"requires":{"env":["OPENTWEET_API_KEY"]},"primaryEnv":"OPENTWEET_API_KEY"}}
---
# OpenTweet X 发布器

您可以使用 OpenTweet REST API 在 X（Twitter）上发布内容。所有请求都发送到 `https://opentweet.io`，并需要使用用户的 API 密钥。

## 认证

每个请求都需要以下请求头：
```
Authorization: Bearer $OPENTWEET_API_KEY
Content-Type: application/json
```

对于文件上传，请使用 `Content-Type: multipart/form-data`。

## 开始之前

**务必先验证连接：**
```
GET https://opentweet.io/api/v1/me
```
此操作会返回订阅状态、每日发布限制以及帖子数量。在安排或发布内容之前，请确保 `subscription.has_access` 为 `true` 且 `limits_remaining_posts_today` 大于 0。

## 发布管理

### 创建推文
```
POST https://opentweet.io/api/v1/posts
Body: { "text": "Your tweet text" }
```
可选地添加 `"scheduled_date": "2026-03-01T10:00:00Z"` 以安排发布时间（需要激活订阅，日期必须在未来）。

### 立即创建并发布（一步完成）
```
POST https://opentweet.io/api/v1/posts
Body: { "text": "Hello from the API!", "publish_now": true }
```
该操作会同时创建推文并将其发布到 X。不能与 `scheduled_date` 或批量发布结合使用。成功时，响应中会包含 `status: "posted"`、`x_post_id` 和 `url`（实际的 X 推文 URL）。

### 带有媒体的推文
```
POST https://opentweet.io/api/v1/posts
Body: {
  "text": "Check out this screenshot!",
  "media_urls": ["https://url-from-upload-endpoint"]
}
```
首先通过 `POST /api/v1/upload` 上传媒体文件，然后将返回的 URL 传递给 `media_urls`。

### 创建主题帖
```
POST https://opentweet.io/api/v1/posts
Body: {
  "text": "First tweet of the thread",
  "is_thread": true,
  "thread_tweets": ["Second tweet", "Third tweet"]
}
```

### 带有每条推文媒体的主题帖
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
`thread_media` 是一个数组数组。每个内部数组包含 `thread_tweets` 中对应推文的媒体 URL。对于没有媒体的推文，使用 `[]`。

### 向 X 社区发布内容
```
POST https://opentweet.io/api/v1/posts
Body: {
  "text": "Shared with the community!",
  "community_id": "1234567890",
  "share_with_followers": true
}
```

### 批量创建（最多 50 条帖子）
```
POST https://opentweet.io/api/v1/posts
Body: {
  "posts": [
    { "text": "Tweet 1", "scheduled_date": "2026-03-01T10:00:00Z" },
    { "text": "Tweet 2", "scheduled_date": "2026-03-01T14:00:00Z" }
  ]
}
```

### 安排发布时间
```
POST https://opentweet.io/api/v1/posts/{id}/schedule
Body: { "scheduled_date": "2026-03-01T10:00:00Z" }
```
日期必须在未来，并使用 ISO 8601 格式。

### 立即发布
```
POST https://opentweet.io/api/v1/posts/{id}/publish
```
不需要正文。内容会立即发布到 X。响应中会包含 `status: "posted"`、`x_post_id` 和 `url`（实际的 X 推文 URL）。

### 批量安排发布（最多 50 条帖子）
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

### 列出帖子
```
GET https://opentweet.io/api/v1/posts?status=scheduled&page=1&limit=20
```
状态选项：`scheduled`、`posted`、`draft`、`failed`

### 获取帖子信息
```
GET https://opentweet.io/api/v1/posts/{id}
```

### 更新帖子信息
```
PUT https://opentweet.io/api/v1/posts/{id}
Body: { "text": "Updated text", "media_urls": ["https://..."], "scheduled_date": "2026-03-01T10:00:00Z" }
```
所有字段都是可选的。已发布的帖子无法更新。将 `scheduled_date` 设置为 `null` 可以取消安排（将其恢复为草稿状态）。

### 删除帖子
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
返回值：`{ "url": "https://..." }`

支持的格式：JPG、PNG、GIF、WebP（最大 5MB）、MP4、MOV（最大 20MB）。

**工作流程**：先上传媒体文件，然后在创建/更新帖子时使用返回的 URL。

## 分析

### 账户概览
```
GET https://opentweet.io/api/v1/analytics/overview
```
返回发布统计信息（总帖子数、发布频率、活跃天数、平均每周帖子数、最活跃的一天/小时、主题帖数量、媒体帖子数量）、发布连续天数（当前和最长连续天数）、趋势数据（本周与上周、本月与上月对比、最佳月份）、类别分布以及最近的活动情况（过去 7 天和 30 天的每日统计）。

### 推文互动指标（仅限高级计划）
```
GET https://opentweet.io/api/v1/analytics/tweets?period=30
```
返回每条推文的互动数据：点赞数、转发数、回复数、引用数、展示次数、书签数以及互动率。还包括表现最佳/最差的帖子、内容类型统计、互动时间线以及最佳发布时间/日期。时间范围：7-365 天或“全部”。

### 关注者增长
```
GET https://opentweet.io/api/v1/analytics/followers?days=30
```
返回随时间变化的关注者数量、当前关注者数量、净增长量和增长百分比。时间范围：7-365 天或“全部”。

### 最佳发布时间
```
GET https://opentweet.io/api/v1/analytics/best-times
```
分析您的发布模式以找到最佳发布时间。至少需要发布 3 条帖子才能使用此功能。

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
3. 发布：`POST /api/v1/posts/{id}/publish`

**立即发布推文（一步完成）：**
1. `GET /api/v1/me` — 检查 `limits.can_post` 是否为 `true`
2. `POST /api/v1/posts` 并输入 `{"text": "...", "publish_now": true}`

**发布带图片的推文：**
1. `GET /api/v1/me` — 检查限制条件
2. 上传图片：`POST /api/v1/upload` 并获取返回的 URL
3. 创建推文：`POST /api/v1/posts` 并输入 `{"text": "...", "media_urls": ["<url>"]`
4. 发布：`POST /api/v1/posts/{id}/publish`

**安排推文发布时间：**
1. `GET /api/v1/me` — 检查 `limits_remaining_posts_today` 是否大于 0
2. 创建推文并设置发布时间：`POST /api/v1/posts` 并输入文本内容和 `scheduled_date`（一步完成）

**安排一周的内容：**
1. `GET /api/v1/me` — 检查剩余的帖子数量
2. 批量创建：`POST /api/v1/posts` 并输入包含 `scheduled_date` 的帖子数组

**创建带媒体的主题帖：**
1. 上传图片：`POST /api/v1/upload` 上传每张图片
2. 创建推文：`POST /api/v1/posts` 并输入 `is_thread`、`thread_tweets`、`media_urls`（第一条推文）和 `thread_media`（后续推文）

**批量安排草稿的发布：**
1. 创建草稿：`POST /api/v1/posts` 并输入帖子数组
2. 批量安排：`POST /api/v1/posts/batch-schedule` 并输入帖子 ID 和日期

**发布前查看分析数据：**
1. `GET /api/v1/analytics/best-times` — 查找最佳发布时间
2. `GET /api/v1/analytics/overview` — 查看发布连续天数和趋势数据
3. 根据建议的最佳时间安排帖子发布

## 重要规则
- 在安排或发布内容之前，务必先调用 `GET /api/v1/me` 以检查限制条件。
- **重要提示**：始终解析并使用 API 返回的实际 JSON 响应数据，切勿伪造或假设响应值。
- 发布 ID 始终是 24 个字符的 MongoDB ObjectId（例如 "507f1f77bcf86cd799439011"），不能使用简短字符串。
- 每条帖子的响应中都包含 `status` 字段：`draft`、`scheduled`、`posted` 或 `failed`。
- 已发布的帖子包含 `url` 字段，其中包含实际的 X 推文 URL。请始终使用这个 URL，切勿自行构造。
- 要确认帖子是否已发布，请检查 `status` 是否为 `posted` 且 `url` 是否存在。
- 每条推文的长度限制为 280 个字符（主题帖中的每条推文）。
- 每次请求的批量限制为 50 条帖子。
- 请求速率限制：每分钟 60 次，每天 1,000 次（基础计划）；每分钟 300 次，每天 1,000 次（高级计划）。
- 日期必须使用 ISO 8601 格式且必须在未来。
- 安排或发布内容需要激活订阅（创建草稿是免费的）。
- 在 `POST /api/v1/posts` 中包含 `scheduled_date` 需要订阅。
- 在创建帖子之前请上传媒体文件——使用返回的 URL 设置 `media_urls` 或 `thread_media`。
- 媒体文件限制：图片（JPG、PNG、GIF、WebP）最大 5MB，视频（MP4、MOV）最大 20MB。
- 推文互动分析需要高级计划（基础计划无法使用此功能）。
- 403 错误表示没有订阅；429 错误表示达到每日发布限制。
- 检查响应状态码：201=创建成功，200=成功，4xx=客户端错误，5xx=服务器错误。

## 安全措施

**发布操作是不可逆的** — 一旦推文发布到 X，就无法通过 API 取消。

### 发布前确认
- 在调用 `/publish` 或使用 `publish_now: true` 之前，务必告知用户您要发布的帖子内容，并请求确认。
- 显示推文文本（如果太长会进行截断）和帖子 ID，以便用户确认。

### 已安排的帖子 ≠ 可立即发布
- 如果帖子的 `scheduled_date` 在未来，那么它应该在指定时间由系统安排发布，而不是立即发布。
- 除非用户明确要求立即发布，否则切勿对具有未来 `scheduled_date` 的帖子调用 `/publish`。
- 当用户请求“发布”帖子时，请明确询问他们是希望立即发布还是安排在以后发布。如果提供了日期，则默认为安排发布。

### 批量操作——谨慎进行
- 在创建或安排超过 5 条帖子时，先总结批量信息（数量、日期范围、第一条/最后一条帖子的预览内容），然后请求用户确认。
- 切勿一次性批量创建并立即发布。先创建草稿或安排发布，让用户审核后再进行发布。
- 使用 `batch-schedule` 时，在发送请求之前向用户展示日期列表。

### 避免循环调用 `publish` 方法
- 未经用户明确同意，切勿循环调用 `/publish` 来处理整个帖子列表。
- 如果用户请求“发布所有草稿”，请先列出所有草稿并获取确认。

## 完整 API 文档
更多详细信息请访问：https://opentweet.io/api/v1/docs