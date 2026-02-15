---
name: xmtp-cli-sync
description: 使用 XMTP CLI 同步对话记录和消息。适用于同步部分对话或全部对话记录的情况。
license: MIT
metadata:
  author: xmtp
  version: "1.0.0"
---

# CLI 同步

用于同步对话记录和群组信息，或者同步所有对话记录及消息。

## 使用场景

- 同步特定对话记录（增量同步）
- 同步所有对话记录及消息（完全同步）

## 命令规则

- `sync-syncall`：同时执行 `sync` 和 `syncall` 命令

## 快速入门

```bash
# Sync conversations
xmtp sync

# Sync all conversations and messages
xmtp syncall
```

详情请参阅 `rules/sync-syncall.md` 文件。