---
name: rocketchat
description: RocketChat团队消息系统：通过REST API管理频道、消息、用户及集成功能
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - RC_URL
        - RC_TOKEN
        - RC_USER_ID
      bins:
        - curl
      anyBins:
        - jq
    primaryEnv: RC_TOKEN
    homepage: https://developer.rocket.chat/reference/api/rest-api
---
# RocketChat 技能

这是一个开源的团队聊天平台，用于促进沟通与协作。

## 概述

RocketChat 支持以下功能：
- 频道（公共/私有）、私信、主题讨论
- 用户和角色管理
- 集成（WebHook、机器人）
- 多渠道通信（跨平台聊天）

房间类型有三种：频道（`channels.*`）、小组/私有房间（`groups.*`）和私信（`im.*`）。通用的 `chat.*` 端点可以通过 `roomId` 与所有类型的房间进行交互。

## API 认证

```bash
# Header-based auth
curl -s \
  -H "X-Auth-Token: $RC_TOKEN" \
  -H "X-User-Id: $RC_USER_ID" \
  "$RC_URL/api/v1/me"

# Get tokens from login
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"user":"username","password":"password"}' \
  "$RC_URL/api/v1/login" | jq '{userId: .data.userId, authToken: .data.authToken}'
```

## 关键标识符

- **roomId** — 房间标识符（例如：`GENERAL`、`ByehQjC44FwMeiLbX`）
- **msgId** — 消息的 alphanumeric ID（与 Slack 不同，不是时间戳）
- **emoji** — 不带冒号的表情符号名称（例如：`thumbsup`、`white_check_mark`）

消息上下文行包含 `rocketchat message id` 和 `room` 字段——可以直接使用这些字段。

## 频道

```bash
# List channels
curl -s -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  "$RC_URL/api/v1/channels.list?count=50"

# Channel info
curl -s -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  "$RC_URL/api/v1/channels.info?roomId=ROOM_ID"

# Get channel history
curl -s -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  "$RC_URL/api/v1/channels.history?roomId=ROOM_ID&count=50"

# Create channel
curl -s -X POST -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  -H "Content-Type: application/json" \
  -d '{"name":"new-channel","members":["user1"]}' \
  "$RC_URL/api/v1/channels.create"

# Archive channel
curl -s -X POST -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  -H "Content-Type: application/json" \
  -d '{"roomId":"ROOM_ID"}' \
  "$RC_URL/api/v1/channels.archive"

# Set channel topic
curl -s -X POST -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  -H "Content-Type: application/json" \
  -d '{"roomId":"ROOM_ID","topic":"Weekly standup notes"}' \
  "$RC_URL/api/v1/channels.setTopic"

# List channel members
curl -s -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  "$RC_URL/api/v1/channels.members?roomId=ROOM_ID&count=50"
```

对于私有小组，请使用 `groups.*`；对于私信，请使用 `im.*`。查询参数相同。

## 消息

```bash
# Send message (simple)
curl -s -X POST -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  -H "Content-Type: application/json" \
  -d '{"channel":"#general","text":"Hello!"}' \
  "$RC_URL/api/v1/chat.postMessage"
```

`channel` 参数可以接受：`#channel-name`、`@username`（私信）或 `roomId`。

```bash
# Send message (advanced — custom _id, alias, avatar)
curl -s -X POST -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  -H "Content-Type: application/json" \
  -d '{"message":{"rid":"ROOM_ID","msg":"Hello from Clawdbot"}}' \
  "$RC_URL/api/v1/chat.sendMessage"

# Read recent messages
curl -s -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  "$RC_URL/api/v1/channels.messages?roomId=ROOM_ID&count=20"

# Edit message
curl -s -X POST -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  -H "Content-Type: application/json" \
  -d '{"roomId":"ROOM_ID","msgId":"MSG_ID","text":"Updated text"}' \
  "$RC_URL/api/v1/chat.update"

# Delete message
curl -s -X POST -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  -H "Content-Type: application/json" \
  -d '{"roomId":"ROOM_ID","msgId":"MSG_ID"}' \
  "$RC_URL/api/v1/chat.delete"

# Search messages
curl -s -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  "$RC_URL/api/v1/chat.search?roomId=ROOM_ID&searchText=keyword"

# React to message (toggle — calling again removes it)
curl -s -X POST -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  -H "Content-Type: application/json" \
  -d '{"messageId":"MSG_ID","emoji":"thumbsup"}' \
  "$RC_URL/api/v1/chat.react"

# Get message (includes reactions in message.reactions field)
curl -s -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  "$RC_URL/api/v1/chat.getMessage?msgId=MSG_ID"
```

## 固定消息（Pin）

```bash
# Pin a message
curl -s -X POST -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  -H "Content-Type: application/json" \
  -d '{"messageId":"MSG_ID"}' \
  "$RC_URL/api/v1/chat.pinMessage"

# Unpin a message
curl -s -X POST -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  -H "Content-Type: application/json" \
  -d '{"messageId":"MSG_ID"}' \
  "$RC_URL/api/v1/chat.unPinMessage"

# List pinned messages (query is URL-encoded {"pinned":true})
curl -s -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  "$RC_URL/api/v1/channels.messages?roomId=ROOM_ID&query=%7B%22pinned%22%3Atrue%7D"
```

## 用户

```bash
# List users
curl -s -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  "$RC_URL/api/v1/users.list"

# Get user info (by username or userId)
curl -s -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  "$RC_URL/api/v1/users.info?username=john"

curl -s -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  "$RC_URL/api/v1/users.info?userId=USER_ID"

# Create user (admin)
curl -s -X POST -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","name":"John","username":"john","password":"pass123"}' \
  "$RC_URL/api/v1/users.create"

# Set user status
curl -s -X POST -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  -H "Content-Type: application/json" \
  -d '{"message":"In a meeting","status":"busy"}' \
  "$RC_URL/api/v1/users.setStatus"
```

## 表情符号

```bash
# List custom emoji
curl -s -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  "$RC_URL/api/v1/emoji-custom.list"
```

## 集成

```bash
# List webhooks
curl -s -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  "$RC_URL/api/v1/integrations.list?type=webhook-incoming"

# Use incoming webhook (no auth needed)
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"text":"Alert from external system!"}' \
  "$RC_URL/hooks/WEBHOOK_ID/WEBHOOK_TOKEN"
```

## 统计数据

```bash
# Server statistics
curl -s -H "X-Auth-Token: $RC_TOKEN" -H "X-User-Id: $RC_USER_ID" \
  "$RC_URL/api/v1/statistics"
```

## 速率限制

默认限制：每位用户每秒 20 次请求。请查看请求头中的字段：`X-RateLimit-Limit` 和 `X-RateLimit-Remaining`。

## 可尝试的功能：

- 使用 `white_check_mark` 表示任务已完成
- 固定重要的决策或每周状态更新
- 在提问前搜索之前的讨论记录
- 创建特定于项目的频道并设置描述性标题
- 通过 `chat.postMessage` 以 `“channel”: “@username` 的方式给用户发送私信
- 使用未经认证的传入 WebHook 来接收外部系统的警报

如需完整文档，请参阅 [RocketChat API 文档](https://developer.rocket.chat/reference/api)。