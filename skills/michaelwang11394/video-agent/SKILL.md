---
name: heygen
description: >
  HeyGen AI 视频创建 API 的使用场景包括：  
  1. 使用 Video Agent 进行一次性提示到视频的生成；  
  2. 通过 `/v2/video/generate` 生成 AI 虚拟形象视频；  
  3. 操作 HeyGen 提供的虚拟形象、语音、背景或字幕功能；  
  4. 创建透明格式的 WebM 视频以用于后期合成；  
  5. 查询视频生成状态或处理 Webhook 事件；  
  6. 将 HeyGen 与 Remotion 结合以实现程序化视频处理；  
  7. 翻译或为现有视频添加字幕；  
  8. 通过 `/v1/audio` 使用 Starfish 模型生成独立的 TTS（文本转语音）音频文件。
homepage: https://docs.heygen.com/reference/generate-video-agent
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---
# HeyGen API

这是一个用于生成AI头像视频的API，能够创建带语音的讲解视频和演示文稿。

## 默认工作流程

对于大多数视频请求，建议使用**Video Agent API**（`POST /v1/video_agent/generate`）。在编写提示时，请务必遵循 [prompt-optimizer.md](references/prompt-optimizer.md) 中提供的指南，确保提示中包含场景、时间安排和视觉风格等信息。

仅在用户有以下明确需求时，才使用 v2/video/generate：
- 需要未经AI修改的精确脚本
- 需要指定特定的 `voice_id`
- 每个场景需要使用不同的头像或背景
- 需要对每个场景的时间进行精确控制
- 需要按照具体要求进行程序化或批量生成视频

## 快速参考

| 任务 | 参考文档 |
|------|------|
| 根据提示生成视频（简单） | [prompt-optimizer.md](references/prompt-optimizer.md) → [video-agent.md](references/video-agent.md) |
| 具有精确控制的视频生成 | [video-generation.md](references/video-generation.md), [avatars.md](references/avatars.md), [voices.md](references/voices.md) |
| 查看视频状态/获取下载链接 | [video-status.md](references/video-status.md) |
| 添加字幕或文本叠加层 | [captions.md](references/captions.md), [text-overlays.md](references/text-overlays.md) |
| 用于视频合成的透明视频 | [video-generation.md](references/video-generation.md)（WebM格式部分） |
| 生成独立的TTS音频 | [text-to-speech.md](references/text-to-speech.md) |
| 翻译/为现有视频添加配音 | [video-translation.md](references/video-translation.md) |
| 与Remotion集成使用 | [remotion-integration.md](references/remotion-integration.md) |

## 参考文件

### 基础知识
- [references/authentication.md](references/authentication.md) - API密钥设置及X-Api-Key头信息
- [references/quota.md](references/quota.md) - 信用系统和使用限制
- [references/video-status.md](references/video-status.md) - 视频状态查询及下载链接获取
- [references/assets.md](references/assets.md) - 图片、视频和音频的上传

### 核心视频制作功能
- [references/avatars.md](references/avatars.md) - 头像列表、样式选择及头像ID管理
- [references/voices.md](references/voices.md) - 语音列表、语言设置及音速/音调调整
- [references/scripts.md](references/scripts.md) - 脚本编写、暂停设置及播放节奏控制
- [references/video-generation.md](references/video-generation.md) - 使用 `POST /v2/video/generate` 功能生成多场景视频
- [references/video-agent.md](references/video-agent.md) - 一次性生成视频的功能
- [references/prompt-optimizer.md](references/prompt-optimizer.md) - 如何编写有效的视频生成提示
- [references/dimensions.md](references/dimensions.md) - 视频分辨率和宽高比设置

### 视频定制功能
- [references/backgrounds.md](references/backgrounds.md) - 单色背景、图片背景或视频背景的设置
- [references/text-overlays.md](references/text-overlays.md) - 添加文本、设置字体和位置
- [references/captions.md](references/captions.md) - 自动生成的字幕和标题

### 高级功能
- [references/templates.md](references/templates.md) - 模板列表及变量替换功能
- [references/video-translation.md](references/video-translation.md) - 视频翻译和配音功能
- [references/text-to-speech.md](references/text-to-speech.md) - 使用Starfish模型生成独立TTS音频
- [references/photo-avatars.md](references/photo-avatars.md) - 从照片创建头像
- [references/webhooks.md](references/webhooks.md) - Webhook端点及事件通知

### 集成功能
- [references/remotion-integration.md](references/remotion-integration.md) - 如何在Remotion中集成使用HeyGen API