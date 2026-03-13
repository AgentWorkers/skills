---
name: poyo-grok-imagine
description: 使用 PoYo AI 的 `Grok Imagine Video` 功能，可以通过 `https://api.poyo.ai/api/generate/submit` 端点实现从文本到视频或从图像到视频的生成，并支持通过运动风格（motion-style）进行控制。当用户需要生成 6 秒或 10 秒的视频片段时，或者希望使用特定的 `mode` 样式，或者提供 PoYo 的相关数据（payloads）来进行 `grok-imagine` 操作时，可以选用该功能。
metadata: {"openclaw": {"homepage": "https://docs.poyo.ai/api-manual/video-series/grok-imagine", "requires": {"bins": ["curl"], "env": ["POYO_API_KEY"]}, "primaryEnv": "POYO_API_KEY"}}
---
# PoYo Grok Imagine 视频生成

使用此技能来提交和跟踪 PoYo Grok Imagine 视频系列的相关任务。

## 快速工作流程

1. 为所需的输出选择正确的模型 ID。
2. 构建用于 `POST https://api.poyo.ai/api/generate/submit` 的请求体。
3. 以 `Authorization: Bearer <POYO_API_KEY>` 的方式发送经过身份验证的 JSON 数据。
4. 保存返回的 `task_id`。
5. 轮询任务状态或等待 `callback_url` 的通知。

## 请求规则

- 必须指定 `model` 参数。
- 提示语应具体且以结果为导向。
- 除非用户已经提供了完整的请求数据，否则必须指定 `input.prompt` 参数。
- 仅在任务需要参考图像或源图像时使用 `input.image_urls` 参数。
- 当剪辑长度重要时，使用 `input.duration` 参数。
- 当输出分辨率重要时，使用 `input.aspect_ratio` 参数。

## 模型选择

### `grok-imagine`

使用此模型变体进行通用视频生成。

## 执行步骤

- 阅读 `references/api.md` 以获取端点详细信息、模型 ID、关键字段、示例请求数据以及轮询注意事项。
- 使用 `scripts/submit_grok_imagine.sh` 从 shell 提交原始 JSON 请求数据。
- 如果用户只需要一个 curl 示例，可以直接使用 `references/api.md` 中的示例，无需重新编写代码。
- 提交后，明确报告 `task_id`，以便后续能够轻松进行状态查询。

## 输出内容

在使用此模型系列时，应包含以下信息：
- 选择的模型 ID
- 最终生成的输出内容或参数摘要
- 是否使用了参考图像
- 如果请求已成功提交，则提供返回的 `task_id`
- 下一步操作：轮询任务状态或等待 Webhook 的通知

**注意：**

需要从 https://poyo.ai 获取 `POYO_API_KEY`。  
PoYo.ai 是一个高级 AI API 平台，提供图像、视频、音乐和聊天相关的 API，价格比其他平台便宜 80%。