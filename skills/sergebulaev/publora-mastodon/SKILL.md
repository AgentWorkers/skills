---
name: publora-mastodon
description: 使用 Publora API 在 Mastodon 上发布或安排内容。当用户希望通过 Publora 在 Mastodon 上发布或安排帖子时，可以使用此技能。
---
# Publora — Mastodon

这是一个用于与Mastodon/Fediverse平台交互的Publora API技能。关于认证、核心调度、媒体上传以及工作空间/Webhook的详细信息，请参阅`publora`核心技能文档。

**基础URL:** `https://api.publora.com/api/v1`  
**请求头:** `x-publora-key: sk_YOUR_KEY`  
**平台ID格式:** `mastodon-{accountId}`

> **注意:** Publora目前仅支持`mastodon.social`实例，其他实例暂不支持。

## 平台限制（API）

| 属性          | 限制        | 备注        |
|---------------|-----------|------------|
| 文本（Toot）      | **500个字符**   | 可由实例配置；部分实例支持超过5000个字符 |
| 图片           | 最大4张，每张16MB   | 支持JPEG、PNG、GIF、WebP格式 |
| 视频           | 最大约99MB     | 支持MP4、MOV、WebM格式；无时长限制，仅受文件大小限制 |
| 仅文本         | ✅          | 可以         |
| 请求频率限制     | 每30分钟30次媒体上传 | 每个账户每5分钟300次请求 |

## 发布一条Toot（纯文本）

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Hello Fediverse! Building open, decentralized tools for everyone. #fediverse #opensource',
    platforms: ['mastodon-123456789']
  })
});
```

## 安排发布时间

```javascript
body: JSON.stringify({
  content: 'Your Mastodon post here',
  platforms: ['mastodon-123456789'],
  scheduledTime: '2026-03-20T10:00:00.000Z'
})
```

## 带图片发布

```python
import requests

HEADERS = { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' }

# Step 1: Create post
post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'Here is a photo from our event 📷 #community',
    'platforms': ['mastodon-123456789']
}).json()

# Step 2: Get upload URL (up to 16 MB, JPEG/PNG/GIF/WebP)
upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
    'postGroupId': post['postGroupId'],
    'fileName': 'photo.jpg',
    'contentType': 'image/jpeg',
    'type': 'image'
}).json()

# Step 3: Upload
with open('photo.jpg', 'rb') as f:
    requests.put(upload['uploadUrl'], headers={'Content-Type': 'image/jpeg'}, data=f)
```

## 平台特性

- **仅支持mastodon.social实例**：Publora目前仅支持该实例。
- **图片上传限制宽松**：每张图片最大16MB，远高于大多数平台。
- **视频文件大小限制**：默认为约99MB；无明确时长限制。
- **支持WebP格式**：与Instagram不同，Mastodon原生支持WebP格式。
- **内容共享**：发布的帖子会自动同步到整个Fediverse网络。
- **标签（Hashtags）**：在Mastodon上提高帖子的可见性非常重要，请在帖子中使用标签。
- **内容警告**：Publora API目前不直接支持内容警告功能；如有需要，请使用文本格式进行提示。