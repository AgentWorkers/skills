---
name: publora-twitter
description: 使用 Publora API 在 X（Twitter）上发布或安排内容发布。当用户希望发推文、安排推文发布时间，或通过 Publora 在 X/Twitter 上发布一系列推文时，可以使用此技能。
---
# Publora — X（Twitter）

通过 Publora API 发布和安排 X/Twitter 的内容。

> **先决条件：** 需要安装 `publora` 核心插件以进行身份验证设置并获取平台 ID。

## 获取您的 Twitter 平台 ID

```bash
GET https://api.publora.com/api/v1/platform-connections
# Look for entries like "twitter-123456"
```

## 立即发推文

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Just shipped something exciting. More soon. 👀',
    platforms: ['twitter-123456']
  })
});
```

## 安排推文时间

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Hot take: most productivity advice is just procrastination in disguise.',
    platforms: ['twitter-123456'],
    scheduledTime: '2026-03-16T14:00:00.000Z'
  })
});
```

## 带图片发推文

```python
import requests

HEADERS = { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' }

post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'New dashboard dropped 🎉',
    'platforms': ['twitter-123456'],
    'scheduledTime': '2026-03-16T14:00:00.000Z'
}).json()

upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
    'fileName': 'dashboard.png', 'contentType': 'image/png',
    'type': 'image', 'postGroupId': post['postGroupId']
}).json()

with open('dashboard.png', 'rb') as f:
    requests.put(upload['uploadUrl'], headers={'Content-Type': 'image/png'}, data=f)
```

## 同时发布到 X 和 LinkedIn

```javascript
body: JSON.stringify({
  content: 'Your content here',
  platforms: ['twitter-123456', 'linkedin-ABC123'],
  scheduledTime: '2026-03-16T10:00:00.000Z'
})
```

## X/Twitter 使用技巧：

- **字符限制：** 280 个字符（订阅 X Premium 可增加字符数）
- **最佳发布时间：** 工作日早上 8 点至下午 4 点，中午 12 点为高峰时段
- **吸引注意力的内容：** 首句必须吸引用户注意力——大多数用户不会点击“显示更多”
- **图片：** 使用 2 或 4 张图片效果更好（采用网格布局）
- **标签：** X 上最多使用 1–2 个标签；使用过多标签会显得像垃圾信息