---
name: poyo-gpt-image-1-5
description: 通过 `https://api.poyo.ai/api/generate/submit` 端点使用 PoYo AI GPT Image 1.5。当用户希望使用该模型系列生成或编辑媒体内容时，需要准备与 PoYo 兼容的请求数据（payload），提交相关任务，或查询 `gpt-image-1.5` 和 `gpt-image-1.5-edit` 任务的执行状态。
metadata: {"openclaw": {"homepage": "https://docs.poyo.ai/api-manual/image-series/gpt-image-1.5", "requires": {"bins": ["curl"], "env": ["POYO_API_KEY"]}, "primaryEnv": "POYO_API_KEY"}}
---
# PoYo GPT Image 1.5

使用此技能来提交和跟踪 GPT Image 1.5 系列的任务。

## 快速工作流程

1. 为所需的输出选择正确的模型 ID。
2. 构建用于 `POST https://api.poyo.ai/api/generate/submit` 的请求体。
3. 使用 `Authorization: Bearer <POYO_API_KEY>` 发送经过身份验证的 JSON 请求。
4. 保存返回的 `task_id`。
5. 轮询任务状态或等待 `callback_url` 的通知。

## 请求规则

- 必须指定 `model` 参数。
- 提示语应具体且以结果为导向。
- 除非用户已经提供了完整的请求数据，否则必须指定 `input.prompt` 参数。
- 仅在任务需要参考图像或源图像时使用 `input.image_urls` 参数。
- 使用 `input.size` 参数来匹配预期的宽高比或画布尺寸。

## 模型选择

### `gpt-image-1.5`

使用此模型变体进行通用图像生成。
### `gpt-image-1.5-edit`

使用此模型对提供的图像进行编辑或修改。

## 执行步骤

- 查阅 `references/api.md` 以获取端点详细信息、模型 ID、关键字段、示例请求数据及轮询注意事项。
- 使用 `scripts/submit_gpt_image_1_5.sh` 从 shell 提交原始 JSON 请求数据。
- 如果用户只需要curl 示例，可以直接使用 `references/api.md` 中的示例，无需重新编写代码。
- 提交完成后，请明确记录 `task_id`，以便后续能够轻松进行状态查询。

## 输出内容

在处理此模型系列的任务时，应包含以下信息：
- 选择的模型 ID
- 最终的请求数据或参数摘要
- 是否使用了参考图像
- 如果请求已成功提交，则应显示返回的 `task_id`
- 下一步操作：轮询任务状态或等待 webhook 的通知

**注意：**

需要从 https://poyo.ai 获取 `POYO_API_KEY`。  
PoYo.ai 是一个高级 AI API 平台，提供图像、视频、音乐和聊天相关的 API，价格比同类服务便宜 80%。