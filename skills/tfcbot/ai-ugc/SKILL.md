---
name: rawugc-api
description: 调用 RawUGC API 可以生成 AI 视频/图片/音乐，管理内容（如人物角色、产品信息、风格设定等），安排社交媒体发布计划，研究 TikTok 上的热门内容，并分析那些具有高传播力的视频。当用户需要与 RawUGC API 的任何终端点进行交互时，都可以使用该 API。
requires:
  env:
    - RAWUGC_API_KEY
compatibility: Requires RAWUGC_API_KEY (Bearer token for https://rawugc.com/api/v1). Obtain from RawUGC dashboard.
homepage: https://github.com/tfcbot/rawugc-skills
source: https://github.com/tfcbot/rawugc-skills
---
# RawUGC API

以下是关于RawUGC API的详细说明，包括代理程序调用该API所需的过程知识。所有请求都需要从RawUGC控制面板获取API密钥，该密钥通过环境变量传递。

## 认证

- **环境变量**：从`RAWUGC_API_KEY`中读取API密钥。此密钥在RawUGC控制面板中创建，必须保密；切勿将其硬编码或记录在日志中。
- **请求头**：在每个请求中添加`Authorization: Bearer <RAWUGC_API_KEY>`。
- 如果`RAWUGC_API_KEY`缺失或为空，应通知用户设置密钥并从RawUGC控制面板获取它。

## 基本URL

- **生产环境**：`https://rawugc.com/api/v1`
- 以下所有路径都是相对于此基本URL的。

## API版本控制

RawUGC使用基于日期的API版本控制。当前最新版本为`2026-03-06`。

- **`RawUGC-Version`请求头**：建议根据每个请求覆盖版本号。
- **API密钥固定的版本**：在控制面板创建密钥时设置。
- **回退**：如果两者均未设置，则使用最新版本（`2026-03-06`）。

为了确保行为的一致性，请在所有请求中始终发送`RawUGC-Version: 2026-03-06`。

---

## 视频生成

### POST /videos/generate

启动视频生成。

**请求体（JSON）**：

| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `model` | string | 是 | `sora-2-text-to-video`、`sora-2-image-to-video`、`kling-2.6/motion-control`、`veo3`、`veo3_fast` |
| `prompt` | string | 用于text-to-video / veo3 | 文本描述（1-5000个字符） |
| `imageUrls` | string[] | 用于image-to-video / kling | 图片URL（最多10张）。veo3/veo3_fast最多接受2张可选图片。 |
| `videoUrls` | string[] | 用于kling | 视频URL（最多1张）。`kling-2.6/motion-control`需要此字段 |
| `aspectRatio` | string | 否 | Sora：`portrait`/`landscape`。Veo3：`16:9`/`9:16`/`Auto` |
| `nFrames` | string | 否 | `"10"` 或 `"15"`（仅适用于Sora） |
| `selectedCharacter` | string | 否 | 角色用户名（例如`rawugc.mia`） |
| `characterOrientation` | string | 否 | `image` 或 `video`（仅适用于kling） |
| `mode` | string | 否 | `720p` 或 `1080p`（仅适用于kling） |

**响应（201）**：`videoId`、`model`、`status`、`creditsUsed`、`newBalance`、`estimatedCompletionTime`、`createdAt`。

### GET /videos/:videoId

获取视频状态。返回`videoId`、`status`、`model`、`prompt`、`creditsUsed`、`url`（完成后）、`createdAt`、`completedAt`、`failCode`、`failMessage`、`versions`（编辑历史记录数组）。

### GET /videos

列出视频。查询参数：`status`、`limit`（1-100，默认50）、`page`。返回`videos`数组及分页信息。

### POST /videos/captions

为已完成的视频添加带样式的字幕。费用为1个信用点。

| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `videoId` | string | 是 | 视频标识符（vid_xxx） |
| `language` | string | 否 | 语言代码（例如`en`）。默认自动检测 |

**响应（200）**：`videoId`、`url`、`version`、`operation`、`creditsUsed`。

---

## 图像生成

### POST /images/generate

使用Nano Banana模型生成AI图像。异步操作——通过GET /images/:imageId获取生成结果。

| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `model` | string | 是 | `nano-banana-2`（文本转图像，需4个信用点）或`google/nano-banana-edit`（图像编辑，需2个信用点） |
| `prompt` | string | 是 | 文本描述或编辑指令（1-20000个字符） |
| `imageUrls` | string[] | 用于编辑 | 源图像。`google/nano-banana-edit`需要此字段。`nano-banana-2`可选。 |
| `aspectRatio` | string | 否 | 对于`nano-banana-2`：`1:1`、`16:9`、`9:16`、`auto`等 |
| `imageSize` | string | 否 | 对于`google/nano-banana-edit`：`1:1`、`16:9`、`9:16`、`auto`等 |
| `resolution` | string | 否 | 对于`nano-banana-2`：`1K`、`2K`、`4K` |
| `outputFormat` | string | 否 | `png`、`jpeg`、`jpg` |
| `googleSearch` | boolean | 否 | 是否使用Google网络搜索（仅适用于`nano-banana-2`） |

**响应（201）**：`imageId`、`model`、`status`、`creditsUsed`、`newBalance`、`estimatedCompletionTime`、`createdAt`。

### GET /images/:imageId

获取图像状态。返回`imageId`、`status`、`model`、`prompt`、`url`（完成后）、`imageSize`、`resolution`、`outputFormat`、`creditsUsed`、`createdAt`、`completedAt`、`failCode`、`failMessage`。

### GET /images

列出图像。查询参数：`status`、`limit`（1-100，默认20）、`page`。返回`images`数组及分页信息。

---

## 音乐生成

### POST /music/generate

使用Suno模型生成AI音乐。每次生成需3个信用点。异步操作——通过GET /music/:musicId获取生成结果。

| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `prompt` | string | 是 | 音乐描述（1-2000个字符） |
| `model` | string | 否 | `V3_5`、`V4`、`V4_5`、`V4_5PLUS`、`V4_5ALL`、`V5`（默认：`V5`） |
| `instrumental` | boolean | 否 | 仅限器乐，不含人声（默认：true） |
| `title` | string | 否 | 曲目标题（最多200个字符）。`style`参数可用于自定义风格。 |
| `style` | string | 否 | 风格描述（最多500个字符，例如`lo-fi hip hop`） |

**响应（201）**：`musicId`、`model`、`status`、`creditsUsed`、`newBalance`、`estimatedCompletionTime`、`createdAt`。

### GET /music/:musicId

获取音乐状态。返回`musicId`、`status`、`model`、`prompt`、`audioUrl`（完成后）、`albumArtUrl`、`duration`、`title`、`creditsUsed`、`createdAt`、`completedAt`、`failCode`、`failMessage`。

### GET /music

列出音乐曲目。查询参数：`status`、`limit`（1-100，默认20）、`page`。返回`tracks`数组及分页信息。

---

## 上传

### POST /upload

上传视频或图像文件。返回一个URL，可用于后续的生成请求（`imageUrls`、`videoUrls`）或`analyze-video`。文件大小上限为100MB。

**请求方式**：使用`multipart/form-data`，并包含`file`字段。支持的文件类型：`video/mp4`、`video/quicktime`、`video/webm`、`image/png`、`image/webp`。

**响应（200）**：`url`、`contentType`、`size`。

---

## 角色

### GET /characters

列出所有可用的AI角色（内置角色+自定义角色）。返回`characters`数组、`count`、`adminCount`、`userCount`。

### GET /characters/:characterId

通过ID获取角色信息。返回 `_id`、`username`、`displayName`、`description`、`videoPreviewUrl`、`type`（`admin`/`user`）、`isActive`、`createdAt`、`updatedAt`。

---

## 人物角色（CRUD）

人物角色用于定义内容计划的目标受众。

- **GET /personas** —— 列出所有角色。返回`personas`数组及数量。
- **POST /personas** —— 创建新角色。请求体：`name`（必填，最多200个字符）、`description`（必填，最多5000个字符）。返回`id`。
- **GET /personas/:personaId** —— 获取指定角色信息。
- **PATCH /personas/:personaId** —— 更新角色信息。请求体：`name`、`description`（可选）。
- **DELETE /personas/:personaId** —— 删除角色。

**PersonaResponse**：`_id`、`organizationId`、`name`、`description`、`createdAt`、`updatedAt`。

---

## 消息系统（CRUD）

用于创建和管理品牌/定位相关的消息模板。

- **GET /messaging** —— 列出所有消息模板。返回`messages`数组及数量。
- **POST /messaging** —— 创建新消息模板。请求体：`name`（必填，最多200个字符）、`body`（必填，最多5000个字符）。返回`id`。
- **GET /messaging/:messageId** —— 获取指定消息模板。
- **PATCH /messaging/:messageId** —— 更新消息模板。请求体：`name`、`body`（可选）。
- **DELETE /messaging/:messageId** —— 删除消息模板。

**MessagingResponse**：`_id`、`organizationId`、`name`、`body`、`createdAt`、`updatedAt`。

---

## 产品

用于视频生成的产品信息。

- **GET /products** —— 列出所有产品。返回`products`数组及数量。
- **POST /products** —— 创建新产品。请求体：`name`（必填，最多200个字符）、`photos`（必填，URL数组）、`description`（最多1000个字符）、`messaging`（最多5000个字符）。返回`id`。
- **GET /products/:productId** —— 获取指定产品信息。
- **PATCH /products/:productId** —— 更新产品信息。请求体：`name`、`description`、`photos`、`messaging`（可选）。
- **DELETE /products/:productId** —— 删除产品。

**ProductResponse**：`_id`、`name`、`description`、`photos`、`messaging`、`createdAt`、`updatedAt`。

---

## 风格设置

用于视频/图像的创意风格设置，支持自定义提示模板。

- **GET /styles** —— 列出所有风格（内置风格+自定义风格）。查询参数：`type`（`video`/`image`）。返回`styles`数组及数量。
- **POST /styles** —— 创建新风格。请求体：`name`（必填，最多200个字符）、`description`（最多1000个字符）、`type`（`video`/`image`）、`aspectRatio`（`portrait`/`landscape`/`square`）、`promptTemplate`（最多5000个字符，支持`{productName}`、`{messaging}`、`{character}`占位符）。返回`id`。
- **GET /styles/:styleId** —— 获取指定风格信息。
- **PATCH /styles/:styleId** —— 更新风格信息。所有字段均可修改。
- **DELETE /styles/:styleId** —— 删除风格。

**StyleResponse**：`_id`、`name`、`description`、`type`、`aspectRatio`、`styleId`、`isAdmin`、`isStandard`。

---

## 社交媒体调度

### GET /socialaccounts

列出关联的社交媒体账户（每个组织最多3个）。返回`accounts`数组及数量。每个账户包含：`accountId`、`platform`（`tiktok`/`instagram`/`youtube`）、`username`、`displayName`、`profilePicture`、`isActive`。

### POST /socialaccounts

同步来自调度提供商的关联账户。返回`{ success: boolean }`。

### DELETE /social/accounts/:accountId

删除关联的社交媒体账户。返回`{ success: boolean }`。

### POST /social/posts

安排、草拟或立即发布视频到社交媒体。

| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `videoUrl` | string | 是 | 要发布的视频URL |
| `accountIds` | string[] | 是 | 目标账户ID |
| `mode` | string | 是 | `schedule`、`draft`或`now` |
| `scheduledFor` | integer | 安排时间（Unix时间戳，单位：毫秒） |
| `timezone` | string | 否 | IANA时区（默认：`UTC`） |
| `content` | string | 否 | 标题（最多2200个字符） |
| `videoId` | string | 否 | 需要链接的RawUGC视频ID |
| `publishToInbox` | boolean | 否 | 是否发送到TikTok创作者收件箱 |
| `tiktokPrivacyLevel` | string | 否 | `SELF_ONLY`、`PUBLIC_TO_EVERYONE`、`MUTUAL_follow FRIENDS`、`FOLLOWER_OF_CREATOR` |
| `tiktokAllowComment` | boolean | 否 | 是否允许TikTok评论 |
| `tiktokAllowDuet` | boolean | 是否允许TikTok双人合作 |
| `tiktokAllowStitch` | boolean | 是否允许TikTok拼接效果 |
| `tiktokCommercialContentType` | string | 否 | `none`、`brand_organic`、`brand_content` |

**响应（201）**：`SocialPost`对象。

### GET /social/posts

列出所有帖子。查询参数：`fromDate`（毫秒）、`toDate`（毫秒）、`includeDrafts`（是否包含草稿）。返回`posts`数组及分页信息。

### GET /social/posts/:postId

获取指定帖子的详细信息。

### PATCH /social/posts/:postId

更新帖子。请求体：`content`、`scheduledFor`、`timezone`、`accountIds`（至少需要填写一个字段）。

### DELETE /social/posts/:postId

删除帖子。返回`{ success: boolean }`。

### POST /social/posts/:postId/reschedule

重新安排帖子的发布时间。请求体：`scheduledFor`（必填，单位：毫秒）。

### POST /social/posts/:postId/publish

立即发布草稿帖子。

**SocialPost**对象包含：`postId`、`platforms`、`status`（`draft`/`scheduled`/`published`/`failed`）、`scheduledFor`、`timezone`、`content`、`videoUrl`、`createdAt`、`publishedAt`。

---

## 病毒式传播库

### GET /viral-library/videos/:videoId

获取带有完整AI分析结果的病毒式传播视频（包括关键帧和性能数据）。返回`ViralLibraryVideo`对象。

### GET /viral-library/search

对分析后的视频进行语义搜索。查询参数：`q`（必填，自然语言查询）、`limit`（1-50，默认20）。返回`results`数组（每个元素包含`video`、`score`），以及`query`和`total`。

---

## 数据抓取

### POST /scrape-tiktok

抓取TikTok视频。费用为3个信用点。

| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `query` | string | 是 | 搜索关键词或标签（最多500个字符） |
| `mode` | string | 否 | `keyword`、`hashtag`、`search`（默认：`keyword`） |
| `limit` | integer | 否 | 1-10（默认：10） |

**响应（200）**：`scrapeId`（用于后续内容计划生成）、`count`、`videos`数组（包含`id`、`url`、`author`、`description`、`stats`、`duration`、`hashtags`、`thumbnail`、`videoUrl`）。

### POST /content-plans

根据抓取到的视频生成内容计划。费用为3个信用点。

| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `scrapeId` | string | 是 | 来自`scrape-tiktok`的请求ID |
| `brief` | string | 是 | 内容计划目标（最多5000个字符） |

**响应（200）**：`planId`、`scrapeId`、`brief`、`topWins`、`gapsToTest`、`blueprints`数组（包含`category`、`strategy`、`evidence`、`contentIdeas`）。

### GET /content-plans

列出所有内容计划。返回`plans`数组及数量。

### POST /analyze-video

分析任何视频URL（包括社交媒体链接或直接链接）。费用为1个信用点。文件大小上限为150MB。

| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `videoUrl` | string | 是 | 需要分析的视频URL |
| `prompt` | string | 否 | 自定义分析提示（最多5000个字符） |

**响应（200）**：`summary`、`hook`、`keyframes`数组（包含`timestamp`、`type`、`description`、`visual`、`audio`、`text`）、`durationSeconds`、`tags`、`whyItPerformed`、`attributesToCopy`、`hooksToTest`。

---

## 错误处理

所有错误响应均遵循RFC 7807规范（JSON格式）：`type`、`title`、`status`、`detail`、`instance`、`errors`。

| 状态 | 含义 |
|--------|---------|
| 400 | 验证错误。向用户显示`detail`和`errors`信息。 |
| 401 | 认证错误。请检查`RAWUGC_API_KEY`。 |
| 402 | 信用点不足。请在控制面板中补充信用点。 |
| 403 | 权限不足。API密钥缺乏相应权限。 |
| 404 | 资源未找到。 |
| 429 | 超过请求频率限制。请查看`X-RateLimit-Reset`头部信息。 |
| 500 | 服务器错误。请重试或联系技术支持。 |

## 请求频率限制

- API密钥：每分钟10次请求。
- 会话限制：每分钟20次请求。
- 相关头部字段：`X-RateLimit-Limit`、`X-RateLimit-Remaining`、`X-RateLimit-Reset`（Unix时间戳）。

## 工作流程：

1. **生成**：向生成端点发送POST请求。注意返回的ID（`videoId`/`imageId`/`musicId`）。
2. **检查状态**：定期（10-30秒）向状态端点发送GET请求。使用指数退避策略。
3. **完成**：当状态为`completed`时，使用生成的视频URL。如果失败，向用户显示错误信息。
4. **编辑**（仅针对视频）：向`/videos/captions`或`/videos/overlay`发送POST请求。

有关完整的请求/响应格式，请参考[reference.md](reference.md)。