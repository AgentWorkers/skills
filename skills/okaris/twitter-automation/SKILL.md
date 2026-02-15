---
name: twitter-automation
description: |
  Automate Twitter/X with posting, engagement, and user management via inference.sh CLI.
  Apps: x/post-tweet, x/post-create (with media), x/post-like, x/post-retweet, x/dm-send, x/user-follow.
  Capabilities: post tweets, schedule content, like posts, retweet, send DMs, follow users, get profiles.
  Use for: social media automation, content scheduling, engagement bots, audience growth, X API.
  Triggers: twitter api, x api, tweet automation, post to twitter, twitter bot,
  social media automation, x automation, tweet scheduler, twitter integration,
  post tweet, twitter post, x post, send tweet
allowed-tools: Bash(infsh *)
---

# Twitter/X 自动化

通过 [inference.sh](https://inference.sh) 命令行工具（CLI）实现 Twitter/X 的自动化操作。

## 快速入门

```bash
# Install CLI
curl -fsSL https://cli.inference.sh | sh && infsh login

# Post a tweet
infsh app run x/post-tweet --input '{"text": "Hello from inference.sh!"}'
```

## 可用的应用程序

| 应用程序 | 应用程序 ID | 功能描述 |
|-----|--------|-------------|
| 发布推文 | `x/post-tweet` | 发布纯文本推文 |
| 创建帖子 | `x/post-create` | 发布带有图片/视频的帖子 |
| 点赞推文 | `x/post-like` | 给推文点赞 |
| 转发推文 | `x/post-retweet` | 转发推文 |
| 删除推文 | `x/post-delete` | 删除推文 |
| 获取推文信息 | `x/post-get` | 通过 ID 获取推文详情 |
| 发送私信 | `x/dm-send` | 发送私信 |
| 关注用户 | `x/user-follow` | 关注用户 |
| 获取用户信息 | `x/user-get` | 获取用户资料 |

## 示例

### 发布推文

```bash
infsh app run x/post-tweet --input '{"text": "Just shipped a new feature! 🚀"}'
```

### 发布带有图片/视频的推文

```bash
infsh app sample x/post-create --save input.json

# Edit input.json:
# {
#   "text": "Check out this AI-generated image!",
#   "media_url": "https://your-image-url.jpg"
# }

infsh app run x/post-create --input input.json
```

### 给推文点赞

```bash
infsh app run x/post-like --input '{"tweet_id": "1234567890"}'
```

### 转发推文

```bash
infsh app run x/post-retweet --input '{"tweet_id": "1234567890"}'
```

### 发送私信

```bash
infsh app run x/dm-send --input '{
  "recipient_id": "user_id_here",
  "text": "Hey! Thanks for the follow."
}'
```

### 关注用户

```bash
infsh app run x/user-follow --input '{"username": "elonmusk"}'
```

### 获取用户资料

```bash
infsh app run x/user-get --input '{"username": "OpenAI"}'
```

### 获取推文详情

```bash
infsh app run x/post-get --input '{"tweet_id": "1234567890"}'
```

### 删除推文

```bash
infsh app run x/post-delete --input '{"tweet_id": "1234567890"}'
```

## 工作流程：生成 AI 图像并发布

```bash
# 1. Generate image
infsh app run falai/flux-dev-lora --input '{"prompt": "sunset over mountains"}' > image.json

# 2. Post to Twitter with the image URL
infsh app run x/post-create --input '{
  "text": "AI-generated art of a sunset 🌅",
  "media_url": "<image-url-from-step-1>"
}'
```

## 工作流程：生成并发布视频

```bash
# 1. Generate video
infsh app run google/veo-3-1-fast --input '{"prompt": "waves on a beach"}' > video.json

# 2. Post to Twitter
infsh app run x/post-create --input '{
  "text": "AI-generated video 🎬",
  "media_url": "<video-url-from-step-1>"
}'
```

## 相关技能

```bash
# Full platform skill (all 150+ apps)
npx skills add inference-sh/agent-skills@inference-sh

# Image generation (create images to post)
npx skills add inference-sh/agent-skills@ai-image-generation

# Video generation (create videos to post)
npx skills add inference-sh/agent-skills@ai-video-generation

# AI avatars (create presenter videos)
npx skills add inference-sh/agent-skills@ai-avatar-video
```

查看所有应用程序：`infsh app list`

## 文档资料

- [X.com 集成](https://inference.sh/docs/integrations/x) - 设置 Twitter/X 集成
- [X.com 集成示例](https://inference.sh/docs/examples/x-integration) - 完整的 Twitter 自动化工作流程
- [应用程序概述](https://inference.sh/docs/apps/overview) - 了解应用程序生态系统