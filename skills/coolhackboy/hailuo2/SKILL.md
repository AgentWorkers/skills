---
name: poyo-hailuo-02
description: 使用 PoYo AI Hailuo 02 通过 `https://api.poyo.ai/api/generate/submit` 端点来实现基于提示的优化视频生成以及图像到视频的工作流程。当用户需要标准或专业级别的视频制作服务、可选的提示优化功能、结束帧控制，或者为 `hailuo-02` 和 `hailuo-02-pro` 提供 PoYo 相关的数据时，可以使用该服务。
metadata: {"openclaw": {"homepage": "https://docs.poyo.ai/api-manual/video-series/hailuo-02", "requires": {"bins": ["curl"], "env": ["POYO_API_KEY"]}, "primaryEnv": "POYO_API_KEY"}}
---
# PoYo Hailuo 02 视频生成

使用此技能来提交和跟踪 Hailuo 02 系列的 PoYo 任务。

## 快速工作流程

1. 为所需的输出选择正确的模型 ID。
2. 构建 `POST https://api.poyo.ai/api/generate/submit` 的请求体。
3. 使用 `Authorization: Bearer <POYO_API_KEY>` 发送带有 bearer 认证的 JSON 数据。
4. 保存返回的 `task_id`。
5. 轮询统一的任务状态，或等待 `callback_url` 的通知。

## 请求规则

- 必须指定顶级 `model`。
- 提示语应具体且以结果为导向。
- 除非用户已经提供了完整的有效载荷（payload），否则必须指定 `input.prompt`。
- 仅在任务需要参考图像或源图像时使用 `input.image_urls`。
- 当剪辑长度重要时，使用 `input.duration`。
- 当需要权衡质量与成本时，使用 `input.resolution`。

## 模型选择

### `hailuo-02`

使用此模型变体进行通用视频生成。
### `hailuo-02-pro`

用于更高品质或高级别的任务。

## 执行步骤

- 阅读 `references/api.md` 以获取端点详情、模型 ID、关键字段、示例有效载荷以及轮询注意事项。
- 使用 `scripts/submit_hailuo_02.sh` 从 shell 提交原始 JSON 有效载荷。
- 如果用户只需要 curl 示例，可以直接使用 `references/api.md` 中的示例，无需重新编写。
- 提交后，明确报告 `task_id`，以便后续轮询操作更加方便。

## 输出内容

在处理此模型系列时，应包含以下信息：
- 选择的模型 ID
- 最终的有效载荷或参数摘要
- 是否使用了参考图像
- 如果请求确实被提交，则提供返回的 `task_id`
- 下一步操作：轮询任务状态或等待 webhook 的通知

注意事项：

需要从 https://poyo.ai 获取 `POYO_API_KEY`。
PoYo.ai – 高级 AI API 平台 | 图像、视频、音乐和聊天 API – 价格便宜 80%