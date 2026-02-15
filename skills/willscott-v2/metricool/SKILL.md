---
name: metricool
description: 通过 Metricool API 来安排和管理社交媒体帖子。适用于在多个平台（如 LinkedIn、X（前身为 Twitter）、Bluesky、Threads、Instagram）上发布内容、查看已安排的帖子或分析社交媒体数据的情况。
---

# Metricool 集成

通过 Metricool 的 API 将帖子安排发布到多个社交媒体平台。

## 设置

从 Metricool 仪表板获取您的 API 令牌。

在 `~/.moltbot/moltbot.json` 文件中添加环境变量：
```json
{
  "env": {
    "vars": {
      "METRICOOL_USER_TOKEN": "your-api-token",
      "METRICOOL_USER_ID": "your@email.com"
    }
  }
}
```

或者在您的工作区 `.env` 文件中添加：
```
METRICOOL_USER_TOKEN=your-api-token
METRICOOL_USER_ID=your@email.com
```

## 脚本

### 获取品牌信息

列出已连接的品牌及其博客 ID：
```bash
node skills/metricool/scripts/get-brands.js
node skills/metricool/scripts/get-brands.js --json
```

### 安排帖子发布

```bash
node skills/metricool/scripts/schedule-post.js '{
  "platforms": ["linkedin", "x", "bluesky", "threads", "instagram"],
  "text": "Your post text here",
  "datetime": "2026-01-30T09:00:00",
  "timezone": "America/New_York",
  "blogId": "YOUR_BLOG_ID"
}'
```

**参数：**
- `platforms`：数组 — linkedin, x, bluesky, threads, instagram, facebook
- `text`：字符串或对象，包含每个平台的发布内容（见下文）
- `datetime`：用于安排发布的 ISO 格式日期时间
- `timezone`：时区（默认：America/Chicago）
- `imageUrl`：可选的公开可访问的图片 URL
- `blogId`：从 `get-brands.js` 获取的品牌 ID

**每个平台的发布内容：**
```json
{
  "text": {
    "linkedin": "Full LinkedIn post with more detail...",
    "x": "Short X post under 280 chars",
    "bluesky": "Bluesky version under 300 chars",
    "threads": "Threads version under 500 chars",
    "instagram": "Instagram with #hashtags"
  }
}
```

### 列出已安排的帖子

```bash
node skills/metricool/scripts/list-scheduled.js
node skills/metricool/scripts/list-scheduled.js --start 2026-01-30 --end 2026-02-05
```

### 获取最佳发布时间

```bash
node skills/metricool/scripts/best-time.js linkedin
node skills/metricool/scripts/best-time.js x
```

## 字符限制

| 平台 | 字符限制 |
|----------|-------|
| LinkedIn | 3,000 |
| X/Twitter | 280 |
| Bluesky | 300 |
| Threads | 500 |
| Instagram | 2,200 |

## 图片要求

- 图片必须是公开可访问的 URL（例如 S3、GCS 等）
- 推荐的图片格式：PNG、JPG
- 对于 Instagram/Threads，方形图片效果最佳
- 对于 X/LinkedIn，宽高比为 1.91:1 的图片效果最佳