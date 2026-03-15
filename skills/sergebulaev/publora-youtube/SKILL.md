---
name: publora-youtube
description: 使用 Publora API 将视频内容上传并发布到 YouTube。当用户希望通过 Publora 上传或安排 YouTube 视频时，可以使用此技能。
---
# Publora — YouTube

这是一个用于 Publora API 的 YouTube 相关功能。关于身份验证、核心调度、媒体上传以及工作区/Webhook 的详细信息，请参阅 `publora` 核心功能文档。

**基础 URL:** `https://api.publora.com/api/v1`  
**请求头:** `x-publora-key: sk_YOUR_KEY`  
**平台 ID 格式:** `youtube-{channelId}`

## 平台限制（API）

| 属性 | 限制 | 备注 |
|----------|-------|-------|
| 标题 | **100 个字符** | — |
| 描述 | **5,000 个字符** | 只显示前 150 个字符 |
| 视频时长 | **12 小时** | — |
| 视频大小 | 最大 256 GB | — |
| 视频格式 | MP4、MOV、AVI、WebM | — |
| 图片 | 不支持 | 只支持视频 |
| 仅文本 | 不支持 | 必须包含视频 |
| 隐私设置 | 公开 / 非公开 / 私人 | 默认为公开 |

## 上传 YouTube 视频

YouTube 支持视频上传，并允许设置隐私选项和元数据：

```javascript
// Step 1: Create post with YouTube-specific platform settings
const post = await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Your video description here. Full details about what this video covers.',
    platforms: ['youtube-UC_CHANNEL_ID'],
    scheduledTime: '2026-03-20T15:00:00.000Z'
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

# Step 1: Create post (content = video description)
post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'Complete guide to building REST APIs in 2026. We cover authentication, rate limiting, and best practices.',
    'platforms': ['youtube-UC_CHANNEL_ID'],
    'scheduledTime': '2026-03-20T15:00:00.000Z'
}).json()

# Step 2: Get upload URL
upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
    'postGroupId': post['postGroupId'],
    'fileName': 'tutorial.mp4',
    'contentType': 'video/mp4',
    'type': 'video'
}).json()

# Step 3: Upload
with open('tutorial.mp4', 'rb') as f:
    requests.put(upload['uploadUrl'], headers={'Content-Type': 'video/mp4'}, data=f)

print(f"Scheduled: {post['postGroupId']}")
```

## 平台特性：

- **仅支持视频**：YouTube 不支持图片或纯文本的帖子。
- `content` 字段对应 YouTube 视频的描述信息。
- **标题**：通过平台设置进行设置（如果未设置，则使用描述的第一行作为标题）。
- **隐私设置**：默认为公开，可通过平台设置更改为非公开或私人。
- **YouTube Shorts**：时长小于 60 秒、采用竖屏格式（9:16）的视频会自动被识别为 Shorts。
- **文件大小限制**：最大 256 GB — YouTube 在文件大小方面支持度最高。
- **处理时间**：YouTube 会在视频发布前对其进行处理；在调度计划中需要考虑到这一点。