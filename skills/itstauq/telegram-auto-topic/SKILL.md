---
name: telegram-auto-topic
description: >
  Add `/topic` to the start of any message in a Telegram forum group to
  auto-create a new topic from it. A title is generated automatically from
  the message content.
  Github: https://github.com/itstauq/telegram-auto-topic
metadata:
  openclaw:
    requires:
      config:
        - ~/.openclaw/openclaw.json
      env:
        - OPENCLAW_CONFIG
      bins:
        - curl
        - jq
---

# Telegram自动创建主题功能

在Telegram论坛群组中，如果在消息开头添加 `/topic`，系统会自动创建一个新的主题。主题的名称会从你的消息中自动生成，无需你手动指定。

### 示例

**1.** 你发送一条以 `/topic` 开头的消息：
> /topic @your_bot 我需要在3月之前办理护照续签手续

**2.** 系统会创建一个名为 “Passport Renewal Before March” 的新论坛主题，并在主题中引用你的原始消息。你会收到一条回复，其中包含指向新主题的链接。

## 先决条件

- 该群组必须在 OpenClaw 中进行配置（`channelsTelegram.groups.<CHAT_ID>`），这样才能让 OpenClaw 正确处理来自该群组的消息。
- 该群组必须启用了 “forum/topics” 功能。
- 你的机器人需要在该群组中具有管理员权限，并且拥有 “Manage Topics” 的权限。

## `/topic` 的处理流程

当消息以 `/topic` 开头时，系统会执行以下操作：

1. 生成一个简洁的、3到7个字的标题来概括这条消息的内容。
2. 运行相应的脚本（使用占位符替换消息中的实际信息）：
   ```
   scripts/telegram-auto-topic.sh <chat_id> <message_id> "<sender name>" "<title>" "<text after /topic>"
   ```
   如果消息中没有文本内容（例如仅包含媒体文件），则将 `text` 参数设置为空字符串。
   脚本会使用相对于当前脚本目录的路径来处理消息。
3. 脚本返回一个 JSON 对象，其中包含 `topic_id`、`title` 和 `link` 三个字段。
4. 向原始消息回复：“主题已创建 → [<title>](<link>)”。
5. 然后在新创建的主题中回复原始消息的内容（使用 `topic_id` 中的 `threadId`）。回复方式应与处理普通消息相同。
6. 在完成这两步回复后，再回复 “NO_REPLY”。

## 工作原理

1. 用户发送一条以 `/topic` 开头的消息。
2. 系统根据这条消息自动生成一个新主题。
3. 原始消息会被引用到新主题中，并显示发送者的名称。
4. 用户会收到一条包含新主题链接的回复。
5. 机器人会在新主题中回复用户。

**注意：** 该功能也支持媒体文件。如果图片、视频或文档的标题中包含 `/topic`，它们也会被自动转发到新主题中。

## 脚本参考

```bash
scripts/telegram-auto-topic.sh <chat_id> <message_id> <sender> [title] [text]
```

| 参数 | 类型 | 是否必填 | 说明 |
|---------|------|---------|-------------------|
| `chat_id` | 参数 | 是 | 超级群组的聊天ID（负数格式） |
| `message_id` | 参数 | 是 | 需要引用的原始消息ID |
| `sender` | 参数 | 是 | 原始消息的发送者名称 |
| `title` | 参数 | 否 | 主题名称（如果省略，则使用消息的前50个字符作为默认标题） |
| `text` | 参数 | 否 | `/topic` 后面的消息内容；如果为空，则视为媒体文件进行转发 |

脚本返回的JSON格式如下：`{"topic_id": 123, "title": "Used title", "link": "https://t.me/c/..."}`

## 可选配置

- **忽略对机器人的提及**：默认情况下，机器人仅会在被提及时才作出响应。如果你想直接使用 `/topic` 而不提及机器人，可以这样配置：
   ```json
"channels.telegram.groups.<CHAT_ID>": {
  "requireMention": false
}
```

- **在Telegram中添加自动完成功能**：你可以在 `channelsTelegram` 目录下添加相应的配置，以便在 Telegram 的命令菜单中显示 `/topic` 命令：
   ```json
{
  "customCommands": [
    {
      "command": "topic",
      "description": "Create a new forum topic from a message"
    }
  ]
}
```

## 限制事项

- **归属显示**：由于Telegram API的限制，被引用的消息会显示为机器人的发送内容，发送者名称会作为归属信息显示在消息下方。
- **媒体文件**：转发的媒体文件会显示 “Forwarded from” 的来源提示，但这并非Telegram的原生功能。
- **仅适用于论坛群组**：该功能不适用于普通群组或私信。
- **权限要求**：机器人需要具有 “Manage Topics” 的管理员权限。
- **主题长度限制**：Telegram 对主题名称的长度有限制，最多为128个字符。