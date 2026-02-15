---
name: gemini-tg-image-gen
description: 通过 OpenRouter（google/gemini-2.5-flash-image）生成图像，并将其发送到 Telegram。当用户在 Telegram 中请求 AI 生成的图像时，可以使用此功能。
---

# Gemini TG Image Gen (OpenRouter)

## 工作流程

1. 立即通过 Telegram 通知用户：“⏳ 图像生成中，请稍候……”
2. 使用 OpenRouter 的 `google/gemini-2.5-flash-image` 模型。
3. 从环境变量中读取 API 密钥：`OPENROUTER_API_KEY`。
4. 运行脚本以生成图像并将其保存到本地。
5. 使用 `message` 工具将图像发送到 Telegram（发送路径为本地文件路径）。
6. 不需要回复用户。

## 使用方法

```bash
OPENROUTER_API_KEY=... python3 scripts/generate_image.py "<prompt>"
```

脚本会输出一个包含图像路径的 JSON 对象。

## 通过 Telegram 发送图像

```
# step 1: waiting message
message action=send channel=telegram text="⏳ Идёт генерация, подождите немного..."

# step 5: send image
message action=send channel=telegram media="/root/.openclaw/workspace/tmp/openrouter_image_*.png" caption="Generated: <prompt>"
```

发送图像后，无需回复用户。