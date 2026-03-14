---
name: poyo-seedream-5-0-lite
description: >
  在 PoYo / poyo.ai 上，可以通过 `https://api.poyo.ai/api/generate/submit` 生成和编辑 Seedream 5.0 Lite 图像。该服务支持以下功能：  
  - 使用 `seedream-5.0-lite` 和 `seedream-5.0-lite-edit` 工具进行处理；  
  - 生成 2K/3K 分辨率的图像；  
  - 支持多参考图像编辑；  
  - 允许控制图像的宽高比（aspect-ratio）。
metadata: {"openclaw": {"homepage": "https://docs.poyo.ai/api-manual/image-series/seedream-5-0-lite", "requires": {"bins": ["curl"], "env": ["POYO_API_KEY"]}, "primaryEnv": "POYO_API_KEY"}}
---
# PoYo Seedream 5.0 Lite：图像生成与编辑功能

该技能适用于在 PoYo 平台上使用 Seedream 5.0 Lite 进行图像处理任务，支持高效的高分辨率图像生成、编辑以及灵活的尺寸控制。

## 使用场景

- 当用户明确请求使用 `Seedream 5.0 Lite`、`seedream-5.0-lite` 或 `seedream-5.0-lite-edit` 时。
- 当任务需要高分辨率图像生成、图像转换或图像编辑时。
- 当工作流程需要 2K/3K 分辨率的输出或精确的宽高比控制时。

## 模型选择

- `seedream-5.0-lite`：标准图像生成模型。
- `seedream-5.0-lite-edit`：用于处理用户提供的图像编辑请求。

## 关键输入参数

- 必须提供 `prompt` 参数。
- `image_urls` 参数支持最多 10 张图像路径，编辑任务时必须提供该参数。
- `size` 可以设置为 `2K`、`3K`，或指定宽高比（如 `1:1`、`16:9`、`21:9`）。
- `n` 参数用于指定输出图像的数量（范围为 1 到 15）。

## 执行步骤

- 请参考 `references/api.md` 以获取端点详情、模型 ID、关键字段、示例数据格式及轮询注意事项。
- 使用 `scripts/submit_seedream_5_0_lite.sh` 命令从 shell 提交原始 JSON 数据。
- 如果用户只需要使用 curl 进行请求，可以直接参考 `references/api.md` 中的示例代码，无需重新编写。
- 提交请求后，务必明确记录返回的 `task_id`，以便后续进行状态查询。

## 输出结果

在处理该模型系列任务时，应提供以下信息：
- 选择的模型 ID。
- 最终的处理结果或参数摘要。
- 是否使用了参考图像。
- 如果请求已成功提交，应显示返回的 `task_id`。
- 下一步操作：根据需要轮询任务状态或等待 Webhook 响应。