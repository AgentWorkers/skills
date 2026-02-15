---
name: xmtp-cli-list
description: 列出 XMTP CLI 中的对话记录、成员信息以及消息内容。适用于查看或查找特定对话时使用。
license: MIT
metadata:
  author: xmtp
  version: "1.0.0"
---

# CLI 功能列表

该 CLI 可用于列出对话记录、成员信息以及消息内容，或根据地址或收件箱 ID 查找特定的对话。

## 使用场景

- 列出对话记录、对话中的成员信息或消息内容
- 根据地址或收件箱 ID 查找特定的对话

## 使用规则

- `conversations-members-messages`：用于列出对话记录（`list conversations`）、对话成员（`members`）或消息内容（`messages`），并支持相关选项
- `find`：用于根据地址或收件箱 ID 查找特定的对话记录（`list find`）

## 快速入门

```bash
xmtp list conversations
xmtp list members --conversation-id <id>
xmtp list messages --conversation-id <id>
xmtp list find --address 0x1234...
```

详情请参阅 `rules/conversations-members-messages.md` 和 `rules/find.md` 文件。