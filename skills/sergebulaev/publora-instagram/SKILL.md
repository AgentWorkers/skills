---
name: publora-instagram
description: 使用 Publora API 将内容发布或安排到 Instagram 上。当用户希望通过 Publora 将图片、Reels、Stories 或轮播图发布到 Instagram 时，可以使用此技能。
---
# Publora — Instagram

这是一个用于Publora API的Instagram相关功能。关于授权、核心调度、媒体上传以及工作区/Webhook的详细信息，请参阅`publora`核心技能文档。

**基础URL:** `https://api.publora.com/api/v1`  
**请求头:** `x-publora-key: sk_YOUR_KEY`  
**平台ID格式:** `instagram-{accountId}`

## 使用要求

- **必须使用Instagram企业账户**（个人账户和创作者账户不支持Instagram Graph API）  
- 账户必须关联到一个Facebook页面  
- 通过Publora控制台使用OAuth进行连接

## 平台限制（API）

> ⚠️ Instagram API的限制比原生应用程序更为严格。

| 属性          | API限制      | 原生应用程序 |
|----------------|------------|------------|
| 标题            | **2,200个字符**    | 2,200个字符    |
| 图片              | **每张图片大小不超过8 MB** | 每张图片不超过20 MB |
| 图片格式          | **仅支持JPEG**    | 支持PNG和GIF格式 |
| 混合轮播           | **不允许图片和视频混合** | 可以混合图片和视频 |
| Reels（短视频）时长    | **90秒**      | 最长15–20分钟   |
| Reels文件大小       | **300 MB**      | —          |
| 轮播视频          | **每个视频片段最长60秒** | —          |
| 仅文本            | **必须包含媒体内容** | 不允许仅文本   |
| 请求频率限制      | **24小时内50条帖子** | —          |

在“查看更多”之前，前125个字符会显示在页面上。

**常见错误：**
- `(#10) 用户不是Instagram企业账户` — 不支持创作者账户，请切换为企业账户  
- `Error 2207010` — 标题超过2,200个字符  
- `Error 2207004` — 图片大小超过8 MB  
- `Error 9, Subcode 2207042` — 达到请求频率限制

## 发布图片

```javascript
// Step 1: Create the post
const post = await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Your caption here ✨ #hashtag',
    platforms: ['instagram-17841412345678'],
    scheduledTime: '2026-03-20T12:00:00.000Z'
  })
}).then(r => r.json());

// Step 2: Get upload URL
const upload = await fetch('https://api.publora.com/api/v1/get-upload-url', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    postGroupId: post.postGroupId,
    fileName: 'photo.jpg',
    contentType: 'image/jpeg',   // ⚠️ JPEG only for Instagram
    type: 'image'
  })
}).then(r => r.json());

// Step 3: Upload to S3
await fetch(upload.uploadUrl, {
  method: 'PUT',
  headers: { 'Content-Type': 'image/jpeg' },
  body: imageFileBytes
});
```

## 发布轮播（最多10张图片）

使用相同的`postGroupId`，多次调用`get-upload-url`接口：

```python
import requests

HEADERS = { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' }

# Create post
post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'Swipe through our product highlights! 👆',
    'platforms': ['instagram-17841412345678'],
    'scheduledTime': '2026-03-20T12:00:00.000Z'
}).json()

# Upload each image (max 10)
images = ['slide1.jpg', 'slide2.jpg', 'slide3.jpg']
for img_path in images:
    upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
        'postGroupId': post['postGroupId'],
        'fileName': img_path,
        'contentType': 'image/jpeg',
        'type': 'image'
    }).json()
    with open(img_path, 'rb') as f:
        requests.put(upload['uploadUrl'], headers={'Content-Type': 'image/jpeg'}, data=f)
```

## 发布Reel（视频，最长90秒）

```javascript
// Create post, then upload video via get-upload-url with type: 'video'
const post = await createPost({
  content: 'Check out our latest Reel! 🎬',
  platforms: ['instagram-17841412345678']
});

const upload = await getUploadUrl({
  postGroupId: post.postGroupId,
  fileName: 'reel.mp4',
  contentType: 'video/mp4',
  type: 'video'
});
// Then PUT the video file to upload.uploadUrl
```

> ⚠️ 通过API发布的Reel时长不得超过90秒，超过时将无法上传。

## 平台的特殊规定

- **仅支持JPEG格式**：Instagram Graph API不支持PNG和GIF格式，上传前请将图片转换为JPEG。Publora本身不自动进行格式转换。
- **仅限企业账户使用**：创作者账户无法使用此API。
- **API不允许使用购物标签、品牌内容、滤镜或音乐**。
- **轮播功能**：API最多支持10个图片或视频；同一轮播中不能混合图片和视频。
- **WebP格式**：上传前必须手动转换为JPEG格式。