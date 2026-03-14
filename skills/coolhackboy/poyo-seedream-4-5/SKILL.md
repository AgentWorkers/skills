---
name: poyo-seedream-4-5
description: 在 PoYo / poyo.ai 上，可以通过 `https://api.poyo.ai/api/generate/submit` 来生成和编辑 Seedream 4.5 图像。该功能支持 `seedream-4.5` 和 `seedream-4.5-edit` 命令，能够生成 2K/4K 分辨率的图像，并支持多参考图像的编辑以及处理更多图像数据。
metadata: {"openclaw": {"homepage": "https://docs.poyo.ai/api-manual/image-series/seedream-4-5", "requires": {"bins": ["curl"], "env": ["POYO_API_KEY"]}, "primaryEnv": "POYO_API_KEY"}}
---
# PoYo Seedream 4.5 图像生成与编辑

此技能适用于在 PoYo 上使用 Seedream 4.5 进行的相关任务，支持高分辨率图像生成、多参考图像处理以及图像编辑功能。

## 使用场景

- 当用户明确请求使用 `Seedream 4.5`、`seedream-4.5` 或 `seedream-4.5-edit` 时；
- 任务涉及高分辨率图像生成、图像转换或图像编辑；
- 工作流程需要使用多张参考图像或生成大量输出图像时。

## 模型选择

- `seedream-4.5`：标准图像生成入口点；
- `seedream-4.5-edit`：用于处理需要对提供的图像进行编辑的请求。

## 关键输入参数

- 必须提供 `prompt`（提示信息）；
- `image_urls` 参数最多可接受 10 张图像的 URL，且在 `seedream-4.5-edit` 请求中为必填项；
- `size` 可以是分辨率（如 `2K`/`4K`）或宽高比（如 `1:1`、`16:9`、`21:9`）；
- `n` 用于指定输出图像的数量（范围为 1 到 15）。

## 执行步骤

- 查阅 `references/api.md` 以获取端点详情、模型 ID、关键字段、示例数据格式以及轮询相关说明；
- 使用 `scripts/submit_seedream_4_5.sh` 命令从 shell 提交原始 JSON 数据；
- 如果用户只需要使用 curl 进行请求，可以直接参考 `references/api.md` 中的示例代码，无需重新编写；
- 提交请求后，务必明确记录 `task_id`，以便后续进行状态查询。

## 输出结果

在处理该模型系列的任务时，应提供以下信息：

- 选择的模型 ID；
- 最终生成的图像数据或参数摘要；
- 是否使用了参考图像；
- 如果请求已成功提交，应显示返回的 `task_id`；
- 下一步操作：继续轮询任务状态或等待 Webhook 的响应。