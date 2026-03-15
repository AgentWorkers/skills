---
name: heygen
description: [已弃用] 如需基于提示生成视频，请使用 `create-video`；如需精确控制头像或场景，请使用 `avatar-video`。此旧技能结合了这两种工作流程——较新的专用技能提供了更清晰的指导。
homepage: https://docs.heygen.com/reference/generate-video-agent
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---
# HeyGen API（已弃用）

> **此功能已弃用。** 请改用以下功能：  
> - **`create-video`** — 根据文本提示生成视频（Video Agent API）  
> - **`avatar-video`** — 使用特定头像、语音、脚本和场景构建视频（v2 API）  

该功能仅保留以支持向后兼容性，将在未来的版本中移除。

---

**HeyGen** 是一个用于生成带语音讲解的视频、演示文稿等的 AI 平台。  

## 工具选择  

如果可以使用 HeyGen 的 MCP 工具（格式为 `mcp__heygen__*`），**建议优先使用它们**，因为它们可以自动处理身份验证和请求格式化：  

| 任务 | MCP 工具 | 备选方案（直接使用 API） |  
|------|----------|----------------------|  
| 根据提示生成视频 | `mcp__heygen__generate_video_agent` | `POST /v1/video_agent/generate` |  
| 检查视频状态/获取下载链接 | `mcp__heygen__get_video` | `GET /v2/videos/{video_id}` |  
| 列出账户中的视频 | `mcp__heygen__list_videos` | `GET /v2/videos` |  
| 删除视频 | `mcp__heygen__delete_video` | `DELETE /v2/videos/{video_id}` |  

如果无法使用 HeyGen 的 MCP 工具，请按照参考文件中的说明，直接使用 HTTP API，并在请求头中添加 `X-Api-Key: $HEYGEN_API_KEY`。  

## 默认工作流程  

**大多数视频请求建议使用 Video Agent：**  
始终参考 [prompt-optimizer.md](references/prompt-optimizer.md) 中的指南来构建包含场景、时间和视觉风格的提示。  

**使用 MCP 工具时：**  
1. 使用 [prompt-optimizer.md](references/prompt-optimizer.md) 和 [visual-styles.md](references/visual-styles.md) 编写优化后的提示内容。  
2. 调用 `mcp__heygen__generate_video_agent` 并传入提示内容及配置参数（如持续时间、方向、头像 ID）。  
3. 使用返回的 `video_id` 调用 `mcp__heygen__get_video` 来获取视频状态和下载链接。  

**不使用 MCP 工具（直接使用 API）时：**  
1. 使用 [prompt-optimizer.md](references/prompt-optimizer.md) 和 [visual-styles.md] 编写优化后的提示内容。  
2. 执行 `POST /v1/video_agent/generate`（详情请参阅 [video-agent.md](references/video-agent.md)。  
3. 执行 `GET /v2/videos/{id}`（详情请参阅 [video-status.md]）。  

**仅在以下情况下使用 v2/video/generate：**  
- 需要未经 AI 修改的原始脚本；  
- 需要指定特定的语音 ID；  
- 每个场景需要不同的头像或背景；  
- 需要对每个场景进行精确的时间控制；  
- 需要按程序或批量生成视频，并且有明确的规格要求。  

## 快速参考  

| 任务 | MCP 工具 | 参考文档 |  
|------|----------|------|  
| 根据提示生成视频（简单流程） | `mcp__heygen__generate_video_agent` | [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md](references/visual-styles.md) → [video-agent.md](references/video-agent.md) |  
| 具有精确控制的视频生成 | — | [video-generation.md](references/video-generation.md), [avatars.md](references/avatars.md), [voices.md](references/voices.md) |  
| 检查视频状态/获取下载链接 | `mcp__heygen__get_video` | [video-status.md](references/video-status.md) |  
| 添加字幕或文本叠加层 | — | [captions.md](references/captions.md), [text-overlays.md](references/text-overlays.md) |  
| 用于合成操作的透明视频 | — | [video-generation.md](references/video-generation.md)（WebM 格式） |  
| 与 Remotion 工具集成 | — | [remotion-integration.md](references/remotion-integration.md) |  

## 参考文件  

### 基础知识  
- [references/authentication.md](references/authentication.md) — API 密钥设置和 `X-Api-Key` 头部信息  
- [references/quota.md](references/quota.md) — 信用系统和使用限制  
- [references/video-status.md](references/video-status.md) — 请求状态检查和下载链接获取方法  
- [references/assets.md](references/assets.md) — 图像、视频和音频的上传方法  

### 核心视频生成功能  
- [references/avatars.md](references/avatars.md) — 头像列表、样式选择及头像 ID 的使用  
- [references/voices.md](references/voices.md) — 语音列表、语言设置及音速调整  
- [references/scripts.md](references/scripts.md) — 脚本编写、暂停设置及播放节奏控制  
- [references/video-generation.md](references/video-generation.md) — 使用 `/v2/video/generate` 功能生成多场景视频  
- [references/video-agent.md](references/video-agent.md) — 一次性生成视频的功能  
- [references/prompt-optimizer.md](references/prompt-optimizer.md) — 有效的 Video Agent 提示编写方法  
- [references/visual-styles.md](references/visual-styles.md) — 20 种预定义的视觉样式及详细规格  
- [references/prompt-examples.md](references/prompt-examples.md) — 完整的提示示例及现成的模板  
- [references/dimensions.md](references/dimensions.md) — 视频分辨率和宽高比设置  

### 视频自定义功能  
- [references/backgrounds.md](references/backgrounds.md) — 固定颜色、图片或视频背景的设置  
- [references/text-overlays.md](references/text-overlays.md) — 添加带有字体和定位效果的文本  
- [references/captions.md](references/captions.md) — 自动生成的字幕和标题  

### 高级功能  
- [references/templates.md](references/templates.md) — 模板列表及变量替换功能  
- [references/photo-avatars.md](references/photo-avatars.md) — 从照片创建头像  
- [references/webhooks.md](references/webhooks.md) — Webhook 终端和事件触发机制  

### 集成说明  
- [references/remotion-integration.md](references/remotion-integration.md) — 如何在 Remotion 组件中集成 HeyGen 功能