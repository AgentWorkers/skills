---
name: postproxy
description: 调用 PostProxy API 来创建和管理社交媒体帖子。
allowed-tools: Bash
---

# PostProxy API 功能

调用 PostProxy API 可以管理多个平台（Facebook、Instagram、TikTok、LinkedIn、YouTube、X/Twitter、Threads）上的社交媒体帖子。

## 设置

API 密钥必须设置为环境变量 `POSTPROXY_API_KEY`。
您可以在以下链接获取 API 密钥：https://app.postproxy.dev/api_keys

## 基本 URL

```
https://api.postproxy.dev
```

## 认证

所有请求都需要使用 Bearer 令牌：
```bash
-H "Authorization: Bearer $POSTPROXY_API_KEY"
```

## 端点

### 列出个人资料
```bash
curl -X GET "https://api.postproxy.dev/api/profiles" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

### 列出帖子
```bash
curl -X GET "https://api.postproxy.dev/api/posts" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

### 获取帖子信息
```bash
curl -X GET "https://api.postproxy.dev/api/posts/{id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

### 创建帖子（包含媒体链接）
```bash
curl -X POST "https://api.postproxy.dev/api/posts" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "post": {
      "body": "Post content here"
    },
    "profiles": ["twitter", "linkedin", "threads"],
    "media": ["https://example.com/image.jpg"]
  }'
```

### 创建帖子（文件上传）
使用 multipart 形式的数据上传本地文件：
```bash
curl -X POST "https://api.postproxy.dev/api/posts" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -F "post[body]=Check out this image!" \
  -F "profiles[]=instagram" \
  -F "profiles[]=twitter" \
  -F "media[]=@/path/to/image.jpg" \
  -F "media[]=@/path/to/image2.png"
```

### 创建草稿
在创建帖子时添加 `post[draft]=true` 选项以不立即发布：
```bash
curl -X POST "https://api.postproxy.dev/api/posts" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -F "post[body]=Draft post content" \
  -F "profiles[]=twitter" \
  -F "media[]=@/path/to/image.jpg" \
  -F "post[draft]=true"
```

### 发布草稿
```bash
curl -X POST "https://api.postproxy.dev/api/posts/{id}/publish" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

个人资料选项：`facebook`、`instagram`、`tiktok`、`linkedin`、`youtube`、`twitter`、`threads`（或使用个人资料 ID）

### 安排帖子发布时间
在帖子对象中添加 `scheduled_at` 选项：
```bash
curl -X POST "https://api.postproxy.dev/api/posts" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "post": {
      "body": "Scheduled post",
      "scheduled_at": "2024-01-16T09:00:00Z"
    },
    "profiles": ["twitter"]
  }'
```

### 删除帖子
```bash
curl -X DELETE "https://api.postproxy.dev/api/posts/{id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

## 平台特定参数

对于 Instagram、TikTok 和 YouTube，需要添加 `platforms` 对象：
```json
{
  "platforms": {
    "instagram": { "format": "reel", "first_comment": "Link in bio!" },
    "youtube": { "title": "Video Title", "privacy_status": "public" },
    "tiktok": { "privacy_status": "PUBLIC_TO_EVERYONE" }
  }
}
```

## 用户请求参数
$ARGUMENTS