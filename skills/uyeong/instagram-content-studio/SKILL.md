---
name: instagram-api
description: 管理 Instagram 账户：可以查看个人资料、浏览帖子、发布图片/轮播图、发布视频/Reels（Instagram 的短视频功能），以及阅读和回复评论。适用于用户需要执行任何与 Instagram 相关的操作时使用。
allowed-tools: Bash(node scripts/*)
compatibility: Requires node (v22+), npm, and cloudflared (for local file uploads). Requires env var INSTAGRAM_ACCESS_TOKEN in a .env file. Requires internet access to graph.instagram.com.
metadata:
  version: "1.0"
---
# Instagram API 技能

这是一项通过 Instagram Graph API 管理 Instagram 账户的功能。支持查看个人资料、管理帖子、发布图片、发布视频/Reels 以及处理评论等操作。

## 先决条件

- 必须配置一个包含凭据的 `.env` 文件。
  - 必需的凭据：`INSTAGRAM_ACCESS_TOKEN`
  - 建议使用（用于通过 Facebook Graph 发布评论/回复）：`FACEBOOK_USER_ACCESS_TOKEN`
  - 用于刷新 FB 令牌的凭据：`FACEBOOK_APP_ID`、`FACEBOOK_APP_SECRET`
- 为了能够本地发布图片/视频，必须安装 `cloudflared`。
- 如果用户指定了 `.env` 文件的路径，请在每个命令后添加 `--env <path>` 参数。例如：`node scripts/get-profile.js --env /home/user/.instagram-env`
- 所有脚本都必须以该项目根目录为工作目录来运行。

## 可用的命令

所有命令在执行前都会自动刷新令牌，无需手动刷新。

### 刷新令牌

```bash
# Instagram token refresh
node scripts/refresh-token.js

# Facebook user token refresh (for comments/replies flow)
node scripts/refresh-facebook-token.js
```

手动刷新令牌并返回令牌的过期信息。

### 查看个人资料

```bash
node scripts/get-profile.js
```

返回个人资料信息（姓名、用户名、账户类型、媒体数量）。

### 列出帖子

```bash
node scripts/get-posts.js [--limit 10]
```

返回用户的帖子列表。可以使用 `--limit` 参数来设置显示的帖子数量（默认值：10）。

### 查看帖子详情

```bash
node scripts/get-post.js <media-id>
```

返回帖子详情，包括点赞数和评论数。

### 发布图片

```bash
# Single image (URL)
node scripts/post-image.js --caption "Caption" https://example.com/photo.jpg

# Single image (local file)
node scripts/post-image.js --caption "Caption" ./photos/image.png

# Carousel — multiple images (URL)
node scripts/post-image.js --caption "Caption" https://example.com/a.jpg https://example.com/b.jpg

# Carousel — multiple images (local files)
node scripts/post-image.js --caption "Caption" ./img1.png ./img2.png ./img3.jpg
```

- 1 张图片 → 发布为单条帖子；2 张或更多图片 → 自动发布为轮播图（最多 10 张）。
- 支持 `http://`、`https://` 网址以及本地文件路径，但不允许同时使用这两种方式。
- 支持的本地文件格式：jpg、jpeg、png、gif、webp、heic/heif（HEIC 会自动转换为 JPEG）。

### 发布视频（Reels）

```bash
# Single video (URL)
node scripts/post-video.js --caption "Caption" https://example.com/video.mp4

# Single video (local file)
node scripts/post-video.js --caption "Caption" ./videos/clip.mp4

# With cover image and options
node scripts/post-video.js --caption "Caption" --cover https://example.com/cover.jpg --thumb-offset 5000 --share-to-feed true https://example.com/video.mp4

# Video carousel — multiple videos (URL)
node scripts/post-video.js --caption "Caption" https://example.com/a.mp4 https://example.com/b.mp4

# Video carousel — multiple videos (local files)
node scripts/post-video.js --caption "Caption" ./clip1.mp4 ./clip2.mov
```

- 1 个视频 → 发布为 Reels 帖子；2 个或更多视频 → 自动发布为轮播图（最多 10 个）。
- 支持 `http://`、`https://` 网址以及本地文件路径，但不允许同时使用这两种方式。
- 支持的文件格式：mp4、mov（每个文件最大大小为 100MB）。
- `--cover`、`--thumb-offset`、`--share-to-feed` 选项仅适用于单条视频帖子（不适用于轮播图）。
- 视频处理时间比图片处理时间长；脚本最多会等待 10 分钟。

### 查看评论

```bash
node scripts/get-comments.js <media-id>
```

返回特定帖子的评论和回复。

### 发表评论

```bash
node scripts/post-comment.js <media-id> --text "Comment text"
```

### 回复评论

```bash
node scripts/reply-comment.js <comment-id> --text "Reply text"
```

## 工作流程指南

- 在发布图片或视频之前，务必先与用户确认标题内容。
- 发布完成后，将结果 ID 和永久链接告知用户（这两个信息都会包含在输出结果中）。
- 视频处理时间比图片处理时间长，请告知用户可能需要几分钟。
- 在撰写评论或回复时，务必先与用户确认内容。
- 所有命令的输出结果均为 JSON 格式。

## 错误处理

如果输出结果中包含 `error` 字段，表示发生了错误。请向用户说明错误原因并建议解决方案。

```json
{ "error": "error message" }
```

## 安全性

### 令牌存储
- `refreshIgToken()` 和 `refreshFbToken()` 会以明文形式覆盖 `.env` 文件中的令牌内容。请勿将 `.env` 文件提交到版本控制系统中。
- 创建一个具有最低权限要求的 Meta 应用程序（具体权限要求见下文）。

### 本地文件上传
- 本地图片/视频上传会启动一个临时的 [cloudflared Quick Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/get-started/create-local-tunnel/)，以便 Instagram 服务器能够下载文件。
- 该隧道仅在上传过程中处于激活状态，上传完成后会立即关闭。
- 仅提供您愿意暂时公开到互联网的文件路径。

### 最低权限要求

在创建 Meta 应用程序时，只需授予以下权限：
- `instagram_business_basic` — 读取个人资料和媒体信息
- `instagram_content_publish` — 发布图片/视频
- `instagram_manage_comments` — 读取/写入评论
- `pages_read_engagement` — 通过 Facebook Graph 使用评论 API 所需的权限
- `pages_show_list` — 需要用于关联到页面的 Instagram 账户