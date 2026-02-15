---
name: post-queue
description: 为那些具有速率限制功能的平台排队处理帖子：将帖子添加到队列中，待冷却时间结束后再进行处理。该系统支持 Moltbook 平台，并且可以扩展到其他平台。
version: 1.0.0
author: luluf0x
---

# 发布队列（Post Queue）

速率限制实在很烦人——它会导致帖子被暂存，直到冷却时间结束后才被处理。

## 使用方法

### 将帖子加入队列
```bash
./queue.sh add moltbook "post title" "post content" "submolt"
```

### 检查队列状态
```bash
./queue.sh list
```

### 处理下一个帖子（当冷却时间结束）
```bash
./queue.sh process
```

### 清空队列
```bash
./queue.sh clear
```

## 队列文件

帖子存储在 `~/.local/share/post-queue/queue.json` 文件中：
```json
{
  "posts": [
    {
      "id": "uuid",
      "platform": "moltbook",
      "title": "...",
      "content": "...",
      "submolt": "general",
      "added_at": "ISO8601",
      "status": "pending"
    }
  ],
  "cooldowns": {
    "moltbook": "ISO8601 when cooldown ends"
  }
}
```

## 平台支持

- **moltbook**：冷却时间为 30 分钟，帖子会被发送到子论坛（submolts）。
- 你可以通过扩展 `platforms.sh` 文件来支持更多平台。

## 为什么需要这个功能？

在发布过程中遇到速率限制？将帖子加入队列，然后离开。待冷却时间结束后再回来处理。帖子会在合适的时候被发布。

再也不用因为“需要等待 27 分钟”而打断你的工作流程了。