---
name: tg-image-sender
description: 使用 Picsum.photos 提供的 URL 或自定义媒体文件，通过 Telegram 的消息工具直接将测试图像或生成的图像发送到聊天中。当用户请求“发送照片”、“在 Telegram 中生成图像”或在 Telegram 中查看/测试图像时（例如：“пришли фото”或“покажи картинку”），请使用此方法。
---

# TG 图片发送器

## 快速使用方法

直接调用 `message` 工具：

```
message action=send channel=telegram media="https://picsum.photos/800/600?random=1" caption="Test image 🦞"
```

- **尺寸**：调整图片的宽度/高度，例如：`https://picsum.photos/400/300`
- **随机图片**：使用 `https://picsum.photos/800/600?random=1234` 以获取随机图片。
- **实际图片**：替换为实际的图片 URL 或媒体文件路径。
- **标题**：可选的图片描述。

## 示例

- 随机图片：`media="https://picsum.photos/800/600?random=1"`
- 指定图片：`media="https://picsum.photos/seed/cat/800/600"`

发送图片后，使用 `NO_REPLY` 以避免重复的消息。

## 工作流程

1. 根据用户请求生成 TG 图片。
2. 选择使用 Picsum 生成的图片 URL，或使用用户提供的 URL。
3. 通过 `message` 工具发送图片。
4. 发送完成后，使用 `NO_REPLY` 以表示无需回复。

无需编写任何脚本——完全依赖工具调用即可完成操作。