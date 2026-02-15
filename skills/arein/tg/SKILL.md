---
name: tg
description: Telegram CLI（命令行工具）用于读取、搜索和发送消息。当用户需要查询Telegram消息、查看收件箱、搜索聊天记录、发送消息或查找联系人及群组时，可以使用该工具。
---

# Telegram CLI

这是一个快速的 Telegram 命令行工具，用于读取、搜索和发送消息。

## 使用场景

当用户需要执行以下操作时，可以使用此工具：
- 查看 Telegram 的消息或收件箱内容
- 在 Telegram 中搜索特定主题/关键词
- 向某人发送消息
- 了解 Telegram 的群组、联系人或聊天信息
- 查看未读消息
- 查找群组成员或管理员信息

## 安装

可以通过以下方式安装：
```bash
npm install -g @cyberdrk/tg
```

或者从源代码进行安装：
```bash
cd ~/Code/cyberdrk305/telegram && npm install && npm run build && npm link
```

## 认证

首次使用需要从 https://my.telegram.org/apps 获取 API 凭据。

```bash
tg auth
```

## 命令

### 读取消息
```bash
tg inbox                               # Unread messages summary
tg chats                               # List all chats
tg read "ChatName" -n 50               # Read last 50 messages
tg read "ChatName" --since "1h"        # Messages from last hour
tg read @username -n 20                # Read DM with user
tg search "query" --chat "ChatName"    # Search within chat
tg search "query" --all                # Search all chats
```

### 发送消息
```bash
tg send @username "message"            # Send DM
tg send "GroupName" "message"          # Send to group
tg reply "ChatName" 12345 "response"   # Reply to message ID
```

### 联系人与群组
```bash
tg contact @username                   # Get contact info
tg members "GroupName"                 # List group members
tg admins "GroupName"                  # List admins only
tg groups --admin                      # Groups where you're admin
```

### 状态信息
```bash
tg whoami                              # Show logged-in account
tg check                               # Verify session
```

## 输出格式

所有命令都支持使用 `--json` 选项，以结构化格式输出结果，便于进一步处理：

```bash
tg inbox --json                        # JSON format
tg read "Chat" --json                  # JSON with messages array
tg chats --json                        # JSON with chat list
```

## 示例

- 查看收件箱内容：
```bash
tg inbox
```

- 读取某个聊天中的最新消息：
```bash
tg read "MetaDAO Community" -n 20
```

- 搜索特定主题：
```bash
tg search "futarchy" --chat "MetaDAO"
```

- 发送消息：
```bash
tg send @username "Hello, checking in!"
```

## 注意事项

- 聊天名称可以部分匹配（例如，“MetaDAO”会匹配“MetaDAO Community”）
- 用户名必须以 @ 开头（例如 @username）
- 消息会按时间倒序返回（最新的消息在前面）
- `--since` 选项支持的时间格式包括 “1h”、“30m”、“7d” 等