---
name: feishu-memory-recall
version: 2.0.0
description: OpenClaw Feishu代理的跨组内存、搜索和事件共享功能
tags: [feishu, memory, cross-session, search, digest]
---

# Feishu 记忆回溯功能

该功能支持 OpenClaw 在不同组之间的信息共享，包括搜索消息、生成摘要以及在所有 Feishu 组和私信中分享事件。

## 命令

| 命令 | 描述 |
|---|---|
| `recall --user <id> [--hours 24]` | 在所有组中查找指定用户的消息 |
| `search --keyword <text> [--hours 24]` | 按关键词在所有组中搜索消息 |
| `digest [--hours 6]` | 显示所有被跟踪组的活动摘要 |
| `log-event -s <source> -e <text>` | 将事件记录到 `RECENT_events.md` 文件以及每日日志中 |
| `sync-groups` | 从网关会话中自动发现新的组 |
| `add-group -i <id> -n <name>` | 手动添加一个组到跟踪列表 |
| `list-groups` | 显示所有被跟踪的组 |

## 使用方法

```bash
# Search for "GIF error" across all groups
node skills/feishu-memory-recall/index.js search -k "GIF" --hours 12

# What happened in all groups in the last 6 hours?
node skills/feishu-memory-recall/index.js digest --hours 6

# Log a cross-session event
node skills/feishu-memory-recall/index.js log-event -s "dev-group" -e "Fixed GIF crash in gateway"

# Auto-discover all Feishu groups from gateway sessions
node skills/feishu-memory-recall/index.js sync-groups

# Find what a specific user said recently
node skills/feishu-memory-recall/index.js recall -u ou_cdc63fe05e88c580aedead04d851fc04 --hours 48
```

## 工作原理

1. **sync-groups**: 读取 `~/.openclaw/agents/main/sessions/sessions.json` 文件，自动识别代理连接的 Feishu 组。
2. **search/recall/digest**: 调用 Feishu API 从被跟踪的组中获取消息，并根据关键词、用户或时间进行过滤。
3. **log-event**: 将事件记录到 `RECENT_events.md`（24 小时跨会话的事件记录）和 `memory/YYYY-MM-DD.md`（永久性每日日志）文件中。

## 配置要求

需要在 `.env` 文件中配置 Feishu 的认证信息：
```
FEISHU_APP_ID=cli_xxxxx
FEISHU_APP_SECRET=xxxxx
```

组列表存储在 `memory/active_groups.json` 文件中，可以通过 `sync-groups` 命令自动更新。