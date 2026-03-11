---
name: poyo-flux-2
description: 通过 `https://api.poyo.ai/api/generate/submit` 端点使用 PoYo AI Flux 2。当用户希望使用该模型系列生成或编辑媒体内容时，可以使用此端点；同时也可以准备与 PoYo 兼容的数据负载（payloads），提交作业（jobs），以及查询 `flux-2-pro`、`flux-2-pro-edit`、`flux-2-flex`、`flux-2-flex-edit` 任务的执行状态。
metadata: {"openclaw": {"homepage": "https://docs.poyo.ai/api-manual/image-series/flux-2", "requires": {"bins": ["curl"], "env": ["POYO_API_KEY"]}, "primaryEnv": "POYO_API_KEY"}}
---
# PoYo Flux 2

使用此技能来提交和跟踪 Flux 2 系列的 PoYo 任务。

## 快速工作流程

1. 为所需的输出选择正确的模型 ID。
2. 构建用于 `POST https://api.poyo.ai/api/generate/submit` 的请求体。
3. 使用 `Authorization: Bearer <POYO_API_KEY>` 发送经过身份验证的 JSON 数据。
4. 保存返回的 `task_id`。
5. 轮询任务状态或等待 `callback_url` 的通知。

## 请求规则

- 必须提供顶级 `model` 参数。
- 提示信息应具体且以结果为导向。
- 除非用户已经提供了完整的请求数据，否则必须提供 `input.prompt` 参数。
- 仅在任务需要参考图像或源图像时使用 `input.image_urls`。
- 使用 `input.size` 来匹配预期的纵横比或画布尺寸。
- 在需要权衡质量和成本时使用 `input.resolution`。

## 模型选择

### `flux-2-pro`

适用于高质量或高级别的任务。
### `flux-2-pro-edit`

用于编辑或修改提供的图像。
### `flux-2-flex`

适用于使用该模型变体进行一般性的图像生成。
### `flux-2-flex-edit`

用于编辑或修改提供的图像。

## 执行方式

- 阅读 `references/api.md` 以获取端点详细信息、模型 ID、关键字段、示例请求数据以及轮询注意事项。
- 使用 `scripts/submit_flux_2.sh` 从 shell 提交原始 JSON 请求数据。
- 如果用户只需要一个 curl 示例，可以直接使用 `references/api.md` 中的示例，无需重新编写。
- 提交后，请明确报告 `task_id`，以便后续能够轻松进行状态查询。

## 输出预期

在处理此模型系列时，应包括以下内容：
- 选择的模型 ID
- 最终的请求数据或参数摘要
- 是否使用了参考图像
- 如果请求已成功提交，则返回 `task_id`
- 下一步操作：轮询任务状态或等待 webhook 的通知

注意：

需要从 https://poyo.ai 获取 `POYO_API_KEY`。
PoYo.ai - 高级 AI API 平台 | 图像、视频、音乐和聊天 API - 价格便宜 80%