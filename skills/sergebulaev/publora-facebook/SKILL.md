---
name: publora-facebook
description: 使用 Publora API 在 Facebook 页面上发布或安排内容。当用户希望通过 Publora 发布或安排 Facebook 帖子时，可以使用此技能。
---
# Publora — Facebook

通过 Publora API 发布和安排 Facebook 页面的内容。

> **先决条件：** 需要安装 `publora` 核心技能，以便进行身份验证设置和获取平台 ID。

## 平台 ID 格式

`facebook-{pageId}` — 从 `GET /api/v1/platform-connections` 中获取您的确切 ID。

## 账户要求

- **仅支持 Facebook 页面** — 个人资料不支持通过此 API 使用
- 每个连接的页面都有自己的 `facebook-{pageId}` 平台 ID
- **多个页面：** 可以在单个 API 调用中发布到多个页面，只需在 `platforms` 数组中包含多个 ID 即可

## 支持的内容类型

| 类型 | 是否支持 | 备注 |
|------|-----------|-------|
| 纯文本 | ✅ | 最长 63,206 个字符 |
| 单张图片 | ✅ | 支持 JPEG/PNG 格式；WebP 图片会自动转换为 JPEG |
| 多张图片 | ✅ | 会生成图片专辑/轮播效果 |
| 视频 | ✅ | 仅支持 MP4 格式；不能与图片同时发布 |
| 链接预览 | ✅ | 会从文本中的 URL 生成链接预览（遵循 Facebook 的行为）

## 文本长度限制

最多支持 **63,206 个字符**（API 没有硬性限制，但这是 Facebook 推荐的最大长度）。

## 向 Facebook 页面发布内容

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Big news from our team today! We just crossed 10,000 customers. 🎉\n\nThank you all for your support. Here is what is coming next...',
    platforms: ['facebook-PAGE_ID']
  })
});
```

## 向多个页面发布内容

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Announcement going out to all our brand pages!',
    platforms: ['facebook-PAGE_ID_1', 'facebook-PAGE_ID_2', 'facebook-PAGE_ID_3']
  })
});
```

## 带图片发布内容（生成图片专辑）

发布多张图片会生成一个 Facebook 图片专辑。请按照以下三步上传流程操作：每张图片都需要调用 `get-upload-url` 并使用相同的 `postGroupId`。

```python
import requests

HEADERS = { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' }

# Step 1: Create post
post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'Photos from our annual company retreat! Great time with the team.',
    'platforms': ['facebook-PAGE_ID'],
    'scheduledTime': '2026-03-16T10:00:00.000Z'
}).json()
post_group_id = post['postGroupId']

# Steps 2+3: Upload each image (all use same postGroupId)
for img_path in ['retreat1.jpg', 'retreat2.jpg', 'retreat3.jpg']:
    upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
        'fileName': img_path, 'contentType': 'image/jpeg',
        'type': 'image', 'postGroupId': post_group_id
    }).json()
    with open(img_path, 'rb') as f:
        requests.put(upload['uploadUrl'], headers={'Content-Type': 'image/jpeg'}, data=f)
```

**关于 WebP 图片：** Publora 会自动将 WebP 图片转换为 JPEG 格式。

## 发布视频

视频必须单独发布——不能在同一条帖子中同时发布图片和视频。

```python
# Step 1: Create post
post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'Watch our product demo — 2 minutes to see everything! 🎬',
    'platforms': ['facebook-PAGE_ID']
}).json()

# Step 2: Get upload URL
upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
    'fileName': 'demo.mp4', 'contentType': 'video/mp4',
    'type': 'video', 'postGroupId': post['postGroupId']
}).json()

# Step 3: Upload to S3
with open('demo.mp4', 'rb') as f:
    requests.put(upload['uploadUrl'], headers={'Content-Type': 'video/mp4'}, data=f)
```

## 安排 Facebook 帖子的发布时间

```javascript
body: JSON.stringify({
  content: 'Weekly update post — scheduled for Monday morning.',
  platforms: ['facebook-PAGE_ID'],
  scheduledTime: '2026-03-16T08:00:00.000Z'
})
```

## 访问令牌的自动刷新

Facebook 的访问令牌在 **59 天** 后会过期。Publora 会自动刷新令牌。

- 如果自动刷新 **成功**：无需任何操作
- 如果自动刷新 **失败**：请通过 Publora 仪表板（设置 → 连接）重新连接

## 链接预览

当您在帖子文本中包含 URL 时，Facebook 会 **自动生成链接预览**（包括标题、描述和缩略图）。这是 Facebook 的内置功能——Publora 无法对其进行控制。

## 使用 Publora 发布内容时的注意事项：

- **仅支持 Facebook 页面** — 个人资料无法通过此 API 使用
- 如果要发布到多个页面，请在 `platforms` 数组中包含所有页面的 `facebook-{pageId}` 值
- 不能在同一条帖子中同时发布图片和视频——请选择其中一种类型
- 当文本中包含 URL 时，系统会自动生成链接预览
- 访问令牌每 59 天更新一次——Publora 会自动刷新令牌，但请留意重新连接的提示
- 支持较长的内容——Facebook 允许发布最多 63,206 个字符，非常适合发布详细信息