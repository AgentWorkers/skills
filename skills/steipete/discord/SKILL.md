---
name: discord
description: **使用说明：**  
当您需要通过 `Clawdbot` 使用 Discord 工具来控制 Discord 时，请使用以下功能：发送消息、做出反应、发布或上传贴纸、上传表情符号、运行投票、管理主题/置顶帖子/搜索内容、获取权限或成员/角色/频道信息，以及在 Discord 的私信或频道中执行管理操作。
---

# Discord 动作

## 概述

使用 `discord` 可以管理消息、反应、主题帖、投票以及执行 moderation（管理）操作。您可以通过 `discord.actions.*` 来禁用某些功能组（默认情况下这些功能都是启用的，除非特别指定了禁用）。该工具会使用为 Clawdbot 配置的机器人令牌。

## 需要收集的输入参数

- 对于反应（reactions）：`channelId`、`messageId` 和一个 `emoji`。
- 对于贴纸（stickers）/投票（polls）/发送消息（sendMessage）：一个接收目标（`to`，格式为 `channel:<id>` 或 `user:<id>`），可选的 `content` 文本。
- 投票还需要提供一个 `question` 以及 2 到 10 个 `answers`。
- 对于媒体文件（media）：`mediaUrl`，本地文件使用 `file:///path`，远程文件使用 `https://...`。
- 对于表情符号上传（emoji uploads）：`guildId`、`name`、`mediaUrl`，可选的 `roleIds`（文件大小限制为 256KB，支持 PNG/JPG/GIF 格式）。
- 对于贴纸上传（sticker uploads）：`guildId`、`name`、`description`、`tags`、`mediaUrl`（文件大小限制为 512KB，支持 PNG/APNG/Lottie JSON 格式）。

消息上下文信息中包含 `discord message id` 和 `channel` 字段，这些字段可以直接在后续操作中使用。

**注意：** `sendMessage` 使用的格式是 `to: "channel:<id>"`，而不是 `channelId`。其他操作（如 `react`、`readMessages`、`editMessage`）则直接使用 `channelId`。

## 可用的动作

### 对消息做出反应（React to a message）

```json
{
  "action": "react",
  "channelId": "123",
  "messageId": "456",
  "emoji": "✅"
}
```

### 列出所有反应及发送者（List reactions + users）

```json
{
  "action": "reactions",
  "channelId": "123",
  "messageId": "456",
  "limit": 100
}
```

### 发送贴纸（Send a sticker）

```json
{
  "action": "sticker",
  "to": "channel:123",
  "stickerIds": ["9876543210"],
  "content": "Nice work!"
}
```

- 每条消息最多可以发送 3 个贴纸 ID。
- `to` 可以是 `user:<id>`，用于发送私信（DM）。

### 上传自定义表情符号（Upload a custom emoji）

```json
{
  "action": "emojiUpload",
  "guildId": "999",
  "name": "party_blob",
  "mediaUrl": "file:///tmp/party.png",
  "roleIds": ["222"]
}
```

- 表情符号图片必须是 PNG/JPG/GIF 格式，大小不超过 256KB。
- `roleIds` 是可选的；如果省略，则表情符号对所有用户可见。

### 上传贴纸（Upload a sticker）

```json
{
  "action": "stickerUpload",
  "guildId": "999",
  "name": "clawdbot_wave",
  "description": "Clawdbot waving hello",
  "tags": "👋",
  "mediaUrl": "file:///tmp/wave.png"
}
```

- 上传贴纸时需要提供 `name`、`description` 和 `tags`。
- 上传的文件必须是 PNG/APNG/Lottie JSON 格式，大小不超过 512KB。

### 创建投票（Create a poll）

```json
{
  "action": "poll",
  "to": "channel:123",
  "question": "Lunch?",
  "answers": ["Pizza", "Sushi", "Salad"],
  "allowMultiselect": false,
  "durationHours": 24,
  "content": "Vote now"
}
```

- `durationHours` 的默认值为 24 小时；最长为 32 天（768 小时）。

### 检查机器人在该频道的权限（Check bot permissions for a channel）

```json
{
  "action": "permissions",
  "channelId": "123"
}
```

## 可以尝试的功能：

- 使用 ✅/⚠️ 对状态更新做出反应。
- 发布投票以收集关于发布决策或会议时间的意见。
- 在成功部署后发送庆祝贴纸。
- 为重要发布时刻上传新的表情符号/贴纸。
- 在团队频道中每周进行“优先级检查”投票。
- 在用户请求完成时通过私信发送贴纸作为确认。

## 动作的禁用

使用 `discord.actions.*` 来禁用以下功能组：
- `reactions`（对消息做出反应 + 查看所有反应 + 列出已发送的表情符号）
- `stickers`、`polls`、`permissions`、`messages`、`threads`、`pins`、`search`
- `emojiUploads`、`stickerUploads`
- `memberInfo`、`roleInfo`、`channelInfo`、`voiceStatus`、`events`
- `roles`（添加/删除角色，默认值为 `false`）
- `moderation`（设置超时/踢出/禁言用户，默认值为 `false`）

### 阅读最近的消息（Read recent messages）

```json
{
  "action": "readMessages",
  "channelId": "123",
  "limit": 20
}
```

### 发送/编辑/删除消息（Send/edit/delete a message）

```json
{
  "action": "sendMessage",
  "to": "channel:123",
  "content": "Hello from Clawdbot"
}
```

**带有媒体附件时：**

```json
{
  "action": "sendMessage",
  "to": "channel:123",
  "content": "Check out this audio!",
  "mediaUrl": "file:///tmp/audio.mp3"
}
```

- `to` 的格式为 `channel:<id>` 或 `user:<id>`（用于私信，而非 `channelId`）。
- `mediaUrl` 支持本地文件（`file:///path/to/file`）和远程 URL（`https://...`）。
- 可选的 `replyTo` 参数用于回复特定消息。

```json
{
  "action": "editMessage",
  "channelId": "123",
  "messageId": "456",
  "content": "Fixed typo"
}
```

### 主题帖（Threads）

```json
{
  "action": "threadCreate",
  "channelId": "123",
  "name": "Bug triage",
  "messageId": "456"
}
```

```json
{
  "action": "threadList",
  "guildId": "999"
}
```

```json
{
  "action": "threadReply",
  "channelId": "777",
  "content": "Replying in thread"
}
```

### 固定帖子（Pin posts）

```json
{
  "action": "pinMessage",
  "channelId": "123",
  "messageId": "456"
}
```

```json
{
  "action": "listPins",
  "channelId": "123"
}
```

### 搜索消息（Search messages）

```json
{
  "action": "searchMessages",
  "guildId": "999",
  "content": "release notes",
  "channelIds": ["123", "456"],
  "limit": 10
}
```

### 成员和角色信息（Member + role info）

```json
{
  "action": "memberInfo",
  "guildId": "999",
  "userId": "111"
}
```

```json
{
  "action": "roleInfo",
  "guildId": "999"
}
```

### 列出可用的自定义表情符号（List available custom emojis）

```json
{
  "action": "emojiList",
  "guildId": "999"
}
```

### 角色更改（默认禁用）（Role changes, disabled by default）

```json
{
  "action": "roleAdd",
  "guildId": "999",
  "userId": "111",
  "roleId": "222"
}
```

### 频道信息（Channel info）

```json
{
  "action": "channelInfo",
  "channelId": "123"
}
```

```json
{
  "action": "channelList",
  "guildId": "999"
}
```

### 音频状态（Voice status）

```json
{
  "action": "voiceStatus",
  "guildId": "999",
  "userId": "111"
}
```

### 预定事件（Scheduled events）

```json
{
  "action": "eventList",
  "guildId": "999"
}
```

### Management 功能（默认禁用）（Moderation, disabled by default）

## Discord 编写风格指南

**保持对话式的风格！** Discord 是一个聊天平台，而不是正式的文档。

### 建议：
- 信息简短精炼（1-3 句最佳）
- 多次快速回复，避免长篇大论
- 使用表情符号来表达语气或强调（🦞）
- 使用小写和 casual 的写作风格
- 将信息分成易于理解的段落
- 保持与对话的节奏一致

### 不建议：
- 不要使用 markdown 表格（Discord 会将其显示为难看的原始格式 `| text |`）
- 在非正式聊天中不要使用 `## 标题**（使用 **粗体** 或大写字母来强调）
- 避免冗长的多段文字
- 对简单的内容不要过度解释
- 省略不必要的客套话（如 “我很乐意帮忙！”）

### 有效的格式：
- 使用 **粗体** 来强调重点
- 使用 `code` 标记技术术语
- 使用列表来列出多个项目
- 使用 `>` 引号来引用内容
- 使用 `<>` 将多个链接包裹起来，以避免嵌入问题

### 示例转换：

❌ 不好的格式：
```
I'd be happy to help with that! Here's a comprehensive overview of the versioning strategies available:

## Semantic Versioning
Semver uses MAJOR.MINOR.PATCH format where...

## Calendar Versioning
CalVer uses date-based versions like...
```

✅ 良好的格式：
```
versioning options: semver (1.2.3), calver (2026.01.04), or yolo (`latest` forever). what fits your release cadence?
```