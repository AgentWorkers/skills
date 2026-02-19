---
name: postqued-api
description: PostQued 社交媒体调度 API 集成：在通过 API 调用 PostQued 时使用，用于内容上传、发布到 TikTok（及其他平台）、管理平台账户或查询发布状态。该集成会在涉及社交媒体发布、内容调度、TikTok 草稿发布或任何 PostQued API 操作的任务触发。
---
# PostQued API 技能

## 设置

将您的 PostQued API 密钥添加到工作区的 `.env` 文件中：

```
POSTQUED_API_KEY=pq_your_api_key_here
```

API 密钥可以在 PostQued 的控制台（https://postqued.com/console）中创建，密钥以 `pq_` 为前缀。

## 认证

所有 API 请求都需要通过 Bearer Token 进行认证：

```
Authorization: Bearer $POSTQUED_API_KEY
```

## 基本 URL

```
https://api.postqued.com
```

## API 文档

OpenAPI 规范：https://api.postqued.com/v1/docs/openapi.json

## 核心工作流程：上传和发布内容

### 第 1 步：上传内容

**对于视频**（使用预签名的 URL 上传）：

```bash
# Start upload session
curl -X POST https://api.postqued.com/v1/content/upload \
  -H "Authorization: Bearer $POSTQUED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "video.mp4",
    "contentType": "video/mp4",
    "fileSize": 52428800
  }'
# Response: { "contentId": "uuid", "upload": { "url": "presigned-url", "method": "PUT", "headers": {...} } }

# Upload file to presigned URL
curl -X PUT "PRESIGNED_URL" \
  -H "Content-Type: video/mp4" \
  --data-binary @video.mp4

# Confirm upload
curl -X POST https://api.postqued.com/v1/content/upload/complete \
  -H "Authorization: Bearer $POSTQUED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contentId": "uuid-from-step-1",
    "key": "content/user-id/content-id.mp4",
    "filename": "video.mp4",
    "contentType": "video/mp4",
    "size": 52428800,
    "width": 1920,
    "height": 1080,
    "durationMs": 30000
  }'
```

**对于图片**（直接上传）：

```bash
curl -X POST https://api.postqued.com/v1/content/upload-image \
  -H "Authorization: Bearer $POSTQUED_API_KEY" \
  -F "file=@image.jpg"
```

### 第 2 步：获取平台账户 ID

```bash
curl https://api.postqued.com/v1/platform-accounts?platform=tiktok \
  -H "Authorization: Bearer $POSTQUED_API_KEY"
# Response: { "accounts": [{ "id": "account-uuid", "username": "@user", ... }] }
```

### 第 3 步：发布内容

**重要提示：** 必须在请求头中包含一个唯一的 `Idempotency-Key`（有效期为 24 小时）。

```bash
curl -X POST https://api.postqued.com/v1/content/publish \
  -H "Authorization: Bearer $POSTQUED_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: unique-uuid-per-request" \
  -d '{
    "contentId": "content-uuid",
    "targets": [{
      "platform": "tiktok",
      "accountId": "account-uuid",
      "intent": "draft",
      "caption": "Check this out! #fyp",
      "dispatchAt": null,
      "options": {
        "privacyLevel": "SELF_ONLY",
        "disableDuet": false,
        "disableStitch": false,
        "disableComment": false
      }
    }]
  }'
# Response: { "publishId": "uuid", "status": "pending", "targets": [...] }
```

### 第 4 步：检查发布状态

```bash
curl https://api.postqued.com/v1/content/publish/PUBLISH_ID \
  -H "Authorization: Bearer $POSTQUED_API_KEY"
```

## API 参考

请参阅 [references/api.md](references/api.md) 以获取完整的端点文档。

## TikTok 特定选项

| 选项                | 类型    | 描述                                                                       |
| --------------------- | ------- | --------------------------------------------------------------------------------- |
| privacyLevel          | 字符串  | `PUBLIC_TO_EVERYONE`, `MUTUAL_follow FRIENDS`, `FOLLOWER_OF_CREATOR`, `SELF_ONLY` |
| disableDuet           | 布尔值 | 禁用双人模式                                                                      |
| disableStitch         | 布尔值 | 禁用拼接功能                                                                    |
| disableComment        | 布尔值 | 禁用评论功能                                                                  |
| videoCoverTimestampMs | 整数 | 视频封面帧的时间戳                                                    |
| autoAddMusic          | 布尔值 | 自动添加音乐（仅适用于图片）                                                           |
| brandContentToggle    | 布尔值 | 是否显示品牌合作伙伴关系信息                                                       |
| brandOrganicToggle    | 布尔值 | 是否显示推广内容                                                    |

## 操作类型

- `draft` - 作为草稿发送到 TikTok 收件箱（用户需手动发布）
- `publish` - 直接发布（当前被禁用，需要 API 批准）

## 状态代码

**发布请求：** `pending` | `processing` | `completed` | `partial_failed` | `failed` | `canceled`

**目标状态：** `queued` | `scheduled` | `processing` | `sent` | `published` | `failed` | `canceled`

## 安排时间

将 `dispatchAt` 设置为未来的 UTC ISO 时间戳：

```json
{
  "dispatchAt": "2026-02-20T15:00:00Z"
}
```

设置为 `null` 表示立即执行。

## 速率限制

| 操作    | 限制      |
| --------- | -------- |
| 上传      | 每分钟 20 次     |
| 阅读      | 每分钟 30 次     |
| 发布      | 每分钟 10 次     |
| 删除      | 每分钟 20 次     |

## 错误处理

错误返回信息：

```json
{
  "error": "Message",
  "code": "ERROR_CODE"
}
```

常见错误代码：`MISSING_IDEMPOTENCY_KEY`, `IDEMPOTENCY_CONFLICT`, `SUBSCRIPTION_REQUIRED`