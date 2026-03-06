---
name: adaptlypost
description: 使用 AdaptlyPost API 可以在 Instagram、X（Twitter）、Bluesky、TikTok、Threads、LinkedIn、Facebook、Pinterest 和 YouTube 等平台上安排和管理社交媒体帖子。当用户需要安排社交媒体发布、管理社交媒体内容、上传用于发布的媒体文件、查看帖子状态、将内容跨平台发布，或自动化其社交媒体工作流程时，可以使用该工具。AdaptlyPost 是一款 SaaS 工具，无需自行托管。
homepage: https://adaptlypost.com
metadata: { 'openclaw': { 'emoji': '📬', 'primaryEnv': 'ADAPTLYPOST_API_KEY', 'requires': { 'env': ['ADAPTLYPOST_API_KEY'] } } }
---
# AdaptlyPost

通过一个API在9个平台上安排社交媒体帖子的发布。无需自行托管，提供SaaS服务。

## 设置

1. 在 https://adaptlypost.com/signup 注册。
2. 进入“设置” → “API令牌”，生成一个API令牌。
3. 设置环境变量：
   ```bash
   export ADAPTLYPOST_API_KEY="adaptly_your-token-here"
   ```

基础URL：`https://post.adaptlypost.com/post/api/v1`
认证头：`Authorization: Bearer $ADAPTLYPOST_API_KEY`

## 核心工作流程

### 1. 列出已连接的账户

```bash
curl -s -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  https://post.adaptlypost.com/post/api/v1/social-accounts
```

返回 `{ "accounts": [{ "id", "platform", "displayName", "username", "avatarUrl" }] }`。保存 `id`，在创建帖子时将其用作连接ID。

### 2. 立即发布帖子（不安排时间）

要立即发布，请完全省略 `scheduledAt` 并且不要设置 `saveAsDraft`：

```bash
curl -X POST https://post.adaptlypost.com/post/api/v1/social-posts \
  -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["TWITTER"],
    "contentType": "TEXT",
    "text": "This goes live right now!",
    "timezone": "America/New_York",
    "twitterConnectionIds": ["CONNECTION_ID_HERE"]
  }'
```

**重要提示**：不要将 `scheduledAt` 设置为未来的时间作为临时解决方案。省略 `scheduledAt` 是立即发布的正确方式。

返回 `{ "postId", "queuedPlatforms", "skippedPlatforms", "isScheduled", "scheduledAt" }`。

**重要提示**：必须在 `platforms` 中为每个平台提供正确的 `ConnectionIds` 数组。例如，如果要同时发布到Instagram和Twitter，需要包含 `instagramConnectionIds` 和 `twitterConnectionIds`。对于Facebook，则使用 `pageIds`。

### 3. 预安排文本帖子的发布时间

```bash
curl -X POST https://post.adaptlypost.com/post/api/v1/social-posts \
  -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["TWITTER"],
    "contentType": "TEXT",
    "text": "Your post text here",
    "timezone": "America/New_York",
    "scheduledAt": "2026-06-15T10:00:00.000Z",
    "twitterConnectionIds": ["CONNECTION_ID_HERE"]
  }'
```

### 4. 将帖子保存为草稿（不安排时间）

与安排时间类似，但设置 `saveAsDraft: true` 并省略 `scheduledAt`：

```bash
curl -X POST https://post.adaptlypost.com/post/api/v1/social-posts \
  -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["INSTAGRAM"],
    "contentType": "TEXT",
    "text": "Draft post to review later",
    "timezone": "Europe/London",
    "saveAsDraft": true,
    "instagramConnectionIds": ["CONNECTION_ID_HERE"]
  }'
```

### 5. 预安排带媒体的帖子（三步流程）

**步骤A** — 获取预签名的上传URL：

```bash
curl -X POST https://post.adaptlypost.com/post/api/v1/upload-urls \
  -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "files": [{ "fileName": "photo.jpg", "mimeType": "image/jpeg" }] }'
```

返回 `{ "urls": [{ "fileName", "uploadUrl", "publicUrl", "key", "expiresAt" }] }`。

**步骤B** — 将文件上传到存储：

```bash
curl -X PUT "UPLOAD_URL_HERE" \
  -H "Content-Type: image/jpeg" \
  --data-binary @/path/to/photo.jpg
```

**步骤C** — 使用公共URL创建帖子：

```bash
curl -X POST https://post.adaptlypost.com/post/api/v1/social-posts \
  -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["INSTAGRAM"],
    "contentType": "IMAGE",
    "text": "Post with image!",
    "mediaUrls": ["PUBLIC_URL_FROM_STEP_A"],
    "timezone": "America/New_York",
    "scheduledAt": "2026-06-15T10:00:00.000Z",
    "instagramConnectionIds": ["CONNECTION_ID_HERE"]
  }'
```

对于视频：使用 `mimeType: "video/mp4"`，`contentType: "VIDEO"`。
对于轮播图：上传多个文件，并在 `mediaUrls` 中包含所有公共URL，使用 `contentType: "CAROUSEL"`。

### 6. 列出帖子

```bash
curl -s -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  "https://post.adaptlypost.com/post/api/v1/social-posts?limit=20&offset=0"
```

返回 `{ "posts": [...], "total": 25, "hasMore": true }`。可以使用 `limit`（1-100，默认为20）和 `offset`（默认为0）进行分页。

### 7. 获取帖子详情

```bash
curl -s -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  https://post.adaptlypost.com/post/api/v1/social-posts/POST_ID
```

返回包含每个目标平台特定状态的完整帖子对象。

### 8. 跨平台发布

在单个请求中包含多个平台及其连接ID：

```bash
curl -X POST https://post.adaptlypost.com/post/api/v1/social-posts \
  -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["TWITTER", "BLUESKY", "LINKEDIN"],
    "contentType": "TEXT",
    "text": "Same post across 3 platforms!",
    "timezone": "America/New_York",
    "scheduledAt": "2026-06-15T10:00:00.000Z",
    "twitterConnectionIds": ["TWITTER_ID"],
    "blueskyConnectionIds": ["BLUESKY_ID"],
    "linkedinConnectionIds": ["LINKEDIN_ID"]
  }'
```

### 9. 为特定平台自定义文本

覆盖默认文本：

```bash
curl -X POST https://post.adaptlypost.com/post/api/v1/social-posts \
  -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["TWITTER", "LINKEDIN"],
    "contentType": "TEXT",
    "text": "Default text for all platforms",
    "platformTexts": [
      { "platform": "TWITTER", "text": "Short version for X #shortform" },
      { "platform": "LINKEDIN", "text": "Longer professional version with more detail for LinkedIn audience." }
    ],
    "timezone": "America/New_York",
    "scheduledAt": "2026-06-15T10:00:00.000Z",
    "twitterConnectionIds": ["TWITTER_ID"],
    "linkedinConnectionIds": ["LINKEDIN_ID"]
  }'
```

## 平台特定配置

将这些配置作为数组传递到请求体中。详细信息请参阅 [references/platform-configs.md](references/platform-configs.md)。

| 平台        | 配置字段       | 可选键值                                                                                                             |
| --------------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| **TikTok**      | `tiktokConfigs`    | `privacyLevel`（必填），`allowComments`，`allowDuet`，`allowStitch`，`sendAsDraft`，`brandedContent`，`autoAddMusic` |
| **Instagram**   | `instagramConfigs` | `postType`（FEED/REEL/STORY）                                                                 |
| **Facebook**    | `facebookConfigs`  | `postType`（FEED/REEL/STORY），`videoTitle`                                                                              |
| **YouTube**     | `youtubeConfigs`   | `postType`（VIDEO/SHORTS），`videoTitle`，`tags`，`privacyStatus`，`madeForKids`，`playlistId`                           |
| **Pinterest**   | `pinterestConfigs` | `boardId`（必填），`title`，`link`                                                                                   |
| **X (Twitter)** | —                  | 仅使用 `twitterConnectionIds`                                                                      |
| **Bluesky**     | —                  | 仅使用 `blueskyConnectionIds`                                                                      |
| **Threads**     | —                  | 仅使用 `threadsConnectionIds`                                                                      |
| **LinkedIn**    | —                  | 仅使用 `linkedinConnectionIds`                                                                     |

**TikTok配置示例：**

```bash
curl -X POST https://post.adaptlypost.com/post/api/v1/social-posts \
  -H "Authorization: Bearer $ADAPTLYPOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["TIKTOK"],
    "contentType": "VIDEO",
    "text": "Check out this clip!",
    "mediaUrls": ["https://cdn.adaptlypost.com/social-media-posts/uuid/video.mp4"],
    "timezone": "America/New_York",
    "scheduledAt": "2026-06-15T18:00:00.000Z",
    "tiktokConnectionIds": ["TIKTOK_ID"],
    "tiktokConfigs": [{
      "connectionId": "TIKTOK_ID",
      "privacyLevel": "PUBLIC_TO_EVERYONE",
      "allowComments": true,
      "allowDuet": false,
      "allowStitch": true
    }]
  }'
```

## 支持的上传文件类型

| MIME类型         | 扩展名   | 适用平台         |
| ----------------- | ----------- | ------------------------- |
| `image/jpeg`      | .jpg, .jpeg | 图片              |
| `image/png`       | .png        | 图片              |
| `image/webp`      | .webp       | 图片              |
| `video/mp4`       | .mp4        | 视频              |
| `video/quicktime` | .mov        | 视频              |

每次请求最多可上传1-20个文件。

## 媒体格式快速参考

| 平台    | 图片          | 视频                     | 轮播图        |
| ----------- | --------------- | ------------------------- | --------------- |
| TikTok      | 仅支持轮播图     | MP4/MOV格式，文件大小≤250MB，时长3-10分钟 | 最多2-35张图片     |
| Instagram   | JPEG/PNG        | 视频时长≤30秒（Reels）       | 最多10张图片     |
| Facebook    | 文件大小≤30MB，格式JPG/PNG | 每条帖子最多1张图片                | 最多10张图片     |
| YouTube     | 不支持轮播图     | 视频时长≤3分钟，格式H.264       | —               |
| LinkedIn    | 最多9张图片     | 视频时长≤10分钟                    | 最多9张图片     |
| X (Twitter) | 最多4张图片     | 不支持轮播图             | —               |
| Pinterest   | 建议比例2:3     | 支持轮播图                 | 最多2-5张图片      |
| Bluesky     | 不支持轮播图     | 不支持轮播图             | —               |
| Threads     | 支持轮播图     | 支持轮播图                 | 最多10张图片      |

## 代理使用提示

### 关键提示 — 发布前务必询问用户

- **切勿** 假定用户想要立即发布、安排时间或保存为草稿。**务必** 询问用户：“您是想现在发布、安排在特定时间发布，还是保存为草稿？” 在调用API之前等待用户的回答。
- 如果用户选择“立即发布”、“现在发布”或“马上处理”，请**完全省略`scheduledAt`字段** — 不要将其设置为未来的时间。当`scheduledAt`缺失时，API会立即执行发布。
- 如果用户选择“安排时间”，请询问具体的日期和时间，然后将`scheduledAt`设置为ISO 8601时间戳。
- 如果用户选择“保存为草稿”，请设置`saveAsDraft: true`并省略`scheduledAt`。

### 时区处理

- 每次创建帖子请求时都必须提供 `timezone` 字段。
- **首次交互时**，询问用户：“您所在的时区是什么？（例如：Europe/Berlin, America/New_York）”。一旦用户回答，**在后续的所有帖子中都使用该时区设置**，无需再次询问。
- 如果用户之前已经告知过时区，请直接使用该时区设置。
- 常见时区：`Europe/London`，`Europe/Berlin`，`Europe/Paris`，`America/New_York`，`America/Chicago`，`America/Los_Angeles`，`Asia/Tokyo`，`Australia/Sydney`。

### API工作流程

- 首先调用 `/social-accounts` 以获取每个平台的有效连接ID。
- 对于带有媒体的帖子，需要完成完整的三个步骤：获取上传URL → 上传文件 → 使用 `mediaUrls` 创建帖子。
- `scheduledAt` 必须是ISO 8601格式，并且表示未来的时间。当使用 `saveAsDraft: true` 时可以省略该字段。
- 每个平台都需要对应的连接ID：`twitterConnectionIds`，`instagramConnectionIds`，`blueskyConnectionIds`，`linkedinConnectionIds`，`tiktokConnectionIds`，`threadsConnectionIds`，`pinterestConnectionIds`，`youtubeConnectionIds`。Facebook使用 `pageIds`。
- TikTok配置中必须设置 `privacyLevel`（例如：`PUBLIC_TO_EVERYONE`）。
- Pinterest配置中必须设置 `boardId`（目前无法通过此API获取板块信息，因此需要询问用户使用哪个板块）。
- 对于轮播图，需要上传多个文件并将所有公共URL包含在 `mediaUrls` 中。
- 在跨平台发布时，使用 `platformTexts` 来自定义每个平台的文本。
- 内容类型：`TEXT`（无媒体），`IMAGE`（单张图片），`VIDEO`（单视频），`CAROUSEL`（多张图片/视频）。
- 查看响应中的 `skippedPlatforms` 字段 — 该字段会显示是否跳过了某些平台以及原因。