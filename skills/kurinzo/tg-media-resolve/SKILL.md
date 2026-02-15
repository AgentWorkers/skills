---
name: tg-media-resolve
description: 将 Telegram 中的 `<media:image>`, `<media:document>`, `<media:video>` 等媒体占位符解析为实际的文件，以便进行视觉分析或处理。当 Telegram 消息中包含这些媒体占位符（例如 `<media:image>`）时，可以使用此功能（通常出现在被引用或回复的消息中，或群聊历史记录中）。通过 Telegram Bot API 下载这些媒体文件，并返回文件的本地路径，以便后续使用图像处理工具或其他程序进行处理。
---

# Telegram Media Resolver

该工具用于将 Telegram 消息中的 `<media:*>` 占位符解析为可下载的文件。

## 使用场景

当您在 Telegram 消息中看到 `<media:image>`、`<media:document>`、`<media:video>`、`<media:sticker>`、`<media:voice>` 或 `<media:animation>`（尤其是在回复或群组历史记录中）时，如果需要查看或分析这些内容，可以使用该工具。

## 工作原理

1. 通过 Bot API 将目标消息临时转发以获取文件元数据。
2. 从 Telegram 服务器下载文件。
3. 删除转发的副本（进行清理操作）。
4. 返回文件的本地路径，以便使用 `image` 工具或 `exec` 命令进行处理。

## 使用方法

```bash
python3 scripts/fetch_media.py \
  --bot-token "$BOT_TOKEN" \
  --chat-id CHAT_ID \
  --message-id MESSAGE_ID \
  [--out /tmp] \
  [--forward-to SELF_CHAT_ID]
```

### 参数

- `--bot-token` — Telegram Bot API 令牌（从 OpenClaw 配置文件 `channelsTelegram.botToken` 中获取）
- `--chat-id` — 包含该消息的聊天室 ID（来自消息上下文，例如 `-1001234567890`）
- `--message-id` — 包含媒体的消息的 ID（来自消息上下文中的 `[id:XXXXX]`）
- `--out` — 输出目录（默认值：`/tmp`）
- `--forward-to` — 临时转发的目标聊天室 ID（默认值：与 `--chat-id` 相同）。建议使用机器人所有者的私信聊天室 ID，以避免在群组中显示转发记录。

### 从消息上下文中提取参数

OpenClaw 对 Telegram 消息的格式如下：
```
[Telegram GroupName id:CHAT_ID topic:N ...] User (USER_ID): <media:image> [id:MSG_ID chat:CHAT_ID]
```

请从该格式中提取 `CHAT_ID` 和 `MSG_ID`。

## 工作流程

1. 从消息上下文中提取 `chat_id` 和 `message_id`。
2. 读取 Bot API 令牌：`cat ~/.openclaw/openclaw.json | python3 -c "import sys,json; print(json.load(sys.stdin)['channels']['telegram']['botToken'])"`
3. 运行获取文件的脚本。
4. 使用返回的文件路径通过 `image` 工具进行图像分析。

## 支持的媒体类型

照片、文档、视频、动画（GIF）、贴纸、语音消息、视频笔记、音频文件。

## 限制条件

- 机器人必须是包含目标消息的聊天室的成员。
- 大于 20MB 的文件无法通过 Bot API 下载。
- 临时转发的消息可能会在目标聊天室中短暂显示，随后会被删除。
- 建议使用 `--forward-to` 参数将文件转发到私信聊天室（例如机器人所有者的私信），以避免在群组中显示转发记录。