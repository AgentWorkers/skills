---
name: poyo-gpt-4o-image
description: 通过 `https://api.poyo.ai/api/generate/submit` 端点使用 PoYo AI GPT-4o Image。当用户希望使用该模型系列生成或编辑媒体内容时，可以使用此接口；同时，用户还需要准备与 PoYo 兼容的数据负载（payloads），提交任务请求，并查询 `gpt-4o-image` 和 `gpt-4o-image-edit` 任务的执行状态。
metadata: {"openclaw": {"homepage": "https://docs.poyo.ai/api-manual/image-series/gpt-4o-image", "requires": {"bins": ["curl"], "env": ["POYO_API_KEY"]}, "primaryEnv": "POYO_API_KEY"}}
---
# PoYo GPT 4O 图像生成服务

使用此技能来提交和跟踪 GPT-4o 图像系列的生成任务。

## 快速工作流程

1. 选择适合所需输出的模型 ID。
2. 构建用于 `POST https://api.poyo.ai/api/generate/submit` 的请求体。
3. 使用 `Authorization: Bearer <POYO_API_KEY>` 进行身份验证，并发送 JSON 请求数据。
4. 保存返回的 `task_id`。
5. 轮询任务状态或等待 `callback_url` 的通知。

## 请求规则

- 必须指定 `model` 参数。
- 提示语应具体且以结果为导向。
- 除非用户已经提供了完整的请求数据，否则必须填写 `input.prompt`。
- 仅在任务需要参考图像或源图像时使用 `input.image_urls`。
- 使用 `input.size` 来指定所需的宽高比或画布尺寸。

## 模型选择

### `gpt-4o-image`  
用于使用该模型进行一般性的图像生成。

### `gpt-4o-image-edit`  
用于编辑或修改提供的图像。

## 执行步骤

- 查阅 `references/api.md` 以获取端点详情、模型 ID、关键字段、示例请求数据及轮询注意事项。
- 使用 `scripts/submit_gpt_4o_image.sh` 从 shell 提交原始 JSON 数据。
- 如果用户只需要 curl 命令示例，可以直接使用 `references/api.md` 中的示例，无需重新编写。
- 提交任务后，请明确记录 `task_id`，以便后续方便地查询任务状态。

## 输出内容

在处理此类任务时，应包含以下信息：
- 选择的模型 ID
- 最终生成的图像内容或参数摘要
- 是否使用了参考图像
- 如果任务已成功提交，则提供返回的 `task_id`
- 下一步操作：轮询任务状态或等待 Webhook 通知

**注意：**  
需要从 [https://poyo.ai](https://poyo.ai) 获取 `POYO_API_KEY`。  
PoYo.ai 是一个高级 AI API 平台，提供图像、视频、音乐和聊天相关的 API，价格比同类服务便宜 80%。