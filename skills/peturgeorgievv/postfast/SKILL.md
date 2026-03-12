---
name: postfast
description: 使用 PostFast API 来安排和管理在 TikTok、Instagram、Facebook、X（Twitter）、YouTube、LinkedIn、Threads、Bluesky、Pinterest 和 Telegram 上的社交媒体帖子。当用户需要安排社交媒体发布、管理社交媒体内容、上传用于发布的媒体文件、列出已连接的社交媒体账户、查看已安排的帖子、删除已安排的帖子、将内容跨平台发布，或自动化他们的社交媒体工作流程时，可以使用该工具。PostFast 是一款 SaaS 工具——无需自行托管。
homepage: https://postfa.st
metadata: {"openclaw":{"emoji":"⚡","primaryEnv":"POSTFAST_API_KEY","requires":{"env":["POSTFAST_API_KEY"]}}}
---
# PostFast

这是一个用于通过一个API在10个平台上安排社交媒体发布的工具。它属于SaaS服务，无需自行托管。

## 设置

1. 在 [https://app.postfa.st/register](https://app.postfa.st/register) 注册（提供7天免费试用，无需信用卡）。
2. 进入“工作区设置”（Workspace Settings），然后生成API密钥。
3. 设置环境变量：
   ```bash
   export POSTFAST_API_KEY="your-api-key"
   ```

基础URL：`https://api.postfa.st`
认证头：`pf-api-key: $POSTFAST_API_KEY`

## 核心工作流程

### 1. 列出已连接的账户

```bash
curl -s -H "pf-api-key: $POSTFAST_API_KEY" https://api.postfa.st/social-media/my-social-accounts
```

返回一个包含 `{ id, platform, platformUsername, displayName }` 的数组。请保存 `id`，因为它是每条帖子所需的 `socialMediaId`。

支持的平台：`TIKTOK`、`INSTAGRAM`、`FACEBOOK`、`X`、`YOUTUBE`、`LINKEDIN`、`THREADS`、`BLUESKY`、`PINTEREST`、`TELEGRAM`

### 2. 安排纯文本帖子（无需媒体）

```bash
curl -X POST https://api.postfa.st/social-posts \
  -H "pf-api-key: $POSTFAST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "posts": [{
      "content": "Your post text here",
      "mediaItems": [],
      "scheduledAt": "2026-06-15T10:00:00.000Z",
      "socialMediaId": "ACCOUNT_ID_HERE"
    }],
    "controls": {}
  }'
```

返回 `{ "postIds": ["uuid-1"] }`。

### 3. 安排带媒体的帖子（三步流程）

**步骤A** — 获取签名上传URL：
```bash
curl -X POST https://api.postfa.st/file/get-signed-upload-urls \
  -H "pf-api-key: $POSTFAST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "contentType": "image/png", "count": 1 }'
```
返回 `[{ "key": "image/uuid.png", "signedUrl": "https://..." }]`。

**步骤B** — 将文件上传到S3：
```bash
curl -X PUT "SIGNED_URL_HERE" \
  -H "Content-Type: image/png" \
  --data-binary @/path/to/file.png
```

**步骤C** — 使用媒体密钥创建帖子：
```bash
curl -X POST https://api.postfa.st/social-posts \
  -H "pf-api-key: $POSTFAST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "posts": [{
      "content": "Post with image!",
      "mediaItems": [{ "key": "image/uuid.png", "type": "IMAGE", "sortOrder": 0 }],
      "scheduledAt": "2026-06-15T10:00:00.000Z",
      "socialMediaId": "ACCOUNT_ID_HERE"
    }],
    "controls": {}
  }'
```

对于视频，请设置 `contentType: "video/mp4"` 和 `type: "VIDEO"`，并使用 `video/` 作为密钥前缀。

### 4. 列出已安排的帖子

```bash
curl -s -H "pf-api-key: $POSTFAST_API_KEY" "https://api.postfa.st/social-posts?page=0&limit=20"
```

返回 `{ "data": [...], "totalCount": 25, "pageInfo": { "page": 1, "hasNextPage": true, "perPage": 20 } }`。

**查询参数：**
- `page`（整数，默认值0）——基于0的页码索引。`pageInfo.page` 表示实际的显示页码（从1开始）。
- `limit`（整数，默认值20，最大值50）——每页显示的条目数。
- `platforms`（字符串）——用逗号分隔的过滤条件：`FACEBOOK,INSTAGRAM,X`。
- `statuses`（字符串）——用逗号分隔的过滤条件：`DRAFT`, `SCHEDULED`, `PUBLISHED`, `FAILED`。
- `from` / `to`（ISO 8601 UTC格式）——根据 `scheduledAt` 过滤日期范围。

示例：`GET /social-posts?page=0&limit=50&platforms=X,LINKEDIN&statuses=SCHEDULED&from=2026-06-01T00:00:00Z&to=2026-06-30T23:59:59Z`

### 5. 删除已安排的帖子

```bash
curl -X DELETE -H "pf-api-key: $POSTFAST_API_KEY" https://api.postfa.st/social-posts/POST_ID
```

### 6. 跨平台发布

在 `posts` 数组中包含多个条目，每个条目都有不同的 `socialMediaId`。它们共享相同的 `controls` 和 `mediaItems` 键。

### 7. 生成连接链接（供客户端使用）

允许客户端将他们的社交媒体账户连接到您的工作区，而无需创建PostFast账户：

```bash
curl -X POST https://api.postfa.st/social-media/connect-link \
  -H "pf-api-key: $POSTFAST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "expiryDays": 7, "sendEmail": true, "email": "client@example.com" }'
```

返回 `{ "connectUrl": "https://app.postfa.st/connect?token=..." }`。分享此链接，他们可以直接连接账户。每小时的发送次数限制为50次。

### 8. 创建草稿帖子

省略 `scheduledAt` 并设置 `status: "DRAFT"` 以保存帖子但不安排发布：

```bash
curl -X POST https://api.postfa.st/social-posts \
  -H "pf-api-key: $POSTFAST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "posts": [{ "content": "Draft idea...", "mediaItems": [], "socialMediaId": "ACCOUNT_ID" }],
    "status": "DRAFT",
    "controls": {}
  }'
```

### 9. 获取帖子分析

获取已发布的帖子及其性能指标：

```bash
curl -s -H "pf-api-key: $POSTFAST_API_KEY" \
  "https://api.postfa.st/social-posts/analytics?startDate=2026-03-01T00:00:00.000Z&endDate=2026-03-31T23:59:59.999Z&platforms=TIKTOK,INSTAGRAM"
```

**查询参数：**
- `startDate`（ISO 8601格式，必填）——日期范围的开始时间。
- `endDate`（ISO 8601格式，必填）——日期范围的结束时间。
- `platforms`（字符串，可选）——用逗号分隔的过滤条件。
- `socialMediaIds`（字符串，可选）——用逗号分隔的账户UUID。

返回 `{ "data": [{ id, content, socialMediaId, platformPostId, publishedAt, latestMetric }] }`。

`latestMetric` 字段包括：`impressions`（展示次数）、`reach`（ reach）、`likes`（点赞数）、`comments`（评论数）、`shares`（分享次数）、`totalInteractions`（总互动次数）、`fetchedAt`（获取时间）、`extras`（其他数据）。所有数字均为字符串（bigint类型）。如果尚未获取指标，则 `latestMetric` 为 `null`。LinkedIn个人账户将被排除在外。

每小时的发送次数限制为350次。

## 常见用法

### 模式1：跨平台活动

同时在LinkedIn、X和Threads上发布相同的内容：

```bash
curl -X POST https://api.postfa.st/social-posts \
  -H "pf-api-key: $POSTFAST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "posts": [
      { "content": "Big announcement!", "mediaItems": [], "scheduledAt": "2026-06-15T09:00:00.000Z", "socialMediaId": "LINKEDIN_ID" },
      { "content": "Big announcement!", "mediaItems": [], "scheduledAt": "2026-06-15T09:00:00.000Z", "socialMediaId": "X_ID" },
      { "content": "Big announcement!", "mediaItems": [], "scheduledAt": "2026-06-15T09:00:00.000Z", "socialMediaId": "THREADS_ID" }
    ],
    "controls": {}
  }'
```

请参阅 [examples/cross-platform-post.json](examples/cross-platform-post.json) 以获取完整示例。

### 模式2：Instagram Reel（带上传功能）

1. 使用 `contentType: "video/mp4"` 获取签名上传URL。
2. 将视频上传到签名URL。
3. 使用 `instagramPublishType: "REEL"` 创建帖子。

请参阅 [examples/instagram-reel.json](examples/instagram-reel.json) 以获取请求体示例。

### 模式3：TikTok视频（带隐私设置）

上传视频，然后设置隐私选项后发布：

```bash
# controls object:
{
  "tiktokPrivacy": "PUBLIC",
  "tiktokAllowComments": true,
  "tiktokAllowDuet": false,
  "tiktokAllowStitch": false,
  "tiktokBrandContent": true
}
```

请参阅 [examples/tiktok-video.json](examples/tiktok-video.json) 以获取详细步骤。

### 模式4：Pinterest Pin（需要指定Pinterest板块）

始终先获取板块信息，然后再发布内容：

```bash
# Step 1: Get boards
curl -s -H "pf-api-key: $POSTFAST_API_KEY" \
  https://api.postfa.st/social-media/PINTEREST_ACCOUNT_ID/pinterest-boards

# Step 2: Post with board ID
# controls: { "pinterestBoardId": "BOARD_ID", "pinterestLink": "https://yoursite.com" }
```

请参阅 [examples/pinterest-pin.json](examples/pinterest-pin.json) 以获取详细步骤。

### 模式5：YouTube Short（带标签和播放列表）

上传视频，然后使用YouTube的发布设置进行发布：

```bash
# controls object:
{
  "youtubeIsShort": true,
  "youtubeTitle": "Quick Tip: Batch Your Content",
  "youtubePrivacy": "PUBLIC",
  "youtubePlaylistId": "PLxxxxxx",
  "youtubeTags": ["tips", "productivity", "social media"],
  "youtubeMadeForKids": false
}
```

请参阅 [examples/youtube-short.json](examples/youtube-short.json) 以获取详细步骤。

### 模式6：LinkedIn文档帖子

PDF、PPTX或DOCX格式的文档会在LinkedIn上以可滑动轮播的形式展示。

1. 使用 `contentType: "application/pdf"` 获取签名上传URL。
2. 将文件上传到签名URL。
3. 使用 `linkedinAttachmentKey` 而不是 `mediaItems` 来创建帖子。

请参阅 [examples/linkedin-document.json](examples/linkedin-document.json) 以获取详细步骤。

### 模式7：发布后自动添加第一条评论

在任何帖子发布后自动添加一条评论（最多尝试3次）：

```json
{
  "posts": [{ "content": "Main post text", "firstComment": "Link: https://postfa.st", "mediaItems": [], "scheduledAt": "...", "socialMediaId": "X_ID" }],
  "controls": {}
}
```

支持的平台：X、Instagram、Facebook、YouTube、Threads。不支持的平台：TikTok、Pinterest、Bluesky、LinkedIn。

请参阅 [examples/x-first-comment.json](examples/x-first-comment.json) 以获取详细步骤。

### 模式8：X（Twitter）转发

安排转发——内容和媒体将被忽略：

```json
{
  "posts": [{ "content": "", "scheduledAt": "...", "socialMediaId": "X_ID" }],
  "controls": { "xRetweetUrl": "https://x.com/username/status/1234567890" }
}
```

请参阅 [examples/x-retweet.json](examples/x-retweet.json) 以获取详细步骤。如果需要带自定义评论的转发，请使用 `xQuoteTweetUrl`（请参阅 [examples/x-quote-tweet.json]）。 

### 模式9：批量安排（一周内的多条帖子）

通过一次API调用安排多条帖子（每次请求最多15条）：

请参阅 [examples/batch-scheduling.json](examples/batch-scheduling.json) 以获取详细步骤。

## 平台特定控制选项

请在 `controls` 对象中传递这些参数。详细信息请参阅 [references/platform-controls.md](references/platform-controls.md)。

| 平台 | 控制选项 |
|---|---|
| **TikTok** | `tiktokPrivacy`, `tiktokAllowComments`, `tiktokAllowDuet`, `tiktokAllowStitch`, `tiktokIsDraft`, `tiktokBrandOrganic`, `tiktokBrandContent`, `tiktokAutoAddMusic` |
| **Instagram** | `instagramPublishType`（TIMELINE/STORY/REEL），`instagramPostToGrid`, `instagramCollaborators` |
| **Facebook** | `facebookContentType`（POST/REEL/STORY），`facebookReelsCollaborators` |
| **YouTube** | `youtubeIsShort`, `youtubeTitle`, `youtubePrivacy`, `youtubePlaylistId`, `youtubeTags`, `youtubeMadeForKids`, `youtubeCategoryId` |
| **LinkedIn** | `linkedinAttachmentKey`, `linkedinAttachmentTitle`（用于文档帖子） |
| **X (Twitter)** | `xQuoteTweetUrl`（引用推文），`xRetweetUrl`（转发），`xCommunityId`（发布到社区） |
| **Pinterest** | `pinterestBoardId`（必填），`pinterestLink` |
| **Bluesky** | 无平台特定控制选项——仅支持文本和图片 |
| **Threads** | 无平台特定控制选项——支持文本和图片/视频 |
| **Telegram** | 无平台特定控制选项——支持文本、图片和混合媒体 |

## 辅助端点

- **Pinterest板块**：`GET /social-media/{id}/pinterest-boards` → 返回 `[{ boardId, name }]`
- **YouTube播放列表**：`GET /social-media/{id}/youtube-playlists` → 返回 `[{ playlistId, title }]`
- **连接链接**：`POST /social-media/connect-link` → 返回 `{ connectUrl }`。允许客户端无需PostFast账户即可连接账户。参数：`expiryDays`（1-30天，默认值7天），`sendEmail`（布尔值），`email`（如果 `sendEmail` 为true则必填）。

## 发送次数限制

**全局限制**（每个API密钥）：每分钟60次、每5分钟150次、每小时300次、每天2000次

**每个端点的限制：**
- `POST /social-posts`：每天350次
- `GET /social-posts`：每小时200次
- `GET /social-posts/analytics`：每小时350次
- `POST /social-media/connect-link`：每小时50次

**平台特定限制：**
- X（Twitter）通过API：每个账户每天最多5条帖子——请遵守此限制。

请检查 `X-RateLimit-Remaining-*` 头部信息。如果达到限制，会返回429错误代码；请查看 `Retry-After-*` 头部信息。进行批量操作时，请在API调用之间间隔1秒。

## 媒体格式快速参考

| 平台 | 图片 | 视频 | 轮播 |
|---|---|---|---|
| TikTok | 仅支持轮播 | 最大文件大小250MB，格式MP4/MOV，时长3秒至10分钟 | 最多2-35张图片 |
| Instagram | JPEG/PNG格式 | 最大文件大小1GB，时长3-90秒（Reel） | 最多10张图片 |
| Facebook | 最大文件大小30MB，格式JPG/PNG | 每条帖子最多1张图片 | 最多10张图片 |
| YouTube | 视频时长不超过3分钟，格式H.264 | — |
| LinkedIn | 最多9张图片 | 最长时长10分钟；支持文档（PDF/PPTX/DOCX） |
| X（Twitter） | 最多4张图片 | — | — |
| Pinterest | 建议图片比例为2:3 | 支持这种格式 | 最多2-5张图片 |
| Bluesky | 最多4张图片 | 不支持这种格式 | — |
| Threads | 支持这种格式 | 支持这种格式 | 最多10张图片 |
| Telegram | 支持这种格式 | 支持文本、图片和混合媒体 |

## 常见注意事项

1. **务必先获取账户信息** — `socialMediaId` 是一个UUID，而不是平台名称。请调用 `GET /social-media/my-social-accounts` 来获取有效的ID。
2. **媒体文件必须经过三步上传流程** — 不允许使用外部URL。必须先获取签名URL，然后上传到S3，最后在 `mediaItems` 中使用该URL的 `key`。
3. `scheduledAt` 必须是未来的时间——格式为ISO 8601 UTC。过去的日期会导致400错误。
4. **Pinterest要求必须提供 `pinterestBoardId` — 请先使用 `GET /social-media/{id}/pinterest-boards` 获取板块信息。
5. **TikTok的标准帖子需要视频** — 图片仅适用于轮播格式（最多2-35张图片）。
6. **LinkedIn的文档帖子使用 `linkedinAttachmentKey`** — 不使用 `mediaItems`。发布文档时请将 `mediaItems` 设置为 `[]`。
7. **S3上传时的 `Content-Type` 必须匹配** — S3上传请求中的 `Content-Type` 头部信息必须与 `get-signed-upload-urls` 中请求的格式一致。
8. **Instagram Reel需要时长3-90秒的视频** — 超出这个时间范围的视频会导致错误。
9. **YouTube Short视频时长不得超过3分钟** — 建议使用H.264编码格式和AAC音频。
10. **X（Twitter）的帖子长度限制为280个字符** — 超过这个长度的内容会被自动截断。
11. **跨平台发布时需要调整内容长度** — `controls` 对象适用于批量中的所有帖子。与平台无关的控制选项将被忽略。
12. **X（Twitter）的API每天每个账户最多允许5条帖子** — 超过此限制可能会导致账户被限制。
13. **`firstComment` 功能仅支持5个平台** — X、Instagram、Facebook、YouTube、Threads。TikTok、Pinterest、Bluesky、LinkedIn不支持此功能。
14. **不能同时使用 `xQuoteTweetUrl` 和 `xRetweetUrl` — 请选择其中一个。转发时内容会被忽略。
15. **LinkedIn的文档支持PDF、DOC、DOCX、PPT、PPTX格式** — 最大文件大小为60MB。这些格式不能与普通媒体混合使用。
16. **分页从0开始** — `page=0` 返回第一页。`pageInfo.page` 表示实际的显示页码（从1开始）。

## 支持资源

**参考文档：**
- [references/api-reference.md](references/api-reference.md) — 完整的API端点参考及响应示例
- [references/platform-controls.md](references/platform-controls.md) — 所有平台特定的控制选项及其类型和默认值
- [references/media-specs.md](references/media-specs.md) — 各平台的媒体大小、格式和尺寸限制
- [references/upload-flow.md](references/upload-flow.md) — 详细的媒体上传指南

**即用示例：**
- [examples/EXAMPLES.md](examples/EXAMPLES.md) — 所有18个示例的索引
- [examples/cross-platform-post.json](examples/cross-platform-post.json) — 多平台发布示例
- [examples/tiktok-video.json](examples/tiktok-video.json) — 带隐私设置的TikTok帖子
- [examples/tiktok-carousel.json](examples/tiktok-carousel.json) — TikTok轮播帖子
- [examples/tiktok-draft.json](examples/tiktok-draft.json) — 保存为草稿的TikTok帖子
- [examples/instagram-reel.json](examples/instagram-reel.json) — Instagram Reel帖子
- [examples/instagram-story.json](examples/instagram-story.json) — Instagram Story帖子
- [examples/instagram-carousel.json](examples/instagram-carousel.json) — Instagram轮播帖子
- [examples/facebook-reel.json](examples/facebook-reel.json) — Facebook Reel帖子
- [examples/facebook-story.json](examples/facebook-story.json) — Facebook Story帖子
- [examples/youtube-short.json](examples/youtube-short.json) — 带标签的YouTube Short帖子
- [examples/pinterest-pin.json](examples/pinterest-pin.json) — 使用Pinterest板块的帖子
- [examples/linkedin-document.json](examples/linkedin-document.json) — LinkedIn文档帖子
- [examples/x-quote-tweet.json](examples/x-quote-tweet.json) — X平台的引用推文
- [examples/x-retweet.json](examples/x-retweet.json) — X平台的转发帖子
- [examples/x-first-comment.json](examples/x-first-comment.json) — 带自动评论的X平台帖子
- [examples/threads-carousel.json](examples/threads-carousel.json) — Threads平台的轮播帖子
- [examples/batch-scheduling.json](examples/batch-scheduling.json) — 一周内的多条帖子安排
- [examples/telegram-mixed-media.json](examples/telegram-mixed-media.json) — Telegram平台的混合媒体帖子

## 快速参考

```
# Auth
Header: pf-api-key: $POSTFAST_API_KEY

# List accounts
GET /social-media/my-social-accounts

# Schedule post
POST /social-posts  { posts: [{ content, mediaItems, scheduledAt, socialMediaId, firstComment? }], status?, approvalStatus?, controls: {} }

# Draft post (no scheduledAt needed)
POST /social-posts  { posts: [...], status: "DRAFT", controls: {} }

# List posts (page is 0-based, limit max 50)
GET /social-posts?page=0&limit=20
GET /social-posts?page=0&limit=50&platforms=X,LINKEDIN&statuses=SCHEDULED&from=2026-06-01T00:00:00Z&to=2026-06-30T23:59:59Z

# Delete post
DELETE /social-posts/:id

# Upload media (3 steps)
POST /file/get-signed-upload-urls  { contentType, count }
PUT  <signedUrl>  (raw file, matching Content-Type)
# then use key in mediaItems

# Pinterest boards
GET /social-media/:id/pinterest-boards

# YouTube playlists
GET /social-media/:id/youtube-playlists

# Post analytics (published posts with metrics)
GET /social-posts/analytics?startDate=...&endDate=...&platforms=...

# Connect link (for clients)
POST /social-media/connect-link  { expiryDays?, sendEmail?, email? }
```

## 给开发者的建议

- 请始终先调用 `my-social-accounts` 以获取有效的 `socialMediaId` 值。
- 对于媒体帖子，必须完成完整的三步上传流程（获取签名URL → 上传到S3 → 创建帖子）。
- `scheduledAt` 必须是ISO 8601 UTC格式，并且是未来的时间。
- Pinterest始终要求提供 `pinterestBoardId` — 请先获取板块信息。
- LinkedIn的文档帖子使用 `linkedinAttachmentKey` 而不是 `mediaItems`。
- 对于轮播帖子，在 `mediaItems` 中包含多个项目，并设置 `sortOrder`。
- TikTok视频的缩略图：在 `mediaItems` 中设置 `coverTimestamp`（以秒为单位）。
- 在跨平台发布时，请根据每个平台的限制调整内容长度（X：280个字符；Bluesky：300个字符；TikTok：2200个字符）。
- 如果用户未指定时间，建议设置为他们所在时区的明天上午9:00。
- 为了提高效率，每次API调用最多安排15条帖子。
- 使用 `firstComment` 功能添加CTA链接，以保持主帖子的简洁性并提高互动率。
- X（Twitter）通过API每天每个账户最多允许5条帖子——如果用户批量发布大量帖子，请提前提醒他们。
- 对于草稿帖子，将 `status` 设置为 `DRAFT` 并省略 `scheduledAt`，用户可以在PostFast仪表板中完成发布。
- 使用 `GET /social-posts` 并设置 `from`/`to` 参数来查看已安排的帖子，然后再添加新的帖子。