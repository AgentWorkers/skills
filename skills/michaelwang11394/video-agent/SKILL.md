---
name: video-agent
description: |
  HeyGen AI video creation API. Use when: (1) Using Video Agent for one-shot prompt-to-video generation, (2) Generating AI avatar videos with /v2/video/generate, (3) Working with HeyGen avatars, voices, backgrounds, or captions, (4) Creating transparent WebM videos for compositing, (5) Polling video status or handling webhooks, (6) Integrating HeyGen with Remotion for programmatic video, (7) Translating or dubbing existing videos.
homepage: https://docs.heygen.com/reference/generate-video-agent
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "bins": ["python3", "curl"], "env": ["HEYGEN_API_KEY"] },
        "primaryEnv": "HEYGEN_API_KEY",
      },
  }
---

# HeyGen API

这是一个用于生成AI头像视频的API，能够制作带语音的讲解视频和演示文稿。

## 默认工作流程

对于大多数视频请求，建议使用**Video Agent API**（`POST /v1/video_agent/generate`）。在编写提示语时，请务必遵循[prompt-optimizer.md](references/prompt-optimizer.md)中的指南，确保包含场景、时间安排和视觉风格等信息。

仅在以下情况下使用v2/video/generate：
- 需要未经AI修改的精确脚本；
- 需要指定特定的`voice_id`；
- 每个场景需要使用不同的头像或背景；
- 需要对每个场景的时间进行精确控制；
- 需要按照具体要求进行程序化或批量生成视频。

## 快速参考

| 任务 | 参考文档 |
|------|------|
| 根据提示生成视频（简单） | [prompt-optimizer.md](references/prompt-optimizer.md) → [video-agent.md](references/video-agent.md) |
| 具有精确控制的视频生成 | [video-generation.md](references/video-generation.md), [avatars.md](references/avatars.md), [voices.md](references/voices.md) |
| 检查视频状态/获取下载链接 | [video-status.md](references/video-status.md) |
| 添加字幕或文本叠加层 | [captions.md](references/captions.md), [text-overlays.md](references/text-overlays.md) |
| 用于视频合成的透明视频 | [video-generation.md](references/video-generation.md)（WebM部分） |
| 实时交互式头像 | [streaming-avatars.md](references/streaming-avatars.md) |
| 翻译/为现有视频添加配音 | [video-translation.md](references/video-translation.md) |
| 与Remotion集成使用 | [remotion-integration.md](references/remotion-integration.md) |

## 参考文件

### 基础知识
- [references/authentication.md](references/authentication.md) - API密钥设置和X-Api-Key头部信息
- [references/quota.md](references/quota.md) - 信用系统和使用限制
- [references/video-status.md](references/video-status.md) - 查询视频状态和下载链接的方法
- [references/assets.md](references/assets.md) - 上传图片、视频和音频文件

### 核心视频制作功能
- [references/avatars.md](references/avatars.md) - 头像列表、样式选择及头像ID的获取
- [references/voices.md](references/voices.md) - 语音列表、语言设置及音速/音调调整
- [references/scripts.md](references/scripts.md) - 脚本编写、暂停设置及播放节奏控制
- [references/video-generation.md](references/video-generation.md) - 使用`POST /v2/video/generate`生成多场景视频
- [references/video-agent.md](references/video-agent.md) - 一次性生成视频
- [references/prompt-optimizer.md](references/prompt-optimizer.md) - 编写有效的视频提示语
- [references/dimensions.md](references/dimensions.md) - 视频分辨率和宽高比设置

### 视频自定义功能
- [references/backgrounds.md](references/backgrounds.md) - 单色背景、图片背景或视频背景的设置
- [references/text-overlays.md](references/text-overlays.md) - 添加文本并设置字体和位置
- [references/captions.md](references/captions.md) - 自动生成字幕和 subtitles

### 高级功能
- [references/templates.md](references/templates.md) - 模板列表及变量替换功能
- [references/video-translation.md](references/video-translation.md) - 视频翻译和配音服务
- [references/streaming-avatars.md](references/streaming-avatars.md) - 实时交互式头像功能
- [references/photo-avatars.md](references/photo-avatars.md) - 从照片创建头像
- [references/webhooks.md](references/webhooks.md) - Webhook端点和事件通知

### 集成说明
- [references/remotion-integration.md](references/remotion-integration.md) - 如何在Remotion中集成使用HeyGen API