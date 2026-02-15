---
name: beeper
description: 使用 beeper-cli 在 Beeper Desktop 中搜索聊天记录、查看/阅读消息以及发送消息。
metadata: {"clawdbot":{"requires":{"bins":["beeper"]}}}
---

# beeper

当您需要通过 **Beeper Desktop** 搜索聊天记录、查看/读取消息或发送消息时，请使用此技能。

## 功能简介
这是一个基于 Beeper Desktop API 的命令行工具（CLI）封装层。无需使用 MCP 或 curl，只需使用 `beeper` 命令即可完成操作。

**依赖项：** [beeper-cli](https://github.com/foeken/beeper-cli)

## 先决条件
- 确保 Beeper Desktop 已启用 API 功能（设置 > 开发者选项）
- 安装 [beeper-cli](https://github.com/foeken/beeper-cli)
- 设置环境变量 `BEEPER_ACCESS_TOKEN`（可在 Beeper Desktop 的设置 > 开发者 > API 访问令牌中获取）

## 安装 beeper-cli
您可以从 [releases](https://github.com/foeken/beeper-cli/releases) 下载 beeper-cli，或自行编译安装：

```bash
go install github.com/foeken/beeper-cli@latest
```

## 命令列表

### 账户操作
```bash
beeper accounts list
beeper accounts list -o table
```

### 聊天记录操作
```bash
# List all chats (sorted by last activity)
beeper chats list

# Search chats
beeper chats search --query "John"
beeper chats search --query "project" --type group

# Get specific chat
beeper chats get "<chatID>"

# Archive
beeper chats archive "<chatID>"

# Create
beeper chats create --account-id "telegram:123" --participant "user1" --type dm

# Reminders
beeper chats reminders create "<chatID>" --time "2025-01-26T10:00:00Z"
beeper chats reminders delete "<chatID>"
```

### 消息操作
```bash
# List messages in a chat
beeper messages list "<chatID>"

# Search messages
beeper messages search --query "dinner"
beeper messages search --query "dinner" --limit 10
beeper messages search --query "meeting" --sender me
beeper messages search --query "budget" --after "2025-01-01T00:00:00Z"
beeper messages search --chat-ids "<chatID>" --media-type image

# Send a message
beeper messages send "<chatID>" "Hello!"

# Send with reply
beeper messages send "<chatID>" "Thanks!" --reply-to "<messageID>"

# Edit a message
beeper messages edit "<chatID>" "<messageID>" "Corrected text"
```

### 附件操作
```bash
# Upload a file
beeper assets upload /path/to/image.png

# Download an asset
beeper assets download "mxc://beeper.local/abc123" --output /path/to/save.jpg

# Send with attachment (upload first)
beeper assets upload /path/to/photo.jpg  # returns uploadID
beeper messages send "<chatID>" "Check this!" --upload-id "<uploadID>"
```

### 其他操作
```bash
# Focus Beeper window
beeper focus
beeper focus --chat-id "<chatID>"

# Global search
beeper search "important"
```

## 输出格式
```bash
beeper chats list -o json   # default
beeper chats list -o table  # human-readable
```

## 使用流程
1. 查找聊天记录：`beeper chats search --query "名称"`
2. 查看消息：`beeper messages list "<chatID>"`
3. 搜索特定内容：`beeper messages search --query "关键词"`
4. 发送消息：`beeper messages send "<chatID>" "消息内容"`

## 安全提示
- 请妥善保管 `BEEPER_ACCESS_TOKEN`（建议使用密码管理工具进行存储）。
- 在引用消息内容时，仅包含必要的信息。
- 除非另有说明，否则在发送消息前请先确认消息内容是否正确。