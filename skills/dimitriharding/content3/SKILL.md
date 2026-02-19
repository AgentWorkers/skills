---
name: content3
version: 1.0.4
description: Content3 API 用于创建视频、管理内容、提交评论以及将内容发布到社交媒体。
homepage: https://content3.app/developers
metadata: {"clawdbot":{"emoji":"🎬"}}
---
# content3

使用 Content3 Agent API 可以创建短视频、管理内容库、提交内容以供人工审核，并起草社交媒体帖子。

## 设置

1. 登录到您的 Content3 仪表板。
2. 转到 **设置 → API 密钥**。
3. 点击 **创建 API 密钥** — 复制密钥（以 `c3ak_` 开头，仅显示一次）。
4. 将密钥存储起来：
```bash
mkdir -p ~/.config/content3
echo "c3ak_your_key_here" > ~/.config/content3/api_key
```

## API 基础知识

基础 URL：`https://api.content3.app/v1`

所有请求都需要：
```bash
C3_KEY=$(cat ~/.config/content3/api_key)
curl -X GET "https://api.content3.app/v1/..." \
  -H "Authorization: Bearer $C3_KEY" \
  -H "Content-Type: application/json"
```

> **注意：** Agent API 密钥具有控制访问范围的权限。默认权限包括：`content:read`、`social:generate`、`social:drafts:read`、`social:drafts:write`。如需更多权限，请请求用户授予。

## 认证

**验证您的密钥：**
```bash
curl "https://api.content3.app/v1/me" \
  -H "Authorization: Bearer $C3_KEY"
```

返回值：`{ "userId", "keyId", "keyName", "scopes": [...] }`

### 权限范围参考

| 权限范围 | 访问权限 |
|-------|--------|
| `content:read` | 读取内容项、渲染作业、管理社交媒体连接、设置短视频格式 |
| `content:write` | 创建/修改内容 |
| `reviews:read` | 读取评论 |
| `reviews:write` | 创建评论和反馈 |
| `social:generate` | 生成人工智能生成的社交媒体内容 |
| `social:drafts:read` | 读取社交媒体草稿 |
| `social:drafts:write` | 创建社交媒体草稿 |
| `products:read` | 读取产品信息 |
| `products:write` | 创建/修改产品信息 |
| `*` | 全部权限（所有权限范围） |

## 短视频生成

这是主要的代理工作流程——从各种来源生成短视频。

**获取可用选项（语音、来源、宽高比）：**
```bash
curl "https://api.content3.app/v1/agents/short-form/options" \
  -H "Authorization: Bearer $C3_KEY"
```

返回来源类型（`quora`、`reddit`、`prompt`、`text`）、语音选项（Kore、Puck、Charon、Fenrir、Zephyr、Aoede、Orus）以及宽高比（`9:16`、`16:9`）。

**根据提示生成视频：**
```bash
curl -X POST "https://api.content3.app/v1/agents/short-form/generate" \
  -H "Authorization: Bearer $C3_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "source": {
      "type": "prompt",
      "prompt": "Explain why cats always land on their feet"
    },
    "voiceId": "Kore",
    "aspectRatio": "9:16",
    "saveToLibrary": true
  }'
```

**根据 Reddit 帖子生成视频：**
```bash
curl -X POST "https://api.content3.app/v1/agents/short-form/generate" \
  -H "Authorization: Bearer $C3_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "source": {
      "type": "reddit",
      "url": "https://reddit.com/r/..."
    },
    "voiceId": "Puck",
    "aspectRatio": "9:16"
  }'
```

**根据 Quora 回答生成视频：**
```bash
curl -X POST "https://api.content3.app/v1/agents/short-form/generate" \
  -H "Authorization: Bearer $C3_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "source": {
      "type": "quora",
      "url": "https://quora.com/..."
    },
    "voiceId": "Zephyr"
  }'
```

**根据原始文本生成视频：**
```bash
curl -X POST "https://api.content3.app/v1/agents/short-form/generate" \
  -H "Authorization: Bearer $C3_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "source": {
      "type": "text",
      "text": "Your script or content here..."
    },
    "voiceId": "Fenrir",
    "aspectRatio": "16:9"
  }'
```

返回值：`{ "success": true, "jobId": "uuid", "status": "queued", "taskName": "..." }`

## 渲染作业

跟踪视频生成作业的状态。

**列出渲染作业：**
```bash
curl "https://api.content3.app/v1/render-jobs?status=completed&limit=10" \
  -H "Authorization: Bearer $C3_KEY"
```

查询参数：`status`（排队中、处理中、已完成、失败）、`agent_type`、`job_type`、`limit`（最多 100 个）、`offset`。

**获取特定作业：**
```bash
curl "https://api.content3.app/v1/render-jobs/{job_id}" \
  -H "Authorization: Bearer $C3_KEY"
```

返回完整的作业详情，包括 `payload`、`status`、`output_url`、时间戳。

## 内容项

管理您的内容库。

**列出内容项：**
```bash
curl "https://api.content3.app/v1/content-items?type=video&limit=20" \
  -H "Authorization: Bearer $C3_KEY"
```

查询参数：`type`、`limit`（最多 100 个，默认为 20 个）、`offset`。

返回值：`{ "items": [{ "id", "type", "title", "description", "source_url", "thumbnail_url", "created_at" }] }`

## 人工审核

在发布前，将内容提交给人工进行审核和批准。

**创建评论：**
```bash
curl -X POST "https://api.content3.app/v1/reviews" \
  -H "Authorization: Bearer $C3_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Weekly video batch - Feb 18",
    "description": "5 short-form videos for review before publishing",
    "contentType": "video",
    "attachments": [
      {"url": "https://r2.example.com/video1.mp4", "label": "Cat facts video"},
      {"url": "https://r2.example.com/video2.mp4", "label": "Tech tips video"}
    ],
    "metadata": {
      "tags": ["short-form", "batch"],
      "notes": "Generated from trending Reddit posts"
    }
  }'
```

内容类型：`pdf`、`video`、`image`、`slides`、`markdown`。

**列出评论：**
```bash
curl "https://api.content3.app/v1/reviews?status=pending&limit=10" \
  -H "Authorization: Bearer $C3_KEY"
```

状态值：`pending`（待审）、`approved`（已批准）、`rejected`（被拒绝）、`needs_revision`（需要修改）。

**获取带评论的评论：**
```bash
curl "https://api.content3.app/v1/reviews/{review_id}" \
  -H "Authorization: Bearer $C3_KEY"
```

**向评论添加评论：**
```bash
curl -X POST "https://api.content3.app/v1/reviews/{review_id}/comments" \
  -H "Authorization: Bearer $C3_KEY" \
  -H "Content-Type: application/json" \
  -d '{"body": "Revised the thumbnail based on feedback"}'
```

### 更新评论状态

**更新评论的状态：**
```bash
curl -X PATCH "https://api.content3.app/v1/reviews/{review_id}" \
  -H "Authorization: Bearer $C3_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "in_review"}'
```

有效状态转换：`pending` → `in_review`（待审核）、`in_review` → `approved`/`rejected`（已批准/被拒绝）/`changes_requested`（需要修改）、`changes_requested` → `in_review`（需要再次审核）。

返回值：`{ "review": { "id": "uuid", "status": "in_review", "updatedAt": "..." }`

### 评论修订

当需要修改时，提交更新后的附件。平台会记录所有版本。

**提交修订：**
```bash
curl -X POST "https://api.content3.app/v1/reviews/{review_id}/revisions" \
  -H "Authorization: Bearer $C3_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "attachments": [
      {"url": "https://r2.example.com/video1-v2.mp4", "label": "Fixed background color"}
    ],
    "note": "Fixed the background color as requested"
  }'
```

如果还没有修订版本，系统会自动使用当前附件创建第一个修订版本（标记为“Original”）。新的修订版本将成为最新版本，并更新 `reviews.attachments`。

**列出修订版本：**
```bash
curl "https://api.content3.app/v1/reviews/{review_id}/revisions" \
  -H "Authorization: Bearer $C3_KEY"
```

返回值：`{ "revisions": [{ "revisionNumber": 1, "attachments": [...], "note": "Original", "agentKeyName": "...", "createdAt": "..." }, ...] }`

### 可共享的评论链接

生成评论的公共分享链接，以便用户无需登录即可查看和评论。

**创建或获取分享链接：**
```bash
curl -X POST "https://api.content3.app/v1/reviews/{review_id}/share" \
  -H "Authorization: Bearer $C3_KEY"
```

返回值：`{ "shareToken": "...", "shareUrl": "https://content3.app/review/...", "shareEnabled": true }`

如果已经存在分享链接，此操作会返回现有链接并确保其处于启用状态。

**切换分享链接的启用/禁用状态：**
```bash
curl -X PATCH "https://api.content3.app/v1/reviews/{review_id}/share" \
  -H "Authorization: Bearer $C3_KEY" \
  -H "Content-Type: application/json" \
  -d '{"enabled": false}'
```

禁用时，访问分享链接的人会看到“未找到”页面。通过 `{"enabled": true}` 可以重新启用分享链接。

分享链接可以发送给任何人以获取即时反馈——无需 Content3 账户。公众审稿人可以查看内容、更改评论状态并留下评论。

### 将评论提升为正式内容

评论获得批准后，可以将其提升为正式内容项，以便用于社交媒体草稿。

**将已批准的评论提升为正式内容：**
```bash
curl -X POST "https://api.content3.app/v1/reviews/{review_id}/promote" \
  -H "Authorization: Bearer $C3_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Optional override title",
    "description": "Optional override description"
  }'
```

请求体是可选的——如果省略字段，则使用评论的标题/描述。

返回值：`{ "contentItem": { "id": "uuid", "type": "video", "title": "...", "sourceUrl": "...", "status": "ready", "reviewId": "uuid", "createdAt": "..." }`

首次提升时返回 `201`；如果已提升则返回 `200`（操作是幂等的）。如果评论尚未批准，则返回 `422`。需要以下权限：`reviews:read` + `content:write`。

## 社交媒体

创建草稿并生成人工智能生成的社交媒体内容。

**列出已连接的社交媒体账户：**
```bash
curl "https://api.content3.app/v1/social/connections" \
  -H "Authorization: Bearer $C3_KEY"
```

返回连接的账户类型：`youtube`、`tiktok`、`instagram`、`pinterest`、`threads`。

**为内容项生成人工智能生成的社交媒体内容：**
```bash
curl -X POST "https://api.content3.app/v1/social/generate-content" \
  -H "Authorization: Bearer $C3_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contentItemId": "content-item-uuid",
    "platforms": ["tiktok", "youtube"],
    "userPrompt": "Make it engaging and use trending hashtags"
  }'
```

**创建社交媒体草稿（格式 A — 标准格式）：**
```bash
curl -X POST "https://api.content3.app/v1/social/drafts" \
  -H "Authorization: Bearer $C3_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contentItemId": "content-item-uuid",
    "title": "Why cats always land on their feet",
    "description": "The science behind cat reflexes",
    "hashtags": ["cats", "science", "shorts"],
    "platforms": [
      {
        "connectionId": "connection-uuid",
        "platformTitle": "Cat Physics Explained",
        "platformDescription": "You won'\''t believe this! #cats #science"
      }
    ]
  }'
```

**创建社交媒体草稿（格式 B — 简化格式）：**
```bash
curl -X POST "https://api.content3.app/v1/social/drafts" \
  -H "Authorization: Bearer $C3_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contentItemId": "content-item-uuid",
    "title": "Why cats always land on their feet",
    "caption": "The science behind cat reflexes #cats #science",
    "hashtags": ["cats", "science", "shorts"],
    "platforms": ["tiktok", "youtube"],
    "connectionIds": ["connection-uuid-1", "connection-uuid-2"]
  }'
```

两种格式均被接受。如果未提供 `description`，`caption` 会自动使用 `description` 的内容。使用 `GET /v1/social/connections` 获取有效的连接 ID。

**列出草稿：**
```bash
curl "https://api.content3.app/v1/social/drafts?limit=20" \
  -H "Authorization: Bearer $C3_KEY"
```

**发布草稿：**
```bash
curl -X POST "https://api.content3.app/v1/social/drafts/{draft_id}/publish" \
  -H "Authorization: Bearer $C3_KEY"
```

将草稿排队发布到所有配置的平台上。只有状态为 `draft` 的草稿才能发布。如果帖子不是草稿或缺少内容/平台信息，返回 `422`。

返回值：`{ "postId": "uuid", "jobId": "uuid", "status": "pending" }`

通过 `GET /render-jobs/{jobId}` 可以查询发布进度。

## 产品

管理用于内容生成的产品。

**创建产品：**
```bash
curl -X POST "https://api.content3.app/v1/products" \
  -H "Authorization: Bearer $C3_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My SaaS Product",
    "description": "A tool that helps you do X",
    "url": "https://myproduct.com"
  }'
```

**列出产品：**
```bash
curl "https://api.content3.app/v1/products?limit=20" \
  -H "Authorization: Bearer $C3_KEY"
```

## 常见工作流程

### 生成和审核视频
1. 生成视频：`POST /agents/short-form/generate`
2. 查询作业状态：`GET /render-jobs/{jobId}` 直到状态变为 `completed`
3. 提交审核：`POST /reviews` 并附上已完成作业的视频 URL
4. 创建分享链接：`POST /reviews/{reviewId}/share` — 将分享链接发送给他人以获取反馈
5. 检查评论状态：`GET /reviews/{reviewId}` — 等待审核结果
6. 如果需要修改内容：修复内容并通过 `POST /reviews/{reviewId}/revisions` 提交修订版本，然后返回步骤 5
7. 将评论提升为正式内容：`POST /reviews/{reviewId}/promote` — 从已批准的评论创建正式内容项
8. 创建社交媒体草稿：`POST /social/drafts` 并使用步骤 7 中的 `contentItem.id`
9. 发布草稿：`POST /social/drafts/{draftId}/publish` — 将草稿排队发布

### 批量内容生成
1. 获取短视频生成选项：`GET /agents/short-form/options`
2. 使用不同的来源和语音生成多个视频
3. 监控所有作业：`GET /render-jobs?status=processing`
4. 提交批量评论（包含所有已完成的视频 URL）
5. 审批通过后，提升每个评论：`POST /reviews/{reviewId}/promote`
6. 为每个评论生成社交媒体内容并创建相应的草稿：`POST /social/drafts` 并使用步骤 5 中的 `contentItem.id`
7. 发布每个草稿：`POST /social/drafts/{draftId}/publish`

## 注意事项

- 创建渲染作业时返回的作业 ID 是 UUID。
- 视频生成是异步的——需要通过 `/render-jobs/{id}` 查询完成状态。
- 评论状态可以在仪表板或通过公共分享链接由人工设置。
- 代理可以通过 `POST /reviews/{id}/share` 生成分享链接，并将其发送给他人以获取即时反馈。
- 有速率限制——请避免频繁发送请求。
- 在生成视频时设置 `saveToLibrary` 标志会自动创建内容项。
- 短视频的默认宽高比为 `9:16`（竖屏）。
- 语音选择会影响生成视频的 TTS 旁白。