---
name: publora-threads
description: 使用 Publora API 在 Threads 中发布或安排内容。当用户希望通过 Publora 发布或安排 Threads 的帖子时，可以使用此技能。
---
# Publora — Threads

您可以通过 Publora API 发布和安排 Threads 内容。

> **先决条件：** 需要安装 `publora` 核心技能，以完成身份验证设置并获取平台 ID。

## 获取您的 Threads 平台 ID

```bash
GET https://api.publora.com/api/v1/platform-connections
# Look for entries like "threads-789"
```

## 立即发布 Threads 内容

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Good morning Threads 👋 What are you building today?',
    platforms: ['threads-789']
  })
});
```

## 安排 Threads 内容的发布时间

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Reminder: ship it, then make it perfect. Done beats perfect.',
    platforms: ['threads-789'],
    scheduledTime: '2026-03-16T11:00:00.000Z'
  })
});
```

## Threads 与图片的结合使用

```python
import requests

HEADERS = { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' }

post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'Behind the scenes 👇',
    'platforms': ['threads-789'],
    'scheduledTime': '2026-03-16T11:00:00.000Z'
}).json()

upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
    'fileName': 'behind-scenes.jpg', 'contentType': 'image/jpeg',
    'type': 'image', 'postGroupId': post['postGroupId']
}).json()

with open('behind-scenes.jpg', 'rb') as f:
    requests.put(upload['uploadUrl'], headers={'Content-Type': 'image/jpeg'}, data=f)
```

## Threads 使用技巧：

- **采用对话式的语气**：这种方式更受欢迎，因为 Threads 更看重内容的真实性而非表面的精致度。
- **每条帖子的字符限制为 500 个。
- **最佳发布时间**：早上（7–9 点）和晚上（7–9 点）。
- **不要使用标签**：Threads 并不通过标签来展示内容。
- **在 Instagram 上进行转发**：以便在 Meta 平台上获得更广泛的传播。