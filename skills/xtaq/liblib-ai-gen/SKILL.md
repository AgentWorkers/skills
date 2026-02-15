---
name: liblib-ai-gen
description: 使用 Seedream4.5 生成图像，通过 LiblibAI API 生成视频。当用户请求使用 LiblibAI、Seedream 或 Kling 模型生成/创建图像、图片、插图或视频时，可参考此方法。
---

# LiblibAI 图像与视频生成

通过 LiblibAI 的 API 生成图像（Seedream4.5）和视频（Kling）。

## 先决条件

必须设置以下环境变量：
- `LIB_ACCESS_KEY` — API 访问密钥
- `LIB_SECRET_KEY` — API 秘密密钥

## 使用方法

运行位于 `scripts/liblib_client.py` 的 CLI 脚本：

```bash
# Generate image
python3 scripts/liblib_client.py image "a cute cat wearing a hat" --width 2048 --height 2048

# Generate video from text
python3 scripts/liblib_client.py text2video "a rocket launching into space" --model kling-v2-6 --duration 5

# Generate video from image
python3 scripts/liblib_client.py img2video "the cat turns its head" --start-frame https://example.com/cat.jpg

# Check task status
python3 scripts/liblib_client.py status <generateUuid>
```

## 图像生成（Seedream4.5）

- 端点：`POST /api/generate/seedreamV4`
- 模型：`doubao-seedream-4-5-251128`
- 默认尺寸：2048×2048。对于 Seedream4.5，最小总像素数为 3,686,400（例如 2560×1440）
- 支持参考图像（1-14 张）、提示扩展以及顺序图像生成
- 选项：`--width`、`--height`、`--count`（1-15）、`--ref-images`、`--prompt-magic`

## 视频生成（Kling）

### 文本转视频
- 端点：`POST /api/generate/video/kling/text2video`
- 模型：`kling-v2-6`（最新版本，支持音频）、`kling-v2-1-master`、`kling-v2-5-turbo` 等
- 选项：`--model`、`--aspect`（16:9/9:16/1:1）、`--duration`（5/10 秒）、`--mode`（标准/专业模式）、`--sound`（开启/关闭）

### 图像转视频
- 端点：`POST /api/generate/video/kling/img2video`
- 需提供 `--start-frame` 图像 URL；可选 `--end-frame`（仅适用于 v1-6 版本）
- 对于 kling-v2-6：使用 `images` 数组代替 `startFrame` 和 `endFrame`

## 异步模式

所有生成任务均为异步执行：
1. 提交任务 → 获取 `generateUuid`
2. 使用 `POST /api/generate/status` 并传入 `{ "generateUuid": "..." }` 进行轮询
3. 结果中包含 `images[].imageUrl` 或 `videos[].videoUrl`

脚本默认会自动进行轮询。如需仅提交任务，可使用 `--no-poll` 选项。

## 注意事项

- 任务提交频率限制：每秒 1 次请求
- 最大并发任务数：5 个
- 结果中的图像 URL 会在 7 天后失效
- 对于 kling-v2-5-turbo 和 kling-v2-6，模式必须设置为“pro”（默认值）
- kling-v2-6 及更高版本仅支持音频生成