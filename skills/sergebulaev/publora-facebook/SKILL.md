---
name: publora-facebook
description: 使用 Publora API 在 Facebook 页面上发布或安排内容。当用户希望通过 Publora 发布或安排 Facebook 帖子时，可以使用此技能。
---
# Publora — Facebook

这是一个用于 Publora API 的 Facebook 平台相关功能。关于认证、核心调度、媒体上传以及工作空间/Webhook 的详细信息，请参阅 `publora` 核心功能文档。

**基础 URL：** `https://api.publora.com/api/v1`  
**请求头：** `x-publora-key: sk_YOUR_KEY`  
**平台 ID 格式：** `facebook-{pageId}`  

如果您管理多个 Facebook 页面，每个页面都会有自己的平台 ID。

## 使用要求

- 需要一个通过 OAuth 连接的 **Facebook 页面**（而非个人资料）。  
- 在 OAuth 过程中，必须授予页面管理员权限。  

## 平台限制（API）

> ⚠️ API 对视频的使用限制比 Facebook 原生应用更为严格：

| 属性          | API 限制        | 原生应用限制      |
|---------------|--------------|--------------|
| 文本            | **63,206 个字符**    | 相同           |
| 图片            | 最大 10 × 10 MB     | JPEG, PNG, GIF, BMP, TIFF   |
| 视频            | **最长 45 分钟**     | 最长 240 分钟     |
| Reels（短视频）     | **时长 3–90 秒**    | 每页每天最多 30 个     |
| 发布 Reels       | 仅限页面（非个人资料）   |                |
| 仅文本           | ✅ 可以         |                |

**常见错误：**
- `Error 1363026`：视频时长超过 45 分钟 → 请将视频修剪至 45 分钟以内。  
- `Error 1363023`：文件大小超过 2 GB → 请压缩文件。  
- `Error 1363128`：Reels 的时长不在 3–90 秒范围内。  

> 在 Facebook 上，文本帖子的互动率会高出 66%。  

## 发布文本更新  
```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Exciting news from our team! We just launched a new feature. Check it out at publora.com 🎉',
    platforms: ['facebook-123456789']
  })
});
```  

## 安排帖子发布  
```javascript
body: JSON.stringify({
  content: 'Your Facebook Page update',
  platforms: ['facebook-123456789'],
  scheduledTime: '2026-03-20T13:00:00.000Z'
})
```  

## 发布带有图片的帖子  
```javascript
// Step 1: Create post
const post = await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Check out our latest product photo!',
    platforms: ['facebook-123456789']
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

// Step 3: Upload
await fetch(upload.uploadUrl, {
  method: 'PUT',
  headers: { 'Content-Type': 'image/jpeg' },
  body: imageBytes
});
```  

## 发布 Reels（时长 3–90 秒）  
使用相同的流程，但上传一个短视频文件。Reels 仅能发布在页面上。  

## 平台的特殊注意事项：  
- **仅限页面**：个人资料无法通过 Facebook Graph API 进行操作。  
- **多个页面**：每个页面都有独立的平台 ID；需在 Publora 控制台中分别进行配置。  
- **视频限制**：API 中视频最长为 45 分钟，文件大小不超过 2 GB；原生应用支持最长 240 分钟，文件大小不超过 4 GB。  
- **Reels**：时长必须在 3–90 秒之间，每页每天最多发布 30 个。  
- **轮播图**：最多可包含 10 张图片或视频（不能在同一轮播图中混合使用）。  
- **发布频率限制**：每小时每用户最多 200 次发布。