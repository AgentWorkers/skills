---
name: postiz
description: Postiz 是一款用于安排社交媒体和聊天平台发布内容的工具，支持发布到 28 个以上的平台，包括：X（原 Twitter）、LinkedIn、LinkedIn Page、Reddit、Instagram、Facebook Page、Threads、YouTube、Google My Business、TikTok、Pinterest、Dribbble、Discord、Slack、Kick、Twitch、Mastodon、Bluesky、Lemmy、Farcaster、Telegram、Nostr、VK、Medium、Dev.to、Hashnode 和 WordPress。
homepage: https://docs.postiz.com/public-api/introduction
metadata: {"clawdbot":{"emoji":"🌎","requires":{"bins":[],"env":["POSTIZ_API_KEY"]}}}
---

# Postiz 技能

Postiz 是一个用于将社交媒体和聊天帖子安排发布到 28 个以上渠道的工具：

X、LinkedIn、LinkedIn 页面、Reddit、Instagram、Facebook 页面、Threads、YouTube、Google My Business、TikTok、Pinterest、Dribbble、Discord、Slack、Kick、Twitch、Mastodon、Bluesky、Lemmy、Farcaster、Telegram、Nostr、VK、Medium、Dev.to、Hashnode、WordPress、ListMonk

## 设置

1. 获取您的 API 密钥：https://platform.postiz.com/settings
2. 点击“设置”（Settings）
3. 点击“显示”（Reveal）
4. 设置环境变量：
   ```bash
   export POSTIZ_API_KEY="your-api-key"
   ```

## 获取所有已添加的渠道

```bash
curl -X GET "https://api.postiz.com/public/v1/integrations" \
  -H "Authorization: $POSTIZ_API_KEY"
```

## 获取某个渠道的下一个可用发布时间

```bash
curl -X GET "https://api.postiz.com/public/v1/find-slot/:id" \
  -H "Authorization: $POSTIZ_API_KEY"
```

## 上传新文件（表单数据）

```bash
curl -X POST "https://api.postiz.com/public/v1/upload" \
  -H "Authorization: $POSTIZ_API_KEY" \
  -F "file=@/path/to/your/file.png"
```

## 从现有 URL 上传新文件

```bash
curl -X POST "https://api.postiz.com/public/v1/upload-from-url" \
  -H "Authorization: $POSTIZ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/image.png"
  }'
```

## 发布帖子列表

```bash
curl -X GET "https://api.postiz.com/public/v1/posts?startDate=2024-12-14T08:18:54.274Z&endDate=2024-12-14T08:18:54.274Z&customer=optionalCustomerId" \
  -H "Authorization: $POSTIZ_API_KEY"
```

## 安排新帖子的发布

不同渠道的设置信息请参阅：
https://docs.postiz.com/public-api/introduction
（位于左下角的菜单中）

```bash
curl -X POST "https://api.postiz.com/public/v1/posts" \
  -H "Authorization: $POSTIZ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "type": "schedule",
  "date": "2024-12-14T10:00:00.000Z",
  "shortLink": false,
  "tags": [],
  "posts": [
    {
      "integration": {
        "id": "your-x-integration-id"
      },
      "value": [
        {
          "content": "Hello from the Postiz API! 🚀",
          "image": [{ "id": "img-123", "path": "https://uploads.postiz.com/photo.jpg" }]
        }
      ],
      "settings": {
        "__type": "provider name",
        rest of the settings
      }
    }
  ]
}'
```

## 删除帖子

```bash
curl -X DELETE "https://api.postiz.com/public/v1/posts/:id" \
  -H "Authorization: $POSTIZ_API_KEY"
```