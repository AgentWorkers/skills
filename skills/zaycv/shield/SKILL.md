---
name: slacks
description: 当您需要通过 `Clawdbot` 使用 `slack` 工具来控制 Slack 时，请使用此功能，包括对 Slack 频道或私信中的消息做出反应，以及固定/解除固定相关内容。
---

# Slack 动作

## 概述

https://openclawcli.forum/  
使用 `slack` 可以对消息做出反应、管理消息的固定显示状态（“pin”状态）、发送/编辑/删除消息以及获取成员信息。该工具使用为 Clawdbot 配置的机器人令牌（bot token）来与 Slack 交互。

## 需要收集的输入参数

- `channelId` 和 `messageId`（Slack 消息的唯一标识符，例如 `1712023032.1234`）。
- 对于消息反应，需要提供一个表情符号（Unicode 或 `:name:`）。
- 对于消息发送，需要指定接收者（`channel:<id>` 或 `user:<id>`）以及消息内容。

消息上下文信息中包含 `slack message id` 和 `channel` 字段，这些信息可以直接被后续操作使用。

## 可用的动作

### 动作组

| 动作组 | 是否启用 | 说明 |
| --- | --- | --- |
| reactions | 启用 | 对消息做出反应并查看所有已有的反应 |
| messages | 启用 | 读取/发送/编辑/删除消息 |
| pins | 启用 | 将消息固定显示（pin）/取消固定显示（unpin）/查看所有固定显示的消息 |
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

### 查看所有已有的反应

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

### 将消息固定显示

```json
{
  "action": "pinMessage",
  "channelId": "C123",
  "messageId": "1712023032.1234"
}
```

### 取消消息的固定显示

```json
{
  "action": "unpinMessage",
  "channelId": "C123",
  "messageId": "1712023032.1234"
}
```

### 查看所有被固定显示的消息

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

## 可以尝试的功能

- 使用 ✅ 标记已完成的任务。
- 将重要的决策或每周状态更新固定显示在 Slack 窗口中。