---
name: publora-tiktok
description: 使用 Publora API 在 TikTok 上发布或安排视频内容的发布。当用户希望通过 Publora 在 TikTok 上发布或安排视频的发布时，可以使用此技能。
---
# Publora — TikTok

这是一个用于 Publora API 的 TikTok 相关功能。关于授权、核心调度、媒体上传以及工作区/Webhook 的详细信息，请参阅 `publora` 核心技能文档。

**基础 URL:** `https://api.publora.com/api/v1`  
**请求头:** `x-publora-key: sk_YOUR_KEY`  
**平台 ID 格式:** `tiktok-{userId}`

## 平台限制（API）

> ⚠️ TikTok API 对字幕和视频时长有更严格的要求，相比原生应用程序。

| 属性          | API 限制        | 原生应用程序     |
|------------------|--------------|-------------|
| 字幕            | **2,200 个字符**     | 4,000 个字符     |
| 视频时长        | **10 分钟**       | 60 分钟       |
| 视频大小        | 4 GB          | —            |
| 视频格式        | MP4, MOV, WebM      | —            |
| 图片            | ❌ 仅支持视频     | —            |
| 仅文本          | ❌ 必须使用视频     | —            |
| 每日发布数量      | 15–20 条       | —            |
| 请求速率限制      | 每分钟 2 个视频     | —            |

**常见错误：**
- `spam_risk_too_many_posts` — 达到每日发布限制，需等待 24 小时
- `duration_check_failed` — 视频时长必须在 3 秒到 10 分钟之间
- `unaudited_client_can_only_post_to_private_accounts` — 该应用程序尚未通过 TikTok 的审核

> ⚠️ 如果您的 TikTok 应用程序未通过 TikTok 的审核，所有发布的视频将默认设置为 **私密**。

## 上传 TikTok 视频

TikTok 支持视频上传。请按照以下三步流程进行操作：

```javascript
// Step 1: Create post (draft without scheduledTime, or scheduled)
const post = await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Your TikTok caption here #trending',
    platforms: ['tiktok-123456789'],
    scheduledTime: '2026-03-20T18:00:00.000Z'
  })
}).then(r => r.json());

// Step 2: Get upload URL
const upload = await fetch('https://api.publora.com/api/v1/get-upload-url', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    postGroupId: post.postGroupId,
    fileName: 'video.mp4',
    contentType: 'video/mp4',
    type: 'video'
  })
}).then(r => r.json());

// Step 3: Upload video to S3
await fetch(upload.uploadUrl, {
  method: 'PUT',
  headers: { 'Content-Type': 'video/mp4' },
  body: videoFileBytes
});
```

## Python 示例

```python
import requests

HEADERS = { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' }

# Step 1: Create post
post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'Your TikTok caption #viral',
    'platforms': ['tiktok-123456789'],
    'scheduledTime': '2026-03-20T18:00:00.000Z'
}).json()

# Step 2: Get upload URL
upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
    'postGroupId': post['postGroupId'],
    'fileName': 'video.mp4',
    'contentType': 'video/mp4',
    'type': 'video'
}).json()

# Step 3: Upload
with open('video.mp4', 'rb') as f:
    requests.put(upload['uploadUrl'], headers={'Content-Type': 'video/mp4'}, data=f)
```

## 平台特性：

- **仅支持视频** — TikTok 不支持通过 API 发布图片或纯文本内容
- **最低时长要求**：3 秒；API 最大支持时长为 10 分钟
- **未通过审核的应用程序发布的视频将设置为私密** — 如果 Publora 的 TikTok 应用程序未通过 TikTok 的审核，视频将默认设置为私密状态
- **API 对字幕长度的限制**：最多 2,200 个字符（而非原生应用程序的 4,000 个字符）——请确保字幕简洁明了
- **每日发布数量限制**：TikTok 规定每天最多可发布 15–20 条视频