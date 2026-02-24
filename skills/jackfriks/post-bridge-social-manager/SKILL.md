---
name: post-bridge-social-manager
version: 1.0.6
title: Social Media Assistant (via post-bridge.com)
description: 将你的 OpenClaw 转换为一个自主的社交媒体管理工具，通过使用 Post Bridge API 来实现跨多个平台的发布和内容管理功能。该工具支持在 TikTok、Instagram Reels、YouTube Shorts、Twitter/X、LinkedIn、Pinterest、Facebook、Threads 以及 Bluesky 等平台上进行内容调度、发布和操作。功能包括媒体上传、帖子创建、发布计划制定、平台特定配置设置、草稿模式以及发布结果跟踪等。
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

1. 在 [post-bridge.com](https://post-bridge.com) 上创建一个 Post Bridge 账户。
2. 连接您的社交媒体账户（TikTok、Instagram、YouTube、Twitter 等）。
3. 启用 API 访问（设置 → API）。
4. 将您的 API 密钥存储在工作区的 `.env` 文件中：
   ```
   POST_BRIDGE_API_KEY=pb_live_xxxxx
   ```
5. 下载 API 文档：`https://api.post-bridge.com/reference` → 保存到工作区并命名为 `post-bridge-api.json`。

## 认证

所有请求都使用 Bearer 令牌进行认证：
```
Authorization: Bearer <POST_BRIDGE_API_KEY>
```

基础 URL：`https://api.post-bridge.com`

## 核心工作流程

### 1. 获取社交媒体账户信息
```
GET /v1/social-accounts
```
返回包含 `id`、`platform`、`username` 的已连接账户数组。请保存这些 ID，因为每个帖子都需要它们。

### 2. 上传媒体文件
```
POST /v1/media/create-upload-url
Body: { "mime_type": "video/mp4", "size_bytes": <int>, "name": "video.mp4" }
```
返回 `media_id` 和 `upload_url`。之后：
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

### 4. 检查结果
```
GET /v1/posts/<post_id>
```
返回状态：`processing`（处理中）、`scheduled`（已安排）、`posted`（已发布）、`failed`（失败）。

### 5. 分析数据（TikTok）
```
GET /v1/analytics?platform=tiktok
```
检索 TikTok 帖子的性能数据（观看次数、点赞数、分享次数等）。支持按 `timeframe`（7 天、30 天、90 天、全部）和 `post_result_id` 进行过滤。

```
POST /v1/analytics/sync
```
可以手动触发 TikTok 分析数据的同步。此操作有频率限制，请在调用之间等待适当的时间间隔。

## 平台配置

在创建帖子时，将这些配置传递给 `platform_configurations` 对象中。**重要提示：**务必使用正确的平台键来确保配置仅适用于目标平台，避免在其他平台上引发问题。

**TikTok (`tiktok`):**
- `draft: true` — 保存为草稿（需手动在 TikTok 上发布并添加热门音效）
- `video_cover_timestamp_ms: 3000` — 覆盖图缩略图时间
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
- `video_cover_timestamp_ms: 3000` — 覆盖图缩略图时间
- `is_trial_reel: true` — 试用模式（需要 1000+ 关注者）
- `trial_graduation: "SS_PERFORMANCE"` — 根据表现自动升级

**YouTube:**
- `video_cover_timestamp_ms: 3000` — 覆盖图缩略图时间
- `title: "我的短片标题"` — 覆盖帖子标题

**Twitter/X:**
- `caption: "自定义标题"` — 平台特定的标题

所有平台都支持 `caption` 和 `media` 的自定义设置。

## 视频内容的推荐工作流程

1. 将视频存储在本地文件夹中。
2. 使用 ffmpeg 提取视频中的帧以读取文字叠加层：
   ```
   ffmpeg -i video.mp4 -ss 00:00:04 -frames:v 1 frame.jpg -y
   ```
3. 根据视频内容生成标题并添加标签。
4. 上传视频 → 创建帖子 → 安排发布或立即发布。
5. 将已发布的视频移动到 `posted/` 子文件夹中以避免重复。
6. 设置定时任务，在预定时间后 5 分钟检查帖子状态。
7. 通过浏览平台页面或查看帖子结果来跟踪表现。

## 提示

- 通过包含多个账户 ID 同时发布到多个平台。
- 分散时间发布帖子（例如上午 9 点和下午 3 点），以提高覆盖范围。
- 使用 `scheduled_at` 预安排发布批次——Post Bridge 会处理时间安排。
- TikTok 的草稿模式允许您在发布前手动添加热门音效。
- 每个帖子使用 4-5 个标签以获得最佳互动效果。
- 监测哪些方法有效，并不断优化标题和格式。