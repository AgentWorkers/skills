---
name: poyo-nano-banana-2
description: >
  在 PoYo / poyo.ai 平台上，可以通过 `https://api.poyo.ai/api/generate/submit` 生成 Nano Banana 2 的图像并进行高级编辑。该服务支持以下功能：  
  - 生成新的 Nano Banana 2 图像（`nano-banana-2-new`）  
  - 对已有的 Nano Banana 2 图像进行编辑（`nano-banana-2-new-edit`）  
  - 多参考图像生成（multi-reference workflows）  
  - 文本转图像（text-to-image）  
  - 图像转图像（image-to-image）  
  - 输出格式包括 1K、2K 和 4K。
metadata: {"openclaw":{"homepage":"https://docs.poyo.ai/api-manual/image-series/nano-banana-2-new","requires":{"bins":["curl"],"env":["POYO_API_KEY"]},"primaryEnv":"POYO_API_KEY"}}
---
# PoYo Nano Banana 2 图像生成与高级编辑功能

此技能用于在 PoYo 平台上执行 Nano Banana 2 相关的任务，支持多参考图像的生成、高级编辑以及高分辨率输出。如需了解产品端的默认设置，请参阅 `references/frontend-notes.md`。

## 使用场景

- 当用户明确请求生成 `Nano Banana 2`、`nano-banana-2-new` 或 `nano-banana-2-new-edit` 图像时。
- 当任务需要使用多张参考图像、进行图像合成或高级编辑时。
- 当需要生成 1K、2K 或 4K 分辨率的图像时；或者需要使用 `google_search` 功能时。

## 模型选择

- `nano-banana-2-new`：用于文本到图像或图像到图像的转换。
- `nano-banana-2-new-edit`：当用户希望编辑提供的图像时使用。

## 关键输入参数

- `prompt` 是必填项，长度限制为 1000 个字符。
- `image_urls` 可输入最多 14 张参考图像的 URL。
- `size` 可选参数，支持以下比例：`1:1`、`2:3`、`3:2`、`3:4`、`4:3`、`4:5`、`5:4`、`9:16`、`16:9`、`21:9`。
- `resolution` 可选参数，支持 1K、2K、4K 分辨率，默认值为 1K。
- `google_search` 是可选参数，主要用于获取真实世界的参考数据。

## 执行流程

- 阅读 `references/api.md` 以了解任务所需的数据字段、示例及相关注意事项。
- 如需使用产品端的默认设置或模拟当前桌面前端的行为，请参阅 `references/frontend-notes.md`。
- 在适合直接通过 API 执行任务的情况下，可以使用 `scripts/submit_nano_banana_2.sh` 脚本从 shell 提交任务。
- 如果用户需要 curl 命令示例，请参考 `references/api.md` 中的相关内容。
- 提交任务后，请明确显示 `task_id`，以便后续能够轻松查询任务状态。

## 输出结果

在完成 Nano Banana 2 相关任务时，应提供以下信息：
- 选择的模型。
- 最终生成的图像或参数摘要。
- 是否使用了参考图像。
- 如果任务已成功提交，则需提供返回的 `task_id`。
- 下一步操作：继续查询任务状态或等待 Webhook 的响应。