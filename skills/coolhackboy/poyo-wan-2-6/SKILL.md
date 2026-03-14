---
name: poyo-wan-2-6
description: 在 PoYo / poyo.ai 上，可以使用 `https://api.poyo.ai/api/generate/submit` 生成 Wan 2.6 格式的视频。该接口支持以下功能：`wan2.6-text-to-video`（文本转视频）、`wan2.6-image-to-video`（图片转视频）、`wan2.6-video-to-video`（视频转视频）、`text-to-video`（文本转视频）、`image-to-video`（图片转视频）以及 `multi_shots`（多帧合成视频）。
metadata: {"openclaw": {"homepage": "https://docs.poyo.ai/api-manual/video-series/wan-2-6", "requires": {"bins": ["curl"], "env": ["POYO_API_KEY"]}, "primaryEnv": "POYO_API_KEY"}}
---
# PoYo Wan 2.6 视频生成

此技能用于在 PoYo 平台上执行 Wan 2.6 相关的任务。它支持在同一模型系列内实现文本到视频、图像到视频以及视频到视频的转换。

## 使用场景

- 用户明确请求使用 `Wan 2.6` 或任何以 `wan2.6-*` 结尾的模型 ID。
- 任务需要支持文本到视频、图像到视频以及视频到视频的转换功能。
- 工作流程需要使用多帧合成（`multi_shots`）、控制视频分辨率或对源视频进行转换。

## 模型选择

- `wan2.6-text-to-video`：仅基于文本提示生成视频。
- `wan2.6-image-to-video`：根据单张图像生成视频。
- `wan2.6-video-to-video`：使用最多 3 个参考视频对源视频进行转换。

## 关键输入参数

- `prompt`：必填参数，用于提供视频生成的文本提示。
- `image_urls`：仅用于 `wan2.6-image-to-video`，支持上传单张图像。
- `video_urls`：仅用于 `wan2.6-video-to-video`，支持上传最多 3 个视频文件。
- `duration`：可选参数，支持 `5`、`10`、`15` 秒的生成时长。
- `resolution`：可选参数，支持 `720p`、`1080p` 的视频分辨率；`multi_shots` 参数用于控制生成视频是单帧还是多帧合成。

## 执行步骤

- 查阅 `references/api.md` 以获取端点详情、模型 ID、关键字段、示例数据格式以及轮询注意事项。
- 使用 `scripts/submit_wan_2_6.sh` 命令从 shell 提交原始 JSON 数据。
- 如果用户只需要使用 curl 命令进行测试，可以直接参考 `references/api.md` 中的示例，无需重新编写代码。
- 提交请求后，务必明确记录 `task_id`，以便后续进行状态查询。

## 输出结果

在处理此类任务时，应提供以下信息：
- 选定的模型 ID。
- 最终生成的视频内容或参数摘要。
- 是否使用了参考图像。
- 如果请求已成功提交，应显示返回的 `task_id`。
- 下一步操作：根据需要轮询任务状态或等待 Webhook 的响应。