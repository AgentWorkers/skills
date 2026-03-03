---
name: heygen
description: >
  HeyGen AI 视频创建 API。适用场景包括：  
  (1) 使用 Video Agent 进行一次性提示到视频的生成；  
  (2) 通过 /v2/video/generate 功能生成 AI 虚拟形象视频；  
  (3) 操作 HeyGen 提供的虚拟形象、语音、背景或字幕；  
  (4) 创建透明格式的 WebM 视频以用于合成；  
  (5) 查询视频状态或处理 Webhook 事件；  
  (6) 将 HeyGen 与 Remotion 结合以实现程序化视频处理；  
  (7) 从图片生成照片虚拟形象。
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

这是一个用于生成带语音的头像视频、讲解视频以及演示文稿的AI头像视频创建API。

## 工具选择

如果可以使用HeyGen的MCP工具（`mcp__heygen__*`），**建议优先使用它们**，因为它们可以自动处理身份验证和请求格式化：

| 任务 | MCP工具 | 备选方案（直接API调用） |
|------|----------|----------------------|
| 根据提示生成视频 | `mcp__heygen__generate_video_agent` | `POST /v1/video_agent/generate` |
| 检查视频状态/获取下载链接 | `mcp__heygen__get_video` | `GET /v1/video_status.get` |
| 列出账户中的视频 | `mcp__heygen__list_videos` | `GET /v1/video.list` |
| 删除视频 | `mcp__heygen__delete_video` | `DELETE /v1/video.delete` |

如果无法使用HeyGen的MCP工具，请按照参考文件中的说明，使用带有`X-Api-Key: $HEYGEN_API_KEY`头的直接HTTP API调用。

## 默认工作流程

对于大多数视频请求，**建议使用视频生成工具（Video Agent）**。在编写提示时，请务必遵循[prompt-optimizer.md](references/prompt-optimizer.md)中的指南，确保提示包含场景、时间安排和视觉风格。

**使用MCP工具时：**
1. 使用[prompt-optimizer.md](references/prompt-optimizer.md)和[visual-styles.md]生成优化后的提示。
2. 调用`mcp__heygen__generate_video_agent`，传入提示和配置参数（如持续时间、方向、头像ID）。
3. 使用返回的视频ID调用`mcp__heygen__get_video`来获取视频状态和下载链接。

**不使用MCP工具（直接API调用时：**
1. 使用[prompt-optimizer.md]和[visual-styles.md]生成优化后的提示。
2. 发送`POST`请求到`/v1/video_agent/generate`（详细说明请参见[video-agent.md]）。
3. 发送`GET`请求到`/v1/video_status.get?video_id=<id>`（详细说明请参见[video-status.md]）。

只有在以下情况下才使用`v2/video/generate`接口：
- 需要未经AI修改的原始脚本。
- 需要指定特定的语音ID。
- 每个场景需要使用不同的头像或背景。
- 需要对每个场景的时间进行精确控制。
- 需要按程序化方式或批量生成视频，并且有具体的要求。

## 快速参考

| 任务 | MCP工具 | 参考文档 |
|------|----------|------|
| 根据提示生成视频（简单流程） | `mcp__heygen__generate_video_agent` | [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md] → [video-agent.md] |
| 需要精确控制的视频生成 | — | [video-generation.md](references/video-generation.md), [avatars.md](references/avatars.md), [voices.md](references/voices.md) |
| 检查视频状态/获取下载链接 | `mcp__heygen__get_video` | [video-status.md](references/video-status.md) |
| 添加字幕或文本覆盖层 | — | [captions.md](references/captions.md), [text-overlays.md](references/text-overlays.md) |
| 用于合成的透明视频 | — | [video-generation.md](references/video-generation.md)（WebM格式相关内容） |
| 与Remotion集成 | — | [remotion-integration.md](references/remotion-integration.md) |

## 参考文件

### 基础知识
- [references/authentication.md](references/authentication.md) - API密钥设置和`X-Api-Key`头部的使用方法
- [references/quota.md](references/quota.md) - 信用系统和使用限制
- [references/video-status.md](references/video-status.md) - 视频状态查询和下载链接的获取方法
- [references/assets.md](references/assets.md) - 图像、视频和音频的上传方法

### 核心视频创建功能
- [references/avatars.md](references/avatars.md) - 头像列表、样式选择及头像ID的获取
- [references/voices.md](references/voices.md) - 语音列表、语言设置及音速调整
- [references/scripts.md](references/scripts.md) - 脚本编写、暂停设置及节奏控制
- [references/video-generation.md](references/video-generation.md) - 使用`/v2/video/generate`接口生成多场景视频
- [references/video-agent.md](references/video-agent.md) - 一次性生成视频的功能
- [references/prompt-optimizer.md](references/prompt-optimizer.md) - 有效的视频生成提示编写方法（核心工作流程及规则）
- [references/visual-styles.md](references/visual-styles.md) - 20种预定义的视觉风格及详细规格
- [references/prompt-examples.md](references/prompt-examples.md) - 完整的提示示例及可复用的模板
- [references/dimensions.md](references/dimensions.md) - 视频分辨率和宽高比设置

### 视频自定义功能
- [references/backgrounds.md](references/backgrounds.md) - 单色背景、图片背景的设置
- [references/text-overlays.md](references/text-overlays.md) - 添加文本及文本位置的设置
- [references/captions.md](references/captions.md) - 自动生成的字幕功能

### 高级功能
- [references/templates.md](references/templates.md) - 模板列表及变量替换功能
- [references/photo-avatars.md](references/photo-avatars.md) - 从照片创建头像的功能
- [references/webhooks.md](references/webhooks.md) - Webhook端点和事件触发机制

### 集成
- [references/remotion-integration.md](references/remotion-integration.md) - 如何在Remotion软件中集成HeyGen功能