---
name: postfast
description: 使用 PostFast API 来安排和管理在 TikTok、Instagram、Facebook、X（Twitter）、YouTube、LinkedIn、Threads、Bluesky 和 Pinterest 上的社交媒体帖子。当用户需要安排社交媒体发布、管理社交媒体内容、上传用于发布的媒体文件、列出已连接的社交媒体账户、查看已安排的帖子、删除已安排的帖子、将内容跨多个平台发布，或自动化其社交媒体工作流程时，可以使用该工具。PostFast 是一款 SaaS 工具，无需自行托管。
homepage: https://postfa.st
metadata: {"openclaw":{"emoji":"⚡","primaryEnv":"POSTFAST_API_KEY","requires":{"env":["POSTFAST_API_KEY"]}}}
---

# PostFast

通过一个API在9个平台上安排社交媒体发布。属于SaaS服务，无需自行托管。

## 设置

1. 在 [https://app.postfa.st/register](https://app.postfa.st/register) 注册。
2. 进入“工作区设置”（Workspace Settings），生成API密钥。
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

返回一个包含 `{ id, platform, platformUsername, displayName }` 的数组。保存 `id`，它将用作发布的 `socialMediaId`。

### 2. 安排纯文本帖子（无需媒体）

```bash
curl -X POST https://api.postfa.st/social-posts \
  -H "pf-api-key: $POSTFAST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "posts": [{
      "content": "Your post text here",
      "mediaItems": [],
      "scheduledAt": "2025-06-15T10:00:00.000Z",
      "socialMediaId": "ACCOUNT_ID_HERE"
    }],
    "controls": {}
  }'
```

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

**步骤C** — 使用媒体键创建帖子：
```bash
curl -X POST https://api.postfa.st/social-posts \
  -H "pf-api-key: $POSTFAST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "posts": [{
      "content": "Post with image!",
      "mediaItems": [{ "key": "image/uuid.png", "type": "IMAGE", "sortOrder": 0 }],
      "scheduledAt": "2025-06-15T10:00:00.000Z",
      "socialMediaId": "ACCOUNT_ID_HERE"
    }],
    "controls": {}
  }'
```

对于视频：使用 `contentType: "video/mp4"`，`type: "VIDEO"`，键前缀为 `video/`。

### 4. 列出已安排的帖子

```bash
curl -s -H "pf-api-key: $POSTFAST_API_KEY" https://api.postfa.st/social-posts
```

### 5. 删除已安排的帖子

```bash
curl -X DELETE -H "pf-api-key: $POSTFAST_API_KEY" https://api.postfa.st/social-posts/POST_ID
```

### 6. 跨平台发布

在 `posts` 数组中包含多个条目，每个条目都有不同的 `socialMediaId`。它们共享相同的 `controls` 和 `mediaItems` 键。

## 平台特定的控制参数

将这些参数传递给 `controls` 对象。详细信息请参见 [references/platform-controls.md](references/platform-controls.md)。

| 平台 | 控制参数 |
|---|---|
| **TikTok** | `tiktokPrivacy`, `tiktokAllowComments`, `tiktokAllowDuet`, `tiktokAllowStitch`, `tiktokIsDraft`, `tiktokBrandContent`, `tiktokAutoAddMusic` |
| **Instagram** | `instagramPublishType`（TIMELINE/STORY/REEL），`instagramPostToGrid`, `instagramCollaborators` |
| **Facebook** | `facebookContentType`（POST/REEL/STORY） |
| **YouTube** | `youtubeIsShort`, `youtubeTitle`, `youtubePrivacy`, `youtubePlaylistId`, `youtubeTags`, `youtubeMadeForKids` |
| **LinkedIn** | `linkedinAttachmentKey`, `linkedinAttachmentTitle`（用于文档帖子） |
| **X (Twitter)** | `xQuoteTweetUrl`（用于引用推文） |
| **Pinterest** | `pinterestBoardId`（必填），`pinterestLink` |
| **Bluesky** | 无平台特定控制参数 — 仅支持文本和图片 |
| **Threads** | 无平台特定控制参数 — 仅支持文本和图片/视频 |

## 帮助端点

- **Pinterest板块**：`GET /social-media/{id}/pinterest-boards` → 返回 `[{ boardId, name }]`
- **YouTube播放列表**：`GET /social-media/{id}/youtube-playlists` → 返回 `[{ playlistId, title }]`

## 速率限制

- 每个API密钥的速率限制为：60次/分钟，150次/5分钟，300次/小时，2000次/天
- 查看 `X-RateLimit-Remaining-*` 头部字段
- 如果达到速率限制，返回429状态码，请查看 `Retry-After-*` 头部字段

## 媒体格式快速参考

| 平台 | 图片 | 视频 | 轮播图 |
|---|---|---|---|
| TikTok | 仅支持轮播图 | 大小≤250MB，格式MP4/MOV，时长3秒至10分钟 | 最多2-35张图片 |
| Instagram | 格式JPEG/PNG | 大小≤1GB，时长3-90秒（Reels） | 最多10张图片 |
| Facebook | 大小≤30MB，格式JPG/PNG | 每条帖子最多1张图片 | 最多10张图片 |
| YouTube | 不支持图片 | 视频时长≤3分钟，格式H.264 | — |
| LinkedIn | 最多9张图片 | 视频时长≤10分钟 | 最多9张图片，或支持文档（PDF/PPTX/DOCX） |
| X (Twitter) | 最多4张图片 | 不支持图片 | — |
| Pinterest | 建议使用2:3的比例 | 支持轮播图 | 最多2-5张图片 |
| Bluesky | 不支持图片 | 仅支持文本和视频 |
| Threads | 支持图片和视频 | 最多10张图片 |

## 代理使用提示

- 在使用其他功能前，务必先调用 `my-social-accounts` 以获取有效的 `socialMediaId` 值。
- 对于带媒体的帖子，请完成完整的上传流程（获取签名URL → 上传到S3 → 创建帖子）。
- `scheduledAt` 必须为ISO 8601 UTC格式，并且表示未来的时间。
- Pinterest始终需要 `pinterestBoardId` — 请先获取相关板块信息。
- LinkedIn的文档帖子使用 `linkedinAttachmentKey` 而不是 `mediaItems`。
- 对于轮播图，需要在 `mediaItems` 中包含多个图片，并指定顺序（`sortOrder`）。
- TikTok视频缩略图：在 `mediaItems` 中设置 `coverTimestamp`（以秒为单位）。