---
name: publora-linkedin
description: 使用 Publora API 在 LinkedIn 上发布或安排内容。当用户需要发布或安排 LinkedIn 帖子、获取分析数据（浏览量、互动情况、关注者数量）、管理用户互动、发表评论，或通过 Publora @ 提及他人/组织时，可以使用此技能。
---
# Publora — LinkedIn

这是一个用于Publora API的LinkedIn平台相关技能。关于认证、核心调度、媒体上传以及工作区/Webhook的详细文档，请参考`publora`核心技能。

**基础URL：** `https://api.publora.com/api/v1`  
**请求头：** `x-publora-key: sk_YOUR_KEY`  
**平台ID格式：** `linkedin-{profileId}`

## 平台限制（API）

> ⚠️ API的限制与原生应用程序有所不同。请在设计时考虑到这些限制。

| 属性          | API限制          | 原生应用程序限制          |
|------------------|------------------|----------------------|
| 文本            | **3,000个字符**       | 3,000个字符             |
| 图片            | 最大20张，每张5MB（JPEG/PNG/GIF格式） | 同API限制             |
| 视频            | 最长30分钟，最大500MB      | 最长15分钟，最大5GB            |
| 视频格式          | 仅支持MP4           | 支持MP4和MOV格式           |
| 自动轮播图片        | 🚫 无法通过API实现       | ✅ 可通过API实现             |
| 混合媒体          | 🚫 不支持           | ✅ 可通过API实现             |
| 请求频率限制      | 每小时约200次请求     | 无限制                 |

在“查看更多”之前，前210个字符会显示在页面上。

**常见错误：**
- `MEDIA_ASSET_PROCESSING_FAILED` — 文件过大或格式不支持
- `Error 429` — 超过请求频率限制

## 发布文本更新

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Excited to announce our latest product update! #buildinpublic',
    platforms: ['linkedin-ABC123']
  })
});
```

## 提及人员和组织

在`content`字段中使用以下语法来提及人员和组织：

```
@{urn:li:person:MEMBER_ID|Display Name}       # person
@{urn:li:organization:ORG_ID|Company Name}    # company
```

显示名称必须与LinkedIn上的个人资料名称完全匹配（区分大小写）。

```javascript
body: JSON.stringify({
  content: 'Great collaboration with @{urn:li:organization:107107343|Creative Content Crafts Inc}!',
  platforms: ['linkedin-ABC123']
})
```

## 安排帖子发布时间

```javascript
body: JSON.stringify({
  content: 'Your LinkedIn update here',
  platforms: ['linkedin-ABC123'],
  scheduledTime: '2026-03-20T09:00:00.000Z'
})
```

## 分析

### 帖子统计信息

```javascript
const res = await fetch('https://api.publora.com/api/v1/linkedin-post-statistics', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    postedId: 'urn:li:share:7123456789',   // or urn:li:ugcPost:xxx
    platformId: 'linkedin-ABC123',
    queryTypes: 'ALL'   // IMPRESSION | MEMBERS_REACHED | RESHARE | REACTION | COMMENT
  })
});
```

### 账户统计信息

```javascript
await fetch('https://api.publora.com/api/v1/linkedin-account-statistics', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({ platformId: 'linkedin-ABC123' })
});
```

### 关注者数量及增长情况

```javascript
await fetch('https://api.publora.com/api/v1/linkedin-followers', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({ platformId: 'linkedin-ABC123' })
});
```

### 个人资料概览

```javascript
await fetch('https://api.publora.com/api/v1/linkedin-profile-summary', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({ platformId: 'linkedin-ABC123' })
});
```

> 发布后的数据分析可能需要最多24小时才能完整显示。

## 互动反应

支持的互动类型：`LIKE`（点赞）、`PRAISE`（赞美）、`EMPATHY`（表示同情）、`INTEREST`（表示感兴趣）、`APPRECIATION`（表示感谢）、`ENTERTAINMENT`（表示觉得内容有趣）

### 创建互动反应

```javascript
await fetch('https://api.publora.com/api/v1/linkedin-reactions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    postedId: 'urn:li:ugcPost:7429953213384187904',
    reactionType: 'INTEREST',
    platformId: 'linkedin-ABC123'
  })
});
```

### 删除互动反应

```javascript
await fetch('https://api.publora.com/api/v1/linkedin-reactions', {
  method: 'DELETE',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    postedId: 'urn:li:ugcPost:7429953213384187904',
    platformId: 'linkedin-ABC123'
  })
});
```

## 评论

### 创建评论

```javascript
await fetch('https://api.publora.com/api/v1/linkedin-comments', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    postedId: 'urn:li:share:7434685316856377344',
    message: 'Great post! Thanks for sharing.',  // max 1,250 characters
    platformId: 'linkedin-ABC123',
    // parentComment: 'urn:li:comment:(...)' ← for nested replies
  })
});
```

### 删除评论

```javascript
await fetch('https://api.publora.com/api/v1/linkedin-comments', {
  method: 'DELETE',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    postedId: 'urn:li:share:7434685316856377344',
    commentId: 'urn:li:comment:(urn:li:activity:xxx,7434695495614312448)',
    platformId: 'linkedin-ABC123'
  })
});
```

## 平台特性

- **API不支持粗体/斜体格式** — LinkedIn API不支持丰富的文本格式
- **帖子ID格式**：通过Publora创建的帖子使用`/get-post`接口返回的`postedId`；外部帖子的ID格式为`urn:li:share:xxx`或`urn:li:ugcPost:xxx`
- **WebP格式的图片**会自动转换为JPEG格式
- **标签**以纯文本形式显示，但可点击
- **API无法实现自动轮播图片** — 只能显示多张图片的网格布局