---
name: poyo-grok-imagine
description: Grok：您可以通过 `https://api.poyo.ai/api/generate/submit` 在 PoYo / poyo.ai 上生成视频。该功能支持以下用途：`grok-imagine`（文本转视频）、`image-to-video`（图片转视频），以及视频时长控制（6秒或10秒），同时还可以选择视频模式（`fun`、`normal` 或 `spicy`）。
metadata: {"openclaw": {"homepage": "https://docs.poyo.ai/api-manual/video-series/grok-imagine", "requires": {"bins": ["curl"], "env": ["POYO_API_KEY"]}, "primaryEnv": "POYO_API_KEY"}}
---
# PoYo Grok Imagine 视频生成

此技能可用于在 PoYo 上执行 `grok-imagine` 任务，支持将短文本转换为视频、将图片转换为视频，以及根据特定模式对视频进行样式化处理。

## 使用场景

- 用户明确请求使用 `Grok Imagine` 或 `grok-imagine` 功能。
- 需要生成时长为 6 秒或 10 秒的视频片段。
- 工作流程需要将文本转换为视频、将图片转换为视频，或根据特定模式对视频进行样式化处理。

## 核心功能

- `grok-imagine` 是一个统一的视频生成入口点。使用 `image_urls` 参数进行图片到视频的转换，使用 `mode` 参数来控制视频的风格（`fun`、`normal` 或 `spicy`）。

## 关键输入参数

- 必需输入 `prompt`（提示信息）。
- `image_urls` 参数用于图片到视频的转换，支持上传一张图片。
- `duration` 参数支持 6 秒或 10 秒的生成时长。
- `aspect_ratio` 参数支持文本到视频时的分辨率比例（`1:1`、`2:3`、`3:2`）。
- `mode` 参数支持视频的风格（`fun`、`normal`、`spicy`）。

## 执行步骤

- 查阅 `references/api.md` 以获取端点详情、模型 ID、关键字段、示例数据格式以及轮询注意事项。
- 使用 `scripts/submit_grok_imagine.sh` 命令从 shell 提交原始 JSON 数据。
- 如果用户只需要使用 curl 命令来执行操作，可以直接参考 `references/api.md` 中的示例代码，无需重新编写。
- 提交请求后，务必明确显示返回的 `task_id`，以便后续进行状态查询。

## 输出结果

在处理此类任务时，应提供以下信息：
- 选择的模型 ID。
- 最终生成的视频内容或参数摘要。
- 是否使用了参考图片。
- 如果请求已成功提交，应显示返回的 `task_id`。
- 下一步操作：轮询任务状态或等待 Webhook 响应。