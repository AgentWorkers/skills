---
name: publora-bluesky
description: 使用 Publora API 在 Bluesky 中发布或安排内容。当用户希望通过 Publora 在 Bluesky 中发布或安排帖子时，可以使用此技能。
---
# Publora — Bluesky

Bluesky 是一个基于 AT 协议的平台技能，用于与 Publora API 进行交互。关于身份验证、核心调度、媒体上传以及工作空间/Webhook 的详细信息，请参考 `publora` 核心技能文档。

**基础 URL:** `https://api.publora.com/api/v1`  
**请求头:** `x-publora-key: sk_YOUR_KEY`  
**平台 ID 格式:** `bluesky-{did}`  
其中 `{did}` 是您在连接时获得的 Bluesky 去中心化标识符（DID）。

## 使用要求

- 需要使用 **用户名 + 应用密码**（而非您的主密码）登录 Bluesky 账户  
- 生成应用密码：请前往 Bluesky 设置 → 应用密码  
- 通过 Publora 仪表板进行操作  

## 平台限制（API）

| 属性 | 限制 | 备注 |
|---------|------|------|
| 文本 | **300 个字符** | 链接不计入字符限制 |
| 图片 | 最多 4 张，每张大小不超过 1 MB | 支持 JPEG、PNG、WebP 格式（最大尺寸 2000×2000 像素） |
| 视频 | 最长 3 分钟，文件大小不超过 100 MB | 必须使用 MP4 格式；上传前需要完成邮件验证 |
| 短视频 | 最长 60 秒，文件大小不超过 50 MB | 视频大小会分为不同的等级 |
| 仅文本 | 可 | — |
| 每日视频上传限制 | 25 个视频，总大小不超过 10 GB | — |
| 请求速率限制 | 每 5 分钟内最多 3,000 次请求 | — |

**常见错误：**
- `429 Too Many Requests`：请求次数过多，请稍后重试 |
- 视频状态为 `JOB_STATE_FAILED`：请检查视频格式（MP4）和大小是否符合要求 |

## 发布文本帖子

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Building in public on Bluesky today! Links, hashtags, and mentions all auto-detected. #buildinpublic',
    platforms: ['bluesky-did:plc:abc123']
  })
});
```

Publora 会自动识别标签（#hashtags）、链接（URL）和 @提及（@mentions），并自动生成符合 AT 协议要求的元数据（facets）。

## 安排帖子发布时间

```javascript
body: JSON.stringify({
  content: 'Your Bluesky post here',
  platforms: ['bluesky-did:plc:abc123'],
  scheduledTime: '2026-03-20T11:00:00.000Z'
})
```

## 发布带图片的帖子

> ⚠️ Bluesky 对图片大小有严格限制，每张图片不得超过 1 MB。建议将图片压缩至 JPEG 质量 80–85%。

```python
import requests

HEADERS = { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' }

# Step 1: Create post
post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'Check out this photo! 📸',
    'platforms': ['bluesky-did:plc:abc123']
}).json()

# Step 2: Get upload URL (make sure image is <1 MB and JPEG/PNG/WebP)
upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
    'postGroupId': post['postGroupId'],
    'fileName': 'photo.jpg',
    'contentType': 'image/jpeg',
    'type': 'image'
}).json()

# Step 3: Upload
with open('photo_compressed.jpg', 'rb') as f:
    requests.put(upload['uploadUrl'], headers={'Content-Type': 'image/jpeg'}, data=f)
```

## 平台的特殊注意事项：

- **链接不计入字符限制**：非常适合包含链接的帖子 |
- **自动元数据生成**：Publora 会自动识别标签、@提及和链接，并生成相应的 Bluesky 元数据 |
- **图片大小限制**：每张图片的最大大小为 1 MB，上传前请务必压缩图片 |
- **图片尺寸**：最大 2000×2000 像素 |
- **需要应用密码**：切勿使用您的主 Bluesky 密码，应创建专门的应用密码 |
- **邮件验证**：上传视频前必须完成邮件验证（在 Bluesky 设置中完成一次性操作） |
- **平台 ID 格式**：平台 ID 会包含完整的 DID，例如 `bluesky-did:plc:abc123xyz`