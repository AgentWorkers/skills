---
name: publora-tiktok
description: 使用 Publora API 在 TikTok 上发布或安排视频内容的发布。当用户希望通过 Publora 在 TikTok 上发布或安排视频的发布时，可以使用此技能。
---
# Publora — TikTok

通过 Publora API 发布和安排 TikTok 视频内容。

> **前提条件：** 安装 `publora` 核心技能，以进行身份验证设置并获取平台 ID。

## 获取您的 TikTok 平台 ID

```bash
GET https://api.publora.com/api/v1/platform-connections
# Look for entries like "tiktok-99887766"
```

## 发布 TikTok 视频

TikTok 要求上传视频。请务必在 TikTok 帖子中附加视频。

```javascript
const API_KEY = 'sk_YOUR_KEY';
const BASE_URL = 'https://api.publora.com/api/v1';
const headers = { 'Content-Type': 'application/json', 'x-publora-key': API_KEY };

// Step 1: Create post with TikTok settings
const postRes = await fetch(`${BASE_URL}/create-post`, {
  method: 'POST', headers,
  body: JSON.stringify({
    content: 'How we built our startup in 60 seconds #startup #tech #coding',
    platforms: ['tiktok-99887766'],
    platformSettings: {
      tiktok: {
        viewerSetting: 'PUBLIC_TO_EVERYONE',
        allowComments: true,
        allowDuet: true,
        allowStitch: true,
        commercialContent: false,
        brandOrganic: false,
        brandedContent: false
      }
    }
  })
});
const { postGroupId } = await postRes.json();

// Step 2: Get upload URL
const uploadRes = await fetch(`${BASE_URL}/get-upload-url`, {
  method: 'POST', headers,
  body: JSON.stringify({
    fileName: 'video.mp4', contentType: 'video/mp4',
    type: 'video', postGroupId
  })
});
const { uploadUrl } = await uploadRes.json();

// Step 3: Upload video (use fs/buffer in Node.js)
const fs = require('fs');
const axios = require('axios');
const videoBuffer = fs.readFileSync('./video.mp4');
await axios.put(uploadUrl, videoBuffer, {
  headers: { 'Content-Type': 'video/mp4' },
  maxContentLength: 512 * 1024 * 1024
});
```

## 安排 TikTok 帖子的发布时间

```javascript
body: JSON.stringify({
  content: 'Day in the life of a founder 📱',
  platforms: ['tiktok-99887766'],
  scheduledTime: '2026-03-16T18:00:00.000Z',
  platformSettings: {
    tiktok: {
      viewerSetting: 'PUBLIC_TO_EVERYONE',
      allowComments: true,
      allowDuet: false,
      allowStitch: false,
      commercialContent: false,
      brandOrganic: false,
      brandedContent: false
    }
  }
})
```

## TikTok 平台设置参考

| 设置 | 类型 | 描述 |
|---------|------|-------------|
| `viewerSetting` | 字符串 | `PUBLIC_TO_EVERYONE`, `MUTUAL_follow FRIENDS`, `SELF_ONLY` |
| `allowComments` | 布尔值 | 是否允许观众评论 |
| `allowDuet` | 布尔值 | 是否允许使用“Duet”功能 |
| `allowStitch` | 布尔值 | 是否允许使用“Stitch”功能 |
| `commercialContent` | 布尔值 | 是否标记为商业/广告内容 |
| `brandOrganic` | 布尔值 | 品牌原创内容 |
| `brandedContent` | 布尔值 | 付费品牌合作内容 |

## TikTok 使用技巧：

- **必须上传视频** — 仅文本的帖子在 TikTok 上无法发布。
- **视频格式必须为 9:16 的竖屏格式** — 其他格式的视频会被裁剪。
- **最大文件大小**：512 MB。
- **开头 1–3 秒的内容至关重要** — 这直接影响观看时长和算法推荐。
- **最佳时长**：7–15 秒适合快速传播的内容；60 秒以上适合教育类内容。
- **最佳发布时间**：工作日下午 6–10 点；周末上午 9–11 点。
- **使用热门背景音乐** — 可显著提高视频的传播范围。