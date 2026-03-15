---
name: publora-telegram
description: 使用 Publora API 将内容发布到 Telegram 频道或群组中，或安排内容的发布时间。当用户希望通过 Publora 发布或安排 Telegram 消息时，可以使用此技能。
---
# Publora — Telegram

这是一个用于与Publora API交互的Telegram平台技能。关于认证、核心调度、媒体上传以及工作空间/Webhook的相关文档，请参考`publora`核心技能。

**基础URL：** `https://api.publora.com/api/v1`  
**请求头：** `x-publora-key: sk_YOUR_KEY`  
**平台ID格式：** `telegram-{chatId}`

## 使用要求

1. 通过[@BotFather](https://t.me/BotFather)在Telegram上创建一个机器人。
2. 复制机器人的Token。
3. 将该机器人添加为目标频道或群组的**管理员**。
4. 使用机器人的Token和频道名称，通过Publora控制台进行连接。

## 平台限制（API — 机器人API）

> ⚠️ Telegram机器人API对文件大小有严格的限制，最大为50 MB（而非用户客户端允许的4 GB）。

| 属性          | 机器人API限制    | 用户客户端限制    |
|---------------|------------|-------------|
| 文本（消息）       | **4,096个字符**   | 相同          |
| 媒体标题        | **1,024个字符**   | （高级版）4,096个字符 |
| 图片            | 最大10 MB      | JPEG, PNG, GIF, WebP, BMP |
| 视频            | **50 MB**      | 4 GB          |
| 视频格式        | MP4, MOV, AVI, MKV, WebM | 不支持        |
| 仅文本消息       | ✅ 可       | 不支持          |
| 发送频率限制     | 每秒30条消息    | 每群组每分钟20条消息   |

**常见错误：**
- `MEDIA_CAPTION_TOO_LONG` — 标题超过1,024个字符 → 请缩短标题或将其放入消息正文中。
- `Bad Request: file is too big` — 文件大小超过50 MB → 请压缩文件或使用更小的文件。

## 发送文本消息

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: '📢 **Announcement**: Our new feature is live! Check it out at publora.com\n\n#update #publora',
    platforms: ['telegram--1001234567890']  // note: group chat IDs are negative
  })
});
```

在Telegram消息中支持Markdown格式。

## 安排消息的发送时间

```javascript
body: JSON.stringify({
  content: 'Your Telegram channel message here',
  platforms: ['telegram--1001234567890'],
  scheduledTime: '2026-03-20T09:00:00.000Z'
})
```

## 发送图片

```python
import requests

HEADERS = { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' }

# Step 1: Create post (content = caption, max 1,024 chars for media)
post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'Check out our latest update! 🚀',   # keep under 1,024 chars when attaching media
    'platforms': ['telegram--1001234567890']
}).json()

# Step 2: Get upload URL (max 10 MB per image)
upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
    'postGroupId': post['postGroupId'],
    'fileName': 'image.jpg',
    'contentType': 'image/jpeg',
    'type': 'image'
}).json()

# Step 3: Upload
with open('image.jpg', 'rb') as f:
    requests.put(upload['uploadUrl'], headers={'Content-Type': 'image/jpeg'}, data=f)
```

## 发送视频（最大50 MB）

发送视频的流程与发送图片相同，只需在请求头中添加`contentType: 'video/mp4'`和`type: 'video'`。请确保文件大小不超过50 MB。

## 平台的特殊注意事项：

- **机器人API的文件大小限制为50 MB**，而非用户客户端允许的4 GB。对于较大的文件，您需要使用本地机器人API服务器（Publora不支持此功能）。
- **标题与消息正文的关系**：在上传媒体文件时，文件内容会被视为标题（最多1,024个字符）。对于仅包含文本的消息，内容长度可达到4,096个字符。
- **Markdown格式支持**：可以在消息内容中使用`**bold**、`_italic_`、````、`code`、`[link](url)`等标记。
- **群组ID为负数形式**：例如`telegram--1001234567890`。
- **机器人必须具有管理员权限**：机器人需要在频道中具有管理员权限才能发布消息；在群组中，至少需要“发送消息”的权限。
- **发送频率限制**：全局范围内每秒30条消息；每个群组每分钟20条消息——Publora会自动处理发送请求的排队。