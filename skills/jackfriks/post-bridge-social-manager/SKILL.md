---
name: post-bridge-social-manager
version: 1.0.7
title: Social Media Assistant (via post-bridge.com)
description: 将您的 OpenClaw 转换为使用 Post Bridge API 的自主社交媒体管理工具。该工具可用于在 TikTok、Instagram Reels、YouTube Shorts、Twitter/X、LinkedIn、Pinterest、Facebook、Threads 或 Bluesky 等平台上安排发布、发布内容或管理内容。功能包括媒体上传、帖子创建、发布计划制定、平台特定配置、草稿模式以及帖子发布结果跟踪。
license: MIT
author: Jack Friks <jack@frikit.net>
homepage: https://clawhub.ai/jackfriks/post-bridge-social-manager
repository: https://github.com/jackfriks/post-bridge-social-manager
keywords: social-media, automation, post-bridge, tiktok, instagram, youtube, twitter, linkedin
metadata:
  openclaw:
    requires:
      env:
        - POST_BRIDGE_API_KEY
      bins:
        - ffmpeg
    primaryEnv: POST_BRIDGE_API_KEY
---
# 社交媒体助手（通过 post-bridge.com）

通过 [Post Bridge](https://post-bridge.com) 的 API 自动管理社交媒体发布。

## 设置

1. 在 [post-bridge.com](https://post-bridge.com) 创建一个 Post Bridge 账户。
2. 连接您的社交媒体账户（TikTok、Instagram、YouTube、Twitter 等）。
3. 启用 API 访问权限（设置 → API）。
4. 将您的 API 密钥存储在工作区的 `.env` 文件中：
   ```
   POST_BRIDGE_API_KEY=pb_live_xxxxx
   ```
5. 下载 API 文档：`https://api.post-bridge.com/reference` → 保存到工作区并命名为 `post-bridge-api.json`。

## 身份验证

所有请求都使用 Bearer 令牌进行身份验证：
```
Authorization: Bearer <POST_BRIDGE_API_KEY>
```

基础 URL：`https://api.post-bridge.com`

## 核心工作流程

### 1. 获取社交媒体账户信息
```
GET /v1/social-accounts
```
返回已连接的账户数组，包含 `id`、`platform` 和 `username`。请保存这些 ID，因为它们在每次发布时都会用到。

### 2. 上传媒体文件
```
POST /v1/media/create-upload-url
Body: { "mime_type": "video/mp4", "size_bytes": <int>, "name": "video.mp4" }
```
返回 `media_id` 和 `upload_url`。然后：
```
PUT <upload_url>
Content-Type: video/mp4
Body: <binary file>
```

### 3. 创建帖子
```
POST /v1/posts
Body: {
  "caption": "your caption here #hashtags",
  "media": ["<media_id>"],
  "social_accounts": [<account_id_1>, <account_id_2>],
  "scheduled_at": "2026-01-01T14:00:00Z",  // omit for instant post
  "platform_configurations": { ... }  // optional, see below
}
```

**额外的创建选项：**

- `media_urls`：公开可访问的 URL 数组（如果没有媒体 ID，可以使用这些 URL）。示例：`["https://example.com/video.mp4"]`
- `is_draft`：如果设置为 `true`，则创建帖子但不会立即发布，直到设置了预定发布时间或立即发布。
- `processing_enabled`：如果设置为 `false`，则跳过视频处理。默认值为 `true`。
- `use_queue`：自动将帖子安排到下一个可用的队列中（在 Post Bridge 仪表板中配置）。不能与 `scheduled_at` 选项同时使用。传递 `true` 可以使用您保存的时区，或者使用 `{ "timezone": "America/New_York" }` 来覆盖默认时区。

**`use_queue` 示例：**
```json
{
  "caption": "Queued post!",
  "media": ["<media_id>"],
  "social_accounts": [44029],
  "use_queue": true
}
```
此选项会自动找到队列中的下一个可用时间槽并设置 `scheduled_at`。您必须先在仪表板中配置好队列计划。

### 4. 更新或删除已安排的帖子
```
PATCH /v1/posts/<post_id>
```
更新已安排的帖子（例如标题、发布时间等）。仅适用于状态为 `scheduled` 的帖子。

```
DELETE /v1/posts/<post_id>
```
删除已安排的帖子。仅适用于状态为 `scheduled` 的帖子。

### 5. 检查结果
```
GET /v1/posts/<post_id>
```
返回帖子的状态：`processing`、`scheduled`、`posted`、`failed`。

```
GET /v1/post-results
```
列出所有平台的帖子结果（通过 `offset` 和 `limit` 进行分页）。

### 6. 分析数据
```
GET /v1/analytics
```
检索帖子的性能数据（观看次数、点赞数、分享次数、评论数等）。

查询参数：
- `platform` — 按平台过滤（例如 `tiktok`、`youtube`、`instagram`）
- `post_result_id[]` — 按特定帖子 ID 过滤（多个值表示 OR 关系）
- `timeframe` — `7d`、`30d`、`90d` 或 `all`（默认：`all`）
- `offset` / `limit` — 分页参数

返回结果：每条记录包含 `view_count`、`like_count`、`comment_count`、`share_count`、`cover_image_url`、`share_url`、`duration` 等信息。

```
POST /v1/analytics/sync
```
手动触发从各个平台的分析数据同步。可以选择传递 `?platform=tiktok` 仅同步特定平台的数据。同步频率限制为每 5 分钟一次。

## 平台配置

在创建帖子时，将这些配置传递给 `platform_configurations` 对象中。**重要提示：**务必使用正确的平台键进行封装，以确保这些配置仅适用于目标平台，避免在其他平台上引发问题。

**TikTok (`tiktok`):**
- `draft: true` — 将帖子保存为草稿状态（在 TikTok 上手动发布时添加热门音效）
- `video_cover_timestamp_ms: 3000` — 覆盖图缩略图的时间戳（单位：毫秒）
- `is_aigc: true` — 标记为 AI 生成的内容

**正确的多平台配置示例：**
```json
{
  "caption": "Default caption",
  "social_accounts": [44029, 44030],
  "platform_configurations": {
    "tiktok": {
      "draft": true,
      "is_aigc": false
    },
    "instagram": {
      "is_trial_reel": false
    }
  }
}
```

**Instagram (`instagram`):**
- `video_cover_timestamp_ms: 3000` — 覆盖图缩略图的时间戳（单位：毫秒）
- `is_trial_reel: true` — 试用模式（需要至少 1000 名粉丝）
- `trial_graduation: "SS_PERFORMANCE"` — 根据表现自动升级帖子等级

**YouTube:**
- `video_cover_timestamp_ms: 3000` — 覆盖图缩略图的时间戳（单位：毫秒）
- `title: "My Short Title"` — 覆盖帖子的标题

**Twitter/X:**
- `caption: "override caption"` — 平台特定的标题

所有平台都支持 `caption` 和 `media` 的自定义设置。

## 视频内容的推荐工作流程

1. 将视频存储在本地文件夹中。
2. 使用 ffmpeg 提取视频中的文字信息。
3. 根据视频内容生成标题并添加相关标签。
4. 上传视频 → 创建帖子 → 安排发布时间或立即发布（或使用 `use_queue` 自动安排发布）。
5. 将已发布的视频移动到 `posted/` 子文件夹中以避免重复。
6. 设置定时任务，在预定发布时间后 5 分钟检查帖子状态。
7. 通过 `GET /v1/analytics` 或浏览平台页面来跟踪帖子的表现数据。

## 提示

- 通过添加多个账户 ID 同时在多个平台上发布帖子。
- 在一天中的不同时间（例如上午 9 点和下午 3 点）分批发布帖子，以提高覆盖范围。
- 使用 `scheduled_at` 预先安排发布时间——Post Bridge 会处理时间安排。
- 使用 `use_queue` 自动填充队列计划，无需手动计算时间。
- TikTok 的草稿模式允许在发布前手动添加热门音效。
- 每条帖子使用 4-5 个标签以获得更好的互动效果。
- 监测哪些方法有效，并不断优化标题和格式。