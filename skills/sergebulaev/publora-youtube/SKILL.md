---
name: publora-youtube
description: 使用 Publora API 将视频内容发布或安排到 YouTube 上。当用户希望通过 Publora 发布或安排 YouTube 视频时，可以使用此技能。
---
# Publora — YouTube

通过 Publora API 发布和安排 YouTube 视频内容。

> **先决条件：** 需要安装 `publora` 核心技能，以便进行身份验证设置和获取平台 ID。

## 获取您的 YouTube 平台 ID

```bash
GET https://api.publora.com/api/v1/platform-connections
# Look for entries like "youtube-012"
```

## 上传和安排 YouTube 视频

```python
import requests

HEADERS = { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' }

# Step 1: Create post
post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'How We Built a SaaS in 30 Days — Full Breakdown',
    'platforms': ['youtube-012'],
    'scheduledTime': '2026-03-16T16:00:00.000Z'
}).json()

# Step 2: Get upload URL
upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
    'fileName': 'saas-breakdown.mp4', 'contentType': 'video/mp4',
    'type': 'video', 'postGroupId': post['postGroupId']
}).json()

# Step 3: Upload video (max 512MB)
with open('saas-breakdown.mp4', 'rb') as f:
    requests.put(upload['uploadUrl'], headers={'Content-Type': 'video/mp4'}, data=f)

print(f"Video scheduled: {post['postGroupId']}")
```

## 发布 YouTube 短视频

流程与普通视频相同——只需确保视频为竖屏格式（9:16 比例）且时长不超过 60 秒：

```javascript
body: JSON.stringify({
  content: 'One tip that 10x\'d our productivity #shorts #productivity',
  platforms: ['youtube-012'],
  scheduledTime: '2026-03-16T12:00:00.000Z'
})
```

## YouTube 使用技巧：

- **内容字段**：填写视频标题/描述——请确保内容适合搜索引擎优化（SEO）。
- **视频是必需的**：没有视频的 YouTube 帖子将无法发布。
- **最大文件大小**：512 MB。
- **最佳上传时间**：每周四至周六下午 2 点至 4 点（根据目标观众的时区）。
- **短视频**：时长不超过 60 秒，且为竖屏 9:16 比例——YouTube 会自动识别并推广为短视频。
- **缩略图**：无法通过 API 设置——请在发布后在 YouTube Studio 中进行设置。
- **描述优化**：描述的前 2-3 句应包含关键词，以提升搜索排名。