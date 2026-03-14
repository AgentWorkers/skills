---
name: poyo-kling-3-0
description: 在 PoYo / poyo.ai 上使用 `https://api.poyo.ai/api/generate/submit` 生成 Kling 3.0 视频；该接口支持 `kling-3.0/standard`、`kling-3.0/pro`、单次生成、多次生成、多提示输入（`multi_prompt`）以及包含声音的输出格式。
metadata: {"openclaw": {"homepage": "https://docs.poyo.ai/api-manual/video-series/kling-3-0", "requires": {"bins": ["curl"], "env": ["POYO_API_KEY"]}, "primaryEnv": "POYO_API_KEY"}}
---
# PoYo Kling 3.0 多镜头视频生成

此技能用于在 PoYo 平台上使用 Kling 3.0 生成视频。它支持单镜头和多镜头视频的生成、基于元素的提示系统，以及带有声音的输出效果。

## 使用场景

- 当用户明确请求使用 `kling-3.0`、`kling-3.0/standard` 或 `kling-3.0/pro` 时。
- 当任务需要多镜头叙事或结构化的多提示输入时。
- 当工作流程依赖于 `kling_elements`、参考帧或声音控制时。

## 模型选择

- `kling-3.0/standard`：提供标准质量的视频生成结果。
- `kling-3.0/pro`：为追求更高质量输出的用户提供的高级版本。

## 关键输入参数

- `sound`、`multi_shots` 和 `duration` 是控制视频生成流程的主要参数。
- `prompt` 用于单镜头视频生成；`multiprompt` 用于多镜头视频生成。
- `image_urls` 用于指定视频的起始和结束帧，当使用 `kling_elements` 时也是必需的。
- `aspect_ratio` 支持 `1:1`、`16:9` 和 `9:16` 的宽高比。

## 执行步骤

- 查阅 `references/api.md` 以获取端点详情、模型 ID、关键字段、示例数据格式以及轮询注意事项。
- 使用 `scripts/submit_kling_3_0.sh` 从 shell 提交原始 JSON 数据。
- 如果用户只需要使用 curl 来提交请求，可以直接参考 `references/api.md` 中的示例代码，无需重新编写。
- 提交请求后，请明确记录 `task_id`，以便后续进行状态查询。

## 输出结果

在处理该模型系列时，应提供以下信息：
- 选择的模型 ID。
- 最终生成的视频内容或参数摘要。
- 是否使用了参考图像。
- 如果请求已成功提交，应显示返回的 `task_id`。
- 下一步操作：根据需要轮询任务状态或等待 Webhook 的响应。