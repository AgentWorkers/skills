---
name: heygen
description: >
  HeyGen AI 视频创建 API。适用场景包括：  
  1. 使用 Video Agent 进行一次性提示到视频的生成；  
  2. 通过 `/v2/video/generate` 生成 AI 阿바타视频；  
  3. 使用 HeyGen 的阿바타、语音、背景或字幕；  
  4. 创建用于合成的透明 WebM 视频；  
  5. 查询视频状态或处理 Webhook；  
  6. 将 HeyGen 与 Remotion 集成以实现程序化视频处理；  
  7. 翻译或为现有视频添加字幕；  
  8. 通过 `/v1/audio` 使用 Starfish 模型生成独立的 TTS（文本转语音）音频。
homepage: https://docs.heygen.com/reference/generate-video-agent
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---
# HeyGen API

这是一个用于生成AI头像视频、讲解视频和演示文稿的API。

## 工具选择

如果可以使用HeyGen的MCP工具（`mcp__heygen__*`），**建议优先使用它们**，因为它们可以自动处理身份验证和请求格式化。

| 任务 | MCP工具 | 备选方案（直接API） |
|------|----------|----------------------|
| 根据提示生成视频 | `mcp__heygen__generate_video_agent` | `POST /v1/video_agent/generate` |
| 检查视频状态/获取下载链接 | `mcp__heygen__get_video` | `GET /v1/video_status.get` |
| 列出账户中的视频 | `mcp__heygen__list_videos` | `GET /v1/video.list` |
| 生成TTS音频 | `mcp__heygen__text_to_speech` | `POST /v1/audio/text_to_speech` |
| 列出TTS语音 | `mcp__heygen__list_audio_voices` | `GET /v1/audio/voices` |
| 删除视频 | `mcp__heygen__delete_video` | `DELETE /v1/video.delete` |

如果无法使用HeyGen的MCP工具，请按照参考文件中的说明，使用带有`X-Api-Key: $HEYGEN_API_KEY`头部的直接HTTP API调用。

## 默认工作流程

对于大多数视频请求，**建议使用Video Agent**。  
在编写提示时，请始终遵循[prompt-optimizer.md](references/prompt-optimizer.md)中的指南，确保提示包含场景、时间和视觉风格。

**使用MCP工具时：**
1. 使用[prompt-optimizer.md](references/prompt-optimizer.md)和[visual-styles.md]生成优化后的提示。
2. 调用`mcp__heygen__generate_video_agent`，并提供提示以及相关配置（如持续时间、方向、头像ID）。
3. 使用返回的视频ID调用`mcp__heygen__get_video`来获取视频状态和下载链接。

**不使用MCP工具（直接API时：**
1. 使用[prompt-optimizer.md]和[visual-styles.md]生成优化后的提示。
2. 发送`POST`请求到`/v1/video_agent/generate`（详情请参阅[video-agent.md]）。
3. 发送`GET`请求到`/v1/video_status.get?video_id=<id>`（详情请参阅[video-status.md]）。

只有在以下情况下才使用`v2/video/generate`：
- 需要未经AI修改的原始脚本。
- 需要指定特定的语音ID。
- 每个场景需要不同的头像或背景。
- 需要对每个场景进行精确的时间控制。
- 需要按照具体要求进行程序化或批量生成视频。

## 快速参考

| 任务 | MCP工具 | 需要参考的文档 |
|------|----------|------|
| 根据提示生成视频（简单流程） | `mcp__heygen__generate_video_agent` | [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md] → [video-agent.md] |
| 需要精确控制的视频生成 | — | [video-generation.md](references/video-generation.md), [avatars.md](references/avatars.md), [voices.md](references/voices.md) |
| 检查视频状态/获取下载链接 | `mcp__heygen__get_video` | [video-status.md](references/video-status.md) |
| 添加字幕或文本覆盖层 | — | [captions.md](references/captions.md), [text-overlays.md](references/text-overlays.md) |
| 用于合成的透明视频 | — | [video-generation.md](references/video-generation.md)（WebM相关部分） |
| 生成独立的TTS音频 | `mcp__heygen__text_to_speech` | [text-to-speech.md](references/text-to-speech.md) |
| 列出TTS语音 | `mcp__heygen__list_audio_voices` | [voices.md](references/voices.md) |
| 翻译/为现有视频添加配音 | — | [video-translation.md](references/video-translation.md) |
| 与Remotion集成 | — | [remotion-integration.md](references/remotion-integration.md) |

## 参考文件

### 基础知识
- [references/authentication.md](references/authentication.md) - API密钥设置和X-Api-Key头部
- [references/quota.md](references/quota.md) - 信用系统和使用限制
- [references/video-status.md](references/video-status.md) - 查询视频状态和下载链接
- [references/assets.md](references/assets.md) - 上传图片、视频和音频文件

### 核心视频生成功能
- [references/avatars.md](references/avatars.md) - 列出头像、选择头像样式
- [references/voices.md](references/voices.md) - 列出可用语音、设置语音参数（速度、音调）
- [references/scripts.md](references/scripts.md) - 编写脚本、设置暂停和节奏
- [references/video-generation.md](references/video-generation.md) - 使用`v2/video/generate`接口生成多场景视频
- [references/video-agent.md](references/video-agent.md) - 一次性生成视频
- [references/prompt-optimizer.md](references/prompt-optimizer.md) - 编写有效的视频生成提示（核心工作流程和规则）
- [references/visual-styles.md](references/visual-styles.md) - 提供20种预定义的视觉样式及其详细规格
- [references/prompt-examples.md](references/prompt-examples.md) - 完整的提示示例及可使用的模板
- [references/dimensions.md](references/dimensions.md) - 视频分辨率和宽高比

### 视频自定义功能
- [references/backgrounds.md](references/backgrounds.md) - 设置视频背景（纯色、图片）
- [references/text-overlays.md](references/text-overlays.md) - 添加文本和调整文本位置
- [references/captions.md](references/captions.md) - 自动生成字幕

### 高级功能
- [references/templates.md](references/templates.md) - 模板列表和变量替换功能
- [references/video-translation.md](references/video-translation.md) - 视频翻译和配音
- [references/text-to-speech.md](references/text-to-speech.md) - 使用Starfish模型生成独立TTS音频
- [references/photo-avatars.md](references/photo-avatars.md) - 从照片创建头像
- [references/webhooks.md](references/webhooks.md) - Webhook接口和事件触发

### 集成
- [references/remotion-integration.md](references/remotion-integration.md) - 在Remotion软件中集成HeyGen功能