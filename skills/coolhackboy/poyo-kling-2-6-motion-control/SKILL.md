---
name: poyo-kling-2-6-motion-control
description: Kling 2.6 的运动控制功能可以通过 `https://api.poyo.ai/api/generate/submit` 在 PoYo / poyo.ai 平台上实现。该功能可用于实现角色动画、方向控制以及 720p/1080p 视频输出。
metadata: {"openclaw": {"homepage": "https://docs.poyo.ai/api-manual/video-series/kling-2.6-motion-control", "requires": {"bins": ["curl"], "env": ["POYO_API_KEY"]}, "primaryEnv": "POYO_API_KEY"}}
---
# PoYo Kling 2.6 运动控制

此技能适用于在 PoYo 平台上使用 `kling-2.6-motion-control` 的任务。它专为需要同时使用角色图像和参考视频的精确运动传输工作流程而设计。

## 使用场景

- 用户明确请求使用 `Kling 2.6 Motion Control` 或 `kling-2.6-motion-control` 时。
- 需要将参考视频中的动作转移到目标角色图像上时。
- 工作流程依赖于 `character_orientation`（角色方向）和明确的分辨率控制。

## 核心功能

- `kling-2.6-motion-control` 并不是一个通用的视频处理模型。仅当任务需要从提供的图像中生成角色动画，并结合提供的动作视频时，才应使用该模型。

## 关键输入参数

- `image_urls`：必需参数，支持一张角色图像，图像中应清晰显示头部、肩膀和躯干。
- `video_urls`：必需参数，支持一个参考视频，视频时长必须在 3 到 30 秒之间。
- `character_orientation`：必需参数，支持 `image`（图像）或 `video`（视频）两种格式。
- `resolution`：必需参数，支持 `720p` 或 `1080p` 分辨率。
- `prompt`：可选参数，用于提供场景指导。

## 执行步骤

- 查阅 `references/api.md` 以获取端点详情、模型 ID、关键字段、示例数据格式以及轮询注意事项。
- 使用 `scripts/submit_kling_2_6_motion_control.sh` 从 shell 提交原始 JSON 数据。
- 如果用户只需要使用 curl 进行请求，可以直接参考 `references/api.md` 中的示例代码，无需重新编写。
- 提交请求后，请明确记录 `task_id`，以便后续进行状态查询。

## 输出结果

在处理此类模型时，应提供以下信息：
- 选择的模型 ID。
- 最终处理后的数据或参数摘要。
- 是否使用了参考图像。
- 如果请求已成功提交，应返回 `task_id`。
- 下一步操作：轮询任务状态或等待 Webhook 的响应。