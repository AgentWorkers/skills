---
name: slack
description: 当您需要通过 `Clawdbot` 使用 `slack` 工具来控制 Slack 时，请使用此功能，包括对 Slack 频道或私信中的消息做出反应，以及将消息固定（pin）或取消固定（unpin）。
---

# Slack Actions

## 概述

使用 `slack` 可以对消息做出反应、管理消息的固定显示状态（如“置顶”）、发送/编辑/删除消息以及获取成员信息。该工具会使用为 Clawdbot 配置的机器人令牌（bot token）来与 Slack 交互。

## 需要收集的输入参数

- `channelId` 和 `messageId`（Slack 消息的唯一标识符，例如 `1712023032.1234`）。
- 对于反应操作，需要提供一个表情符号（Unicode 格式或 `:name:` 格式）。
- 对于发送消息的操作，需要指定接收者（`channel:<id>` 或 `user:<id>`）以及消息内容。

消息上下文信息中包含 `slack message id` 和 `channel` 字段，这些信息可以直接在后续操作中使用。

## 可用的操作

### 操作组

| 操作组 | 默认状态 | 说明 |
| --- | --- | --- |
| reactions | 启用 | 对消息做出反应并查看已有的反应记录 |
| messages | 启用 | 读取/发送/编辑/删除消息 |
| pins | 启用 | 将消息置顶/取消置顶/查看已置顶的消息列表 |
| memberInfo | 启用 | 获取成员信息 |
| emojiList | 启用 | 查看自定义表情符号列表 |

### 对消息做出反应

```json
{
  "action": "react",
  "channelId": "C123",
  "messageId": "1712023032.1234",
  "emoji": "✅"
}
```

### 查看已有的反应记录

```json
{
  "action": "reactions",
  "channelId": "C123",
  "messageId": "1712023032.1234"
}
```

### 发送消息

```json
{
  "action": "sendMessage",
  "to": "channel:C123",
  "content": "Hello from Clawdbot"
}
```

### 编辑消息

```json
{
  "action": "editMessage",
  "channelId": "C123",
  "messageId": "1712023032.1234",
  "content": "Updated text"
}
```

### 删除消息

```json
{
  "action": "deleteMessage",
  "channelId": "C123",
  "messageId": "1712023032.1234"
}
```

### 查看最近的消息

```json
{
  "action": "readMessages",
  "channelId": "C123",
  "limit": 20
}
```

### 将消息置顶

```json
{
  "action": "pinMessage",
  "channelId": "C123",
  "messageId": "1712023032.1234"
}
```

### 取消消息的置顶状态

```json
{
  "action": "unpinMessage",
  "channelId": "C123",
  "messageId": "1712023032.1234"
}
```

### 查看已置顶的消息列表

```json
{
  "action": "listPins",
  "channelId": "C123"
}
```

### 获取成员信息

```json
{
  "action": "memberInfo",
  "userId": "U123"
}
```

### 查看自定义表情符号列表

```json
{
  "action": "emojiList"
}
```

## 建议尝试的操作

- 使用 ✅ 表示任务已完成。
- 将重要的决策或每周状态更新置顶显示。