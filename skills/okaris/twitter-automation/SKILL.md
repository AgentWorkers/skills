---
name: twitter-automation
description: "通过 `inference.sh` CLI 自动化 Twitter/X 的发布、互动及用户管理功能。支持的命令包括：`x/post-tweet`（发布推文）、`x/post-create`（带媒体文件的发布）、`x/post-like`（点赞）、`x/post-retweet`（转发推文）、`x/dm-send`（发送私信）、`x/user-follow`（关注用户）。主要功能包括：发布推文、安排发布时间、点赞推文、转发推文、发送私信、关注用户以及获取用户信息。适用于：社交媒体自动化、内容调度、互动机器人、粉丝增长等场景。触发条件包括：Twitter API、`x` API、推文自动化、Twitter 机器人、社交媒体自动化等。"
allowed-tools: Bash(infsh *)
---
# Twitter/X 自动化

通过 [inference.sh](https://inference.sh) 命令行工具（CLI）实现 Twitter/X 的自动化操作。

![Twitter/X 自动化示例](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kgad3pxsh3z3hnfpjyjpx4x4.jpeg)

## 快速入门

```bash
# Install CLI
curl -fsSL https://cli.inference.sh | sh && infsh login

# Post a tweet
infsh app run x/post-tweet --input '{"text": "Hello from inference.sh!"}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可以手动进行安装和验证：[手动安装与验证](https://dist.inference.sh/cli/checksums.txt)。

## 可用应用

| 应用 | 应用 ID | 功能描述 |
|-----|--------|-------------|
| 发布推文 | `x/post-tweet` | 发布纯文本推文 |
| 创建推文 | `x/post-create` | 发布带图片的推文 |
| 点赞推文 | `x/post-like` | 点赞推文 |
| 转发推文 | `x/post-retweet` | 转发推文 |
| 删除推文 | `x/post-delete` | 删除推文 |
| 获取推文 | `x/post-get` | 通过 ID 获取推文 |
| 发送私信 | `x/dm-send` | 发送私信 |
| 关注用户 | `x/user-follow` | 关注用户 |
| 获取用户信息 | `x/user-get` | 获取用户资料 |

## 示例

### 发布推文

```bash
infsh app run x/post-tweet --input '{"text": "Just shipped a new feature! 🚀"}'
```

### 发布带图片的推文

```bash
infsh app sample x/post-create --save input.json

# Edit input.json:
# {
#   "text": "Check out this AI-generated image!",
#   "media_url": "https://your-image-url.jpg"
# }

infsh app run x/post-create --input input.json
```

### 点赞推文

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
npx skills add inference-sh/skills@inference-sh

# Image generation (create images to post)
npx skills add inference-sh/skills@ai-image-generation

# Video generation (create videos to post)
npx skills add inference-sh/skills@ai-video-generation

# AI avatars (create presenter videos)
npx skills add inference-sh/skills@ai-avatar-video
```

查看所有应用：`infsh app list`

## 文档资料

- [X.com 集成](https://inference.sh/docs/integrations/x) - 设置 Twitter/X 集成
- [X.com 集成示例](https://inference.sh/docs/examples/x-integration) - 完整的 Twitter 自动化工作流程
- [应用概览](https://inference.sh/docs/apps/overview) - 了解应用生态系统