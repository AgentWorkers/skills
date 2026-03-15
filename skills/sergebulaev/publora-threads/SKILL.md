---
name: publora-threads
description: 使用 Publora API 在 Threads 中发布或安排内容。当用户希望通过 Publora 发布或安排 Threads 的帖子时，可以使用此技能。
---
# Publora — 线程（Threads）

这是用于 Publora API 的线程相关功能。关于认证、核心调度、媒体上传以及工作区/Webhook 的详细信息，请参阅 `publora` 核心技能文档。

**基础 URL：** `https://api.publora.com/api/v1`  
**请求头：** `x-publora-key: sk_YOUR_KEY`  
**平台 ID 格式：** `threads-{accountId}`

## ⚠️ 临时限制：线程嵌套功能不可用

由于 Threads 应用程序的重新连接问题，目前暂时无法使用多线程嵌套帖子功能。

这意味着：超过 500 个字符的文本内容（通常会自动拆分为多个回复）将无法正常显示。

**目前仍可正常使用的功能：**
- 单个帖子（文本、图片、视频、轮播图）
- 字符数少于 500 的独立帖子

如需了解线程嵌套功能何时恢复的更新信息，请联系 support@publora.com。

## 平台限制（API）

| 属性          | API 限制        | 备注              |
|------------------|------------------|-------------------|
| 文本            | 最多 500 个字符    | 可通过文本附件上传最多 10,000 个字符 |
| 图片            | 最大尺寸 20 × 8 MB    | 支持 JPEG 和 PNG 格式         |
| 视频            | 最长 5 分钟      | 最大文件大小 500 MB         | 支持 MP4 和 MOV 格式         |
| 最大链接数        | 每个帖子最多 5 个    |                    |
| 仅文本帖子        | 可以              |                    |
| 线程功能        | ⚠️ 临时不可用       | 详见上文              |
| 日发送帖子数量限制    | 24 小时内 250 条    | 24 小时内最多 1,000 条回复     |

## 发布单个帖子

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Building in public is the best marketing strategy. Here\'s why 👇',
    platforms: ['threads-17841412345678']
  })
});
```

## 安排帖子发布时间

```javascript
body: JSON.stringify({
  content: 'Your Threads post here',
  platforms: ['threads-17841412345678'],
  scheduledTime: '2026-03-20T10:00:00.000Z'
})
```

## 发布带图片的帖子

```javascript
// Step 1: Create post
const post = await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Caption for your image post',
    platforms: ['threads-17841412345678']
  })
}).then(r => r.json());

// Step 2: Get upload URL
const upload = await fetch('https://api.publora.com/api/v1/get-upload-url', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    postGroupId: post.postGroupId,
    fileName: 'photo.jpg',
    contentType: 'image/jpeg',
    type: 'image'
  })
}).then(r => r.json());

// Step 3: Upload to S3
await fetch(upload.uploadUrl, {
  method: 'PUT',
  headers: { 'Content-Type': 'image/jpeg' },
  body: imageBytes
});
```

## 线程嵌套（功能恢复后）

当线程嵌套功能恢复后，您可以使用 `---` 在单独的行中分隔长文本内容：

```javascript
body: JSON.stringify({
  content: 'First post in thread.\n\n---\n\nSecond post continues the thought.\n\n---\n\nFinal post wraps up.',
  platforms: ['threads-17841412345678']
})
```

> ⚠️ 目前该功能已被禁用。单个帖子和轮播图仍可正常使用。

## 平台特性：
- **通过 Meta OAuth 连接** — 与 Instagram 使用相同的账户登录
- **每个帖子最多 5 个链接** — Threads 在 API 级别强制执行此限制
- **支持 PNG 格式的图片** — 与 Instagram 不同，Threads 支持 PNG 格式的图片
- **线程嵌套限制** — 详见上文中的通知