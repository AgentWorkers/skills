---
name: powerpost
description: 通过一个命令生成社交媒体内容，并将其发布到所有主要平台上。
version: 0.2.0
metadata:
  openclaw:
    requires:
      env:
        - POWERPOST_API_KEY
        - POWERPOST_WORKSPACE_ID
      bins:
        - curl
    primaryEnv: POWERPOST_API_KEY
    emoji: "⚡"
    homepage: https://powerpost.ai
---
# PowerPost 技能

PowerPost 可以生成社交媒体配文、图片和视频，并通过一个统一的 API 将内容发布到 Instagram、TikTok、X/Twitter、YouTube、Facebook 和 LinkedIn 上。

## 设置

用户需要两个凭据：

- `POWERPOST_API_KEY`：他们的 API 密钥（以 `pp_live_sk_` 开头）。他们可以在 https://powerpost.ai/settings/api 创建一个 API 密钥。
- `POWERPOST_WORKSPACE_ID`：他们的工作空间 ID。可以在 https://powerpost.ai/settings/workspaces 查到。

在 OpenClaw 中有两种配置这些凭据的方法。API 密钥可以直接在 Skills UI 的 “API key” 字段中输入，或者通过配置文件设置。工作空间 ID 必须通过配置文件设置，因为 UI 只为每个技能提供一个字段：

```bash
openclaw config set skills.entries.powerpost.apiKey "pp_live_sk_YOUR_KEY"
openclaw config set skills.entries.powerpost.env.POWERPOST_WORKSPACE_ID "YOUR_WORKSPACE_ID"
```

API 密钥有两种类型：
- `read_write`：具有完整的访问权限，包括发布功能。
- `read_draft`：可以生成内容并创建草稿，但无法发布（会返回 403 错误）。当需要人工审核后再发布内容时使用。

新账户初始有 50 个免费信用点。价格详情请查看 https://powerpost.ai/pricing。

## 首次运行

在运行任何 PowerPost 命令之前，请确保这两个凭据都已设置。如果缺少任意一个凭据，请指导用户完成设置：

1. 如果 `POWERPOST_API_KEY` 未设置：
   - 询问用户是否拥有 PowerPost 账户。如果没有，他们可以在 https://powerpost.ai/login 注册。
   - 指导他们前往 https://powerpost.ai/settings/api 创建 API 密钥。
   - 他们可以将密钥粘贴到 OpenClaw UI 的 “API key” 字段中，或者运行：`openclaw config set skills.entries.powerpost.apiKey "pp_live_sk_..."`。

2. 如果 `POWERPOST_WORKSPACE_ID` 未设置：
   - 指导他们前往 https://powerpost.ai/settings/workspaces 查找工作空间 ID。
   - 他们需要运行：`openclaw config set skills.entries.powerpost.env.POWERPOST_WORKSPACE_ID "他们的-workspace-id"` — UI 没有专门用于设置工作空间 ID 的字段，必须通过配置文件设置。

3. 设置完成后，通过调用 `GET /account/credits` 来验证凭据是否正确。如果返回余额，则说明设置成功；如果返回 401 错误，则说明 API 密钥有误。

在确认两个凭据都正确之前，不要运行其他 PowerPost 命令。

## 基本 URL

所有请求的地址为：

```
https://powerpost.ai/api/v1
```

## 认证头部

每个请求都需要 `x-api-key`（或 `Authorization: Bearer <key>`）。所有内容端点还需要 `X-Workspace-Id`。唯一的例外是 `GET /account/credits`，它只需要 `x-api-key`。

```
x-api-key: $POWERPOST_API_KEY
X-Workspace-Id: $POWERPOST_WORKSPACE_ID
```

## 核心工作流程

标准的 PowerPost 流程如下：

1. **检查信用点**，确保用户有足够的余额。
2. **根据文本、图片或视频生成内容**（异步操作，返回生成 ID）。
3. 每 2-3 秒轮询一次结果，直到状态变为 `completed` 或 `failed`。
4. （可选）根据配文或文本提示生成图片或视频（也是异步操作）。
5. 将生成的配文和图片组合成草稿。
6. 在发布前向用户展示草稿以供审核。
7. 将草稿发布到连接的社交平台。

在生成内容之前，请务必检查信用点，并在调用发布端点之前向用户展示将要发布的内容并获得确认。

---

## 端点

### 1. 检查信用点

使用此端点来检查用户在开始生成内容之前的信用点余额。

```bash
curl https://powerpost.ai/api/v1/account/credits \
  -H "x-api-key: $POWERPOST_API_KEY"
```

注意：此端点不需要 `X-Workspace-Id` 头部。

响应：

```json
{
  "balance": 47
}
```

向用户显示当前的余额。如果余额不足，在开始生成内容之前提醒他们。

### 信用点费用

不同操作的信用点费用如下：
- **配文生成**：取决于研究模式、输入类型、源 URL 的数量以及视频长度。
- **图片生成**：取决于使用的模型和数量。
- **视频生成**：取决于使用的模型、时长以及是否启用音频。
- **发布**：取决于平台。像 X 这样的高级平台费用更高。

每个 API 响应中都会通过 `credits_used` 和 `remaining_credits` 显示具体费用。在开始生成内容之前，请务必检查信用点余额，以便用户提前了解费用。

只有成功完成的操作才会计费。失败的生成、失败的发布尝试以及失败的 URL 抓取操作都会退还信用点。

---

### 2. 上传媒体

当用户希望从图片或视频生成内容，或者希望将媒体附加到帖子中时，使用此端点。

```bash
curl -X POST https://powerpost.ai/api/v1/media/upload \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID" \
  -F "file=@/path/to/file" \
  -F "type=image"
```

`type` 字段必须是 `image` 或 `video`。

支持的格式：
- 图片：JPEG、PNG、WebP（最大 10 MB）
- 视频：MP4、MOV、WebM（最大 500 MB）

响应：

```json
{
  "media_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "type": "image",
  "file_name": "photo.jpg",
  "file_size": 245000,
  "mime_type": "image/jpeg",
  "created_at": "2026-01-10T18:30:00Z"
}
```

保存响应中的 `media_id`。您需要这个 ID 来生成内容（在 `media_ids` 字段中）或创建帖子（在帖子项的 `media_ids` 中）。

向用户确认上传成功，并显示文件名称和大小。

---

### 3. 生成内容

当用户希望创建社交媒体配文时，使用此端点。

根据提供的字段，有三种输入模式：
- **仅文本**：发送 `prompt`（必填，3-2000 个字符）。
- **图片输入**：发送 `media_ids`（附带图片 ID，可选 `prompt` 作为上下文）。
- **视频输入**：发送 `media_ids`（附带视频 ID，可选 `prompt` 作为上下文）。

您必须提供 `prompt` 或 `media_ids`（或两者都提供）。

```bash
curl -X POST https://powerpost.ai/api/v1/content/generate \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "We just shipped dark mode across all our apps",
    "post_types": ["instagram-reel", "tiktok-video", "x-post"],
    "research_mode": "regular"
  }'
```

**必填字段**：
- `post_types`（字符串数组）：至少选择一个帖子类型。请参见下面的帖子类型表。
- `research_mode`（字符串）：`regular` 或 `deep`。快速任务使用 `regular`，重要帖子使用 `deep`。

**可选字段**：
- `writing_style_id`（字符串）：在仪表板中创建的自定义写作风格 ID。
- `cta_text`（字符串，最多 100 个字符）：自定义的呼吁行动语。
- `source_urls`（字符串数组，最多 10 个）：用于抓取研究上下文的 URL。必须是 HTTPS 格式。为了安全起见，系统会过滤掉私有/内部 URL。每个 URL 都会增加生成成本。

**帖子类型**：

| 平台      | 帖子类型                                      |
|-----------|-------------------------------------------------------|
| Instagram   | `instagram-feed`、`instagram-reel`、`instagram-story`          |
| TikTok     | `tiktok-video`、`tiktok-photos`                          |
| YouTube    | `youtube-video`、`youtube-short`                          |
| X         | `x-post`                                      |
| Facebook    | `facebook-post`、`facebook-reel`、`facebook-story`          |
| LinkedIn   | `linkedin-post`                                |

同一平台下的多个帖子类型会生成一个共享的配文。帖子类型决定了发布格式。

响应：

```json
{
  "generation_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "credits_used": 10,
  "remaining_credits": 90,
  "status_url": "/api/v1/content/generations/550e8400-e29b-41d4-a716-446655440000"
}
```

告诉用户生成已经开始，生成所需的信用点数量，并等待生成完成。然后立即开始轮询。

---

### 4. 获取生成状态（轮询）

在开始生成后，每 2-3 秒轮询一次此端点，直到状态变为 `completed` 或 `failed`。不要轮询超过 60 次（大约 2 分钟）。

```bash
curl https://powerpost.ai/api/v1/content/generations/GENERATION_ID \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID"
```

**处理中**：

```json
{
  "generation_id": "550e8400-...",
  "status": "processing",
  "prompt": "We just shipped dark mode",
  "platforms": ["tiktok", "instagram"],
  "research_mode": "regular",
  "credits_used": 10,
  "created_at": "2026-01-10T18:30:00Z"
}
```

如果状态仍为 `processing` 或 `pending`，等待 3 秒后再进行轮询。

**完成时**：

```json
{
  "generation_id": "550e8400-...",
  "status": "completed",
  "prompt": "We just shipped dark mode",
  "platforms": ["tiktok", "instagram"],
  "research_mode": "regular",
  "credits_used": 10,
  "created_at": "2026-01-10T18:30:00Z",
  "outputs": {
    "tiktok": "Dark mode activated! POV: your eyes at 2am finally getting some relief... #darkmode #tech",
    "instagram": "Dark mode is here!\n\nYour late-night scrolling just got easier on the eyes... #DarkMode #ProductUpdate"
  }
}
```

`outputs` 对象按平台名称进行分组（而不是按帖子类型）。每个值都是一个字符串，除了 YouTube，YouTube 的响应中包含 `title` 和 `description`：

```json
"youtube": {
  "title": "We Just Shipped Dark Mode",
  "description": "Dark mode is finally here across all our apps... #darkmode"
}
```

完成生成后，向用户显示所有生成的配文，并明确标注每个配文对应的平台。

**失败时**：

响应中包含一个 `error` 对象，其中包含 `code` 和 `message`。如果生成失败，系统会退还信用点。告诉用户生成失败，并显示错误信息。

---

### 5. 列出生成内容

当用户想要查看最近的生成内容或搜索过去的生成内容时，使用此端点。

```bash
curl "https://powerpost.ai/api/v1/content/generations?status=completed&limit=10" \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID"
```

查询参数（全部可选）：
- `status` — 按 `pending`、`processing`、`completed`、`failed` 进行过滤
- `limit` — 每页显示的结果数量，1-100 个（默认 20 个）
- `cursor` — 基于上一次响应中的 `next_cursor` 进行分页

响应：

```json
{
  "data": [
    {
      "generation_id": "550e8400-...",
      "status": "completed",
      "prompt": "We just shipped dark mode",
      "platforms": ["tiktok", "instagram"],
      "research_mode": "regular",
      "credits_used": 10,
      "created_at": "2026-01-10T18:30:00Z"
    }
  ],
  "next_cursor": "gen_cursor_abc123",
  "has_more": true
}
```

列表端点不包含 `outputs`。要获取特定生成的完整内容，请使用带有其 ID 的获取端点。

向用户显示生成的摘要表格。如果用户想要查看某个生成的内容，可以使用获取端点来获取具体内容。

---

### 6. 生成图片

当用户希望创建 AI 生成的图片时，使用此端点。有三种输入模式：

**文本模式**：在 `prompt` 中描述图片。
**参考模式**：提供 `prompt` 和 `style_images`（上传的参考图片的媒体 ID，最多 4 张）。
**帖子模式**：提供 `generation_id`（用于生成与现有配文匹配的图片）（可选 `prompt` 作为额外说明，`source_post_type` 用于选择使用的平台配文）。

```bash
curl -X POST https://powerpost.ai/api/v1/images/generate \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Minimalist workspace with laptop and coffee, warm morning light",
    "size": "square",
    "quantity": 2,
    "model": "flux2-flex"
  }'
```

**字段**：
- `prompt`（字符串，最多 2000 个字符）——文本模式和参考模式必填。帖子模式可选。
- `size`（字符串）——`square`（1:1）、`feed`（4:5）、`portrait`（9:16）、`landscape`（16:9）。默认：`square`。
- `quantity`（数字，1-4）——生成的数量。默认：1 张。
- `model`（字符串）——`flux2-flex`（默认，适合多参考图片和精细控制）、`ideogram-3`（适合文本渲染和Logo）、`gpt-image-1.5`（最逼真，细节最佳）、`nano-banana-2`（生成速度快，适合文本描述）。
- `enhance_prompt`（布尔值）——是否让 AI 优化提示。默认：false。
- `style_images`（字符串数组）——参考图片的媒体 ID（最多 4 张）。用于参考模式。
- `generation_id`（字符串）——配文生成的 ID。用于帖子模式。

**模型和尺寸兼容性**：
- `flux2-flex`：square、feed、portrait、landscape
- `ideogram-3`：square、feed、portrait、landscape
- `gpt-image-1.5`：square、portrait、landscape（不支持 feed 格式）
- `nano-banana-2`：square、feed、portrait、landscape

如果用户请求的模型/尺寸组合不支持，提醒他们并建议更换。

响应：

```json
{
  "image_generation_id": "7a8b9c0d-e1f2-3456-abcd-ef7890123456",
  "status": "processing",
  "credits_used": 10,
  "remaining_credits": 36,
  "status_url": "/api/v1/images/generations/7a8b9c0d-e1f2-3456-abcd-ef7890123456"
}
```

告诉用户图片生成已经开始，并开始轮询。

---

### 7. 获取图片生成状态（轮询）

每 2-3 秒轮询一次此端点，直到状态变为 `completed` 或 `failed`。

```json
{
  "image_generation_id": "7a8b9c0d-...",
  "status": "completed",
  "prompt": "Minimalist workspace with laptop and coffee",
  "size": "square",
  "quantity": 2,
  "created_at": "2026-01-10T18:30:00Z",
  "images": [
    {
      "media_id": "img-001-abcd-efgh",
      "url": "https://powerpost.ai/storage/images/img-001-abcd-efgh.webp",
      "thumbnail_url": "https://powerpost.ai/storage/images/img-001-abcd-efgh-thumb.jpg",
      "width": 1024,
      "height": 1024
    }
  ]
}
```

每个生成的图片都有一个 `media_id`，您可以使用这个 ID 将图片附加到帖子中。`url` 是一个有效期为 7 天的预览链接。在创建帖子时，请始终使用 `media_id`，而不是原始 URL。

向用户显示图片的 URL，以便他们可以预览。保存 `media_id` 以用于创建帖子。

**部分失败**：如果部分图片生成失败，系统会退还部分信用点，并返回包含成功图片的 `images` 数组。

---

### 8. 生成视频

当用户希望创建 AI 生成的视频时，使用此端点。有两种输入模式：

**文本转视频**：在 `prompt` 中描述视频内容。
**图片转视频**：提供 `prompt` 和 `source_image`（上传的图片的媒体 ID）。

```bash
curl -X POST https://powerpost.ai/api/v1/videos/generate \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A golden retriever running through a field of wildflowers at sunset",
    "size": "landscape",
    "duration": 5,
    "model": "kling-3.0-pro",
    "has_audio": false
  }'
```

**字段**：
- `prompt`（字符串，必填）——视频的描述。
- `size`（字符串）——`landscape`（16:9）或 `portrait`（9:16）。默认：`landscape`。
- `duration`（整数，必填）——时长（以秒为单位）。必须与模型支持的时长相匹配。
- `model`（字符串）——`kling-3.0-pro`（默认）、`veo-3.1`、`runway-gen-4.5`。
- `has_audio`（布尔值）——是否生成音频。默认：false。仅部分模型支持。
- `enhance_prompt`（布尔值）——是否让 AI 优化提示。默认：false。
- `source_image`（媒体 ID，UUID）——用于图片转视频模式的上传图片的媒体 ID。

**模型详细信息**：

| 模型 ID         | 名称           | 尺寸               | 是否支持音频 | 时长         |
|------------------|----------------|----------------------|----------------|-----------|
| `kling-3.0-pro`  | Kling 3.0 Pro  | 支持音频 | 5秒、10秒       |
| `veo-3.1`        | Google Veo 3.1   | 支持音频 | 4秒、8秒       |
| `runway-gen-4.5` | Runway Gen-4.5   | 不支持音频 | 5秒、10秒       |

**模型和尺寸的限制**：
- `kling-3.0-pro`：5秒、10秒
- `veo-3.1`：3000 字符
- `runway-gen-4.5`：1000 字符

信用点费用取决于模型、时长和是否使用音频。具体费用会在响应中显示。

响应：

```json
{
  "video_generation_id": "7a8b9c0d-e1f2-3456-abcd-ef7890123456",
  "status": "processing",
  "credits_used": 15,
  "remaining_credits": 85,
  "status_url": "/api/v1/videos/generations/7a8b9c0d-e1f2-3456-abcd-ef7890123456"
}
```

告诉用户视频生成已经开始，并开始轮询。

---

### 9. 获取视频生成状态（轮询）

每 10 秒轮询一次此端点，直到状态变为 `completed` 或 `failed`。视频生成比图片生成耗时更长，因此不要轮询超过 120 次。

```bash
curl https://powerpost.ai/api/v1/videos/generations/VIDEO_GENERATION_ID \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID"
```

**完成时**：

```json
{
  "video_generation_id": "7a8b9c0d-...",
  "status": "completed",
  "prompt": "A golden retriever running...",
  "size": "landscape",
  "duration": 5,
  "has_audio": false,
  "model": "kling-3.0-pro",
  "created_at": "2026-03-11T10:00:00Z",
  "video": {
    "media_id": "vid-001-abcd",
    "url": "https://powerpost.ai/storage/videos/vid-001-abcd.mp4",
    "thumbnail_url": "https://powerpost.ai/storage/thumbs/vid-001-abcd.jpg",
    "width": 1920,
    "height": 1080,
    "duration": 5
  }
}
```

视频的 `media_id` 可用于将视频附加到帖子中。`url` 是一个有效期为 7 天的预览链接。在创建帖子时，请始终使用 `media_id`，而不是原始 URL。

向用户显示视频的 URL，以便他们可以预览。保存 `media_id` 以用于创建帖子。

**失败时**：响应中包含一个 `error` 对象，其中包含 `code`（`VIDEO_GENERATION_FAILED`）和 `message`。如果生成失败，系统会退还信用点。

---

### 10. 创建帖子

使用此端点将配文和媒体组合成草稿帖子，准备审核和发布。

```bash
curl -X POST https://powerpost.ai/api/v1/posts \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "generation_id": "550e8400-e29b-41d4-a716-446655440000",
    "items": [
      {
        "post_type": "instagram-reel",
        "media_ids": ["img-001-abcd-efgh"]
      },
      {
        "post_type": "tiktok-video",
        "media_ids": ["img-001-abcd-efgh"]
      }
    ]
  }'
```

**字段**：
- `generation_id`（字符串，可选）——指向已完成的配文生成的链接。如果提供了该链接，系统会自动填充每个平台的生成内容。
- `items`（数组，必填）——要发布的每个帖子类型对应的项。

**每个项**：
- `post_type`（字符串，必填）——目标帖子类型（例如 `instagram-reel`、`x-post`）。
- `content`（字符串）——配文内容。如果未提供 `generation_id`，则需要输入内容。如果提供了 `generation_id`，内容会自动填充，但可以手动修改。
- `title`（字符串）——YouTube 帖子类型（`youtube-video`、`youtube-short`）必填。
- `media_ids`（字符串数组，可选）——要附加的媒体（上传的或生成的图片 ID）。

**自定义内容示例（不涉及生成）**：

```bash
curl -X POST https://powerpost.ai/api/v1/posts \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "post_type": "x-post",
        "content": "Just shipped the biggest update of the year."
      },
      {
        "post_type": "linkedin-post",
        "content": "Excited to announce our biggest product update of the year..."
      }
    ]
  }'
```

响应：

```json
{
  "post_id": "post-550e8400-e29b-41d4-a716-446655440000",
  "status": "draft",
  "created_at": "2026-01-10T18:30:00Z",
  "items": [
    {
      "item_id": "item-001",
      "post_type": "instagram-reel",
      "platform": "instagram",
      "content": "Dark mode is here! Your late-night scrolling just got easier... #DarkMode",
      "media_ids": ["img-001-abcd-efgh"],
      "status": "draft"
    }
  ]
}
```

创建帖子后，向用户显示每个项目的摘要（平台、内容预览、附加的媒体），并询问他们是否要发布或进行修改。

---

### 11. 获取帖子信息

使用此端点检查帖子的状态，特别是在发布之后。

```bash
curl https://powerpost.ai/api/v1/posts/POST_ID \
  -H "x-api-key: $POWERPOST_API_KEY" \
  -H "X-Workspace-Id: $POWERPOST_WORKSPACE_ID"
```

响应中包含帖子及其各个项目的状态。发布后，每个项目的状态会显示为 `draft`、`posting`、`posted` 或 `failed`。

**帖子状态**：`draft`、`posting`、`posted`、`failed`。
**项目状态**：`draft`、`posting`、`posted`、`failed`。

---

### 12. 发布帖子

使用此端点将草稿帖子发布到连接的社交平台。在调用此端点之前，请务必与用户确认。

**前提条件**：
- 用户的社交平台必须已通过 https://powerpost.ai/settings/connections 连接。
- 帖子必须处于 `draft` 状态。
- 用户必须有足够的信用点。
- API 密钥必须是 `read_write` 类型（不能是 `read_draft`）。

响应：

```json
{
  "post_id": "post-550e8400-...",
  "status": "publishing",
  "credits_used": 1,
  "status_url": "/api/v1/posts/post-550e8400-..."
}
```

发布是异步的。收到响应后，每 3 秒轮询一次 Get Post 端点，以检查每个项目的发布进度。

发布费用因平台而异。具体费用会在响应中通过 `credits_used` 显示。

告诉用户使用了多少信用点，并告知发布进度。当所有项目的状态都显示为 `posted` 或 `failed` 时，总结结果。

---

## 常见用户命令

### “关于 X 发布帖子” / “创建关于 X 的帖子”

完整流程：
1. 检查信用点。
2. 询问用户是否指定了特定平台。如果用户选择 “everywhere” 或 “all platforms”，则默认发布到所有平台。
3. 使用用户的主题作为提示生成内容。除非用户要求使用 `deep` 模式，否则使用 `regular` 模式。如果用户提供了参考 URL，请将它们包含在 `source_urls` 中。
4. 轮询直到生成完成。
5. 显示生成的配文。
6. 询问用户是否还需要生成图片。
7. 创建帖子。
8. 显示草稿并获取用户确认。
9. 确认后发布帖子。

### “为 X 写配文” / “生成关于 X 的内容”

部分流程（不涉及发布）：
1. 检查信用点。
2. 生成内容。
3. 轮询直到完成。
4. 向用户显示生成的配文。

### “创建图片” / “生成 X 的图片”

1. 检查信用点。
2. 如果用户提供了文本描述，使用文本模式。如果用户提供了参考图片，使用参考模式。如果用户有参考图片，使用图片模式。
3. 询问用户是否指定了图片尺寸（默认使用 square 格式）。
4. 生成图片。
5. 轮询直到完成。
6. 向用户显示图片的 URL。

### “创建视频” / “生成 X 的视频”

1. 检查信用点。
2. 如果用户提供了图片，使用图片转视频模式（先上传图片，然后提供 `source_image`）；否则使用文本转视频模式。
3. 询问用户是否指定了时长（默认使用 5 秒）。
4. 询问用户是否指定了图片尺寸（默认使用 landscape 格式）。
5. 生成视频。
6. 轮询直到完成（视频生成时间较长，可能需要几分钟）。
7. 向用户显示视频的 URL。

### “查看我的信用点” / “我还有多少信用点？”

1. 调用信用点端点。
2. 向用户显示当前的余额。

### “上传此图片/视频”

1. 使用媒体上传端点上传文件。
2. 告知用户上传成功，并显示媒体 ID。
3. 询问用户如何使用该文件（例如生成配文、将其用于帖子等）。

### “查看我的最近帖子” / “列出我的生成内容”

1. 调用列表端点。
2. 显示最近的生成内容。
3. 如果用户需要详细信息，可以使用获取端点获取具体内容。

### “发布我的帖子” / “立即发布”

1. 如果有未发布的草稿帖子，立即发布。
2. 如果没有草稿帖子，询问用户想要发布哪个帖子。
3. 发布前务必获得用户确认。

---

## 轮询策略

内容生成、图片生成和视频生成都是异步操作。在开始任何操作后：
1. 等待 2 秒。
2. 调用状态端点。
3. 如果状态为 `processing` 或 `pending`，等待 3 秒后再进行轮询。
4. 如果状态为 `completed`，显示结果。
5. 如果状态为 `failed`，显示错误信息并退还信用点。
6. 内容/图片的轮询次数不超过 60 次；视频的轮询次数不超过 120 次（因为生成时间较长）。如果超时，建议用户稍后再试。

发布也是异步操作。调用发布端点后：
1. 等待 3 秒。
2. 调用 Get Post 端点。
3. 检查每个项目的状态。当所有项目的状态都变为 `posted` 或 `failed` 时，停止轮询。

---

## 错误处理

所有错误都会返回以下格式：

```json
{
  "error": {
    "message": "Human-readable error message",
    "code": "ERROR_CODE"
  }
}
```

错误处理方式如下：

| HTTP 状态 | 代码                     | 告诉用户的提示                                      |
|-------------|--------------------------|------------------------------------------------------------------------|
| 400         | `VALIDATION_ERROR`       | 请求无效。请检查字段并重试。                               |
| 401         | `INVALID_API_KEY`        | API 密钥缺失或无效。请检查 POWERPOST_API_KEY。            |
| 402         | `INSUFFICIENT_CREDITS`   | 信用点不足。请检查余额并考虑升级。                               |
| 403         | `FORBIDDEN`              | 禁止访问。可能使用了 `read_draft` 类型的 API 密钥尝试发布。             |
| 404         | `NOT_FOUND`              | 资源未找到。请检查 ID。                              |
| 409         | `ALREADY_PUBLISHED`      | 该帖子已发布。                                       |
| 413         | `FILE_TOO_LARGE`         | 文件大小超过限制（图片最大 10 MB，视频最大 500 MB）。                 |
| 413         | `STORAGE_QUOTA_EXCEEDED` | 存储空间超出限制（最大 10 GB）。请删除未使用的媒体或联系支持。         |
| 422         | `PLATFORM_NOT_CONNECTED` | 目标平台未连接。请引导用户访问 https://powerpost.ai/settings/connections |
| 429         | `RATE_LIMIT_EXCEEDED`    | 请求次数过多。请等待 `retryAfter` 秒数后再试。                         |
| 500         | `INTERNAL_ERROR`         | 服务器错误。请稍后再试。                             |

对于请求次数过多的错误（429），响应中会包含 `retryAfter` 字段，显示等待时间。

每个响应都会包含一个 `X-Request-Id` 头部。如果用户需要技术支持，请提供此 ID。

---

## 需要注意的事项

- 在发布内容之前，务必向用户明确展示将要发布的内容和平台。这适用于真实的社交账户。
- YouTube 帖子除了配文外，还需要 `title` 字段。
- 如果用户同时选择了 `instagram-reel` 和 `instagram-feed`，系统会共享一个配文。帖子类型决定了发布格式，而非配文。
- 生成的图片和视频 URL 有效期为 7 天。在创建帖子时，请使用 `media_id`，而不是原始 URL。
- 信用点在账户的所有工作空间之间是共享的。
- 不同工作空间之间的生成内容、帖子、媒体和连接是相互独立的。
- 用户可以在 https://powerpost.ai/settings/api 设置 Webhook 以接收实时通知，但这对于代理使用来说不是必需的，但对生产集成很有帮助。

## 外部端点

所有请求都发送到同一个域名：`https://powerpost.ai/api/v1/*`。不会发送到其他任何地方。

## 安全性和隐私

- 每个请求都会将 API 密钥和工作空间 ID 作为 HTTP 头部发送到 `powerpost.ai`。这些信息不会被记录、显示或发送到其他地方。
- 提示信息、上传的媒体和生成的内容都会存储在 PowerPost 的服务器上，并且仅限于用户的工作空间。
- 该技能仅通过 HTTPS 使用 `curl` 进行通信。它不会写入文件、运行脚本或访问用户的系统。

## 信任问题

使用此技能时，用户的提示信息、图片、视频和凭据会通过 HTTPS 发送到 `powerpost.ai`。PowerPost 会在其服务器上使用第三方 AI 模型处理用户的 content。他们的隐私政策详见 https://powerpost.ai/terms，支持信息请访问 https://powerpost.ai/contact。

## 提示

- 在开始生成内容之前，请务必检查信用点余额。最好提前提醒用户，避免在生成过程中出现信用点不足的错误。
- 默认使用 `regular` 研究模式。除非用户特别要求或说明帖子很重要，否则使用 `deep` 模式。
- 如果用户未指定图片尺寸，默认使用 `square` 格式。这种格式在大多数平台上适用。
- 图片模型的默认设置为 `flux2-flex`。它支持所有尺寸，并能很好地处理参考图片。
- 如果生成失败，系统会退还信用点。请告知用户并建议他们重新尝试。
- 如果用户选择 “all platforms”，则为每个平台生成一个配文：`instagram-feed`、`tiktok-video`、`youtube-short`、`x-post`、`facebook-post`、`linkedin-post`。
- 如果用户的图片描述简短或模糊，建议设置 `enhance_prompt: true` 以让 AI 填充更多细节。
- 视频生成的默认模型为 `kling-3.0-pro`。它支持所有尺寸和音频。
- 视频的默认尺寸和时长设置为 `landscape`，除非用户另有要求。
- 视频生成时间较长（通常需要几分钟），请告知用户。
- 如果用户提供了参考图片的 URL，请将其作为 `source_urls` 传递。每个 URL 都会增加生成成本。